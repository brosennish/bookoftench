from savethewench.component.base import GatekeepingComponent
from savethewench.component.game import VictoryOrDeathHandler
from savethewench.component.menu import ActionMenu
from savethewench.model import GameState


# Component only to be used for initializing game in "debug mode"
class DebugInit(GatekeepingComponent):
    def __init__(self, game_state):
        super().__init__(game_state,
                         decision_function=self._decision_function,
                         accept_component=VictoryOrDeathHandler,
                         deny_component=ActionMenu)

    def _decision_function(self):
        return self.game_state.victory or not self.game_state.player.is_alive()

    def run(self) -> GameState:
        while True:
            self.game_state = super().run()