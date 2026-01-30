import random
from dataclasses import dataclass
from typing import List

from savethewench.data.rites import Rites, RITE_OF_ILLUMINATION, RITE_OF_PURIFICATION, RITE_OF_RESTORATION
from savethewench.model.base import Buyable
from savethewench.model.player import Player
from savethewench.ui import cyan, orange, dim, purple, green
from savethewench.util import print_and_sleep


@dataclass
class Rite(Buyable):
    name: str
    description: str
    cost: int


    def get_simple_format(self, player: Player) -> str:
        display_cost = self.cost
        if self.name == RITE_OF_ILLUMINATION:
            display_cost = player.blind_turns * 5
        return dim(' | ').join([
            cyan(f"{self.name:<20}"),
            f"Cost: {orange(display_cost):<3}",
            f"{purple(self.description)}",
        ])


    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<20}"),
            f"Cost: {orange(self.cost):<3}",
            f"{purple(self.description)}",
        ])


    def perform(self, player: Player):
        if self.name == RITE_OF_ILLUMINATION:
            print_and_sleep(f"{cyan('Your vision has been restored.')}", 2)
            player.blind = False
            player.blind_turns = 0

        elif self.name == RITE_OF_PURIFICATION:
            print_and_sleep(f"{cyan(f'You have been cured of {player.illness}.')}", 2)
            player.illness = None
            player.illness_death_lvl = None

        elif self.name == RITE_OF_RESTORATION:
            gain = random.randint(0, 50)
            original_hp = player.hp
            player.gain_hp(gain)
            print_and_sleep(f"You restored {green(player.hp - original_hp)} hp.", 2)


def load_rites() -> List[Rite]:
    return [
        Rite(**rite_dict)
        for rite_dict in Rites
    ]