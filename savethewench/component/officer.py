from savethewench.component.registry import register_component
from savethewench.component.base import functional_component, GatekeepingComponent, BinarySelectionComponent, NoOpComponent
from savethewench.data.components import OFFICER
from savethewench.data.perks import BROWNMAIL
from savethewench.model import GameState
from savethewench.model.perk import perk_is_active
from savethewench.model.util import display_officer_header, display_officer_message
from savethewench.util import print_and_sleep


@register_component(OFFICER)
class OfficerBouncer(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: not perk_is_active(BROWNMAIL),
                         accept_component=OfficerComponent,
                         deny_component=NoOpComponent
                         )


class OfficerComponent(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Bribe Officer Hohkken",
                         yes_component=functional_component()(lambda: game_state.obey_officer()),
                         no_component=functional_component()(lambda: game_state.disobey_officer()),
                         )

    def display_options(self):
        print(display_officer_header(self.game_state))
        print(display_officer_message())
        print_and_sleep(f"{self.query.strip()} (y/n)?")


    def play_theme(self):
        pass