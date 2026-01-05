from typing import List

from savethewench.audio import play_music
from savethewench.component.base import LabeledSelectionComponent, SelectionBinding, functional_component, \
    BinarySelectionComponent
from savethewench.component.registry import register_component
from savethewench.data.audio import BANK_THEME
from savethewench.data.components import BANK
from savethewench.model import GameState
from savethewench.model.util import display_bank_balance
from savethewench.ui import blue, yellow
from savethewench.util import print_and_sleep, safe_input


def _very_well():
    print_and_sleep(blue("Very well..."), 1)


@register_component(BANK)
class BankComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState, allow_deposit=True):
        self.allow_deposit = allow_deposit
        super().__init__(game_state, bindings=self._get_bindings(), top_level_prompt_callback=display_bank_balance)
        self.bank = self.game_state.bank
        self.leave_bank = False
        self._display_greeting()

    def play_theme(self):
        play_music(BANK_THEME)

    def _get_bindings(self) -> List[SelectionBinding]:
        res = [SelectionBinding('W', 'Withdraw', self._make_withdrawal(not self.allow_deposit)),
               SelectionBinding('Q', 'Leave', functional_component()(self._return))]
        if self.allow_deposit:
            return [SelectionBinding('D', 'Deposit', self._make_deposit), *res]
        return res

    def _display_greeting(self):
        if self.allow_deposit:
            print_and_sleep("Welcome to the Shebokken Transnational Offshore Bank.\n"
                            "While banking with us, you may deposit or withdraw coins.\n"
                            f"Each time you level up, your account value will increase by "
                            f"{int(self.bank.interest_rate * 100)}%.", 1)
        else:
            print_and_sleep("Welcome to the Shebokken Transnational Offshore Bank.\n"
                            "We do not accept deposits between level-ups.\n"
                            "Withdrawals will incur a 10% fee.", 1)

    @staticmethod
    @functional_component(state_dependent=True)
    def _make_deposit(game_state: GameState):
        raw_amount = safe_input("How much would you like to deposit?")
        if raw_amount.isdigit():
            amount = int(raw_amount)
            if amount <= game_state.player.coins:
                game_state.bank.make_deposit(amount)
                game_state.player.coins -= amount
            else:
                print_and_sleep(yellow("You don't have that many coins."), 1)
        else:
            print_and_sleep(yellow("Invalid choice."))

    @staticmethod
    def _make_withdrawal(incur_fee=False):
        @functional_component(state_dependent=True)
        def component(game_state: GameState):
            raw_amount = safe_input("How much would you like to withdraw?")
            if raw_amount.isdigit():
                amount = int(raw_amount)
                if incur_fee:
                    amount = int(amount * 0.9)
                    print_and_sleep(yellow("10% fee applied."), 1)
                if game_state.bank.make_withdrawal(amount):
                    game_state.player.coins += amount
            else:
                print_and_sleep(yellow("Invalid choice."))
        return component

    def _return(self):  # TODO stop duplicating this pattern
        _very_well()
        self.leave_bank = True

    def can_exit(self):
        return self.leave_bank


class BankVisitDecision(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, query="Would you like to visit the bank?",
                         yes_component=BankComponent, no_component=functional_component()(_very_well))


class WithdrawalOnlyBank(BankComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, allow_deposit=False)
