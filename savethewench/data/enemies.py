from savethewench.ui import Colors
from . import audio, weapons

# Constants
ANCIENT_MAN = "Ancient Man"
BAYOU_BILL = "Bayou Bill"
BAYOU_MAN = "Bayou Man"
BIGFOOT_IMPERSONATOR = "Bigfoot Impersonator"
BODY_BUILDER = "Body Builder"
CAPTAIN_HOLE = "Captain Hole"
DENNY_BILTMORE = "Denny Biltmore"
DISGRACED_EXILE = "Disgraced Exile"
GOON = "Goon"
GRAVE_ROBBER = "Grave Robber"
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
    {'name': HOBO, 'hp': 80, 'weapons': [weapons.BROKEN_BOTTLE, weapons.KNIFE, weapons.POCKET_SAND],
     'bounty': 50, 'type': NORMAL},
    {'name': THIEF, 'hp': 90, 'weapons': [weapons.KNIFE, weapons.BAT], 'bounty': 75, 'type': NORMAL},
    {'name': GOON, 'hp': 100, 'weapons': [weapons.CHILI_POWDER, weapons.BAT, weapons.PISTOL],
     'bounty': 100, 'type': NORMAL},
    {'name': PIMP, 'hp': 110,
     'weapons': [weapons.PEPPER_SPRAY, weapons.BRASS_KNUCKLES, weapons.REVOLVER], 'bounty': 125, 'type': NORMAL},
    {'name': BODY_BUILDER, 'hp': 125,
     'weapons': [weapons.BAT, weapons.BRASS_KNUCKLES], 'bounty': 125, 'type': NORMAL},

    # ========================
    #       FOREST ENEMIES
    # ========================
    {'name': HIKER, 'hp': 80, 'weapons': [weapons.HATCHET, weapons.KNIFE, weapons.BEAR_SPRAY],
     'bounty': 50, 'type': NORMAL},
    {'name': HUNTER, 'hp': 90, 'weapons': [weapons.KNIFE, weapons.RIFLE, weapons.BEAR_SPRAY],
     'bounty': 75, 'type': NORMAL},
    {'name': BIGFOOT_IMPERSONATOR, 'hp': 100, 'weapons': [weapons.PISTOL, weapons.CLAWS, weapons.BEAR_SPRAY],
     'bounty': 100, 'type': NORMAL},
    {'name': POACHER, 'hp': 110, 'weapons': [weapons.CROSSBOW, weapons.MACHETE, weapons.BEAR_SPRAY],
     'bounty': 125, 'type': NORMAL},

    # ========================
    #        CAVE ENEMIES
    # ========================
    {'name': MINER, 'hp': 80, 'weapons': [weapons.PICKAXE, weapons.KNIFE], 'bounty': 50, 'type': NORMAL},
    {'name': SPELUNKER, 'hp': 90, 'weapons': [weapons.PICKAXE, weapons.KNIFE], 'bounty': 75, 'type': NORMAL},
    {'name': ANCIENT_MAN, 'hp': 95, 'weapons': [weapons.HARPOON, weapons.KNIFE], 'bounty': 85, 'type': NORMAL},
    {'name': MOLE_PERSON, 'hp': 100, 'weapons': [weapons.CLAWS, weapons.PICKAXE], 'bounty': 100, 'type': NORMAL},
    {'name': HUMANOID_CAVE_CREATURE, 'hp': 110, 'weapons': [weapons.CLAWS, weapons.SLEDGEHAMMER],
     'bounty': 125, 'type': NORMAL},

    # ========================
    #        SWAMP ENEMIES
    # ========================
    {'name': HAND_FISHERMAN, 'hp': 80, 'weapons': [weapons.HATCHET, weapons.KNIFE], 'bounty': 50, 'type': NORMAL},
    {'name': VOODOO_PRIESTESS, 'hp': 90,
     'weapons': [weapons.VOODOO_STAFF, weapons.KNIFE, weapons.CHILI_POWDER], 'bounty': 75, 'type': NORMAL},
    {'name': GRAVE_ROBBER, 'hp': 95,
     'weapons': [weapons.SHOVEL, weapons.KNIFE, weapons.POCKET_SAND], 'bounty': 85, 'type': NORMAL},
    {'name': BAYOU_MAN, 'hp': 100, 'weapons': [weapons.MACHETE, weapons.SHOTGUN], 'bounty': 100, 'type': NORMAL},
    {'name': SKIN_COLLECTOR, 'hp': 110, 'weapons': [weapons.MACHETE, weapons.CHAINSAW], 'bounty': 125, 'type': NORMAL},

    # ========================
    #        MULTI-LOCATION ENEMIES
    # ========================
    {'name': SERIAL_KILLER, 'hp': 120, 'weapons': [weapons.KNIFE, weapons.MACHETE], 'bounty': 200, 'type': NORMAL},
    {'name': DISGRACED_EXILE, 'hp': 90, 'weapons': [weapons.HATCHET, weapons.SHOVEL], 'bounty': 75, 'type': NORMAL},
]

