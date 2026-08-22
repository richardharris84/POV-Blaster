from dataclasses import dataclass


@dataclass
class GameState:
    name: str = 'playing'
    time_remaining: int = 0

    def set(self, name: str, duration: int = 1500) -> None:
        self.name = name
        self.time_remaining = duration

    def advance(self, delta_time: int) -> bool:
        if self.name == 'playing':
            return False
        self.time_remaining -= delta_time
        return self.time_remaining <= 0
