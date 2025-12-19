from savethewench.ui import red, Colors
from . import audio, weapons

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
FINAL_BOSS = "final_boss"

Enemies = [
    # ========================
    #        CITY ENEMIES
    # ========================
    {'name': BANDIT, 'hp': 80, 'weapons': [weapons.KNIFE, weapons.BAT], 'bounty': 30, 'type': NORMAL},
    {'name': GOON, 'hp': 100, 'weapons': [weapons.CHILI_POWDER, weapons.BAT, weapons.PISTOL],
     'bounty': 40, 'type': NORMAL},
    {'name': PIMP, 'hp': 120,
     'weapons': [weapons.PEPPER_SPRAY, weapons.BRASS_KNUCKLES, weapons.REVOLVER], 'bounty': 60, 'type': NORMAL},
    {'name': HOBO, 'hp': 80, 'weapons': [weapons.BROKEN_BOTTLE, weapons.KNIFE, weapons.POCKET_SAND],
     'bounty': 25, 'type': NORMAL},
    {'name': SERIAL_KILLER, 'hp': 120, 'weapons': [weapons.KNIFE, weapons.MACHETE], 'bounty': 65, 'type': NORMAL},

    # ========================
    #       FOREST ENEMIES
    # ========================
    {'name': HIKER, 'hp': 80, 'weapons': [weapons.HATCHET, weapons.KNIFE, weapons.BEAR_SPRAY],
     'bounty': 30, 'type': NORMAL},
    {'name': HUNTER, 'hp': 100, 'weapons': [weapons.KNIFE, weapons.RIFLE, weapons.BEAR_SPRAY],
     'bounty': 50, 'type': NORMAL},
    {'name': POACHER, 'hp': 120, 'weapons': [weapons.CROSSBOW, weapons.MACHETE, weapons.BEAR_SPRAY],
     'bounty': 60, 'type': NORMAL},
    {'name': DISGRACED_EXILE, 'hp': 100, 'weapons': [weapons.HATCHET, weapons.SHOVEL], 'bounty': 45, 'type': NORMAL},

    # ========================
    #        CAVE ENEMIES
    # ========================
    {'name': MINER, 'hp': 80, 'weapons': [weapons.PICKAXE, weapons.KNIFE], 'bounty': 35, 'type': NORMAL},
    {'name': SPELUNKER, 'hp': 100, 'weapons': [weapons.PICKAXE, weapons.KNIFE], 'bounty': 40, 'type': NORMAL},
    {'name': MOLE_PERSON, 'hp': 120, 'weapons': [weapons.CLAWS, weapons.PICKAXE], 'bounty': 55, 'type': NORMAL},
    {'name': HUMANOID_CAVE_CREATURE, 'hp': 120, 'weapons': [weapons.CLAWS, weapons.SLEDGEHAMMER],
     'bounty': 65, 'type': NORMAL},

    # ========================
    #        SWAMP ENEMIES
    # ========================
    {'name': HAND_FISHERMAN, 'hp': 80, 'weapons': [weapons.HATCHET, weapons.KNIFE], 'bounty': 30, 'type': NORMAL},
    {'name': BAYOU_MAN, 'hp': 100, 'weapons': [weapons.MACHETE, weapons.SHOTGUN], 'bounty': 45, 'type': NORMAL},
    {'name': VOODOO_PRIESTESS, 'hp': 120,
     'weapons': [weapons.VOODOO_STAFF, weapons.KNIFE, weapons.CHILI_POWDER], 'bounty': 70, 'type': NORMAL},
    {'name': SKIN_COLLECTOR, 'hp': 110, 'weapons': [weapons.MACHETE, weapons.CHAINSAW], 'bounty': 75, 'type': NORMAL},
]

Bosses = [
    # ========================
    #        AREA BOSSES
    # ========================
    {'name': SLEDGE_HAMMOND, 'hp': 220,
     'weapons': [weapons.SLEDGEHAMMER, weapons.AXE, weapons.CHAINSAW, weapons.BRASS_KNUCKLES],
     'bounty': 0, 'type': BOSS, 'preamble': {}},

    {'name': THE_MAYOR, 'hp': 200,
     'weapons': [weapons.PISTOL, weapons.SHOTGUN, weapons.REVOLVER, weapons.BRASS_KNUCKLES],
     'bounty': 0, 'type': BOSS, 'theme': audio.FINAL_BOSS_THEME},

    {'name': BAYOU_BILL, 'hp': 200,
     'weapons': [weapons.MACHETE, weapons.SLEDGEHAMMER, weapons.SHOTGUN, weapons.CHAINSAW],
     'bounty': 0, 'type': BOSS,
     'preamble': [
         {'text': "What do we have here?", 'color': Colors.RED,'sleep': 2},
         {'text': "Looks like anotha one a dem riverboat bad boys right heuh uh huh.",
          'color': Colors.RED, 'sleep': 2},
         {'text': "Bill's had a hankerin' for some a dat riverboat gumbo, mmhm.", 'color': Colors.RED, 'sleep': 2},
         {'text': red("We gonna cook up some riverboat gumbo with some stuffin' with that mmhm riverboat boy."),
          'color': Colors.RED, 'sleep': 2},
     ],
     'random_dialogue': [
         {'upper_threshold': 0.08,
          'dialogue': [
             {'text': "Riverboat... riverboat... we cookin' today, boy.", 'color': Colors.RED, 'sleep': 2},
             {'text': "Gonna toss some crawdad in dat pot, mmhm.", 'color': Colors.RED, 'sleep': 2},
             {'text': "Alligator gumbo! Now we talkin'.", 'color': Colors.RED, 'sleep': 2},
         ]},
         {'upper_threshold': 0.16,
          'dialogue': [
             {'text': "When you livin' in the swamp, ain't nobody come round lessen dey askin' for trouble...",
              'color': Colors.RED, 'sleep': 2},
         ]},
     ]},

    {'name': CAPTAIN_HOLE, 'hp': 50,
     'weapons': [weapons.RIFLE, weapons.HARPOON, weapons.KNIFE, weapons.PISTOL],
     'bounty': 0, 'type': BOSS, 'preamble': [
        {'text': "Captain Hole has offered to shoot himself in the jines in exchange for your Tench Filet",
        'sleep': 4}
    ]}
]

# ========================
#        FINAL BOSS
# ========================
Final_Boss = {'name': DENNY_BILTMORE, 'hp': 275,
              'weapons': [weapons.BRASS_KNUCKLES, weapons.PISTOL, weapons.REVOLVER, weapons.SHOTGUN],
              'bounty': 0, 'type': FINAL_BOSS}
