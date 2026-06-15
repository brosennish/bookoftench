from bookoftench.data.illnesses import MAD_TENCH_DISEASE, INWARD_HAIR_GROWTH_DISORDER, HERPES, RESTLESS_BUTT_SYNDROME
from bookoftench.data import items as i, Perks, Weapons, Items
from bookoftench.data import perks as p
from bookoftench.data import weapons as w

# ================================================================================================

BRO = "Bro"
DENNY = "Denny"
RANDOM = "Random"
YOUNG_SALT = "Young Salt"

# ================================================================================================
# ================================================================================================

Builds = [
    {'name': DENNY, 'lives': 2, 'lvl': 1, 'hp': 100, 'str': 1, 'acc': 1, 'coins': 25, 'luck': 0,
     'fishing_lvl': 1, 'rod_lvl': 1,
     'items': [i.TENCH_FILET],
     'weapons': [w.KNIFE],
     'perks': [],
     'illness': None,
     'notes': 'Denny, Jeffrey, Jasper. Son of Mayor - The Chosen Spawn.'},

# ================================================================================================

    {'name': YOUNG_SALT, 'lives': 2, 'lvl': 1, 'hp': 100, 'str': 1.03, 'acc': 0.97, 'coins': 25, 'luck': 3,
     'fishing_lvl': 3, 'rod_lvl': 3,
     'items': [i.CRITICAL_BASS, i.OCEAN_MAN_LUNCH_BOX],
     'weapons': [w.HARPOON],
     'perks': [p.TENCH_GENES, p.TENCH_EYES],
     'illness': None,
     'notes': 'While not an Old Salt - a salt, nonetheless.'},

# ================================================================================================

    {'name': BRO, 'lives': 99, 'lvl': 99, 'hp': 999, 'str': 10, 'acc': 10, 'coins': 999, 'luck': 9,
     'fishing_lvl': 99, 'rod_lvl': 99,
     'items': [b['name'] for b in Items],
     'weapons': [b['name'] for b in Weapons],
     'perks': [b['name'] for b in Perks],
     'illness': None,
     'notes': "Bro... really bro?"},

# ================================================================================================

    {'name': RANDOM, 'lives': 0, 'lvl': 0, 'hp': 0, 'str': 0, 'acc': 0, 'coins': 0, 'luck': 0,
     'fishing_lvl': 0, 'rod_lvl': 0,
     'items': [],
     'weapons': [],
     'perks': [],
     'illness': None,
     'notes': None},
]