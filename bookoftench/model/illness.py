from dataclasses import dataclass

from bookoftench.data.illnesses import Illnesses
from bookoftench.ui import cyan, dim, orange, yellow

# ================================================================================================

@dataclass
class Illness:
    name: str
    description: str
    levels_until_death: int
    cost: int
    success_rate: float
    hp_loss: int
    death_message: str

    @property
    def causes_instant_death(self) -> bool:
        return self.levels_until_death == 0

    def get_simple_format(self) -> str:
        return dim(" | ").join([
            cyan(f"{self.name:<19}"),
            f"Cost: +{orange(self.cost)}",
            f"Success rate: +{yellow(int(self.success_rate * 100))}",
        ])

    def __repr__(self) -> str:
        return self.get_simple_format()

# ================================================================================================

def load_illness(entry: dict | None) -> Illness | None:
    if not entry:
        return None

    return Illness(**entry)


def load_illnesses(restriction: list[str] | None = None) -> list[Illness]:
    return [
        Illness(**data)
        for data in Illnesses
        if restriction is None or data["name"] in restriction
    ]
