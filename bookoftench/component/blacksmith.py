import random

from bookoftench import event_logger
from bookoftench.audio import play_music, play_sound
from bookoftench.component.base import LabeledSelectionComponent, SelectionBinding, ReprBinding, Component, \
    functional_component, GatekeepingComponent
from bookoftench.component.registry import register_component
from bookoftench.data.audio import PURCHASE
from bookoftench.data.components import WIZARD, BLACKSMITH
from bookoftench.data.enviroment import DAYTIME
from bookoftench.data.weapons import BLIND, SPECIAL
from bookoftench.model import GameState
from bookoftench.model.events import WizardEvent
from bookoftench.model.player import PlayerWeapon
from bookoftench.model.spell import load_spells, Spell
from bookoftench.model.util import display_wizard_header
from bookoftench.model.weapon import load_weapons, make_elite_weapon, load_weapon
from bookoftench.ui import blue, yellow, cyan
from bookoftench.util import print_and_sleep


@register_component(BLACKSMITH)
class BlacksmithBouncer(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        player = game_state.player
        super().__init__(game_state, decision_function=lambda: player.coins >= 120,
                         accept_component=BlacksmithSleeping,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             blue("Come back when you have 120 of coin.\nHTH isn't cheap."), 1.5)))

class BlacksmithSleeping(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: game_state.time_of_day == DAYTIME,
                         accept_component=BlacksmithComponent,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             blue("Sledge Jr. is resting his fishy muscles."), 1.5)))

# TODO - build component
class BlacksmithComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        player = game_state.player
        valid = [i for i in player.weapon_dict.values() if i.type not in [BLIND, SPECIAL]]
        if not valid:
            print_and_sleep(yellow("Sledge Jr. does not work on special or blind-type weapons."))

        weapon_bindings = [ReprBinding(str(i + 1), weapon.name, self._make_purchase_component(weapon), weapon) for
                          i, weapon in enumerate(valid)]

        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*weapon_bindings, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                weapon_bindings,
                top_level_prompt_callback=display_blacksmith_header, # TODO - add header
            ),
            LabeledSelectionComponent(
                game_state,
                [return_binding]
            ),
        ]
        self.leave = False

    def play_theme(self) -> None:
        play_music(BLACKSMITH_THEME) # TODO - add theme

    def _return(self):
        self.leave = True
        print_and_sleep(f"{blue("Come back soon. I need coins for HTH.")}", 1)

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

    def display_options(self) -> None:
        message = random.choice(Blacksmith_Lines) # TODO - add lines
        print_and_sleep(
            f"{blue(message)}", 1.5
        )
        for component in self.selection_components:
            component.display_options()

    # TODO - add conversion logic
    @staticmethod
    def _make_purchase_component(weapon: PlayerWeapon) -> type[Component]:
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            player = game_state.player
            if player.coins < 120:
                print_and_sleep(yellow(f"Need more coin"), 2)
                return

            player.coins -= 120
            play_sound(PURCHASE)
            event_logger.log_event(BlacksmithEvent()) # TODO - add event
            forge_weapon(weapon, game_state)

        return purchase_component


def forge_weapon(weapon: PlayerWeapon, game_state) -> None:
    player = game_state.player
    name = weapon.name # log name
    og_uses = weapon.uses # log uses
    player.weapon_dict.pop([name, weapon]) # remove weapon
    base = load_weapon(name) # recreate Weapon object
    base.uses = og_uses # restore uses
    elite = make_elite_weapon(base) # convert to elite weapon
    player.weapon_dict.update({elite.name: PlayerWeapon.from_weapon(elite)}) # add to weapon_dict
    player.current_weapon = next(i for i in player.weapon_dict.values() if i.name == elite.name) # set current

    print_and_sleep(cyan(f"{name} has been upgraded."), 1.5)

