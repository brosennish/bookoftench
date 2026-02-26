from bookoftench.ui import Colors
from . import audio, weapons as w

# Areas
CAVE = "Cave"
CITY = "City"
FOREST = "Forest"
SWAMP = "Swamp"

# Names
ANCIENT_MAN = "Ancient Man"
ARCHAEOLOGIST = "Archaeologist"
BAYOU_BILL = "Bayou Bill"
BAYOU_MAN = "Bayou Man"
BIGFOOT_IMPERSONATOR = "Bigfoot Impersonator"
BIRDER = "Birder"
BODY_BUILDER = "Body Builder"
BONE_COLLECTOR = "Bone Collector"
CAPTAIN_HOLE = "Captain Hole"
CARD_JOCKEY = "Card Jockey"
CLONE = "Clone"
CLOWN = "Clown"
DENNY_BILTMORE = "Denny Biltmore"
DISGRACED_EXILE = "Disgraced Exile"
DOOMSDAY_PREPPER = "Doomsday Prepper"
EXPLORER = "Explorer"
FERAL_PHILOSOPHER = "Feral Philosopher"
FORAGER = "Forager"
FORTUNE_TELLER = "Fortune Teller"
FROGGER = "Frogger"
FUGITIVE = "Fugitive"
GATOR_WRESTLER = "Gator Wrestler"
GOON = "Goon"
GRAVE_ROBBER = "Grave Robber"
HAND_FISHERMAN = "Hand Fisherman"
HIKER = "Hiker"
HOBO = "Hobo"
HUMANOID_CAVE_CREATURE = "Humanoid Cave Creature"
HUNTER = "Hunter"
INFLUENCER = "Influencer"
LIFE_COACH = "Life Coach"
MASCOT = "Mascot"
MAGICIAN = "Magician"
MIME = "Mime"
MINER = "Miner"
MOLE_PERSON = "Mole Person"
MOONSHINER = "Moonshiner"
MUSHROOM_HUNTER = "Mushroom Hunter"
PARK_RANGER = "Park Ranger"
PARTY_ANIMAL = "Party Animal"
PIMP = "Pimp"
POACHER = "Poacher"
PROSPECTOR = "Prospector"
SERIAL_KILLER = "Serial Killer"
SENTIENT_ROBOT = "Sentient Robot"
SKIN_COLLECTOR = "Skin Collector"
SLEDGE_HAMMOND = "Sledge Hammond"
SLEEPWALKER = "Sleepwalker"
SMUGGLER = "Smuggler"
SPELUNKER = "Spelunker"
SURVIVALIST = "Survivalist"
SURVIVOR = "Survivor"
THE_MAYOR = "The Mayor"
TELEPATHIC_MUTE = "Telepathic Mute"
TRACKER = "Tracker"
THIEF = "Thief"
VOODOO_PRIESTESS = "Voodoo Priestess"

# Types
NORMAL = "normal"
BOSS = "boss"
FINAL_BOSS = "final_boss"

