from dataclasses import dataclass, field
from typing import List

from savethewench.data.rituals import Rituals
from savethewench.model.ritual import Ritual


@dataclass
class Occultist:
    _coffee_item_inventory: List[Ritual] = field(init=False)

    def __post_init__(self):
        self._all_coffee_items = [i for i in Rituals]

    @property
    def ritual_inventory(self) -> List[Ritual]:
        return [
            Ritual(**ritual_dict)
            for ritual_dict in Rituals
        ]