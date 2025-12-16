from dataclasses import dataclass

from savethewench.event_logger import subscribe_function
from savethewench.model.events import LevelUpEvent
from savethewench.ui import yellow
from savethewench.util import print_and_sleep


@dataclass
class Bank:
    balance: int = 0
    interest: int = 0
    interest_rate: float = 0.10

    def __post_init__(self):
        self._subscribe_listeners()

    def make_withdrawal(self, amount: int) -> bool:
        if amount > self.balance:
            print_and_sleep(yellow("Insufficient funds for withdrawal.\n"), 1)
            return False
        self.balance -= amount
        return True

    def apply_interest(self):
        self.interest += int(self.balance * self.interest_rate)
        self.balance += int(self.balance * self.interest_rate)
        print("Applied interest")

    def _subscribe_listeners(self):
        @subscribe_function(LevelUpEvent)
        def handle_level_up(_: LevelUpEvent):
            self.apply_interest()
