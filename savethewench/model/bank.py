from dataclasses import dataclass

from savethewench import event_logger
from savethewench.event_logger import subscribe_function
from savethewench.model.events import LevelUpEvent, BankWithdrawalEvent, BankDepositEvent
from savethewench.ui import yellow, green
from savethewench.util import print_and_sleep


@dataclass
class Bank:
    balance: int = 0
    interest: int = 0
    interest_rate: float = 0.10

    def __post_init__(self):
        self._subscribe_listeners()

    def make_deposit(self, amount: int):
        self.balance += amount
        event_logger.log_event(BankDepositEvent(amount))

    def make_withdrawal(self, amount: int) -> bool:
        if amount > self.balance:
            print_and_sleep(yellow("Insufficient funds for withdrawal.\n"), 1)
            return False
        self.balance -= amount
        event_logger.log_event(BankWithdrawalEvent(amount))
        return True

    def apply_interest(self):
        self.interest += int(self.balance * self.interest_rate)
        self.balance += int(self.balance * self.interest_rate)

    def _subscribe_listeners(self):
        @subscribe_function(LevelUpEvent)
        def handle_level_up(_: LevelUpEvent):
            self.apply_interest()
