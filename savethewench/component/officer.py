import random
from dataclasses import dataclass

from savethewench import event_logger
from savethewench.audio import play_music, play_sound
from savethewench.component.base import functional_component, BinarySelectionComponent, ConditionalComponent
from savethewench.component.registry import register_component
from savethewench.data.audio import OFFICER_THEME, BLUNT
from savethewench.data.components import OFFICER
from savethewench.data.perks import BROWNMAIL
from savethewench.data.weapons import SPECIAL
from savethewench.event_base import EventType
from savethewench.model import GameState
from savethewench.model.enemy import Enemy
from savethewench.model.events import OfficerEvent
from savethewench.model.perk import attach_perk
from savethewench.model.util import p_color
from savethewench.model.weapon import Weapon
from savethewench.ui import dim, yellow, green, purple, blue
from savethewench.util import print_and_sleep


@register_component(OFFICER)
class OfficerEncounterDecision(ConditionalComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=is_officer_lurking,
                         component=OfficerEncounter)


class OfficerEncounter(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Bribe Officer Hohkken",
                         yes_component=obey_officer,
                         no_component=disobey_officer,
                         )
        self.greeting_displayed = False

    def play_theme(self):
        play_music(OFFICER_THEME)

    @staticmethod
    def _display_greeting() -> None:
        lines = ["Hey ther'... uh...", "This is Officer Hohkken.", "I'm, uh...", "gonna need you to cough up some coin",
                 "or else I'll, uh...", "have to rough you up a bit ther'.\n"]
        for l in lines:
            print_and_sleep(blue(l), random.choice([1, 1.5, 2]))

    def _display_header(self) -> None:
        player = self.game_state.player
        player_color = p_color(player.hp, player.max_hp)

        print_and_sleep(dim(" | ").join([
            f"Lives: {yellow(player.lives)}",
            f"HP: {player_color(f'{player.hp}/{player.max_hp}')}",
            f"Coins: {green(player.coins)}",
            f"Bribe: {purple(calculate_bribe(self.game_state))}",
        ]))

    def display_options(self):
        if not self.greeting_displayed:
            self._display_greeting()
            self.greeting_displayed = True
        self._display_header()
        super().display_options()


@attach_perk(BROWNMAIL)
def is_officer_lurking() -> bool:
    return random.random() < 0.08


def calculate_bribe(game_state: GameState):
    return min(game_state.player.lvl * 10, 50)


@functional_component(state_dependent=True)
def obey_officer(game_state: GameState):
    if game_state.player.coins >= calculate_bribe(game_state):
        game_state.player.coins -= calculate_bribe(game_state)
        event_logger.log_event(OfficerEvent(EventType.OFFICER_PAID))
    else:
        disobey_officer(game_state).run()


@functional_component(state_dependent=True)
def disobey_officer(game_state: GameState):
    player = game_state.player
    OfficerHohkken(calculate_bribe(game_state)).handle_hit(player)
    event_logger.log_event(OfficerEvent(EventType.OFFICER_UNPAID))

@dataclass
class PoliceBrutality(Weapon):
    name: str = "Police Brutality"
    damage: int = 0
    uses: int = -1
    accuracy: float = 1.0
    spread: int = 0
    crit: float = 0.0
    cost: int = 0
    sell_value: int = 0
    type: str = SPECIAL
    sound: str = BLUNT

    def use(self) -> None:
        play_sound(self.sound)

class OfficerHohkken(Enemy):
    def __init__(self, bribe: int):
        self.name: str = 'Officer Hohkken'
        self.hp: int = 100
        self.current_weapon: Weapon = PoliceBrutality()
        self.current_weapon.damage = random.randint(5, bribe)
        self.random_dialogue = [] # TODO maybe add some here?
