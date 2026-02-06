import random

from savethewench.component.base import LabeledSelectionComponent, SelectionBinding, ReprBinding, Component, \
    functional_component, GatekeepingComponent
from savethewench.component.registry import register_component
from savethewench.data.components import SHAMAN
from savethewench.data.rites import TOAD_JUICE, Shaman_Lines
from savethewench.model import GameState
from savethewench.model.rite import Rite, load_rites
from savethewench.model.util import display_shaman_header
from savethewench.ui import blue, yellow
from savethewench.util import print_and_sleep


@register_component(SHAMAN)
class ShamanBouncer(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        player = game_state.player
        super().__init__(game_state, decision_function=lambda: player.illness or player.blind
                         or player.hp != player.max_hp,
                         accept_component=ShamanComponent,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             blue("There is nothing the Shaman can do you for you at this time.\n"), 1.5)))

class ShamanComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        rite_options = load_rites(game_state.player)

        rite_bindings = [ReprBinding(str(i + 1), rite.name, self._make_purchase_component(rite), rite) for
                         i, rite in enumerate(rite_options)]
        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))
        super().__init__(game_state, refresh_menu=True,
                         bindings=[*rite_bindings, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                rite_bindings,
                top_level_prompt_callback=display_shaman_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [return_binding]
            ),
        ]
        self.leave = False

    def _return(self):
        self.leave = True
        print_and_sleep(f"{blue('Go now.')}", 1)

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

    def display_options(self) -> None:
        message = random.choice(Shaman_Lines)
        print_and_sleep(
            f"{blue(message)}\n", 1
        )
        for component in self.selection_components:
            component.display_options()

    @staticmethod
    def _make_purchase_component(rite: Rite) -> type[Component]:
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            player = game_state.player

            if player.coins < rite.cost:
                print_and_sleep(yellow(f"Need more coin"), 1)
            else:
                player.coins -= rite.cost
                rite.perform(player)

        return purchase_component