from dataclasses import dataclass
from typing import List
from savethewench.data import Items

@dataclass
class Item:
    name: str
    hp: int
    cost: int
    sell_value: int


def load_items(restriction: List[str] = None) -> List[Item]:
    return [Item(**d) for d in Items if restriction is None or d['name'] in restriction]