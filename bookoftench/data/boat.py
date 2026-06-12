from bookoftench.ui import blue, green, cyan, purple, red, yellow, white

# ================================================================================================

ALL_NEW_ONLY = 'All/New Only'
CAST = "Cast"
FISHING_LOG = "Fishing Log"
SHOP = "Shop"
TACKLE_BOX = "Tackle Box"

FISHING_OPTIONS = [
    {'name': CAST, 'color': cyan},
    {'name': TACKLE_BOX, 'color': purple},
    {'name': FISHING_LOG, 'color': blue},
    {'name': ALL_NEW_ONLY, 'color': green},
]

# ================================================================================================

PULL = "Pull"
REEL = "Reel"
GIVE_LINE = "Give Line"
OBSERVE = "Observe"
USE_ITEM = "Use Item"

FISHING_BATTLE_OPTIONS = [
    {'name': PULL, 'color': red},
    {'name': REEL, 'color': blue},
    {'name': GIVE_LINE, 'color': yellow},
    {'name': OBSERVE, 'color': purple},
    {'name': USE_ITEM, 'color': cyan},
]
