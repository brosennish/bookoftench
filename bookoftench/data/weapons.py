import bookoftench.data.audio as audio

# ================================================================================================

CAVE = "Cave"
CITY = "City"
FOREST = "Forest"
SWAMP = "Swamp"
NA = "NA" # Not applicable / can't be found or purchased

# ================================================================================================

# Names
AXE = "Axe"
BARE_HANDS = "Bare Hands"
BASEBALL_BAT = "Baseball Bat"
BEAK = "Beak"
BINOCULARS = "Binoculars"
BEAR_SPRAY = "Bear Spray"
BONE_CLUB = "Bone Club"
BONE_SAW = "Bone Saw"
BRANCH_SPEAR = "Branch Spear"
BRASS_KNUCKLES = "Brass Knuckles"
BRICK = "Brick"
BROKEN_BOTTLE = "Broken Bottle"
CANE = "Cane"
CHAINSAW = "Chainsaw"
CHILI_POWDER = "Chili Powder"
CHISEL = "Chisel"
CLAWS = "Claws"
COMPOUND_BOW = "Compound Bow"
CROSSBOW = "Crossbow"
CROWBAR = "Crowbar"
DUMBBELL = "Dumbbell"
FANGS = "Fangs"
FIRE_AXE = "Fire Axe"
FISHING_SPEAR = "Fishing Spear"
FLASHLIGHT = "Flashlight"
FLARE_GUN = "Flare Gun"
FOAM_FINGER = "Foam Finger"
FROG_GIG = "Frog Gig"
GAFF_HOOK = "Gaff Hook"
HARDCOVER_BOOK = "Hardcover Book"
HARPOON = "Harpoon"
HATCHET = "Hatchet"
HOCKEY_STICK = "Hockey Stick"
INJECTION_NEEDLE = "Injection Needle"
KATANA = "Katana"
KNIFE = "Knife"
LASER_BEAMS = "Laser Beams"
LONGBOW = "Longbow"
MACHETE = "Machete"
MAGIC_WAND = "Magic Wand"
MEAT_CLEAVER = "Meat Cleaver"
NAIL_GUN = "Nail Gun"
OBSIDIAN_KNIFE = "Obsidian Knife"
PEPPER_SPRAY = "Pepper Spray"
PICKAXE = "Pickaxe"
PILLOW = "Pillow"
PISTOL = "Pistol"
POCKET_KNIFE = "Pocket Knife"
POCKET_SAND = "Pocket Sand"
POOL_CUE = "Pool Cue"
REVOLVER = "Revolver"
RIFLE = "Rifle"
RUBBER_CHICKEN = "Rubber Chicken"
SCYTHE = "Scythe"
SELFIE_STICK = "Selfie Stick"
SHIV = "Shiv"
SHOTGUN = "Shotgun"
SHOVEL = "Shovel"
SICKLE = "Sickle"
SLEDGEHAMMER = "Sledgehammer"
SLINGSHOT = "Slingshot"
STAFF = "Staff"
STONE_SPEAR = "Stone Spear"
STUN_GUN = "Stun Gun"
SUITCASE = "Suitcase"
SURVIVAL_KNIFE = "Survival Knife"
SWITCHBLADE = "Switchblade"
TAIL = "Tail"
TEETH = "Teeth"
TENCH_CANNON = "Tench Cannon"
TENTACLES = "Tentacles"
TIRE_IRON = "Tire Iron"
TORCH_CLUB = "Torch Club"
TREKKING_POLE = "Trekking Pole"
TRIPOD = "Tripod"
TROWEL = "Trowel"
T_SHIRT_CANNON = "T-Shirt Cannon"
VOODOO_STAFF = "Voodoo Staff"
WALKING_STICK = "Walking Stick"
WOODEN_CLUB = "Wooden Club"

# ================================================================================================

# Types
BLADED = 'bladed'
BLIND = 'blind'
BLUNT = 'blunt'
MELEE = 'melee'
RANGED = 'ranged'
SPECIAL = 'special'
STUN = 'stun'

# ================================================================================================

