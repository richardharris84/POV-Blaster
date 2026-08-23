from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree


@dataclass(frozen=True)
class Score:
    player_name: str
    kills: int


class HighScores:
    def __init__(self, path='scores.xml', limit=10):
        self.path = Path(path)
        self.limit = limit
        if not self.path.exists():
            self._save([])

    def load(self):
        if not self.path.exists():
            return []
        try:
            root = ElementTree.parse(self.path).getroot()
        except (ElementTree.ParseError, OSError):
            return []

        scores = []
        for entry in root.findall('score'):
            name = entry.get('name', '').strip()
            try:
                kills = int(entry.get('kills', '0'))
            except ValueError:
                continue
            if name and kills >= 0:
                scores.append(Score(name, kills))
        return self._sort(scores)

    def add(self, player_name, kills):
        scores = self.load()
        scores.append(Score(player_name.strip() or 'Player', max(0, int(kills))))
        scores = self._sort(scores)[:self.limit]
        self._save(scores)
        return scores

    def _sort(self, scores):
        return sorted(scores, key=lambda score: (-score.kills, score.player_name.casefold()))
    def _save(self, scores):
        root = ElementTree.Element('scores')
        for score in scores:
            ElementTree.SubElement(root, 'score', name=score.player_name, kills=str(score.kills))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        ElementTree.ElementTree(root).write(self.path, encoding='utf-8', xml_declaration=True)

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

    def __init__(self, limit=10):
        self.limit = limit
        self._memory = []

    def load(self):
        try:
            import json
            import platform
            stored = platform.window.localStorage.getItem(self.storage_key)
            if stored:
                return self._sort([Score(item['player_name'], int(item['kills'])) for item in json.loads(stored)])
        except (AttributeError, ImportError, KeyError, TypeError, ValueError):
            pass
        return list(self._memory)

    def add(self, player_name, kills):
        scores = self._sort(self.load() + [Score(player_name.strip() or 'Player', max(0, int(kills)))])[:self.limit]
        self._memory = scores
        try:
            import json
            import platform
            platform.window.localStorage.setItem(
                self.storage_key,
                json.dumps([score.__dict__ for score in scores]),
            )
        except (AttributeError, ImportError):
            pass
        return scores

    def _sort(self, scores):
        return sorted(scores, key=lambda score: (-score.kills, score.player_name.casefold()))
