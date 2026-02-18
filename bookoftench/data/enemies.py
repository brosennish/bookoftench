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
     'bounty': 140, 'type': NORMAL, 'areas': [CITY]},
    {'name': CLONE, 'hp': 100, 'weapons': [w.POCKET_KNIFE, w.CANE, w.CHILI_POWDER],
     'bounty': 145, 'type': NORMAL, 'areas': [CITY]},
    {'name': CLOWN, 'hp': 95, 'weapons': [w.BROKEN_BOTTLE, w.MEAT_CLEAVER],
     'bounty': 135, 'type': NORMAL, 'areas': [CITY]},
    {'name': FROGGER, 'hp': 90, 'weapons': [w.FROG_GIG, w.PILLOW, w.PISTOL, w.POCKET_KNIFE],
     'bounty': 155, 'type': NORMAL, 'areas': [CITY]},
    {'name': INFLUENCER, 'hp': 75, 'weapons': [w.POCKET_KNIFE, w.SELFIE_STICK, w.PEPPER_SPRAY],
     'bounty': 75, 'type': NORMAL, 'areas': [CITY]},
    {'name': LIFE_COACH, 'hp': 85, 'weapons': [w.KNIFE, w.BASEBALL_BAT, w.FIRE_AXE],
     'bounty': 150, 'type': NORMAL, 'areas': [CITY]},
    {'name': MAGICIAN, 'hp': 80, 'weapons': [w.SWITCHBLADE, w.SUITCASE, w.PISTOL],
     'bounty': 140, 'type': NORMAL, 'areas': [CITY]},
    {'name': MASCOT, 'hp': 95, 'weapons': [w.T_SHIRT_CANNON, w.FOAM_FINGER, w.BROKEN_BOTTLE],
     'bounty': 145, 'type': NORMAL, 'areas': [CITY]},
    {'name': MIME, 'hp': 105, 'weapons': [w.SLINGSHOT, w.CANE, w.SUITCASE],
     'bounty': 155, 'type': NORMAL, 'areas': [CITY]},
    {'name': PARTY_ANIMAL, 'hp': 105, 'weapons': [w.BROKEN_BOTTLE, w.POOL_CUE],
     'bounty': 150, 'type': NORMAL, 'areas': [CITY]},
    {'name': SENTIENT_ROBOT, 'hp': 115, 'weapons': [w.LASER_BEAMS],
     'bounty': 190, 'type': NORMAL, 'areas': [CITY]},
    {'name': SLEEPWALKER, 'hp': 95, 'weapons': [w.PILLOW, w.SHOTGUN],
     'bounty': 160, 'type': NORMAL, 'areas': [CITY]},

    # --- original ---
    {'name': BODY_BUILDER, 'hp': 125, 'weapons': [w.BASEBALL_BAT, w.INJECTION_NEEDLE],
     'bounty': 190, 'type': NORMAL, 'areas': [CITY]},
    {'name': GOON, 'hp': 105, 'weapons': [w.BASEBALL_BAT, w.SHOTGUN, w.BRASS_KNUCKLES],
     'bounty': 185, 'type': NORMAL, 'areas': [CITY]},
    {'name': HOBO, 'hp': 85, 'weapons': [w.BROKEN_BOTTLE, w.KNIFE, w.POCKET_SAND],
     'bounty': 120, 'type': NORMAL, 'areas': [CITY]},
    {'name': PIMP, 'hp': 95, 'weapons': [w.CANE, w.BRASS_KNUCKLES, w.REVOLVER, w.SWITCHBLADE],
     'bounty': 175, 'type': NORMAL, 'areas': [CITY]},
    {'name': SERIAL_KILLER, 'hp': 120, 'weapons': [w.BONE_SAW, w.KNIFE, w.MEAT_CLEAVER],
     'bounty': 240, 'type': NORMAL, 'areas': [CITY, FOREST]},
    {'name': THIEF, 'hp': 85, 'weapons': [w.KNIFE, w.CROWBAR, w.PISTOL],
     'bounty': 170, 'type': NORMAL, 'areas': [CITY]},

    # ========================
    #       FOREST ENEMIES
    # ========================
    # --- new ---
    {'name': BIRDER, 'hp': 75, 'weapons': [w.TRIPOD, w.BINOCULARS, w.BEAR_SPRAY, w.PEPPER_SPRAY],
     'bounty': 90, 'type': NORMAL, 'areas': [FOREST]},
    {'name': DOOMSDAY_PREPPER, 'hp': 90, 'weapons': [w.KNIFE, w.PISTOL, w.SHOTGUN],
     'bounty': 170, 'type': NORMAL, 'areas': [FOREST]},
    {'name': FERAL_PHILOSOPHER, 'hp': 85, 'weapons': [w.CANE, w.PISTOL, w.SCYTHE],
     'bounty': 170, 'type': NORMAL, 'areas': [FOREST]},
    {'name': FORAGER, 'hp': 90, 'weapons': [w.KNIFE, w.SICKLE, w.BEAR_SPRAY],
     'bounty': 125, 'type': NORMAL, 'areas': [FOREST]},
    {'name': MUSHROOM_HUNTER, 'hp': 100, 'weapons': [w.KNIFE, w.SICKLE, w.BEAR_SPRAY],
     'bounty': 140, 'type': NORMAL, 'areas': [FOREST]},
    {'name': SURVIVALIST, 'hp': 100, 'weapons': [w.SURVIVAL_KNIFE, w.LONGBOW, w.BRANCH_SPEAR],
     'bounty': 155, 'type': NORMAL, 'areas': [FOREST]},
    {'name': TELEPATHIC_MUTE, 'hp': 90, 'weapons': [w.SCYTHE, w.SLINGSHOT, w.CHILI_POWDER],
     'bounty': 165, 'type': NORMAL, 'areas': [FOREST]},

    # --- original ---
    {'name': BIGFOOT_IMPERSONATOR, 'hp': 115, 'weapons': [w.WOODEN_CLUB, w.BRANCH_SPEAR, w.CLAWS, w.BEAR_SPRAY],
     'bounty': 185, 'type': NORMAL, 'areas': [FOREST]},
    {'name': DISGRACED_EXILE, 'hp': 80, 'weapons': [w.KNIFE, w.HATCHET, w.SHOVEL, w.TROWEL],
     'bounty': 120, 'type': NORMAL, 'areas': [CAVE, FOREST, SWAMP]},
    {'name': HIKER, 'hp': 90, 'weapons': [w.TREKKING_POLE, w.KNIFE, w.BEAR_SPRAY, w.BINOCULARS],
     'bounty': 115, 'type': NORMAL, 'areas': [FOREST]},
    {'name': HUNTER, 'hp': 100, 'weapons': [w.KNIFE, w.RIFLE, w.BEAR_SPRAY, w.LONGBOW, w.BEAR_SPRAY],
     'bounty': 175, 'type': NORMAL, 'areas': [FOREST]},
    {'name': PARK_RANGER, 'hp': 100, 'weapons': [w.FLARE_GUN, w.KNIFE, w.BEAR_SPRAY, w.MACHETE, w.LONGBOW],
     'bounty': 160, 'type': NORMAL, 'areas': [FOREST]},
    {'name': POACHER, 'hp': 100, 'weapons': [w.CROSSBOW, w.MACHETE, w.KNIFE, w.COMPOUND_BOW],
     'bounty': 210, 'type': NORMAL, 'areas': [FOREST]},

    # ========================
    #        CAVE ENEMIES
    # ========================
    # --- new ---
    {'name': ARCHAEOLOGIST, 'hp': 80, 'weapons': [w.FLASHLIGHT, w.CHISEL, w.PICKAXE, w.PEPPER_SPRAY],
     'bounty': 120, 'type': NORMAL, 'areas': [CAVE]},
    {'name': EXPLORER, 'hp': 100, 'weapons': [w.BINOCULARS, w.TREKKING_POLE, w.LONGBOW, w.SURVIVAL_KNIFE],
     'bounty': 140, 'type': NORMAL, 'areas': [CAVE]},
    {'name': FUGITIVE, 'hp': 90, 'weapons': [w.SHIV, w.INJECTION_NEEDLE, w.PISTOL, w.POCKET_SAND],
     'bounty': 225, 'type': NORMAL, 'areas': [CAVE, FOREST, SWAMP]},
    {'name': PROSPECTOR, 'hp': 80, 'weapons': [w.FLASHLIGHT, w.PICKAXE, w.CHISEL],
     'bounty': 110, 'type': NORMAL, 'areas': [CAVE]},
    {'name': SURVIVOR, 'hp': 100, 'weapons': [w.FLARE_GUN, w.SURVIVAL_KNIFE, w.POCKET_SAND],
     'bounty': 135, 'type': NORMAL, 'areas': [CAVE]},

    # --- original ---
    {'name': ANCIENT_MAN, 'hp': 80, 'weapons': [w.TORCH_CLUB, w.STONE_SPEAR, w.OBSIDIAN_KNIFE],
     'bounty': 130, 'type': NORMAL, 'areas': [CAVE]},
    {'name': HUMANOID_CAVE_CREATURE, 'hp': 110, 'weapons': [w.CLAWS, w.SCYTHE, w.BONE_CLUB],
     'bounty': 200, 'type': NORMAL, 'areas': [CAVE]},
    {'name': MINER, 'hp': 80, 'weapons': [w.FLASHLIGHT, w.KNIFE, w.PICKAXE],
     'bounty': 115, 'type': NORMAL, 'areas': [CAVE]},
    {'name': MOLE_PERSON, 'hp': 105, 'weapons': [w.CLAWS, w.PICKAXE, w.BONE_CLUB],
     'bounty': 175, 'type': NORMAL, 'areas': [CAVE]},
    {'name': SPELUNKER, 'hp': 80, 'weapons': [w.FLASHLIGHT, w.PICKAXE, w.FLARE_GUN],
     'bounty': 120, 'type': NORMAL, 'areas': [CAVE]},

    # ========================
    #        SWAMP ENEMIES
    # ========================
    # --- new ---
    {'name': BONE_COLLECTOR, 'hp': 110, 'weapons': [w.BONE_SAW, w.BONE_CLUB, w.MEAT_CLEAVER],
     'bounty': 205, 'type': NORMAL, 'areas': [SWAMP]},
    {'name': FORTUNE_TELLER, 'hp': 80, 'weapons': [w.KNIFE, w.PEPPER_SPRAY, w.PISTOL],
     'bounty': 130, 'type': NORMAL, 'areas': [SWAMP]},
    {'name': GATOR_WRESTLER, 'hp': 110, 'weapons': [w.FROG_GIG, w.SHOTGUN, w.SURVIVAL_KNIFE],
     'bounty': 195, 'type': NORMAL, 'areas': [SWAMP]},
    {'name': MOONSHINER, 'hp': 80, 'weapons': [w.SWITCHBLADE, w.SHOTGUN, w.NAIL_GUN],
     'bounty': 170, 'type': NORMAL, 'areas': [SWAMP]},
    {'name': SMUGGLER, 'hp': 85, 'weapons': [w.KNIFE, w.INJECTION_NEEDLE, w.POCKET_SAND, w.PISTOL],
     'bounty': 210, 'type': NORMAL, 'areas': [SWAMP]},
    {'name': TRACKER, 'hp': 90, 'weapons': [w.FLASHLIGHT, w.KNIFE, w.LONGBOW, w.RIFLE],
     'bounty': 160, 'type': NORMAL, 'areas': [SWAMP]},

    # --- original ---
    {'name': BAYOU_MAN, 'hp': 105, 'weapons': [w.FROG_GIG, w.GAFF_HOOK, w.SHOTGUN],
     'bounty': 185, 'type': NORMAL, 'areas': [SWAMP]},
    {'name': GRAVE_ROBBER, 'hp': 95, 'weapons': [w.POCKET_KNIFE, w.SHOVEL, w.CROWBAR, w.POCKET_SAND],
     'bounty': 165, 'type': NORMAL, 'areas': [SWAMP]},
    {'name': HAND_FISHERMAN, 'hp': 90, 'weapons': [w.KNIFE, w.FISHING_SPEAR, w.GAFF_HOOK, w.FROG_GIG],
     'bounty': 150, 'type': NORMAL, 'areas': [SWAMP]},
    {'name': SKIN_COLLECTOR, 'hp': 110, 'weapons': [w.KNIFE, w.MEAT_CLEAVER, w.CHAINSAW, w.MACHETE],
     'bounty': 230, 'type': NORMAL, 'areas': [SWAMP]},
    {'name': VOODOO_PRIESTESS, 'hp': 80, 'weapons': [w.VOODOO_STAFF, w.CHILI_POWDER],
     'bounty': 150, 'type': NORMAL, 'areas': [SWAMP]},
]


