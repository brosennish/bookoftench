import random

from bookoftench import event_logger
from bookoftench.audio import play_music
from bookoftench.component.base import LabeledSelectionComponent, SelectionBinding, ReprBinding, Component, \
    functional_component, GatekeepingComponent
from bookoftench.component.registry import register_component
from bookoftench.data.components import WIZARD
from bookoftench.data.enviroment import DAYTIME
from bookoftench.model import GameState
from bookoftench.model.events import WizardEvent
from bookoftench.model.spell import load_spells, Spell
from bookoftench.model.util import display_wizard_header
from bookoftench.ui import blue, yellow
from bookoftench.util import print_and_sleep


@register_component(WIZARD) # TODO
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
    def _make_purchase_component(spell: Spell) -> type[Component]:
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            player = game_state.player
            if player.coins < spell.cost:
                print_and_sleep(yellow(f"Need more coin"), 2)
                return

            player.coins -= spell.cost
            event_logger.log_event(WizardEvent())
            spell.cast(player)

        return purchase_component
