import random

from bookoftench import event_logger
from bookoftench.audio import play_music, play_sound
from bookoftench.component.base import LabeledSelectionComponent, SelectionBinding, ReprBinding, Component, \
    functional_component
from bookoftench.component.registry import register_component
from bookoftench.data.audio import PURCHASE
from bookoftench.data.fishing_areas import Fishing_Areas
from bookoftench.data.fishmonger import Fishmonger_Lines
from bookoftench.data.components import FISHING
from bookoftench.model import GameState
from bookoftench.model.FishingArea import load_fishing_areas, FishingArea
from bookoftench.ui import blue, yellow
from bookoftench.util import print_and_sleep

# ================================================================================================

@register_component(FISHING)
class FishingComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        player = game_state.player
        valid = [i['name'] for i in Fishing_Areas if i.level <= player.lvl]
        available = load_fishing_areas(valid)

        fishing_area_bindings = [ReprBinding(str(i + 1), area.name,
                                       self._make_purchase_component(area), area) for
                          i, area in enumerate(available)]

        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*fishing_area_bindings, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                fishing_area_bindings,
                top_level_prompt_callback=display_fishing_header,
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
        message = random.choice(Fishmonger_Lines)
        print_and_sleep(
            f"{blue(message)}", 1.5
        )
        for component in self.selection_components:
            component.display_options()

# ================================================================================================

    # todo - add logic for cost to increase with player level and vary w/ season

    @staticmethod
    def _make_purchase_component(fishing_area: FishingArea) -> type[Component]:
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            player = game_state.player

            if fishing_area.travel_cost > player.coins:
                print_and_sleep(yellow(f"Need more coin"), 2)
            else:
                player.coins -= fishing_area.travel_cost
                play_sound(PURCHASE)
                game_state.current_fishing_area = fishing_area.name

            event_logger.log_event(FishingEvent())

        return FishingComponent(game_state).run()

