from savethewench.audio import stop_all_sounds
from savethewench.component import StartMenu
from savethewench.component.base import Component
from savethewench.model import GameState


class SaveTheWenchGame:

    @staticmethod
    def run():
        try:
            StartMenu(GameState()).run()
        except Exception as e:
            print(e)
            raise e
        finally:
            stop_all_sounds()

    @staticmethod
    def debug_from(component_type: type[Component]):
        try:
            component_type(GameState()).run()
        except Exception as e:
            print(e)
            raise e
        finally:
            stop_all_sounds()
