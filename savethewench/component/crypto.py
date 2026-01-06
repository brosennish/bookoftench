import curses
import time
from typing import List

from savethewench.component.base import Component
from savethewench.model import GameState
from savethewench.model.crypto import CryptoCurrency


class CryptoExchange(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.coins: List[CryptoCurrency] = game_state.crypto_service.coins
        self.selected = 1
        self.curs_set = 0
        self.options_start = 4
        self.prompt_start = self.options_start + len(self.coins) + 3
        self.can_exit = False

    def _format_and_add_coin(self, stdscr, selection: int, line: int, coin: CryptoCurrency):
        stdscr.addstr(line, 0, f"[{selection}]", curses.color_pair(7) if selection == self.selected else curses.color_pair(1))
        stdscr.addstr(line, 5, coin.name, curses.color_pair(2))

        pct_change = coin.historical_percent_change
        color = 5
        if pct_change > 0.0:
            color = 3
        elif pct_change < 0.0:
            color = 4
        stdscr.addstr(line, 25, coin.format_price(), curses.color_pair(color))
        stdscr.addstr(line, 35, coin.format_percent_change(), curses.color_pair(color))

    def _add_return_option(self, stdscr, selection: int, line: int):
        stdscr.addstr(line, 0, f"[R]",
                      curses.color_pair(7) if selection == self.selected else curses.color_pair(1))
        stdscr.addstr(line, 5, "Return", curses.color_pair(2))

    def display_header(self, stdscr):
        stdscr.addstr(0, 0, f"Crypto Market", curses.color_pair(1) | curses.A_UNDERLINE | curses.A_BOLD)
        greeting_parts = [(f"Welcome, {self.game_state.player.name}. You have ", 5),
                          (f"{self.game_state.player.coins}", 3), (" of coin to spend.", 5)]
        offset = 0
        for text, color in greeting_parts:
            stdscr.addstr(2, offset, text, curses.color_pair(color))
            offset += len(text)

    def display_options(self, stdscr):
        for i in range(len(self.game_state.crypto_service.coins)):
            coin = self.game_state.crypto_service.coins[i]
            self._format_and_add_coin(stdscr, i + 1, self.options_start + i, coin)
        self._add_return_option(stdscr, len(self.coins) + 1, self.options_start + len(self.coins) + 1)

    def display_prompt(self, stdscr):
        pass

    def handle_selection(self, stdscr):
        ch = stdscr.getch()
        if ch in (curses.KEY_ENTER, 10, 13):
            if self.selected <= len(self.coins):
                self.coins[self.selected - 1].freeze()
                QuantitySelector(self.game_state, self.selected).c_run(stdscr)
            else:
                self.can_exit = True # TODO goodbye message, sleep, etc
        elif ch == curses.KEY_UP:
            self.selected -= 1
            if self.selected == 0:
                self.selected = len(self.game_state.crypto_service.coins) + 1
        elif ch == curses.KEY_DOWN:
            self.selected += 1
            if self.selected > len(self.game_state.crypto_service.coins) + 1:
                self.selected = 1

    def c_run(self, stdscr):
        init_colors()
        while not self.can_exit:
            curses.curs_set(self.curs_set)
            stdscr.keypad(True)
            stdscr.nodelay(True)
            stdscr.clear()
            self.display_header(stdscr)
            self.display_options(stdscr)
            self.display_prompt(stdscr)
            stdscr.refresh()
            try:
                self.handle_selection(stdscr)
            except curses.error:
                pass  # no input
            time.sleep(0.01)

    def run(self) -> GameState:
        curses.wrapper(self.c_run)
        return self.game_state

class QuantitySelector(CryptoExchange):
    def __init__(self, game_state: GameState, selected: int):
        super().__init__(game_state)
        self.selected = selected
        self.coin = self.coins[self.selected-1]
        self.curs_set = 1
        self.max_purchase = int(self.game_state.player.coins / self.coin.price)
        self.user_input = ""

    def display_prompt(self, stdscr):
        stdscr.addstr(self.prompt_start, 0, f"How much {self.coin.name} do you want to buy? (max {self.max_purchase})")
        stdscr.addstr(self.prompt_start + 1, 0, "> ", curses.color_pair(6))
        stdscr.addstr(self.prompt_start + 1, 2, self.user_input)

    def handle_selection(self, stdscr):
        ch = stdscr.getch()
        if ord('0') <= ch <= ord('9'):
            if ch > ord('0') or len(self.user_input) != 0:
                self.user_input += chr(ch)
        elif ch in (curses.KEY_ENTER, 10, 13):
            quantity = int(self.user_input)
            # TODO handle all this stuff properly
            if quantity <= self.max_purchase:
                self.game_state.player.coins -= int(self.coin.price * quantity)
                self.can_exit = True
                self.coin.unfreeze()
            else:
                # TODO display error message somehow
                self.user_input = ""
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            self.user_input = self.user_input[:-1]

    def run(self):
        raise RuntimeError("Quantity Selector not runnable from outside of preexisting curses context")


def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)

    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    curses.init_pair(8, curses.COLOR_CYAN, curses.COLOR_WHITE)
    curses.init_pair(9, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(10, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(12, curses.COLOR_BLUE, curses.COLOR_WHITE)