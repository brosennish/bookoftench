from dataclasses import dataclass
from typing import List

from bookoftench.model.item import Item
from bookoftench.model.perk import Perk
from bookoftench.model.weapon import Weapon


@dataclass
class Build:
    notes: str | None
    name: str
    hp: int
    str: float
    acc: float
    coins: int
    items: List[Item]
    weapons: List[Weapon]
    perks: List[Perk]
