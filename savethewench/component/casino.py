import random
from abc import abstractmethod
from functools import partial
from typing import Callable

from savethewench.audio import play_music, play_sound
from savethewench.data.audio import GOLF_CLAP, CASINO_THEME
from savethewench.data.components import CASINO
from savethewench.data.perks import GRAMBLING_ADDICT, WrapperIndices
from savethewench.model.game_state import GameState
from savethewench.model.perk import attach_perk
from savethewench.ui import blue, cyan, green, orange, purple, yellow, dim, red
from savethewench.util import print_and_sleep, safe_input
from .bank import BankVisitDecision
from .base import LabeledSelectionComponent, SelectionBinding, NoOpComponent, \
    GatekeepingComponent, functional_component, Component, BinarySelectionComponent, TextDisplayingComponent
from .registry import register_component


@register_component(CASINO)
class CasinoBouncer(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: game_state.player.coins > 0,
                         accept_component=CasinoCheck,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             blue("Your paper's no good here.\nCome back with some coins.\n"), 1.5)))


# --- Casino entry / gatekeeping ---

def can_gamble(game_state: GameState) -> bool:
    player = game_state.player
    return player.remaining_plays > 0 and player.coins >= 5


@functional_component(state_dependent=True)
def display_crapped_out_message(game_state: GameState):
    player = game_state.player
    message = "You're out of plays. Buy a perk or level up, bozo.\n" if player.remaining_plays == 0 else \
        "Later, bozo.\n"
    print_and_sleep(blue(message), 2)


class CasinoCheck(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         decision_function=partial(can_gamble, game_state), accept_component=Casino,
                         deny_component=display_crapped_out_message)


# --- Casino menu ---

class Casino(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, bindings=[
            SelectionBinding('1', "Krill or Cray", KrillOrCray),
            SelectionBinding('2', "Above or Below", AboveOrBelowRulesDecision),
            SelectionBinding('3', "TBD", NoOpComponent),
            SelectionBinding('R', "Return", functional_component()(lambda: self._return())),
        ])
        self.leave_casino = False
        print_and_sleep(blue("Welcome to Riverboat Casino, where the water flows like brine."), 2)

    def _return(self):
        self.leave_casino = True

    def can_exit(self):
        return self.leave_casino

    def play_theme(self):
        play_music(CASINO_THEME)


# --- Base game class ---

class CasinoGame(Component):
    def __init__(self, game_state: GameState, game_description: str):
        super().__init__(game_state)
        self.game_description = game_description
        self.player_quit = False

    @abstractmethod
    def play_round(self, wager: int) -> GameState:
        pass

    def get_wager_or_quit(self) -> int:
        player = self.game_state.player
        print_and_sleep(f"Coins: {green(player.coins)} {dim('|')} Plays: {cyan(player.remaining_plays)}")
        while True:
            raw_wager = safe_input("[#] : Wager\n"
                                   "[q] : Leave").strip().lower()
            if raw_wager != 'q' and not raw_wager.isdigit():
                print_and_sleep(yellow("Invalid choice."))
            elif raw_wager.isdigit():
                if int(raw_wager) < 5:
                    print_and_sleep(
                        blue("Minimum wager is 5 coins, bozo."), 1)
                elif int(raw_wager) > self.game_state.player.coins:
                    print_and_sleep(
                        blue(f"Can't bet what ya don't have, bozo."), 1)
                else:
                    return int(raw_wager)
            else:
                self.player_quit = True
                return -1

    def run(self) -> GameState:
        if can_gamble(self.game_state):
            print_and_sleep(self.game_description)
        while (not self.player_quit) and can_gamble(self.game_state):
            wager = self.get_wager_or_quit()
            if not self.player_quit:
                self.game_state = self.play_round(wager)
        if self.player_quit:
            print_and_sleep(blue("Later bozo."), 1)
        else:
            self.game_state = display_crapped_out_message(self.game_state).run()
        return self.game_state


# --- Krill or Cray ---

