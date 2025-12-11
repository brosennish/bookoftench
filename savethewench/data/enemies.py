from . import weapons

# Constants
BANDIT = "Bandit"
BAYOU_BILL = "Bayou Bill"
BAYOU_MAN = "Bayou Man"
CAPTAIN_HOLE = "Captain Hole"
DENNY_BILTMORE = "Denny Biltmore"
DISGRACED_EXILE = "Disgraced Exile"
GOON = "Goon"
HAND_FISHERMAN = "Hand Fisherman"
HIKER = "Hiker"
HOBO = "Hobo"
HUMANOID_CAVE_CREATURE = "Humanoid Cave Creature"
HUNTER = "Hunter"
MINER = "Miner"
MOLE_PERSON = "Mole Person"
PIMP = "Pimp"
POACHER = "Poacher"
SERIAL_KILLER = "Serial Killer"
SKIN_COLLECTOR = "Skin Collector"
SLEDGE_HAMMOND = "Sledge Hammond"
SPELUNKER = "Spelunker"
THE_MAYOR = "The Mayor"
VOODOO_PRIESTESS = "Voodoo Priestess"

# Types
NORMAL = "normal"
BOSS = "boss"
FINAL_BOSS = "boss_final"

Enemies = [
    # ========================
    #        CITY ENEMIES
    # ========================
    {'name': BANDIT, 'hp': 80, 'weapons': [weapons.KNIFE, weapons.BAT], 'bounty': 30, 'type': 'normal'},
    {'name': GOON, 'hp': 100, 'weapons': [weapons.CHILI_POWDER, weapons.BAT, weapons.PISTOL],
     'bounty': 40, 'type': 'normal'},
    {'name': PIMP, 'hp': 120,
     'weapons': [weapons.PEPPER_SPRAY, weapons.BRASS_KNUCKLES, weapons.REVOLVER], 'bounty': 60,
     'type': 'normal'},
    {'name': HOBO, 'hp': 80, 'weapons': [weapons.BROKEN_BOTTLE, weapons.KNIFE, weapons.POCKET_SAND],
     'bounty': 25, 'type': 'normal'},
    {'name': SERIAL_KILLER, 'hp': 120, 'weapons': [weapons.KNIFE, weapons.MACHETE], 'bounty': 65,
     'type': 'normal'},

    # ========================
    #       FOREST ENEMIES
    # ========================
    {'name': HIKER, 'hp': 80, 'weapons': [weapons.HATCHET, weapons.KNIFE, weapons.BEAR_SPRAY],
     'bounty': 30, 'type': 'normal'},
    {'name': HUNTER, 'hp': 100, 'weapons': [weapons.KNIFE, weapons.RIFLE, weapons.BEAR_SPRAY],
     'bounty': 50, 'type': 'normal'},
    {'name': POACHER, 'hp': 120, 'weapons': [weapons.CROSSBOW, weapons.MACHETE, weapons.BEAR_SPRAY],
     'bounty': 60, 'type': 'normal'},
    {'name': DISGRACED_EXILE, 'hp': 100, 'weapons': [weapons.HATCHET, weapons.SHOVEL], 'bounty': 45,
     'type': 'normal'},

    # ========================
    #        CAVE ENEMIES
    # ========================
    {'name': MINER, 'hp': 80, 'weapons': [weapons.PICKAXE, weapons.KNIFE], 'bounty': 35, 'type': 'normal'},
    {'name': SPELUNKER, 'hp': 100, 'weapons': [weapons.PICKAXE, weapons.KNIFE], 'bounty': 40,
     'type': 'normal'},
    {'name': MOLE_PERSON, 'hp': 120, 'weapons': [weapons.CLAWS, weapons.PICKAXE], 'bounty': 55,
     'type': 'normal'},
    {'name': HUMANOID_CAVE_CREATURE, 'hp': 120, 'weapons': [weapons.CLAWS, weapons.SLEDGEHAMMER],
     'bounty': 65, 'type': 'normal'},

    # ========================
    #        SWAMP ENEMIES
    # ========================
    {'name': HAND_FISHERMAN, 'hp': 80, 'weapons': [weapons.HATCHET, weapons.KNIFE], 'bounty': 30,
     'type': 'normal'},
    {'name': BAYOU_MAN, 'hp': 100, 'weapons': [weapons.MACHETE, weapons.SHOTGUN], 'bounty': 45,
     'type': 'normal'},
    {'name': VOODOO_PRIESTESS, 'hp': 120,
     'weapons': [weapons.VOODOO_STAFF, weapons.KNIFE, weapons.CHILI_POWDER], 'bounty': 70,
     'type': 'normal'},
    {'name': SKIN_COLLECTOR, 'hp': 110, 'weapons': [weapons.MACHETE, weapons.CHAINSAW], 'bounty': 75,
     'type': 'normal'},
]

Bosses = [
    # ========================
    #        AREA BOSSES
    # ========================
    {'name': SLEDGE_HAMMOND, 'hp': 220,
     'weapons': [weapons.SLEDGEHAMMER, weapons.AXE, weapons.CHAINSAW, weapons.BRASS_KNUCKLES],
     'bounty': 0, 'type': 'boss'},

    {'name': THE_MAYOR, 'hp': 200,
     'weapons': [weapons.PISTOL, weapons.SHOTGUN, weapons.REVOLVER, weapons.BRASS_KNUCKLES],
     'bounty': 0, 'type': 'boss'},

    {'name': BAYOU_BILL, 'hp': 200,
     'weapons': [weapons.MACHETE, weapons.SLEDGEHAMMER, weapons.SHOTGUN, weapons.CHAINSAW],
     'bounty': 0, 'type': 'boss'},

    {'name': CAPTAIN_HOLE, 'hp': 200,
     'weapons': [weapons.RIFLE, weapons.HARPOON, weapons.KNIFE, weapons.PISTOL],
     'bounty': 0, 'type': 'boss'},
]

# ========================
#        FINAL BOSS
# ========================
Final_Boss = {'name': DENNY_BILTMORE, 'hp': 275,
              'weapons': [weapons.BRASS_KNUCKLES, weapons.PISTOL, weapons.REVOLVER, weapons.SHOTGUN],
              'bounty': 0, 'type': 'boss_final'}
