import random
from copy import deepcopy

from bookoftench.audio import play_music, play_sound, stop_music
from bookoftench.component import BoatComponent, TackleBox, FishingLog
from bookoftench.component.base import LabeledSelectionComponent, SelectionBinding, ReprBinding, Component, \
    functional_component, GatekeepingComponent
from bookoftench.component.registry import register_component
from bookoftench.data.audio import PURCHASE, TRAVEL_THEME, FISHMONGER_THEME_1, FISHMONGER_THEME_2, FISHMONGER_THEME_3
from bookoftench.data.bait import Bait_And_Lures
from bookoftench.data.environment import DAY
from bookoftench.data.fishing_areas import Fishing_Areas
from bookoftench.data.components import FISHMONGER
from bookoftench.data.fishing_items import Fishing_Items
from bookoftench.model import GameState
from bookoftench.model.fishing_area import load_fishing_areas, FishingArea
from bookoftench.model.bait import load_baits, Bait
from bookoftench.model.fishing_item import load_fishing_items, FishingItem
from bookoftench.model.util import display_fishmonger_header, display_bait_shop_header, display_fishing_item_shop_header
from bookoftench.ui import blue, yellow, cyan, orange
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
        themes = [FISHMONGER_THEME_1, FISHMONGER_THEME_2, FISHMONGER_THEME_3]
        self.theme = random.choice(themes)

        player = game_state.player
        valid = [i['name'] for i in Fishing_Areas if i['lvl'] <= player.lvl]
        available = load_fishing_areas(valid)

        fishing_area_bindings = [ReprBinding(str(i + 1), area.name,
                                       self._make_purchase_component(area), area) for
                          i, area in enumerate(available)]

        bait_shop_binding = SelectionBinding('S', "Shop", functional_component()(lambda: self.bait_shop()))
        tackle_box_binding = SelectionBinding('T', "Tackle Box", functional_component()(lambda: self.tackle_box()))
        fishing_log_binding = SelectionBinding('L', "Fishing Log", functional_component()(lambda: self.fishing_log()))

        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*fishing_area_bindings, bait_shop_binding,
                                   tackle_box_binding, fishing_log_binding,
                                   return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                fishing_area_bindings,
                top_level_prompt_callback=display_fishmonger_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [bait_shop_binding, tackle_box_binding, fishing_log_binding, return_binding],
            ),
        ]
        self.leave = False

    def play_theme(self) -> None:
        play_music(self.theme)

    def _return(self):
        self.leave = True
        print_and_sleep(blue("Aye."), 1)

    def bait_shop(self):
        BaitShop(self.game_state).run()

    def tackle_box(self):
        TackleBox(self.game_state).run()

    def fishing_log(self):
        FishingLog(self.game_state).run()

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

    def display_options(self) -> None:
        for component in self.selection_components:
            component.display_options()

# ================================================================================================

    # todo - add logic for cost to increase with player level and vary w/ season

    @staticmethod
    def _make_purchase_component(fishing_area: FishingArea) -> type[Component]:
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            player = game_state.player
            when = "tonight" if game_state.time_of_day == DAY else "tomorrow"

            if game_state.player_went_fishing:
                print_and_sleep(yellow(f"Boat's already been out. Come back {when}."), 2)
                return None
            elif fishing_area.travel_cost > player.coins:
                print_and_sleep(yellow(f"Need more coin."), 2)
                return None
            elif not player.current_bait:
                print_and_sleep(yellow(f"Equip some bait."), 2)
                return None
            else:
                game_state.player_went_fishing = True
                player.coins -= fishing_area.travel_cost
                game_state.current_fishing_area = fishing_area

                play_music(TRAVEL_THEME)
                print_and_sleep(cyan(f"Traveling by boat to the {fishing_area.name}..."), 4)

                BoatComponent(game_state).run()
                return None

            # event_logger.log_event(FishingEvent())

        return purchase_component

# ================================================================================================
# ================================================================================================

