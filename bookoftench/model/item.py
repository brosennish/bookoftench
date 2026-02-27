from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List

from bookoftench.data import Items
from bookoftench.model.base import Buyable
from bookoftench.ui import dim, cyan, orange, green


@dataclass
class Item(Buyable):
    name: str
    type: str
    hp: int
    cost: int
    sell_value: int
    areas: List[str]
    desc: str | None

    def get_simple_format(self, length: int) -> str:
        return dim(' | ').join([
            cyan(f"{self.name:<{length}}"),
            (f"HP: +{green(self.hp)}" if self.hp > 0 else f"{self.desc}")
        ])

    def get_found_format(self) -> str:
        return dim(' | ').join([
            cyan(f"{self.name:}"),
            (f"HP: +{green(self.hp)}" if self.hp > 0 else f"{self.desc}")
        ])

    def to_sellable_item(self) -> SellableItem:
        return SellableItem.from_dict(asdict(self))

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<24}"),
            f"Cost: {orange(self.cost):<18}",
            (f"HP: +{green(self.hp)}" if self.hp > 0 else f"{self.desc}"),
        ])


@dataclass
class SellableItem(Item):
    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<24}"),
            f"Value: {orange(self.sell_value):<17}",
            (f"HP: +{green(self.hp)}" if self.hp > 0 else f"{self.desc}"),
        ])


def load_items(restriction: List[str] = None) -> List[Item]:
    return [Item(**d) for d in Items if restriction is None or d['name'] in restriction]