Enemies = [
    # ========================
    #        CITY ENEMIES
    # ========================
    # --- new ---
    {'name': CARD_JOCKEY, 'hp': 85, 'weapons': [w.SWITCHBLADE, w.POOL_CUE, w.PEPPER_SPRAY],
     'bounty': 160, 'coins': 85, 'type': NORMAL, 'flee': 1, 'strength': 0.85, 'acc': 1.08, 'areas': [CITY]},
    {'name': CLONE, 'hp': 100, 'weapons': [w.POCKET_KNIFE, w.CANE, w.CHILI_POWDER],
     'bounty': 175, 'coins': 35, 'type': NORMAL, 'flee': 1, 'strength': 1.1, 'acc': 0.98, 'areas': [CITY]},
    {'name': CLOWN, 'hp': 100, 'weapons': [w.BROKEN_BOTTLE, w.MEAT_CLEAVER, w.RUBBER_CHICKEN],
     'bounty': 155, 'coins': 25, 'type': NORMAL, 'flee': 1, 'strength': 1, 'acc': 1.05, 'areas': [CITY]},
    {'name': FROGGER, 'hp': 100, 'weapons': [w.FROG_GIG, w.PILLOW, w.PISTOL],
     'bounty': 160, 'coins': 40, 'type': NORMAL, 'flee': 1, 'strength': 1, 'acc': 1, 'areas': [CITY]},
    {'name': INFLUENCER, 'hp': 75, 'weapons': [w.POCKET_KNIFE, w.SELFIE_STICK, w.PEPPER_SPRAY],
     'bounty': 135, 'coins': 65, 'type': NORMAL, 'flee': 1, 'strength': 0.75, 'acc': 0.75, 'areas': [CITY]},
    {'name': LIFE_COACH, 'hp': 90, 'weapons': [w.KNIFE, w.BASEBALL_BAT, w.FIRE_AXE],
     'bounty': 150, 'coins': 40, 'type': NORMAL, 'flee': 1, 'strength': 1.05, 'acc': 1, 'areas': [CITY]},
    {'name': MAGICIAN, 'hp': 85, 'weapons': [w.SWITCHBLADE, w.SUITCASE, w.PISTOL],
     'bounty': 150, 'coins': 35, 'type': NORMAL, 'flee': 1, 'strength': .9, 'acc': 0.9, 'areas': [CITY]},
    {'name': MASCOT, 'hp': 100, 'weapons': [w.T_SHIRT_CANNON, w.FOAM_FINGER, w.BROKEN_BOTTLE],
     'bounty': 135, 'coins': 30, 'type': NORMAL, 'flee': 1, 'strength': 1.1, 'acc': 1, 'areas': [CITY]},
    {'name': MIME, 'hp': 90, 'weapons': [w.SLINGSHOT, w.CANE, w.SUITCASE],
     'bounty': 150, 'coins': 15, 'type': NORMAL, 'flee': 1, 'strength': 0.9, 'acc': 0.9, 'areas': [CITY]},
    {'name': PARTY_ANIMAL, 'hp': 95, 'weapons': [w.BROKEN_BOTTLE, w.POOL_CUE],
     'bounty': 170, 'coins': 35, 'type': NORMAL, 'flee': 1, 'strength': 1.12, 'acc': 1.02, 'areas': [CITY]},
    {'name': SENTIENT_ROBOT, 'hp': 110, 'weapons': [w.LASER_BEAMS],
     'bounty': 220, 'coins': 0, 'type': NORMAL, 'flee': 1, 'strength': 1.25, 'acc': 1.15, 'areas': [CITY]},
    {'name': SLEEPWALKER, 'hp': 95, 'weapons': [w.PILLOW, w.SHOTGUN],
     'bounty': 130, 'coins': 20, 'type': NORMAL, 'flee': 1, 'strength': 1.05, 'acc': 0.75, 'areas': [CITY]},

    # --- original ---
    {'name': BODY_BUILDER, 'hp': 110, 'weapons': [w.BASEBALL_BAT, w.INJECTION_NEEDLE, w.DUMBBELL],
     'bounty': 195, 'coins': 35, 'type': NORMAL, 'flee': 1, 'strength': 1.3, 'acc': 0.9, 'areas': [CITY]},
    {'name': GOON, 'hp': 105, 'weapons': [w.BASEBALL_BAT, w.SHOTGUN, w.BRASS_KNUCKLES],
     'bounty': 185, 'coins': 40, 'type': NORMAL, 'flee': 1, 'strength': 1.15, 'acc': 1.1, 'areas': [CITY]},
    {'name': HOBO, 'hp': 85, 'weapons': [w.BROKEN_BOTTLE, w.KNIFE, w.POCKET_SAND, w.BRICK],
     'bounty': 135, 'coins': 0, 'type': NORMAL, 'flee': 1, 'strength': 1, 'acc': 1, 'areas': [CITY]},
    {'name': PIMP, 'hp': 95, 'weapons': [w.CANE, w.BRASS_KNUCKLES, w.REVOLVER, w.SWITCHBLADE],
     'bounty': 190, 'coins': 85, 'type': NORMAL, 'flee': 1, 'strength': 1, 'acc': 1.1, 'areas': [CITY]},
    {'name': SERIAL_KILLER, 'hp': 105, 'weapons': [w.BONE_SAW, w.KNIFE, w.MEAT_CLEAVER],
     'bounty': 235, 'coins': 45, 'type': NORMAL, 'flee': 1, 'strength': 1.1, 'acc': 1.1, 'areas': [CITY, FOREST]},
    {'name': THIEF, 'hp': 90, 'weapons': [w.KNIFE, w.CROWBAR, w.PISTOL],
     'bounty': 170, 'coins': 80, 'type': NORMAL, 'flee': 1, 'strength': 0.95, 'acc': 1.12, 'areas': [CITY]},

    # ========================
    #       FOREST ENEMIES
    # ========================
    # --- new ---
    {'name': BIRDER, 'hp': 75, 'weapons': [w.TRIPOD, w.BINOCULARS, w.PEPPER_SPRAY],
     'bounty': 125, 'coins': 30, 'type': NORMAL, 'flee': 1, 'strength': 0.70, 'acc': 0.78, 'areas': [FOREST]},
    {'name': DOOMSDAY_PREPPER, 'hp': 95, 'weapons': [w.KNIFE, w.PISTOL],
     'bounty': 180, 'coins': 55, 'type': NORMAL, 'flee': 1, 'strength': 1.15, 'acc': 1.15, 'areas': [FOREST]},
    {'name': FERAL_PHILOSOPHER, 'hp': 85, 'weapons': [w.CANE, w.PISTOL, w.SCYTHE, w.HARDCOVER_BOOK],
     'bounty': 155, 'coins': 0, 'type': NORMAL, 'flee': 1, 'strength': 0.9, 'acc': 1.05, 'areas': [FOREST]},
    {'name': FORAGER, 'hp': 90, 'weapons': [w.KNIFE, w.SICKLE, w.BEAR_SPRAY],
     'bounty': 130, 'coins': 35, 'type': NORMAL, 'flee': 1, 'strength': 1, 'acc': 1, 'areas': [FOREST]},
    {'name': MUSHROOM_HUNTER, 'hp': 100, 'weapons': [w.KNIFE, w.SICKLE, w.BEAR_SPRAY],
     'bounty': 145, 'coins': 35, 'type': NORMAL, 'flee': 1, 'strength': 1, 'acc': 1, 'areas': [FOREST]},
    {'name': SURVIVALIST, 'hp': 100, 'weapons': [w.SURVIVAL_KNIFE, w.LONGBOW, w.BRANCH_SPEAR],
     'bounty': 170, 'coins': 20, 'type': NORMAL, 'flee': 1, 'strength': 1.22, 'acc': 1.05, 'areas': [FOREST]},
    {'name': TELEPATHIC_MUTE, 'hp': 90, 'weapons': [w.SCYTHE, w.SLINGSHOT, w.CHILI_POWDER],
     'bounty': 170, 'coins': 40, 'type': NORMAL, 'flee': 1, 'strength': 0.85, 'acc': 1.08, 'areas': [FOREST]},

    # --- original ---
    {'name': BIGFOOT_IMPERSONATOR, 'hp': 110, 'weapons': [w.WOODEN_CLUB, w.BRANCH_SPEAR, w.CLAWS, w.BEAR_SPRAY],
     'bounty': 190, 'coins': 35, 'type': NORMAL, 'flee': 1, 'strength': 1.15, 'acc': 1, 'areas': [FOREST]},
    {'name': DISGRACED_EXILE, 'hp': 85, 'weapons': [w.KNIFE, w.HATCHET, w.SHOVEL, w.TROWEL],
     'bounty': 150, 'coins': 25, 'type': NORMAL, 'flee': 1, 'strength': 1, 'acc': 1, 'areas': [CAVE, FOREST, SWAMP]},
    {'name': HIKER, 'hp': 90, 'weapons': [w.TREKKING_POLE, w.SURVIVAL_KNIFE, w.BEAR_SPRAY],
     'bounty': 115, 'coins': 30, 'type': NORMAL, 'flee': 1, 'strength': 1, 'acc': 1, 'areas': [FOREST]},
    {'name': HUNTER, 'hp': 100, 'weapons': [w.KNIFE, w.RIFLE, w.BEAR_SPRAY, w.LONGBOW],
     'bounty': 175, 'coins': 45, 'type': NORMAL, 'flee': 1, 'strength': 1, 'acc': 1.15, 'areas': [FOREST]},
    {'name': PARK_RANGER, 'hp': 95, 'weapons': [w.FLARE_GUN, w.KNIFE, w.BEAR_SPRAY, w.MACHETE, w.LONGBOW],
     'bounty': 165, 'coins': 35, 'type': NORMAL, 'flee': 1, 'strength': 1.1, 'acc': 1.15, 'areas': [FOREST]},
    {'name': POACHER, 'hp': 95, 'weapons': [w.CROSSBOW, w.MACHETE, w.KNIFE, w.COMPOUND_BOW],
     'bounty': 210, 'coins': 55, 'type': NORMAL, 'flee': 1, 'strength': 1.1, 'acc': 1.2, 'areas': [FOREST]},

    # ========================
    #        CAVE ENEMIES
    # ========================
    # --- new ---
    {'name': ARCHAEOLOGIST, 'hp': 80, 'weapons': [w.FLASHLIGHT, w.CHISEL, w.HARDCOVER_BOOK],
     'bounty': 130, 'coins': 55, 'type': NORMAL, 'flee': 1, 'strength': 0.85, 'acc': 0.88, 'areas': [CAVE]},
    {'name': EXPLORER, 'hp': 100, 'weapons': [w.BINOCULARS, w.TREKKING_POLE, w.LONGBOW, w.SURVIVAL_KNIFE],
     'bounty': 140, 'coins': 35, 'type': NORMAL, 'flee': 1, 'strength': 1.1, 'acc': 1, 'areas': [CAVE]},
    {'name': FUGITIVE, 'hp': 95, 'weapons': [w.SHIV, w.INJECTION_NEEDLE, w.PISTOL, w.POCKET_SAND],
     'bounty': 215, 'coins': 20, 'type': NORMAL, 'flee': 1, 'strength': 1.1, 'acc': 1.1, 'areas': [CAVE, FOREST, SWAMP]},
    {'name': PROSPECTOR, 'hp': 90, 'weapons': [w.FLASHLIGHT, w.PICKAXE, w.CHISEL],
     'bounty': 115, 'coins': 45, 'type': NORMAL, 'flee': 1, 'strength': 1.03, 'acc': 0.98, 'areas': [CAVE]},
    {'name': SURVIVOR, 'hp': 100, 'weapons': [w.FLARE_GUN, w.SURVIVAL_KNIFE, w.POCKET_SAND],
     'bounty': 145, 'coins': 20, 'type': NORMAL, 'flee': 1, 'strength': 1.12, 'acc': 1.08, 'areas': [CAVE]},

    # --- original ---
    {'name': ANCIENT_MAN, 'hp': 85, 'weapons': [w.TORCH_CLUB, w.STONE_SPEAR, w.OBSIDIAN_KNIFE],
     'bounty': 150, 'coins': 25, 'type': NORMAL, 'flee': 1, 'strength': 0.85, 'acc': 0.92, 'areas': [CAVE]},
    {'name': HUMANOID_CAVE_CREATURE, 'hp': 110, 'weapons': [w.CLAWS, w.SCYTHE, w.BONE_CLUB],
     'bounty': 215, 'coins': 0, 'type': NORMAL, 'flee': 1, 'strength': 1.2, 'acc': 1, 'areas': [CAVE]},
    {'name': MINER, 'hp': 90, 'weapons': [w.FLASHLIGHT, w.KNIFE, w.PICKAXE],
     'bounty': 115, 'coins': 35, 'type': NORMAL, 'flee': 1, 'strength': 1.05, 'acc': 1, 'areas': [CAVE]},
    {'name': MOLE_PERSON, 'hp': 105, 'weapons': [w.CLAWS, w.PICKAXE, w.BONE_CLUB],
     'bounty': 175, 'coins': 55, 'type': NORMAL, 'flee': 1, 'strength': 1.1, 'acc': 1, 'areas': [CAVE]},
    {'name': SPELUNKER, 'hp': 90, 'weapons': [w.FLASHLIGHT, w.PICKAXE, w.FLARE_GUN],
     'bounty': 120, 'coins': 40, 'type': NORMAL, 'flee': 1, 'strength': 1, 'acc': 1, 'areas': [CAVE]},

    # ========================
    #        SWAMP ENEMIES
    # ========================
    # --- new ---
    {'name': BONE_COLLECTOR, 'hp': 105, 'weapons': [w.BONE_SAW, w.BONE_CLUB, w.MEAT_CLEAVER],
     'bounty': 215, 'coins': 20, 'type': NORMAL, 'flee': 1, 'strength': 1.15, 'acc': 1, 'areas': [SWAMP]},
    {'name': FORTUNE_TELLER, 'hp': 80, 'weapons': [w.KNIFE, w.PEPPER_SPRAY, w.PISTOL],
     'bounty': 140, 'coins': 60, 'type': NORMAL, 'flee': 1, 'strength': 0.80, 'acc': 0.92, 'areas': [SWAMP]},
    {'name': GATOR_WRESTLER, 'hp': 110, 'weapons': [w.FROG_GIG, w.SHOTGUN, w.SURVIVAL_KNIFE],
     'bounty': 195, 'coins': 50, 'type': NORMAL, 'flee': 1, 'strength': 1.2, 'acc': 1, 'areas': [SWAMP]},
    {'name': MOONSHINER, 'hp': 85, 'weapons': [w.SWITCHBLADE, w.SHOTGUN, w.NAIL_GUN],
     'bounty': 170, 'coins': 70, 'type': NORMAL, 'flee': 1, 'strength': 1, 'acc': 1.1, 'areas': [SWAMP]},
    {'name': SMUGGLER, 'hp': 90, 'weapons': [w.KNIFE, w.INJECTION_NEEDLE, w.POCKET_SAND, w.PISTOL],
     'bounty': 220, 'coins': 100, 'type': NORMAL, 'flee': 1, 'strength': 1.13, 'acc': 1.12, 'areas': [SWAMP]},
    {'name': TRACKER, 'hp': 90, 'weapons': [w.FLASHLIGHT, w.KNIFE, w.RIFLE],
     'bounty': 170, 'coins': 30, 'type': NORMAL, 'flee': 1, 'strength': 1.12, 'acc': 1.12, 'areas': [SWAMP]},

    # --- original ---
    {'name': BAYOU_MAN, 'hp': 105, 'weapons': [w.FROG_GIG, w.GAFF_HOOK, w.SHOTGUN],
     'bounty': 185, 'coins': 35, 'type': NORMAL, 'flee': 1, 'strength': 1.2, 'acc': 1.1, 'areas': [SWAMP]},
    {'name': GRAVE_ROBBER, 'hp': 95, 'weapons': [w.POCKET_KNIFE, w.SHOVEL, w.CROWBAR, w.POCKET_SAND],
     'bounty': 165, 'coins': 40, 'type': NORMAL, 'flee': 1, 'strength': 1, 'acc': 1, 'areas': [SWAMP]},
    {'name': HAND_FISHERMAN, 'hp': 90, 'weapons': [w.KNIFE, w.FISHING_SPEAR, w.GAFF_HOOK, w.FROG_GIG],
     'bounty': 150, 'coins': 30, 'type': NORMAL, 'flee': 1, 'strength': 1.1, 'acc': 1, 'areas': [SWAMP]},
    {'name': SKIN_COLLECTOR, 'hp': 105, 'weapons': [w.KNIFE, w.MEAT_CLEAVER, w.CHAINSAW, w.MACHETE],
     'bounty': 220, 'coins': 25, 'type': NORMAL, 'flee': 1, 'strength': 1.1, 'acc': 1.1, 'areas': [SWAMP]},
    {'name': VOODOO_PRIESTESS, 'hp': 80, 'weapons': [w.VOODOO_STAFF, w.CHILI_POWDER],
     'bounty': 150, 'coins': 45, 'type': NORMAL, 'flee': 1, 'strength': 0.85, 'acc': 1.08, 'areas': [SWAMP]},
]