class KrillOrCray(CasinoGame):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, game_description=blue("One to one bets. Classic Riverboat Gambling."))

    @staticmethod
    def get_pick(wager: int) -> str:
        while True:
            pick = safe_input(f"You bet {green(wager)} coins.\n\nWhat's the call?\n"
                              f"[K] : {red('Krill')}\n[C] : {orange('Cray')}").strip().lower()
            if pick in ('k', 'c'):
                return pick
            print_and_sleep(yellow("Invalid choice."), 1)

    @staticmethod
    @attach_perk(GRAMBLING_ADDICT, WrapperIndices.GramblingAddict.PAYOUT, value_description="payout")
    def get_payout(wager: int) -> int:
        return int(wager * 0.9)

    def play_round(self, wager) -> GameState:
        player = self.game_state.player
        winner = random.choice(['k', 'c'])
        pick = self.get_pick(wager)
        if pick == winner:
            payout = int(self.get_payout(wager))
            player.coins += payout
            player.casino_won += payout
            print_and_sleep(green(f"Lucky guess, bozo! You won {payout} coins."), 0.5)
            play_sound(GOLF_CLAP)
            if player.gain_xp_other(1):
                BankVisitDecision(self.game_state).run()  # TODO figure out a way to not call this in so many places
        else:
            print_and_sleep(
                blue("Bozo's blunder. Classic. Could've seen that coming from six or eight miles away."), 2)
            player.coins -= wager
            player.casino_lost += wager
        player.games_played += 1
        return self.game_state


def roll_die() -> int:
    roll = random.randint(1, 6)
    safe_input("[ ] Roll the die")
    print_and_sleep(cyan(f"You rolled a {roll}."))
    return roll


# --- Above or Below rules ---

class AboveOrBelowRules(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         next_component=AboveOrBelow,
                         display_callback=lambda _: print_and_sleep("""1. Place a wager and roll a die.
2. Guess whether the next roll will be higher or lower, then roll again.
3. Each correct guess increases your payout.
4. A wrong guess ends the game and forfeits your wager.
5. You may play up to four rounds or cash out at any time.\n"""))


class AboveOrBelowRulesDecision(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Do you want to see the rules?",
                         yes_component=AboveOrBelowRules,
                         no_component=AboveOrBelow)


# --- Above or Below ---

class AboveOrBelow(CasinoGame):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, game_description=blue("Welcome to Above or Below!"))
        self.turn = 0
        self.ladder = [1.0, 1.5, 2.0, 2.8, 4.0]
        self.wager = 0

    def display_status(self) -> None:
        print_and_sleep(f"{dim(' | ').join([
            f"Round: {cyan(self.turn + 1)}", f"Wager: {green(self.wager)}",
            f"Mult: {purple(self.ladder[self.turn])}", f"Payout: {green(self.get_payout())}"])}")

    @staticmethod
    def get_eval_function() -> Callable[[int, int], bool]:
        while True:
            call = safe_input("[A] : Above\n"
                              "[B] : Below").strip().lower()
            if call not in ('a', 'b'):
                print_and_sleep(yellow("Invalid choice."))
            else:
                break
        comp: Callable[[int, int], bool] = lambda r1, r2: r2 > r1 if call == 'a' else r2 < r1
        return comp

    @staticmethod
    def should_cash_out() -> bool:
        while True:
            choice = safe_input("[C] : Continue\n"
                                "[Q] : Cash Out\n")
            if choice not in ('q', 'c'):
                print_and_sleep(yellow("Invalid choice."))
            else:
                return choice == 'q'

    def get_wager_or_quit(self) -> int:
        if self.turn == 0:
            self.wager = super().get_wager_or_quit()
        return self.wager

    @attach_perk(GRAMBLING_ADDICT, WrapperIndices.GramblingAddict.PAYOUT, value_description='payout')
    def get_payout(self) -> int:
        return int(self.wager * self.ladder[self.turn])

    def play_round(self, wager: int) -> GameState:
        player = self.game_state.player
        player.games_played += 1
        self.display_status()
        roll1 = roll_die()
        call_is_correct = self.get_eval_function()
        roll2 = roll_die()
        if call_is_correct(roll1, roll2):
            self.turn += 1
            payout = self.get_payout()
            print_and_sleep(blue(f"Lucky guess!\nPayout increased to {payout} coins.\n"))
            if self.turn == len(self.ladder) - 1 or self.should_cash_out():
                player.coins += payout
                if self.turn == len(self.ladder):
                    print_and_sleep(f"{blue("You completed the final round.")}")
                    if player.gain_xp_other(3):
                        BankVisitDecision(
                            self.game_state).run()  # TODO figure out a way to not call this in so many places
                print_and_sleep(f"{green(f"You cashed out {payout} coins!")}")
                player.casino_won += payout
                self.player_quit = True
                return self.game_state
        else:
            print_and_sleep(yellow("Your guess was dry."))
            player.coins -= wager
            player.casino_lost += wager
            self.turn = 0
        return self.game_state


class DoubleOrDry(NoOpComponent):
    pass
