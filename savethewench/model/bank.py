from dataclasses import dataclass

from savethewench.ui import yellow
from savethewench.util import print_and_sleep


@dataclass
class Bank:
    balance: int = 0
    interest_rate: float = 0.10

    def make_withdrawal(self, amount: int) -> bool:
        if amount > self.balance:
            print_and_sleep(yellow("Insufficient funds for withdrawal.\n"), 1)
            return False
        self.balance -= amount
        return True