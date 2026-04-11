import random

from bookoftench import event_logger
from bookoftench.audio import play_music, play_sound
from bookoftench.component.base import LabeledSelectionComponent, SelectionBinding, ReprBinding, Component, \
    functional_component, GatekeepingComponent
from bookoftench.component.registry import register_component
from bookoftench.data.audio import OCCULTIST_THEME, RITUAL
from bookoftench.data.components import OCCULTIST
from bookoftench.data.enviroment import FULL, NIGHTTIME
from bookoftench.data.rituals import Occultist_Lines
from bookoftench.model import GameState
from bookoftench.model.events import OccultistEvent
from bookoftench.model.ritual import Ritual, load_rituals
from bookoftench.model.util import display_occultist_header
from bookoftench.ui import blue, yellow
from bookoftench.util import print_and_sleep


@register_component(OCCULTIST)
class OccultistBouncer(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: game_state.moon == FULL,
                         accept_component=OccultistComponent,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             blue("The Occultist requires a Full Moon to perform rituals."), 1.5)))

class OccultistComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        ritual_options = load_rituals()

        ritual_bindings = [ReprBinding(str(i + 1), ritual.name, self._make_purchase_component(ritual), ritual) for
                           i, ritual in enumerate(ritual_options)]
        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))
        super().__init__(game_state, refresh_menu=True,
                         bindings=[*ritual_bindings, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                ritual_bindings,
                top_level_prompt_callback=display_occultist_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [return_binding]
            ),
        ]
        self.leave = False

    def play_theme(self) -> None:
        play_music(OCCULTIST_THEME)

    def _return(self):
        self.leave = True
        print_and_sleep(f"{blue('Farewell.')}", 1)

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

    def display_options(self) -> None:
        message = random.choice(Occultist_Lines)
        print_and_sleep(
            f"{blue(message)}\n", 1.5
        )
        for component in self.selection_components:
            component.display_options()

    @staticmethod
    def _make_purchase_component(ritual: Ritual) -> type[Component]:
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            player = game_state.player
            if player.coins < ritual.cost:
                print_and_sleep(yellow(f"Need more coin"), 1)
            else:
                player.coins -= ritual.cost
                event_logger.log_event(OccultistEvent())
                play_sound(RITUAL)
                ritual.invoke(player)

        return purchase_component
