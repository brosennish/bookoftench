from dataclasses import dataclass
from typing import List

from bookoftench.data.builds import Builds
from bookoftench.model.illness import Illness
from bookoftench.model.item import Item
from bookoftench.model.perk import Perk
from bookoftench.model.weapon import Weapon
from bookoftench.ui import dim, green, yellow, red, cyan, orange, purple, blue


@dataclass
class Build:
    notes: str | None
    illness: Illness | None
    name: str
    lives: int
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
            f"Lives: {cyan(self.lives)}",
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
                f"{'Illness'}  {dim('|')} {yellow(self.illness.name)}",
                f"{'Items'}    {dim('|')} {items}",
                f"{'Weapons'}  {dim('|')} {weapons}",
                f"{'Perks'}    {dim('|')} {perks_str}",
                f"{'Notes'}    {dim('|')} {blue(f"{self.notes}")}",
                "\n",
            ])
        else:
            return "\n".join([
                header,
                values,
                f"{'Items'}    {dim('|')} {items}",
                f"{'Weapons'}  {dim('|')} {weapons}",
                f"{'Perks'}    {dim('|')} {perks_str}",
                f"{'Notes'}    {dim('|')} {blue(f"{self.notes}")}",
                "\n",
            ])

def load_builds(restriction: List[str] = None):
    return [Build(**d) for d in Builds if restriction is None or d['name'] in restriction]