from dataclasses import dataclass


@dataclass
class Health:
    maximum: int
    current: int

    @classmethod
    def full(cls, maximum: int) -> 'Health':
        return cls(maximum=maximum, current=maximum)

    def damage(self, amount: int) -> int:
        self.current = max(0, self.current - max(0, amount))
        return self.current

    def recover(self, amount: int = 1) -> int:
        self.current = min(self.maximum, self.current + max(0, amount))
        return self.current

    @property
    def depleted(self) -> bool:
        return self.current == 0
