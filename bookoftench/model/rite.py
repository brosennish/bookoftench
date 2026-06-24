import copy
import random
from dataclasses import dataclass

from bookoftench import event_logger
from bookoftench.audio import play_sound
from bookoftench.data.audio import DRINK
from bookoftench.data.rites import HERBAL_TEA, SHAMANS_CIGAR, TOAD_JUICE, Rites
from bookoftench.event_base import EventType
from bookoftench.model.base import Buyable
from bookoftench.model.events import TreatmentEvent
from bookoftench.model.player import Player
from bookoftench.ui import cyan, dim, green, orange, purple
from bookoftench.util import print_and_sleep

# ================================================================================================

@dataclass
class Rite(Buyable):
    name: str
    description: str
    cost: int

    def get_simple_format(self, player: Player) -> str:
        display_cost = self.cost

        if self.name == TOAD_JUICE:
            display_cost = 5 + (5 * player.blind_turns)

        return dim(" | ").join([
            cyan(f"{self.name:<16}"),
            f"Cost: {orange(f'{display_cost:<3}')}",
            purple(self.description),
        ])

    def __repr__(self) -> str:
        return dim(" | ").join([
            cyan(f"{self.name:<16}"),
            f"Cost: {orange(f'{self.cost:<3}')}",
            purple(self.description),
        ])

    def perform(self, player: Player) -> None:
        if self.name == TOAD_JUICE:
            play_sound(DRINK)

            if not player.blind:
                print_and_sleep(cyan("Your vision remains unimpaired."), 2)
            else:
                print_and_sleep(cyan("Your vision has been restored."), 2)
                player.blind = False
                player.blind_turns = 0

        elif self.name == HERBAL_TEA:
            play_sound(DRINK)

            if not player.illness:
                print_and_sleep(cyan("You remain free of contamination."), 2)
            else:
                event_logger.log_event(TreatmentEvent(player.illness, EventType.TREATMENT_EVENT))
                player.illness = None
                player.illness_death_lvl = None

        elif self.name == SHAMANS_CIGAR:
            gain = random.randint(0, 50)
            original_hp = player.hp
            player.gain_hp(gain)
            print_and_sleep(f"You restored {green(player.hp - original_hp)} hp.", 2)

# ================================================================================================

def load_rites(player: Player) -> list[Rite]:
    rite_data_list = copy.deepcopy(Rites)

    for rite_data in rite_data_list:
        if rite_data["name"] == TOAD_JUICE:
            rite_data["cost"] = 5 + (5 * player.blind_turns)

    return [
        Rite(**rite_data)
        for rite_data in rite_data_list
    ]