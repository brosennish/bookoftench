from savethewench.audio import play_music
from savethewench.component.registry import register_component
from savethewench.component.base import functional_component, GatekeepingComponent, BinarySelectionComponent, NoOpComponent
from savethewench.data.audio import SHOP_THEME
from savethewench.data.components import HOSPITAL
from savethewench.model import GameState
from savethewench.model.util import display_hospital_header, display_hospital_intro
from savethewench.ui import blue
from savethewench.util import print_and_sleep

@register_component(HOSPITAL)
class HospitalBouncer(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: game_state.player.illness is not None,
                         accept_component=HospitalComponent,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             blue("Come back when you have something we can make money from.\n"), 1.5)))


class HospitalComponent(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Pay for treatment",
                         yes_component=functional_component()(lambda: game_state.make_treatment_purchase()),
                         no_component=NoOpComponent,
                         )
        self.exit_hospital = False

    def display_options(self):
        print(display_hospital_intro())
        print(display_hospital_header(self.game_state))
        print_and_sleep(f"{self.query.strip()} (y/n)?")

    def play_theme(self):
        play_music(SHOP_THEME)

    def _return(self):
        self.exit_hospital = True
        print_and_sleep(blue("You'll be back!"), 1)

    def can_exit(self):
        return (self.exit_hospital
                or not self.game_state.player.is_alive()
                or not self.game_state.player.is_sick())

    @staticmethod
    def _make_purchase_component():
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            game_state.make_treatment_purchase()

        return purchase_component