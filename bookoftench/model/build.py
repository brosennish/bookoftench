from dataclasses import dataclass
from typing import List

from bookoftench.model.item import Item
from bookoftench.model.perk import Perk
from bookoftench.model.weapon import Weapon
from bookoftench.ui import dim, green, yellow, red


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


    def __repr__(self) -> str:
        header = f"{self.name}"

        values = dim(' | ').join([
            f"HP: {green(self.hp):<3}",
            f"Strength: {red(f'{self.str:<3}')}",
            f"Accuracy: {yellow(f'{self.acc:<3}')}",
            f"Coins: {green(f'{self.coins:<3}')}",
        ])

        items = dim(', ').join(i.name for i in self.items)
        weapons = dim(', ').join(w.name for w in self.weapons)
        perks = dim(', ').join(p.name for p in self.perks)

        return "\n".join([
            header,
            values,
            f"Items: {items}",
            f"Weapons: {weapons}",
            f"Perks: {perks}",
            f"Notes: {self.notes}",
        ])
