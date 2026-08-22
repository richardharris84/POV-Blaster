from pathlib import Path
from typing import Any, Protocol

import pygame as pg


class ImageLoader(Protocol):
    def __call__(self, path: Path, size=None, alpha=True, fallback_label='?') -> pg.Surface:
        ...


class AssetLoaderPort(Protocol):
    def load_image(self, path: Path, size=None, alpha=True, fallback_label='?') -> pg.Surface:
        ...


class AudioClip(Protocol):
    def play(self) -> None:
        ...


class AudioOutput(Protocol):
    shotgun: AudioClip
    npc_pain: AudioClip
    npc_death: AudioClip
    npc_shot: AudioClip
    player_pain: AudioClip


class InputPort(Protocol):
    def poll(self) -> list[Any]:
        ...


class Renderer(Protocol):
    def draw(self, snapshot=None) -> None:
        ...

    def win(self) -> None:
        ...

    def game_over(self) -> None:
        ...

    def player_damage(self) -> None:
        ...


class GameContext(Protocol):
    player_name: str
    theme: Any
    screen: pg.Surface
    map: Any
    player: Any
    object_renderer: Renderer
    raycasting: Any
    object_handler: Any
    weapon: Any
    sound: AudioOutput
    pathfinding: Any
    asset_loader: AssetLoaderPort
    delta_time: int
    mouse_active: bool
    global_trigger: bool

    def set_state(self, state: str) -> None:
        ...
