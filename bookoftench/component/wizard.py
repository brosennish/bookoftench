import random

from bookoftench import event_logger
from bookoftench.component.base import LabeledSelectionComponent, SelectionBinding, ReprBinding, Component, \
    functional_component, GatekeepingComponent
from bookoftench.component.registry import register_component
from bookoftench.data.components import WIZARD
from bookoftench.data.spells import Wizard_Lines, WEAPON, ITEM
from bookoftench.model import GameState
from bookoftench.model.events import WizardEvent
from bookoftench.model.spell import load_spells, Spell
from bookoftench.model.util import display_wizard_header
from bookoftench.ui import blue, yellow
from bookoftench.util import print_and_sleep


@register_component(WIZARD)
class WizardBouncer(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        player = game_state.player
        super().__init__(game_state, decision_function=lambda: player.coins >= 30,
                         accept_component=WizardComponent,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             blue("Come back when you have 30 of coin!\nI gotta take a wiz anyway."), 1.5)))


class WizardComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        spell_options = load_spells()

        spell_bindings = [ReprBinding(str(i + 1), spell.name, self._make_purchase_component(spell), spell) for
                          i, spell in enumerate(spell_options)]
        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))
        super().__init__(game_state, refresh_menu=True,
                         bindings=[*spell_bindings, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                spell_bindings,
                top_level_prompt_callback=display_wizard_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [return_binding]
            ),
        ]
        self.leave = False

    def _return(self):
        self.leave = True
        print_and_sleep(f"{blue('Hush, mortal. Be gone with you.')}", 1)

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

    def display_options(self) -> None:
        message = random.choice(Wizard_Lines)
        print_and_sleep(
            f"{blue(message)}", 1.5
        )
        for component in self.selection_components:
            component.display_options()

    @staticmethod
    def _make_purchase_component(spell: Spell) -> type[Component]:
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            player = game_state.player
            if player.coins < spell.cost:
                print_and_sleep(yellow(f"Need more coin"), 2)
                return
            if spell.type == WEAPON:
                if len(player.get_weapons()) == player.max_weapons:
                    print_and_sleep(yellow(f"No room in sack"), 2)
                    return
            if spell.type == ITEM:
                if len(player.items) == player.max_items:
                    print_and_sleep(yellow(f"No room in sack"), 2)
                    return

            player.coins -= spell.cost
            event_logger.log_event(WizardEvent())
            spell.cast(player)

        return purchase_component
