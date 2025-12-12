from dataclasses import dataclass
from typing import List

from savethewench.data import Weapons
from savethewench.model.base import WeaponBase


@dataclass
class Weapon(WeaponBase):
    name: str
    damage: int
    uses: int
    accuracy: float
    spread: int
    crit: float
    cost: int
    sell_value: int
    type: str


def load_weapon(name: str) -> Weapon:
    matches = load_weapons([name])
    if len(matches) == 0:
        raise ValueError(f"Could not find weapon data for {name}")
    return matches[0]


def load_weapons(restriction: List[str] = None):
    return [Weapon(**d) for d in Weapons if restriction is None or d['name'] in restriction]


def load_discoverable_weapons():
    return [w for w in load_weapons() if w.uses > 0]