from enum import Enum

# Constants
AP_TENCH_STUDIES = "AP Tench Studies"
AMBROSE_BLADE = "Ambrose Blade"
BARTER_SAUCE = "Barter Sauce"
BEER_GOGGLES = "Beer Goggles"
BROWN_FRIDAY = "Brown Friday"
BROWNMAIL = "Brownmail"
BULLETPROOF = "Bulletproof"
CATFISH_BURGLAR = "Catfish Burglar"
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
NEW_SNEAKERS = "New Sneakers"
NOMADS_LAND = "Nomad's Land"
RICKETY_PICKPOCKET = "Rickety Pickpocket"
ROSETTI_THE_GYM_RAT = "Rosetti the Gym Rat"
SHERLOCK_TENCH = "Sherlock Tench"
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
        'cost': 222,
        'description': "+20% XP from battles and +1 XP from all other sources",
        'wrappers': [
            {'wrapper_type': WrapperType.INT_CHANGE_BY_PERCENT, 'wrapper_config': {'change': 20}},
            {'wrapper_type': WrapperType.INT_CHANGE, 'wrapper_config': {'change': 1}}
        ]

    },
    {
        'name': KARATE_LESSONS,
        'cost': 55,
        'description': "Bare Hands +2 damage",
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 2}
    },
    {
        'name': BEER_GOGGLES,
        'cost': 99,
        'description': "Prevents blindness",
        'wrapper_type': WrapperType.BOOLEAN_OVERRIDE,
        'wrapper_config': {'override': False}
    },
    {
        'name': BROWN_FRIDAY,
        'cost': 123,
        'description': "Shop inventories contain +1 listing",
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 1}
    },
    {
        'name': SLEDGE_FUND,
        'cost': 160,
        'description': "Bank interest rate +8%",
        'wrapper_type': WrapperType.PERCENT_CHANGE,
        'wrapper_config': {'change': 8}
    },
    {
        'name': LUCKY_TENCHS_FIN,
        'cost': 111,
        'description': "Crit chance +5%",
        'wrapper_type': WrapperType.PERCENT_CHANGE,
        'wrapper_config': {'change': 5}
    },
    {
        'name': DOCTOR_FISH,
        'cost': 120,
        'description': "Healing items restore +2 additional HP",
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 2}
    },
    {
        'name': VAGABONDAGE,
        'cost': 130,
        'description': "Carry +1 weapon and item",
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 1}
    },
    {
        'name': NOMADS_LAND,
        'cost': 130,
        'description': "Carry +1 weapon and item",
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 1}
    },
    {
        'name': RICKETY_PICKPOCKET,
        'cost': 120,
        'description': "Steal an extra 10-25 coins from every enemy you defeat",
        'wrapper_type': WrapperType.BOUNDED_RANDOM,
        'wrapper_config': {'lower_bound': 10, 'upper_bound': 25}
    },
    {
        'name': CATFISH_BURGLAR,
        'cost': 100,
        'description': "Boost shoplifting odds by 10%",
        'wrapper_type': WrapperType.INT_CHANGE,
        'wrapper_config': {'change': 10}
    },
    {
        'name': MARTIAL_ARTS_TRAINING,
        'cost': 85,
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
        'cost': 165,
        'description': "Take 10% less damage from attacks",
        'wrapper_type': WrapperType.PERCENT_CHANGE,
        'wrapper_config': {'change': -10}
    },
    {
        'name': HEALTH_NUT,
        'cost': 110,
        'description': "Gain +10% health from items",
        'wrapper_type': WrapperType.INT_CHANGE_BY_PERCENT,
        'wrapper_config': {'change': 10}
    },
    {
        'name': INTRO_TO_TENCH,
        'cost': 135,
        'description': "+10% XP gained from winning battles",
        'wrapper_type': WrapperType.INT_CHANGE_BY_PERCENT,
        'wrapper_config': {'change': 10}
    },
    {
        'name': ROSETTI_THE_GYM_RAT,
        'cost': 145,
        'description': "Melee weapons do +8% damage",
        'wrapper_type': WrapperType.PERCENT_CHANGE,
        'wrapper_config': {'change': 8}
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
        'cost': 99,
        'description': "Flee chance +10%",
        'wrapper_type': WrapperType.PERCENT_CHANGE,
        'wrapper_config': {'change': 10}
    },
    {
        'name': BULLETPROOF,
        'cost': 140,
        'description': "Take 10% less damage from guns",
        'wrapper_type': WrapperType.PERCENT_CHANGE,
        'wrapper_config': {'change': -10}
    },
    {
        'name': WALLET_CHAIN,
        'cost': 100,
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
        'name': SHERLOCK_TENCH,
        'cost': 120,
        'description': "+10% chance to find the wanted enemy when searching their area",
    },
    {
        'name': TENCH_THE_BOUNTY_HUNTER,
        'cost': 100,
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
        'cost': 180,
        'description': "Once per battle, a fatal blow leaves you at 1 HP",
    },
    {
        'name': BARTER_SAUCE,
        'cost': 100,
        'description': "Shop prices are 5% lower",
        'wrapper_type': WrapperType.INT_CHANGE_BY_PERCENT,
        'wrapper_config': {'change': -5}
    },
    {
        'name': TRADE_SHIP,
        'cost': 165,
        'description': "Shop prices are 10% lower",
        'wrapper_type': WrapperType.INT_CHANGE_BY_PERCENT,
        'wrapper_config': {'change': -10}
    },
    {
        'name': CROWS_NEST,
        'cost': 200,
        'description': "View enemies remaining in each area",
    },
    {
        'name': SOLOMON_TRAIN,
        'cost': 250,
        'description': "10% chance to negate a fatal blow and instantly kill the enemy instead",
    },
    {
        'name': WENCH_LOCATION,
        'cost': 500,
        'description': "Reveal the wench's location",
    },
]
