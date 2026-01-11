from savethewench.component.registry import register_component
from savethewench.component.base import functional_component, GatekeepingComponent, BinarySelectionComponent, NoOpComponent
from savethewench.data.components import OFFICER
from savethewench.model import GameState


@register_component(OFFICER)
class OfficerBouncer(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: game_state.officer_active,
                         accept_component=OfficerComponent,
                         deny_component=NoOpComponent)


class OfficerComponent(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Bribe Officer Hohkken",
                         yes_component=functional_component()(lambda: game_state.make_treatment_purchase()),
                         no_component=NoOpComponent,
                         )

    def display_options(self):
        pass

    def play_theme(self):
        pass