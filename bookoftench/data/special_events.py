from bookoftench.data import areas as a
from bookoftench.data.audio import ROULETTE_THEME, HOHKKEN_THEME, HOSPITAL_THEME
from bookoftench.data.enemies import OILY_DOILY
from bookoftench.data.enviroment import DAY, NIGHT
from bookoftench.ui import green, purple, yellow, blue, red, white, orange

# ================================================================================================

# Standard Events
GREEDY_BASTARD = "Greedy Bastard" # formatted
HERPES_KISS = "Herpes Kiss" # formatted
LOST_GOLD_P1 = "Lost Gold P1"
LOST_GOLD_P2 = "Lost Gold P2"
PROBING = "Probing"
SHEBOKKEN_ROULETTE = "Shebokken Roulette"
STINGY_BASTARD = "Stingy Bastard"
THREE_HOLES = "Three Holes"
TRIPLE_TENCH_DARE = "Triple Tench Dare"
ZONKED = "Zonked"

# News
NEWS_HEADLESS_WHORES_MAN = "News Headless Whore's Man"
NEWS_HOHKKEN_ENTERS_CITY = "Hohkken Enters City"
NEWS_WHALE_MAN = "News Whale Man" # formatted
WEDNESDAY_NEWS = "Wednesday News"

# Boss Introductions
OILY_PROPOSAL = "Oily Introduction"

# Investment Opportunities


# Text-Only
SANTAS_SNOW = "Santa's Snow"

# ================================================================================================

