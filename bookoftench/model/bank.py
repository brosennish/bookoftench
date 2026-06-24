from dataclasses import dataclass

from bookoftench import event_logger
from bookoftench.data.perks import SLEDGE_FUND
from bookoftench.event_logger import subscribe_function
from bookoftench.model.events import LevelUpEvent, BankWithdrawalEvent, BankDepositEvent
from bookoftench.model.perk import attach_perk
from bookoftench.ui import yellow
from bookoftench.util import print_and_sleep

from dataclasses import dataclass

from bookoftench import event_logger
from bookoftench.data.perks import SLEDGE_FUND
from bookoftench.event_logger import subscribe_function
from bookoftench.model.events import BankDepositEvent, BankWithdrawalEvent, LevelUpEvent
from bookoftench.model.perk import attach_perk
from bookoftench.ui import yellow
from bookoftench.util import print_and_sleep

# ================================================================================================

@dataclass
class Bank:
    balance: int = 0
    interest: int = 0
    _interest_rate: float = 0.10

    def __post_init__(self) -> None:
        self._subscribe_listeners()

    @property
    @attach_perk(SLEDGE_FUND, silent=True)
    def interest_rate(self) -> float:
        return self._interest_rate

    def make_deposit(self, amount: int) -> None:
        self.balance += amount
        event_logger.log_event(BankDepositEvent(amount))

    def make_withdrawal(self, amount: int) -> bool:
        if amount > self.balance:
            print_and_sleep(yellow("Insufficient funds for withdrawal.\n"), 1)
            return False

        self.balance -= amount
        event_logger.log_event(BankWithdrawalEvent(amount))
        return True

    def apply_interest(self) -> None:
        interest = int(self.balance * self.interest_rate)

        self.interest += interest
        self.balance += interest

    def _subscribe_listeners(self) -> None:
        @subscribe_function(LevelUpEvent)
        def handle_level_up(_: LevelUpEvent) -> None:
            self.apply_interest()

    # For loading from save file.
    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self._subscribe_listeners()
