import random
from dataclasses import dataclass
from typing import List

from savethewench import event_logger
from savethewench.data.rituals import Rituals, TENCH_SACRIFICE, CARP_SACRIFICE
from savethewench.model.base import Buyable
from savethewench.model.events import PlayerDeathEvent
from savethewench.model.player import Player
from savethewench.ui import cyan, orange, dim, purple, red
from savethewench.util import print_and_sleep


@dataclass
class Ritual(Buyable):
    name: str
    description: str
    cost: int

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<15}"),
            f"Cost: {orange(self.cost)}",
            f"{purple(self.description)}",
        ])


    def invoke(self, player: Player):
        if self.name == TENCH_SACRIFICE:
            player.lives += 1
            print_and_sleep(f"{cyan(f'Praise be to the superior Tench. Lives: {player.lives}')}", 2)
        elif self.name == CARP_SACRIFICE:
            if random.random() < 0.5:
                player.lives += 1
                print_and_sleep(f"{cyan(f'Praise be to the inferior Carp. Lives: {player.lives}')}", 2)
            else:
                player.lives -= 1
                if player.lives > 1:
                    print_and_sleep(f"{red(f'Ritual was a bust. Carp didn\'t take. Lives: {player.lives}')}", 2)
                else:
                    print_and_sleep(f"{red(f'Ritual was a bust. Carp didn\'t take.')}", 2)
                    player.hp = 0
                    event_logger.log_event(PlayerDeathEvent(player.lives))


def load_rituals() -> List[Ritual]:
    return [
        Ritual(**ritual_dict)
        for ritual_dict in Rituals
    ]