import curses
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import savethewench.service.crypto_service as crypto_service
from savethewench.component.base import Component
from savethewench.component.registry import register_component
from savethewench.curses_util import init_colors, c_print
from savethewench.data.components import CRYPTO_EXCHANGE
from savethewench.model import GameState
from savethewench.model.crypto import CryptoCurrency, Transaction, TransactionType


@register_component(CRYPTO_EXCHANGE)
class CryptoExchange(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.coins: List[CryptoCurrency] = crypto_service.get_active_coins()
        self.coin_options: CoinOptions = CoinOptions()
        self.selected = 1
        self.curs_set = 0
        self.options_start = 4
        self.prompt_start = self.options_start + len(self.coins) + 4
        self.can_exit = False

    def _add_return_option(self, stdscr, selection: int, line: int):
        c_print(stdscr, line, 0, '[R]', curses.COLOR_MAGENTA, highlight=self.selected == selection)
        c_print(stdscr, line, 4, "Return", curses.COLOR_CYAN)

    def display_header(self, stdscr):
        c_print(stdscr, 0, 0, 'Crypto Market', curses.COLOR_MAGENTA, underline=True, bold=True)
        greeting_parts = [(f"Welcome, {self.game_state.player.name}. You have ", curses.COLOR_WHITE),
                          (f"{self.game_state.player.coins}", curses.COLOR_GREEN),
                          (" of coin to spend.", curses.COLOR_WHITE)]
        offset = 0
        for text, color in greeting_parts:
            c_print(stdscr, 2, offset, text, color)
            offset += len(text)

    def display_additional_options(self, stdscr):
        self._add_return_option(stdscr, len(self.coins) + 1, self.options_start + len(self.coins) + 2)

    def display_prompt(self, stdscr):
        pass

    def handle_selection(self, stdscr):
        # Note - logic will need to change if we ever want more than 10 numbered options
        ch = stdscr.getch()
        if ch in (curses.KEY_ENTER, 10, 13):
            if self.selected <= len(self.coins):
                self.coins[self.selected - 1].freeze()
                CoinActionSelector(self.game_state, self.selected).c_run(stdscr)
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
        # key selection for numbered options won't work if we have more than 9 options
        elif ch in range(ord('1'), ord(str(len(self.coins)))+1):
            self.selected = int(chr(ch))
        elif ch in (ord('r'), ord('R')):
            self.selected = len(self.coins) + 1

    def c_run(self, stdscr):
        init_colors()
        while not self.can_exit:
            curses.curs_set(self.curs_set)
            curses.mousemask(0)
            stdscr.keypad(True)
            stdscr.nodelay(True)
            stdscr.clear()
            self.display_header(stdscr)
            self.coin_options.display(stdscr, self.options_start, self.selected)
            self.display_additional_options(stdscr)
            self.display_prompt(stdscr)
            stdscr.refresh()
            try:
                self.handle_selection(stdscr)
            except curses.error:
                pass  # no input
            time.sleep(0.05)
            # need to update on each iteration since `get_active_coins` returns a copy
            self.coins = crypto_service.get_active_coins()
            self.coin_options.refresh()

    def run(self) -> GameState:
        curses.wrapper(self.c_run)
        return self.game_state


class CryptoExchangeExtension(CryptoExchange):
    def run(self):
        raise RuntimeError("Quantity Selector not runnable from outside of preexisting curses context")


class CoinActionSelector(CryptoExchangeExtension):
    def __init__(self, game_state: GameState, selected: int):
        super().__init__(game_state)
        self.selected = selected
        self.coin = self.coins[self.selected - 1]
        self.sub_selection = 0
        self.actions_start = self.options_start + len(self.coins) + 2

    def display_additional_options(self, stdscr):
        c_print(stdscr, self.actions_start, 0, "[B]", curses.COLOR_MAGENTA,
                highlight=self.sub_selection == 0)
        c_print(stdscr, self.actions_start, 4, "Buy", curses.COLOR_CYAN)
        line = self.actions_start + 1
        if self.coin.quantity_owned > 0:
            c_print(stdscr, line, 0, "[S]", curses.COLOR_MAGENTA,
                    highlight=self.sub_selection == 1)
            c_print(stdscr, line, 4, "Sell", curses.COLOR_CYAN)
            line += 1
        c_print(stdscr, line, 0, '[H]', curses.COLOR_MAGENTA,
                highlight=self.sub_selection == (2 if self.coin.quantity_owned > 0 else 1))
        c_print(stdscr, line, 4, "History", curses.COLOR_CYAN)

        c_print(stdscr, line + 2, 0, '[R]', curses.COLOR_MAGENTA,
                highlight=self.sub_selection == (3 if self.coin.quantity_owned > 0 else 2))
        c_print(stdscr, line + 2, 4, "Return", curses.COLOR_CYAN)

    def handle_selection(self, stdscr):
        ch = stdscr.getch()

        if ch in (curses.KEY_ENTER, 10, 13):
            self.can_exit = True
            if self.sub_selection == 0:
                BuySelector(self.game_state, self.selected).c_run(stdscr)
            elif self.sub_selection == 1:
                if self.coin.quantity_owned > 0:
                    SellSelector(self.game_state, self.selected).c_run(stdscr)
                else:
                    self.can_exit = False
                    TransactionHistoryDisplay(self.game_state, self.coin).c_run(stdscr)
            elif self.sub_selection == 2 and self.coin.quantity_owned > 0:
                self.can_exit = False
                TransactionHistoryDisplay(self.game_state, self.coin).c_run(stdscr)
        elif ch == curses.KEY_UP:
            self.sub_selection -= 1
            if self.sub_selection < 0:
                self.sub_selection = (3 if self.coin.quantity_owned > 0 else 2)
        elif ch == curses.KEY_DOWN:
            self.sub_selection += 1
            if self.sub_selection > (3 if self.coin.quantity_owned > 0 else 2):
                self.sub_selection = 0
        elif ch in (ord('b'), ord('B')):
            self.sub_selection = 0
        elif ch in (ord('s'), ord('S')):
            self.sub_selection = 1 if self.coin.quantity_owned > 0 else self.sub_selection
        elif ch in (ord('h'), ord('H')):
            self.sub_selection = 1 if self.coin.quantity_owned == 0 else 2
        elif ch in (ord('r'), ord('R')):
            self.sub_selection = 2 if self.coin.quantity_owned == 0 else 3


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
        int_price = int(self.coin.price)
        total_cost = quantity * int(self.coin.price)
        self.game_state.player.coins -= total_cost
        self.coin.log_purchase(quantity, int_price)


class SellSelector(QuantitySelector):

    def get_max_quantity(self):
        return self.coin.quantity_owned

    def display_prompt(self, stdscr):
        c_print(stdscr, self.prompt_start, 0,
                f"How much {self.coin.name} do you want to sell? (max {self.get_max_quantity()})")

    def handle_quantity(self, quantity: int):
        int_price = int(self.coin.price)
        total_cost = quantity * int(self.coin.price)
        self.game_state.player.coins += total_cost
        self.coin.log_sale(quantity, int_price)


class TransactionHistoryDisplay(CryptoExchangeExtension):
    def __init__(self, game_state: GameState, coin: CryptoCurrency):
        super().__init__(game_state)
        self.coin = coin
        self.transactions_per_page = 10
        self.page = 0

    def display_header(self, stdscr):
        prefix = "Transaction History:"
        c_print(stdscr, 0, 0, self.coin.name, curses.COLOR_CYAN)
        c_print(stdscr, 0, len(self.coin.name) + 1, prefix, curses.COLOR_MAGENTA)


    def add_buy(self, stdscr, transaction: Transaction, line: int):
        c_print(stdscr, line, 0, f"{transaction.format_timestamp()} | Buy {transaction.quantity} @ {transaction.price}")

    def add_sell(self, stdscr, transaction: Transaction, line: int):
        c_print(stdscr, line, 0, f"{transaction.format_timestamp()} | Sell {transaction.quantity} @ {transaction.price}")

    def display_history(self, stdscr):
        line = 2
        for i in range(len(self.coin.history.transactions)):
            transaction = self.coin.history.transactions[i]
            if transaction.type == TransactionType.BUY:
                self.add_buy(stdscr, transaction, line)
            elif transaction.type == TransactionType.SELL:
                self.add_sell(stdscr, transaction, line)
            line += 1
        c_print(stdscr, line + 1, 0,"Press <enter> to return.", color=curses.COLOR_CYAN)

    def handle_selection(self, stdscr):
        ch = stdscr.getch()
        if ch in (curses.KEY_ENTER, 10, 13):
            self.can_exit = True

    def c_run(self, stdscr):
        init_colors()
        while not self.can_exit:
            curses.curs_set(self.curs_set)
            curses.mousemask(0)
            stdscr.keypad(True)
            stdscr.nodelay(True)
            stdscr.clear()
            self.display_header(stdscr)
            self.display_history(stdscr)
            stdscr.refresh()
            try:
                self.handle_selection(stdscr)
            except curses.error:
                pass  # no input
            time.sleep(0.05)


@dataclass
class LinePart:
    value: str
    color: int = curses.COLOR_WHITE
    underlined: bool = False
    highlighted: bool = False
    dim: bool = False

    def add_to_line(self, stdscr, line: int, offset: int):
        c_print(stdscr, line, offset, self.value, self.color,
                underline=self.underlined, highlight=self.highlighted, dim=self.dim)

def header_part(value: str) -> LinePart:
    return LinePart(value, underlined=True)

def name_part(coin: CryptoCurrency) -> LinePart:
    return LinePart(coin.name, color=curses.COLOR_CYAN, dim=coin.delisted)

def price_part(coin: CryptoCurrency) -> LinePart:
    color = (curses.COLOR_RED if coin.historical_percent_change < 0 else
             curses.COLOR_GREEN if coin.historical_percent_change > 0 else
             curses.COLOR_WHITE)
    return LinePart(f"{coin.price:.2f}", color=color)

def delta_part(coin: CryptoCurrency) -> LinePart:
    color = (curses.COLOR_RED if coin.historical_percent_change < 0 else
             curses.COLOR_GREEN if coin.historical_percent_change > 0 else
             curses.COLOR_WHITE)
    return LinePart(f"{coin.historical_percent_change:.1f}%", color=color)

def quantity_owned_part(coin: CryptoCurrency) -> LinePart:
    return LinePart(str(coin.quantity_owned), color=curses.COLOR_MAGENTA)

def owned_value_part(coin: CryptoCurrency) -> LinePart:
    return LinePart(f"{round(float(coin.quantity_owned * coin.price), 2)}")

def cost_basis_part(coin: CryptoCurrency) -> LinePart:
    return LinePart(f"{round(coin.history.cost_basis, 2)}")

def gain_part(coin: CryptoCurrency) -> LinePart:
    color = (curses.COLOR_RED if coin.open_pl < 0 else
             curses.COLOR_GREEN if coin.open_pl > 0 else
             curses.COLOR_WHITE)
    return LinePart(f"{round(coin.open_pl, 2)}", color=color)

def gain_pct_part(coin: CryptoCurrency) -> LinePart:
    color = (curses.COLOR_RED if coin.open_pl < 0 else
             curses.COLOR_GREEN if coin.open_pl > 0 else
             curses.COLOR_WHITE)
    return LinePart(f"{coin.open_pl_percent:.1f}%", color=color)

class CoinOptions:
    def __init__(self):
        self.headers = ['Name', 'Price', 'Chg', 'Owned', 'Value', 'Cost Basis', 'P/L', 'Chg']
        self.coin_line_part_factories = [name_part, price_part, delta_part, quantity_owned_part, owned_value_part,
                                         cost_basis_part, gain_part, gain_pct_part]
        self.columns = len(self.headers)
        self._ingest_coins()

    def get_coin_line_parts(self, coin) -> List[LinePart]:
        return [f(coin) for f in self.coin_line_part_factories]

    def _ingest_coins(self):
        self.coins = crypto_service.get_active_coins()
        self.offsets = [0 for _ in range(self.columns)]
        self.offsets[0] = len(str(len(self.coins))) + 3
        lines: List[List[LinePart]] = [[header_part(h) for h in self.headers],
                                            *[self.get_coin_line_parts(coin) for coin in self.coins]]
        widths = [0] * self.columns
        for parts in lines:
            for i, part in enumerate(parts):
                widths[i] = max(widths[i], len(part.value))

        self.offsets = [0] * self.columns
        self.offsets[0] = len(str(len(self.coins))) + 3
        for i in range(1, self.columns):
            self.offsets[i] = self.offsets[i - 1] + widths[i - 1] + 3

    def display_header(self, stdscr, line: int):
        for i in range(len(self.headers)):
            header_part(self.headers[i]).add_to_line(stdscr, line, self.offsets[i])

    def display_coin(self, stdscr, line: int, coin: CryptoCurrency):
        parts = self.get_coin_line_parts(coin)
        for i in range(len(parts)):
            parts[i].add_to_line(stdscr, line, self.offsets[i])

    def display(self, stdscr, line: int, selected: int):
        self.display_header(stdscr, line)
        for i in range(1, len(self.coins)+1):
            c_print(stdscr, line + i, 0, f"[{i}]", curses.COLOR_MAGENTA, highlight=selected == i)
            self.display_coin(stdscr, line + i, self.coins[i-1])

    def refresh(self):
        self._ingest_coins()
