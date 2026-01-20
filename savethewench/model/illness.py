from dataclasses import dataclass

from savethewench.ui import dim, cyan, orange, yellow


@dataclass
class Illness:
    name: str
    description: str
    levels_until_death: int
    cost: int
    success_rate: float

    def get_simple_format(self) -> str:
        return dim(' | ').join([
            cyan(f"{self.name:<19}"),
            f"Cost: +{orange(self.cost)}"
            f"Success rate: +{yellow(int(self.success_rate * 100))}",
        ])

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<19}"),
            f"Cost: {orange(self.cost)}",
            f"Success rate: {yellow(f'{int(self.success_rate * 100)}%')}"
        ])
