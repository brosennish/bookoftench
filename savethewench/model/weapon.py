import random
from dataclasses import dataclass, field
from typing import List

from savethewench.data import Weapons
from savethewench.data.perks import BULLETPROOF
from savethewench.data.weapons import PISTOL, REVOLVER, RIFLE, SHOTGUN
from savethewench.model.base import WeaponBase, Buyable
from savethewench.model.perk import attach_perk
from savethewench.ui import dim, cyan, orange, red, yellow


@dataclass
class Weapon(WeaponBase, Buyable):
    name: str
    damage: int
    uses: int
    accuracy: float
    spread: int
    crit: float
    cost: int
    sell_value: int
    type: str

    blind_effect: float = 0.0
    blind_turns_min: int = 0
    blind_turns_max: int = 0

    def _is_gun(self):
        return self.name in (PISTOL, REVOLVER, RIFLE, SHOTGUN)

    def calculate_base_damage_no_perk(self) -> int:
        return super().calculate_base_damage()

    def calculate_base_damage(self) -> int:
        base_damage = self.calculate_base_damage_no_perk()

        @attach_perk(BULLETPROOF, value_description="enemy bullet damage",
                     condition=lambda: self._is_gun())
        def apply_perks():
            return base_damage

        return int(apply_perks())

    def get_blind_effect(self) -> float:
        return self.blind_effect

    def get_blind_turns(self) -> int:
        return random.randint(self.blind_turns_min, self.blind_turns_max)

    def to_sellable_weapon(self):
        return SellableWeapon(**vars(self))

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<24}"),
            f"{f"Cost: {orange(self.cost)}":<24}",
            f"{f"DMG: {red(self.damage)}":<16}",
            f"{f"ACC: {yellow(self.accuracy)}":<18}",
            f"Uses: {self.format_uses()}"
        ])


@dataclass
class SellableWeapon(Weapon):
    _sell_value: int = field(init=False)

    def __post_init__(self):
        self._sell_value = self.sell_value

    @property
    def sell_value(self):
        max_uses = load_weapon(self.name).uses  # TODO optimize out object construction overhead
        if max_uses == -1:
            return self._sell_value

        proportion = self.uses / max_uses
        price = self._sell_value * proportion
        return max(int(price), 1)

    @sell_value.setter
    def sell_value(self, value):
        self._sell_value = value

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<24}"),
            f"{f"Value: {orange(self.sell_value)}":<24}",
            f"{f"DMG: {red(self.damage)}":<16}",
            f"{f"ACC: {yellow(self.accuracy)}":<18}",
            f"Uses: {self.uses}"
        ])


def load_weapon(name: str) -> Weapon:
    matches = load_weapons([name])
    if len(matches) == 0:
        raise ValueError(f"Could not find weapon data for {name}")
    return matches[0]


def load_weapons(restriction: List[str] = None):
    return [Weapon(**d) for d in Weapons if restriction is None or d['name'] in restriction]


def load_discoverable_weapons():
    return [w for w in load_weapons() if w.uses > 0]
