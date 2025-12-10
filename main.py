import listeners  # noqa: F401

from api import LabeledSelectionComponent, SelectionBinding
from audio import stop_all_sounds
from component.menu import NewGame, LoadGame, QuitGame
from model.game_state import GameState


class StartMenu(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[SelectionBinding(key='N', name="New Game", component=NewGame),
                                   SelectionBinding(key='L', name="Load Game", component=LoadGame),
                                   SelectionBinding(key='Q', name="Quit", component=QuitGame)])

    def can_exit(self):
        return False


if __name__ == '__main__':

    try:
        gs = GameState()
        StartMenu(gs).run()
    except Exception as e:
        print(e)
        raise e
    finally:
        stop_all_sounds()
