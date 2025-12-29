from dataclasses import dataclass
from typing import List

from savethewench.data import Items
from savethewench.model.base import Buyable
from savethewench.ui import dim, cyan, orange, green


@dataclass
class Item(Buyable):
    name: str
    hp: int
    cost: int
    sell_value: int
    area: str

    def get_simple_format(self) -> str:
        return dim(' | ').join([
            cyan(f"{self.name:<24}"),
            f"HP: +{green(self.hp)}"
        ])

    def get_found_format(self) -> str:
        return dim(' | ').join([
            cyan(f"{self.name:}"),
            f"HP: +{green(self.hp)}"
        ])

    def to_sellable_item(self) -> "SellableItem":
        return SellableItem(**vars(self))

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<24}"),
            f"Cost: {orange(self.cost):<18}",
            f"HP: +{green(self.hp)}"
        ])


@dataclass
class SellableItem(Item):
    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<24}"),
            f"Value: {orange(self.sell_value):<17}",
            f"HP: +{green(self.hp)}"
        ])


def load_items(restriction: List[str] = None) -> List[Item]:
    return [Item(**d) for d in Items if restriction is None or d['name'] in restriction]
