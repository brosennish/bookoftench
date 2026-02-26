from enum import Enum

from bookoftench.event_base import EventType

ALWAYS_SOMETHING = "Always Something"
CHICKEN = "Chicken"
DRY_FIVE = "Dry Five"
FIRST_BUST = "First Bust"
GOLDEN_TENCH = "Golden Tench"
KARMIC_DECEIVER = "Karmic Deceiver"
KELPTOMANIAC = "Kelptomaniac"
KRILL_OR_BE_KRILLED = "Krill Or Be Krilled"
LEGENDARY = "Legendary"
LEVEL_TENCH = "Level Tench"
MASTER_OF_TENCH = "Master of Tench"
MYTHIC = "Mythic"
PATIENT_68 = "Patient 68"
RECKLESS = "Reckless"
TENCH_BUNDY = "Tench Bundy"
TENCH_KILLS = "Tench Kills"
VIGILANTE = "Vigilante"


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
        'id': TENCH_BUNDY,
        'name': "Tench Bundy",
        'description': "Defeat 25 enemies",
        'reward_type': RewardType.XP,
        'reward_value': 50,
        'event_type': EventType.KILL,
        'event_threshold': 25
    },
    {
        'id': RECKLESS,
        'name': "Reckless",
        'description': "Drink 10 coffee items",
        'reward_type': RewardType.XP,
        'reward_value': 25,
        'event_type': EventType.COFFEE_EVENT,
        'event_threshold': 10
    },
    {
        'id': DRY_FIVE,
        'name': "Dry Five",
        'description': "Reach level 5",
        'reward_type': RewardType.PERK,
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
        'id': MASTER_OF_TENCH,
        'name': "Master of Tench",
        'description': "Reach level 15",
        'reward_type': RewardType.PERK,
        'event_type': EventType.LEVEL_UP,
        'event_threshold': 15
    },
    {
        'id': GOLDEN_TENCH,
        'name': "Golden Tench",
        'description': "Reach level 20",
        'reward_type': RewardType.PERK,
        'event_type': EventType.LEVEL_UP,
        'event_threshold': 20
    },
    {
        'id': CHICKEN,
        'name': "Chicken",
        'description': "Flee 10 times",
        'reward_type': RewardType.XP,
        'reward_value': 15,
        'event_type': EventType.FLEE,
        'event_threshold': 10
    },
    {
        'id': FIRST_BUST,
        'name': "First Bust",
        'description': "Collect 1 bounty",
        'reward_type': RewardType.XP,
        'reward_value': 10,
        'event_type': EventType.BOUNTY_COLLECTED,
        'event_threshold': 1
    },
    {
        'id': VIGILANTE,
        'name': "Vigilante",
        'description': "Collect 5 bounties",
        'reward_type': RewardType.XP,
        'reward_value': 30,
        'event_type': EventType.BOUNTY_COLLECTED,
        'event_threshold': 5
    },
    {
        'id': PATIENT_68,
        'name': "Patient 68",
        'description': "Receive first treatment",
        'reward_type': RewardType.XP,
        'reward_value': 10,
        'event_type': EventType.TREATMENT_EVENT,
        'event_threshold': 1
    },
    {
        'id': ALWAYS_SOMETHING,
        'name': "Always Something",
        'description': "Receive treatment 3 times",
        'reward_type': RewardType.XP,
        'reward_value': 20,
        'event_type': EventType.TREATMENT_EVENT,
        'event_threshold': 3
    },
    {
        'id': KARMIC_DECEIVER,
        'name': "Karmic Deceiver",
        'description': "Shoplift 1 time",
        'reward_type': RewardType.XP,
        'reward_value': 10,
        'event_type': EventType.STEAL,
        'event_threshold': 1
    },
    {
        'id': KELPTOMANIAC,
        'name': "Kelptomaniac",
        'description': "Shoplift 5 times",
        'reward_type': RewardType.XP,
        'reward_value': 20,
        'event_type': EventType.STEAL,
        'event_threshold': 5
    },
    {
        'id': LEGENDARY,
        'name': "Legendary",
        'description': "Make a legendary discovery",
        'reward_type': RewardType.XP,
        'reward_value': 10,
        'event_type': EventType.DISCOVERY_LEGENDARY,
        'event_threshold': 1
    },
    {
        'id': MYTHIC,
        'name': "Mythic",
        'description': "Make a mythical discovery",
        'reward_type': RewardType.XP,
        'reward_value': 20,
        'event_type': EventType.DISCOVERY_MYTHIC,
        'event_threshold': 1
    },
]
