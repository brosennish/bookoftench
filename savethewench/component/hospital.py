import random

from savethewench import event_logger
from savethewench.audio import play_music
from savethewench.component.base import functional_component, GatekeepingComponent, BinarySelectionComponent
from savethewench.component.registry import register_component
from savethewench.data.audio import HOSPITAL_THEME
from savethewench.data.components import HOSPITAL
from savethewench.event_base import EventType
from savethewench.model import GameState
from savethewench.model.events import TreatmentEvent
from savethewench.model.illness import Illness
from savethewench.model.player import Player
from savethewench.model.util import display_hospital_header
from savethewench.ui import blue, cyan, yellow
from savethewench.util import print_and_sleep


@register_component(HOSPITAL)
class HospitalBouncer(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: game_state.player.illness is not None,
                         accept_component=HospitalComponent,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             blue("Come back when you have something we can make money from.\n"), 1.5)))


class HospitalComponent(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Pay for treatment",
                         yes_component=treatment_component,
                         no_component=functional_component()(self._return),
                         )
        self.exit_hospital = False

    def display_options(self) -> None:
        display_hospital_header(self.game_state)
        super().display_options()

    def play_theme(self) -> None:
        play_music(HOSPITAL_THEME)

    def can_exit(self) -> bool:
        return (self.exit_hospital
                or not self.game_state.player.is_alive()
                or not self.game_state.player.is_sick())

    def _return(self):
        self.exit_hospital = True
        print_and_sleep(blue("You'll be back!"), 1)


@functional_component(state_dependent=True)
def treatment_component(game_state: GameState) -> None:
    player: Player = game_state.player
    illness: Illness = player.illness

    if illness is None:
        raise RuntimeError("Player should not be able to purchase treatment without an illness.")

    if player.coins < illness.cost:
        print_and_sleep(yellow(f"Need more coin"), 1)
        return

    if random.random() < illness.success_rate:
        print_and_sleep(f"{cyan("Woah, I really didn't expect that to work.")}", 2)
        player.illness = None
        player.illness_death_lvl = None
        event_logger.log_event(TreatmentEvent(illness, EventType.TREATMENT_SUCCESS))
    else:
        print_and_sleep(blue(
            f"Shit didn't take. You still owe me {illness.cost} of coin. Also - you into crypto?"),
            2)
        event_logger.log_event(TreatmentEvent(illness, EventType.TREATMENT_FAIL))

    player.coins -= illness.cost
