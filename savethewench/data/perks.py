from enum import Enum

# Constants
AP_TENCH_STUDIES = "AP Tench Studies"
AMBROSE_BLADE = "Ambrose Blade"
BARTER_SAUCE = "Barter Sauce"
BEER_GOGGLES = "Beer Goggles"
BROWN_FRIDAY = "Brown Friday"
BROWNMAIL = "Brownmail"
BULLETPROOF = "Bulletproof"
CROWS_NEST = "Crow's Nest"
DEATH_CAN_WAIT = "Death Can Wait"
DOCTOR_FISH = "Doctor Fish"
GRAMBLIN_MAN = "Gramblin' Man"
GRAMBLING_ADDICT = "Grambling Addict"
HEALTH_NUT = "Health Nut"
INTRO_TO_TENCH = "Intro to Tench"
KARATE_LESSONS = "Karate Lessons"
LEATHER_SKIN = "Leather Skin"
LUCKY_TENCHS_FIN = "Lucky Tench's Fin"
MARTIAL_ARTS_TRAINING = "Martial Arts Training"
METAL_DETECTIVE = "Metal Detective"
NEW_SNEAKERS = "New Sneakers"
NOMADS_LAND = "Nomad's Land"
RICKETY_PICKPOCKET = "Rickety Pickpocket"
ROSETTI_THE_GYM_RAT = "Rosetti the Gym Rat"
SLEDGE_FUND = "Sledge Fund"
SOLOMON_TRAIN = "Solomon Train"
TENCH_EYES = "Tench Eyes"
TENCH_GENES = "Tench Genes"
TENCH_THE_BOUNTY_HUNTER = "Tench the Bounty Hunter"
TRADE_SHIP = "Trade Ship"
USED_SNEAKERS = "Used Sneakers"
VAGABONDAGE = "Vagabondage"
VAMPIRIC_SPERM = "Vampiric Sperm"
WALLET_CHAIN = "Wallet Chain"
WENCH_LOCATION = "Wench Location"


class WrapperType(Enum):
    BOOLEAN_OVERRIDE = 0
    BOUNDED_RANDOM = 1
    INT_CHANGE = 2
    PERCENT_CHANGE = 3
    INT_CHANGE_BY_PERCENT = 4
    FLOAT_CHANGE_BY_PERCENT = 5
    NONE = 6


class WrapperIndices:
    class ApTenchStudies:
        BATTLE_XP: int = 0
        OTHER_XP: int = 1

    class GramblingAddict:
        PLAYS: int = 0
        PAYOUT: int = 1

    class TenchGenes:
        RISK: int = 0
        SURVIVAL: int = 1


