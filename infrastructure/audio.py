import base64

import pygame as pg

from pathlib import Path

MIME_TYPES = {'.wav': 'audio/wav', '.ogg': 'audio/ogg', '.mp3': 'audio/mpeg'}


def _data_uri(path):
    mime = MIME_TYPES.get(path.suffix.lower(), 'application/octet-stream')
    encoded = base64.b64encode(path.read_bytes()).decode('ascii')
    return f'data:{mime};base64,{encoded}'


class SilentClip:
    def play(self):
        return None

    def set_volume(self, volume):
        return None


class Sound:
    def __init__(self, game, sound_loader=None, music_loader=None):
        self.game = game
        pg.mixer.init()
        sound_loader = sound_loader or pg.mixer.Sound
        music_loader = music_loader or pg.mixer.music.load
        self.path = game.theme.resource_dir / 'sound'
        self.shotgun = self._load(sound_loader, game.theme.fire_sound)
        self.npc_pain = self._load(sound_loader, 'npc_pain.wav')
        self.npc_death = self._load(sound_loader, 'npc_death.wav')
        self.npc_shot = self._load(sound_loader, 'npc_attack.wav')
        self.npc_shot.set_volume(0.2)
        self.player_pain = self._load(sound_loader, 'player_pain.wav')
        try:
            # pg.mixer.music.load() always returns None on success (per pygame's own
            # docs), so the return value can't signal success -- track it explicitly.
            music_loader(self._resolve('theme.mp3'))
            self.theme = True
        except (FileNotFoundError, OSError, pg.error):
            self.theme = None
        pg.mixer.music.set_volume(0.3)

    def play_theme(self):
        if self.theme is not None:
            pg.mixer.music.play(-1)

    def stop_theme(self):
        pg.mixer.music.stop()

    def _resolve(self, filename):
        ogg_path = self.path / (Path(filename).stem + '.ogg')
        return ogg_path if ogg_path.is_file() else self.path / filename

    def _load(self, sound_loader, filename):
        try:
            return sound_loader(self._resolve(filename))
        except (FileNotFoundError, OSError, pg.error):
            return SilentClip()


class BrowserClip:
    """Pool of pre-loaded HTML5 Audio elements. Cloning+decoding a fresh node on every
    play() was too slow to keep up with rapid-fire triggers, causing missed/late sounds;
    round-robining a small pool of already-decoded elements plays back reliably instead."""

    POOL_SIZE = 4

    def __init__(self, document, path, volume=1.0):
        self._volume = volume
        self._pool = []
        self._next = 0
        if path.is_file():
            src = _data_uri(path)
            for _ in range(self.POOL_SIZE):
                clip = document.createElement('audio')
                clip.src = src
                clip.volume = volume
                clip.load()
                self._pool.append(clip)

    def play(self):
        if not self._pool:
            return
        clip = self._pool[self._next]
        self._next = (self._next + 1) % len(self._pool)
        clip.currentTime = 0
        clip.play()

    def set_volume(self, volume):
        self._volume = volume
        for clip in self._pool:
            clip.volume = volume


class BrowserSound:
    """Web build audio backend: plays clips through the browser's own Audio API,
    since pygame's WASM mixer plays back the wrong or garbled sound content."""

    def __init__(self, game):
        import platform
        document = platform.document
        self.game = game
        self.path = game.theme.resource_dir / 'sound'
        self.shotgun = self._clip(document, game.theme.fire_sound)
        self.npc_pain = self._clip(document, 'npc_pain.wav')
        self.npc_death = self._clip(document, 'npc_death.wav')
        self.npc_shot = self._clip(document, 'npc_attack.wav')
        self.npc_shot.set_volume(0.2)
        self.player_pain = self._clip(document, 'player_pain.wav')
        self.theme = None
        self._theme_requested = False
        self._theme_started = False
        theme_path = self._resolve('theme.mp3')
        if theme_path.is_file():
            self.theme = document.createElement('audio')
            self.theme.src = _data_uri(theme_path)
            self.theme.loop = True
            self.theme.volume = 0.3
            self.theme.load()

    def play_theme(self):
        self._theme_requested = True
        self.ensure_theme_started()

    def stop_theme(self):
        if self.theme is not None:
            self.theme.pause()
            self.theme.currentTime = 0
        self._theme_started = False

    def ensure_theme_started(self):
        if self.theme is None or not self._theme_requested:
            return
        if self._theme_started and not self.theme.paused:
            return
        try:
            self.theme.play()
            # Some browsers reject play() asynchronously; only mark started when
            # the element actually leaves paused state.
            self._theme_started = not self.theme.paused
        except Exception:
            # Browsers may block autoplay before gesture; retry on next input event.
            self._theme_started = False

    def _resolve(self, filename):
        ogg_path = self.path / (Path(filename).stem + '.ogg')
        return ogg_path if ogg_path.is_file() else self.path / filename

    def _clip(self, document, filename):
        return BrowserClip(document, self._resolve(filename))
