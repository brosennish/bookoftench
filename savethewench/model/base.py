import random
from abc import ABC
from dataclasses import dataclass


@dataclass
class AttackResult:
    success: bool
    critical: bool
    damage: int


@dataclass
class WeaponBase:
    name: str
    damage: int
    uses: int
    accuracy: float
    spread: int
    crit: float


@dataclass
class Combatant(ABC):
    hp: int
    current_weapon: WeaponBase

    blind: bool = False
    blinded_by: str = ''
    blind_effect: float = 0.0
    blind_turns: int = 0

    def __post_init__(self):
        self.blind = False
        self.blinded_by = ""
        self.blind_effect = 0.0
        self.blind_turns = 0

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, damage: int) -> int:
        self.hp -= damage
        return damage

    def calculate_accuracy(self) -> float:
        return self.current_weapon.accuracy

    def calculate_base_damage(self) -> int:
        weapon = self.current_weapon
        base = weapon.damage + random.randint(-weapon.spread, weapon.spread)  # Base damage +/- 10
        return max(5, base)  # Damage >= 5

    def get_crit_chance(self) -> float:
        return self.current_weapon.crit

    def attack(self, other: "Combatant") -> AttackResult:
        if random.random() > self.calculate_accuracy():
            return AttackResult(False, False, 0)
        # TODO Critical hit
        base_damage = self.calculate_base_damage()
        crit = random.random() < self.get_crit_chance()
        dmg = base_damage * 2 if crit else base_damage  # 2x damage if crit, otherwise dmg after spread
        damage_inflicted = other.take_damage(dmg)
        return AttackResult(True, crit, damage_inflicted)
