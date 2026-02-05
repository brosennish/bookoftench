from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List

from bookoftench.model.crypto import CryptoMarketState, CryptoCurrency


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

    def populate_market_state(self):
        while len(self.active_coins) < self.max_active_coins:
            self.market_state.list_new_coin()


_state: Optional[State] = None


def init(market_state: CryptoMarketState) -> None:
    global _state
    if _state is not None:
        # TODO log that state is being reinitialized and old thread is being killed
        stop()
    _state = State(market_state)


def _run() -> None:
    while not _state.stop_event.is_set():
        _state.populate_market_state()
        for coin in _state.active_coins:
            _state.executor.submit(coin.poll_market if not coin.zeroed else coin.poll_delist)
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
