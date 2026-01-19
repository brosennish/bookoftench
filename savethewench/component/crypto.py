import curses
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import savethewench.service.crypto_service as crypto_service
from savethewench.audio import play_music, play_sound
from savethewench.component.base import Component
from savethewench.component.registry import register_component
from savethewench.curses_util import init_colors, c_print
from savethewench.data.audio import CRYPTO_THEME, PURCHASE
from savethewench.data.components import CRYPTO_EXCHANGE
from savethewench.model import GameState
from savethewench.model.crypto import CryptoCurrency, TransactionType


@dataclass
class LinePart:
    text: str
    color: int = curses.COLOR_WHITE
    underline: bool = False
    highlight: bool = False
    bold: bool = False
    dim: bool = False
    offset: int = 0

    def add_to_line(self, stdscr, line: int, offset: int):
        c_print(stdscr, line, offset, self.text, self.color,
                underline=self.underline, highlight=self.highlight, bold=self.bold, dim=self.dim)


@dataclass
class Line:
    parts: List[LinePart]
    line_number: int = 0

    def add_to_screen(self, stdscr):
        for part in self.parts:
            c_print(stdscr, self.line_number, offset=part.offset, text=part.text, color=part.color,
                    highlight=part.highlight, underline=part.underline, bold=part.bold, dim=part.dim)


class SimpleWindow:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self._current_line = 0
        self._lines = []

    def add_line(self, line: Line):
        line.line_number = self._current_line
        self._lines.append(line)
        self.add_newlines(1)

    def add_newlines(self, newlines: int):
        self._current_line += newlines

    def flush(self):
        self.stdscr.clear()
        for line in self._lines:
            line.add_to_screen(self.stdscr)
        self.stdscr.refresh()
        self._lines.clear()
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

    def play_theme(self):
        play_music(CRYPTO_THEME)

    def add_header(self, window):
        window.add_line(Line(parts=[LinePart('Crypto Market', color=curses.COLOR_MAGENTA, underline=True, bold=True)]))
        window.add_newlines(1)
        greeting_parts = [LinePart(f"Welcome, {self.game_state.player.name}. You have ", color=curses.COLOR_WHITE),
                          LinePart(f"{self.game_state.player.coins}", color=curses.COLOR_GREEN),
                          LinePart(" of coin to spend.", color=curses.COLOR_WHITE)]
        offset = 0
        for part in greeting_parts:
            part.offset = offset
            offset += len(part.text)
        window.add_line(Line(greeting_parts))

    def add_additional_options(self, window):
        window.add_newlines(1)
        window.add_line(
            Line([LinePart('[R]', color=curses.COLOR_MAGENTA, highlight=self.selected == len(self.coins) + 1),
                  LinePart('Return', color=curses.COLOR_CYAN, offset=4)]))

    def add_coin_options(self, window):
        window.add_newlines(1)
        for line in self.coin_options.to_lines(self.selected):
            window.add_line(line)

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
        elif ch in range(ord('1'), ord(str(len(self.coins))) + 1):
            self.selected = int(chr(ch))
        elif ch in (ord('r'), ord('R')):
            self.selected = len(self.coins) + 1

    def c_run(self, stdscr):
        init_colors()
        window = SimpleWindow(stdscr)
        self.play_theme()
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
        window.add_newlines(1)
        window.add_line(Line([LinePart('[B]', color=curses.COLOR_MAGENTA, highlight=self.sub_selection == 0),
                              LinePart('Buy', color=curses.COLOR_CYAN, offset=4)]))
        if self.coin.quantity_owned > 0:
            window.add_line(Line([LinePart('[S]', color=curses.COLOR_MAGENTA, highlight=self.sub_selection == 1),
                                  LinePart('Sell', color=curses.COLOR_CYAN, offset=4)]))
        window.add_line(Line([LinePart('[H]', color=curses.COLOR_MAGENTA,
                                       highlight=self.sub_selection == (2 if self.coin.quantity_owned > 0 else 1)),
                              LinePart('History', color=curses.COLOR_CYAN, offset=4)]))
        window.add_newlines(1)
        window.add_line(Line([LinePart('[R]', color=curses.COLOR_MAGENTA,
                                       highlight=self.sub_selection == (3 if self.coin.quantity_owned > 0 else 2)),
                              LinePart('Return', color=curses.COLOR_CYAN, offset=4)]))

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
            else:  # player selected Return
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
                play_sound(PURCHASE)
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
        window.add_newlines(1)
        window.add_line(
            Line([LinePart(f"How much {self.coin.name} do you want to buy? (max {self.get_max_quantity()})")]))
        window.add_line(Line([LinePart('> ', color=curses.COLOR_BLUE), LinePart(self.user_input, offset=2)]))

    def handle_quantity(self, quantity: int):
        int_price = int(self.coin.price)
        total_cost = quantity * int(self.coin.price)
        self.game_state.player.coins -= total_cost
        self.coin.log_purchase(quantity, int_price)


class SellSelector(QuantitySelector):

    def get_max_quantity(self):
        return self.coin.quantity_owned

    def add_prompt(self, window):
        window.add_newlines(1)
        window.add_line(
            Line([LinePart(f"How much {self.coin.name} do you want to sell? (max {self.get_max_quantity()})")]))
        window.add_line(Line([LinePart('> ', color=curses.COLOR_BLUE), LinePart(self.user_input, offset=2)]))

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
        window.add_line(Line([LinePart(self.coin.name, color=curses.COLOR_CYAN),
                              LinePart("Transaction History:", color=curses.COLOR_MAGENTA,
                                       offset=len(self.coin.name) + 1)]))

    def add_coin_options(self, window):
        pass

    def add_additional_options(self, window: SimpleWindow):
        pass

    def add_prompt(self, window: SimpleWindow):
        window.add_newlines(1)
        for i in range(len(self.coin.history.transactions)):
            transaction = self.coin.history.transactions[i]
            if transaction.type == TransactionType.BUY:
                window.add_line(Line([LinePart(f"{transaction.format_timestamp()} | "
                                               f"Buy {transaction.quantity} @ {transaction.price}")]))
            elif transaction.type == TransactionType.SELL:
                window.add_line(Line([LinePart(f"{transaction.format_timestamp()} | "
                                               f"Sell {transaction.quantity} @ {transaction.price}")]))
        window.add_newlines(1)
        window.add_line(Line([LinePart("Press <enter> to return.", color=curses.COLOR_CYAN)]))

    def handle_selection(self, stdscr):
        ch = stdscr.getch()
        if ch in (curses.KEY_ENTER, 10, 13):
            self.can_exit = True


def header_part(value: str) -> LinePart:
    return LinePart(value, underline=True)


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
                widths[i] = max(widths[i], len(part.text))

        self.offsets = [0] * self.columns
        self.offsets[0] = len(str(len(self.coins))) + 3
        for i in range(1, self.columns):
            self.offsets[i] = self.offsets[i - 1] + widths[i - 1] + 3

    def to_lines(self, selected: int) -> List[Line]:
        res = [Line([LinePart(self.headers[i], offset=self.offsets[i]) for i in range(len(self.headers))])]
        for idx in range(len(self.coins)):
            coin = self.coins[idx]
            parts = [LinePart(f'[{idx + 1}]', curses.COLOR_MAGENTA, highlight=selected == idx + 1)]
            for i in range(self.columns):
                lp = self.coin_line_part_factories[i](coin)
                lp.offset = self.offsets[i]
                parts.append(lp)
            res.append(Line(parts))
        return res

    def refresh(self):
        self._ingest_coins()