class BaitShop(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        player = game_state.player

        cost = get_rod_upgrade_cost(player)
        cost_display = orange(f"{cost}")

        valid = [i['name'] for i in Bait_And_Lures]
        available = load_baits(valid)

        bait_bindings = [ReprBinding(str(i + 1), bait.name,
                                       self._make_purchase_component(bait), bait) for
                          i, bait in enumerate(available)]

        upgrade_rod_binding = SelectionBinding('U', f"Upgrade Rod ({cost_display})",
                                               functional_component()(lambda: upgrade_rod(player, cost)))
        fishing_item_shop_binding = SelectionBinding('I', "Item Shop",
                                                     functional_component()(lambda: self.launch_fishing_item_shop()))
        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*bait_bindings, upgrade_rod_binding, fishing_item_shop_binding, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                bait_bindings,
                top_level_prompt_callback=display_bait_shop_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [upgrade_rod_binding, fishing_item_shop_binding, return_binding]
            ),
        ]
        self.leave = False

    def play_theme(self) -> None:
        pass

    def launch_fishing_item_shop(self) -> None:
        self.leave = True
        FishingItemShop(self.game_state).run()

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
                print_and_sleep(yellow("Need more coin."), 1.5)
                return

            if bait.name in player.tackle_box:
                player.tackle_box[bait.name].casts += bait.casts
            else:
                purchased_bait = deepcopy(bait)

                if not player.tackle_box:
                    player.current_bait = purchased_bait

                player.tackle_box[purchased_bait.name] = purchased_bait

            play_sound(PURCHASE)
            player.coins -= bait.cost
            print_and_sleep(cyan(f"{bait.name} added to tackle box."), 1)

        return purchase_component

# ================================================================================================
# ================================================================================================

class FishingItemShop(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        player = game_state.player

        cost = get_rod_upgrade_cost(player)
        cost_display = orange(f"{cost}")

        valid = [i['name'] for i in Fishing_Items]
        available = load_fishing_items(valid)

        fishing_item_bindings = [ReprBinding(str(i + 1), fishing_item.name,
                                       self._make_purchase_component(fishing_item), fishing_item) for
                          i, fishing_item in enumerate(available)]

        upgrade_rod_binding = SelectionBinding('U', f"Upgrade Rod ({cost_display})",
                                               functional_component()(lambda: upgrade_rod(player, cost)))
        bait_shop_binding = SelectionBinding('B', "Bait Shop", functional_component()(lambda: self.launch_bait_shop()))
        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*fishing_item_bindings, upgrade_rod_binding, bait_shop_binding, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                fishing_item_bindings,
                top_level_prompt_callback=display_fishing_item_shop_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [upgrade_rod_binding, bait_shop_binding, return_binding]
            ),
        ]
        self.leave = False

    def play_theme(self) -> None:
        pass

    def launch_bait_shop(self):
        self.leave = True
        BaitShop(self.game_state).run()

    def _return(self):
        self.leave = True

    def can_exit(self) -> bool:
        return self.leave

    def display_options(self) -> None:
        for component in self.selection_components:
            component.display_options()

# ================================================================================================

    @staticmethod
    def _make_purchase_component(fishing_item: FishingItem) -> type[Component]:
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            player = game_state.player

            if fishing_item.cost > player.coins:
                print_and_sleep(yellow("Need more coin"), 1.5)
                return

            if fishing_item.name in player.fishing_item_box:
                player.fishing_item_box[fishing_item.name].count += 1
            else:
                player.fishing_item_box[fishing_item.name] = deepcopy(fishing_item)

            play_sound(PURCHASE)
            player.coins -= fishing_item.cost
            print_and_sleep(cyan(f"{fishing_item.name} added to fishing items."), 1)

        return purchase_component

# ================================================================================================

def get_rod_upgrade_cost(player) -> int:
    cost = 25 * (player.rod_lvl ** 1.8)
    return round(cost / 5) * 5

def upgrade_rod(player, cost):
    if player.coins >= cost:
        original = player.rod_lvl
        player.rod_lvl += 1
        play_sound(PURCHASE)
        player.coins -= cost
        print_and_sleep(cyan(f"Rod Level: {original} -> {player.rod_lvl}"), 1)
    else:
        print_and_sleep(yellow("Need more coin."), 1)