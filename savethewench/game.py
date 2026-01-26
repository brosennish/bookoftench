from savethewench.audio import stop_all_sounds
from savethewench.component import InitGame
from savethewench.component.base import Component
from savethewench.data.components import CRYPTO_EXCHANGE
from savethewench.model import GameState
from savethewench.model.perk import load_perks
from savethewench.model.player import PlayerWeapon
from savethewench.model.weapon import load_discoverable_weapons
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
            game_state = GameState()
            for perk in load_perks():
                perk._active = True
            player = game_state.player
            player.name = "debug"
            player.coins = 10000
            player.max_hp = 1000
            player.hp = player.max_hp
            player.xp = 99
            for weapon in load_discoverable_weapons():
                player.weapon_dict[weapon.name] = PlayerWeapon.from_weapon(weapon)
            for area in game_state.areas:
                if area.name == "City":
                    area.actions_menu.pages[-1].append(CRYPTO_EXCHANGE)
            component_type(game_state).run()
        except KeyboardInterrupt:
            print_and_sleep("\nExiting...", 1)
        except Exception as e:
            print(e)
            raise e
        finally:
            stop_all_sounds()
