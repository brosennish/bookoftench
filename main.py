from api import LabeledSelectionComponent, SelectionBinding
from audio import stop_all_sounds
from component.actions import Travel
from component.menu import NewGame, LoadGame, QuitGame, ActionMenu
from model.game_state import GameState


class StartMenu(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[SelectionBinding(key='N', name="New Game", component=NewGame),
                                   SelectionBinding(key='L', name="Load Game", component=LoadGame),
                                   SelectionBinding(key='Q', name="Quit", component=QuitGame)])


if __name__ == '__main__':
    try:
        gs = GameState()
        ActionMenu(gs).run()
    except Exception as e:
        print(e)
        raise e
    finally:
        stop_all_sounds()
