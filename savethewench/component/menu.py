import sys
from typing import List

from savethewench.audio import play_music, stop_all_sounds
from savethewench.component.base import Component, LinearComponent, BinarySelectionComponent, \
    TextDisplayingComponent, SelectionBinding, PaginatedMenuComponent
from savethewench.data.audio import INTRO_THEME
from savethewench.data.components import EXPLORE, AREA_BOSS_FIGHT, FINAL_BOSS_FIGHT, NEW_GAME, QUIT_GAME, \
    InGameMenuDefaults, StartGameMenuDefaults
from savethewench.model import GameState
from savethewench.model.area import AreaActions
from savethewench.model.util import get_player_status_view
from savethewench.ui import red
from savethewench.util import print_and_sleep, safe_input
from .registry import get_registered_component, register_component


class StartMenu(PaginatedMenuComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def construct_pages(self) -> List[List[SelectionBinding]]:
        return [[SelectionBinding(str(i), name, get_registered_component(name))
                 for i, name in enumerate(StartGameMenuDefaults.page_one, 1)]]


@register_component(NEW_GAME)
class NewGame(LinearComponent):
    def __init__(self, _: GameState):
        super().__init__(GameState(), TutorialDecision)

    def execute_current(self) -> GameState:
        stop_all_sounds()
        player = self.game_state.player
        while not player.name:
            player.name = safe_input("What is your name?")
        return self.game_state


@register_component(QUIT_GAME)
class QuitGame(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self) -> GameState:
        print_and_sleep(red("You'll be back.\nOh... yes.\nYou'll be back."), 1)
        sys.exit()


class TutorialDecision(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Do tutorial?",
                         yes_component=Tutorial,
                         no_component=Intro)

    def play_theme(self) -> None:
        play_music(INTRO_THEME)


class Tutorial(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         next_component=Intro,
                         display_callback=lambda _: print_and_sleep("""
SAVE THE WENCH - HOW TO PLAY

    1. Explore areas to find enemies, loot, perks, and events
    2. Fight enemies in turn-based combat to earn XP and coins
    3. Buy and sell items and weapons in the shop
    4. Use items freely during your turn or between battles
    5. Gain perks that permanently affect combat, coins, or luck
    6. Play casino games to risk coins for big rewards
    7. Store coins in the bank to earn interest upon level-up
    8. Each area has a boss and a hidden number of enemies
    9. Clear the wench’s area to unlock the final showdown
    10. Defeat the final boss to save the wench and win the game
"""))


class Intro(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         next_component=ActionMenu,
                         display_callback=lambda _: print_and_sleep(red("""
You swim up to a rocky beach with nothing but your knife and a tench.
The champion informed you that a wench has been captured - he can feel it in his jines.
Save her before her life runs dry...
""")))

    def play_theme(self) -> None:
        play_music(INTRO_THEME)


class ActionMenu(PaginatedMenuComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, top_level_prompt_callback=lambda gs: print_and_sleep(get_player_status_view(gs)),
                         main_menu_component=InGameMenu)

    def construct_pages(self) -> List[List[SelectionBinding]]:
        area_actions: AreaActions = self.game_state.current_area.actions_menu
        pages = []
        for page in area_actions.pages:
            modified = [c for c in page]
            if EXPLORE in modified:
                if self.game_state.current_area.enemies_remaining == 0:
                    modified.remove(EXPLORE)
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
        return [[SelectionBinding(str(i), name, get_registered_component(name))
                 for i, name in enumerate(InGameMenuDefaults.page_one, 1)]]
