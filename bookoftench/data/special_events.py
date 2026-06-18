from bookoftench.data import areas as a
from bookoftench.data.audio import ROULETTE_THEME, HOHKKEN_THEME, HOSPITAL_THEME, BATTLE_THEME
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
BASTA_INTRO = "Basta Intro"
CYCLOPS_INTRO = "Cyclops Intro"
DEATH_WORM_INTRO = "Death Worm Intro"
GIANT_MUTANT_RAT_INTRO = "Giant Mutant Rat Intro"
OILY_DOILY_INTRO = "Oily Intro"
SABERTOOTH_LIGER_INTRO = "Sabertooth Liger Intro"
SEWER_GATOR_INTRO = "Sewer Gator Intro"
SLENDER_INTRO = "Slender Intro"

# Investment Opportunities


# Text-Only
SANTAS_SNOW = "Santa's Snow"

# ================================================================================================

Special_Events = [

    {'name': GREEDY_BASTARD, 'color': purple, 'sleep': 3, 'theme': None,
     'areas': [a.CITY, a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """An old woman with wrinkled eyeballs wearing a soiled cloak approaches you.

Old Woman: Hey! You there! 

I have coin...

How much do you want? Hehehe.
""",
     'choices': ['10', '20', '30', '40', '50'],
     'optional': True, 'method': 'greedy_bastard', 'replayable': True},

# ================================================================================================

    {'name': HERPES_KISS, 'color': purple, 'sleep': 3, 'theme': None,
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

    {'name': LOST_GOLD_P1, 'stage': 1, 'color': blue, 'sleep': 3, 'theme': None,
     'areas': [a.CITY], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """You smell the overwhelming stench of brine-soaked jines...

Pirate: Argh! I lost me gold.
Tell me matey, wher' can I find me gold?
""",
     'choices': ['Cave', 'City', 'Forest', 'Swamp'],
     'optional': False, 'method': 'lost_gold_p1', 'replayable': False,
     'related': [LOST_GOLD_P2]},

# ================================================================================================

    {'name': LOST_GOLD_P2, 'stage': 2, 'color': red, 'sleep': 3, 'theme': None,
     'areas': [a.CITY], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """You smell a familiar stench...

Pirate: Argh! You lied to me, matey.
I searched for me gold and came up dry!

Give me coin or I'll shoot ya right in yer jines.
Aye, and if yer dry, a tench filet would also do.
""",
     'choices': ['Give Coin (50)', 'Give Tench Filet', 'Beg for Mercy'],
     'optional': False, 'method': 'lost_gold_p2', 'replayable': False,
     'related': [LOST_GOLD_P1]},

# ================================================================================================

    {'name': NEWS_HEADLESS_WHORES_MAN, 'color': '', 'sleep': 3, 'theme': None,
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

# ================================================================================================

    {'name': NEWS_HOHKKEN_ENTERS_CITY, 'color': '', 'sleep': 3, 'theme': None,
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

# ================================================================================================

    {'name': NEWS_WHALE_MAN, 'color': '', 'sleep': 3, 'theme': None,
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

# ================================================================================================

    {'name': WEDNESDAY_NEWS, 'color': '', 'sleep': 3, 'theme': None,
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

    {'name': PROBING, 'color': green, 'sleep': 3, 'theme': None,
     'areas': [a.CITY, a.FOREST, a.SWAMP], 'time': [NIGHT], 'moon': None, 'season': None,
     'text': """You were abducted by aliens!

Perverto: Are you ready for your probing?

What do you do?
""",
     'choices': ['Accept Probe', 'Attempt to Probe the Aliens', 'Try to Escape'],
     'optional': False, 'method': 'probing', 'replayable': True},

# ================================================================================================

    {'name': SANTAS_SNOW, 'color': white, 'sleep': 3, 'theme': None,
     'areas': [a.CITY], 'time': [NIGHT], 'moon': None, 'season': None,
     'text': """A sad, old, fat man with a huge bulge descends from the sky.

Santa: The only thing better than a hole in the sled...
Is a hole in the head.

I think I left my Snow in the Cave...
""",
     'choices': [],
     'optional': True, 'method': 'santas_snow', 'replayable': False},

# ================================================================================================

    {'name': SHEBOKKEN_ROULETTE, 'color': purple, 'sleep': 3, 'theme': ROULETTE_THEME,
     'areas': [a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """A leather-skinned man approaches you, revolver in hand.

Man: I reckon it's high time for a round of Shebokken Roulette.
One bullet, two blindfolds.

What's your wager?
""",
     'choices': ['10', '20', '30', '40', '50'],
     'optional': False, 'method': 'shebokken_roulette', 'replayable': True},

# ================================================================================================

    {'name': STINGY_BASTARD, 'color': purple, 'sleep': 3, 'theme': None,
     'areas': [a.CAVE, a.CITY, a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """An old woman with two noses and three nostrils approaches you.

Old Woman: Hey! You there!

I need coin...

How much will you give me? Hehehe.
""",
     'choices': ['10', '20', '30', '40', '50'],
     'optional': True, 'method': 'stingy_bastard', 'replayable': True},

# ================================================================================================

    {'name': THREE_HOLES, 'color': purple, 'sleep': 3, 'theme': None,
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

    {'name': TRIPLE_TENCH_DARE, 'color': yellow, 'sleep': 3, 'theme': None,
     'areas': [a.CITY, a.FOREST, a.SWAMP], 'time': [DAY], 'moon': None, 'season': None,
     'text': """A rambunctious boy approaches you, dad's wallet in hand...
     
He triple-tench-dares you to stare at the sun.
For every second, he will give you 5 of coin.

How many seconds?
""",
     'choices': ['5', '10', '15', '20'],
     'optional': True, 'method': 'triple_tench_dare', 'replayable': True},

# ================================================================================================

    {'name': ZONKED, 'color': purple, 'sleep': 3, 'theme': None,
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

{'name': OILY_DOILY_INTRO, 'color': red, 'sleep': 3, 'theme': HOSPITAL_THEME,
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

# ================================================================================================

    {'name': BASTA_INTRO, 'color': red, 'sleep': 3, 'theme': BATTLE_THEME,
     'areas': [a.CITY], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """A pair of hands clutches your shirt and pulls you into an alleyway...

As your eyes adjust, it becomes apparent that it is a man with tench eyes.

Basta Sherman: Look, your dad, The Mayor, hired me to kill you.
He propositioned me immediately after the Crispy Daniels murder trial.

The thing is, he only offered me a measly 50 coins... 
I guess Biltmore must have tightened the purse strings on him.

Anyway, being that he's your dad, and that him putting a hit on you
is pretty fucked up, I will spare you this time if you can match his offer.

What's it gonna be, Mr. Son of Mayor? 
""",
     'choices': ['Pay Up', 'Run Away'],
     'optional': False, 'method': 'basta_deal', 'replayable': False},

# ================================================================================================

    {'name': SLENDER_INTRO, 'color': red, 'sleep': 3, 'theme': HOSPITAL_THEME,
     'areas': [a.FOREST], 'time': [NIGHT], 'moon': None, 'season': None,
     'text': """Stumbling through the dark forest, you feel you're being followed...

You turn around, but nothing is there.

You turn around again - nothing.

You fake turn around, and then suddenly fully turn around, and there it is.

A faceless, 10-foot tall creature in a tailored suit stands before you -
its interests and motivations perfectly ambiguous.

Suddenly, an array of pitch-black tentacles emerge from its back and
begin wriggling violently.

What do you do?
""",
     'choices': ['Fill Dipe', 'Bail'],
     'optional': False, 'method': 'slender_intro', 'replayable': False},

# ================================================================================================

{'name': DEATH_WORM_INTRO, 'color': red, 'sleep': 3, 'theme': None,
     'areas': [a.CAVE], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """You feel the damp floor of the cave begin to shake...

Stalactites fall and crumble...

Worms and mole people scurry back to their holes...

You jump aside as the ceiling caves in, allowing for a blinding ray of light to shine down.

Bursting through the ground, illuminated by the light, is the very thing your demented grandma
would never shut up about.

You adjust your jines and prepare for the inevitable...
""",
     'choices': ['Battle the Death Worm'],
     'optional': False, 'method': 'death_worm_intro', 'replayable': False},

# ================================================================================================

{'name': CYCLOPS_INTRO, 'color': red, 'sleep': 3, 'theme': None,
     'areas': [a.CAVE], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """You feel something off about the latest tunnel you ventured into...

Like there is someone, or something, watching your every movement -

Listening to your every thought like its music.

You rotate your head as far as you can, straining your neck, to scan your pitch-black surroundings.

Suddenly, you see movement... you see... a giant, bloodshot eyeball, slowly revealed by the opening
of two enormous eyelids. 

The creature quickly rises to its feet and begins charging towards you.

What do you do?
""",
     'choices': ['Battle the Cyclops', 'Try to Escape'],
     'optional': False, 'method': 'death_worm_intro', 'replayable': False},

# ================================================================================================

{'name': SABERTOOTH_LIGER_INTRO, 'color': red, 'sleep': 3, 'theme': None,
     'areas': [a.CAVE], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """Something tackles you from behind...

You flip over and a pair of claws digs into your jines.

Before your eyes can make out what it is that's attacking you...

It lets out an Earth-shaking roar that can only be from one thing -
a Sabertooth Liger. 
""",
     'choices': ['Battle the Sabertooth Liger'],
     'optional': False, 'method': 'sabertooth_liger_intro', 'replayable': False},

# ================================================================================================

{'name': GIANT_MUTANT_RAT_INTRO, 'color': red, 'sleep': 3, 'theme': None,
     'areas': [a.CITY], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """Searching for Chula in the back of Renaldo's Pizzeria -

an establishment you have dreamt of one day calling your own -

you hear the unmistakable sound of giant feet shuffling behind the kitchen door...

Suddenly, an gigantic rodent bursts into the room, throwing you into the pizza oven.

The creature itself is covered in pizza residue, so you cannot help but suspect that it 
wishes to bake you into a pizza pie for its consumption.

It tries to speak, and nearly does, but its rodent vocal chords haven't mutated enough
for that level of communication.

Nonetheless, this monstrosity has been waiting for someone to cook and eat,
and you arrived right on time.
""",
     'choices': ['Battle the Giant Mutant Rat'],
     'optional': False, 'method': 'giant_mutant_rat_intro', 'replayable': False},

# ================================================================================================

{'name': SEWER_GATOR_INTRO, 'color': green, 'sleep': 3, 'theme': None,
     'areas': [a.CITY], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """Swimming through the sewers underneath the streets of Shebokken,

you begin to smell something especially rotten...

it's neither poop, nor trash, nor a decaying human body.

Everyone in Shebokken knows those smells well, and this particular smell is 
definitely something different... something new.

You swim a little more and feel something large brush against your jines.

You've brushed against enough poop, trash, and decaying human bodies to 
know that this was something different... something new.

You feel sharp teeth latch onto your jines, and in an instant, you are submerged
beneath the chunky surface.

Struggling, you manage to break free, now resting on the metal platform.

A creature bursts from the water and joins you, clearly ready for its next meal.
""",
     'choices': ['Battle the Sewer Gator'],
     'optional': False, 'method': 'sewer_gator_intro', 'replayable': False},

]