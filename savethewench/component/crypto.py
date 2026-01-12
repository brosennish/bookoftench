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

@dataclass
class Displayable:
    line: int
    offset: int
    text: str
    color: int
    underline: bool
    bold: bool
    highlight: bool
    dim: bool

    def add_to_screen(self, stdscr):
        c_print(stdscr, self.line, self.offset, self.text, color=self.color, highlight=self.highlight,
                underline=self.underline, bold=self.bold, dim=self.dim)

class SimpleWindow:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.displayables: List[Displayable] = []
        self._current_line = 0

    def add_newlines(self, newlines: int):
        self._current_line += newlines

    def add_to_display(self, offset: int, text: str, color: int=curses.COLOR_WHITE,
                       underline: bool=False, bold: bool=False, highlight: bool=False, dim: bool=False):
        self.displayables.append(Displayable(self._current_line, offset, text, color, underline, bold, highlight, dim))

    def flush(self):
        self.stdscr.clear()
        for displayable in self.displayables:
            displayable.add_to_screen(self.stdscr)
        self.stdscr.refresh()
        self.displayables.clear()
        self._current_line = 0

@register_component(CRYPTO_EXCHANGE)
class CryptoExchange(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.coins: List[CryptoCurrency] = crypto_service.get_active_coins()
        self.coin_options: CoinOptions = CoinOptions()
        self.selected = 1
        self.curs_set = 0
        self.can_exit = False

    def add_header(self, window):
        window.add_to_display(0, 'Crypto Market', curses.COLOR_MAGENTA, underline=True, bold=True)
        window.add_newlines(1)
        greeting_parts = [(f"Welcome, {self.game_state.player.name}. You have ", curses.COLOR_WHITE),
                          (f"{self.game_state.player.coins}", curses.COLOR_GREEN),
                          (" of coin to spend.", curses.COLOR_WHITE)]
        offset = 0
        for text, color in greeting_parts:
            window.add_to_display(offset, text, color)
            offset += len(text)

    def add_additional_options(self, window):
        window.add_newlines(2)
        window.add_to_display(0, '[R]', curses.COLOR_MAGENTA, highlight=self.selected == len(self.coins) + 1)
        window.add_to_display(4, "Return", curses.COLOR_CYAN)

    def add_coin_options(self, window):
        window.add_newlines(1)
        self.coin_options.add_to_window(window, self.selected)

    def add_prompt(self, window):
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
        window = SimpleWindow(stdscr)
        while not self.can_exit:
            curses.curs_set(self.curs_set)
            curses.mousemask(0)
            stdscr.keypad(True)
            stdscr.nodelay(True)
            self.add_header(window)
            self.add_coin_options(window)
            self.add_additional_options(window)
            self.add_prompt(window)
            window.flush()
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

    def add_additional_options(self, window):
        window.add_newlines(2)
        window.add_to_display(0, '[B]', curses.COLOR_MAGENTA, highlight=self.sub_selection == 0)
        window.add_to_display(4, "Buy", curses.COLOR_CYAN)
        window.add_newlines(1)
        if self.coin.quantity_owned > 0:
            window.add_to_display(0, "[S]", curses.COLOR_MAGENTA,
                    highlight=self.sub_selection == 1)
            window.add_to_display(4, "Sell", curses.COLOR_CYAN)
            window.add_newlines(1)
        window.add_to_display(0, '[H]', curses.COLOR_MAGENTA,
                highlight=self.sub_selection == (2 if self.coin.quantity_owned > 0 else 1))
        window.add_to_display(4, "History", curses.COLOR_CYAN)

        window.add_newlines(2)
        window.add_to_display(0, '[R]', curses.COLOR_MAGENTA,
                highlight=self.sub_selection == (3 if self.coin.quantity_owned > 0 else 2))
        window.add_to_display(4, "Return", curses.COLOR_CYAN)

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
            else: # player selected Return
                if not self.coin.ipo:
                    self.coin.unfreeze()
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
    def add_prompt(self, window: SimpleWindow):
        pass

    @abstractmethod
    def handle_quantity(self, quantity: int):
        pass

    def handle_selection(self, stdscr):
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

    def add_prompt(self, window):
        window.add_to_display(0,
                f"How much {self.coin.name} do you want to buy? (max {self.get_max_quantity()})")
        window.add_newlines(1)
        window.add_to_display(0, "> ", curses.COLOR_BLUE)
        window.add_to_display(2, self.user_input)

    def handle_quantity(self, quantity: int):
        int_price = int(self.coin.price)
        total_cost = quantity * int(self.coin.price)
        self.game_state.player.coins -= total_cost
        self.coin.log_purchase(quantity, int_price)


class SellSelector(QuantitySelector):

    def get_max_quantity(self):
        return self.coin.quantity_owned

    def add_prompt(self, window):
        window.add_to_display(0,
                              f"How much {self.coin.name} do you want to sell? (max {self.get_max_quantity()})")
        window.add_newlines(1)
        window.add_to_display(0, "> ", curses.COLOR_BLUE)
        window.add_to_display(2, self.user_input)

    def handle_quantity(self, quantity: int):
        int_price = int(self.coin.price)
        total_cost = quantity * int(self.coin.price)
        self.game_state.player.coins += total_cost
        self.coin.log_sale(quantity, int_price)


class TransactionHistoryDisplay(CryptoExchangeExtension):
    def __init__(self, game_state: GameState, coin: CryptoCurrency):
        super().__init__(game_state)
        self.coin = coin
        # TODO paginate this
        self.transactions_per_page = 10
        self.page = 0

    def add_header(self, window: SimpleWindow):
        window.add_to_display(0, self.coin.name, curses.COLOR_CYAN)
        window.add_to_display(len(self.coin.name) + 1, "Transaction History:", curses.COLOR_MAGENTA)

    def add_coin_options(self, window): pass

    def add_additional_options(self, window: SimpleWindow): pass

    def add_prompt(self, window: SimpleWindow):
        self.add_header(window)
        window.add_newlines(1)
        for i in range(len(self.coin.history.transactions)):
            window.add_newlines(1)
            transaction = self.coin.history.transactions[i]
            if transaction.type == TransactionType.BUY:
                window.add_to_display(0, f"{transaction.format_timestamp()} | "
                                               f"Buy {transaction.quantity} @ {transaction.price}")
            elif transaction.type == TransactionType.SELL:
                window.add_to_display(0, f"{transaction.format_timestamp()} | "
                                               f"Sell {transaction.quantity} @ {transaction.price}")
        window.add_newlines(2)
        window.add_to_display(0,"Press <enter> to return.", color=curses.COLOR_CYAN)

    def handle_selection(self, stdscr):
        ch = stdscr.getch()
        if ch in (curses.KEY_ENTER, 10, 13):
            self.can_exit = True

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

    def add_to_window(self, window: SimpleWindow, selected: int):
        window.add_newlines(1)
        self.add_header(window)
        for i in range(0, len(self.coins)):
            self.add_coin(window, i, selected)

    def add_header(self, window: SimpleWindow):
        for i in range(len(self.headers)):
            window.add_to_display(self.offsets[i], self.headers[i])

    def add_coin(self, window: SimpleWindow, idx: int, selected: int):
        parts = self.get_coin_line_parts(coin=self.coins[idx])
        window.add_newlines(1)
        window.add_to_display(0, f'[{idx+1}]', curses.COLOR_MAGENTA, highlight=selected == idx+1)
        for i in range(len(parts)):
            part = parts[i]
            window.add_to_display(self.offsets[i], part.value, color=part.color, underline=part.underlined,
                                  highlight=part.highlighted, dim=part.dim)

    def refresh(self):
        self._ingest_coins()
