from savethewench.component import LabeledSelectionComponent, SelectionBinding, ReprBinding, Component, \
    functional_component, register_component
from savethewench.data.components import OCCULTIST
from savethewench.model import GameState
from savethewench.model.ritual import Ritual, ritual_inventory, apply_ritual_effect
from savethewench.model.util import display_occultist_header
from savethewench.ui import blue, yellow
from savethewench.util import print_and_sleep


@register_component(OCCULTIST)
class OccultistComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        ritual_options = ritual_inventory()

        ritual_bindings = [ReprBinding(str(i + 1), ritual.name, self._make_purchase_component(ritual), ritual) for
                         i, ritual in enumerate(ritual_options)]
        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))
        super().__init__(game_state, refresh_menu=True,
                         bindings=[*ritual_bindings, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                ritual_bindings,
                top_level_prompt_callback=display_occultist_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [return_binding]
            ),
        ]
        self.leave = False

    def _return(self):
        self.leave = True
        print_and_sleep(f"{blue('Farewell.')}", 1)

    def can_exit(self) -> bool:
        return (self.leave
                or not self.game_state.player.is_alive()
                )

    def display_options(self) -> None:
        print_and_sleep(
            f"{blue('Tench magic gives life, Carp magic might. Shall I perform a ritual?')}"
        )
        for component in self.selection_components:
            component.display_options()

    @staticmethod
    def _make_purchase_component(ritual: Ritual) -> type[Component]:
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            player = game_state.player
            if player.coins < ritual.cost:
                print_and_sleep(yellow(f"Need more coin"), 1)
            else:
                player.coins -= ritual.cost
                apply_ritual_effect(ritual, player)

        return purchase_component