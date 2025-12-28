from enum import Enum

from savethewench.event_base import EventType

KRILL_OR_BE_KRILLED = "Krill Or Be Krilled"
TENCH_KILLS = "Tench Kills"

class RewardType(Enum):
    XP = "xp"
    COIN = "coin"
    PERK = "perk"


Achievements = [
    {
        'id': KRILL_OR_BE_KRILLED,
        'name': "Krill or be Krilled",
        'description': "Defeat your first enemy",
        'reward_type': RewardType.XP,
        'reward_value': 10,
        'event_type': EventType.KILL,
        'event_threshold': 1
    },
    {
        'id': TENCH_KILLS,
        'name': "Tench Kills",
        'description': "Defeat 10 enemies",
        'reward_type': RewardType.PERK,
        'event_type': EventType.KILL,
        'event_threshold': 10
    },
]
