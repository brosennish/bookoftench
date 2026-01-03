from dataclasses import dataclass
from savethewench.ui import dim, red, cyan, orange, green


@dataclass
class Illness():
    name: str
    hp: int
    cost: int
    risk: float

    def get_simple_format(self) -> str:
        return dim(' | ').join([
            cyan(f"{self.name:<19}"),
            f"HP: +{green(self.hp)}",
        ])

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<19}"),
            f"Cost: {orange(self.cost)}",
            f"HP: +{green(self.hp)}",
            f"Risk: {red(f'{int(self.risk * 100)}%')}"
        ])