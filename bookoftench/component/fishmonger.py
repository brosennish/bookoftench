import random

from bookoftench.audio import play_music, play_sound, stop_music
from bookoftench.component import BoatComponent, TackleBox, FishLog
from bookoftench.component.base import LabeledSelectionComponent, SelectionBinding, ReprBinding, Component, \
    functional_component, GatekeepingComponent
from bookoftench.component.registry import register_component
from bookoftench.data.audio import PURCHASE, TRAVEL_THEME
from bookoftench.data.bait import Bait_And_Lures
from bookoftench.data.fishing_areas import Fishing_Areas
from bookoftench.data.fishmonger import Fishmonger_Lines
from bookoftench.data.components import FISHMONGER
from bookoftench.model import GameState
from bookoftench.model.FishingArea import load_fishing_areas, FishingArea
from bookoftench.model.bait import load_baits, Bait
from bookoftench.model.util import display_fishmonger_header, display_bait_shop_header
from bookoftench.ui import blue, yellow, cyan
from bookoftench.util import print_and_sleep

# ================================================================================================

# --- check if fishmonger is open ---

@register_component(FISHMONGER)
class FishmongerOpen(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: game_state.fishmonger_is_open,
                         accept_component=Fishmonger,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             blue("The Fishmonger is lost at sea.\n"), 1.5)))

# ================================================================================================

class Fishmonger(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        player = game_state.player
        valid = [i['name'] for i in Fishing_Areas if i['lvl'] <= player.lvl]
        available = load_fishing_areas(valid)

        fishing_area_bindings = [ReprBinding(str(i + 1), area.name,
                                       self._make_purchase_component(area), area) for
                          i, area in enumerate(available)]

        bait_shop_binding = SelectionBinding('S', "Shop", functional_component()(lambda: self._shop()))
        fish_log_binding = SelectionBinding('L', "Fish Log", FishLog)
        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*fishing_area_bindings, bait_shop_binding, fish_log_binding, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                fishing_area_bindings,
                top_level_prompt_callback=display_fishmonger_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [bait_shop_binding, return_binding],
            ),
        ]
        self.leave = False

    def play_theme(self) -> None:
        pass
        # play_music(FISHMONGER_THEME)

    def _return(self):
        self.leave = True
        print_and_sleep(f"{blue("Aye.")}", 1)

    def _shop(self):
        BaitShop(self.game_state).run()

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
                game_state.current_fishing_area = fishing_area
                play_music(TRAVEL_THEME)
                print_and_sleep(cyan(f'Traveling by boat to the {fishing_area.name}...'), 4)
                stop_music() # todo - remove this once boat component has theme
                BoatComponent(game_state).run()

            # event_logger.log_event(FishingEvent())

        return purchase_component

# ================================================================================================
# ================================================================================================

class BaitShop(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        valid = [i['name'] for i in Bait_And_Lures]
        available = load_baits(valid)

        bait_bindings = [ReprBinding(str(i + 1), bait.name,
                                       self._make_purchase_component(bait), bait) for
                          i, bait in enumerate(available)]

        tackle_box_binding = SelectionBinding('T', "Return", TackleBox)
        return_binding = SelectionBinding('R', "Return", Fishmonger)

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*bait_bindings, tackle_box_binding, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                bait_bindings,
                top_level_prompt_callback=display_bait_shop_header,
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
        return self.leave

    def display_options(self) -> None:
        for component in self.selection_components:
            component.display_options()

# ================================================================================================

    @staticmethod
    def _make_purchase_component(bait: Bait) -> type[Component]:
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            player = game_state.player

            if bait.cost > player.coins:
                print_and_sleep(yellow(f"Need more coin"), 1.5)
            else:
                if bait.name in player.tackle_box:
                    player.tackle_box[bait.name].casts += bait.casts
                else:
                    player.tackle_box[bait.name] = bait
                play_sound(PURCHASE)
                print_and_sleep(cyan(f"{bait.name} added to tackle box."), 1.5)

            # BoatComponent(game_state).run() (not sure if it will return to Fishmonger)
            # event_logger.log_event(FishingEvent())

        return purchase_component

