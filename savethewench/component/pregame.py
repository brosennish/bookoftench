from savethewench.audio import play_sound, stop_all_sounds
from savethewench.component.base import GatekeepingComponent, TextDisplayingComponent, BinarySelectionComponent, \
    LinearComponent
from savethewench.component.menu import ActionMenu
from savethewench.component.menu import StartMenu, QuitGame, Intro
from savethewench.data.audio import DEVIL_THUNDER
from savethewench.event_logger import subscribe_function
from savethewench.model import GameState
from savethewench.model.events import PlayerDeathEvent
from savethewench.ui import red
from savethewench.util import print_and_sleep


class InitGame(GatekeepingComponent):
    def __init__(self, game_state: GameState = GameState()):
        self.handle_death = False
        super().__init__(game_state,
                         decision_function=lambda: _decision_function(),
                         accept_component=DeathHandler,
                         deny_component=StartMenu)

        @subscribe_function(PlayerDeathEvent)
        def handle_death_event(_: PlayerDeathEvent):
            self.handle_death = True

        def _decision_function():
            if self.handle_death:
                self.handle_death = False
                return True
            return False

    def run(self) -> GameState:
        while True:
            if not self.handle_death:
                stop_all_sounds()
            self.game_state = super().run()


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
