from bookoftench.data.illnesses import MAD_TENCH_DISEASE, INWARD_HAIR_GROWTH_DISORDER, HERPES, RESTLESS_BUTT_SYNDROME
from bookoftench.data import items as i, Perks, Weapons, Items
from bookoftench.data import perks as p
from bookoftench.data import weapons as w

# ================================================================================================

BRO = "Bro"
CAT_BURGLAR = "Cat Burglar"
COWARD = "Coward"
CYBORG = "Cyborg"
DENNY = "Denny"
DOG_MAN = "Dog Man"
MAKE_A_FISH = "Make a Fish"
MERCENARY = "Mercenary"
RANDOM = "Random"
SHOPAHOLIC = "Shopaholic"
TENCH = "Tench"

# ================================================================================================

Builds = [
    {'name': DENNY, 'lives': 2, 'hp': 100, 'str': 1, 'acc': 1, 'coins': 25, 'luck': 0,
     'fishing_lvl': 1,
     'items': [i.TENCH_FILET],
     'weapons': [w.KNIFE],
     'perks': [],
     'illness': None,
     'notes': 'Denny, Jeffrey, Jasper. Son of Mayor - The Chosen Spawn.'},

    {'name': BRO, 'lives': 99, 'hp': 9999, 'str': 999, 'acc': 999, 'coins': 9999, 'luck': 9,
     'fishing_lvl': 99,
     'items': [b['name'] for b in Items],
     'weapons': [b['name'] for b in Weapons],
     'perks': [b['name'] for b in Perks],
     'illness': None,
     'notes': "Bro... really bro?"},

    {'name': RANDOM, 'lives': 0, 'hp': 0, 'str': 0, 'acc': 0, 'coins': 0, 'luck': 0,
     'fishing_lvl': 0,
     'items': [],
     'weapons': [],
     'perks': [],
     'illness': None,
     'notes': None},
]