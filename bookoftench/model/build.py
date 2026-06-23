from dataclasses import dataclass
from typing import List

from bookoftench.data.builds import Builds, BRO
from bookoftench.model.illness import Illness
from bookoftench.model.item import Item
from bookoftench.model.perk import Perk
from bookoftench.model.weapon import Weapon
from bookoftench.ui import dim, green, yellow, red, cyan, orange, purple, blue

# ================================================================================================

@dataclass
class Build:
    notes: str | None
    illness: Illness | None
    name: str
    label: str
    lives: int
    lvl: int
    hp: int
    str: float
    acc: float
    coins: int
    luck: float | int
    fishing_lvl: int
    rod_lvl: int
    items: List[Item]
    weapons: List[Weapon]
    perks: List[Perk]

    def __repr__(self) -> str:
        row_1 = dim(' | ').join([
            f"{'Lvl: ':<11}{cyan(f'{self.lvl:<3}')}",
            f"{'Lives: ':<11}{yellow(f'{self.lives:<3}')}",
            f"{'HP: ':<11}{green(f'{self.hp:<3}')}",
            f"{'Strength: ':<11}{red(f'{self.str:<4g}')}",
            f"{'Accuracy: ':<11}{yellow(f'{self.acc:<4g}')}",
        ])

        row_2 = dim(' | ').join([
            f"{'Luck: ':<11}{purple(f'{self.luck:<3}')}",
            f"{'Fishing: ':<11}{blue(f'{self.fishing_lvl:<3}')}",
            f"{'Rod: ':<11}{cyan(f'{self.rod_lvl:<3}')}",
            f"{'Coins: ':<11}{green(f'{self.coins:<3}')}",
        ])

        stats = f"{row_1}\n{row_2}"

        label_width = 9
        detail_rows = []

        if self.illness:
            detail_rows.append(f"{'Illness':<{label_width}} {dim('|')} {yellow(self.illness.name)}")

        if self.name != BRO:
            items = dim(', ').join(cyan(i.name) for i in self.items)
            weapons = dim(', ').join(red(w.name) for w in self.weapons)
            perks = dim(', ').join(purple(p.name) for p in self.perks)

            if self.items:
                detail_rows.append(f"{'Items':<{label_width}} {dim('|')} {items}")

            if self.weapons:
                detail_rows.append(f"{'Weapons':<{label_width}} {dim('|')} {weapons}")

            if self.perks:
                detail_rows.append(f"{'Perks':<{label_width}} {dim('|')} {perks}")

        if self.notes:
            detail_rows.append(f"{'Notes':<{label_width}} {dim('|')} {blue(self.notes)}")

        label = getattr(self, "label", None)
        title = f"{orange(self.name)} {dim(f'({label})')}" if label else orange(self.name)

        return "\n".join([
            title,
            "",
            stats,
            "",
            *detail_rows,
            "",
        ])

def load_builds(restriction: List[str] = None):
    return [Build(**d) for d in Builds if restriction is None or d['name'] in restriction]