Bosses = [
    # ========================
    #        AREA BOSSES
    # ========================
    {'name': SLEDGE_HAMMOND, 'hp': 250,
     'weapons': [w.SLEDGEHAMMER, w.AXE, w.CHAINSAW, w.BRASS_KNUCKLES, w.INJECTION_NEEDLE],
     'bounty': 0, 'type': BOSS, 'preamble': {}},

    {'name': THE_MAYOR, 'hp': 200,
     'weapons': [w.PISTOL, w.SHOTGUN, w.REVOLVER, w.BRASS_KNUCKLES, w.BASEBALL_BAT],
     'bounty': 0, 'type': BOSS, 'theme': audio.FINAL_BOSS_THEME},

    {'name': BAYOU_BILL, 'hp': 200,
     'weapons': [w.MACHETE, w.SLEDGEHAMMER, w.SHOTGUN, w.CHAINSAW, w.FROG_GIG],
     'bounty': 0, 'type': BOSS,
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
              {'text': "When you livin' in the swamp, ain't nobody come round lessen dey askin' for trouble...",
               'color': Colors.RED, 'sleep': 2},
          ]},
     ]},

    {'name': CAPTAIN_HOLE, 'hp': 220,
     'weapons': [w.RIFLE, w.HARPOON, w.KNIFE, w.PISTOL, w.MACHETE],
     'bounty': 0, 'type': BOSS, 'preamble': [
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
"I've waited a long, long time to put you down..."
"I knew if I captured the champion's beloved Chula, he would send you to her rescue..."
"Well, let's have at it then.\""""
Final_Boss = {
    'name': DENNY_BILTMORE,
    'hp': 275, 'weapons': [w.BRASS_KNUCKLES, w.PISTOL, w.REVOLVER, w.SHOTGUN],
    'bounty': 0, 'type': FINAL_BOSS, 'preamble': [{'text': text, 'color': Colors.RED, 'sleep': 4}
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
    CARD_JOCKEY: [],
    CLONE: [],
    CLOWN: [],
    FROGGER: [],
    INFLUENCER: [],
    LIFE_COACH: [],
    MASCOT: [],
    MIME: [],
    PARTY_ANIMAL: [],
    SENTIENT_ROBOT: [],
    SLEEPWALKER: [],

    BODY_BUILDER: [
        "Body oil is worth its weight in gold. Well, it should be."
        "Everything I need comes in an unlabeled bottle."
        "I can bench a million, easy.",
        "I'm more concerned about gains than I am about shrinkage.",
        "My neighbor, Gary, is a hell of a speller. Pecs need work though."
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
        "A rich man gave me coin to add you to my list.",
        "God can do a lot, but he can't do the things I can do to you.",
        "How do I know you?",
        "I get a lot of hand-penned letters from the mayor.",
        "If God taketh, but I take your life... am I not, then, God?",
    ],

    THIEF: [
        "An old, rich guy paid me coin to take you out. Who knew you could get coin without stealing?",
        "Give me all of your coin, or else!",
        "I live to steal and steal to live... or maybe I just steal to steal?",
        "I need coin to go out West, so I can steal coin out West.",
        "I stole coin from an old lady today... or was that yesterday? Probably both.",
    ],

    # ===== FOREST =====
    BIRDER: [],
    DOOMSDAY_PREPPER: [],
    FERAL_PHILOSOPHER: [],
    FORAGER: [],
    MUSHROOM_HUNTER: [],
    SURVIVALIST: [],
    TELEPATHIC_MUTE: [],

    PARK_RANGER: [
        "Have you seen any Mystical Mushrooms? I'm going to a music festival this weekend.",
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
    ARCHAEOLOGIST: [],
    EXPLORER: [],
    FUGITIVE: [],
    PROSPECTOR: [],
    SURVIVOR: [],

    ANCIENT_MAN: [
        "A rich man hired me to kill you. While I don't need money, I do need blood to drink.",
        "I know how the Pyramids were built. I was there.",
        "I've never left this cave for fear of falling off the edge of the Earth.",
        "Is Hammurabi still in power?",
        "My liberation is imminent, but yours is... what's more imminent than imminent?",
        "Plato autographed my favorite rock. It's somewhere in my rockpile.",
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
        "I haven't found anything, but my mom always says I'm the real treasure."
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
        "I am one with God, because I am God. You are not God... you are not God."
        "Man pays. God accepts. Man pays.",
        "You think you are holy... but you are not holy. Do you even live in a hole?",
    ],

    # ===== SWAMP =====
    BONE_COLLECTOR: [],
    FORTUNE_TELLER: [],
    GATOR_WRESTLER: [],
    MOONSHINER: [],
    SMUGGLER: [],
    TRACKER: [],

    BAYOU_MAN: [
        "I'd hate to see you get cold out here on the bayou.",
        "Riverboat, Crawdad, Alligator Gumbo!",
        "When you livin' in the swamp ain't nobody come 'round.",
        "Without some fresh feed it's easy for a boy to come up cold out here on the bayou.",
    ],

    GRAVE_ROBBER: [
        "A well-dressed man gave me coin to bury you, dead or alive.",
        "One time I fell asleep in a grave I robbed and woke up under a pile of dirt.",
        "The skeletons don't need jewelry.",
        "They'll be turned into rent soon anyway.",
        "When I'm dead, I hope someone robs my grave. I also hope I'm a zombie when he does.",
        "Zombies are real. Trust me, I would know.",
    ],

    HAND_FISHERMAN: [
        "He pulled me out of a catfish's mouth. How could I turn down his request? Sorry, bud!",
        "I'd use a pole but the fish are just way too big. They ate my first three born.",
        "If you count your hand as a catch, you catch something every time! Unless a catfish bites it off...",
        "Once, I pulled a man out of a hole - but, to his dismay, I put him back, because I wasn't fishing for men that day.",
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
        "I can tell you your future... It's very dark. Soon, you will see what I mean.",
        "I will shrink your head, then raise the dead, then shrink their heads, 'cause I love shrinkin' heads.",
        "Once your head is mine, I will be able to afford a new case to display all of my shrunken heads.",
    ],
}


# ========================
#        ENEMY ADJECTIVES
# ========================

Enemy_Adjectives = [
    "Agitated", "Bestial", "Bloodthirsty", "Cannibalistic", "Crazy",
    "Crazed", "Cursed", "Damned", "Dastardly", "Degenerate",
    "Delirious", "Demented", "Depraved", "Deranged", "Detestable",
    "Diabolical", "Disgruntled", "Disillusioned",
    "Disoriented", "Disturbed", "Drug-fueled",
    "Drunken", "Dubious", "Evil", "Fallen", "Feral",
    "Forgotten", "Godless", "Hallucinatory", "Heartless",
    "Heinous", "Hostile", "Idolatrous", "Immoral",
    "Inbred", "Insane", "Jaded", "Malevolent", "Malicious",
    "Merciless", "Misguided", "Moralless",
    "Obscene", "Possessed", "Psychotic",
    "Rabid", "Sadistic", "Sinful", "Soulless",
    "Tench-eyed", "Typical", "Unholy",
    "Uninspired", "Unnatural", "Unstable", "Untrustworthy",
    "Vile", "Wretched",
]
