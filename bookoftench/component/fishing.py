from bookoftench.audio import play_music, play_sound
from bookoftench.component.base import LabeledSelectionComponent, SelectionBinding, ReprBinding, Component, \
    functional_component, TextDisplayingComponent
from bookoftench.component.casting import DryCastCheck
from bookoftench.component.registry import register_component
from bookoftench.data.audio import EQUIP_WEAPON, OCEAN_THEME, SHALLOWS_THEME, BAY_THEME
from bookoftench.data.boat import TACKLE_BOX, FISHING_OPTIONS, CAST, FISHING_LOG, ALL_NEW_ONLY
from bookoftench.data.components import BOAT, COMPENDIUM
from bookoftench.data.enviroment import DAY
from bookoftench.data.fish import SHALLOWS, OCEAN, BAY
from bookoftench.model import GameState
from bookoftench.model.bait import Bait
from bookoftench.model.fishing_item import FishingItem
from bookoftench.model.util import display_boat_header, display_tackle_box_header, display_fish_log_header, \
    display_fishing_stats, display_area_log, display_area_compendium, display_compendium_header, \
    display_fishing_item_box_header
from bookoftench.ui import blue, cyan, yellow
from bookoftench.util import print_and_sleep

# ================================================================================================
# ================================================================================================

@register_component(BOAT)
class BoatComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        self.fishing_area = game_state.current_fishing_area.name
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

            ),
            LabeledSelectionComponent(
                game_state,
                [return_binding],
            ),
        ]
        self.leave = False

    def play_theme(self) -> None:
        if self.fishing_area == SHALLOWS:
            play_music(SHALLOWS_THEME)
        elif self.fishing_area == BAY:
            play_music(BAY_THEME)
        else:
            play_music(OCEAN_THEME)

    def _return(self):
        self.leave = True

    def can_exit(self) -> bool:
        no_casts_left = self.game_state.current_fishing_area.casts == 0
        no_active_fish = self.game_state.current_fish is None
        player_dead = not self.game_state.player.is_alive()
        no_bait = not self.game_state.player.has_usable_bait

        return (
                self.leave
                or (no_casts_left and no_active_fish)
                or player_dead
                or no_bait
        )

    def toggle_fish(self):
        self.game_state.all_fish = not self.game_state.all_fish

    def display_options(self) -> None:
        if self.can_exit():
            return

        display_boat_header(self.game_state)

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
                if not player.current_bait:
                    print_and_sleep(f"{blue('Need some fresh bait mate.')}", 1)
                    return None
                if player.current_bait.casts == 0:
                    print_and_sleep(f"{blue('Need some fresh bait mate.')}", 1)
                    return None
                DryCastCheck(game_state).run()
                return None

            elif selection == FISHING_LOG:
                FishingLog(game_state).run()
                return None
            elif selection == TACKLE_BOX:
                if player.has_usable_bait:
                    TackleBox(game_state).run()
                else:
                    print_and_sleep(f"{blue('Tackle box is dry.')}", 1)
                return None
            elif selection == ALL_NEW_ONLY:
                BoatComponent(game_state).toggle_fish()
                return None
            else:
                return None

        return selection_component

# ================================================================================================

class TackleBox(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        player = game_state.player

        available = [i for i in player.tackle_box.values() if i.casts > 0 and i != player.current_bait]

        tackle_box_bindings = [ReprBinding(str(i + 1), bait.name,
                                           self._handle_selection_component(bait, self), bait) for
                               i, bait in enumerate(available)]

        items_binding = SelectionBinding('I', "Fishing Items",
                                         functional_component()(lambda: self.open_fishing_box()))
        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*tackle_box_bindings, items_binding, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                tackle_box_bindings,
                top_level_prompt_callback=display_tackle_box_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [items_binding, return_binding]
            ),
        ]
        self.leave = False


    def play_theme(self) -> None:
        pass

    def _return(self):
        self.leave = True

    def open_fishing_box(self) -> None:
        FishingItemBox(self.game_state).run()

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

    def display_options(self) -> None:
        for component in self.selection_components:
            component.display_options()

# ================================================================================================

    @staticmethod
    def _handle_selection_component(selection: Bait, parent) -> type[Component]:
        @functional_component(state_dependent=True)
        def selection_component(game_state: GameState):
            player = game_state.player

            player.equip_bait(selection)
            play_sound(EQUIP_WEAPON)
            print_and_sleep(f"{cyan(selection.name)} equipped.", 1)
            parent.leave = True

        return selection_component

# ================================================================================================

