import curses
import time
from abc import ABC, abstractmethod
from typing import List

import savethewench.service.crypto_service as crypto_service
from savethewench.component.base import Component
from savethewench.component.registry import register_component
from savethewench.curses_util import init_colors, c_print
from savethewench.data.components import CRYPTO_EXCHANGE
from savethewench.model import GameState
from savethewench.model.crypto import CryptoCurrency


@register_component(CRYPTO_EXCHANGE)
class CryptoExchange(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.coins: List[CryptoCurrency] = crypto_service.get_active_coins()
        self.selected = 1
        self.curs_set = 0
        self.options_start = 4
        self.prompt_start = self.options_start + len(self.coins) + 3
        self.can_exit = False

    def _format_and_add_coin(self, stdscr, selection: int, line: int, coin: CryptoCurrency):
        c_print(stdscr, line, 0, f"[{selection}]", curses.COLOR_MAGENTA,
                highlight=self.selected == selection)
        c_print(stdscr, line, 5, coin.name, curses.COLOR_CYAN, dim=coin.delisted)

        pct_change = coin.historical_percent_change
        color = curses.COLOR_WHITE
        if pct_change > 0.0:
            color = curses.COLOR_GREEN
        elif pct_change < 0.0:
            color = curses.COLOR_RED
        c_print(stdscr, line, 25, coin.format_price(), color)
        c_print(stdscr, line, 35, coin.format_percent_change(), color)
        c_print(stdscr, line, 45, str(coin.coins_owned), curses.COLOR_MAGENTA)

    def _add_return_option(self, stdscr, selection: int, line: int):
        c_print(stdscr, line, 0, '[R]', curses.COLOR_MAGENTA, highlight=self.selected == selection)
        c_print(stdscr, line, 5, "Return", curses.COLOR_CYAN)

    def display_header(self, stdscr):
        c_print(stdscr, 0, 0, 'Crypto Market', curses.COLOR_MAGENTA, underline=True, bold=True)
        greeting_parts = [(f"Welcome, {self.game_state.player.name}. You have ", curses.COLOR_WHITE),
                          (f"{self.game_state.player.coins}", curses.COLOR_GREEN),
                          (" of coin to spend.", curses.COLOR_WHITE)]
        offset = 0
        for text, color in greeting_parts:
            c_print(stdscr, 2, offset, text, color)
            offset += len(text)

    def display_options(self, stdscr):
        for i in range(len(self.coins)):
            self._format_and_add_coin(stdscr, i + 1, self.options_start + i, self.coins[i])
        self._add_return_option(stdscr, len(self.coins) + 1, self.options_start + len(self.coins) + 1)

    def display_prompt(self, stdscr):
        pass

    def handle_selection(self, stdscr):
        ch = stdscr.getch()
        if ch in (curses.KEY_ENTER, 10, 13):
            if self.selected <= len(self.coins):
                self.coins[self.selected - 1].freeze()
                BuyOrSellSelector(self.game_state, self.selected).c_run(stdscr)
            else:
                # Leaving exchange - all coins unfreeze since player had an opportunity to buy at initial price
                for coin in self.coins:
                    coin.unfreeze()
                self.can_exit = True  # TODO goodbye message, sleep, etc
        elif ch == curses.KEY_UP:
            self.selected -= 1
            if self.selected == 0:
                self.selected = len(self.coins) + 1
        elif ch == curses.KEY_DOWN:
            self.selected += 1
            if self.selected > len(self.coins) + 1:
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
            # need to update on each iteration since `get_active_coins` returns a copy
            self.coins = crypto_service.get_active_coins()

    def run(self) -> GameState:
        curses.wrapper(self.c_run)
        return self.game_state


class CryptoExchangeExtension(CryptoExchange):
    def run(self):
        raise RuntimeError("Quantity Selector not runnable from outside of preexisting curses context")


class BuyOrSellSelector(CryptoExchangeExtension):
    def __init__(self, game_state: GameState, selected: int):
        super().__init__(game_state)
        self.selected = selected
        self.coin = self.coins[self.selected - 1]
        self.sub_selection = 0

    def display_prompt(self, stdscr):
        c_print(stdscr, self.prompt_start, 0, "[B]", curses.COLOR_MAGENTA,
                highlight=self.sub_selection == 0)
        c_print(stdscr, self.prompt_start, 4, "Buy")
        c_print(stdscr, self.prompt_start + 1, 0, "[S]", curses.COLOR_MAGENTA,
                highlight=self.sub_selection == 1)
        c_print(stdscr, self.prompt_start + 1, 4, "Sell")

    def handle_selection(self, stdscr):
        ch = stdscr.getch()
        if ch in (curses.KEY_ENTER, 10, 13):
            self.can_exit = True
            if self.sub_selection == 0:
                BuySelector(self.game_state, self.selected).c_run(stdscr)
            else:
                SellSelector(self.game_state, self.selected).c_run(stdscr)
        elif ch == curses.KEY_UP:
            self.sub_selection -= 1
            if self.sub_selection < 0:
                self.sub_selection = 1
        elif ch == curses.KEY_DOWN:
            self.sub_selection += 1
            if self.sub_selection > 1:
                self.sub_selection = 0

    def c_run(self, stdscr):
        if self.coin.coins_owned == 0:
            self.can_exit = True
            BuySelector(self.game_state, self.selected).c_run(stdscr)
        super().c_run(stdscr)


class QuantitySelector(CryptoExchangeExtension, ABC):
    def __init__(self, game_state: GameState, selected: int):
        super().__init__(game_state)
        self.selected = selected
        self.coin = self.coins[self.selected - 1]
        self.curs_set = 1
        self.user_input = ""

    @abstractmethod
    def get_max_quantity(self):
        pass

    @abstractmethod
    def display_prompt(self, stdscr):
        pass

    @abstractmethod
    def handle_quantity(self, quantity: int):
        pass

    def handle_selection(self, stdscr):
        c_print(stdscr, self.prompt_start + 1, 0, "> ", curses.COLOR_BLUE)
        c_print(stdscr, self.prompt_start + 1, 2, self.user_input)
        ch = stdscr.getch()
        if ord('0') <= ch <= ord('9'):
            if self.user_input == "0":
                self.user_input = ""
            self.user_input += chr(ch)
        elif ch in (curses.KEY_ENTER, 10, 13) and len(self.user_input) > 0:
            quantity = int(self.user_input)
            if quantity <= self.get_max_quantity():
                self.handle_quantity(quantity)
                self.can_exit = True
                self.coin.unfreeze()
            else:
                # TODO display error message somehow
                self.user_input = ""
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            self.user_input = self.user_input[:-1]


class BuySelector(QuantitySelector):

    def get_max_quantity(self):
        return int(self.game_state.player.coins / self.coin.price)

    def display_prompt(self, stdscr):
        c_print(stdscr, self.prompt_start, 0,
                f"How much {self.coin.name} do you want to buy? (max {self.get_max_quantity()})")

    def handle_quantity(self, quantity: int):
        total_cost = int(quantity * self.coin.price)
        self.game_state.player.coins -= total_cost
        self.coin.log_purchase(quantity, total_cost)


class SellSelector(QuantitySelector):

    def get_max_quantity(self):
        return self.coin.coins_owned

    def display_prompt(self, stdscr):
        c_print(stdscr, self.prompt_start, 0,
                f"How much {self.coin.name} do you want to sell? (max {self.get_max_quantity()})")

    def handle_quantity(self, quantity: int):
        total_cost = int(quantity * self.coin.price)
        self.game_state.player.coins += total_cost
        self.coin.log_sale(quantity, total_cost)
