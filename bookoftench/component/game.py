import sys

from bookoftench.audio import play_sound, stop_all_sounds, play_music
from bookoftench.component.base import GatekeepingComponent, TextDisplayingComponent, BinarySelectionComponent, \
    LinearComponent, Component
from bookoftench.component.menu import ActionMenu
from bookoftench.component.menu import StartMenu
from bookoftench.component.registry import register_component
from bookoftench.data.audio import DEVIL_THUNDER, GREAT_JOB, INTRO_THEME
from bookoftench.data.components import QUIT_GAME, NEW_GAME
from bookoftench.model import GameState
from bookoftench.ui import red, green
from bookoftench.util import print_and_sleep, safe_input


class InitGame(GatekeepingComponent):
    def __init__(self, _: GameState = None):
        super().__init__(GameState(),
                         decision_function=self._decision_function,
                         accept_component=VictoryOrDeathHandler,
                         deny_component=StartMenu)

    def _decision_function(self):
        return self.game_state.victory or not self.game_state.player.is_alive()

    def run(self) -> GameState:
        while True:
            self.game_state = super().run()


class VictoryOrDeathHandler(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         decision_function=self._decision_function,
                         accept_component=VictoryHandler,
                         deny_component=DeathHandler)

    def _decision_function(self):
        if self.game_state.victory:
            return True
        if not self.game_state.player.is_alive():
            return False
        raise Exception(f"{VictoryOrDeathHandler} invoked but neither victory nor death occurred.")


class VictoryHandler(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         display_callback=self._display,
                         next_component=PlayAgainDecision)

    @staticmethod
    def _display(_: GameState):
        print_and_sleep(f"You defeated the evil Denny Biltmore and rescued Chula!\n", 1)
        play_sound(GREAT_JOB)
        print_and_sleep(green("You win!"), 3)


class DeathHandler(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         decision_function=lambda: game_state.player.lives > 0,
                         accept_component=ContinueGame,
                         deny_component=GameOver)


@register_component(NEW_GAME)
class NewGame(LinearComponent):
    def __init__(self, _: GameState):
        super().__init__(GameState(), TutorialDecision)

    def execute_current(self) -> GameState:
        stop_all_sounds()
        player = self.game_state.player
        while not player.name:
            player.name = safe_input("What be your name?")
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
                         query="Need an overview?",
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

    1. Search areas to find discoverables and encounter enemies
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
You wash ashore on a deserted beach on the outskirts of Shebokken.
The champion has informed you that his mother, Chula, was taken in the night.
It is up to you to locate her and return her to the champion...
before her life runs dry.
""")))

    def play_theme(self) -> None:
        play_music(INTRO_THEME)


class ContinueGame(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         display_callback=self._display_and_reset,
                         next_component=ActionMenu
                         )

    @staticmethod
    def _display_and_reset(game_state: GameState):
        print_and_sleep(red("""
You awaken in a dumpster behind Showgirls 3.
You're buried beneath a pile of detritus and covered in slime...
There are parts of another man or men scattered around you."""), 3)
        game_state.player.apply_death_penalties()


class GameOver(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         display_callback=self._display,
                         next_component=PlayAgainDecision)

    @staticmethod
    def _display(_: GameState):
        play_sound(DEVIL_THUNDER)
        print_and_sleep(red("\nGame Over."), 3)
        print_and_sleep(red("\nYou are now in Hell."), 3)


class PlayAgainDecision(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Would you like to play again?",
                         yes_component=NewGameReset,
                         no_component=QuitGame)


class NewGameReset(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         next_component=Intro)

    def execute_current(self) -> GameState:
        name = self.game_state.player.name
        new_game_state = GameState()
        new_game_state.player.name = name
        return new_game_state
