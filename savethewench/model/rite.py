import random
from dataclasses import dataclass
from typing import List

from savethewench.data.rites import Rites, TOAD_JUICE, HERBAL_TEA, SHAMANS_CIGAR
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
        if self.name == TOAD_JUICE:
            display_cost = player.blind_turns * 5

        return dim(' | ').join([
            cyan(f"{self.name:<16}"),
            f"Cost: {orange(f'{display_cost:<3}')}",
            f"{purple(self.description)}",
        ])

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<16}"),
            f"Cost: {orange(f'{self.cost:<3}')}",
            f"{purple(self.description)}",
        ])


    def perform(self, player: Player):
        if self.name == TOAD_JUICE:
            if not player.blind:
                print_and_sleep(f"{cyan('Your vision remains unimpaired.')}", 2)
            else:
                print_and_sleep(f"{cyan('Your vision has been restored.')}", 2)
                player.blind = False
                player.blind_turns = 0

        elif self.name == HERBAL_TEA:
            if not player.illness:
                print_and_sleep(f"{cyan(f'You remain free of contamination.')}", 2)
            else:
                print_and_sleep(f"{cyan(f'You have been cured of {player.illness.name}.')}", 2)
                player.illness = None
                player.illness_death_lvl = None

        elif self.name == SHAMANS_CIGAR:
            gain = random.randint(0, 50)
            original_hp = player.hp
            player.gain_hp(gain)
            print_and_sleep(f"You restored {green(player.hp - original_hp)} hp.", 2)


def load_rites() -> List[Rite]:
    return [
        Rite(**rite_dict)
        for rite_dict in Rites
    ]