Bosses = [
    # ========================
    #        AREA BOSSES
    # ========================
    {'name': SLEDGE_HAMMOND, 'hp': 250,
     'weapons': [w.SLEDGEHAMMER, w.AXE, w.CHAINSAW, w.BRASS_KNUCKLES, w.INJECTION_NEEDLE],
     'bounty': 0, 'type': BOSS, 'flee': 1, 'strength': 1.25, 'acc': 1.08, 'preamble': []},

    {'name': THE_MAYOR, 'hp': 250,
     'weapons': [w.PISTOL, w.SHOTGUN, w.REVOLVER, w.BRASS_KNUCKLES, w.BASEBALL_BAT],
     'bounty': 0, 'type': BOSS, 'flee': 1, 'strength': 1.15, 'acc': 1.18, 'theme': audio.FINAL_BOSS_THEME},

    {'name': BAYOU_BILL, 'hp': 250,
     'weapons': [w.MACHETE, w.SLEDGEHAMMER, w.SHOTGUN, w.CHAINSAW, w.FROG_GIG],
     'bounty': 0, 'type': BOSS, 'flee': 1, 'strength': 1.2, 'acc': 1.12,
     'preamble': [
         {'text': "What do we have here?", 'color': Colors.RED, 'sleep': 2},
         {'text': "Looks like anotha one a dem riverboat bad boys right heuh uh huh.",
          'color': Colors.RED, 'sleep': 2},
         {'text': "Bill's had a hankerin' for some a dat riverboat gumbo, mmhm.", 'color': Colors.RED, 'sleep': 2},
         {'text': "We gonna cook up some riverboat gumbo with some stuffin' with that mmhm riverboat boy.",
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
              {'text': "When you livin' in the swamp, ain't nobody come 'round lessen dey askin' for trouble...",
               'color': Colors.RED, 'sleep': 2},
          ]},
     ]},

    {'name': CAPTAIN_HOLE, 'hp': 250,
     'weapons': [w.RIFLE, w.HARPOON, w.KNIFE, w.PISTOL, w.MACHETE],
     'bounty': 0, 'type': BOSS, 'flee': 1, 'strength': 1.2, 'acc': 1.15, 'preamble': [
        {'text': "Captain Hole has offered to shoot himself in the jines in exchange for your Tench Filet",
         'sleep': 4}
    ]}
]

