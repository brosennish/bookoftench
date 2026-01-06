import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from savethewench.data.cryptocurrencies import Crypto_Currencies

_max_update_lag = 3 #seconds
_max_coins = 5

@dataclass
class CryptoCurrency:
    name: str
    price: float
    lower_limit: int
    upper_limit: int
    volatility: float
    frozen: bool = True

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

    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        self.frozen = False

    def _update_trigger(self):
        self._trigger = random.uniform(0, _max_update_lag)

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


class CryptoExchangeService:
    def __init__(self):
        self.coins = [CryptoCurrency(**d) for d in Crypto_Currencies]
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
            for coin in self.coins:
                self._executor.submit(coin.poll_market)
            self._stop_event.wait(self.interval)
