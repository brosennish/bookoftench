from bookoftench.component import TextDisplayingComponent
from bookoftench.model import GameState
from bookoftench.model.util import display_wanted_enemy


class DisplayWanted(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_wanted_enemy)