Weapons = [
    # =====================================================
    #                       DEFAULT
    # =====================================================
    {'name': BARE_HANDS, 'type': MELEE, 'subtype': MELEE, 'tier': 1,
     'damage': 10, 'uses': -1, 'acc': 0.90, 'var': 2, 'crit': 0.08, 'stun': 0.03,
     'cost': 0, 'sell_value': 0,
     'sound': audio.PUNCH, 'areas': [CAVE, CITY, FOREST, SWAMP]},

    # =====================================================
    #                       TIER 0 (BLIND)
    # =====================================================
    {'name': PEPPER_SPRAY, 'type': BLIND, 'subtype': BLIND, 'tier': 0,
     'damage': 0, 'uses': 4, 'acc': 0.85, 'var': 0, 'crit': 0, 'stun': 0,
     'cost': 30, 'sell_value': 12,
     'blind_effect': 0.50, 'blind_turns_min': 3, 'blind_turns_max': 5,
     'sound': audio.SPRAY, 'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': BEAR_SPRAY, 'type': BLIND, 'subtype': BLIND, 'tier': 0,
     'damage': 0, 'uses': 3, 'acc': 0.85, 'var': 0, 'crit': 0, 'stun': 0,
     'cost': 60, 'sell_value': 30,
     'blind_effect': 0.65, 'blind_turns_min': 3, 'blind_turns_max': 5,
     'sound': audio.SPRAY, 'areas': [CAVE, FOREST, SWAMP]},

    {'name': CHILI_POWDER, 'type': BLIND, 'subtype': BLIND, 'tier': 0,
     'damage': 0, 'uses': 2, 'acc': 0.90, 'var': 0, 'crit': 0, 'stun': 0,
     'cost': 30, 'sell_value': 15,
     'blind_effect': 0.30, 'blind_turns_min': 3, 'blind_turns_max': 5,
     'sound': '', 'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': POCKET_SAND, 'type': BLIND, 'subtype': BLIND, 'tier': 0,
     'damage': 0, 'uses': 2, 'acc': 0.90, 'var': 0, 'crit': 0, 'stun': 0,
     'cost': 20, 'sell_value': 8,
     'blind_effect': 0.20, 'blind_turns_min': 3, 'blind_turns_max': 5,
     'sound': '', 'areas': NA},

    # =====================================================
    #                     TIER 0 (STUN)
    # =====================================================

    {'name': STUN_GUN, 'type': MELEE, 'subtype': MELEE, 'tier': 0,
     'damage': 4, 'uses': 2, 'acc': 0.82, 'var': 1, 'crit': 0.02, 'stun': 1.0,
     'cost': 55, 'sell_value': 25,
     'sound': audio.MAGIC, 'areas': [CITY]},

    # =====================================================
    #                       TIER 1
    # =====================================================

    {'name': FOAM_FINGER, 'type': MELEE, 'subtype': MELEE, 'tier': 1,
     'damage': 1, 'uses': -1, 'acc': 0.88, 'var': 0, 'crit': 0.10, 'stun': 0.01,
     'cost': 0, 'sell_value': 0,
     'sound': audio.PUNCH, 'areas': NA},

    {'name': FLASHLIGHT, 'type': MELEE, 'subtype': BLUNT, 'tier': 1,
     'damage': 11, 'uses': 16, 'acc': 0.88, 'var': 1, 'crit': 0.04, 'stun': 0.06,
     'cost': 18, 'sell_value': 9,
     'sound': audio.BLUNT, 'areas': [CITY, CAVE]},

    {'name': INJECTION_NEEDLE, 'type': MELEE, 'subtype': MELEE, 'tier': 1,
     'damage': 14, 'uses': 11, 'acc': 0.92, 'var': 1, 'crit': 0.15, 'stun': 0,
     'cost': 26, 'sell_value': 13,
     'sound': audio.BLADE, 'areas': [CITY, CAVE]},

    {'name': PILLOW, 'type': MELEE, 'subtype': MELEE, 'tier': 1,
     'damage': 1, 'uses': -1, 'acc': 0.88, 'var': 0, 'crit': 0.10, 'stun': 0.01,
     'cost': 0, 'sell_value': 0,
     'sound': audio.PUNCH, 'areas': NA},

    {'name': POOL_CUE, 'type': MELEE, 'subtype': BLUNT, 'tier': 1,
     'damage': 13, 'uses': 12, 'acc': 0.83, 'var': 2, 'crit': 0.07, 'stun': 0.07,
     'cost': 22, 'sell_value': 12,
     'sound': audio.BLUNT, 'areas': NA},

    {'name': HARDCOVER_BOOK, 'type': MELEE, 'subtype': BLUNT, 'tier': 1,
     'damage': 14, 'uses': 10, 'acc': 0.89, 'var': 2, 'crit': 0.05, 'stun': 0.07,
     'cost': 21, 'sell_value': 11,
     'sound': audio.BLUNT, 'areas': [CITY, CAVE]},

    {'name': BINOCULARS, 'type': MELEE, 'subtype': BLUNT, 'tier': 1,
     'damage': 11, 'uses': 8, 'acc': 0.87, 'var': 2, 'crit': 0.11, 'stun': 0.05,
     'cost': 18, 'sell_value': 9,
     'sound': audio.BLUNT, 'areas': NA},

    {'name': BROKEN_BOTTLE, 'type': MELEE, 'subtype': BLADED, 'tier': 1,
     'damage': 14, 'uses': 7, 'acc': 0.84, 'var': 4, 'crit': 0.14, 'stun': 0,
     'cost': 18, 'sell_value': 9,
     'sound': audio.BLADE, 'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': RUBBER_CHICKEN, 'type': MELEE, 'subtype': MELEE, 'tier': 1,
     'damage': 9, 'uses': 16, 'acc': 0.88, 'var': 1, 'crit': 0.07, 'stun': 0.03,
     'cost': 14, 'sell_value': 7,
     'sound': audio.SQUEAK, 'areas': [CITY]},

    {'name': TREKKING_POLE, 'type': MELEE, 'subtype': MELEE, 'tier': 1,
     'damage': 13, 'uses': 10, 'acc': 0.87, 'var': 2, 'crit': 0.12, 'stun': 0.03,
     'cost': 24, 'sell_value': 12,
     'sound': audio.BLADE, 'areas': NA},

    {'name': SELFIE_STICK, 'type': MELEE, 'subtype': BLUNT, 'tier': 1,
     'damage': 10, 'uses': 15, 'acc': 0.87, 'var': 1, 'crit': 0.05, 'stun': 0.04,
     'cost': 12, 'sell_value': 6,
     'sound': audio.BLUNT, 'areas': NA},

    {'name': TROWEL, 'type': MELEE, 'subtype': BLADED, 'tier': 1,
     'damage': 13, 'uses': 13, 'acc': 0.88, 'var': 2, 'crit': 0.06, 'stun': 0,
     'cost': 19, 'sell_value': 9,
     'sound': audio.BLADE, 'areas': [FOREST, CAVE]},

    {'name': TRIPOD, 'type': MELEE, 'subtype': BLUNT, 'tier': 1,
     'damage': 13, 'uses': 12, 'acc': 0.83, 'var': 2, 'crit': 0.07, 'stun': 0.06,
     'cost': 22, 'sell_value': 11,
     'sound': audio.BLUNT, 'areas': NA},

    {'name': WALKING_STICK, 'type': MELEE, 'subtype': BLUNT, 'tier': 1,
     'damage': 12, 'uses': 14, 'acc': 0.87, 'var': 2, 'crit': 0.05, 'stun': 0.05,
     'cost': 18, 'sell_value': 9,
     'sound': audio.BLUNT, 'areas': NA},

    {'name': SUITCASE, 'type': MELEE, 'subtype': BLUNT, 'tier': 1,
     'damage': 13, 'uses': 13, 'acc': 0.84, 'var': 2, 'crit': 0.06, 'stun': 0.06,
     'cost': 16, 'sell_value': 8,
     'sound': audio.BLUNT, 'areas': NA},

    # =====================================================
    #                       TIER 2
    # =====================================================

    {'name': BASEBALL_BAT, 'type': MELEE, 'subtype': BLUNT, 'tier': 2,
     'damage': 23, 'uses': 12, 'acc': 0.82, 'var': 4, 'crit': 0.10, 'stun': 0.10,
     'cost': 42, 'sell_value': 21,
     'sound': audio.BLUNT, 'areas': [CITY, FOREST, SWAMP]},

    {'name': BONE_CLUB, 'type': MELEE, 'subtype': BLUNT, 'tier': 2,
     'damage': 20, 'uses': 12, 'acc': 0.78, 'var': 3, 'crit': 0.08, 'stun': 0.11,
     'cost': 28, 'sell_value': 14,
     'sound': audio.BLUNT, 'areas': [FOREST, SWAMP, CAVE]},

    {'name': BRASS_KNUCKLES, 'type': MELEE, 'subtype': MELEE, 'tier': 2,
     'damage': 21, 'uses': 12, 'acc': 0.89, 'var': 3, 'crit': 0.11, 'stun': 0.05,
     'cost': 45, 'sell_value': 23,
     'sound': audio.PUNCH, 'areas': [CITY]},

    {'name': BRICK, 'type': MELEE, 'subtype': BLUNT, 'tier': 2,
     'damage': 22, 'uses': 8, 'acc': 0.78, 'var': 5, 'crit': 0.07, 'stun': 0.12,
     'cost': 27, 'sell_value': 14,
     'sound': audio.BLUNT, 'areas': [CITY]},

    {'name': CANE, 'type': MELEE, 'subtype': BLUNT, 'tier': 1,
     'damage': 15, 'uses': 14, 'acc': 0.86, 'var': 2, 'crit': 0.08, 'stun': 0.07,
     'cost': 20, 'sell_value': 10,
     'sound': audio.BLUNT, 'areas': [CITY]},

    {'name': CHISEL, 'type': MELEE, 'subtype': BLADED, 'tier': 2,
     'damage': 17, 'uses': 11, 'acc': 0.84, 'var': 3, 'crit': 0.11, 'stun': 0,
     'cost': 22, 'sell_value': 11,
     'sound': audio.BLADE, 'areas': [CITY, CAVE]},

    {'name': CROWBAR, 'type': MELEE, 'subtype': BLUNT, 'tier': 2,
     'damage': 23, 'uses': 10, 'acc': 0.81, 'var': 4, 'crit': 0.08, 'stun': 0.11,
     'cost': 45, 'sell_value': 22,
     'sound': audio.BLUNT, 'areas': [CITY]},

    {'name': DUMBBELL, 'type': MELEE, 'subtype': BLUNT, 'tier': 2,
     'damage': 26, 'uses': 15, 'acc': 0.82, 'var': 4, 'crit': 0.09, 'stun': 0.13,
     'cost': 44, 'sell_value': 22,
     'sound': audio.BLUNT, 'areas': [CITY]},

    {'name': FISHING_SPEAR, 'type': MELEE, 'subtype': BLADED, 'tier': 2,
     'damage': 21, 'uses': 11, 'acc': 0.80, 'var': 4, 'crit': 0.10, 'stun': 0,
     'cost': 34, 'sell_value': 17,
     'sound': audio.BLADE, 'areas': [SWAMP]},

    {'name': HATCHET, 'type': MELEE, 'subtype': BLADED, 'tier': 2,
     'damage': 18, 'uses': 10, 'acc': 0.84, 'var': 4, 'crit': 0.10, 'stun': 0,
     'cost': 30, 'sell_value': 15,
     'sound': audio.BLADE, 'areas': [CAVE, FOREST, SWAMP]},

    {'name': HOCKEY_STICK, 'type': MELEE, 'subtype': BLUNT, 'tier': 2,
     'damage': 21, 'uses': 10, 'acc': 0.81, 'var': 3, 'crit': 0.12, 'stun': 0.09,
     'cost': 40, 'sell_value': 20,
     'sound': audio.BLUNT, 'areas': [CITY]},

    {'name': KNIFE, 'type': MELEE, 'subtype': BLADED, 'tier': 2,
     'damage': 16, 'uses': 10, 'acc': 0.89, 'var': 3, 'crit': 0.12, 'stun': 0,
     'cost': 26, 'sell_value': 12,
     'sound': audio.BLADE, 'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': POCKET_KNIFE, 'type': MELEE, 'subtype': BLADED, 'tier': 2,
     'damage': 16, 'uses': 14, 'acc': 0.89, 'var': 3, 'crit': 0.09, 'stun': 0,
     'cost': 18, 'sell_value': 9,
     'sound': audio.BLADE, 'areas': [CITY, FOREST]},

    {'name': SHIV, 'type': MELEE, 'subtype': BLADED, 'tier': 2,
     'damage': 18, 'uses': 11, 'acc': 0.89, 'var': 3, 'crit': 0.12, 'stun': 0,
     'cost': 22, 'sell_value': 11,
     'sound': audio.BLADE, 'areas': NA},

    {'name': SHOVEL, 'type': MELEE, 'subtype': BLUNT, 'tier': 2,
     'damage': 22, 'uses': 10, 'acc': 0.79, 'var': 4, 'crit': 0.08, 'stun': 0.10,
     'cost': 38, 'sell_value': 19,
     'sound': audio.BLUNT, 'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': STAFF, 'type': MELEE, 'subtype': BLUNT, 'tier': 1,
     'damage': 15, 'uses': 16, 'acc': 0.88, 'var': 3, 'crit': 0.04, 'stun': 0.07,
     'cost': 20, 'sell_value': 10,
     'sound': audio.BLUNT, 'areas': [SWAMP, FOREST]},

    {'name': SWITCHBLADE, 'type': MELEE, 'subtype': BLADED, 'tier': 2,
     'damage': 19, 'uses': 12, 'acc': 0.90, 'var': 3, 'crit': 0.13, 'stun': 0,
     'cost': 30, 'sell_value': 14,
     'sound': audio.BLADE, 'areas': [CITY]},

    {'name': TIRE_IRON, 'type': MELEE, 'subtype': BLUNT, 'tier': 2,
     'damage': 22, 'uses': 11, 'acc': 0.81, 'var': 4, 'crit': 0.09, 'stun': 0.10,
     'cost': 30, 'sell_value': 15,
     'sound': audio.BLUNT, 'areas': [CITY, SWAMP]},

    {'name': WOODEN_CLUB, 'type': MELEE, 'subtype': BLUNT, 'tier': 2,
     'damage': 19, 'uses': 14, 'acc': 0.81, 'var': 3, 'crit': 0.08, 'stun': 0.09,
     'cost': 24, 'sell_value': 12,
     'sound': audio.BLUNT, 'areas': [FOREST, SWAMP]},

    # =====================================================
    #                       TIER 3
    # =====================================================
    {'name': AXE, 'type': MELEE, 'subtype': BLADED, 'tier': 3,
     'damage': 30, 'uses': 9, 'acc': 0.74, 'var': 4, 'crit': 0.10, 'stun': 0.02,
     'cost': 65, 'sell_value': 32,
     'sound': audio.AXE, 'areas': [CITY, FOREST, SWAMP]},

    {'name': BONE_SAW, 'type': MELEE, 'subtype': BLADED, 'tier': 3,
     'damage': 24, 'uses': 8, 'acc': 0.83, 'var': 4, 'crit': 0.14, 'stun': 0,
     'cost': 46, 'sell_value': 23,
     'sound': audio.BLADE, 'areas': [CITY, CAVE, SWAMP]},

    {'name': BRANCH_SPEAR, 'type': MELEE, 'subtype': BLADED, 'tier': 3,
     'damage': 20, 'uses': 10, 'acc': 0.78, 'var': 4, 'crit': 0.09, 'stun': 0,
     'cost': 28, 'sell_value': 14,
     'sound': audio.BLADE, 'areas': [FOREST, SWAMP]},

    {'name': FIRE_AXE, 'type': MELEE, 'subtype': BLADED, 'tier': 3,
     'damage': 32, 'uses': 8, 'acc': 0.75, 'var': 4, 'crit': 0.09, 'stun': 0.03,
     'cost': 70, 'sell_value': 35,
     'sound': audio.AXE, 'areas': [CITY]},

    {'name': FROG_GIG, 'type': MELEE, 'subtype': BLADED, 'tier': 3,
     'damage': 24, 'uses': 11, 'acc': 0.81, 'var': 4, 'crit': 0.11, 'stun': 0,
     'cost': 36, 'sell_value': 18,
     'sound': audio.BLADE, 'areas': [SWAMP]},

    {'name': GAFF_HOOK, 'type': MELEE, 'subtype': BLADED, 'tier': 3,
     'damage': 27, 'uses': 10, 'acc': 0.80, 'var': 4, 'crit': 0.10, 'stun': 0,
     'cost': 50, 'sell_value': 25,
     'sound': audio.BLADE, 'areas': [SWAMP, CITY]},

    {'name': MACHETE, 'type': MELEE, 'subtype': BLADED, 'tier': 3,
     'damage': 26, 'uses': 10, 'acc': 0.81, 'var': 3, 'crit': 0.11, 'stun': 0,
     'cost': 55, 'sell_value': 28,
     'sound': audio.BLADE, 'areas': [CITY, FOREST, SWAMP]},

    {'name': MEAT_CLEAVER, 'type': MELEE, 'subtype': BLADED, 'tier': 3,
     'damage': 25, 'uses': 11, 'acc': 0.82, 'var': 4, 'crit': 0.13, 'stun': 0,
     'cost': 38, 'sell_value': 19,
     'sound': audio.BLADE, 'areas': [CITY, SWAMP]},

    {'name': OBSIDIAN_KNIFE, 'type': MELEE, 'subtype': BLADED, 'tier': 3,
     'damage': 28, 'uses': 9, 'acc': 0.88, 'var': 4, 'crit': 0.19, 'stun': 0,
     'cost': 60, 'sell_value': 30,
     'sound': audio.BLADE, 'areas': [CAVE, FOREST]},

    {'name': PICKAXE, 'type': MELEE, 'subtype': BLUNT, 'tier': 3,
     'damage': 25, 'uses': 9, 'acc': 0.79, 'var': 4, 'crit': 0.09, 'stun': 0.12,
     'cost': 55, 'sell_value': 28,
     'sound': audio.BLUNT, 'areas': [CAVE, FOREST]},

    {'name': SCYTHE, 'type': MELEE, 'subtype': BLADED, 'tier': 3,
     'damage': 27, 'uses': 12, 'acc': 0.77, 'var': 4, 'crit': 0.11, 'stun': 0,
     'cost': 47, 'sell_value': 25,
     'sound': audio.BLADE, 'areas': [FOREST, SWAMP]},

    {'name': SICKLE, 'type': MELEE, 'subtype': BLADED, 'tier': 3,
     'damage': 21, 'uses': 11, 'acc': 0.80, 'var': 4, 'crit': 0.11, 'stun': 0,
     'cost': 33, 'sell_value': 16,
     'sound': audio.BLADE, 'areas': [FOREST, SWAMP]},

    {'name': STONE_SPEAR, 'type': MELEE, 'subtype': BLADED, 'tier': 3,
     'damage': 22, 'uses': 10, 'acc': 0.77, 'var': 4, 'crit': 0.10, 'stun': 0,
     'cost': 36, 'sell_value': 18,
     'sound': audio.BLADE, 'areas': [CAVE, FOREST]},

    {'name': SURVIVAL_KNIFE, 'type': MELEE, 'subtype': BLADED, 'tier': 3,
     'damage': 21, 'uses': 12, 'acc': 0.86, 'var': 4, 'crit': 0.12, 'stun': 0,
     'cost': 32, 'sell_value': 16,
     'sound': audio.BLADE, 'areas': [FOREST, SWAMP, CAVE]},

    {'name': TORCH_CLUB, 'type': MELEE, 'subtype': BLUNT, 'tier': 3,
     'damage': 22, 'uses': 10, 'acc': 0.79, 'var': 3, 'crit': 0.12, 'stun': 0.11,
     'cost': 44, 'sell_value': 22,
     'sound': audio.BLUNT, 'areas': [CAVE, FOREST]},

    # =====================================================
    #                 TIER 4 (PROJECTILE)
    # =====================================================

    {'name': COMPOUND_BOW, 'type': RANGED, 'subtype': RANGED, 'tier': 4,
     'damage': 29, 'uses': 13, 'acc': 0.75, 'var': 3, 'crit': 0.18, 'stun': 0,
     'cost': 75, 'sell_value': 37,
     'sound': audio.ARROW, 'areas': [FOREST, SWAMP]},

    {'name': CROSSBOW, 'type': RANGED, 'subtype': RANGED, 'tier': 4,
     'damage': 34, 'uses': 7, 'acc': 0.84, 'var': 3, 'crit': 0.13, 'stun': 0,
     'cost': 85, 'sell_value': 40,
     'sound': audio.ARROW, 'areas': [FOREST, SWAMP]},

    {'name': FLARE_GUN, 'type': RANGED, 'subtype': RANGED, 'tier': 4,
     'damage': 27, 'uses': 7, 'acc': 0.72, 'var': 3, 'crit': 0.16, 'stun': 0,
     'cost': 60, 'sell_value': 30,
     'sound': audio.PISTOL, 'areas': [CITY, SWAMP]},

    {'name': HARPOON, 'type': RANGED, 'subtype': RANGED, 'tier': 4,
     'damage': 35, 'uses': 8, 'acc': 0.79, 'var': 3, 'crit': 0.10, 'stun': 0.03,
     'cost': 85, 'sell_value': 42,
     'sound': audio.ARROW, 'areas': [CITY, SWAMP]},

    {'name': KATANA, 'type': MELEE, 'subtype': MELEE, 'tier': 4,
     'damage': 33, 'uses': 10, 'acc': 0.81, 'var': 5, 'crit': 0.15, 'stun': 0,
     'cost': 90, 'sell_value': 45,
     'sound': audio.BLADE, 'areas': [CITY]},

    {'name': LONGBOW, 'type': RANGED, 'subtype': RANGED, 'tier': 4,
     'damage': 26, 'uses': 14, 'acc': 0.76, 'var': 3, 'crit': 0.15, 'stun': 0,
     'cost': 70, 'sell_value': 35,
     'sound': audio.ARROW, 'areas': [FOREST]},

    {'name': NAIL_GUN, 'type': RANGED, 'subtype': RANGED, 'tier': 4,
     'damage': 28, 'uses': 9, 'acc': 0.70, 'var': 4, 'crit': 0.14, 'stun': 0.02,
     'cost': 70, 'sell_value': 35,
     'sound': audio.ARROW, 'areas': [CITY]},

    {'name': PISTOL, 'type': RANGED, 'subtype': RANGED, 'tier': 4,
     'damage': 31, 'uses': 8, 'acc': 0.85, 'var': 5, 'crit': 0.11, 'stun': 0,
     'cost': 75, 'sell_value': 38,
     'sound': audio.PISTOL, 'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': REVOLVER, 'type': RANGED, 'subtype': RANGED, 'tier': 4,
     'damage': 40, 'uses': 6, 'acc': 0.70, 'var': 6, 'crit': 0.17, 'stun': 0,
     'cost': 80, 'sell_value': 40,
     'sound': audio.PISTOL, 'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': RIFLE, 'type': RANGED, 'subtype': RANGED, 'tier': 4,
     'damage': 36, 'uses': 7, 'acc': 0.86, 'var': 5, 'crit': 0.12, 'stun': 0,
     'cost': 90, 'sell_value': 45,
     'sound': audio.RIFLE, 'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': SHOTGUN, 'type': RANGED, 'subtype': RANGED, 'tier': 4,
     'damage': 40, 'uses': 6, 'acc': 0.73, 'var': 6, 'crit': 0.09, 'stun': 0.03,
     'cost': 90, 'sell_value': 45,
     'sound': audio.SHOTGUN, 'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': SLINGSHOT, 'type': RANGED, 'subtype': RANGED, 'tier': 4,
     'damage': 17, 'uses': 17, 'acc': 0.84, 'var': 2, 'crit': 0.12, 'stun': 0.02,
     'cost': 30, 'sell_value': 15,
     'sound': audio.ARROW, 'areas': [CITY, FOREST, SWAMP]},

    {'name': T_SHIRT_CANNON, 'type': RANGED, 'subtype': RANGED, 'tier': 4,
     'damage': 22, 'uses': 13, 'acc': 0.72, 'var': 3, 'crit': 0.09, 'stun': 0.04,
     'cost': 53, 'sell_value': 27,
     'sound': audio.SHOTGUN, 'areas': [CITY]},

    # =====================================================
    #                       TIER 5 (HEAVY)
    # =====================================================

    {'name': CHAINSAW, 'type': MELEE, 'subtype': MELEE, 'tier': 5,
     'damage': 40, 'uses': 8, 'acc': 0.71, 'var': 7, 'crit': 0.10, 'stun': 0.03,
     'cost': 100, 'sell_value': 50,
     'sound': audio.CHAINSAW, 'areas': [CITY, FOREST, SWAMP]},

    {'name': SLEDGEHAMMER, 'type': MELEE, 'subtype': BLUNT, 'tier': 5,
     'damage': 38, 'uses': 15, 'acc': 0.68, 'var': 7, 'crit': 0.08, 'stun': 0.18,
     'cost': 100, 'sell_value': 50,
     'sound': audio.BLUNT, 'areas': [CAVE, CITY, FOREST, SWAMP]},

    # =====================================================
    #                       SPECIAL
    # =====================================================

    {'name': TENCH_CANNON, 'type': RANGED, 'subtype': RANGED, 'tier': 5,
     'damage': 150, 'uses': 1, 'acc': 0.20, 'var': 1, 'crit': 0.10, 'stun': 0,
     'cost': 100, 'sell_value': 40,
     'sound': audio.SHOTGUN, 'areas': [CITY]},

    # =====================================================
    #                NOT OBTAINABLE BY PLAYER
    # =====================================================

    {'name': BEAK, 'type': SPECIAL, 'subtype': MELEE, 'tier': 0,
     'damage': 40, 'uses': -1, 'acc': 0.66, 'var': 5, 'crit': 0.20, 'stun': 0.05,
     'cost': 0, 'sell_value': 0,
     'sound': audio.EAT, 'areas': NA},

    {'name': CLAWS, 'type': SPECIAL, 'subtype': MELEE, 'tier': 0,
     'damage': 22, 'uses': -1, 'acc': 0.86, 'var': 3, 'crit': 0.10, 'stun': 0.03,
     'cost': 0, 'sell_value': 0,
     'sound': audio.PUNCH, 'areas': NA},

    {'name': FANGS, 'type': SPECIAL, 'subtype': MELEE, 'tier': 0,
     'damage': 27, 'uses': -1, 'acc': 0.86, 'var': 3, 'crit': 0.15, 'stun': 0.02,
     'cost': 0, 'sell_value': 0,
     'sound': audio.EAT, 'areas': NA},

    {'name': LASER_BEAMS, 'type': SPECIAL, 'subtype': RANGED, 'tier': 0,
     'damage': 30, 'uses': -1, 'acc': 0.74, 'var': 3, 'crit': 0.12, 'stun': 0,
     'cost': 0, 'sell_value': 0,
     'sound': audio.MAGIC, 'areas': NA},

    {'name': MAGIC_WAND, 'type': SPECIAL, 'subtype': RANGED, 'tier': 0,
     'damage': 25, 'uses': -1, 'acc': 0.77, 'var': 4, 'crit': 0.09, 'stun': 0,
     'cost': 0, 'sell_value': 0,
     'sound': audio.MAGIC, 'areas': NA},

    {'name': TAIL, 'type': SPECIAL, 'subtype': MELEE, 'tier': 0,
     'damage': 25, 'uses': -1, 'acc': 0.86, 'var': 2, 'crit': 0.10, 'stun': 0.08,
     'cost': 0, 'sell_value': 0,
     'sound': audio.PUNCH, 'areas': NA},

    {'name': TEETH, 'type': SPECIAL, 'subtype': MELEE, 'tier': 0,
     'damage': 23, 'uses': -1, 'acc': 0.86, 'var': 3, 'crit': 0.10, 'stun': 0.02,
     'cost': 0, 'sell_value': 0,
     'sound': audio.EAT, 'areas': NA},

    {'name': TENTACLES, 'type': SPECIAL, 'subtype': MELEE, 'tier': 0,
     'damage': 30, 'uses': -1, 'acc': 0.90, 'var': 2, 'crit': 0.10, 'stun': 0.07,
     'cost': 0, 'sell_value': 0,
     'sound': audio.PUNCH, 'areas': NA},

    {'name': VOODOO_STAFF, 'type': SPECIAL, 'subtype': RANGED, 'tier': 0,
     'damage': 28, 'uses': -1, 'acc': 0.76, 'var': 4, 'crit': 0.09, 'stun': 0,
     'cost': 0, 'sell_value': 0,
     'sound': audio.MAGIC, 'areas': NA},
]
