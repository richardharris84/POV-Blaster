from dataclasses import dataclass

from domain.health import Health


@dataclass
class Combatant:
    health: Health
    attack_damage: int
    accuracy: float

    @classmethod
    def create(cls, maximum_health: int, attack_damage: int, accuracy: float) -> 'Combatant':
        return cls(Health.full(maximum_health), attack_damage, accuracy)

    def take_damage(self, amount: int) -> int:
        return self.health.damage(amount)

    def attack_hits(self, roll: float) -> bool:
        return 0 <= roll < self.accuracy

    @property
    def defeated(self) -> bool:
        return self.health.depleted