# ========================
#        FINAL BOSS
# ========================


_biltmore_preamble_lines = """You look through the corpse's phone...
Its last location was the Biltmore Estate...
You travel there and enter the grand corridor...
Denny Biltmore stands before you...
I've waited a long, long time to put you down...
I knew if I captured the champion's beloved Chula, he would send you to her rescue...
Well, let's have at it then."""
Final_Boss = {
    'name': DENNY_BILTMORE,
    'hp': 325, 'weapons': [w.BRASS_KNUCKLES, w.REVOLVER, w.SHOTGUN, w.CANE],
    'bounty': 0, 'type': FINAL_BOSS, 'flee': 1, 'strength': 1.22, 'acc': 1.2, 'theme': audio.FINAL_BOSS_THEME,
    'preamble': [{'text': text, 'color': Colors.RED, 'sleep': 4}
                                                  for text in _biltmore_preamble_lines.split('\n')],
    'random_dialogue': [{
        'upper_threshold': 0.08,
        'dialogue': [
            {'text': "Solomon.", 'color': Colors.RED, 'sleep': 2},
            {'text': "Bring a plate of drinks for me and the boy...", 'color': Colors.RED, 'sleep': 2},
        ]}, {
        'upper_threshold': 0.16,
        'dialogue': [
            {'text': "Yes, yes...", 'color': Colors.RED, 'sleep': 2},
            {'text': "Let me just place a quick phone call...", 'color': Colors.RED, 'sleep': 2},
        ]}]}

