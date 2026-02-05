import random
from dataclasses import dataclass
from typing import List

from bookoftench.data.spells import ITEM_MAGIC, WEAPON_MAGIC, Spells
from bookoftench.model.base import Buyable
from bookoftench.model.item import load_items
from bookoftench.model.player import Player
from bookoftench.model.weapon import load_weapons
from bookoftench.ui import cyan, orange, dim, purple
from bookoftench.util import print_and_sleep


@dataclass
class Spell(Buyable):
    name: str
    description: str
    cost: int
    type: str

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<12}"),
            f"Cost: {orange(self.cost)}",
            f"{purple(self.description)}",
        ])

    def cast(self, player: Player):
        if self.name == ITEM_MAGIC:
            filtered = [i for i in load_items() if i.name not in player.items]
            item = random.choice(filtered)
            player.add_item(item)

            print_and_sleep(f"{cyan(f'{item.name} magically added to sack.')}", 2)

        elif self.name == WEAPON_MAGIC:
            filtered = [w for w in load_weapons() if w.name not in [pw.name for pw in player.get_weapons()]
                        and w.uses > 0]
            weapon = random.choice(filtered)

            low = min(5, weapon.uses)
            high = min(8, weapon.uses)
            weapon.uses = random.randint(low, high)

            player.add_weapon(weapon)
            print_and_sleep(f"{cyan(f'{weapon.name} magically added to sack.')}", 2)


def load_spells() -> List[Spell]:
    return [
        Spell(**spell_dict)
        for spell_dict in Spells
    ]
