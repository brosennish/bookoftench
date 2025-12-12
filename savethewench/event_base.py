from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


# TODO more tightly couple EventType and Event - not good that there could be multiple events with the same type (can lead to innacurate counts if not careful)

class EventType(Enum):
    BOUNTY_COLLECTED = "bounty_collected"
    BUY_ITEM = "buy_item"
    BUY_PERK = "buy_perk"
    BUY_WEAPON = "buy_weapon"
    CRIT = "crit"
    DEPOSIT = "deposit"
    FLEE = "flee"
    HIT = "hit"
    KILL = "kill"
    LEVEL_UP = "level_up"
    MISS = "miss"
    SELL_ITEM = "sell_item"
    SELL_WEAPON = "sell_weapon"
    SWAP_WEAPON = "swap_weapon"
    TRAVEL = "travel"
    USE_ITEM = "use_item"
    WEAPON_BROKE = "weapon_broke"
    WITHDRAW = "withdraw"


@dataclass
class Event:
    type: EventType

    def __hash__(self):
        return hash(self.type)


class Listener(ABC):
    @staticmethod
    @abstractmethod
    def handle_event(event: Event) -> None:
        pass
