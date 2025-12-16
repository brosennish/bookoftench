import sys
import time as t
from typing import List

from savethewench import event_logger
from savethewench.audio import play_music
from savethewench.component.base import Component, LinearComponent, BinarySelectionComponent, \
    TextDisplayingComponent, LabeledSelectionComponent, SelectionBinding, NoOpComponent, anonymous_component
from savethewench.data.audio import INTRO_THEME
from savethewench.model import GameState
from savethewench.ui import red
from savethewench.util import print_and_sleep
from .actions import UseItem, Travel, EquipWeapon, Explore, Achievements, DisplayPerks, Overview, \
    FightBoss, InGameBank
from .casino import CasinoBouncer
from .shop import ShopComponent
from .util import get_player_status_view


class StartMenu(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[SelectionBinding(key='N', name="New Game", component=NewGame),
                                   SelectionBinding(key='L', name="Load Game", component=LoadGame),
                                   SelectionBinding(key='Q', name="Quit", component=QuitGame)])

    def can_exit(self):
        return not self.game_state.player.is_alive()


class NewGame(LinearComponent):
    def __init__(self, _: GameState):
        super().__init__(GameState(), TutorialDecision)

    def execute_current(self) -> GameState:
        player = self.game_state.player
        while not player.name:
            player.name = input("Name: ")
        return self.game_state


class LoadGame(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self) -> GameState:
        pass


class QuitGame(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self) -> GameState:
        print_and_sleep(red("You'll be back.\nOh... yes.\nYou'll be back."), 1)
        t.sleep(1)
        sys.exit()


class TutorialDecision(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Do tutorial?",
                         yes_component=Tutorial,
                         no_component=Intro)

    def play_theme(self):
        play_music(INTRO_THEME)


class Tutorial(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         next_component=Intro,
                         display_callback=lambda _: print("""
1. Explore areas to find enemies, items, weapons, and coins
2. Fight enemies in turn-based combat
3. Use items to restore HP
4. Weapons have limited uses and can break
5. Defeat enemies to earn XP, coins, and a chance to recover their weapons
6. Leveling up restores HP, boosts stats, and refreshes the shop
7. Visit the shop to buy weapons, items, and perks
8. Travel between areas to search for the wench's hidden location
9. Perks offer special rewards and permanent bonuses
10. Clear the enemies in the wench's area and defeat the final boss to save the wench and win the game
"""))


class Intro(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         next_component=ActionMenu,
                         display_callback=lambda _: print(red("""
You wash up on a beach outside of Shebokken.
The champion feels it in his jines that his wench is in danger.
Find her before her life runs dry...
""")))

    def play_theme(self):
        play_music(INTRO_THEME)


class ActionMenu(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, bindings=self._get_bindings(game_state),
                         top_level_prompt_callback=lambda gs: print(get_player_status_view(gs)))

    @staticmethod
    def _get_bindings(game_state: GameState) -> List[SelectionBinding]:
        res = [SelectionBinding('I', "Use Item", UseItem),
               SelectionBinding('W', "Equip Weapon", EquipWeapon),
               SelectionBinding('S', "Shop", ShopComponent),
               SelectionBinding('T', "Travel", Travel),
               SelectionBinding('M', "More Options", ExtendedActionMenu),
               SelectionBinding('Q', "Main Menu", InGameMenu)]
        if game_state.current_area.enemies_remaining > 0:
            return [SelectionBinding('E', "Explore", Explore), *res]
        elif not game_state.current_area.boss_defeated:
            return [SelectionBinding('B', 'Fight Boss', FightBoss), *res]
        else:
            return res

    def play_theme(self):
        self.game_state.play_current_area_theme()

    def can_exit(self):
        return not self.game_state.player.is_alive()


class ExtendedActionMenu(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, bindings=[
            SelectionBinding('A', "Achievements", Achievements),
            SelectionBinding('B', "Bank", InGameBank),
            SelectionBinding('C', "Casino", CasinoBouncer),
            SelectionBinding('P', "Perks", DisplayPerks),
            SelectionBinding('O', "Overview", Overview),
            SelectionBinding('R', "Return", anonymous_component()(lambda: self._return()))
        ])
        self.leave_menu = False

    def _return(self):
        self.leave_menu = True

    def can_exit(self):
        return self.leave_menu


class SaveGame(NoOpComponent): pass


class InGameMenu(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, bindings=[
            SelectionBinding('N', "New Game", NewGame),
            # TODO signal to go all the way back through the call stack to start new game
            SelectionBinding('S', "Save Game", SaveGame),
            SelectionBinding('L', "Load Game", LoadGame),
            SelectionBinding('R', "Return", anonymous_component()(lambda: self._return())), # TODO clean up duplicate code
            SelectionBinding('Q', "Quit", QuitGame)
        ])
        self.leave_menu = False

    def _return(self):
        self.leave_menu = True

    def can_exit(self):
        return self.leave_menu
