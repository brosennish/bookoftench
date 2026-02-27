import bookoftench.data.audio as audio

# --------- #
# Constants #
# --------- #

CAVE = "Cave"
CITY = "City"
FOREST = "Forest"
SWAMP = "Swamp"
NA = "NA" # Not applicable / can't be found or purchased

# Names
AXE = "Axe"
BARE_HANDS = "Bare Hands"
BASEBALL_BAT = "Baseball Bat"
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
INJECTION_NEEDLE = "Injection Needle"
KNIFE = "Knife"
LASER_BEAMS = "Laser Beams"
LONGBOW = "Longbow"
MACHETE = "Machete"
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
STONE_SPEAR = "Stone Spear"
SUITCASE = "Suitcase"
SURVIVAL_KNIFE = "Survival Knife"
SWITCHBLADE = "Switchblade"
TENCH_CANNON = "Tench Cannon"
TIRE_IRON = "Tire Iron"
TORCH_CLUB = "Torch Club"
TREKKING_POLE = "Trekking Pole"
TRIPOD = "Tripod"
TROWEL = "Trowel"
T_SHIRT_CANNON = "T-Shirt Cannon"
VOODOO_STAFF = "Voodoo Staff"
WALKING_STICK = "Walking Stick"
WOODEN_CLUB = "Wooden Club"


# Types
BLIND = 'blind'
MELEE = 'melee'
RANGED = 'ranged'
SPECIAL = 'special'

