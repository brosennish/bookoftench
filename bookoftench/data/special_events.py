from bookoftench.data import areas as a
from bookoftench.data.audio import ROULETTE_THEME, HOSPITAL_THEME, BATTLE_THEME
from bookoftench.data.environment import DAY, NIGHT
from bookoftench.data.investments import SEMEN_CANDLE, SUN_SUITS, BOBS_BOXES, MAIL_ORDER_EGGS
from bookoftench.ui import green, purple, yellow, blue, red, orange, cyan

# ================================================================================================

# Types
BOSS_INTRO = "Boss Intro"
INVESTMENT = "Investment"
JOKE = "Joke"
NEWS = "News"
NORMAL = "Normal"

# ================================================================================================

# Normal
GREEDY_BASTARD = "Greedy Bastard"
HERPES_KISS = "Herpes Kiss"
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
NEWS_WHALE_MAN = "News Whale Man"
WEDNESDAY_NEWS = "Wednesday News"

# Boss Intro
BASTA_INTRO = "Basta Intro"
CYCLOPS_INTRO = "Cyclops Intro"
DEATH_WORM_INTRO = "Death Worm Intro"
FAIRY_CODMOTHER_INTRO = "Fairy Codmother Intro"
GIANT_MUTANT_RAT_INTRO = "Giant Mutant Rat Intro"
HODAG_INTRO = "Hodag Intro"
LUCKY_THE_LEPRECHAUN_INTRO = "Lucky The Leprechaun Intro"
MOTHMAN_INTRO = "Mothman Intro"
OGRE_INTRO = "Ogre Intro"
OILY_DOILY_INTRO = "Oily Doily Intro"
SABERTOOTH_LIGER_INTRO = "Sabertooth Liger Intro"
SASQUATCH_INTRO = "Sasquatch Intro"
SEWER_GATOR_INTRO = "Sewer Gator Intro"
SKUNK_APE_INTRO = "Skunk Ape Intro"

# Investment
BOB_ROBERTSON_PROPOSAL = "Bob Robertson Proposal"
MAIL_ORDER_EGGS_PROPOSAL = "Mail Order Eggs Proposal"
SEMEN_CANDLE_PROPOSAL = "Semen Candle Proposal"
SUN_SUITS_PROPOSAL = "Sun Suits Proposal"

# Joke
SANTAS_SNOW = "Santa's Snow"

# ================================================================================================

