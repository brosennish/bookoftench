from typing import List

from savethewench.component.base import SelectionBinding, PaginatedMenuComponent
from savethewench.data.components import SEARCH, AREA_BOSS_FIGHT, FINAL_BOSS_FIGHT, InGameMenuDefaults, \
    StartGameMenuDefaults, SAVE_GAME, LOAD_GAME
from savethewench.globals import is_debug_mode
from savethewench.model import GameState
from savethewench.model.area import AreaActions
from savethewench.model.util import get_player_status_view
from savethewench.util import print_and_sleep
from .registry import get_registered_component


class StartMenu(PaginatedMenuComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def construct_pages(self) -> List[List[SelectionBinding]]:
        return [[SelectionBinding(str(i), name, get_registered_component(name))
                 for i, name in enumerate(StartGameMenuDefaults.page_one, 1)]]


class ActionMenu(PaginatedMenuComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, top_level_prompt_callback=lambda gs: print_and_sleep(get_player_status_view(gs)),
                         main_menu_component=InGameMenu)

    def construct_pages(self) -> List[List[SelectionBinding]]:
        area_actions: AreaActions = self.game_state.current_area.actions_menu
        pages = []
        for page in area_actions.pages:
            modified = [c for c in page]
            if SEARCH in modified:
                if self.game_state.current_area.enemies_remaining == 0:
                    modified.remove(SEARCH)
                    if not self.game_state.current_area.boss_defeated:
                        modified = [AREA_BOSS_FIGHT, *modified]
                    elif self.game_state.is_final_boss_available():
                        modified = [FINAL_BOSS_FIGHT, *modified]
            pages.append(modified)
        return [[SelectionBinding(str(i), name, get_registered_component(name))
                 for i, name in enumerate(spec, 1)] for spec in pages]

    def play_theme(self) -> None:
        self.game_state.play_current_area_theme()

    def can_exit(self) -> bool:
        return self.game_state.victory or not self.game_state.player.is_alive()


class InGameMenu(PaginatedMenuComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, returnable=True)

    def construct_pages(self) -> List[List[SelectionBinding]]:
        page = [c for c in InGameMenuDefaults.page_one]
        if is_debug_mode():
            page += [SAVE_GAME, LOAD_GAME]
        return [[SelectionBinding(str(i), name, get_registered_component(name))
                 for i, name in enumerate(page, 1)]]
