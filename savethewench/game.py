import random

from savethewench.audio import stop_all_sounds
from savethewench.component import InitGame
from savethewench.component.base import Component
from savethewench.model import GameState
from savethewench.model.perk import load_perks
from savethewench.util import print_and_sleep


class SaveTheWenchGame:

    @staticmethod
    def run():
        try:
            InitGame().run()
        except KeyboardInterrupt:
            print_and_sleep("\nExiting...", 1)
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
            player.name = "debug"
            player.coins = 1000
            # for weapon in load_discoverable_weapons():
            #     player.weapon_dict[weapon.name] = weapon
            component_type(game_state).run()
        except KeyboardInterrupt:
            print_and_sleep("\nExiting...", 1)
        except Exception as e:
            print(e)
            raise e
        finally:
            stop_all_sounds()
