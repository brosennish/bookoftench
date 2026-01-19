from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


# TODO more tightly couple EventType and Event - not good that there could be multiple events with the same type (can lead to innacurate counts if not careful)

class EventType(Enum):
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    BOUNTY_COLLECTED = "bounty_collected"
    BUY_ITEM = "buy_item"
    BUY_PERK = "buy_perk"
    BUY_WEAPON = "buy_weapon"
    COFFEE_EVENT = "coffee_event"
    COFFEE_SAFE = "coffee_safe"
    COFFEE_SICK = "coffee_sick"
    CRIT = "crit"
    DEPOSIT = "deposit"
    FAILED_FLEE = "failed_flee"
    FLEE = "flee"
    HIT = "hit"
    KILL = "kill"
    LEVEL_UP = "level_up"
    MISS = "miss"
    OFFICER_PAID = "officer_paid"
    OFFICER_UNPAID = "officer_unpaid"
    PLAYER_DEATH = "player_death"
    SELL_ITEM = "sell_item"
    SELL_WEAPON = "sell_weapon"
    SWAP_WEAPON = "swap_weapon"
    TRAVEL = "travel"
    TREATMENT_EVENT = "treatment_event"
    TREATMENT_FAIL = "treatment_fail"
    TREATMENT_SUCCESS = "treatment_success"
    USE_ITEM = "use_item"
    WEAPON_BROKE = "weapon_broke"
    WITHDRAW = "withdraw"


@dataclass
class Event:
    type: EventType
    callback: Callable[[], None] = field(default_factory=lambda: None)

    def __post_init__(self):
        if not self.callback:
            self.callback = lambda: None

    def __hash__(self):
        return hash(self.type)


class Listener(ABC):
    @staticmethod
    @abstractmethod
    def handle_event(event: Event) -> None:
        pass
