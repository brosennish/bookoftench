import random

from bookoftench import event_logger
from bookoftench.audio import play_music, play_sound
from bookoftench.component.base import LabeledSelectionComponent, SelectionBinding, ReprBinding, Component, \
    functional_component
from bookoftench.component.casting import DryCastCheck
from bookoftench.component.registry import register_component
from bookoftench.data.audio import EQUIP_WEAPON
from bookoftench.data.boat import TACKLE_BOX, FISHING_OPTIONS, CAST, FISH_LOG, SHOP
from bookoftench.data.components import BOAT
from bookoftench.model import GameState
from bookoftench.model.bait import Bait
from bookoftench.model.util import display_boat_header, display_tackle_box_header
from bookoftench.ui import blue, yellow
from bookoftench.util import print_and_sleep

# ================================================================================================
# ================================================================================================

@register_component(BOAT)
class BoatComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
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
        print_and_sleep(blue("Aye."), 1)

    def can_exit(self) -> bool:
        return (self.leave or self.game_state.current_fishing_area.casts == 0
                or not self.game_state.player.is_alive())

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
                if not player.tackle_box:
                    print_and_sleep(f"{blue('Ain\'t got no bait, bozo.')}", 1)
                    return None
                game_state.current_fishing_area.casts -= 1
                DryCastCheck(game_state).run()
                return None
            elif selection == FISH_LOG:
                pass
            elif selection == TACKLE_BOX:
                if player.has_usable_bait:
                    TackleBox(game_state).run()
                else:
                    print_and_sleep(f"{blue('Ain\'t got no bait, bozo.')}", 1)
                return None

            else:
                return None

        return selection_component

# ================================================================================================

class TackleBox(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        player = game_state.player
        available = [i for i in player.tackle_box.values() if i.casts > 0]

        tackle_box_bindings = [ReprBinding(str(i + 1), bait.name,
                                           self._handle_selection_component(bait), bait) for
                               i, bait in enumerate(available)]

        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*tackle_box_bindings, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                tackle_box_bindings,
                top_level_prompt_callback=display_tackle_box_header,
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

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

    def display_options(self) -> None:
        for component in self.selection_components:
            component.display_options()

    # ================================================================================================

    @staticmethod
    def _handle_selection_component(selection: Bait) -> type[Component]:
        @functional_component(state_dependent=True)
        def selection_component(game_state: GameState):
            player = game_state.player

            player.equip_bait(selection)
            play_sound(EQUIP_WEAPON)
            print_and_sleep(f"{selection.name} equipped.", 1)

        return selection_component

