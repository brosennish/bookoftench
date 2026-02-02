from dataclasses import dataclass
from typing import List


@dataclass
class Discoverable:
    name: str
    value: int
    hp: int
    rarity: str
    areas: List[str]