import random
from functools import partial
from typing import Callable

from savethewench.ui import purple
from savethewench.util import print_and_sleep

# Constants
AP_TENCH_STUDIES = "AP Tench Studies"
AMBROSE_BLADE = "Ambrose Blade"
BARTER_SAUCE = "Barter Sauce"
BEER_GOGGLES = "Beer Goggles"
BROWN_FRIDAY = "Brown Friday"
BULLETPROOF = "Bulletproof"
CROWS_NEST = "Crow's Nest"
DEATH_CAN_WAIT = "Death Can Wait"
DOCTOR_FISH = "Doctor Fish"
GRAMBLIN_MAN = "Gramblin' Man"
GRAMBLING_ADDICT = "Grambling Addict"
HEALTH_NUT = "Health Nut"
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
TENCH_THE_BOUNTY_HUNTER = "Tench the Bounty Hunter"
TRADE_SHIP = "Trade Ship"
USED_SNEAKERS = "Used Sneakers"
VAGABONDAGE = "Vagabondage"
VAMPIRIC_SPERM = "Vampiric Sperm"
WALLET_CHAIN = "Wallet Chain"
WENCH_LOCATION = "Wench Location"


def _numeric_change(original: int | float, value_description: str, silent: bool, change: int | float, name: str,
                    change_func: Callable[[int | float, int | float], int | float]) -> int | float:
    if not silent:
        if len(value_description) == 0:
            print_and_sleep(f"Applied perk: {name}", 1)
        else:
            inc_or_dec = "increased" if change >= 0 else "decreased"
            print_and_sleep(purple(f"{name} {inc_or_dec} {value_description} by {abs(change)}%"), 1)
    return change_func(original, change)


def _bounded_random_change(original: int, value_description: str, silent: bool, lower: int, upper: int,
                           name: str) -> int:
    val = random.randint(lower, upper)
    if not silent:
        if len(value_description) == 0:
            print_and_sleep(f"Applied perk: {name}", 1)
        else:
            print_and_sleep(purple(f"{name} increased {original} {value_description} to {original + val}"), 1)
    return original + val


_int_change: Callable[[int, int], int] = lambda orig, i: orig + i
_percent_change: Callable[[float, int], float] = lambda orig, pct: orig + (float(pct) / 100.0)

Perks = [
    {
        'name': KARATE_LESSONS,
        'cost': 50,
        'description': "Bare Hands +2 damage",
    },
    {
        'name': BEER_GOGGLES,
        'cost': 85,
        'description': "Prevents blindness",
    },
    {
        'name': BROWN_FRIDAY,
        'cost': 120,
        'description': "Shop inventories contain +1 listing",
    },
    {
        'name': SLEDGE_FUND,
        'cost': 160,
        'description': "Bank interest rate +5%",
        'wrapper': partial(_numeric_change, change=5, name=SLEDGE_FUND, change_func=_percent_change),
    },
    {
        'name': LUCKY_TENCHS_FIN,
        'cost': 80,
        'description': "Crit chance +5%",
        'wrapper': partial(_numeric_change, change=5, name=LUCKY_TENCHS_FIN, change_func=_percent_change),
    },
    {
        'name': DOCTOR_FISH,
        'cost': 110,
        'description': "Healing items restore +2 additional HP",
    },
    {
        'name': VAGABONDAGE,
        'cost': 100,
        'description': "Carry +1 weapon and item",
        'wrapper': partial(_numeric_change, change=1, name=VAGABONDAGE, change_func=_int_change)
    },
    {
        'name': NOMADS_LAND,
        'cost': 100,
        'description': "Carry +1 weapon and item",
        'wrapper': partial(_numeric_change, change=1, name=NOMADS_LAND, change_func=_int_change)
    },
    {
        'name': RICKETY_PICKPOCKET,
        'cost': 130,
        'description': "Steal an extra 20–30 coins from every enemy you defeat",
    },
    {
        'name': MARTIAL_ARTS_TRAINING,
        'cost': 100,
        'description': "Bare Hands +3 damage",
    },
    {
        'name': USED_SNEAKERS,
        'cost': 40,
        'description': "Flee chance +5%",
        'wrapper': partial(_numeric_change, change=5, name=USED_SNEAKERS, change_func=_percent_change),
    },
    {
        'name': LEATHER_SKIN,
        'cost': 160,
        'description': "Take 10% less damage from attacks",
        'wrapper': partial(_numeric_change, change=-10, name=LEATHER_SKIN, change_func=_percent_change),
    },
    {
        'name': HEALTH_NUT,
        'cost': 150,
        'description': "Gain +25% health from items",
    },
    {
        'name': ROSETTI_THE_GYM_RAT,
        'cost': 140,
        'description': "Melee weapons do +10% damage",
    },
    {
        'name': AMBROSE_BLADE,
        'cost': 130,
        'description': "Melee weapons do +3 damage",
    },
    {
        'name': NEW_SNEAKERS,
        'cost': 90,
        'description': "Flee chance +10%",
        'wrapper': partial(_numeric_change, change=10, name=NEW_SNEAKERS, change_func=_percent_change),
    },
    {
        'name': BULLETPROOF,
        'cost': 130,
        'description': "Take 10% less damage from guns",
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
        'wrapper': partial(_numeric_change, change=5, name=GRAMBLIN_MAN, change_func=_int_change),
    },
    {
        'name': GRAMBLING_ADDICT,
        'cost': 160,
        'description': 'Enjoy +5 plays and +5% payout at the casino',
        # note - this only works for plays
        'wrapper': partial(_numeric_change, change=5, name=GRAMBLIN_MAN, change_func=_int_change),
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
        'wrapper': partial(_bounded_random_change, lower=0, upper=20, name=METAL_DETECTIVE),
    },
    {
        'name': TENCH_THE_BOUNTY_HUNTER,
        'cost': 120,
        'description': "Earn +25 coins from each bounty enemy",
    },
    {
        'name': TENCH_EYES,
        'cost': 130,
        'description': "Projectile weapon accuracy +5%",
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
        'wrapper': partial(_numeric_change, change=-10, name=BARTER_SAUCE, change_func=_percent_change)
    },
    {
        'name': TRADE_SHIP,
        'cost': 300,
        'description': "Shop prices are 20% lower",
        'wrapper': partial(_numeric_change, change=-20, name=TRADE_SHIP, change_func=_percent_change),
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
