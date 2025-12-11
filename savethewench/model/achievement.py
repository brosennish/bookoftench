from dataclasses import dataclass
from typing import Optional, List

from savethewench.data import Achievements


@dataclass
class Achievement:
    id: str
    name: str
    description: str
    reward_type: str
    reward_value: Optional[int]

def load_achievements() -> List[Achievement]:
    return [Achievement(**d) for d in Achievements]