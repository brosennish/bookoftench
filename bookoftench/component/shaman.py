import random

from bookoftench import event_logger
from bookoftench.audio import play_music, play_sound
from bookoftench.component.base import LabeledSelectionComponent, SelectionBinding, ReprBinding, Component, \
    functional_component, GatekeepingComponent
from bookoftench.component.registry import register_component
from bookoftench.data.audio import SHAMAN_THEME, PURCHASE
from bookoftench.data.components import SHAMAN
from bookoftench.data.enviroment import DAY
from bookoftench.data.rites import Shaman_Lines
from bookoftench.model import GameState
from bookoftench.model.events import ShamanEvent
from bookoftench.model.rite import Rite, load_rites
from bookoftench.model.util import display_shaman_header
from bookoftench.ui import blue, yellow
from bookoftench.util import print_and_sleep

# ================================================================================================

# --- check if shaman is open ---

@register_component(SHAMAN)
class ShamanOpen(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         decision_function=self._is_open,
                         accept_component=ShamanBouncer,
                         deny_component=shaman_closed)

    def _is_open(self) -> bool:
        return self.game_state.shaman_is_open


@functional_component(state_dependent=True)
def shaman_closed(game_state: GameState) -> GameState:
    print_and_sleep(blue("The Shaman is in the underworld.\n"), 1.5)
    return game_state

# ================================================================================================

# --- check if player can benefit from any of the shaman's offerings ---

class ShamanBouncer(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         decision_function=self._player_can_benefit,
                         accept_component=ShamanSleeping,
                         deny_component=shaman_has_nothing_to_offer)

    def _player_can_benefit(self) -> bool:
        player = self.game_state.player
        return bool(player.illness or player.blind or player.hp != player.max_hp)


@functional_component(state_dependent=True)
def shaman_has_nothing_to_offer(game_state: GameState) -> GameState:
    print_and_sleep(blue("There is nothing the Shaman can do for you at this time.\n"), 1.5)
    return game_state

# ================================================================================================

# --- check if daytime ---

class ShamanSleeping(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         decision_function=self._is_daytime,
                         accept_component=ShamanComponent,
                         deny_component=shaman_is_sleeping)

    def _is_daytime(self) -> bool:
        return self.game_state.time_of_day == DAY


@functional_component(state_dependent=True)
def shaman_is_sleeping(game_state: GameState) -> GameState:
    print_and_sleep(blue("The Shaman sleeps at night.\n"), 1.5)
    return game_state

# ================================================================================================

class ShamanComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        rite_options = load_rites(game_state.player)

        rite_bindings = [
            ReprBinding(
                str(index + 1),
                rite.name,
                self._make_purchase_component(rite),
                rite,
            )
            for index, rite in enumerate(rite_options)
        ]

        return_binding = SelectionBinding(
            "R",
            "Return",
            self._make_return_component(),
        )

        super().__init__(game_state,
                         refresh_menu=True,
                         bindings=[*rite_bindings, return_binding])

        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                rite_bindings,
                top_level_prompt_callback=display_shaman_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [return_binding],
            ),
        ]
        self.leave = False

    def play_theme(self) -> None:
        play_music(SHAMAN_THEME)

    def _return(self) -> GameState:
        self.leave = True
        print_and_sleep(blue("Go now."), 1.5)
        return self.game_state

    def _make_return_component(self) -> type[Component]:
        @functional_component()
        def return_component() -> GameState:
            return self._return()

        return return_component

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

    def display_options(self) -> None:
        message = random.choice(Shaman_Lines)
        print_and_sleep(blue(f"{message}\n"), 1.5)

        for component in self.selection_components:
            component.display_options()

# ================================================================================================

    @staticmethod
    def _make_purchase_component(rite: Rite) -> type[Component]:
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState) -> GameState:
            player = game_state.player

            if player.coins < rite.cost:
                print_and_sleep(yellow("Need more coin."), 1)
                return game_state

            play_sound(PURCHASE)
            player.coins -= rite.cost
            event_logger.log_event(ShamanEvent())
            rite.perform(player)

            return game_state

        return purchase_component
