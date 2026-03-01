from bookoftench.data.items import TENCH_FILET, IOU, SMOKE_BOMB, WORMHOLE, CRAY, KRILL, CANNED_HORSE
from bookoftench.data.perks import USED_SNEAKERS, NEW_SNEAKERS, TENCH_EYES, TENCH_GENES, BARTER_SAUCE, TRADE_SHIP, \
    BROWN_FRIDAY, LUCKY_TENCHS_FIN, DOCTOR_FISH, TENCH_THE_BOUNTY_HUNTER, SHERLOCK_TENCH, CATFISH_BURGLAR, \
    RICKETY_PICKPOCKET
from bookoftench.data.weapons import BARE_HANDS, KNIFE, REVOLVER, CROWBAR, TENCH_CANNON

# Constants
CAT_BURGLAR = "Cat Burglar"
COWARD = "Coward"
DENNY = "Denny"
MERCENARY = "Mercenary"
SHOPAHOLIC = "Shopaholic"
TENCH = "Tench"

Builds = [
    {'name': CAT_BURGLAR, 'hp': 100, 'str': 1, 'acc': 1, 'coins': 0,
     'items': [SMOKE_BOMB],
     'weapons': [BARE_HANDS, CROWBAR],
     'perks': [CATFISH_BURGLAR, RICKETY_PICKPOCKET],
     'notes': None},
    {'name': COWARD, 'hp': 95, 'str': 0.9, 'acc': 1, 'coins': 10,
     'items': [IOU, SMOKE_BOMB, WORMHOLE],
     'weapons': [BARE_HANDS],
     'perks': [USED_SNEAKERS, NEW_SNEAKERS],
     'notes': None},
    {'name': DENNY, 'hp': 100, 'str': 1, 'acc': 1, 'coins': 25,
     'items': [TENCH_FILET, IOU],
     'weapons': [BARE_HANDS, KNIFE],
     'perks': [],
     'notes': None},
    {'name': MERCENARY, 'hp': 100, 'str': 1.05, 'acc': 1.05, 'coins': 20,
     'items': [CANNED_HORSE],
     'weapons': [BARE_HANDS, KNIFE, REVOLVER],
     'perks': [TENCH_THE_BOUNTY_HUNTER, SHERLOCK_TENCH],
     'notes': None},
    {'name': SHOPAHOLIC, 'hp': 85, 'str': 0.85, 'acc': 0.85, 'coins': 100,
     'items': [IOU],
     'weapons': [BARE_HANDS],
     'perks': [BROWN_FRIDAY, BARTER_SAUCE, TRADE_SHIP],
     'notes': None},
    {'name': TENCH, 'hp': 110, 'str': 1.1, 'acc': 0.75, 'coins': 0,
     'items': [KRILL, CRAY],
     'weapons': [BARE_HANDS, TENCH_CANNON],
     'perks': [TENCH_EYES, TENCH_GENES, LUCKY_TENCHS_FIN, DOCTOR_FISH],
     'notes': None},
]