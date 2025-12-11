from savethewench.component import StartMenu
from savethewench.audio import stop_all_sounds
from savethewench.model import GameState


class SaveTheWenchGame:

    @staticmethod
    def run():
        try:
            gs = GameState()
            StartMenu(gs).run()
        except Exception as e:
            print(e)
            raise e
        finally:
            stop_all_sounds()