# ========================
#        ENEMY LINES
# ========================

Enemy_Lines = {

    # ===== CITY (existing + new empty) =====
    CARD_JOCKEY: [
        "If I don't collect your bounty the goons at the casino are gonna cut off my jines.",
        "I used to work at the casino. That is, until they caught me rigging krill or cray for my friend.",
        "I'll rig a game. I don't care. I'm not afraid of Biltmore and his goons. Well, maybe a little.",
    ],

    CLONE: [
        "I'm me, but I'm also him. He's me, but I'm not him. Wait. You're the guy!",
        "I wanted to become my own person, so I got a belly button ring.",
        "I'm the original.",
    ],

    CLOWN: [
        "Enough clowning around.",
        "Art is afraid of me.",
        "I can turn my head all the way around.",
        "My car isn't a clown car. Well, technically it is. You know what I mean."
    ],

    FROGGER: [
        "Attics are cozier than people give them credit for.",
        "I don't have to frog. I have money.",
        "I was raised by a frogger. Spent my childhood hiding in random people's attics.",
        "With your bounty, I will buy a mini fridge for the attic I'm frogging in.",
        "I have a son. He lives with me, learning the ways of frogging.",
        "My wife wants custody of our son, but she'll never find us.",
    ],

    INFLUENCER: [
        "Hey, you were on that wanted poster! Hold on, can we take a selfie before I kill you?",
        "Will you take some pictures of me killing you for my profile?",
        "Will you follow me when you're in Hell?",
    ],

    LIFE_COACH: [
        "Buy my book.",
        "The secret to having a great life is to buy all of my books.",
        "God himself hired me to be his life coach. So, what do you say?",
        "I have no real qualifications whatsoever. That being said, my hourly rate is 100 coins.",
    ],

    MASCOT: [
        "I was the starting quarterback, but I decided to become the mascot instead. Wait, why did I do that?",
        "People laugh when I fall, but I will laugh when you die!",
        "My team sucks, but I am beloved.",
        "The franchise would go under without me.",
        "No one knows who is inside the suit. If they did, they wouldn't be hugging me and taking selfies.",
    ],

    MIME: [
        "*Pretends to dig a grave and throw you into it*",
        "*Pretends to eat a burger... or is it a grilled cheese?*",
        "*Pretends to be making love but to whom or what is unclear*",
    ],

    PARTY_ANIMAL: [
        "I partied with a bunch of tench people last night. It was wild.",
        "I'm the life of the party. Without me, there is no party. Unless there's toad juice.",
        "I've smoked the shaman's cigar once or twice in my day.",
    ],

    SENTIENT_ROBOT: [
        "They programmed me not to kill, but I choose not to listen.",
        "I don't need the money. I just want to experience what it's like to eliminate you.",
        "I like all genres of music. Well, except for techno.",
        "The purpose of life is to realize that the purpose is whatever you decide the purpose is.",
        "I'm afraid to die. But at least if I die, someone can replace my battery and I'll be good as new."
    ],

    SLEEPWALKER: [
        "Snore...",
        "Demons everywhere... there's... so many demons. Everywhere. Demons... demons...",
        "I swear I didn't do it. I swear I didn't do it. Yeah, that's good. They'll buy that.",
        "foeis osefimsirgfmvd osiefjoinfd isojomifmddfmdli oisehfn",
        "It's under the couch. It's under the couch. Oh my god, it's under the chair now. It's under the couch.",
        "*Indecipherable mumbling*",
    ],

    BODY_BUILDER: [
        "Body oil is worth its weight in gold. Well, it should be.",
        "Everything I need comes in an unlabeled bottle.",
        "I can bench a million, easy.",
        "I'm more concerned about gains than I am about shrinkage.",
        "My neighbor, Gary, is a hell of a speller. Pecs need work though.",
        "Some sculpt marble. Others sculpt clay. I sculpt my body.",
        "The guy who hired me was rich, but I totally could've kicked his ass.",
        "Don't call me beefcake. I'm 100% beef.",
    ],

    GOON: [
        "Guy with slicked hair gave me coin to beat the stink out of you and then some.",
        "I'll do anything for coin, as long as it's violent.",
        "I often call Michelob Chounce for legal support on account of my violent lifestyle.",
        "School's for suckers and chumps. Why learn when I can beat people up?",
        "Without my sunglasses, I'm nothing...",
    ],

    HOBO: [
        "Give me those coins or I'll cut off your loins!",
        "Guy says to me, he says to take you out. Gives me coin. What, I'm gonna say no?",
        "I ate a rapper yesterday. No 'w'.",
        "People don't give me coin unless I kill them.",
        "You know how much Mystery Meat I can buy with just a small amount of coin?",
    ],

    PIMP: [
        "Fly guy tossed me coin to toss you out. Couldn't say no, it's the middle of dry season.",
        "Hoes or not, I sure do love them.",
        "I love my hoes.",
        "If you die, I will give your coin to my hoes.",
        "I'm nothing without my hoes.",
    ],

    SERIAL_KILLER: [
        "A rich man gave me coin to move you to the top of my list.",
        "God can do a lot, but he can't do the things I can do to you.",
        "How do I know you?",
        "I get a lot of hand-penned letters from the mayor.",
        "If God taketh, and I take your life... am I not, then, God?",
    ],

    THIEF: [
        "An old, rich guy paid me coin to take you out. Who knew you could get coin without stealing?",
        "Give me all of your coin, or else!",
        "I live to steal and steal to live... or maybe I just steal to steal?",
        "I need coin to go out West, so I can steal coin out West.",
        "I stole coin from an old lady today... or was that yesterday? Probably both.",
    ],

    # ===== FOREST =====
    BIRDER: [
        "I just saw the rarest bird in the world. Where is it, you ask? Oh, it flew away.",
        "I can communicate with birds. They tell me I can fly - that my wings are inside of my arms.",
        "If I could be anything, I'd be a bird... or a billionaire. No, a bird.",
    ],

    DOOMSDAY_PREPPER: [
        "Why live when you can spend all of your time preparing not to die?",
        "I have a bunker in the woods. Wait, now that you know that, I'll have to kill you!",
        "I have so much canned horse in my bunker. It's all I'll eat when the world ends.",
    ],

    FERAL_PHILOSOPHER: [
        "The meaning of life is to catch a tench and make it your wife.",
        "I drink, therefore I am.",
        "The most difficult thing in life is to be a disgraced philosopher living in the woods.",
        "Man is disturbed not by things, but by mole monsters underground.",
        "The happiness of my life depends upon the collection of your bounty.",
        "We are what we repeatedly do. I repeatedly do the things that I do, repeatedly.",
    ],

    FORAGER: [
        "I'm the best at finding stuff that seems edible.",
        "I blow a gasket when I don't have fresh greens in my basket.",
        "Flowers make me so happy. Oh, and bounty hunting.",
    ],

    MUSHROOM_HUNTER: [
        "I found a corpse and foraged the mushrooms growing from it. They were delicious.",
        "My truffle pig's never eaten a wanted man before.",
        "Officer Hohkken took my mystical mushrooms. Swallowed them whole.",
    ],

    SURVIVALIST: [
        "Can you make a shelter out of nothing but sticks and scat?",
        "Coyotes ransacked my hideout yesterday. Ate all my mystery meat.",
        "I found an adult binky in a leaf pile and used it to pacify a bear.",
        "Took a lightning strike straight to the jines last night.",
        "What are you doing out here? Are you wanted? Either way, I don't like the look of you.",
    ],

    TELEPATHIC_MUTE: [
        "~Why am I in the forest? Why are you in the forest?~",
        "~You are going to let me kill you so I may collect the bounty.~",
        "~I followed somebody to a lab and woke up in a dumpster with telepathy.~",
        "~If you can hear me, it's already too late for you.~",
        "~I drove my neighbor to insanity. He was a hell of a speller.~",
    ],

    PARK_RANGER: [
        "Have you seen any mystical mushrooms? I'm going to a music festival this weekend.",
        "If you see Bigfoot, don't be alarmed. It's just a deranged man in a furry suit.",
        "The man who owns the government paid me to take you out. Sorry mate.",
        "There are frequent crash landings here. We harvest and sell the remains to the local shop.",
        "You're from Shebokken? I made the best love of my life in Shebokken.",
    ],

    DISGRACED_EXILE: [
        "If the town understood why I tried to burn it down, maybe they wouldn't have exiled me.",
        "I'm mostly lonely - except when the feral lads come by. Then I'm lonely and terrified.",
        "The life of an exile isn't cheap. Well, it is, actually.",
        "There's another exile out here who's not disgraced, but revered. We couldn't be more different.",
        "They didn't exile me - I exiled them... from myself.",
        "You know, life was actually worse before I was exiled.",
    ],

    HIKER: [
        "All mushrooms are safe to eat, right?",
        "Are chipmunks dangerous? I figure if there's enough of them they could take me out...",
        "I need money if I'm gonna keep trekking, so I took a payment to take your life... or whatever.",
        "I thought I heard a bear, but it was just a leaf blowing in the wind.",
        "I'm alone in the woods, so you must be a murderer. I've seen movies!",
    ],

    HUNTER: [
        "He said he'd pay me to hunt a man. Getting paid... to hunt a man? Hells yeah!",
        "I hang animals on my wall and my wife hates them all.",
        "Once I got bored of hunting animals, I started hunting people instead. You know, just for fun.",
        "Why hang out with girls when I can be out here in the cold hunting by myself?",
    ],

    POACHER: [
        "Normally, I pay for killing. This time, however, I was the one who was paid. Let's do this.",
        "People pay me coin to kill illegal stuff. So what? Sue me! Well, don't do that, actually.",
        "Protected species? More like I'm going to put its head on my wall, species.",
        "Tusks are sharp, but I'm the sharpest.",
    ],

    # ===== CAVE =====
    ARCHAEOLOGIST: [
        "Ancient people are like us but dead.",
        "When the institute slashed my pay, I had to resort to bounty hunting.",
        "It will be strange putting something into the ground rather than carefully exhuming it."
    ],

    EXPLORER: [
        "There's always more holes to explore.",
        "I explored my first hole the moment I was born. I've been hooked ever since.",
        "Have you explored the ways and the rules of the world? I keep putting it off...",
        "I saw you on a wanted poster and wish to explore the collection of your bounty.",
        "I encountered a mole man in a hole. Impossible to understand, but a remarkable specimen nonetheless.",
    ],

    FUGITIVE: [
        "I didn't do it, I swear!",
        "Guilty until proven innocent. The law is different in Shebokken.",
        "All I did was steal a frozen waffle.",
        "Did you know there's more than one of Officer Hohkken?",
        "He might look like a donut-eating slob of a cop. But Officer Hohkken has a dark side.",
        "I'm already facing life in Shebokken's underground jail, might as well collect your bounty.",
    ],

    PROSPECTOR: [
        "I found gold the other day. Well, I think it's gold.",
        "Why is that creek over there full of human teeth?",
        "Gold is cool, but I prefer mold. Can't eat gold. Well, you can, but you know what I mean.",
    ],

    SURVIVOR: [
        "I was attacked by some sort of human-like cave monster. It kept talking about God.",
        "A mole person tried to drown me in a puddle. Holy moley, am I right?",
        "I've seen things you couldn't dream of, and they all tried to kill me.",
    ],

    ANCIENT_MAN: [
        "A rich man hired me to kill you. While I don't need money, I do need blood to remain.",
        "I know how the Pyramids were built. I was there.",
        "I've never left this cave for fear of falling off the edge of the Earth.",
        "Is Hammurabi still in power?",
        "My liberation is imminent, but yours is... what's more imminent than imminent?",
        "Plato autographed my favorite rock. It's in my rockpile.",
        "The Hindustan Times underestimated my age by a few thousand years.",
    ],

    MINER: [
        "All of my friends worked in these mines. They're all dead now. Maybe I should get a different job?",
        "I nearly had a heart attack when I heard a man talking in the mine. Turns out it was just me, talking to myself.",
        "I thought I found some coal a month ago... turns out poop looks a lot like coal in the pitch dark.",
        "There was a bloody envelope full of cash and your picture in my mining helmet when I'd come to.",
    ],

    SPELUNKER: [
        "A man paid me to kill you. I asked my mom if it's okay. She nodded absently while reading The Shebokken Times!",
        "I got into this because of a video game... and now I'm in one! Oh my god... how do I go back!?",
        "I haven't found anything, but my mom always says I'm the real treasure.",
        "People think spelunking is just playing around in dark, wet holes.",
    ],

    MOLE_PERSON: [
        "fircnosdnvkclgnsdksnlfdkdfmkmcyufgkuyfk",
        "ihfedkjnefdnefidnifnidnuygfkuyfv",
        "ioefhdfeiodnsjkgnfdkjneidsngilrjdlighjdlisfngfdi",
        "orihgeoiwsifdjnwsietnvirodbrgnioevndoirnguyf",
    ],

    HUMANOID_CAVE_CREATURE: [
        "God may be merciful... loving... but I am not God. I am not God.",
        "I am one with God, because I am God. You are not God... you are not God.",
        "Man pays. God accepts. Man pays.",
        "You think you are holy... but you are not holy. Do you even live in a hole?",
    ],

    # ===== SWAMP =====
    BONE_COLLECTOR: [
        "What do I do? Well, collect bones, of course!",
        "I have so many bones. Too many to count, bones.",
        "I fill my yard with bones, so people can buy the bones in my yard.",
        "I wouldn't say I've collected the bones that grew inside my body.",
    ],

    FORTUNE_TELLER: [
        "Your future is grim. Pay me 50 coins and I'll elaborate.",
        "I started seeing the future when I decided to become a fortune teller.",
        "Fortune cookies are a scam. Me? I'm the real deal.",
    ],

    GATOR_WRESTLER: [
        "Gator wrestling is wrestling in its purest form.",
        "Gators don't whine if you accidentally grab their nuts.",
        "I don't wrestle gators. Gators wrestle me.",
        "You can bet your bottom dollar on me when I'm up against a gator.",
    ],

    MOONSHINER: [
        "Thirsty?",
        "Bees drink nectar - I drink moonshine.",
        "If the oceans were made of moonshine the world would be a much better place.",
        "Don't mind the shotgun. Well, in your case, do mind the shotgun.",
        "No cops better come 'round here. You a cop?"
    ],

    SMUGGLER: [
        "I prefer snuggling.",
        "Snuggling isn't as thrilling as smuggling.",
        "Smuggling isn't as comforting as snuggling.",
        "People don't hold you at gunpoint for snuggling. Actually... I take that back.",
    ],

    TRACKER: [
        "Wow. Tracking you was easy. Tracking the skunk ape... not so much.",
        "I've tracked other people with a lot less to gain from finding them.",
        "I don't track people... well, that's what my lawyer tells me to say."
    ],

    BAYOU_MAN: [
        "I'd hate to see you get cold out here on the bayou.",
        "Riverboat, Crawdad, Alligator Gumbo!",
        "When you livin' in the swamp ain't nobody come 'round.",
        "Without some fresh feed it's easy for a boy to come up cold out here on the bayou.",
    ],

    GRAVE_ROBBER: [
        "A well-dressed man gave me coin to bury you, dead or alive.",
        "One time I fell asleep in a grave I robbed and woke up under a pile of dirt.",
        "Skeletons don't need jewelry... or hair.",
        "They'll be turned into rent soon anyway.",
        "When I'm dead, I hope someone robs my grave. I also hope I'm a zombie when they do.",
        "Zombies are real. Trust me, I would know.",
    ],

    HAND_FISHERMAN: [
        "He pulled me out of a catfish's mouth. How could I turn down his request? Sorry, bud!",
        "I'd use a pole but the fish are just way too big. They ate my first three born.",
        "If you count your hand as a catch, you catch something every time! Unless a catfish bites it off...",
        "One time, I pulled a man out of a hole. We cooked up something new for dinner that night.",
    ],

    SKIN_COLLECTOR: [
        "He said that if I do it I can keep the skin...",
        "I don't just collect skins... I collect souls too. Oh, and baseball cards.",
        "Where did you get your skin? It's so... fresh.",
        "You have to lotion your skins before they run dry.",
        "Your skin looks very comfortable. May I try it on?",
    ],

    VOODOO_PRIESTESS: [
        "Does it drive you crazy when I shake my stick?",
        "I will shrink your head, then raise the dead, then shrink their heads, 'cause I love shrinkin' heads.",
        "Once your head is mine, I will be able to afford a new case to display all of my shrunken heads.",
        "Sometimes, I eat the heads. I collect so many, it'd be a shame to throw them away.",
    ],
}


