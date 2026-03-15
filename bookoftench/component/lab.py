import random

from bookoftench.model.game_state import GameState
from bookoftench.ui import blue, cyan, green, yellow, red
from bookoftench.util import print_and_sleep
from .base import LabeledSelectionComponent, SelectionBinding, \
    GatekeepingComponent, functional_component, TextDisplayingComponent
from .registry import register_component
from .. import event_logger
from ..data.components import LAB
from ..model.events import PlayerDeathEvent
from ..model.player import Player


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
            SelectionBinding('Y', "Yes", functional_component()(lambda: conduct_experiment(game_state.player))),
            SelectionBinding('R', "Risks?", ExperimentRisks),
            SelectionBinding('N', "No thanks", functional_component()(lambda: self._return())),
        ])
        self.leave = False
        print_and_sleep(blue("""Welcome! My name is Dr. Smarsh. 
I can offer you 1 of coin for each experiment I conduct upon you.
What do you say?\n"""))

    def _return(self):
        self.leave = True
        print_and_sleep(f"{blue('Is 1 of coin not enough?')}", 1)

    def can_exit(self) -> bool:
        return self.leave

    def play_theme(self) -> None:
        pass

# --- Risks info ---

class ExperimentRisks(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         next_component=LabComponent,
                         display_callback=lambda _: print_and_sleep(yellow(f"""Risk of Mutation:
Max HP   : 33%
Strength : 25%
Accuracy : 25%
Level    : 18%
Lives    : 8%\n""")))


def conduct_experiment(player: Player):
    player.coins += 1
    mutation = False

    if random.random() < 0.33:
        original = player.max_hp
        amount = random.randint(-6, 5)
        player.max_hp += amount
        if player.hp > player.max_hp:
            player.hp = player.max_hp
        if amount > 0:
            print_and_sleep(green(f"Max HP: {original} -> {player.max_hp}"), 1)
            mutation = True
        elif amount < 0:
            print_and_sleep(yellow(f"Max HP: {original} -> {player.max_hp}"), 1)
            mutation = True

    if random.random() < 0.25:
        original = player.strength
        amount = random.uniform(-0.06, 0.05)
        if amount != 0:
            player.strength = round(player.strength + amount, 2)
            if amount > 0:
                print_and_sleep(green(f"Strength: {original} -> {player.strength}"), 1)
                mutation = True
            elif amount < 0:
                print_and_sleep(yellow(f"Strength: {original} -> {player.strength}"), 1)
                mutation = True

    if random.random() < 0.25:
        original = player.acc
        amount = random.uniform(-0.06, 0.05)
        if amount != 0:
            player.acc = round(player.acc + amount, 2)
            if amount > 0:
                print_and_sleep(green(f"Accuracy: {original} -> {player.acc}"), 1)
                mutation = True
            elif amount < 0:
                print_and_sleep(yellow(f"Accuracy: {original} -> {player.acc}"), 1)
                mutation = True

    if random.random() < 0.18:
        original = player.lvl
        amount = random.randint(-1, 2)
        player.lvl += amount
        if player.lvl <= 0:
            player.lvl = 1
        if original != player.lvl:
            if amount > 0:
                print_and_sleep(cyan(f"Level: {original} -> {player.lvl}"), 1)
                mutation = True
            elif amount < 0:
                print_and_sleep(cyan(f"Level: {original} -> {player.lvl}"), 1)
                mutation = True

    if random.random() < 0.08:
        original = player.lives
        amount = 1
        if random.random() < 0.55:
            amount = -1
        player.lives += amount
        if player.lives >= 1:
            if amount > 0:
                print_and_sleep(cyan(f"Lives: {original} -> {player.lives}"), 1)
                mutation = True
            elif amount < 0:
                print_and_sleep(red(f"Lives: {original} -> {player.lives}"), 1)
                mutation = True
        if player.lives <= 0:
            event_logger.log_event(PlayerDeathEvent(player.lives))

    if not mutation and player.lives > 0:
        print_and_sleep(blue("Experiment was a bust."), 1)
