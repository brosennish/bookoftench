import random

from savethewench.audio import stop_all_sounds
from savethewench.component import StartMenu
from savethewench.component.base import Component
from savethewench.model import GameState
from savethewench.model.perk import load_perks


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
            for perk in load_perks():
                perk._active = True
            game_state = GameState()
            player = game_state.player
            random.seed(666)
            player.name = "debug"
            player.coins = 1000
            # for weapon in load_discoverable_weapons():
            #     player.weapon_dict[weapon.name] = weapon
            component_type(game_state).run()
        except Exception as e:
            print(e)
            raise e
        finally:
            stop_all_sounds()
