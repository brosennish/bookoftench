import random

from bookoftench.model.game_state import GameState
from bookoftench.ui import blue, cyan, green, yellow, dim
from bookoftench.util import print_and_sleep
from .base import LabeledSelectionComponent, SelectionBinding, \
    GatekeepingComponent, functional_component, TextDisplayingComponent
from .game import ContinueGame, DeathHandler
from .registry import register_component
from .. import event_logger
from ..audio import play_music
from ..data.audio import LAB_THEME
from ..data.components import LAB
from ..data.environment import NIGHT
from ..model.events import PlayerDeathEvent

# ================================================================================================

# --- check if lab is open ---

@register_component(LAB)
class LabBounder(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: game_state.time_of_day == NIGHT,
                         accept_component=LabComponent,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             blue("The laboratory is closed during the day.\n"), 1.5)))

# ================================================================================================

class LabComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, bindings=[
            SelectionBinding('E', "Experiment", functional_component()(lambda: conduct_experiment(self.game_state))),
            SelectionBinding('R', "Risks", ExperimentRisks),
            SelectionBinding('N', "No thanks", functional_component()(lambda: self._return())),
        ])
        self.leave = False
        print_and_sleep(blue("""Welcome! My name is Dr. Smarsh. 
I conduct experiments on human beings.
Interested? I pay one of coin per trial.\n"""))

    def play_theme(self) -> None:
        play_music(LAB_THEME)

    def _return(self):
        self.leave = True
        print_and_sleep(f"{blue('Is 1 of coin not enough?')}", 1)

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

# ================================================================================================

class ExperimentRisks(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         next_component=LabComponent,
                         display_callback=lambda _: print_and_sleep(yellow(f"""Risk of Mutation:
Strength : 23%
Accuracy : 23%
Max HP   : 21%
Lives    : 7%\n""")))

# ================================================================================================

def conduct_experiment(game_state: GameState) -> GameState:
    player = game_state.player
    player.gain_coins(1)
    mutation = False

    # ============================
    #          STRENGTH
    # ============================

    if random.random() < 0.23:
        original = player.strength
        amount = random.uniform(-0.03, 0.03)
        player.strength = round(player.strength + amount, 2)

        if original != player.strength:
            if amount > 0:
                print_and_sleep(green(f"Strength: {original} -> {player.strength}"), 1)
                player.gain_or_lose_luck(0.1)
                mutation = True
            elif amount < 0:
                print_and_sleep(yellow(f"Strength: {original} -> {player.strength}"), 1)
                player.gain_or_lose_luck(-0.1)
                mutation = True

    # ============================
    #          ACCURACY
    # ============================

    if random.random() < 0.23:
        original = player.acc
        amount = random.uniform(-0.03, 0.03)
        player.acc = round(player.acc + amount, 2)

        if original != player.acc:
            if amount > 0:
                print_and_sleep(green(f"Accuracy: {original} -> {player.acc}"), 1)
                player.gain_or_lose_luck(0.1)
                mutation = True
            elif amount < 0:
                print_and_sleep(yellow(f"Accuracy: {original} -> {player.acc}"), 1)
                player.gain_or_lose_luck(-0.1)
                mutation = True

    # ============================
    #            MAX HP
    # ============================

    if random.random() < 0.21:
        original = player.max_hp
        amount = random.randint(-3, 3)
        player.max_hp += amount

        if player.hp > player.max_hp:
            player.hp = player.max_hp

        if amount > 0:
            print_and_sleep(green(f"Max HP: {original} -> {player.max_hp}"), 1)
            player.gain_or_lose_luck(0.1)
            mutation = True
        elif amount < 0:
            print_and_sleep(yellow(f"Max HP: {original} -> {player.max_hp}"), 1)
            player.gain_or_lose_luck(-0.1)
            mutation = True

    # ============================
    #            LIVES
    # ============================

    if random.random() < 0.07:
        original = player.lives
        amount = 1

        if random.random() < 0.67 - player.luck:
            player.gain_or_lose_luck(-0.25)
            amount = -1
        else:
            player.gain_or_lose_luck(0.25)

            if player.lives == 5:
                amount = 0

        player.lives += amount

        if player.lives >= 1 and amount != 0:
            print_and_sleep(cyan(f"Lives: {original} -> {player.lives}"), 1)
            mutation = True

        if player.lives <= 0:
            event_logger.log_event(PlayerDeathEvent(player.lives))
            return DeathHandler(game_state).run()

    # ============================
    #         NO MUTATION
    # ============================

    if not mutation and player.lives > 0:
        print_and_sleep(dim("No mutations occurred."), 1)

    return game_state
