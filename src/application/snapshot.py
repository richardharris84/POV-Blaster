from dataclasses import dataclass


@dataclass(frozen=True)
class RenderSnapshot:
    objects: tuple = ()
    player_position: tuple = (0.0, 0.0)
    player_angle: float = 0.0
    player_health: int = 0
