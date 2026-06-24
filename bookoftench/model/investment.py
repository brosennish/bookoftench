import random
from dataclasses import dataclass

from bookoftench.data.investments import Investment_Opportunities, Risk_Levels
from bookoftench.ui import dim, cyan, orange, green, white

# ================================================================================================

@dataclass
class Investment:
    name: str
    description: str
    risk_level: str
    success_text: str
    failure_text: str

    cost: int = 0
    value: int = 0
    buy_ins: list[int] | None = None
    success_rate: float = 0
    multiplier: float = 0
    levels_to_maturity: int = 0
    maturity_lvl: int | None = None
    active: bool = False

# ================================================================================================

    def __post_init__(self) -> None:
        self.buy_ins = [10, 25, 50, 100]

        risk_data = next(
            risk
            for risk in Risk_Levels
            if risk["name"] == self.risk_level
        )
        self.get_success_rate(risk_data)
        self.get_levels_to_maturity(risk_data)
        self.get_multiplier(risk_data)

# ================================================================================================

    def get_success_rate(self, risk_data: dict) -> None:
        self.success_rate = random.uniform(
            risk_data["min_success_rate"],
            risk_data["max_success_rate"],
        )

    def get_levels_to_maturity(self, risk_data: dict) -> None:
        min_levels = risk_data["min_levels"]
        max_levels = risk_data["max_levels"]
        self.levels_to_maturity = random.randint(min_levels, max_levels)

    def get_multiplier(self, risk_data: dict) -> None:
        min_multiplier = risk_data["min_multiplier"]
        max_multiplier = risk_data["max_multiplier"]
        self.multiplier = random.uniform(min_multiplier, max_multiplier)

# ================================================================================================

    def get_simple_format(self) -> str:
        return dim(" | ").join([
            cyan(f"{self.name:<19}"),
            f"Risk: {orange(self.risk_level)}",
            f"Return: {green(f'{self.multiplier:.1f}x')}",
            f"Maturity: {cyan(f'{self.levels_to_maturity} lvl')}",
        ])

    def __repr__(self) -> str:
        return dim(" | ").join([
            cyan(f"{self.name:<19}"),
            f"Risk: {orange(f'{self.risk_level:<11}')}",
            f"Return: {green(f'{self.multiplier:.1f}x')}",
            f"Maturity: {cyan(f'{self.levels_to_maturity} lvl')}",
            white(self.description),
        ])

# ================================================================================================

def load_investment(name: str) -> Investment:
    matches = load_investments([name])

    if not matches:
        raise ValueError(f"Could not find investment data for {name}")

    return matches[0]


def load_investments(restriction: list[str] | None = None) -> list[Investment]:
    return [
        Investment(**data)
        for data in Investment_Opportunities
        if restriction is None or data["name"] in restriction
    ]

# ================================================================================================

@dataclass
class Investment:
    name: str
    description: str
    risk_level: str
    success_text: str
    failure_text: str

    cost: int = 0
    value: int = 0
    buy_ins: list | None = None
    success_rate: float = 0
    multiplier: float = 0
    levels_to_maturity: int = 0
    maturity_lvl: int | None = None
    active: bool = False

# ================================================================================================

    def __post_init__(self):
        self.buy_ins = [10, 25, 50, 100]

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