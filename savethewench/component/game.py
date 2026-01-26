from savethewench.audio import play_sound
from savethewench.component.base import GatekeepingComponent, TextDisplayingComponent, BinarySelectionComponent, \
    LinearComponent
from savethewench.component.menu import ActionMenu
from savethewench.component.menu import StartMenu, QuitGame, Intro
from savethewench.data.audio import DEVIL_THUNDER, GREAT_JOB
from savethewench.model import GameState
from savethewench.ui import red, green
from savethewench.util import print_and_sleep


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
        print_and_sleep(f"You defeated the evil Denny Biltmore and rescued the wench!\n", 1)
        play_sound(GREAT_JOB)
        print_and_sleep(green("You win!"), 3)


class DeathHandler(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         decision_function=lambda: game_state.player.lives > 0,
                         accept_component=ContinueGame,
                         deny_component=GameOver)


class ContinueGame(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         display_callback=self._display_and_reset,
                         next_component=ActionMenu
                         )

    @staticmethod
    def _display_and_reset(game_state: GameState):
        print_and_sleep(red("""
You wake up in a dumpster behind Showgirls 3.
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
