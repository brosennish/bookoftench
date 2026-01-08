from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from savethewench.data.cryptocurrencies import Crypto_Currencies, Shit_Coin_Names

_max_update_latency = 3  # seconds
_max_coins = 5


class TransactionType(Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass
class Transaction:
    quantity: int
    price: int
    type: TransactionType


class TransactionHistory:
    def __init__(self):
        self.owned: int = 0
        self.cost_basis: float = 0
        self.history: List[Transaction] = []

    def log_buy(self, quantity: int, price: int):
        self.history.append(Transaction(quantity=quantity, price=price, type=TransactionType.BUY))
        self.owned += quantity

    def log_sell(self, quantity: int, price: int):
        self.history.append(Transaction(quantity=quantity, price=price, type=TransactionType.SELL))
        self.owned -= quantity


@dataclass
class CryptoCurrency:
    name: str
    price: float
    lower_limit: int
    upper_limit: int
    volatility: float
    frozen: bool = True
    ipo: bool = True

    history: TransactionHistory = field(default_factory=TransactionHistory)

    _trigger: float = 0
    _start_price: float = 0
    _last_update: float = 0

    _mu: float = 0.0
    _sigma: float = 0.0

    def __post_init__(self):
        self._update_trigger()
        self._sigma = self.volatility / 2.0
        self._start_price = self.price

    @property
    def start_time(self):
        return self._last_update

    @start_time.setter
    def start_time(self, start_time: float):
        self._last_update = start_time

    @property
    def historical_percent_change(self) -> float:
        return round(((self.price - self._start_price) / self._start_price) * 100, 2)

    @property
    def quantity_owned(self) -> int:
        return self.history.owned

    @property
    def delisted(self) -> bool:
        return self.price == 0

    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        self.start_time = time.time()
        self.ipo = False
        self.frozen = False

    def _update_trigger(self):
        self._trigger = random.uniform(0, _max_update_latency)

    def _update_price(self):
        if self.delisted:
            return
        delta = random.gauss(self._mu, self._sigma)
        new_price = self.price + (self._start_price * delta)
        if new_price > self.upper_limit:
            pass  # TODO
        elif new_price < self.lower_limit:
            pass  # TODO
        self.price = max(new_price, 0)

    def poll_market(self):
        current_time = time.time()
        if self.frozen:
            self._last_update = current_time
            return
        elapsed = current_time - self._last_update
        if elapsed > self._trigger:
            self._update_price()
            self._update_trigger()
            self._last_update = current_time

    def format_price(self) -> str:
        return f"{self.price:.2f}"

    def format_percent_change(self) -> str:
        return f"{self.historical_percent_change:.2f}%"

    def log_purchase(self, quantity: int, price: int):
        self.history.log_buy(quantity, price)

    def log_sale(self, quantity: int, price: int):
        self.history.log_sell(quantity, price)


@dataclass
class ShitCoin(CryptoCurrency):
    price: float = 0
    lower_limit: int = 0
    upper_limit: int = 0
    volatility: float = 0

    def __post_init__(self):
        # TODO set bounds somewhere more configurable
        self.price = random.randint(10, 1000)
        self.upper_limit = random.randint(10 ** 3, 10 ** 6)
        self.volatility = random.uniform(0.25, 0.75)
        super().__post_init__()


class ShitCoinGenerator:
    def __init__(self):
        self.gen_iteration = 1
        self.coin_pool = []

    def _populate_coin_pool(self):
        if len(self.coin_pool) == 0:
            self.coin_pool = [ShitCoin(
                name=f"{name} {self.gen_iteration}" if self.gen_iteration > 1 else name
            ) for name in [f"{sc} Coin" for sc in Shit_Coin_Names]]
            random.shuffle(self.coin_pool)
            self.gen_iteration += 1

    def generate(self) -> ShitCoin:
        self._populate_coin_pool()
        return self.coin_pool.pop()


@dataclass
class CryptoMarketState:
    max_active_coins: int = 5
    active_coins: List[CryptoCurrency] = field(default_factory=list)
    delisted_coins: List[CryptoCurrency] = field(default_factory=list)
    shit_coin_generator: ShitCoinGenerator = field(default_factory=ShitCoinGenerator)

    @classmethod
    def defaults(cls) -> CryptoMarketState:
        return CryptoMarketState(active_coins=[CryptoCurrency(**d) for d in Crypto_Currencies])
