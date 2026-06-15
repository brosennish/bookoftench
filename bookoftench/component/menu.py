from typing import List

from bookoftench.component.base import SelectionBinding, PaginatedMenuComponent, LabeledSelectionComponent, \
    functional_component
from bookoftench.data.components import SEARCH, AREA_BOSS_FIGHT, FINAL_BOSS_FIGHT, InGameMenuDefaults, \
    StartGameMenuDefaults, SAVE_GAME, LOAD_GAME, OverviewMenuDefaults
from bookoftench.globals import is_debug_mode
from bookoftench.model import GameState
from bookoftench.model.area import AreaActions
from bookoftench.model.util import get_player_status_view_1, get_player_status_view_2, get_player_status_view_3, \
    get_player_status_view_4
from bookoftench.util import print_and_sleep
from .registry import get_registered_component

# ================================================================================================

class StartMenu(PaginatedMenuComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def construct_pages(self) -> List[List[SelectionBinding]]:
        return [[SelectionBinding(str(i), name, get_registered_component(name))
                 for i, name in enumerate(StartGameMenuDefaults.page_one, 1)]]

# ================================================================================================

class ActionMenu(PaginatedMenuComponent):
    def __init__(self, game_state: GameState):
        self.status_view = 1

        super().__init__(
            game_state,
            top_level_prompt_callback=self.display_status,
            main_menu_component=InGameMenu
        )

    def display_status(self, game_state: GameState) -> None:
        if self.status_view == 1:
            print_and_sleep(get_player_status_view_1(game_state))
        elif self.status_view == 2:
            print_and_sleep(get_player_status_view_2(game_state))
        elif self.status_view == 3:
            print_and_sleep(get_player_status_view_3(game_state))
        else:
            print_and_sleep(get_player_status_view_4(game_state))

    def toggle_status_view(self):
        if self.status_view == 1:
            self.status_view = 2
        elif self.status_view == 2:
            self.status_view = 3
        elif self.status_view == 3:
            self.status_view = 4
        else:
            self.status_view = 1
        return self.game_state

    def construct_control_component(self) -> LabeledSelectionComponent:
        component = super().construct_control_component()

        component.binding_map["s"] = SelectionBinding(
            "S",
            "Toggle Status",
            functional_component()(lambda: self.toggle_status_view())
        )

        return component

    def construct_pages(self) -> List[List[SelectionBinding]]:
        area_actions: AreaActions = self.game_state.current_area.actions_menu
        pages = []

        for page in area_actions.pages:
            modified = [c for c in page]

            if SEARCH in modified and self.game_state.current_area.enemies_remaining == 0:
                modified.remove(SEARCH)

                if not self.game_state.current_area.boss_defeated:
                    self.game_state.current_area.current_enemy = self.game_state.current_area.boss
                    modified = [AREA_BOSS_FIGHT, *modified]

                elif self.game_state.is_final_boss_available():
                    modified = [FINAL_BOSS_FIGHT, *modified]

            pages.append(modified)

        return [
            [
                SelectionBinding(str(i), name, get_registered_component(name))
                for i, name in enumerate(spec, 1)
            ]
            for spec in pages
        ]

    def play_theme(self) -> None:
        self.game_state.play_current_area_theme()

    def can_exit(self) -> bool:
        return (self.return_selected or
                self.game_state.victory or
                not self.game_state.player.is_alive())

# ================================================================================================

class InGameMenu(PaginatedMenuComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, returnable=True)

    def construct_pages(self) -> List[List[SelectionBinding]]:
        page = [c for c in InGameMenuDefaults.page_one]
        if is_debug_mode():
            page += [SAVE_GAME, LOAD_GAME]
        return [[SelectionBinding(str(i), name, get_registered_component(name))
                 for i, name in enumerate(page, 1)]]

# ================================================================================================

class OverviewMenu(PaginatedMenuComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, returnable=True)

    def construct_pages(self) -> List[List[SelectionBinding]]:
        pages = [
            OverviewMenuDefaults.page_one,
            OverviewMenuDefaults.page_two,
        ]

        return [
            [
                SelectionBinding(str(i), name, get_registered_component(name))
                for i, name in enumerate(page, 1)
            ]
            for page in pages
        ]

    def can_exit(self) -> bool:
        return self.return_selected
