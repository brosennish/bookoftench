import random
from dataclasses import dataclass
from typing import List

from bookoftench.data.investments import Investment_Opportunities, Risk_Levels
from bookoftench.model.base import Buyable
from bookoftench.ui import dim, cyan, orange, green, red, white

# ================================================================================================

@dataclass
class Investment(Buyable):
    name: str
    description: str
    risk_level: str
    buy_ins: list | None

    success_rate: float | None
    success_text: str
    failure_text: str
    multiplier: float | None

    levels_to_maturity: int | None
    maturity_lvl: int | None = None

    buy_in: int = 0
    resolved: bool = False

# ================================================================================================

    def __post_init__(self):
        self.buy_ins = [10, 25, 50]

        risk_dict = next(i for i in Risk_Levels if i['name'] == self.risk_level)
        self.get_success_rate(risk_dict)
        self.get_levels_to_maturity(risk_dict)
        self.get_multiplier(risk_dict)

# ================================================================================================

    def get_success_rate(self, risk_dict: dict):
        self.success_rate = random.uniform(
            risk_dict['min_success_rate'],
            risk_dict['max_success_rate']
        )

    def get_levels_to_maturity(self, risk_dict: dict):
        min_levels = risk_dict['min_levels']
        max_levels = risk_dict['max_levels']
        self.levels_to_maturity = random.randint(min_levels, max_levels)

    def get_multiplier(self, risk_dict: dict):
        min_multiplier = risk_dict['min_multiplier']
        max_multiplier = risk_dict['max_multiplier']
        self.multiplier = random.uniform(min_multiplier, max_multiplier)

# ================================================================================================

    def get_simple_format(self) -> str:
        return dim(' | ').join([
            cyan(f"{self.name:<19}"),
            f"Risk: {orange(self.risk_level)}",
            f"Return: {green(f'{self.multiplier:.1f}x')}",
            f"Maturity: {cyan(f'{self.levels_to_maturity} lvl')}",
        ])

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<19}"),
            f"Risk: {orange(f'{self.risk_level:<11}')}",
            f"Return: {green(f'{self.multiplier:.1f}x')}",
            f"Maturity: {cyan(f'{self.levels_to_maturity} lvl')}",
            white(self.description),
        ])

# ================================================================================================

def load_investment(name: str) -> Investment:
    matches = load_investments([name])
    if len(matches) == 0:
        raise ValueError(f"Could not find investment data for {name}")
    return matches[0]

def load_investments(restriction: List[str] = None) -> List[Investment]:
    return [Investment(**d) for d in Investment_Opportunities if restriction is None or d['name'] in restriction]