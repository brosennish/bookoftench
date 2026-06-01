from bookoftench.data.illnesses import MAD_TENCH_DISEASE, INWARD_HAIR_GROWTH_DISORDER, HERPES, RESTLESS_BUTT_SYNDROME
from bookoftench.data import items as i
from bookoftench.data import perks as p
from bookoftench.data import weapons as w

# Constants (9)
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

Builds = [
    {'name': DENNY, 'lives': 2, 'hp': 100, 'str': 1, 'acc': 1, 'coins': 25,
     'items': [i.TENCH_FILET],
     'weapons': [w.BARE_HANDS, w.KNIFE],
     'perks': [],
     'illness': None,
     'notes': 'Denny, Jeffrey, Jasper. Son of Mayor - The Chosen Spawn.'},

    {'name': CAT_BURGLAR, 'lives': 9, 'hp': 69, 'str': 0.69, 'acc': 0.69, 'coins': 69,
     'items': [i.SMOKE_BOMB],
     'weapons': [w.BARE_HANDS, w.CROWBAR],
     'perks': [p.CATFISH_BURGLAR, p.RICKETY_PICKPOCKET],
     'illness': None,
     'notes': "Steals more than just cats."},

    {'name': COWARD, 'lives': 2, 'hp': 90, 'str': 0.9, 'acc': 0.9, 'coins': 10,
     'items': [i.IOU, i.SMOKE_BOMB, i.WORMHOLE],
     'weapons': [w.BARE_HANDS],
     'perks': [p.USED_SNEAKERS, p.NEW_SNEAKERS],
     'illness': None,
     'notes': "Would rather run than fight... like a little bozo baby coward."},

    {'name': CYBORG, 'lives': 1, 'hp': 110, 'str': 1.1, 'acc': 1.10, 'coins': 0,
     'items': [i.WORMHOLE],
     'weapons': [w.LASER_BEAMS],
     'perks': [p.LEATHER_SKIN, p.BEER_GOGGLES],
     'illness': None,
     'notes': "Moral deficiencies of man, physical capacities of robot. What could go wrong?"},

    {'name': DOG_MAN, 'lives': 2, 'hp': 110, 'str': 1.1, 'acc': 0.75, 'coins': 0,
     'items': [i.MYSTERY_MEAT],
     'weapons': [w.CLAWS, w.TEETH],
     'perks': [],
     'illness': INWARD_HAIR_GROWTH_DISORDER,
     'notes': "Half man - half dog. The wife won't say which half she likes better."},

    {'name': MAKE_A_FISH, 'lives': 1, 'hp': 80, 'str': 0.8, 'acc': 0.9, 'coins': 500,
     'items': [i.OCEAN_MAN_LUNCH_BOX, i.EAGLE_EGG, i.FERMENTED_CELERY_MILK],
     'weapons': [w.BARE_HANDS, w.INJECTION_NEEDLE, w.HARDCOVER_BOOK],
     'perks': [p.BROWNMAIL, p.NEW_SNEAKERS, p.DEATH_CAN_WAIT, p.SOLOMON_TRAIN],
     'illness': MAD_TENCH_DISEASE,
    'notes': 'Terminally ill and foundationally sponsored.'},

    {'name': MERCENARY, 'lives': 2, 'hp': 110, 'str': 1.05, 'acc': 1.05, 'coins': 20,
     'items': [i.CANNED_HORSE],
     'weapons': [w.BARE_HANDS, w.KNIFE, w.REVOLVER],
     'perks': [p.TENCH_THE_BOUNTY_HUNTER, p.SHERLOCK_TENCH],
     'illness': None,
     'notes': 'Enjoys collecting bounties... but mostly killing.'},

    {'name': SHOPAHOLIC, 'lives': 2, 'hp': 100, 'str': 0.95, 'acc': 0.95, 'coins': 300,
     'items': [i.IOU],
     'weapons': [w.BARE_HANDS, w.PEPPER_SPRAY, w.KNIFE],
     'perks': [p.BROWN_FRIDAY, p.BARTER_SAUCE, p.TRADE_SHIP],
     'illness': HERPES,
     'notes': "Wears a shirt that says I'd rather be at the Shebokken Mall."},

    {'name': TENCH, 'lives': 2, 'hp': 110, 'str': 1.10, 'acc': 0.75, 'coins': 0,
     'items': [i.KRILL, i.CRAY],
     'weapons': [w.BARE_HANDS, w.TENCH_CANNON],
     'perks': [p.TENCH_EYES, p.TENCH_GENES, p.LUCKY_TENCHS_FIN, p.DOCTOR_FISH],
     'illness': None,
     'notes': "Half man - half tench. Can you imagine a more ideal being?"},

    {'name': BRO, 'lives': 100, 'hp': 1000, 'str': 150, 'acc': 150, 'coins': 5000,
     'items': [i.IOU, i.SMOKE_BOMB, i.WORMHOLE],
     'weapons': [w.BARE_HANDS, w.SLEDGEHAMMER, w.RIFLE, w.TENCH_CANNON],
     'perks': [],
     'illness': RESTLESS_BUTT_SYNDROME,
     'notes': "Bro... really bro?"},

    {'name': RANDOM, 'lives': 0, 'hp': 0, 'str': 0, 'acc': 0, 'coins': 0,
     'items': [],
     'weapons': [],
     'perks': [],
     'illness': None,
     'notes': 'Randomization at its finest.'},
]