import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from savethewench.data.cryptocurrencies import Crypto_Currencies, Shit_Coin_Names

_max_update_latency = 3 #seconds
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
    def coins_owned(self) -> int:
        return self.history.owned

    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        self.frozen = False

    def _update_trigger(self):
        self._trigger = random.uniform(0, _max_update_latency)

    def _update_price(self):
        if self.price == 0:
            return
        delta = random.gauss(self._mu, self._sigma)
        new_price = self.price + (self._start_price * delta)
        if new_price > self.upper_limit:
            pass # TODO
        elif new_price < self.lower_limit:
            pass # TODO
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
        self.upper_limit = random.randint(10**3, 10**6)
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

class CryptoExchangeService:
    def __init__(self):
        self.coins = [CryptoCurrency(**d) for d in Crypto_Currencies]
        self.shit_coin_generator = ShitCoinGenerator()
        self.interval = 0.1
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._executor = ThreadPoolExecutor(max_workers=_max_coins)

    def start(self):
        if self._thread.is_alive():
            return
        service_start = time.time()
        for coin in self.coins:
            coin.start_time = service_start
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()
        self._executor.shutdown(wait=True)

    def _run(self):
        while not self._stop_event.is_set():
            while len(self.coins) < _max_coins:
                self.coins.append(self.shit_coin_generator.generate())
            for coin in self.coins:
                self._executor.submit(coin.poll_market)
            self._stop_event.wait(self.interval)