Bosses = [
    # ========================
    #        AREA BOSSES
    # ========================
    {'name': SLEDGE_HAMMOND, 'hp': 250,
     'weapons': [weapons.SLEDGEHAMMER, weapons.AXE, weapons.CHAINSAW, weapons.BRASS_KNUCKLES],
     'bounty': 0, 'type': BOSS, 'preamble': {}},

    {'name': THE_MAYOR, 'hp': 200,
     'weapons': [weapons.PISTOL, weapons.SHOTGUN, weapons.REVOLVER, weapons.BRASS_KNUCKLES],
     'bounty': 0, 'type': BOSS, 'theme': audio.FINAL_BOSS_THEME},

    {'name': BAYOU_BILL, 'hp': 200,
     'weapons': [weapons.MACHETE, weapons.SLEDGEHAMMER, weapons.SHOTGUN, weapons.CHAINSAW],
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
     'weapons': [weapons.RIFLE, weapons.HARPOON, weapons.KNIFE, weapons.PISTOL],
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
    'hp': 275, 'weapons': [weapons.BRASS_KNUCKLES, weapons.PISTOL, weapons.REVOLVER, weapons.SHOTGUN],
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
    ANCIENT_MAN: ["The Hindustan Times underestimated my age by a few thousand years.",
                  "Is Hammurabi still in power?",
                  "I've never left this cave for fear of falling off the edge of the Earth.",
                  "Plato autographed my favorite rock. It's somewhere in my rockpile.",
                  "I know how the Pyramids were built. I was there.",
                  "My liberation is imminent, but yours is... what's more imminent than imminent?",
                  "A rich man hired me to kill you. While I don't need money, I do need blood to drink."],
    BODY_BUILDER: ["Some sculpt marble, some sculpt clay. I sculpt my body.",
                "Don't call me beefcake. I'm 100% beef.",
                "I can bench a million, easy.",
                "Body oil is worth its weight in gold. Well, it should be."
                "My neighbor, Gary, is a hell of a speller. Pecs need work though."
                "Everything I need comes in an unlabeled bottle."
                "I'm more concerned about gains than I am about shrinkage.",
                "The guy who hired me was rich, but I totally could've kicked his ass."],
    GRAVE_ROBBER: ["The skeletons don't need jewelry.",
                   "They'll be turned into rent soon anyway.",
                   "A well-dressed man gave me coin to bury you, dead or alive.",
                   "When I'm dead, I hope someone robs my grave. I also hope I'm a zombie when he does."],
    THIEF: ["Give me all of your coin, or else!",
            "I stole coin from an old lady today... or was that yesterday? Probably both.",
            "I live to steal and steal to live... or maybe I just steal to steal?",
            "I need coin to go out West, so I can steal coin out West.",
            "An old, rich guy paid me coin to take you out. Who knew you could get coin without stealing?"],
    GOON: ["I'll do anything for coin, as long as it's violent.",
           "Without my sunglasses, I'm nothing...",
           "I often call Michelob Chounce for legal support on account of my violent lifestyle.",
           "School's for suckers and chumps. Why learn when I can beat people up?"],
    PIMP: ["I love my hoes.",
           "If you die, I will give your coin to my hoes.",
           "Hoes or not, I sure do love them.",
           "I'm nothing without my hoes."],
    HOBO: ["Give me those coins or I'll cut off your loins!",
           "I ate a rapper yesterday. No 'w'.",
           "People don't give me coin unless I kill them.",
           "You know how much Mystery Meat I can buy with just a small amount of coin?"],
    SERIAL_KILLER: ["If God taketh, but I take your life... am I not, then, God?",
                    "God can do a lot, but he can't do the things I can do to you.",
                    "I get a lot of hand-penned letters from the mayor.",
                    "How do I know you?",
                    "A rich man gave me coin to add you to my list."],
    HIKER: ["I'm alone in the woods, so you must be a murderer. I've seen movies!",
            "Are chipmunks dangerous? I figure if there's enough of them they could take me out...",
            "All mushrooms are safe to eat, right?",
            "I thought I heard a bear, but it was just a leaf blowing in the wind."],
    DISGRACED_EXILE: ["You know, life was actually worse before I was exiled.",
                      "If the town understood why I tried to burn it down, maybe they wouldn't have exiled me.",
                      "They didn't exile me - I exiled them... from myself.",
                      "I'm mostly lonely - except when the feral lads come by. Then I'm lonely and terrified.",
                      "There's another exile out here who's not disgraced, but revered. We couldn't be more different."],
    HUNTER: ["Why hang out with girls when I can be out here in the cold hunting by myself?",
             "Once I got bored of hunting animals, I started hunting people instead. You know, just for fun.",
             "I hang animals on my wall and my wife hates them all."],
    POACHER: ["Protected species? More like I'm going to put its head on my wall, species.",
              "Tusks are sharp, but I'm the sharpest.",
              "People pay me coin to kill illegal stuff. So what? Sue me! Well, don't do that, actually."],
    MINER: ["I thought I found some coal a month ago... turns out poop looks a lot like coal in the pitch dark.",
            "I nearly had a heart attack when I heard a man talking in the mine. Turns out it was just me, talking to myself.",
            "All of my friends worked in these mines. They're all dead now. Maybe I should get a different job?"],
    SPELUNKER: ["I haven't found anything, but my mom always says I'm the real treasure."
                "I got into this because of a video game... and now I'm in one! Oh my god... how do I go back!?",
                "People think spelunking is just playing around in dark, wet holes."],
    MOLE_PERSON: ["fircnosdnvkclgnsdksnlfdkdfmkmcyufgkuyfk",
                  "orihgeoiwsifdjnwsietnvirodbrgnioevndoirnguyf",
                  "ihfedkjnefdnefidnifnidnuygfkuyfv"],
    HUMANOID_CAVE_CREATURE: ["God may be merciful... loving... but I am not God. I am not God.",
                             "You think you are holy... but you are not holy. Do you even live in a hole?",
                             "I am one with God, because I am God. You are not God... you are not God."],
    HAND_FISHERMAN: [
        "If you count your hand as a catch, you catch something every time! Unless a catfish bites it off...",
        "I'd use a pole but the fish are just way too big. They ate my first three born.",
        "Once, I pulled a man out of a hole - but, to his dismay, I put him back, because I wasn't fishing for men that day."],
    VOODOO_PRIESTESS: [
        "I will shrink your head, then raise the dead, then shrink their heads, 'cause I love shrinkin' heads.",
        "I can tell you your future... It's very dark. Soon, you will see what I mean.",
        "Does it drive you crazy when I shake my stick?"],
    BAYOU_MAN: ["When you livin' in the swamp ain't nobody come 'round.",
                "Without some fresh feed it's easy for a boy to come up cold out here on the bayou.",
                "Riverboat, Crawdad, Alligator Gumbo!",
                "I'd hate to see you get cold out here on the bayou."],
    SKIN_COLLECTOR: ["I don't just collect skins... I collect souls too. Oh, and baseball cards.",
                     "Your skin looks very comfortable. May I try it on?",
                     "Where did you get your skin? It's so... fresh.",
                     "You have to lotion your skins before they run dry."]
}
