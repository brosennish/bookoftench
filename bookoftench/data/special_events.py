from bookoftench.data import areas as a
from bookoftench.data.audio import ROULETTE_THEME
from bookoftench.ui import green, purple, yellow

# ================================================================================================

# Special Events
FRIENDLY_ALIENS = "Friendly Aliens"
GREEDY_BASTARD = "Greedy Bastard"
HERPES_KISS = "Herpes Kiss"
SHEBOKKEN_ROULETTE = "Shebokken Roulette"
STINGY_BASTARD = "Stingy Bastard"
THREE_HOLES = "Three Holes"
TRIPLE_TENCH_DARE = "Triple Tench Dare"
ZONKED = "Zonked"

# Time
DAY = "Daytime"
NIGHT = "Nighttime"

# ================================================================================================

# if moon in moon or if moon == None

Special_Events = [

    {'name': FRIENDLY_ALIENS, 'color': green, 'sleep': 3, 'theme': None,
     'areas': [a.CITY, a.FOREST, a.SWAMP], 'time': [NIGHT], 'moon': None, 'season': None,
     'text': "You were abducted by aliens!\nThey wish to be of assistance.\nWhat can they do for you?",
     'choices': ['Increase strength by 0.03', 'Increase accuracy by 0.03', 'Increase luck by 2'],
     'optional': True, 'method': 'friendly_aliens'},


    {'name': GREEDY_BASTARD, 'color': purple, 'sleep': 5, 'theme': None,
     'areas': [a.CAVE, a.CITY, a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': "An old woman with wrinkled eyeballs wearing a homemade cloak approaches you.\n"
            "Hey! You there! I have coin...\n"
            "How much do you want? Hehehe.",
     'choices': ['10', '20', '30', '40', '50'],
     'optional': True, 'method': 'greedy_bastard'},


    {'name': SHEBOKKEN_ROULETTE, 'color': purple, 'sleep': 5, 'theme': ROULETTE_THEME,
     'areas': [a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': "A leather-skinned man approaches you, revolver in hand.\n"
             "Might I interest you in a round of Shebokken Roulette?\n"
             "One bullet, two blindfolds.\n"
             "What's your wager?",
     'choices': ['10', '20', '30', '40', '50'],
     'optional': False, 'method': 'shebokken_roulette'},


    {'name': STINGY_BASTARD, 'color': purple, 'sleep': 5, 'theme': None,
     'areas': [a.CAVE, a.CITY, a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': "An old woman with three nostrils and two noses approaches you.\n"
            "Hey! You there! I need coin...\n"
            "How much will you give me? Hehehe.",
     'choices': ['10', '20', '30', '40', '50'],
     'optional': True, 'method': 'stingy_bastard'},


    {'name': THREE_HOLES, 'color': purple, 'sleep': 5, 'theme': None,
     'areas': [a.CAVE, a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': "You come upon three holes in the ground...\n"
             "They are far too deep - and too dark - to see what's inside.\n"
             "A ghastly being with an upside down face rushes towards you.\n"
             "Extending its elastic lips deep into your earhole,\n"
             "It whispers that you may only reach into one of the holes.",
     'choices': ['Hole 1', 'Hole 2', 'Hole 3'],
     'optional': True, 'method': 'three_holes'},


    {'name': TRIPLE_TENCH_DARE, 'color': yellow, 'sleep': 4, 'theme': None,
     'areas': [a.CITY, a.FOREST, a.SWAMP], 'time': [DAY], 'moon': None, 'season': None,
     'text': "A rambunctious boy approaches you, dad's wallet in hand...\n"
             "He triple-tench-dares you to stare at the sun.\n"
             "For every second, he will give you 5 of coin.\n"
             "How many seconds will you do?",
     'choices': ['5', '10', '15', '20'],
     'optional': True, 'method': 'triple_tench_dare'},


    {'name': ZONKED, 'color': purple, 'sleep': 4, 'theme': None,
     'areas': [a.CITY], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': "You come across a man who is totally zonked...\n"
             "His 1977 Slade shirt is caked with drool.\n"
             "You've never seen someone so zonked in your whole dang life.\n"
             "HWhat will you do?",
     'choices': ['Wake Him Up', 'Bury Him Alive'],
     'optional': True, 'method': 'zonked'},

]

# ================================================================================================

Special_Event_Adjectives = [
    "ancient", "angry", "bald", "blind",
    "bloody", "bony", "bored", "brainwashed",
    "braindead", "child-sized", "closeted", "confused",
    "cool", "crazed", "creepy", "cross-eyed",
    "curious", "dead-eyed", "degenerate", "delirious",
    "denim", "deplorable", "deranged", "dirty",
    "disfigured", "disgruntled", "disillusioned", "drug-fueled",
    "drunken", "elderly", "enormous", "felonious",
    "feral", "filthy", "giggly", "gruntled",
    "hairless", "hallucinating", "holy", "hollow",
    "homicidal", "horny", "hungry", "idolatrous",
    "inbred", "insane", "inside-out", "invisible",
    "lazy-eyed", "lonely", "lost", "mealy",
    "misguided", "moralless", "mysterious", "nervous",
    "obscene", "one-eyed", "pale", "peculiar",
    "radioactive", "rancid", "reanimated", "rotten",
    "satanic", "screaming", "sleepy", "sloppy",
    "soaked", "soggy", "soulless", "strange",
    "suspicious", "three-eyed", "tiny", "toothless",
    "two-headed", "uncool", "undead", "unholy",
    "unsettling", "unstable", "upside-down", "vile",
    "wrinkled", "wretched", "zombified"
]

Special_Event_Characters = [
    "man", "woman", "elder", "elderly man",
    "elderly woman", "lady", "guy", "fellow",
    "stranger", "drifter", "traveler", "wanderer",
    "visitor", "boy", "girl", "child",
    "gentleman", "ghost", "creature", "entity",
    "figure", "thing", "being", "presence",
    "apparition", "phantom", "soul", "spirit",
    "individual", "person"
]