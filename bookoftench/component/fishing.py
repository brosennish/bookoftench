import random

from bookoftench import event_logger
from bookoftench.audio import play_music, play_sound
from bookoftench.component.base import LabeledSelectionComponent, SelectionBinding, ReprBinding, Component, \
    functional_component
from bookoftench.component.registry import register_component
from bookoftench.data.fishing import TACKLE_BOX, FISHING_OPTIONS, CAST, FISH_LOG, SHOP
from bookoftench.data.components import BOAT
from bookoftench.model import GameState
from bookoftench.model.util import display_boat_header
from bookoftench.ui import blue, yellow
from bookoftench.util import print_and_sleep

# ================================================================================================

@register_component(BOAT)
class BoatComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        player = game_state.player
        original = FISHING_OPTIONS.copy()
        options = [i['name'] for i in original]

        fishing_option_bindings = [ReprBinding(str(i + 1), option,
                                       self._handle_selection_component(option), option) for
                          i, option in enumerate(options)]

        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*fishing_option_bindings, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                fishing_option_bindings,
                top_level_prompt_callback=display_boat_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [return_binding]
            ),
        ]
        self.leave = False

    def play_theme(self) -> None:
        pass
        # play_music(FISHMONGER_THEME)

    def _return(self):
        self.leave = True
        print_and_sleep(f"{blue("Aye.")}", 1)

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

    def display_options(self) -> None:
        for component in self.selection_components:
            component.display_options()

# ================================================================================================

    # todo - add logic for cost to increase with player level and vary w/ season

    @staticmethod
    def _handle_selection_component(selection: str) -> type[Component]:
        @functional_component(state_dependent=True)
        def selection_component(game_state: GameState):
            player = game_state.player

            if selection == CAST:
                pass
            elif selection == FISH_LOG:
                pass
            elif selection == SHOP:
                pass
            elif selection == TACKLE_BOX:
                pass
            else:
                return selection_component(game_state)

        return selection_component

# ================================================================================================