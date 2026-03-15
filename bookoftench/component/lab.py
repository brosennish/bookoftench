from bookoftench.model.game_state import GameState
from bookoftench.ui import blue, cyan, green, orange, purple, yellow, dim, red
from bookoftench.util import print_and_sleep, safe_input
from .base import LabeledSelectionComponent, SelectionBinding, \
    GatekeepingComponent, functional_component, Component, TextDisplayingComponent
from .registry import register_component
from ..data.components import LAB


@register_component(LAB)
class LabWorldState(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: game_state.lab_active,
                         accept_component=LabComponent,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             blue("The laboratory is closed for decontamination.\n"), 1.5)))

# --- Casino menu ---

class LabComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, bindings=[
            SelectionBinding('Y', "Yes", Experiment),
            SelectionBinding('R', "Risks", ExperimentRisks),
            SelectionBinding('N', "No thanks", functional_component()(lambda: self._return())),
        ])
        self.leave_lab = False
        print_and_sleep("""Welcome! I am Dr. Smarsh. 
        I can offer you 5 of coin to conduct an experiment upon you.
        What do you say?\n""")

    def _return(self):
        self.leave_lab = True

    def can_exit(self) -> bool:
        return self.leave_lab

    def play_theme(self) -> None:
        pass


# --- Experiment class ---

class Experiment(Component):
    pass

# --- Risks info ---

class ExperimentRisks(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         next_component=Experiment,
                         display_callback=lambda _: print_and_sleep("""Risk of Mutation:
Max HP   : 33%
Strength : 25%
Accuracy : 25%
Level    : 16%
Lives    : 7%\n"""))