Weapons = [
    # =====================================================
    #                       DEFAULT
    # =====================================================
    {'name': BARE_HANDS, 'damage': 10, 'uses': -1, 'accuracy': 0.90, 'var': 3, 'crit': 0.08,
     'cost': 0, 'sell_value': 0, 'type': MELEE, 'tier': 1, 'sound': audio.PUNCH,
     'areas': [CAVE, CITY, FOREST, SWAMP]},

    # =====================================================
    #                       TIER 0 (BLIND)
    # =====================================================
    {'name': PEPPER_SPRAY, 'damage': 0, 'uses': 3, 'accuracy': 0.85, 'var': 0,
     'crit': 0, 'cost': 25, 'sell_value': 12, 'type': BLIND, 'tier': 0, 'sound': '',
     'blind_effect': 0.50, 'blind_turns_min': 2, 'blind_turns_max': 4,
     'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': BEAR_SPRAY, 'damage': 0, 'uses': 2, 'accuracy': 0.85, 'var': 0, 'crit': 0,
     'cost': 60, 'sell_value': 30, 'type': BLIND, 'tier': 0, 'sound': '',
     'blind_effect': 0.65, 'blind_turns_min': 2, 'blind_turns_max': 4,
     'areas': [CAVE, FOREST, SWAMP]},

    {'name': CHILI_POWDER, 'damage': 0, 'uses': 1, 'accuracy': 0.90, 'var': 0, 'crit': 0,
     'cost': 30, 'sell_value': 15, 'type': BLIND, 'tier': 0, 'sound': '',
     'blind_effect': 0.30, 'blind_turns_min': 3, 'blind_turns_max': 5,
     'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': POCKET_SAND, 'damage': 0, 'uses': 1, 'accuracy': 0.90, 'var': 0, 'crit': 0,
     'cost': 20, 'sell_value': 8, 'type': BLIND, 'tier': 0, 'sound': '',
     'blind_effect': 0.20, 'blind_turns_min': 3, 'blind_turns_max': 5,
     'areas': NA},

    # =====================================================
    #                       TIER 1
    # =====================================================
    {'name': FOAM_FINGER, 'damage': 1, 'uses': -1, 'accuracy': 0.88, 'var': 3, 'crit': 0.10,
     'cost': 0, 'sell_value': 0, 'type': MELEE, 'tier': 1, 'sound': audio.PUNCH,
     'areas': NA},

    {'name': FLASHLIGHT, 'damage': 11, 'uses': 14, 'accuracy': 0.88, 'var': 1, 'crit': 0.04,
     'cost': 20, 'sell_value': 8, 'type': MELEE, 'tier': 1, 'sound': audio.BLUNT,
     'areas': [CITY, CAVE]},

    {'name': INJECTION_NEEDLE, 'damage': 14, 'uses': 10, 'accuracy': 0.92, 'var': 2, 'crit': 0.15,
     'cost': 26, 'sell_value': 13, 'type': MELEE, 'tier': 1, 'sound': audio.BLADE,
     'areas': [CITY, CAVE]},

    {'name': PILLOW, 'damage': 1, 'uses': -1, 'accuracy': 0.88, 'var': 0, 'crit': 0.10,
     'cost': 0, 'sell_value': 0, 'type': MELEE, 'tier': 1, 'sound': audio.PUNCH,
     'areas': NA},

    {'name': POOL_CUE, 'damage': 13, 'uses': 10, 'accuracy': 0.83, 'var': 1, 'crit': 0.07,
     'cost': 24, 'sell_value': 12, 'type': MELEE, 'tier': 1, 'sound': audio.BLUNT,
     'areas': NA},

    {'name': HARDCOVER_BOOK, 'damage': 14, 'uses': 9, 'accuracy': 0.89, 'var': 2, 'crit': 0.05,
     'cost': 18, 'sell_value': 9, 'type': MELEE, 'tier': 1, 'sound': audio.BLUNT,
     'areas': [CITY, CAVE]},

    {'name': BINOCULARS, 'damage': 11, 'uses': 7, 'accuracy': 0.84, 'var': 3, 'crit': 0.11,
     'cost': 18, 'sell_value': 9, 'type': MELEE, 'tier': 1, 'sound': audio.BLUNT,
     'areas': NA},

    {'name': BROKEN_BOTTLE, 'damage': 14, 'uses': 6, 'accuracy': 0.84, 'var': 4, 'crit': 0.11,
     'cost': 18, 'sell_value': 9, 'type': MELEE, 'tier': 1, 'sound': audio.BLADE,
     'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': RUBBER_CHICKEN, 'damage': 9, 'uses': 14, 'accuracy': 0.88, 'var': 2, 'crit': 0.07,
     'cost': 14, 'sell_value': 7, 'type': MELEE, 'tier': 1, 'sound': audio.PUNCH,
     'areas': [CITY]},

    {'name': TREKKING_POLE, 'damage': 13, 'uses': 9, 'accuracy': 0.87, 'var': 2, 'crit': 0.12,
     'cost': 24, 'sell_value': 12, 'type': MELEE, 'tier': 1, 'sound': audio.BLADE,
     'areas': NA},

    {'name': SELFIE_STICK, 'damage': 10, 'uses': 13, 'accuracy': 0.87, 'var': 1, 'crit': 0.05,
     'cost': 12, 'sell_value': 6, 'type': MELEE, 'tier': 1, 'sound': audio.BLUNT,
     'areas': NA},

    {'name': TROWEL, 'damage': 13, 'uses': 13, 'accuracy': 0.88, 'var': 2, 'crit': 0.06,
     'cost': 14, 'sell_value': 7, 'type': MELEE, 'tier': 1, 'sound': audio.BLADE,
     'areas': [FOREST, CAVE]},

    {'name': TRIPOD, 'damage': 13, 'uses': 10, 'accuracy': 0.83, 'var': 1, 'crit': 0.07,
     'cost': 22, 'sell_value': 11, 'type': MELEE, 'tier': 1, 'sound': audio.BLUNT,
     'areas': NA},

    {'name': WALKING_STICK, 'damage': 12, 'uses': 12, 'accuracy': 0.87, 'var': 1, 'crit': 0.05,
     'cost': 18, 'sell_value': 9, 'type': MELEE, 'tier': 1, 'sound': audio.BLUNT,
     'areas': NA},

    {'name': SUITCASE, 'damage': 13, 'uses': 11, 'accuracy': 0.84, 'var': 2, 'crit': 0.06,
     'cost': 16, 'sell_value': 8, 'type': MELEE, 'tier': 1, 'sound': audio.BLUNT,
     'areas': NA},

    # =====================================================
    #                       TIER 2
    # =====================================================
    {'name': BASEBALL_BAT, 'damage': 23, 'uses': 10, 'accuracy': 0.82, 'var': 4, 'crit': 0.10,
     'cost': 42, 'sell_value': 21, 'type': MELEE, 'tier': 2, 'sound': audio.BLUNT,
     'areas': [CITY, FOREST, SWAMP]},

    {'name': BONE_CLUB, 'damage': 20, 'uses': 9, 'accuracy': 0.78, 'var': 3, 'crit': 0.08,
     'cost': 28, 'sell_value': 14, 'type': MELEE, 'tier': 2, 'sound': audio.BLUNT,
     'areas': [FOREST, SWAMP, CAVE]},

    {'name': BRASS_KNUCKLES, 'damage': 21, 'uses': 11, 'accuracy': 0.89, 'var': 3, 'crit': 0.11,
     'cost': 55, 'sell_value': 25, 'type': MELEE, 'tier': 2, 'sound': audio.PUNCH,
     'areas': [CITY]},

    {'name': BRICK, 'damage': 22, 'uses': 6, 'accuracy': 0.78, 'var': 5, 'crit': 0.07,
     'cost': 20, 'sell_value': 10, 'type': MELEE, 'tier': 2, 'sound': audio.BLUNT,
     'areas': [CITY]},

    {'name': CANE, 'damage': 15, 'uses': 12, 'accuracy': 0.86, 'var': 2, 'crit': 0.08,
     'cost': 20, 'sell_value': 10, 'type': MELEE, 'tier': 1, 'sound': audio.BLUNT,
     'areas': [CITY]},

    {'name': CHISEL, 'damage': 17, 'uses': 9, 'accuracy': 0.84, 'var': 3, 'crit': 0.11,
     'cost': 22, 'sell_value': 11, 'type': MELEE, 'tier': 2, 'sound': audio.BLADE,
     'areas': [CITY, CAVE]},

    {'name': CROWBAR, 'damage': 23, 'uses': 8, 'accuracy': 0.81, 'var': 4, 'crit': 0.08,
     'cost': 45, 'sell_value': 22, 'type': MELEE, 'tier': 2, 'sound': audio.BLUNT,
     'areas': [CITY]},

    {'name': DUMBBELL, 'damage': 26, 'uses': 12, 'accuracy': 0.82, 'var': 4, 'crit': 0.09,
     'cost': 44, 'sell_value': 22, 'type': MELEE, 'tier': 2, 'sound': audio.BLUNT,
     'areas': [CITY]},

    {'name': FISHING_SPEAR, 'damage': 21, 'uses': 9, 'accuracy': 0.80, 'var': 4, 'crit': 0.10,
     'cost': 34, 'sell_value': 17, 'type': MELEE, 'tier': 2, 'sound': audio.BLADE,
     'areas': [SWAMP]},

    {'name': HATCHET, 'damage': 18, 'uses': 8, 'accuracy': 0.84, 'var': 4, 'crit': 0.10,
     'cost': 30, 'sell_value': 15, 'type': MELEE, 'tier': 2, 'sound': audio.BLADE,
     'areas': [CAVE, FOREST, SWAMP]},

    {'name': KNIFE, 'damage': 16, 'uses': 9, 'accuracy': 0.89, 'var': 4, 'crit': 0.12,
     'cost': 24, 'sell_value': 12, 'type': MELEE, 'tier': 2, 'sound': audio.BLADE,
     'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': POCKET_KNIFE, 'damage': 16, 'uses': 12, 'accuracy': 0.89, 'var': 3, 'crit': 0.09,
     'cost': 18, 'sell_value': 9, 'type': MELEE, 'tier': 2, 'sound': audio.BLADE,
     'areas': [CITY, FOREST]},

    {'name': SHIV, 'damage': 18, 'uses': 10, 'accuracy': 0.89, 'var': 3, 'crit': 0.12,
     'cost': 20, 'sell_value': 10, 'type': MELEE, 'tier': 2, 'sound': audio.BLADE,
     'areas': NA},

    {'name': SHOVEL, 'damage': 22, 'uses': 8, 'accuracy': 0.79, 'var': 4, 'crit': 0.08,
     'cost': 38, 'sell_value': 19, 'type': MELEE, 'tier': 2, 'sound': audio.BLUNT,
     'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': SWITCHBLADE, 'damage': 19, 'uses': 11, 'accuracy': 0.90, 'var': 4, 'crit': 0.13,
     'cost': 28, 'sell_value': 14, 'type': MELEE, 'tier': 2, 'sound': audio.BLADE,
     'areas': [CITY]},

    {'name': TIRE_IRON, 'damage': 22, 'uses': 9, 'accuracy': 0.81, 'var': 4, 'crit': 0.09,
     'cost': 30, 'sell_value': 15, 'type': MELEE, 'tier': 2, 'sound': audio.BLUNT,
     'areas': [CITY, SWAMP]},

    {'name': WOODEN_CLUB, 'damage': 19, 'uses': 11, 'accuracy': 0.81, 'var': 3, 'crit': 0.08,
     'cost': 24, 'sell_value': 12, 'type': MELEE, 'tier': 2, 'sound': audio.BLUNT,
     'areas': [FOREST, SWAMP]},

    # =====================================================
    #                       TIER 3
    # =====================================================
    {'name': AXE, 'damage': 30, 'uses': 7, 'accuracy': 0.77, 'var': 6, 'crit': 0.10,
     'cost': 65, 'sell_value': 32, 'type': MELEE, 'tier': 3, 'sound': audio.AXE,
     'areas': [CITY, FOREST, SWAMP]},

    {'name': BONE_SAW, 'damage': 24, 'uses': 7, 'accuracy': 0.83, 'var': 4, 'crit': 0.14,
     'cost': 46, 'sell_value': 23, 'type': MELEE, 'tier': 3, 'sound': audio.BLADE,
     'areas': [CITY, CAVE, SWAMP]},

    {'name': BRANCH_SPEAR, 'damage': 20, 'uses': 8, 'accuracy': 0.78, 'var': 4, 'crit': 0.09,
     'cost': 28, 'sell_value': 14, 'type': MELEE, 'tier': 3, 'sound': audio.BLADE,
     'areas': [FOREST, SWAMP]},

    {'name': FIRE_AXE, 'damage': 32, 'uses': 6, 'accuracy': 0.76, 'var': 6, 'crit': 0.09,
     'cost': 70, 'sell_value': 35, 'type': MELEE, 'tier': 3, 'sound': audio.AXE,
     'areas': [CITY]},

    {'name': FROG_GIG, 'damage': 24, 'uses': 9, 'accuracy': 0.81, 'var': 4, 'crit': 0.11,
     'cost': 36, 'sell_value': 18, 'type': MELEE, 'tier': 3, 'sound': audio.BLADE,
     'areas': [SWAMP]},

    {'name': GAFF_HOOK, 'damage': 27, 'uses': 8, 'accuracy': 0.80, 'var': 5, 'crit': 0.10,
     'cost': 48, 'sell_value': 24, 'type': MELEE, 'tier': 3, 'sound': audio.BLADE,
     'areas': [SWAMP, CITY]},

    {'name': MACHETE, 'damage': 26, 'uses': 8, 'accuracy': 0.81, 'var': 5, 'crit': 0.11,
     'cost': 60, 'sell_value': 30, 'type': MELEE, 'tier': 3, 'sound': audio.BLADE,
     'areas': [CITY, FOREST, SWAMP]},

    {'name': MEAT_CLEAVER, 'damage': 23, 'uses': 9, 'accuracy': 0.82, 'var': 4, 'crit': 0.13,
     'cost': 38, 'sell_value': 19, 'type': MELEE, 'tier': 3, 'sound': audio.BLADE,
     'areas': [CITY, SWAMP]},

    {'name': OBSIDIAN_KNIFE, 'damage': 28, 'uses': 8, 'accuracy': 0.88, 'var': 4, 'crit': 0.16,
     'cost': 58, 'sell_value': 29, 'type': MELEE, 'tier': 3, 'sound': audio.BLADE,
     'areas': [CAVE, FOREST]},

    {'name': PICKAXE, 'damage': 25, 'uses': 7, 'accuracy': 0.79, 'var': 6, 'crit': 0.09,
     'cost': 55, 'sell_value': 28, 'type': MELEE, 'tier': 3, 'sound': audio.BLUNT,
     'areas': [CAVE, FOREST]},

    {'name': SCYTHE, 'damage': 27, 'uses': 9, 'accuracy': 0.79, 'var': 5, 'crit': 0.11,
     'cost': 33, 'sell_value': 16, 'type': MELEE, 'tier': 3, 'sound': audio.BLADE,
     'areas': [FOREST, SWAMP]},

    {'name': SICKLE, 'damage': 21, 'uses': 9, 'accuracy': 0.80, 'var': 4, 'crit': 0.11,
     'cost': 33, 'sell_value': 16, 'type': MELEE, 'tier': 3, 'sound': audio.BLADE,
     'areas': [FOREST, SWAMP]},

    {'name': STONE_SPEAR, 'damage': 22, 'uses': 8, 'accuracy': 0.77, 'var': 4, 'crit': 0.10,
     'cost': 36, 'sell_value': 18, 'type': MELEE, 'tier': 3, 'sound': audio.BLADE,
     'areas': [CAVE, FOREST]},

    {'name': SURVIVAL_KNIFE, 'damage': 21, 'uses': 12, 'accuracy': 0.86, 'var': 4, 'crit': 0.12,
     'cost': 32, 'sell_value': 16, 'type': MELEE, 'tier': 3, 'sound': audio.BLADE,
     'areas': [FOREST, SWAMP, CAVE]},

    {'name': TORCH_CLUB, 'damage': 22, 'uses': 8, 'accuracy': 0.79, 'var': 3, 'crit': 0.12,
     'cost': 44, 'sell_value': 22, 'type': MELEE, 'tier': 3, 'sound': audio.BLUNT,
     'areas': [CAVE, FOREST]},

    # =====================================================
    #                       TIER 4 (PROJECTILE)
    # =====================================================
    {'name': COMPOUND_BOW, 'damage': 29, 'uses': 10, 'accuracy': 0.75, 'var': 5, 'crit': 0.18,
     'cost': 75, 'sell_value': 37, 'type': RANGED, 'tier': 4, 'sound': audio.ARROW,
     'areas': [FOREST, SWAMP]},

    {'name': CROSSBOW, 'damage': 34, 'uses': 6, 'accuracy': 0.84, 'var': 5, 'crit': 0.13,
     'cost': 85, 'sell_value': 40, 'type': RANGED, 'tier': 4, 'sound': audio.ARROW,
     'areas': [FOREST, SWAMP]},

    {'name': FLARE_GUN, 'damage': 27, 'uses': 5, 'accuracy': 0.72, 'var': 3, 'crit': 0.16,
     'cost': 60, 'sell_value': 30, 'type': RANGED, 'tier': 4, 'sound': audio.PISTOL,
     'areas': [CITY, SWAMP]},

    {'name': HARPOON, 'damage': 35, 'uses': 6, 'accuracy': 0.79, 'var': 5, 'crit': 0.10,
     'cost': 85, 'sell_value': 42, 'type': RANGED, 'tier': 4, 'sound': audio.ARROW,
     'areas': [CITY, SWAMP]},

    {'name': LONGBOW, 'damage': 26, 'uses': 11, 'accuracy': 0.76, 'var': 5, 'crit': 0.15,
     'cost': 68, 'sell_value': 34, 'type': RANGED, 'tier': 4, 'sound': audio.ARROW,
     'areas': [FOREST]},

    {'name': NAIL_GUN, 'damage': 28, 'uses': 6, 'accuracy': 0.73, 'var': 4, 'crit': 0.14,
     'cost': 70, 'sell_value': 35, 'type': RANGED, 'tier': 4, 'sound': audio.ARROW,
     'areas': [CITY]},

    {'name': PISTOL, 'damage': 31, 'uses': 6, 'accuracy': 0.85, 'var': 5, 'crit': 0.11,
     'cost': 70, 'sell_value': 34, 'type': RANGED, 'tier': 4, 'sound': audio.PISTOL,
     'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': REVOLVER, 'damage': 38, 'uses': 5, 'accuracy': 0.70, 'var': 6, 'crit': 0.10,
     'cost': 78, 'sell_value': 39, 'type': RANGED, 'tier': 4, 'sound': audio.PISTOL,
     'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': RIFLE, 'damage': 36, 'uses': 6, 'accuracy': 0.86, 'var': 5, 'crit': 0.12,
     'cost': 88, 'sell_value': 41, 'type': RANGED, 'tier': 4, 'sound': audio.RIFLE,
     'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': SHOTGUN, 'damage': 40, 'uses': 4, 'accuracy': 0.73, 'var': 7, 'crit': 0.09,
     'cost': 90, 'sell_value': 45, 'type': RANGED, 'tier': 4, 'sound': audio.SHOTGUN,
     'areas': [CAVE, CITY, FOREST, SWAMP]},

    {'name': SLINGSHOT, 'damage': 17, 'uses': 14, 'accuracy': 0.84, 'var': 2, 'crit': 0.12,
     'cost': 27, 'sell_value': 14, 'type': RANGED, 'tier': 4, 'sound': audio.ARROW,
     'areas': [CITY, FOREST, SWAMP]},

    {'name': T_SHIRT_CANNON, 'damage': 22, 'uses': 9, 'accuracy': 0.72, 'var': 3, 'crit': 0.09,
     'cost': 53, 'sell_value': 27, 'type': RANGED, 'tier': 4, 'sound': audio.SHOTGUN,
     'areas': [CITY]},

    # =====================================================
    #                       TIER 5 (HEAVY)
    # =====================================================
    {'name': CHAINSAW, 'damage': 40, 'uses': 6, 'accuracy': 0.71, 'var': 7, 'crit': 0.10,
     'cost': 95, 'sell_value': 47, 'type': MELEE, 'tier': 5, 'sound': audio.CHAINSAW,
     'areas': [CITY, FOREST, SWAMP]},

    {'name': SLEDGEHAMMER, 'damage': 38, 'uses': 10, 'accuracy': 0.71, 'var': 6, 'crit': 0.08,
     'cost': 100, 'sell_value': 50, 'type': MELEE, 'tier': 5, 'sound': audio.BLUNT,
     'areas': [CAVE, CITY, FOREST, SWAMP]},

    # =====================================================
    #                       SPECIAL
    # =====================================================
    {'name': TENCH_CANNON, 'damage': 99, 'uses': 1, 'accuracy': 0.20, 'var': 8, 'crit': 0.10,
     'cost': 100, 'sell_value': 50, 'type': RANGED, 'tier': 5, 'sound': audio.SHOTGUN,
     'areas': [CITY]},

    # =====================================================
    #                NOT OBTAINABLE BY PLAYER
    # =====================================================
    {'name': CLAWS, 'damage': 22, 'uses': -1, 'accuracy': 0.86, 'var': 4, 'crit': 0.10,
     'cost': 0, 'sell_value': 0, 'type': SPECIAL, 'tier': 0, 'sound': audio.PUNCH,
     'areas': NA},

    {'name': LASER_BEAMS, 'damage': 30, 'uses': -1, 'accuracy': 0.74, 'var': 4, 'crit': 0.12,
     'cost': 0, 'sell_value': 0, 'type': SPECIAL, 'tier': 0, 'sound': audio.MAGIC,
     'areas': NA},

    {'name': VOODOO_STAFF, 'damage': 28, 'uses': -1, 'accuracy': 0.76, 'var': 7, 'crit': 0.09,
     'cost': 0, 'sell_value': 0, 'type': SPECIAL, 'tier': 0, 'sound': audio.MAGIC,
     'areas': NA},
]
