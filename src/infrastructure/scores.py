from contextlib import closing
from dataclasses import dataclass
import json
import os
import sqlite3
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_SCORE_PATH = Path(__file__).resolve().parents[2] / 'data' / 'scores.sqlite3'


@dataclass(frozen=True)
class Score:
    player_name: str
    kills: int


class HighScores:
    def __init__(self, path=DEFAULT_SCORE_PATH, limit=10):
        self.path = Path(path)
        self.limit = limit
        self._initialize()

    def load(self):
        with closing(sqlite3.connect(self.path)) as connection:
            rows = connection.execute(
                'SELECT player_name, kills FROM scores ORDER BY kills DESC, player_name COLLATE NOCASE ASC, id ASC'
            ).fetchall()
        return [Score(name, kills) for name, kills in rows]

    def add(self, player_name, kills):
        score = Score(player_name.strip() or 'Player', max(0, int(kills)))
        with closing(sqlite3.connect(self.path)) as connection:
            with connection:
                connection.execute(
                    'INSERT INTO scores (player_name, kills) VALUES (?, ?)',
                    (score.player_name, score.kills),
                )
                connection.execute(
                    'DELETE FROM scores WHERE id NOT IN ('
                    'SELECT id FROM scores ORDER BY kills DESC, player_name COLLATE NOCASE ASC, id ASC LIMIT ?)',
                    (self.limit,),
                )
        return self.load()

    def sync(self, api_url, direction='push'):
        """Synchronize local scores with the API in the requested direction."""
        api_url = api_url.rstrip('/')
        if direction == 'push':
            for score in self.load():
                self._post_remote(api_url, score)
            return self.load()
        if direction == 'pull':
            remote_scores = self._get_remote(api_url)
            with closing(sqlite3.connect(self.path)) as connection:
                with connection:
                    connection.execute('DELETE FROM scores')
                    connection.executemany(
                        'INSERT INTO scores (player_name, kills) VALUES (?, ?)',
                        [(score.player_name, score.kills) for score in remote_scores[:self.limit]],
                    )
            return self.load()
        raise ValueError("direction must be 'push' or 'pull'")

    def _sort(self, scores):
        return sorted(scores, key=lambda score: (-score.kills, score.player_name.casefold()))

    def _initialize(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.path)) as connection:
            with connection:
                connection.execute(
                    'CREATE TABLE IF NOT EXISTS scores ('
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                    'player_name TEXT NOT NULL, kills INTEGER NOT NULL CHECK (kills >= 0))'
                )

    def _get_remote(self, api_url):
        request = Request(f'{api_url}/scores', headers={'User-Agent': 'POV-Blaster/1.0'})
        try:
            with urlopen(request, timeout=3) as response:
                data = json.loads(response.read().decode('utf-8'))
        except (HTTPError, URLError, OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            raise RuntimeError('Unable to pull scores from the remote API.') from error
        return self._sort([Score(item['player_name'], int(item['kills'])) for item in data])

    def _post_remote(self, api_url, score):
        payload = json.dumps(score.__dict__).encode('utf-8')
        request = Request(
            f'{api_url}/scores', data=payload,
            headers={'Content-Type': 'application/json'}, method='POST',
        )
        try:
            with urlopen(request, timeout=3):
                pass
        except (HTTPError, URLError, OSError) as error:
            raise RuntimeError('Unable to push scores to the remote API.') from error

    def display(self, output_func=print):
        scores = self.load()
        output_func('')
        output_func('Top 10 Scores:')
        if not scores:
            output_func('No scores yet.')
            return scores
        for index, score in enumerate(scores, start=1):
            output_func(f'{index}) {score.player_name} - {score.kills} kills')
        return scores


class BrowserHighScores:
    storage_key = 'pov-blaster-high-scores'

    def __init__(self, limit=10, api_url=None):
        self.limit = limit
        self.api_url = (api_url if api_url is not None else os.environ.get('POV_BLASTER_API_URL', '')).rstrip('/')
        self._memory = []

    def load(self):
        # Try to fetch from remote API first
        if self.api_url:
            try:
                scores = self._load_remote()
                if scores:
                    self._memory = scores
                    return self._sort(scores)
            except Exception:
                pass
        
        # Fall back to local storage
        try:
            import platform
            stored = platform.window.localStorage.getItem(self.storage_key)
            if stored:
                return self._sort([Score(item['player_name'], int(item['kills'])) for item in json.loads(stored)])
        except (AttributeError, ImportError, KeyError, TypeError, ValueError):
            pass
        return list(self._memory)

    def add(self, player_name, kills):
        score = Score(player_name.strip() or 'Player', max(0, int(kills)))
        scores = self._sort(self.load() + [score])[:self.limit]
        self._memory = scores
        self._save_local(scores)
        self._submit_remote(score)
        return scores

    def record_session(self, player_name):
        """Record a web session when a player joins the game."""
        if not self.api_url:
            return
        player_name = player_name.strip() or 'Player'
        payload = json.dumps({'player_name': player_name}).encode('utf-8')
        try:
            import platform
            platform.window.fetch(
                f'{self.api_url}/sessions',
                {'method': 'POST', 'headers': {'Content-Type': 'application/json'}, 'body': payload.decode('utf-8')},
            )
            return
        except (AttributeError, ImportError, TypeError):
            pass
        try:
            request = Request(
                f'{self.api_url}/sessions',
                data=payload,
                headers={'Content-Type': 'application/json'},
                method='POST',
            )
            with urlopen(request, timeout=3):
                pass
        except OSError:
            pass

    def _load_remote(self):
        """Load scores from the remote API."""
        try:
            request = Request(f'{self.api_url}/scores', headers={'User-Agent': 'POV-Blaster/1.0'})
            with urlopen(request, timeout=3) as response:
                payload = response.read().decode('utf-8')
            data = json.loads(payload)
            return [Score(item['player_name'], int(item['kills'])) for item in data]
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            return None

    def _save_local(self, scores):
        try:
            import platform
            platform.window.localStorage.setItem(
                self.storage_key,
                json.dumps([score.__dict__ for score in scores]),
            )
        except (AttributeError, ImportError):
            pass

    def _submit_remote(self, score):
        if not self.api_url:
            return
        payload = json.dumps(score.__dict__).encode('utf-8')
        try:
            import platform
            platform.window.fetch(
                f'{self.api_url}/scores',
                {'method': 'POST', 'headers': {'Content-Type': 'application/json'}, 'body': payload.decode('utf-8')},
            )
            return
        except (AttributeError, ImportError, TypeError):
            pass
        try:
            request = Request(
                f'{self.api_url}/scores',
                data=payload,
                headers={'Content-Type': 'application/json'},
                method='POST',
            )
            with urlopen(request, timeout=3):
                pass
        except OSError:
            pass

    def _sort(self, scores):
        return sorted(scores, key=lambda score: (-score.kills, score.player_name.casefold()))
