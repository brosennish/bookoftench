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
    lives: int
    lvl: int
    hp: int
    str: float
    acc: float
    coins: int
    luck: float | int
    fishing_lvl: int
    items: List[Item]
    weapons: List[Weapon]
    perks: List[Perk]

    def __repr__(self) -> str:
        strength = f"{self.str:g}"
        accuracy = f"{self.acc:g}"

        label_width = 9

        stat_rows = [
            f"{'Lvl':<{label_width}} {dim('|')} {cyan(self.lvl)}",
            f"{'Lives':<{label_width}} {dim('|')} {yellow(self.lives)}",
            f"{'HP':<{label_width}} {dim('|')} {green(self.hp)}",
            f"{'Strength':<{label_width}} {dim('|')} {red(strength)}",
            f"{'Accuracy':<{label_width}} {dim('|')} {yellow(accuracy)}",
            f"{'Luck':<{label_width}} {dim('|')} {purple(self.luck)}",
            f"{'Fishing':<{label_width}} {dim('|')} {blue(self.fishing_lvl)}",
            f"{'Coins':<{label_width}} {dim('|')} {green(self.coins)}",
        ]

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

        return "\n".join([
            orange(self.name),
            "",
            *stat_rows,
            "",
            *detail_rows,
            "",
        ])

def load_builds(restriction: List[str] = None):
    return [Build(**d) for d in Builds if restriction is None or d['name'] in restriction]