from dataclasses import dataclass
from typing import Optional, List, Callable

from data.achievements import Achievements
from events import Listener, E
from model.game_state import GameState


@dataclass
class Achievement(Listener[E]):
    id: str
    name: str
    description: str
    reward_type: str
    reward_value: Optional[int]
    listen_event: type[E]
    trigger: Callable[[GameState], bool]

    def get_listen_type(self) -> E:
        pass

    def register(self, event: E):
        pass

def load_achievements() -> List[Achievement]:
    return [Achievement(**d) for d in Achievements]