class FishingItemBox(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        player = game_state.player

        available = sorted(
            [i for i in player.fishing_item_box.values() if i.count > 0],
            key=lambda x: (
                x.type,
                -(x.speed_reduction + x.stamina_reduction + x.rage_reduction + x.strength_reduction)
            )
        )

        item_box_bindings = [
            ReprBinding(
                str(i + 1),
                item.name,
                self._handle_selection_component(item, self),
                item.inventory_repr()
            )
            for i, item in enumerate(available)
        ]

        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*item_box_bindings, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                item_box_bindings,
                top_level_prompt_callback=display_fishing_item_box_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [return_binding]
            ),
        ]
        self.leave = False


    def play_theme(self) -> None:
        pass

    def _return(self):
        self.leave = True

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

    def display_options(self) -> None:
        has_usable_items = any(
            item.count > 0 for item in self.game_state.player.fishing_item_box.values()
        )

        if not has_usable_items:
            print_and_sleep(yellow("You're dry."), 1)
            self.leave = True
            return

        for component in self.selection_components:
            component.display_options()

# ================================================================================================

    @staticmethod
    def _handle_selection_component(item: FishingItem, parent) -> type[Component]:
        @functional_component(state_dependent=True)
        def selection_component(game_state: GameState):
            player = game_state.player
            fish = game_state.current_fish
            turns = item.turns

            # --- check if active fish ---
            if not game_state.current_fish:
                print_and_sleep(yellow("Need a fish on the line."), 1)
                return

            # --- check if item valid to use ---
            if item in player.active_fishing_items:
                print_and_sleep(yellow(f"{item.name} is already active."), 1)
                return
            if item_stack_conflict(player, item):
                return
            if len(player.active_fishing_items) >= player.max_active_fishing_items:
                max_active = player.max_active_fishing_items
                print_and_sleep(yellow(f"Maximum active items reached ({max_active})."), 1)
                return

            # --- use item ---
            player.use_fishing_item(fish, item)
            print_and_sleep(
                f"You used {cyan(item.name)}, which will run dry after {yellow(turns)} turns.",
                1.5
            )
            parent.leave = True

        return selection_component

def item_stack_conflict(player, item) -> bool:
    for active in player.active_fishing_items:
        if active.type == item.type:
            print_and_sleep(yellow(f"{active.name} is already active."), 1)
            return True

    return False

# ================================================================================================

@register_component(FISHING_LOG)
class FishingLog(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        areas = [SHALLOWS, BAY, OCEAN]

        fishing_area_bindings = [ReprBinding(str(i + 1), area,
                                           self._handle_selection_component(area), area) for
                               i, area in enumerate(areas)]

        stats_binding = SelectionBinding('S', "Stats", FishingStats)
        compendium_binding = SelectionBinding('C', "Compendium", functional_component()
                                             (lambda: self.open_compendium()))
        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*fishing_area_bindings, stats_binding, compendium_binding, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                fishing_area_bindings,
                top_level_prompt_callback=display_fish_log_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [stats_binding, compendium_binding, return_binding]
            ),
        ]
        self.leave = False

    def play_theme(self) -> None:
        pass

    def _return(self):
        self.leave = True

    def open_compendium(self):
        return Compendium(self.game_state).run()

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

    def display_options(self) -> None:
        for component in self.selection_components:
            component.display_options()

# ================================================================================================

    @staticmethod
    def _handle_selection_component(selection: str) -> type[Component]:
        @functional_component(state_dependent=True)
        def selection_component(game_state: GameState):
            AreaFishLog(game_state, selection).run()

        return selection_component

# ================================================================================================
# ================================================================================================

class FishingStats(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_fishing_stats)


class AreaFishLog(TextDisplayingComponent):
    def __init__(self, game_state: GameState, area: str):
        self.area = area
        super().__init__(
            game_state,
            display_callback=self.display_log
        )

    def display_log(self, game_state: GameState):
        return display_area_log(game_state, self.area)


# ================================================================================================
# ================================================================================================

@register_component(COMPENDIUM)
class Compendium(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        areas = [SHALLOWS, BAY, OCEAN]

        compendium_bindings = [ReprBinding(str(i + 1), area,
                                           self._handle_selection_component(area), area) for
                               i, area in enumerate(areas)]

        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*compendium_bindings, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                compendium_bindings,
                top_level_prompt_callback=display_compendium_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [return_binding],
            ),
        ]
        self.leave = False

    def play_theme(self) -> None:
        pass

    def _return(self):
        self.leave = True

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

    def display_options(self) -> None:
        for component in self.selection_components:
            component.display_options()

# ================================================================================================

    @staticmethod
    def _handle_selection_component(selection: str) -> type[Component]:
        @functional_component(state_dependent=True)
        def selection_component(game_state: GameState):
            AreaCompendium(game_state, selection).run()

        return selection_component

# ================================================================================================

class AreaCompendium(TextDisplayingComponent):
    def __init__(self, game_state: GameState, area: str):
        self.area = area
        super().__init__(
            game_state,
            display_callback=self.display_compendium
        )

    def display_compendium(self, game_state: GameState):
        return display_area_compendium(game_state, self.area)

