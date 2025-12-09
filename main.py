from api import LabeledSelectionComponent, SelectionBinding
from component.menu import NewGame, LoadGame, QuitGame
from listeners import subscribe_listeners
from model.game_state import GameState


class StartMenu(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[SelectionBinding(key='N', name="New Game", component=NewGame),
                                   SelectionBinding(key='L', name="Load Game", component=LoadGame),
                                   SelectionBinding(key='Q', name="Quit", component=QuitGame)])

if __name__ == '__main__':
    gs = GameState()
    subscribe_listeners(gs)
    StartMenu(gs).run()