from typing import List

from savethewench.model.ritual import Ritual

TENCH_SACRIFICE = "Tench Sacrifice"
CARP_SACRIFICE = "Carp Sacrifice"

Rituals = [
    {'name': TENCH_SACRIFICE, 'description': 'Gain one life', 'cost': 500},
    {'name': CARP_SACRIFICE, 'description': 'Gain or lose one life', 'cost': 100}
]


def ritual_inventory() -> List[Ritual]:
    return [
        Ritual(**ritual_dict)
        for ritual_dict in Rituals
    ]