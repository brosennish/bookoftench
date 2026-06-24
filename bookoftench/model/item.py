from __future__ import annotations

from dataclasses import asdict, dataclass

from bookoftench.data import Items
from bookoftench.data.items import BOSS
from bookoftench.model.base import Buyable
from bookoftench.ui import cyan, dim, green, orange

# ================================================================================================

@dataclass
class Item(Buyable):
    name: str
    type: str
    hp: int
    cost: int
    sell_value: int
    areas: list[str] | None
    desc: str | None
    sound: str

    def get_simple_format(self, length: int) -> str:
        if self.type == BOSS:
            return dim(" | ").join([
                cyan(f"{self.name:<{length}}"),
                f"HP: +{green(self.hp)}",
                f"{self.desc}",
            ])

        return dim(" | ").join([
            cyan(f"{self.name:<{length}}"),
            f"HP: +{green(self.hp)}" if self.hp > 0 else f"{self.desc}",
        ])

    def get_found_format(self) -> str:
        return dim(" | ").join([
            cyan(f"{self.name:}"),
            f"HP: +{green(self.hp)}" if self.hp > 0 else f"{self.desc}",
        ])

    def to_sellable_item(self) -> SellableItem:
        return SellableItem.from_dict(asdict(self))

    def __repr__(self) -> str:
        return dim(" | ").join([
            cyan(f"{self.name:<24}"),
            f"Cost: {orange(self.cost):<18}",
            f"HP: +{green(self.hp)}" if self.hp > 0 else f"{self.desc}",
        ])

# ================================================================================================

@dataclass
class SellableItem(Item):
    def __repr__(self) -> str:
        if self.type == BOSS:
            if self.hp > 0:
                return dim(" | ").join([
                    cyan(f"{self.name:<24}"),
                    f"Value: {orange(self.sell_value):<18}",
                    f"HP: +{green(self.hp)}",
                    f"{self.desc}",
                ])

            return dim(" | ").join([
                cyan(f"{self.name:<24}"),
                f"Value: {orange(self.sell_value):<18}",
                f"{self.desc}",
            ])

        return dim(" | ").join([
            cyan(f"{self.name:<24}"),
            f"Value: {orange(self.sell_value):<18}",
            f"HP: +{green(self.hp)}" if self.hp > 0 else f"{self.desc}",
        ])


def load_items(restriction: list[str] | None = None) -> list[Item]:
    return [
        Item(**data)
        for data in Items
        if restriction is None or data["name"] in restriction
    ]

def load_boss_item(name: str) -> Item:
    matches = load_items([name])

    if not matches:
        raise ValueError(f"Could not find item data for {name}")

    return matches[0]
