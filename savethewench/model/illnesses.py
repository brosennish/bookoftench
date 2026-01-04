from dataclasses import dataclass
from typing import List

from savethewench.data.illnesses import All_Illnesses
from savethewench.model.illness import Illness


@dataclass
class Illnesses:

    def __post_init__(self):
        self._all_illnesses = [i for i in All_Illnesses]

    @property
    def all_illnesses(self) -> List[Illness]:
        return [
            Illness(**illness_dict)
            for illness_dict in All_Illnesses
        ]