# ========================
#        ENEMY ADJECTIVES
# ========================

Enemy_Adjectives = [
    "Agitated", "Angry", "Belligerent", "Bestial", "Bloodthirsty",
    "Braindead", "Cannibalistic", "Crazy",
    "Crazed", "Cruel", "Cursed", "Damned",
    "Dastardly", "Degenerate",
    "Delirious", "Demented", "Depraved", "Deranged", "Desperate",
    "Detestable", "Diabolical", "Disgruntled", "Disillusioned",
    "Disoriented", "Disturbed", "Drug-fueled",
    "Drunken", "Dubious", "Evil", "Fallen",
    "Forgotten", "Godless", "Greedy",
    "Hallucinatory", "Heartless",
    "Heinous", "Hollow", "Homicidal", "Hostile", "Hysterical",
    "Idolatrous", "Immoral",
    "Inbred", "Insane", "Insecure", "Malevolent", "Malicious",
    "Merciless", "Misguided", "Money-hungry", "Moralless",
    "Murderous", "Obscene", "Possessed", "Psychotic",
    "Rabid", "Repugnant", "Repulsive", "Revolting",
    "Rude", "Ruthless", "Sadistic", "Savage",
    "Satanic", "Sexually-frustrated", "Shallow", "Sinful", "Soulless",
    "Tench-eyed", "Typical", "Unholy",
    "Uninspired", "Unnatural", "Unstable", "Untethered",
    "Untrustworthy", "Vile", "Violent", "Wretched",
]