Special_Events = [

    {'name': GREEDY_BASTARD, 'color': purple, 'sleep': 3, 'theme': None, 'type': NORMAL,
     'areas': [a.CITY, a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """An old woman with wrinkled eyeballs wearing a soiled cloak approaches you.

Old Woman: Hey! You there! 

I have coin...

How much do you want? Hehehe.
""",
     'choices': ['10', '20', '30', '40', '50'],
     'optional': True, 'method': 'greedy_bastard', 'replayable': True},

# ================================================================================================

    {'name': HERPES_KISS, 'color': purple, 'sleep': 3, 'theme': None, 'type': NORMAL,
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

    {'name': LOST_GOLD_P1, 'stage': 1, 'color': yellow, 'sleep': 3, 'theme': None, 'type': NORMAL,
     'areas': [a.CITY], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """You smell the overwhelming stench of brine-soaked jines...

Pirate: Argh! I lost me gold.
Tell me matey, wher' can I find me gold?
""",
     'choices': ['Cave', 'City', 'Forest', 'Swamp'],
     'optional': False, 'method': 'lost_gold_p1', 'replayable': False,
     'related': [LOST_GOLD_P2]},

# ================================================================================================

    {'name': LOST_GOLD_P2, 'stage': 2, 'color': red, 'sleep': 3, 'theme': None, 'type': NORMAL,
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

    {'name': NEWS_HEADLESS_WHORES_MAN, 'color': orange, 'sleep': 3, 'theme': None, 'type': NEWS,
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

    {'name': NEWS_HOHKKEN_ENTERS_CITY, 'color': orange, 'sleep': 3, 'theme': None, 'type': NEWS,
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

    {'name': NEWS_WHALE_MAN, 'color': orange, 'sleep': 3, 'theme': None, 'type': NEWS,
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

    {'name': WEDNESDAY_NEWS, 'color': orange, 'sleep': 3, 'theme': None, 'type': NEWS,
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

    {'name': PROBING, 'color': green, 'sleep': 3, 'theme': None, 'type': NORMAL,
     'areas': [a.CITY, a.FOREST, a.SWAMP], 'time': [NIGHT], 'moon': None, 'season': None,
     'text': """You were abducted by aliens!

Perverto: Are you ready for your probing?

What do you do?
""",
     'choices': ['Accept Probe', 'Attempt to Probe the Aliens', 'Try to Escape'],
     'optional': False, 'method': 'probing', 'replayable': True},

# ================================================================================================

    {'name': SANTAS_SNOW, 'color': blue, 'sleep': 3, 'theme': None, 'type': JOKE,
     'areas': [a.CITY], 'time': [NIGHT], 'moon': None, 'season': None,
     'text': """A sad, old, fat man with a huge bulge descends from the sky.

Santa: The only thing better than a hole in the sled...
Is a hole in the head.

I think I left my Snow in the Cave...
""",
     'choices': [],
     'optional': True, 'method': 'santas_snow', 'replayable': False},

# ================================================================================================

    {'name': SHEBOKKEN_ROULETTE, 'color': purple, 'sleep': 3, 'theme': ROULETTE_THEME, 'type': NORMAL,
     'areas': [a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """A leather-skinned man approaches you, revolver in hand.

Man: I reckon it's high time for a round of Shebokken Roulette.
One bullet, two blindfolds.

What's your wager?
""",
     'choices': ['10', '20', '30', '40', '50'],
     'optional': False, 'method': 'shebokken_roulette', 'replayable': True},

# ================================================================================================

    {'name': STINGY_BASTARD, 'color': purple, 'sleep': 3, 'theme': None, 'type': NORMAL,
     'areas': [a.CAVE, a.CITY, a.FOREST, a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """An old woman with two noses and three nostrils approaches you.

Old Woman: Hey! You there!

I need coin...

How much will you give me? Hehehe.
""",
     'choices': ['10', '20', '30', '40', '50'],
     'optional': True, 'method': 'stingy_bastard', 'replayable': True},

# ================================================================================================

    {'name': THREE_HOLES, 'color': purple, 'sleep': 3, 'theme': None, 'type': NORMAL,
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

    {'name': TRIPLE_TENCH_DARE, 'color': yellow, 'sleep': 3, 'theme': None, 'type': NORMAL,
     'areas': [a.CITY, a.FOREST, a.SWAMP], 'time': [DAY], 'moon': None, 'season': None,
     'text': """A rambunctious boy approaches you, dad's wallet in hand...

He triple-tench-dares you to stare at the sun.
For every second, he will give you 5 of coin.

How many seconds?
""",
     'choices': ['5', '10', '15', '20'],
     'optional': True, 'method': 'triple_tench_dare', 'replayable': True},

# ================================================================================================

    {'name': ZONKED, 'color': purple, 'sleep': 3, 'theme': None, 'type': NORMAL,
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

    {'name': OILY_DOILY_INTRO, 'color': red, 'sleep': 3, 'theme': HOSPITAL_THEME, 'type': BOSS_INTRO,
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
     'optional': False, 'method': 'oily_doily_intro', 'replayable': False},

# ================================================================================================

    {'name': BASTA_INTRO, 'color': red, 'sleep': 3, 'theme': BATTLE_THEME, 'type': BOSS_INTRO,
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
     'optional': False, 'method': 'basta_intro', 'replayable': False},

# ================================================================================================

    {'name': DEATH_WORM_INTRO, 'color': red, 'sleep': 3, 'theme': BATTLE_THEME, 'type': BOSS_INTRO,
     'areas': [a.CAVE], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """You feel the damp floor of the cave begin to shake...

Stalactites fall and crumble...

Worms and mole people scurry back to their holes...

You jump aside as the ceiling caves in, allowing for a blinding ray of light to shine down.

Bursting through the ground, illuminated by the light, is the very thing your demented grandma
would never shut up about.

You adjust your jines and prepare for the inevitable...
""",
     'choices': ['Battle Death Worm'],
     'optional': False, 'method': 'death_worm_intro', 'replayable': False},

# ================================================================================================

    {'name': CYCLOPS_INTRO, 'color': red, 'sleep': 3, 'theme': BATTLE_THEME, 'type': BOSS_INTRO,
     'areas': [a.CAVE], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """You feel something off about the latest tunnel you ventured into...

Like there is someone, or something, watching your every movement -

Listening to your every thought like it's sad, dried out music.

You rotate your head as far as you can, straining your neck, to scan your pitch-black surroundings.

Suddenly, you see movement... you see... a giant, bloodshot eyeball, slowly revealed by the opening
of two enormous eyelids. 

The creature quickly rises to its feet and begins charging towards you.

What do you do?
""",
     'choices': ['Battle Cyclops', 'Try to Escape'],
     'optional': False, 'method': 'cyclops_intro', 'replayable': False},

# ================================================================================================

    {'name': SABERTOOTH_LIGER_INTRO, 'color': red, 'sleep': 3, 'theme': BATTLE_THEME, 'type': BOSS_INTRO,
     'areas': [a.CAVE], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """Something tackles you from behind...

You flip over and a pair of claws digs into your jines.

Before your eyes can make out what it is that's attacking you...

It lets out an Earth-shaking roar that can only be from one thing -
a Sabertooth Liger. 
""",
     'choices': ['Battle Sabertooth Liger'],
     'optional': False, 'method': 'sabertooth_liger_intro', 'replayable': False},

# ================================================================================================

    {'name': GIANT_MUTANT_RAT_INTRO, 'color': red, 'sleep': 3, 'theme': BATTLE_THEME, 'type': BOSS_INTRO,
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
     'choices': ['Battle Giant Mutant Rat'],
     'optional': False, 'method': 'giant_mutant_rat_intro', 'replayable': False},

# ================================================================================================

    {'name': SEWER_GATOR_INTRO, 'color': green, 'sleep': 3, 'theme': BATTLE_THEME, 'type': BOSS_INTRO,
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
     'choices': ['Battle Sewer Gator'],
     'optional': False, 'method': 'sewer_gator_intro', 'replayable': False},

# ================================================================================================

    {'name': LUCKY_THE_LEPRECHAUN_INTRO, 'color': green, 'sleep': 3, 'theme': BATTLE_THEME, 'type': BOSS_INTRO,
     'areas': [a.FOREST], 'time': [DAY], 'moon': None, 'season': None,
     'text': """Lucky the Leprechaun: Suck me jines,

I'm a leprechaun!

Yer not gettin' a drop of me precious gold!'

Tehehehehehehe.

If yer lucky, ye won't end up in Hell when I'm through with ya!

And ye know what else?

Ye can suck me jines,
'cause I'm a leprechaun!
""",
     'choices': ['Battle Lucky the Leprechaun'],
     'optional': False, 'method': 'lucky_the_leprechaun_intro', 'replayable': False},

# ================================================================================================

    {'name': FAIRY_CODMOTHER_INTRO, 'color': purple, 'sleep': 3, 'theme': BATTLE_THEME, 'type': BOSS_INTRO,
     'areas': [a.FOREST], 'time': [DAY], 'moon': None, 'season': None,
     'text': """Walking through the quiet forest,

You begin to hear the faint sound of whistling in the distance.

Looking and searching for the source, it suddenly becomes deafening,
as if it someone is whistling through a megaphone directly into your earhole.

After a moment, it's even quieter than it was to begin with. 

A moment later, it is the loudest its been, with you covering your ears in
excruciating pain.

Then, silence.

A mist of sparkles appears before you.

From the sparkly mist emerges an unfamiliar being...

Fairy Codmother: Mm... hehe. You think you's comin' into my forest,

and you's not gettin' a piece of me?

Mm... hehe. 

Come on, now. I have very important things to attend to... 

Mmmm... hehehe.
""",
     'choices': ['Battle Fairy Codmother'],
     'optional': False, 'method': 'fairy_codmother_intro', 'replayable': False},

# ================================================================================================

    {'name': MOTHMAN_INTRO, 'color': purple, 'sleep': 3, 'theme': BATTLE_THEME, 'type': BOSS_INTRO,
     'areas': [a.FOREST], 'time': [NIGHT], 'moon': None, 'season': None,
     'text': """Walking down a lonesome forest road,

You hear a loud flapping sound behind you, and it sounds like it's growing closer.

Turning around, you are snatched up by a large, muscular man with insectoid 
features and large, webbed wings.

You bite into its strong hands, causing it to drop you into the adjacent field.

Without saying a word, it quickly circles back and lands before you, ready for combat.
""",
     'choices': ['Battle Mothman'],
     'optional': False, 'method': 'mothman_intro', 'replayable': False},

# ================================================================================================

    {'name': SASQUATCH_INTRO, 'color': purple, 'sleep': 3, 'theme': BATTLE_THEME, 'type': BOSS_INTRO,
     'areas': [a.FOREST], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """You stop to relieve yourself next to a batch of toadstools...

While squeezing, you hear the pleasing sound of a saxophone being played from the bush.

Curious, you make your way over to see who is playing the funky music.

As you pull the bush open to look through, the music suddenly stops.

Before you can think of your next move, a large, smelly, hairy brown head 
pops up on the other side,

and it does not look happy...
""",
     'choices': ['Battle Sasquatch'],
     'optional': False, 'method': 'sasquatch_intro', 'replayable': False},

# ================================================================================================

    {'name': SKUNK_APE_INTRO, 'color': purple, 'sleep': 3, 'theme': BATTLE_THEME, 'type': BOSS_INTRO,
     'areas': [a.SWAMP], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """You sit down for a quick rest...

You'll find Chula eventually, nothing wrong with a quick break.

Simultaneously, you've overcome by both an atrocious stench and 
horrible sound, the sound of someone - or something - trying
to play the saxophone and failing miserably.

Before you can go to investigate, a large, shaggy being rips through
the bush and charges at you.

It has an absolutely bewildered look in its eye, like its capable of
any wrongdoing without any risk of later remorse.
""",
     'choices': ['Battle Skunk Ape'],
     'optional': False, 'method': 'skunk_ape_intro', 'replayable': False},

# ================================================================================================

    {'name': OGRE_INTRO, 'color': green, 'sleep': 3, 'theme': BATTLE_THEME, 'type': BOSS_INTRO,
     'areas': [a.SWAMP], 'time': [DAY], 'moon': None, 'season': None,
     'text': """Bushwhacking through a section of especially dense bush...

You take a wrong step and lose your balance.

Unable to brace your fall, your head bumps against a small boulder
and you lose consciousness.

After an uncertain amount of time, you awaken. 

Looking around, you are on a small bed in a small cottage with a large pot of
boiling water over an open flame.

Before you can look for the door and try to leave,
a towering being enters the room.

As you search for words to navigate the situation,
the being becomes increasingly distressed.

Then, without warning, it lets out a mighty roar, rip off its handmade shirt,
and aggressively stomps towards you.
""",
     'choices': ['Battle Ogre'],
     'optional': False, 'method': 'ogre_intro', 'replayable': False},

# ================================================================================================

    {'name': HODAG_INTRO, 'color': red, 'sleep': 3, 'theme': BATTLE_THEME, 'type': BOSS_INTRO,
     'areas': [a.SWAMP], 'time': [NIGHT], 'moon': None, 'season': None,
     'text': """Trying to spot Chula in the swampy dead of night,

an intimidating silhouette emerges from the brush.

Tired of confrontation, you turn away and hope that, whatever
it is, it loses interest.

Moments later, you hear loud trampling heading towards you from behind. 

Before you can turn around, it knocks you to the muck and jumps on top of you.

Your headlamp flickers on and reveals a massive set of razor sharp teeth
and a large set of eyes, each looking in a different direction.

It roars and attempts to bite off your head, and just as it does so, 
you seize an opportunity to roll over and escape.

It immediately recovers and tramples at you again.
""",
     'choices': ['Battle Hodag'],
     'optional': False, 'method': 'hodag_intro', 'replayable': False},

# ================================================================================================

    {'name': SEMEN_CANDLE_PROPOSAL, 'color': cyan, 'sleep': 3, 'theme': None, 'type': INVESTMENT,
     'areas': [a.CITY], 'time': [DAY, NIGHT], 'moon': None, 'season': None,
     'text': """You encounter a man in a condom costume with a fake flame on his head...

Semen Candle Rep: What's your name, there?

You tell him your name.

Semen Candle Rep: No matter, I'll just call you Jeffrey if that's alright.

You nod.

Semen Candle Rep: Let me ask you, old sport, if a candle were to smell like you,
would it smell like your hair? Maybe your pits? Your seed?

You shrug.

Semen Candle Rep: Very good, it would smell of your seed, and, indeed, it is your
lucky day, as I wish to cordially invite you to get in on the ground floor of 
Shebokken's next and last favorite candle - Semen Candle!

Soon, the scent of man, the stench of potential offspring, and the sweet smell of jines
will fill every room in this terrible city.

So, we have four investment opportunities...

Investment: Semen Candle
Risk: High
Potential Return: 4x-8x
Maturity: 3-4 Levels
""",
     'choices': ['Invest 10', 'Invest 25', 'Invest 50', 'Invest 100'],
     'investment': SEMEN_CANDLE,
     'optional': True, 'method': 'make_investment', 'replayable': False},

# ================================================================================================

    {'name': SUN_SUITS_PROPOSAL, 'color': cyan, 'sleep': 3, 'theme': None, 'type': INVESTMENT,
     'areas': [a.CITY], 'time': [DAY], 'moon': None, 'season': None,
     'text': """You encounter a man who appears to be completely naked...

Sun Suits Rep: Don't be alarmed! I am fully clothed, so there is no need for alarm.

You point to the man's jines, clearly visible in the beating sun.

Sun Suits Rep: Are you tired of spraying sunscreen on your tasty little arms?
Are you sick of having to ask strangers to rub lotion on your jines and rump,
just because it's such a chore for you to do it yourself?

You hesitate, then nod.

Sun Suits Rep: Well fret no more! My company has invented a revolutionary new way
to protect yourself from those pesky UV rays.

You raise an eyebrow in curiosity.

Sun Suits Rep: The answer to your problem is what I am wearing at this very moment...
Sun Suits! Sun Suits are transparent, elastic, and washable. 

Stop burning through gallons of sunblock and join us as an early investor today! 

We have four investment options, and remember, it's now or never, boy.

Investment: Sun Suits
Risk: Medium
Potential Return: 2x-4x
Maturity: 2-3 Levels
""",
     'choices': ['Invest 10', 'Invest 25', 'Invest 50', 'Invest 100'],
     'investment': SUN_SUITS,
     'optional': True, 'method': 'make_investment', 'replayable': False},

# ================================================================================================

    {'name': BOB_ROBERTSON_PROPOSAL, 'color': cyan, 'sleep': 3, 'theme': None, 'type': INVESTMENT,
     'areas': [a.CITY], 'time': [DAY], 'moon': None, 'season': None,
     'text': """A gangly, nervous man with 70's glasses and a Goodwill button-up approaches you...

Bob Robertson: Hi there. I'm, uh, Bob Robertson.

So, yes. Uh... recently, I started up my own door-to-door, uh, cardboard box delivery business.

However, I'm... uh... having some difficulties, both financial and otherwise.

You know, I don't have a, uh, car, so... I have to deliver on foot, yes.

Many times, folks have pulled knives and related weaponry on me when I've knocked on their entryways.

I'm looking for investors to provide funding that I can use to, uh, buy a new pair of shoes, as well as
a bladed weapon of sorts in order to protect myself and my, uh, jines, yes.

Anyway, if you could invest any of the following amounts, I will do my best to give you a, uh, 
real good return on investment there, yes.

Investment: Bob Robertson's Door-to-Door Cardboard Box Delivery Business
Risk: High
Potential Return: 4x-8x
Maturity: 3-4 Levels
""",
     'choices': ['Invest 10', 'Invest 25', 'Invest 50', 'Invest 100'],
     'investment': BOBS_BOXES,
     'optional': True, 'method': 'make_investment', 'replayable': False},

# ================================================================================================

    {'name': MAIL_ORDER_EGGS_PROPOSAL, 'color': cyan, 'sleep': 3, 'theme': None, 'type': INVESTMENT,
     'areas': [a.CITY], 'time': [DAY], 'moon': None, 'season': None,
     'text': """A man in an Vladymir Georgina suit approaches you...

Mail Order Egg Rep: What's more trustworthy than the Shebokken Postal Service?
Your local green grocer? I don't fuckin' think so.

I mean, don't you just fuckin' hate your local green grocer?

You know I do. 

Look, are you tired of having some drunk piece of shit delivery bozo 
smashing up the cases of eggs that you worked your tail off just to afford
so you can feed your gut hut?

You're looking out the window, so happy they finally came, until you see this
behemoth lift up sixteen cases of eggs and carelessly drop them right on your
driveway. Then, when you confront him about it, he threatens to rip your limbs
off, and there's nothing you can do - and you know it.

So what's the answer to that? Mail Order Eggs, of course!

On-time, white-glove delivery, a refined, elegant man or woman will arrive 
to your mailbox and place the eggs inside with the same care and tact they would
if it were a golden tench.

We are seeking investors to get in on this before it becomes the biggest thing
since Crabs on Rye.

What do you say?

Investment: Mail Order Eggs
Risk: Medium
Potential Return: 2x-4x
Maturity: 2-3 Levels
""",
     'choices': ['Invest 10', 'Invest 25', 'Invest 50', 'Invest 100'],
     'investment': MAIL_ORDER_EGGS,
     'optional': True, 'method': 'make_investment', 'replayable': False},

]