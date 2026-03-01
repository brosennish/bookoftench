from dataclasses import dataclass
from typing import List

from bookoftench.model.illness import Illness
from bookoftench.model.item import Item
from bookoftench.model.perk import Perk
from bookoftench.model.weapon import Weapon
from bookoftench.ui import dim, green, yellow, red, cyan, orange, purple


@dataclass
class Build:
    notes: str | None
    illness: Illness | None
    name: str
    hp: int
    str: float
    acc: float
    coins: int
    items: List[Item]
    weapons: List[Weapon]
    perks: List[Perk]

    def __repr__(self) -> str:
        spacing = " " if self.hp < 100 else ""

        header = f"{orange(self.name)}\n"
        values = dim(' | ').join([
            f"HP: {green(self.hp)}{spacing}",
            f"Strength: {yellow(f'{self.str:<3}')}",
            f"Accuracy: {yellow(f'{self.acc:<3}')}",
            f"Coins: {green(f'{self.coins:<3}')}\n"
        ])

        items = dim(', ').join(f"{green(p.name)}" for p in self.items)
        weapons = dim(', ').join(f"{red(p.name)}" for p in self.weapons)
        perks_str = dim(', ').join(f"{purple(p.name)}" for p in self.perks)

        if self.illness:
            return "\n".join([
                header,
                values,
                f"{cyan('Illness')} {dim('|')} {yellow(self.illness.name)}",
                f"{cyan('Items')}   {dim('|')} {items}",
                f"{cyan('Weapons')} {dim('|')} {weapons}",
                f"{cyan('Perks')}   {dim('|')} {perks_str}",
                f"{cyan('Notes')}   {dim('|')} {self.notes}",
                "\n",
            ])
        else:
            return "\n".join([
                header,
                values,
                f"{cyan('Items')}   {dim('|')} {items}",
                f"{cyan('Weapons')} {dim('|')} {weapons}",
                f"{cyan('Perks')}   {dim('|')} {perks_str}",
                f"{cyan('Notes')}   {dim('|')} {self.notes}",
                "\n",
            ])