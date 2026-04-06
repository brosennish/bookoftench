from dataclasses import dataclass
from typing import List

from bookoftench.data.enemies import Traits


@dataclass
class Trait:
    name: str
    desc: str

def load_traits(restriction: List[str] = None) -> List[Trait]:
    return [Trait(**d) for d in Traits if restriction is None or d['name'] in restriction]

def load_trait(entry: dict | None) -> Trait | None:
    if entry:
        return Trait(**entry)
    else:
        return None