Special_Events = [

    {'name': GREEDY_BASTARD, 'color': purple, 'sleep': 5, 'theme': None,
     'areas': [a.CITY, a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """An old woman with wrinkled eyeballs wearing a soiled cloak approaches you.
        
Old Woman: Hey! You there! 

I have coin...

How much do you want? Hehehe.
""",
     'choices': ['10', '20', '30', '40', '50'],
     'optional': True, 'method': 'greedy_bastard', 'replayable': True},

# ================================================================================================

    {'name': HERPES_KISS, 'color': purple, 'sleep': 5, 'theme': None,
     'areas': [a.CITY, a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """A sensuous being with mealy lips and a hint of humanity approaches.
     
Sensuous Being: Your lips...
They are so nice... so luscious.
Oh, I've just been so lonely since I lost my imaginary lover.

Might I have a taste?

I will give you 8 of coin for each kiss... hehehe.
""",
     'choices': ['Kiss 1x', 'Kiss 3x', 'Kiss 5x', 'Kiss 10x'],
     'optional': True, 'method': 'herpes_kiss', 'replayable': True},

# ================================================================================================

    {'name': LOST_GOLD_P1, 'stage': 1, 'color': blue, 'sleep': 5, 'theme': None,
     'areas': [a.CITY], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """You smell the overwhelming stench of brine-soaked jines...
     
Pirate: Argh! I lost me gold.
Tell me matey, wher' can I find me gold?
""",
     'choices': ['Cave', 'City', 'Forest', 'Swamp'],
     'optional': False, 'method': 'lost_gold_p1', 'replayable': False,
     'related': [LOST_GOLD_P2]},

    {'name': LOST_GOLD_P2, 'stage': 2, 'color': red, 'sleep': 5, 'theme': None,
     'areas': [a.CITY], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """You smell a familiar stench...
        
Pirate: Argh! You lied to me, matey.
I searched for me gold and came up dry!

Give me coin or I'll shoot ya right in yer jines.
Aye, and if yer dry, a tench filet would also do.
""",
     'choices': ['Give Coin (50), Give Tench Filet, Beg for Mercy'],
     'optional': False, 'method': 'lost_gold_p2', 'replayable': False,
     'related': [LOST_GOLD_P1]},

# ================================================================================================

    {'name': NEWS_HEADLESS_WHORES_MAN, 'color': white, 'sleep': 8, 'theme': None,
     'areas': [a.CITY, a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """Your flip phone buzzes with a news alert...
        
*** BREAKING NEWS ***

Reporter: Police have found a headless body in Shebokken's swamp region.
Forensics believe the body belonged to the late husband of a beloved local prostitute.
He has already become affectionately known as the \"Headless Whore's Man\".

Reporting live from the Swamp, I'm Shannon O'Shanahan, Shebokken News.
""",
     'choices': [],
     'optional': True, 'method': None, 'replayable': False},

    {'name': NEWS_HOHKKEN_ENTERS_CITY, 'color': white, 'sleep': 8, 'theme': HOHKKEN_THEME,
     'areas': [a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """Your flip phone buzzes with a news alert...
     
*** BREAKING NEWS ***

Reporter: Behind me is the aftermath of a once-in-a-lifetime event.

The Hohkken, a legendary sea monster, emerged from the ocean and entered the city.
Despite the immeasurable destruction of the city, no lives were lost.
Our experts believe this to be a sign that it was searching for something -
or someone - specifically.

Whoever you are, wherever you are, just know, the Hohkken is coming for you.

Reporting live from Shebokken, I'm Shannon O'Shanahan, Shebokken News.
""",
     'choices': [],
     'optional': True, 'method': None, 'replayable': False},

    {'name': NEWS_WHALE_MAN, 'color': white, 'sleep': 8, 'theme': None,
     'areas': [a.FOREST], 'time': [DAY], 'moon': None, 'season': None,
     'text': """Your flip phone buzzes with a news alert...
     
*** BREAKING NEWS ***

Reporter: Behind me is the home of a spectacular creature
who was discovered just a few hours ago.

Escaped death-row inmate Wimbo Gillio stumbled upon a massive estuary
in Shebokken's forest region.

Submerging into the murky water to relieve himself of the rotten slop in his gut,
Gillio was startled by an anthropomorphic marine specimen leaping from the water.
While he initially suspected residual effects from the drugs he'd taken in prison,
Gillio was not hallucinating... 

What Gillio saw was a man who had evolved into a human whale.

Hambilton Taine, the name he was known by while living among Shebokken's elite,
reports having become disillusioned with the incessant orgy fundraisers 
and fetus buffets.

As a result, Taine decided to leave the city and start a new life for himself underwater.
Though Taine maintains the phallic and rectal anatomy of a human man,
his body quickly consumed its lungs in order to develop fully-functioning gills and fins.

Reporting live from Shebokken, I'm Shannon O'Shanahan, Shebokken News.
""",
     'choices': [],
     'optional': True, 'method': None, 'replayable': False},

    {'name': WEDNESDAY_NEWS, 'color': orange, 'sleep': 8, 'theme': None,
     'areas': [a.FOREST, a.SWAMP], 'time': [DAY], 'moon': None, 'season': None,
     'text': """Your flip phone buzzes with a news alert...
        
*** BREAKING NEWS ***

Wednesday Wednesday: Good morning, Shebokken.
It's Wednesday, and I'm Wednesday Wednesday with
Wednesday Wednesday's Wednesday News, hosted by me,
Wednesday Wednesday.
...

Tench Avenue will have a lane closure from 1:15-1:30 next Wednesday.

Reporting live from Shebokken, I'm Wednesday Wednesday, with
Wednesday Wednesday's Wednesday News, only on Wednesdays.
""",
     'choices': [],
     'optional': True, 'method': None, 'replayable': False},

# ================================================================================================

    {'name': PROBING, 'color': green, 'sleep': 5, 'theme': None,
     'areas': [a.CITY, a.FOREST, a.SWAMP], 'time': [NIGHT], 'moon': None, 'season': None,
     'text': """You were abducted by aliens!
     
Perverto: Are you ready for your probing?

What do you do?
""",
     'choices': ['Accept Probe', 'Attempt to Probe the Aliens', 'Try to Escape'],
     'optional': False, 'method': 'probing', 'replayable': True},

# ================================================================================================

    {'name': SANTAS_SNOW, 'color': white, 'sleep': 5, 'theme': None,
     'areas': [a.CITY], 'time': [NIGHT], 'moon': None, 'season': None,
     'text': """A sad, old, fat man with a huge bulge descends from the sky.
        
Santa: The only thing better than a hole in the sled...
Is a hole in the head.

I think I left my Snow in the Cave...
""",
     'choices': [],
     'optional': True, 'method': 'santas_snow', 'replayable': False},

# ================================================================================================

    {'name': SHEBOKKEN_ROULETTE, 'color': purple, 'sleep': 5, 'theme': ROULETTE_THEME,
     'areas': [a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """A leather-skinned man approaches you, revolver in hand.
     
Man: I reckon it's high time for a round of Shebokken Roulette.
One bullet, two blindfolds.

What's your wager?
""",
     'choices': ['10', '20', '30', '40', '50'],
     'optional': False, 'method': 'shebokken_roulette', 'replayable': True},

# ================================================================================================

    {'name': STINGY_BASTARD, 'color': purple, 'sleep': 5, 'theme': None,
     'areas': [a.CAVE, a.CITY, a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """An old woman with two noses and three nostrils approaches you.
     
Old Woman: Hey! You there!
 
I need coin...

How much will you give me? Hehehe.
""",
     'choices': ['10', '20', '30', '40', '50'],
     'optional': True, 'method': 'stingy_bastard', 'replayable': True},

# ================================================================================================

    {'name': THREE_HOLES, 'color': purple, 'sleep': 5, 'theme': None,
     'areas': [a.CAVE, a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """You come upon three holes in the ground...
        
They are far too deep - and too dark - to see what's inside.

A ghastly being with an upside-down face rushes towards you.

Extending its elastic lips deep into your earhole,
it whispers that you may only reach into one of the holes.
""",
     'choices': ['Hole 1', 'Hole 2', 'Hole 3'],
     'optional': True, 'method': 'three_holes', 'replayable': True},

# ================================================================================================

    {'name': TRIPLE_TENCH_DARE, 'color': yellow, 'sleep': 5, 'theme': None,
     'areas': [a.CITY, a.FOREST, a.SWAMP], 'time': [DAY], 'moon': None, 'season': None,
     'text': """A rambunctious boy approaches you, dad's wallet in hand...
     
He triple-tench-dares you to stare at the sun.
For every second, he will give you 5 of coin.

How many seconds will you do?
""",
     'choices': ['5', '10', '15', '20'],
     'optional': True, 'method': 'triple_tench_dare', 'replayable': True},

# ================================================================================================

    {'name': ZONKED, 'color': purple, 'sleep': 5, 'theme': None,
     'areas': [a.CITY], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """You come across a man who is totally zonked...

His Slade shirt is caked with drool.
You've never seen someone so zonked in your whole dayng life.
The voice in your jines says that you must do something...

What do you do?
""",
     'choices': ['Wake Him Up', 'Bury Him Alive'],
     'optional': False, 'method': 'zonked', 'replayable': True},

# ================================================================================================

{'name': OILY_PROPOSAL, 'color': red, 'sleep': 8, 'theme': HOSPITAL_THEME,
     'areas': [a.CITY], 'time': [NIGHT], 'moon': None, 'season': None,
     'text': """You turn and see a giant balloon floating towards you...

As it nears, you notice that it is actually a sub-human man in a helium suit.

Oily Doily: Why... hello, to you's... hehehe, hohoho.

You know... you know? You know that I have a store in Shebokken,
and it's just around that corner... hehehe, hohoho.

Why don't you grab ahold of my jines, and I will float us in through
the tallest window of the shortest tower?

Hehehe, hohoho.

What do you do?
""",
    'choices': ['Grab Jines', 'Run Away'],
    'optional': False, 'method': 'oily_proposal', 'replayable': False},

]

# ================================================================================================

# Just in case

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