Perks = [
    {
        'name': AP_TENCH_STUDIES,
        'cost': 260,
        'description': "+30% XP from battles and +1 XP from all other sources",
        'wrappers': [
            {'wrapper_type': WrapperType.INT_CHANGE_BY_PERCENT, 'wrapper_config': {'change': 30}},
            {'wrapper_type': WrapperType.INT_CHANGE, 'wrapper_config': {'change': 1}}
        ]

    },
    {
        'name': KARATE_LESSONS,
        'cost': 50,
        'description': "Bare Hands +2 damage",
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 2}
    },
    {
        'name': BEER_GOGGLES,
        'cost': 85,
        'description': "Prevents blindness",
        'wrapper_type': WrapperType.BOOLEAN_OVERRIDE,
        'wrapper_config': {'override': False}
    },
    {
        'name': BROWN_FRIDAY,
        'cost': 120,
        'description': "Shop inventories contain +1 listing",
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 1}
    },
    {
        'name': SLEDGE_FUND,
        'cost': 160,
        'description': "Bank interest rate +5%",
        'wrapper_type': WrapperType.PERCENT_CHANGE,
        'wrapper_config': {'change': 5}
    },
    {
        'name': LUCKY_TENCHS_FIN,
        'cost': 80,
        'description': "Crit chance +5%",
        'wrapper_type': WrapperType.PERCENT_CHANGE,
        'wrapper_config': {'change': 5}
    },
    {
        'name': DOCTOR_FISH,
        'cost': 110,
        'description': "Healing items restore +2 additional HP",
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 2}
    },
    {
        'name': VAGABONDAGE,
        'cost': 100,
        'description': "Carry +1 weapon and item",
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 1}
    },
    {
        'name': NOMADS_LAND,
        'cost': 100,
        'description': "Carry +1 weapon and item",
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 1}
    },
    {
        'name': RICKETY_PICKPOCKET,
        'cost': 130,
        'description': "Steal an extra 20–30 coins from every enemy you defeat",
        'wrapper_type': WrapperType.BOUNDED_RANDOM,
        'wrapper_config': {'lower_bound': 20, 'upper_bound': 30}
    },
    {
        'name': MARTIAL_ARTS_TRAINING,
        'cost': 100,
        'description': "Bare Hands +3 damage",
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 3}
    },
    {
        'name': USED_SNEAKERS,
        'cost': 40,
        'description': "Flee chance +5%",
        'wrapper_type': WrapperType.PERCENT_CHANGE,
        'wrapper_config': {'change': 5}
    },
    {
        'name': LEATHER_SKIN,
        'cost': 160,
        'description': "Take 10% less damage from attacks",
        'wrapper_type': WrapperType.PERCENT_CHANGE,
        'wrapper_config': {'change': -10}
    },
    {
        'name': HEALTH_NUT,
        'cost': 150,
        'description': "Gain +25% health from items",
        'wrapper_type': WrapperType.PERCENT_CHANGE,
        'wrapper_config': {'change': 25}
    },
    {
        'name': INTRO_TO_TENCH,
        'cost': 140,
        'description': "+15% XP gained from winning battles",
        'wrapper_type': WrapperType.INT_CHANGE_BY_PERCENT,
        'wrapper_config': {'change': 15}
    },
    {
        'name': ROSETTI_THE_GYM_RAT,
        'cost': 140,
        'description': "Melee weapons do +10% damage",
        'wrapper_type': WrapperType.PERCENT_CHANGE,
        'wrapper_config': {'change': 10}
    },
    {
        'name': AMBROSE_BLADE,
        'cost': 130,
        'description': "Bladed weapons do +3 damage",
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 3}
    },
    {
        'name': BROWNMAIL,
        'cost': 120,
        'description': "Gets Officer Hohkken off your back",
        'wrapper_type': WrapperType.BOOLEAN_OVERRIDE,
        'wrapper_config': {'override': False}
    },
    {
        'name': NEW_SNEAKERS,
        'cost': 90,
        'description': "Flee chance +10%",
        'wrapper_type': WrapperType.PERCENT_CHANGE,
        'wrapper_config': {'change': 10}
    },
    {
        'name': BULLETPROOF,
        'cost': 130,
        'description': "Take 10% less damage from guns",
        'wrapper_type': WrapperType.PERCENT_CHANGE,
        'wrapper_config': {'change': -10}
    },
    {
        'name': WALLET_CHAIN,
        'cost': 90,
        'description': 'Save 25% of your coins upon death',
    },
    {
        'name': GRAMBLIN_MAN,
        'cost': 100,
        'description': 'Enjoy +5 plays at the casino',
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 5}
    },
    {
        'name': GRAMBLING_ADDICT,
        'cost': 160,
        'description': 'Enjoy +5 plays and +5% payout at the casino',
        'wrappers': [
            {'wrapper_type': WrapperType.INT_CHANGE, 'wrapper_config': {'change': 5}},
            {'wrapper_type': WrapperType.INT_CHANGE_BY_PERCENT, 'wrapper_config': {'change': 5}}
        ]

    },
    {
        'name': VAMPIRIC_SPERM,
        'cost': 200,
        'description': 'Heal 3 HP each time you land a melee attack',
    },
    {
        'name': METAL_DETECTIVE,
        'cost': 110,
        'description': "Find up to 20 extra coins when exploring",
        'wrapper_type': WrapperType.BOUNDED_RANDOM,
        'wrapper_config': {'lower_bound': 0, 'upper_bound': 20}
    },
    {
        'name': TENCH_THE_BOUNTY_HUNTER,
        'cost': 120,
        'description': "Earn +25 coins from each bounty enemy",
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 25}
    },
    {
        'name': TENCH_EYES,
        'cost': 130,
        'description': "Projectile weapon accuracy +5%",
        'wrapper_type': WrapperType.FLOAT_CHANGE_BY_PERCENT,
        'wrapper_config': {'change': 5}
    },
    {
        'name': TENCH_GENES,
        'cost': 130,
        'description': "Illness risk -2% and survival chance +10%",
        'wrappers': [
            {'wrapper_type': WrapperType.PERCENT_CHANGE, 'wrapper_config': {'change': -2}},
            {'wrapper_type': WrapperType.PERCENT_CHANGE, 'wrapper_config': {'change': 10}}
        ]
    },
    {
        'name': DEATH_CAN_WAIT,
        'cost': 150,
        'description': "Once per battle, a fatal blow leaves you at 1 HP",
    },
    {
        'name': BARTER_SAUCE,
        'cost': 140,
        'description': "Shop prices are 10% lower",
        'wrapper_type': WrapperType.INT_CHANGE_BY_PERCENT,
        'wrapper_config': {'change': -10}
    },
    {
        'name': TRADE_SHIP,
        'cost': 300,
        'description': "Shop prices are 20% lower",
        'wrapper_type': WrapperType.INT_CHANGE_BY_PERCENT,
        'wrapper_config': {'change': -20}
    },
    {
        'name': CROWS_NEST,
        'cost': 200,
        'description': "View enemies remaining in each area",
    },
    {
        'name': SOLOMON_TRAIN,
        'cost': 300,
        'description': "10% chance to negate a fatal blow and instantly kill the enemy instead",
    },
    {
        'name': WENCH_LOCATION,
        'cost': 400,
        'description': "Reveal the wench's location",
    },
]
