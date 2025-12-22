import random
from dataclasses import dataclass
from typing import List

from savethewench.data import Weapons
from savethewench.data.perks import BULLETPROOF
from savethewench.data.weapons import PISTOL, REVOLVER, RIFLE, SHOTGUN
from savethewench.model.base import WeaponBase, Buyable
from savethewench.model.perk import attach_perk_conditional

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

    def calculate_base_damage(self) -> int:
        base_damage = super().calculate_base_damage()
        @attach_perk_conditional(BULLETPROOF, value_description="enemy bullet damage",
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
        return f"{cyan(f"{self.name:<24}")}\n{dim(' | ').join([
            f"{f"Cost: {orange(self.cost)}":<24}",
            f"{f"DMG: {red(self.damage)}":<16}",
            f"{f"ACC: {yellow(self.accuracy)}":<18}",
            f"Uses: {self.format_uses()}"
        ])}"


@dataclass
class SellableWeapon(Weapon):
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
