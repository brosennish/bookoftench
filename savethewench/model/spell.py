import random
from dataclasses import dataclass
from typing import List

from savethewench.data.spells import ITEM_MAGIC, WEAPON_MAGIC, Spells
from savethewench.model.base import Buyable
from savethewench.model.player import Player
from savethewench.ui import cyan, orange, dim, purple
from savethewench.util import print_and_sleep


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
            print_and_sleep(f"{cyan(f'TEXT')}", 2)
        elif self.name == WEAPON_MAGIC:
            print_and_sleep(f"{cyan(f'TEXT')}", 2)


def load_spells() -> List[Spell]:
    return [
        Spell(**spell_dict)
        for spell_dict in Spells
    ]