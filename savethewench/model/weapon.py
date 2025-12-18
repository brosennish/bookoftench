from dataclasses import dataclass
from typing import List

from savethewench.data import Weapons
from savethewench.model.base import WeaponBase, Buyable
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

    def to_sellable_weapon(self):
        return SellableWeapon(**vars(self))

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<24}"),
            f"{f"Cost: {orange(self.cost)}":<24}",
            f"{f"DMG: {red(self.damage)}":<16}",
            f"{f"ACC: {yellow(self.accuracy)}":<18}",
            f"Uses: {self.uses}"
        ])


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
