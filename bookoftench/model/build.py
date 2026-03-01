from dataclasses import dataclass
from typing import List

from bookoftench.model.item import Item
from bookoftench.model.perk import Perk
from bookoftench.model.weapon import Weapon
from bookoftench.ui import dim, green, yellow, red, cyan, orange, purple


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
        header = f"{orange(self.name)}"
        values = dim(' | ').join([
            f"{'HP:':<4}{green(self.hp):<3}",
            f"Strength: {yellow(f'{self.str:<3}')}",
            f"Accuracy: {yellow(f'{self.acc:<3}')}",
            f"Coins: {green(f'{self.coins:<3}')}"
        ])

        items = dim(', ').join(f"{green(p.name)}" for p in self.items)
        weapons = dim(', ').join(f"{red(p.name)}" for p in self.weapons)
        perks_str = dim(', ').join(f"{purple(p.name)}" for p in self.perks)

        return "\n".join([
            header,
            values,
            f"  {cyan('Items')} {dim('|')} {items}",
            f"{cyan('Weapons')} {dim('|')} {weapons}",
            f"  {cyan('Perks')} {dim('|')} {perks_str}",
            f"  {cyan('Notes')} {dim('|')} {self.notes}",
            "\n",
        ])
