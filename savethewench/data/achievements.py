from enum import Enum

from savethewench.event_base import EventType

CHICKEN = "Chicken"
DRY_FIVE = "Dry Five"
KRILL_OR_BE_KRILLED = "Krill Or Be Krilled"
LEVEL_TENCH = "Level Tench"
RECKLESS = "Reckless"
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
    {
        'id': RECKLESS,
        'name': "Reckless",
        'description': "Drink 15 coffee items",
        'reward_type': RewardType.XP,
        'reward_value': 15,
        'event_type': EventType.COFFEE_EVENT,
        'event_threshold': 15
    },
    {
        'id': DRY_FIVE,
        'name': "Dry Five",
        'description': "Reach level 5",
        'reward_type': RewardType.COIN,
        'reward_value': 55,
        'event_type': EventType.LEVEL_UP,
        'event_threshold': 5
    },
{
        'id': LEVEL_TENCH,
        'name': "Level Tench",
        'description': "Reach level 10",
        'reward_type': RewardType.PERK,
        'event_type': EventType.LEVEL_UP,
        'event_threshold': 10
    },
    {
        'id': CHICKEN,
        'name': "Chicken",
        'description': "Flee 10 times",
        'reward_type': RewardType.XP,
        'reward_value': 10,
        'event_type': EventType.FLEE,
        'event_threshold': 10
    },
]
