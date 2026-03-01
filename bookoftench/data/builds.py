from bookoftench.data.illnesses import MAD_TENCH_DISEASE
from bookoftench.data.items import TENCH_FILET, IOU, SMOKE_BOMB, WORMHOLE, CRAY, KRILL, CANNED_HORSE, \
    OCEAN_MAN_LUNCH_BOX, EAGLE_EGG
from bookoftench.data.perks import USED_SNEAKERS, NEW_SNEAKERS, TENCH_EYES, TENCH_GENES, BARTER_SAUCE, TRADE_SHIP, \
    BROWN_FRIDAY, LUCKY_TENCHS_FIN, DOCTOR_FISH, TENCH_THE_BOUNTY_HUNTER, SHERLOCK_TENCH, CATFISH_BURGLAR, \
    RICKETY_PICKPOCKET, BROWNMAIL, DEATH_CAN_WAIT, SOLOMON_TRAIN
from bookoftench.data.weapons import BARE_HANDS, KNIFE, REVOLVER, CROWBAR, TENCH_CANNON, POCKET_KNIFE, HARDCOVER_BOOK

# Constants
CAT_BURGLAR = "Cat Burglar"
COWARD = "Coward"
DENNY = "Denny"
MAKE_A_FISH = "Make a Fish"
MERCENARY = "Mercenary"
SHOPAHOLIC = "Shopaholic"
TENCH = "Tench"

Builds = [
    {'name': CAT_BURGLAR, 'hp': 100, 'str': 1, 'acc': 1, 'coins': 0,
     'items': [SMOKE_BOMB],
     'weapons': [BARE_HANDS, CROWBAR],
     'perks': [CATFISH_BURGLAR, RICKETY_PICKPOCKET],
     'illness': None,
     'notes': "Steals more than just cats."},
    {'name': COWARD, 'hp': 90, 'str': 0.9, 'acc': 0.9, 'coins': 10,
     'items': [IOU, SMOKE_BOMB, WORMHOLE],
     'weapons': [BARE_HANDS],
     'perks': [USED_SNEAKERS, NEW_SNEAKERS],
     'illness': None,
     'notes': "Would rather run than fight... like a little bozo baby coward."},
    {'name': DENNY, 'hp': 100, 'str': 1, 'acc': 1, 'coins': 25,
     'items': [TENCH_FILET, IOU],
     'weapons': [BARE_HANDS, KNIFE],
     'perks': [],
     'illness': None,
     'notes': 'Denny, Jeffrey, Jasper. Son of Mayor - The Chosen Spawn.'},
    {'name': MAKE_A_FISH, 'hp': 80, 'str': 0.75, 'acc': 0.75, 'coins': 500,
     'items': [OCEAN_MAN_LUNCH_BOX, EAGLE_EGG],
     'weapons': [BARE_HANDS, POCKET_KNIFE, HARDCOVER_BOOK],
     'perks': [BROWNMAIL, NEW_SNEAKERS, DEATH_CAN_WAIT, SOLOMON_TRAIN],
     'illness': MAD_TENCH_DISEASE,
    'notes': 'Terminally ill but foundationally sponsored.'},
    {'name': MERCENARY, 'hp': 100, 'str': 1.05, 'acc': 1.05, 'coins': 20,
     'items': [CANNED_HORSE],
     'weapons': [BARE_HANDS, KNIFE, REVOLVER],
     'perks': [TENCH_THE_BOUNTY_HUNTER, SHERLOCK_TENCH],
     'illness': None,
     'notes': 'Enjoys collecting bounties... but mostly killing.'},
    {'name': SHOPAHOLIC, 'hp': 100, 'str': 0.85, 'acc': 0.85, 'coins': 100,
     'items': [IOU],
     'weapons': [BARE_HANDS],
     'perks': [BROWN_FRIDAY, BARTER_SAUCE, TRADE_SHIP],
     'illness': None,
     'notes': "Has a shirt that says I'd rather be at the Shebokken Mall."},
    {'name': TENCH, 'hp': 110, 'str': 1.1, 'acc': 0.75, 'coins': 0,
     'items': [KRILL, CRAY],
     'weapons': [BARE_HANDS, TENCH_CANNON],
     'perks': [TENCH_EYES, TENCH_GENES, LUCKY_TENCHS_FIN, DOCTOR_FISH],
     'illness': None,
     'notes': "Half man - half tench. Can you imagine a more ideal being?"},
]