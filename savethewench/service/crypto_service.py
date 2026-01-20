from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List

from savethewench.model.crypto import CryptoMarketState, CryptoCurrency, ShitCoinGenerator


class State:
    def __init__(self, market_state: CryptoMarketState):
        self.market_state = market_state
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=_run, daemon=True)
        self.executor = ThreadPoolExecutor(market_state.max_active_coins)
        self.interval = 0.1

    @property
    def active_coins(self) -> List[CryptoCurrency]:
        return self.market_state.active_coins

    @property
    def max_active_coins(self) -> int:
        return self.market_state.max_active_coins

    @property
    def shit_coin_generator(self) -> ShitCoinGenerator:
        return self.market_state.shit_coin_generator


_state: Optional[State] = None


def init(market_state: CryptoMarketState) -> None:
    global _state
    _state = State(market_state)


def _run() -> None:
    coins = _state.active_coins
    shit_coin_generator = _state.market_state.shit_coin_generator
    while not _state.stop_event.is_set():
        while len(coins) < _state.max_active_coins:
            coins.append(shit_coin_generator.generate())
        for coin in coins:
            func = coin.poll_market if coin.delisted else coin.poll_market
            _state.executor.submit(func)
        _state.stop_event.wait(_state.interval)


def start() -> None:
    if _state.thread.is_alive():
        return
    service_start = time.time()
    for coin in _state.active_coins:
        coin.start_time = service_start
    _state.thread.start()


def stop() -> None:
    _state.stop_event.set()
    _state.thread.join()
    _state.executor.shutdown(wait=True)


def get_active_coins():
    return [c for c in _state.active_coins]
