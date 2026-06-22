from bookoftench.data.illnesses import MAD_TENCH_DISEASE, HERPES
from bookoftench.data import items as i
from bookoftench.data import perks as p
from bookoftench.data import weapons as w

# ================================================================================================

BRO = "Bro"
DENNY = "Denny"
RANDOM = "Random"
YOUNG_SALT = "Young Salt"
COWARD = "Coward"
LEPRECHAUN = "Leprechaun"
MERCENARY = "Mercenary"
TENCH_PERSON = "Tench Person"
MAKE_A_FISH = "Make a Fish"

# ================================================================================================
# ================================================================================================

Builds = [
    {'name': DENNY, 'label': "Standard",
     'lives': 2, 'lvl': 1, 'hp': 100, 'str': 1, 'acc': 1, 'coins': 25, 'luck': 1,
     'fishing_lvl': 1, 'rod_lvl': 1,
     'items': [i.TENCH_FILET],
     'weapons': [w.KNIFE],
     'perks': [],
     'illness': None,
     'notes': 'Denny, Jeffrey, Jasper. Son of Mayor - The Chosen Spawn.'},

# ================================================================================================

    {'name': YOUNG_SALT, 'label': "Fishermensch",
     'lives': 2, 'lvl': 1, 'hp': 100, 'str': 1, 'acc': 1, 'coins': 35, 'luck': 3,
     'fishing_lvl': 3, 'rod_lvl': 3,
     'items': [i.CRITICAL_BASS, i.OCEAN_MAN_LUNCH_BOX],
     'weapons': [w.HARPOON],
     'perks': [],
     'illness': None,
     'notes': 'Not an Old Salt - but a salt, nonetheless.'},

# ================================================================================================

    {'name': COWARD, 'label': "Survivor",
     'lives': 2, 'lvl': 1, 'hp': 90, 'str': 0.9, 'acc': 0.9, 'coins': 45, 'luck': 1,
     'fishing_lvl': 1, 'rod_lvl': 1,
     'items': [i.SMOKE_BOMB, i.WORMHOLE, i.IOU],
     'weapons': [w.PEPPER_SPRAY],
     'perks': [p.USED_SNEAKERS, p.NEW_SNEAKERS],
     'illness': None,
     'notes': "Little. Bozo. Baby. Coward."},

# ================================================================================================

    {'name': LEPRECHAUN, 'label': "Lucky Bastard",
     'lives': 2, 'lvl': 1, 'hp': 77, 'str': 0.5, 'acc': 1, 'coins': 333, 'luck': 7,
     'fishing_lvl': 1, 'rod_lvl': 1,
     'items': [i.MOON_RUNE, i.PHOTOSYNTHOPHYL],
     'weapons': [w.CANE],
     'perks': [],
     'illness': HERPES,
     'notes': "Luck of the dayng Irish."},

# ================================================================================================

    {'name': MERCENARY, 'label': "Bounty Hunter",
     'lives': 2, 'lvl': 1, 'hp': 100, 'str': 1.05, 'acc': 1.05, 'coins': 25, 'luck': 1,
     'fishing_lvl': 1, 'rod_lvl': 1,
     'items': [i.MOONSHINE, i.CANNED_HORSE],
     'weapons': [w.KNIFE, w.PISTOL],
     'perks': [p.SHERLOCK_TENCH, p.TENCH_THE_BOUNTY_HUNTER],
     'illness': None,
     'notes': "Tench justice - plain and simple."},

# ================================================================================================

    {'name': TENCH_PERSON, 'label': "Fish Person",
     'lives': 2, 'lvl': 1, 'hp': 110, 'str': 1.05, 'acc': 0.8, 'coins': 0, 'luck': 1,
     'fishing_lvl': 1, 'rod_lvl': 1,
     'items': [i.KRILL, i.CRAY],
     'weapons': [w.TENCH_CANNON],
     'perks': [p.TENCH_GENES, p.TENCH_EYES],
     'illness': None,
     'notes': "Human-tench hybridization - Satan's greatest work."},

# ================================================================================================

    {'name': MAKE_A_FISH, 'label': "Comeback Kid",
     'lives': 1, 'lvl': 1, 'hp': 80, 'str': 0.8, 'acc': 0.9, 'coins': 500, 'luck': 0,
     'fishing_lvl': 1, 'rod_lvl': 1,
     'items': [i.OCEAN_MAN_LUNCH_BOX],
     'weapons': [w.POCKET_KNIFE, w.HARDCOVER_BOOK],
     'perks': [p.DEATH_CAN_WAIT, p.SOLOMON_TRAIN, p.BROWNMAIL],
     'illness': MAD_TENCH_DISEASE,
     'notes': "Tench-fed, foundationally sponsored."},

# ================================================================================================

    {'name': RANDOM, 'label': "Randomized",
     'lives': 0, 'lvl': 0, 'hp': 0, 'str': 0, 'acc': 0, 'coins': 0, 'luck': 0,
     'fishing_lvl': 0, 'rod_lvl': 0,
     'items': [],
     'weapons': [],
     'perks': [],
     'illness': None,
     'notes': "Randomize your build."},
]