import os
import pickle
import sys
from functools import partial
from typing import List

from savethewench.audio import play_music
from savethewench.component.base import Component, LinearComponent, BinarySelectionComponent, \
    TextDisplayingComponent, LabeledSelectionComponent, SelectionBinding, functional_component, NoOpComponent
from savethewench.data.audio import INTRO_THEME
from savethewench.model import GameState
from savethewench.model.util import get_player_status_view
from savethewench.ui import red, purple, cyan
from savethewench.util import print_and_sleep, safe_input
from .actions import UseItem, Travel, EquipWeapon, Explore, Achievements, DisplayPerks, Overview, \
    FightBoss, FightFinalBoss
from .bank import WithdrawalOnlyBank
from .casino import CasinoBouncer
from .coffee_shop import CoffeeShopComponent, CoffeeBouncer
from .shop import ShopComponent


class StartMenu(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[SelectionBinding(key='N', name="New Game", component=NewGame),
                                   SelectionBinding(key='L', name="Load Game", component=LoadGame),
                                   SelectionBinding(key='Q', name="Quit", component=QuitGame)])

    def can_exit(self):
        return self.game_state.victory or not self.game_state.player.is_alive()


class NewGame(LinearComponent):
    def __init__(self, _: GameState):
        super().__init__(GameState(), TutorialDecision)

    def execute_current(self) -> GameState:
        player = self.game_state.player
        while not player.name:
            player.name = safe_input("What is your name?")
        return self.game_state


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

    def play_theme(self):
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
You wash up on a beach outside of Shebokken.
The champion feels it in his jines that his wench is in danger.
Find her before her life runs dry...
""")))

    def play_theme(self):
        play_music(INTRO_THEME)


class ActionMenu(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, refresh_menu=True, bindings=self._get_bindings(game_state),
                         top_level_prompt_callback=lambda gs: print_and_sleep(get_player_status_view(gs)))

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
        elif game_state.is_final_boss_available():
            return [SelectionBinding('B', purple("BATTLE DENNY BILTMORE"), FightFinalBoss), *res]
        else:
            return res

    def play_theme(self):
        self.game_state.play_current_area_theme()

    def can_exit(self):
        return self.game_state.victory or not self.game_state.player.is_alive()


class ExtendedActionMenu(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        bindings=[
            SelectionBinding('A', "Achievements", Achievements),
            SelectionBinding('B', "Bank", WithdrawalOnlyBank),
            SelectionBinding('C', "Casino", CasinoBouncer),
            SelectionBinding('P', "Perks", DisplayPerks),
            SelectionBinding('O', "Overview", Overview)
            ]
        if game_state.current_area.name == "City" and not game_state.player.is_sick():
            bindings.append(SelectionBinding('S', "Coffee Shop", CoffeeBouncer))
            # TODO clean up duplicated code
        bindings.append(
            SelectionBinding('R', "Return", functional_component()(lambda: self._return()))
        )
        super().__init__(game_state, bindings=bindings)
        self.leave_menu = False

    def _return(self):
        self.leave_menu = True

    def can_exit(self):
        return self.leave_menu

    def play_theme(self):
        self.game_state.play_current_area_theme()


class InGameMenu(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, bindings=[
            # TODO signal to go all the way back through the call stack to start new game
            SelectionBinding('N', "New Game", NewGame),
            SelectionBinding('S', "Save Game", SaveGame),
            SelectionBinding('L', "Load Game", LoadGame),
            # TODO clean up duplicated code
            SelectionBinding('R', "Return", functional_component()(lambda: self._return())),
            SelectionBinding('Q', "Quit", QuitGame)
        ])
        self.leave_menu = False

    def _return(self):
        self.leave_menu = True

    def can_exit(self):
        return self.leave_menu

_SAVE_DIR = ".saves" # TODO don't just save straight to a directory in the repo

class SaveGame(Component):
    def run(self) -> GameState:
        save_file = f"{self.game_state.player.name}.tench"

        if not os.path.isdir(_SAVE_DIR):
            os.mkdir(_SAVE_DIR)
        with open(f"{_SAVE_DIR}/{save_file}", "wb") as f:  # noinspection PyTypeChecker
            pickle.dump(self.game_state, f)

        print_and_sleep(cyan("Game saved."), 1)
        return self.game_state


class LoadGame(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.save_file = None

    def set_save_file(self, save_file: str):
        self.save_file = save_file

    def run(self) -> GameState:
        saves = dict((str(i), n) for (i, n) in enumerate(set(fn.split(".")[0] for fn in os.listdir(_SAVE_DIR)))) \
            if os.path.isdir(_SAVE_DIR) else {}
        if len(saves) == 0:
            print_and_sleep(red("No saved games exist."))
            return self.game_state

        self.game_state = LabeledSelectionComponent(self.game_state, bindings=[
            SelectionBinding(str(i), fn.split(".")[0], functional_component()(
                partial(self.set_save_file, f"{_SAVE_DIR}/{fn}")))
            for (i, fn) in enumerate(sorted(os.listdir(_SAVE_DIR)), 1)
        ], quittable=True).run()
        if self.save_file is not None:
            with open(self.save_file, "rb") as f:
                self.game_state = pickle.load(f)
            return ActionMenu(self.game_state).run()
        return self.game_state
