import random
from dataclasses import dataclass, field

from bookoftench import event_logger
from bookoftench.audio import play_music, play_sound
from bookoftench.component.base import functional_component, BinarySelectionComponent, ConditionalComponent
from bookoftench.component.registry import register_component
from bookoftench.data.audio import OFFICER_THEME, BLUNT
from bookoftench.data.components import OFFICER
from bookoftench.data.perks import BROWNMAIL
from bookoftench.data.weapons import SPECIAL
from bookoftench.event_base import EventType
from bookoftench.model import GameState
from bookoftench.model.enemy import Enemy
from bookoftench.model.events import OfficerEvent
from bookoftench.model.perk import attach_perk
from bookoftench.model.util import p_color
from bookoftench.model.weapon import Weapon
from bookoftench.ui import dim, yellow, green, purple, blue
from bookoftench.util import print_and_sleep

# ================================================================================================

# --- check if officer is lurking ---

@register_component(OFFICER)
class OfficerEncounterDecision(ConditionalComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         decision_function=self._is_officer_lurking,
                         component=OfficerEncounter)

    def _is_officer_lurking(self) -> bool:
        return OfficerEncounter(self.game_state).is_officer_lurking()

# ================================================================================================

class OfficerEncounter(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Bribe Officer Hohkken",
                         yes_component=obey_officer,
                         no_component=disobey_officer,
                         )
        self.greeting_displayed = False

    def play_theme(self) -> None:
        play_music(OFFICER_THEME)

    @staticmethod
    def _display_greeting() -> None:
        lines = [
            "Hey ther'... uh...",
            "This is Officer Hohkken.",
            "I'm, uh...",
            "gonna need you to cough up some coin",
            "or else I'll, uh...",
            "have to rough you up a bit ther'.\n",
        ]

        for line in lines:
            print_and_sleep(blue(line), random.choice([1, 1.5, 2]))

    def _display_header(self) -> None:
        player = self.game_state.player
        player_color = p_color(player.hp, player.max_hp)

        print_and_sleep(dim(" | ").join([
            f"Lives: {yellow(player.lives)}",
            f"HP: {player_color(f'{player.hp}/{player.max_hp}')}",
            f"Coins: {green(player.coins)}",
            f"Bribe: {purple(calculate_bribe(self.game_state))}",
        ]))

    def display_options(self) -> None:
        if not self.greeting_displayed:
            self._display_greeting()
            self.greeting_displayed = True
        self._display_header()
        super().display_options()

# ================================================================================================

    @attach_perk(BROWNMAIL)
    def is_officer_lurking(self) -> bool:
        if self.game_state.current_fish and self.game_state.current_fish.protected:
            return True

        return random.random() < 0.08


def calculate_bribe(game_state: GameState) -> int:
    if game_state.current_fish and game_state.current_fish.protected:
        return round(game_state.current_fish.base_value / 2)

    return game_state.player.lvl * 10

# ================================================================================================

@functional_component(state_dependent=True)
def obey_officer(game_state: GameState) -> GameState:
    amount = calculate_bribe(game_state)

    if game_state.player.coins < amount:
        return disobey_officer(game_state).run()

    game_state.player.coins -= amount
    game_state.player.sum_of_bribes += amount
    event_logger.log_event(OfficerEvent(EventType.OFFICER_PAID))

    return game_state

# ================================================================================================

@functional_component(state_dependent=True)
def disobey_officer(game_state: GameState) -> GameState:
    player = game_state.player

    OfficerHohkken(bribe=calculate_bribe(game_state)).handle_hit(player)
    event_logger.log_event(OfficerEvent(EventType.OFFICER_UNPAID))

    return game_state

# ================================================================================================

@dataclass
class PoliceBrutality(Weapon):
    name: str = "Police Brutality"
    damage: int = 0
    uses: int = -1
    acc: float = 1.0
    var: int = 0
    crit: float = 0.0
    cost: int = 0
    sell_value: int = 0
    type: str = SPECIAL
    sound: str = BLUNT

    def use(self) -> None:
        play_sound(self.sound)

# ================================================================================================

@dataclass
class OfficerHohkken(Enemy):
    name: str = "Officer Hohkken"
    bribe: int = 10
    hp: int = 100
    current_weapon: Weapon = field(default_factory=PoliceBrutality)

    def __post_init__(self) -> None:
        self.current_weapon.damage = random.randint(
            max(10, round(self.bribe / 2)),
            max(10, self.bribe),
        )
        self.weapon_dict = {self.current_weapon.name: self.current_weapon}










