from bookoftench.data.areas import CAVE, CITY, FOREST, SWAMP
from bookoftench.data.special_events import SANTAS_SNOW

# ================================================================================================

COMMON = "Common"
UNCOMMON = "Uncommon"
RARE = "Rare"
LEGENDARY = "Legendary"
MYTHIC = "Mythic"

# ================================================================================================

Search_Discoverables = [

    # ============================
    #       COMMON / POSITIVE
    # ============================

    {"pre": "an", "name": "Abandoned Undergarments", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "Someone forgot to dipe up..."},

    {"pre": "an", "name": "Adult Binky", "value": 1, "hp": 0, "rarity": COMMON,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "Wreaks of moonshine and toad juice."},

    {"pre": "some", "name": "Ants on a Log", "value": 1, "hp": 3, "rarity": COMMON,
     "areas": [FOREST, SWAMP], 
     "desc": "The perfect appetizer for any formal occasion."},

    {"pre": "a", "name": "Broken Compass", "value": 2, "hp": 0, "rarity": COMMON,
     "areas": [FOREST, SWAMP], 
     "desc": "Hm... it only points towards my jines?"},

    {"pre": "a", "name": "Bum Firework", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "I share at least one thing in common with this firework... impotence."},

    {"pre": "a", "name": "Bunless Hot Dog", "value": 1, "hp": 5, "rarity": COMMON,
     "areas": [FOREST, SWAMP], 
     "desc": "Swallow it whole if you know what's good for ya's."},

    {"pre": "a", "name": "Camel Toad", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Manifests in multiple shapes and sizes."},

    {"pre": "some", "name": "Cattails", "value": 0, "hp": 1, "rarity": COMMON,
     "areas": [SWAMP], 
     "desc": "The locusts add an exquisite flavor that complements the texture."},

    {"pre": "a", "name": "Cigarette Butt", "value": 1, "hp": 1, "rarity": COMMON,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "Score!"},

    {"pre": "a", "name": "Clog Consultant Coupon", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "He evaluates the clog to provide an estimate on how long it will take to clear on its own."},

    {"pre": "a", "name": "Cockroach", "value": 0, "hp": 3, "rarity": COMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Not the most popular insect, but perhaps the most indestructible."},

    {"pre": "a", "name": "Corrupted Floppy Disk", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Floppy discs aren't designed to hold that much pirated, low-res porn..."},

    {"pre": "a", "name": "Deer Antler", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [FOREST], 
     "desc": "Could also be from the Wendigo."},

    {"pre": "some", "name": "Detritus", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Nothing special in this particular pile of detrite."},

    {"pre": "a", "name": "Dipstick", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Used to check your current poop levels - doesn't work on cars."},

    {"pre": "a", "name": "Disposable Camera", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "Why would anyone dispose of this?"},

    {"pre": "a", "name": "Doily", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Would go great with some boiling oil."},

    {"pre": "a bunch of", "name": "Empty White Wine Bottles", "value": 7, "hp": 0, "rarity": COMMON,
     "areas": [CAVE, CITY], 
     "desc": "Shrimp casings and vomit... everywhere."},

    {"pre": "an", "name": "Empty Flask", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Does anyone ever find a filled flask?"},

    {"pre": "a", "name": "Fake Tomato", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Tough luck."},

    {"pre": "a", "name": "Feathered Fedora", "value": 7, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "To be, or not to be... a douche."},

    {"pre": "some", "name": "Frog Eggs", "value": 4, "hp": 5, "rarity": COMMON,
     "areas": [FOREST, SWAMP], 
     "desc": "I wish I was a frog... no... yeah, I wish I was a frog."},

    {"pre": "a", "name": "Heavily-Used CD Player", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "Something tells me that this was used exclusively for spinning Slade's third album."},

    {"pre": "a", "name": "Hot Dog Burger", "value": 5, "hp": 8, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "The most American thing imaginable."},

    {"pre": "some", "name": "Hair Plugs", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [CITY],
     "desc": "Would be a shame to let these go to waste..."},

    {"pre": "a", "name": "Leather Boot", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [FOREST, SWAMP], 
     "desc": "Should be taken to the Shebokken Leathermeister post haste."},

    {"pre": "a", "name": "Mobile Dump Coupon", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "For when you're on the go and gotta go with nowhere to go."},

    {"pre": "a", "name": "Nearly Unscathed Corn Dog", "value": 2, "hp": 5, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "But the scathing is not good... not good at all."},

    {"pre": "some", "name": "Nectar", "value": 1, "hp": 2, "rarity": COMMON,
     "areas": [FOREST, SWAMP], 
     "desc": "Nectar is the bees knees. Wait, do bees have knees?"},

    {"pre": "an", "name": "Oily Doily's Coupon", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "You'd regret using this if a corpse could have regrets."},

    {"pre": "a", "name": "Pair of Sunglasses", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Not today, sun... not today. I can't speak for tomorrow, but today is not the day."},

    {"pre": "a", "name": "Push Music CD", "value": 4, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Jan Terri... a solid choice for a birthing mix."},

    {"pre": "a", "name": "Rat", "value": 0, "hp": 6, "rarity": COMMON,
     "areas": [CITY],
     "desc": "Shebokken's other furry, trash-eating residents."},

    {"pre": "some", "name": "Sap", "value": 2, "hp": 2, "rarity": COMMON,
     "areas": [FOREST, SWAMP], 
     "desc": "Only saps drink sap. Does that make me a cannibal?"},

    {"pre": "a", "name": "Sandal", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [CITY, FOREST], 
     "desc": "Great for slapping faces."},

    {"pre": "a", "name": "Slice of Medical Pizza", "value": 0, "hp": 6, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Consists of scabs, bandages, unidentifiable fluids, yeast, and blood for the sauce."},

    {"pre": "some", "name": "Slime", "value": 0, "hp": 3, "rarity": COMMON,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "This appears to be slime on account of its innate sliminess."},

    {"pre": "some", "name": "Slop", "value": 1, "hp": 5, "rarity": COMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "My mom slopped till she popped. She ate nothing but slop while I was in her gut hut."},

    {"pre": "a", "name": "Pair of Swim Goggles", "value": 4, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "In case it rains or floods, obviously."},

    {"pre": "a", "name": "Pepperoni Salad", "value": 2, "hp": 7, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "A caesar salad covered with delicious pepperonis."},

    {"pre": "some", "name": "Remains", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Forensics would have no chance at identifying these remains."},

    {"pre": "some", "name": "Rope", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "Appeared to be used in church-oriented, sexual activities."},

    {"pre": "a", "name": "Squirrel's Stash", "value": 3, "hp": 6, "rarity": COMMON,
     "areas": [FOREST], 
     "desc": "Mostly peanuts but also several human fingers and testicles."},

    {"pre": "a", "name": "Three-Wheeled Skateboard", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Made for a man with three legs."},

    {"pre": "a", "name": "Toast Roaster", "value": 8, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Roasts your toast."},

    {"pre": "a", "name": "Tooth", "value": 5, "hp": 1, "rarity": COMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Not a mouth tooth."},

    {"pre": "a", "name": "Tumbleweave", "value": 2, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "The origins can be traced back to Sandusky High School."},

    {"pre": "a", "name": "Turtle Shell", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [FOREST, SWAMP], 
     "desc": "A plain yet beautiful shell of a local pond turtle."},

    {"pre": "a", "name": "Used Chapstick", "value": 1, "hp": 1, "rarity": COMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Made in Preston, Idaho?"},

    {"pre": "a", "name": "Vibrator", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Buzz off, can't you see I'm buzzing over here?"},

    {"pre": "a", "name": "Worm", "value": 1, "hp": 2, "rarity": COMMON,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "Like political leaders and celebrities - full of shit."},

    {"pre": "a", "name": "Yo-Yo With No String", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "I must find a string ASAP."},

    # ============================
    #       COMMON / NEGATIVE
    # ============================

    {"pre": "were", "name": "Attacked by a Squirrel", "value": 0, "hp": -3, "rarity": COMMON,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "It went for your nuts!"},

    {"pre": None, "name": "Fell Down a Hole", "value": 0, "hp": -6, "rarity": COMMON,
     "areas": [CAVE], 
     "desc": "Like my proctologist once said, 'Damn, that's one deep hole.'"},

    {"pre": None, "name": "Got Caught in a Bramble", "value": 0, "hp": -3, "rarity": COMMON,
     "areas": [FOREST, SWAMP], 
     "desc": "Poked my loins, poked my jines."},

    {"pre": "were", "name": "Poked by a Thorn", "value": 0, "hp": -3, "rarity": COMMON,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "Right on the tip... right on the tip."},

    {"pre": "were", "name": "Scratched by a Cat", "value": 0, "hp": -3, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Narrowly missed my jugular."},

    {"pre": None, "name": "Slipped on a Mud Pie", "value": 0, "hp": -1, "rarity": COMMON,
     "areas": [FOREST, SWAMP], 
     "desc": "It wasn't mud..."},

    {"pre": None, "name": "Stubbed your Toe", "value": 0, "hp": -3, "rarity": COMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Worse than death."},

    {"pre": "were", "name": "Stung by a Bee", "value": 0, "hp": -3, "rarity": COMMON,
     "areas": [CITY, FOREST], 
     "desc": "Right on the tip... of my nose. Call me bozo."},

    {"pre": "were", "name": "Stung by a Wasp", "value": 0, "hp": -5, "rarity": COMMON,
     "areas": [CITY, FOREST], 
     "desc": "Shouldn't have eaten it first..."},

    {"pre": None, "name": "Swallowed a Bug", "value": 0, "hp": -2, "rarity": COMMON,
     "areas": [FOREST, SWAMP], 
     "desc": "Worth it, so much gooey protein."},

    {"pre": "were", "name": "Swarmed by Mosquitos", "value": 0, "hp": -3, "rarity": COMMON,
     "areas": [FOREST, SWAMP], 
     "desc": "Narrowly avoided mosquito-transmitted herpes."},

    {"pre": None, "name": "Tagged by a Bat", "value": 0, "hp": -3, "rarity": COMMON,
     "areas": [CAVE], 
     "desc": "Guess I'm it now!"},

    {"pre": None, "name": "Tripped On the Curb", "value": 0, "hp": -2, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Yep, gotta watch my step."},

    {"pre": None, "name": "Tripped Over a Log", "value": 0, "hp": -3, "rarity": COMMON,
     "areas": [FOREST, SWAMP], 
     "desc": "That one's on me."},

    # ============================
    #       COMMON / NEUTRAL
    # ============================

    {"pre": "some", "name": "Bat Scat", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [CAVE], 
     "desc": "Droppings from above."},

    {"pre": "a", "name": "Chakra Specialist", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "A total fraud, scamming anyone they can trick into believing their pseudo-scientific bullshit."},

    {"pre": "a", "name": "Condom Brochure", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "Short for \"Condominium\"."},

    {"pre": "a", "name": "Disillusioned Man", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Sees the conventional world for what it is and does not care for it one bit."},

    {"pre": "an", "name": "Expired Riverboat Casino Voucher", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "The expiration date is before the issue date."},

    {"pre": "a", "name": "Glorious Hole", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [CITY, FOREST, SWAMP],
     "desc": "Glory be to the holiest of holes."},

    {"pre": "a", "name": "Mud Bubble", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [SWAMP], 
     "desc": "Just a big old bubbly brown mud bubble."},

    {"pre": "a", "name": "Mole Hole", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [CAVE, FOREST], 
     "desc": "There's a mole in that hole... perhaps a multitude, even."},

    {"pre": "a", "name": "Noodle Man Wanted Poster", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Noodle man arrested for eating his own bones. More at 11."},

    {"pre": "an", "name": "Orange Cat", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Exactly what you're imagining."},

    {"pre": "a", "name": "Petition to Impeach The Mayor of Shebokken", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Nearly every resident of Shebokken has signed this petition."},

    {"pre": "a", "name": "Religious Flyer", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "Ah, yes. The business of organized religion... pay us to save you."},

    {"pre": "some", "name": "Sheeple", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [CITY], 
     "desc": "They follow the herd and dare not do otherwise."},

    {"pre": "a", "name": "Slade CD", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "Came pre-scratched to spare the purchaser from having to listen to it."},

# ================================================================================================

    # ============================
    #      UNCOMMON / POSITIVE
    # ============================

    {"pre": "a", "name": "Bag of Snow", "value": 15, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE], 
     "desc": "\"Property of Santa\" is scribbled on the side."},

    {"pre": "a", "name": "Balloon Man Comic Book", "value": 11, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Balloon Man is a supervillain who kills people by tying large helium balloons to their ankles."},

    {"pre": "a", "name": "Blind Fish", "value": 3, "hp": 7, "rarity": UNCOMMON,
     "areas": [CAVE], 
     "desc": "The stench of unsuspecting snails is all it needs."},

    {"pre": "a", "name": "Blood Brothers DVD Box Set", "value": 11, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "Soap opera about two male friends who menstruate at the same time."},

    {"pre": "a", "name": "Blood Bucket", "value": 8, "hp": 8, "rarity": UNCOMMON,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "There are traces of at least ten individuals in here!?"},

    {"pre": "a", "name": "Blood Soaked Robe", "value": 3, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "Why does this blood taste like ketchup? Oh yeah, ketchup is cheaper than toad juice."},

    {"pre": "a", "name": "Bloody Neighborhood Watch Badge", "value": 3, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "This bozo got more than they bargained for... now that's a real bargain."},

    {"pre": "a", "name": "Bucket of Boiling Oil", "value": 8, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "Pairs great with a fresh doily."},

    {"pre": "some", "name": "Bush Meat", "value": 7, "hp": 10, "rarity": UNCOMMON,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "Never know what you'll find in a deep, dense bush."},

    {"pre": "a", "name": "Can of Spam", "value": 3, "hp": 8, "rarity": UNCOMMON,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "Great for a morning meal in the Alleghenies."},

    {"pre": "a", "name": "Cracked Monocle", "value": 6, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "Wonder if they were playing Monopoly when it happened?"},

    {"pre": "a", "name": "Crispy Daniels Signature Bandana", "value": 15, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "An invaluable relic of a cultural and global icon who was executed sooner than was necessary."},

    {"pre": "a", "name": "Digital Camera", "value": 15, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "All of the photos are blurry and appear to have a lot of skin in them."},

    {"pre": "an", "name": "Engraved Pocket Watch", "value": 13, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Engraved with some bozo's SoundCloud handle."},

    {"pre": "a", "name": "Fanny Pack", "value": 10, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY, FOREST], 
     "desc": "Only the coolest of cool people wear fanny packs on the daily."},

    {"pre": "a", "name": "Giant Worm", "value": 2, "hp": 6, "rarity": UNCOMMON,
     "areas": [CAVE], 
     "desc": "I mean... GIANT."},

    {"pre": "a", "name": "Grown Man's Button Collection", "value": 8, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY, FOREST], 
     "desc": "Most of the buttons are from Area 51, oddly enough. You'd think they'd glow in the dark."},

    {"pre": "a", "name": "Hand Sandwich", "value": 6, "hp": 8, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "What you think it is - a severed human hand between to slices of sourdough."},

    {"pre": "a", "name": "Human-Laid Egg", "value": 6, "hp": 9, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Straight from the snatch and ready to hatch."},

    {"pre": "a", "name": "Lava Lamp", "value": 12, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "Coolest lamp ever invented... tastiest, too."},

    {"pre": "some", "name": "Lawn Darts", "value": 8, "hp": 0, "rarity": UNCOMMON,
     "areas": [FOREST], 
     "desc": "My dad lost his first three kids in lawn darts accidents."},

    {"pre": "a", "name": "Lewd Dream Diary", "value": 5, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "The storytelling and character-development is unmatched in today's literary scene."},

    {"pre": "a vial of", "name": "Lubricare Medicinal Lube", "value": 6, "hp": 6, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "For when you need both lubrication and medication during your time of fornication."},

    {"pre": "a", "name": "Mail Order Egg", "value": 6, "hp": 8, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "An egg - vacuum sealed in a manilla envelope and hand-delivered by the post. Sublime."},

    {"pre": "a", "name": "Manly Man Comic Book", "value": 13, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Manly Man is a superhero who is not only a man but is also very manly as well."},

    {"pre": "a", "name": "Mealy Boy Comic Book", "value": 8, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Mealy Boy is Manly Man's small and impotent sidekick. He is covered in an unknown white powder."},

    {"pre": "some", "name": "Mystery Milk", "value": 6, "hp": 9, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "It's definitely milk. That much we can say for certain."},

    {"pre": "a", "name": "One-Ply Dipe", "value": 1, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Might as well go rogue, 'cause this dipe ain't gonna hold."},

    {"pre": "a", "name": "Melted FlaVorIce Pop", "value": 1, "hp": 1, "rarity": UNCOMMON,
     "areas": [CITY, SWAMP], 
     "desc": "For when you're in the mood to suck down a plastic tube of high-fructose corn syrup and petrochemicals."},

    {"pre": "a", "name": "Mineral Formation", "value": 9, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE], 
     "desc": "A phallic formation of massive proportions."},

    {"pre": "a", "name": "Pack of Clove Cigarettes", "value": 7, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "For ages -9 months and up..."},

    {"pre": "a", "name": "Pager", "value": 3, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "Great for booty calls."},

    {"pre": "a", "name": "Paper Mache Tench Balloon", "value": 15, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "Fun for all ages. May cause death or enlightenment if you're lucky."},

    {"pre": "a pair of", "name": "Paternity Pants", "value": 10, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "To help men dress comfortably while their women does all of the work."},

    {"pre": "a", "name": "Pound Cake", "value": 12, "hp": 8, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "What is a pound cake? Seriously, I don't know and refuse to look it up for no good reason."},

    {"pre": "a", "name": "Real Tomato", "value": 5, "hp": 6, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "It's your lucky day."},

    {"pre": "a pair of", "name": "Reclaimed Tom's Shoes", "value": 8, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Ever wonder what happens to the donated pair following a return?"},

    {"pre": "a", "name": "Spelling Bee Participation Trophy", "value": 1, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "The recipient lost in the first round. The word was 'i', as in me, myself, and i."},

    {"pre": "a", "name": "Spring Chicken", "value": 10, "hp": 10, "rarity": UNCOMMON,
     "areas": [FOREST], 
     "desc": "It's called a spring chicken because what it is is, well, that - a spring chicken, frankly."},

    {"pre": "a", "name": "Stained White T", "value": 5, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "What was once an unstained white t-shirt is now a stained white t-shirt. What a shame."},

    {"pre": "a", "name": "Swedish Sweet Dish", "value": 5, "hp": 10, "rarity": UNCOMMON,
     "areas": [CITY, FOREST],
     "desc": "Say it three times fast."},

    {"pre": "a", "name": "Tackle Box", "value": 9, "hp": 0, "rarity": UNCOMMON,
     "areas": [SWAMP], 
     "desc": "Full of corn, raspberry extract, and tench-sized lures."},

    {"pre": "some", "name": "Teeth", "value": 14, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Not mouth teeth, mind you..."},

    {"pre": "a", "name": "Tench Cookbook", "value": 11, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "10,000 ways to prepare a tench for consumption (including raw)."},

    {"pre": "a", "name": "Tench Light", "value": 8, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "Used for pleasuring oneself - also used as a nightlight in children's bedrooms."},

    {"pre": "a", "name": "Troglodyte", "value": 6, "hp": 10, "rarity": UNCOMMON,
     "areas": [CAVE], 
     "desc": "A cave-dwelling being, often mistaken for a cave ape. If you mess with it, it will go ape though."},

    {"pre": "an", "name": "Unlabeled Bottle of Various Pills", "value": 20, "hp": 5, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "Likely a mixture of party drugs, steroids, and erection pills."},

    # ============================
    #      UNCOMMON / NEGATIVE
    # ============================

    {"pre": "were", "name": "Bitten by a Snake", "value": 0, "hp": -10, "rarity": UNCOMMON,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "Slithered right up behind you..."},

    {"pre": "were", "name": "Bitten by a Cat", "value": 0, "hp": -7, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "It narrowly missed your jugular."},

    {"pre": "were", "name": "Crushed by a Falling Tree", "value": 0, "hp": -15, "rarity": UNCOMMON,
     "areas": [FOREST, SWAMP], 
     "desc": "Fell right on your jines, almost lost your he-nuts."},

    {"pre": "were", "name": "Hit by a Falling Branch", "value": 0, "hp": -8, "rarity": UNCOMMON,
     "areas": [FOREST], 
     "desc": "Plopped right on your head from high above. Jogged your noggin' pretty good ther'."},

    {"pre": "were", "name": "Impaled by a Falling Stalactite", "value": 0, "hp": -13, "rarity": UNCOMMON,
     "areas": [CAVE], 
     "desc": "You leaned back to look up, exposing your jines to the sharp point of the mineral formation."},

    {"pre": None, "name": "Rolled Your Ankle", "value": 0, "hp": -5, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "If you were an NBA player, you'd be out for six to eight... months."},

    {"pre": "were", "name": "Run Over by a Recumbent Bike", "value": 0, "hp": -6, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "The old bastard just kept on going."},

    {"pre": "were", "name": "Wrongfully Slapped by a Righteous Assailant", "value": 0, "hp": -3, "rarity": UNCOMMON,
     "areas": [CITY],
     "desc": "So wrong yet so righteous."},

    # ============================
    #      UNCOMMON / NEUTRAL
    # ============================

    {"pre": "a", "name": "Cannibals Anonymous Flyer", "value": 0, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "For when eating alone turns to feeling alone... a human meat-and-greet."},

    {"pre": "a can of", "name": "Evaporated Milk", "value": 0, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY], 
     "desc": "The can is empty, as the milk has evaporated. Good luck suing."},

    {"pre": "a", "name": "Feral Lads PSA Flyer", "value": 0, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY, FOREST], 
     "desc": "Fair warning regarding the feral lads. They have neither morals nor impulse control."},

    {"pre": "a", "name": "Ghost", "value": 0, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Just your typical ghost. A phantom, a ghoul - hovering about and trying to spook. Nothing better to do."},

    {"pre": "a", "name": "Giant Footprint", "value": 0, "hp": 0, "rarity": UNCOMMON,
     "areas": [FOREST], 
     "desc": "Hm... it couldn't be, could it?"},

    {"pre": "a", "name": "Gray Cat", "value": 0, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "Big boy with white mittens. If you say come, he doesn't listen."},

    {"pre": "an", "name": "Is It Lake Season Two Audition Flyer", "value": 0, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY], 
     "desc": "A show where people have to guess which glass of water is from the lake and which is fake."},

    {"pre": "a", "name": "LeGibbons Slane Wanted Poster", "value": 0, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "The former bassist for ZZ Top and man responsible for the grisly slaying of the great Crispy Daniels."},

    {"pre": "a", "name": "Riverboat Bad Boys PSA Flyer", "value": 0, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY, SWAMP], 
     "desc": "Them's here is sum' bad, riverboat boys lemme tell ya."},

    {"pre": "a", "name": "Rusted Firewatch Tower", "value": 0, "hp": 0, "rarity": UNCOMMON,
     "areas": [FOREST], 
     "desc": "Like society, ready to collapse at any moment."},

    {"pre": "a", "name": "Satanist Doing The Lord's Work", "value": 0, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "If the lord taketh, and the satanist takes people lives, then they are doing the lord's work - no?"},

    {"pre": "some", "name": "Sister Wives", "value": 0, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY],
     "desc": "In Shebokken, it's legal to be someone's sister and their wife."},

# ================================================================================================

    # ============================
    #       RARE / POSITIVE
    # ============================

    {"pre": "an", "name": "Authenticated Photo of the Hohkken", "value": 50, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "Authenticator unknown, but you know it's legit."},

    {"pre": "a signed copy of", "name": "Basta Sherman's Autobiography", "value": 45, "hp": 0, "rarity": RARE,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "A reclusive serial killer's autobiography. Not sure how this came to be?"},

    {"pre": "some", "name": "Bee Liquor", "value": 25, "hp": 25, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Oh, yeah. It's just good vibes all around. Death to them wizards, ya dig?"},

    {"pre": "a", "name": "Big Big Wig for a Big Big Boy", "value": 22, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "A remarkably big wig for whom can only be a remarkably big boy."},

    {"pre": "a", "name": "Bowl Made of Soup Containing The Like and So Forth", "value": 25, "hp": 100, "rarity": RARE,
     "areas": [CITY], 
     "desc": "It's all soup - pretty self-explanatory."},

    {"pre": "some", "name": "Brain Matter", "value": 20, "hp": 15, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Organic brain material."},

    {"pre": "a", "name": "Burner Phone With Pirated Slade Songs", "value": 6, "hp": 0, "rarity": RARE,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "Must have belonged to an absolute maniac. A deranged lunatic who should be sought by the cops until found."},

    {"pre": "a", "name": "Cast-Iron Man Comic Book", "value": 38, "hp": 0, "rarity": RARE,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "The Cast-Iron Man is a supervillain who appears in the woods and knocks out campers with a cast-iron pan."},

    {"pre": "a", "name": "Ceremonious Obsidian Blade", "value": 21, "hp": 0, "rarity": RARE,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "Used for sacrificial killing. It's all in good fun at the end of the day."},

    {"pre": "a", "name": "Cigar Box Guitar", "value": 28, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Repurposed for a greater purpose."},

    {"pre": "a", "name": "Denim Bikini", "value": 13, "hp": 0, "rarity": RARE,
     "areas": [CITY, SWAMP], 
     "desc": "I prefer men in bikini."},

    {"pre": "a bunch of", "name": "Discarded Baby Clothes and Toys", "value": 18, "hp": 0, "rarity": RARE,
     "areas": [FOREST], 
     "desc": "Another broken family after their baby was taken in the night and devoured outright."},

    {"pre": "a", "name": "Dusty Fuse Box", "value": 8, "hp": 0, "rarity": RARE,
     "areas": [CAVE], 
     "desc": "Dusty, rusty, but no need to make a fussy. S'all good, fool."},

    {"pre": "some", "name": "Erotic Prehistoric Pictographs", "value": 69, "hp": 0, "rarity": RARE,
     "areas": [CAVE], 
     "desc": "Depictions of ancient peoples copulating with tench and fellating them in and around gravel pits."},

    {"pre": "a copy of the children's book", "name": "Fatal Christmas", "value": 12, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "Santa comes and startles the father, who fatally blasts him with a shotgun. The father then becomes Santa."},

    {"pre": "a", "name": "Flange Pedal", "value": 34, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "All you need - you don't even need a guitar."},

    {"pre": "a", "name": "Fossilized Tench", "value": 48, "hp": 0, "rarity": RARE,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "Just a great find overall. Tough to beat."},

    {"pre": "a", "name": "Fretless Bass Guitar", "value": 55, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "Smooth and clean. Just how I like my glory holes."},

    {"pre": "a", "name": "Glass Eye", "value": 34, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Engraved with 'Property of Uncle Ed'."},

    {"pre": "a", "name": "Glowing Mineral Formation", "value": 33, "hp": 0, "rarity": RARE,
     "areas": [CAVE], 
     "desc": "Nickelodeon recently announced that semen glows in caves."},

    {"pre": "a", "name": "Gold Canine Tooth", "value": 36, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "This one is hard to explain... as it's actually from a canine species."},

    {"pre": "a copy of", "name": "How to Be a Renaissance Man", "value": 16, "hp": 0, "rarity": RARE,
     "areas": [CITY, FOREST], 
     "desc": "For those who wish not to be one-dimensional and are not so naturally."},

    {"pre": "a", "name": "Humanoid Skull", "value": 44, "hp": 0, "rarity": RARE,
     "areas": [CAVE, FOREST], 
     "desc": "Not a human, and not a tench... something else, it seems?"},

    {"pre": "a copy of The Mayor's book titled", "name": "I Don't Have a Son", "value": 10, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "The mayor has exactly one son, and his name is Denny. He is approximately 30 years old."},

    {"pre": "a", "name": "Jar of Synthetic Hair and Chip Crumbs", "value": 5, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "The chips are simply to add some texture to the already delicious synthetic hair."},

    {"pre": "a", "name": "Mapmaking 101 Cassette Tape", "value": 4, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY], 
     "desc": "Why do anything else when you can learn how to make maps from a cassette tape?"},

    {"pre": "a copy of", "name": "More Than a Consolation", "value": 1, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "Written by a clone during his short time on this wretched earth. He was annihilated at sea."},

    {"pre": "a copy of", "name": "One Boy: Two Sugar Mommas", "value": 16, "hp": 0, "rarity": RARE,
     "areas": [CITY, FOREST], 
     "desc": "A black comedy about a boy who had not one, not three, but two, sugar mommas. But was two enough?"},

    {"pre": "a", "name": "Pearl", "value": 28, "hp": 0, "rarity": RARE,
     "areas": [CAVE], 
     "desc": "A low-to-medium quality pearl like you would find on the Gem Shopping Network."},

    {"pre": "a", "name": "Peg Leg", "value": 23, "hp": 0, "rarity": RARE,
     "areas": [CAVE], 
     "desc": "Belonged to a pirate from days long past. He definitely used it to perform deplorable sexual acts."},

    {"pre": "a", "name": "Pirate Cutlass", "value": 37, "hp": 0, "rarity": RARE,
     "areas": [CAVE], 
     "desc": "A sword used by at least one pirate who wished to maim or murder his fellow seamen."},

    {"pre": "a", "name": "Pirate Hat", "value": 27, "hp": 0, "rarity": RARE,
     "areas": [CAVE], 
     "desc": "Just in case anyone around wasn't sure."},

    {"pre": "a worn copy of", "name": "Pupper's Last Supper", "value": 23, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "A children's book about a boy who feeds his dog chocolate and it dies."},

    {"pre": "a", "name": "Ransom Funeral Home Paperweight", "value": 5, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "Holds your papers down while they wait for you to put the ransom down."},

    {"pre": "a", "name": "Real Gold Chain", "value": 100, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Can make any white guy look fly."},

    {"pre": "a copy of", "name": "Remembering The Tragedy of Solomon Train", "value": 10, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "A documentary about the horrific story of a demented amusement park ride."},

    {"pre": "a", "name": "Shebokken Sucks T-Shirt", "value": 5, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "Most commonly worn clothing item in Shebokken."},

    {"pre": "a", "name": "Shrunken Head", "value": 29, "hp": 15, "rarity": RARE,
     "areas": [SWAMP], 
     "desc": "Was a full-sized head until a Voodoo Priestess got her cold, bony hands around it."},

    {"pre": "a", "name": "Stupor Man Comic Book", "value": 39, "hp": 0, "rarity": RARE,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "A superhero named Stupor Man whose power is to stupefy his enemies with mind-blowing remarks."},

    {"pre": "a", "name": "Taxidermy Alligator", "value": 27, "hp": 0, "rarity": RARE,
     "areas": [SWAMP], 
     "desc": "Fished out of the swamp with a belly full of children. Now, it's a fun decoration."},

    {"pre": "a copy of Meg Craig's", "name": "Tench Are People Too", "value": 33, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "Meg Craig's autobiography written to shine a new light on tench people to the world population."},

    {"pre": "a", "name": "Tench Relic", "value": 22, "hp": 0, "rarity": RARE,
     "areas": [CAVE, FOREST], 
     "desc": "If it doesn't bring a tear to your eye, you should be asking why."},

    {"pre": "a", "name": "Tench University Tuition Voucher", "value": 30, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "The most prestigious and powerful university in the world, founded millennia ago."},

    {"pre": "a signed copy of", "name": "The Legend of Whale Man", "value": 26, "hp": 0, "rarity": RARE,
     "areas": [SWAMP], 
     "desc": "A biography about a human man who lived his entire life underwater, only ever coming up for air."},

    {"pre": "a", "name": "1995 OxiClean VHS", "value": 28, "hp": 0, "rarity": RARE,
     "areas": [SWAMP], 
     "desc": "A pirated tape of all of Billy Mays' OxiClean commercials from 1995."},

    # ============================
    #       RARE / NEGATIVE
    # ============================

    {"pre": "were", "name": "Attacked by the Black Eyed Children", "value": 0, "hp": -17, "rarity": RARE,
     "areas": [CAVE], 
     "desc": "Descendants of malevolent aliens, very unfortunate to encounter whilst perusing the cave."},

    {"pre": "got", "name": "Caught in a Rusty Trap", "value": 0, "hp": -8, "rarity": RARE,
     "areas": [FOREST, SWAMP], 
     "desc": "Pee on the wound to prevent a fatal infection."},

    {"pre": None, "name": "Caught on Fire", "value": 0, "hp": -13, "rarity": RARE,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "All of a sudden your jines burst into flames, and your eyeballs quickly followed suit."},

    {"pre": "were", "name": "Crushed by a Boulder", "value": 0, "hp": -15, "rarity": RARE,
     "areas": [CAVE], 
     "desc": "Sounds a lot worse than it was."},

    {"pre": "were", "name": "Dragged Down", "value": 0, "hp": -11, "rarity": RARE,
     "areas": [CAVE, SWAMP], 
     "desc": "It is unclear by whom or what, but you were definitely dragged down pretty good ther'."},

    {"pre": None, "name": "Fell Down a Manhole", "value": 0, "hp": -8, "rarity": RARE,
     "areas": [CITY], 
     "desc": "It stunk in more ways than one."},

    {"pre": "were", "name": "Mauled by a Panther", "value": 0, "hp": -21, "rarity": RARE,
     "areas": [FOREST, SWAMP], 
     "desc": "You didn't stand much of a chance."},

    {"pre": "were", "name": "Mauled by the Feral Lads", "value": 0, "hp": -18, "rarity": RARE,
     "areas": [FOREST], 
     "desc": "There were at least 20 of them, and you have a feeling they're not through with you..."},

    {"pre": "were", "name": "Ravaged by Cats", "value": 0, "hp": -15, "rarity": RARE,
     "areas": [CITY], 
     "desc": "You protected your jugular as a dozen or more cats ravaged you like a child opening presents."},

    {"pre": "were", "name": "Struck by Lightning", "value": 0, "hp": -13, "rarity": RARE,
     "areas": [CITY, FOREST, SWAMP], 
     "desc": "Caught the tip. Why is it always to the jines?"},

    {"pre": "were", "name": "Thrashed by a Gator", "value": 0, "hp": -13, "rarity": RARE,
     "areas": [SWAMP], 
     "desc": "Looking back, it was actually kind of fun."},

    {"pre": "were", "name": "Trampled by a Crowd", "value": 0, "hp": -7, "rarity": RARE,
     "areas": [CITY], 
     "desc": "They heard the ice cream truck... 50 children died."},

    {"pre": "were", "name": "Trampled by a Herd", "value": 0, "hp": -7, "rarity": RARE,
     "areas": [FOREST], 
     "desc": "It happened so fast that it was impossible to tell exactly what kind of herd it was."},

    # ============================
    #       RARE / POSITIVE
    # ============================

    {"pre": "a", "name": "Cryptic Message from The Gorilla Pages", "value": 0, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "Sent from an anonymous member of the highly secretive Gorilla Pages deep web server."},

    {"pre": "a", "name": "Demon", "value": 0, "hp": 0, "rarity": RARE,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "Your standard, run-of-the-mill demon."},

    {"pre": "a", "name": "Fresh, Half-Eaten Corpse", "value": 0, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "How generous of whoever it was to leave you the other half!"},

    {"pre": "a", "name": "Liminal Space", "value": 0, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "I don't think I took acid this morning?"},

    {"pre": "a", "name": "Missing Tench Flyer", "value": 0, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "How sad... someone's tench has gone missing. I sure do hope the tench is returned safe and sound."},

    {"pre": "a", "name": "Missing Lifeguard Feared Digested Flyer", "value": 0, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Authorities suspect a young, blonde lifeguard may have been devoured whole by a tench monster offshore."},

    {"pre": "a", "name": "Notebook with Your Name Scribbled Hundreds of Times", "value": 0, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP], 
     "desc": "Um..."},

    {"pre": "a", "name": "Polaroid Photo of Yourself Sleeping Last Night", "value": 0, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY], 
     "desc": "A little unsettling if I do say so myself."},

    {"pre": None, "name": "One of The Mayor's Ex Wives", "value": 0, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "Her lips are sewn shut to prevent her from sharing The Mayor's secrets."},

    {"pre": None, "name": "Someone's Imaginary Friend", "value": 0, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "It makes you wish that you had your own imaginary friend."},

    {"pre": "a", "name": "Three-T Scroat Support Group Pamphlet", "value": 0, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "For those with three testicles that want the support of men with the same number of testicles."},

    {"pre": "a", "name": "White Cat", "value": 0, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "A cute, cuddly creature that is obsessed with canned slop."},

    {"pre": "a copy of Roger Mundry's", "name": "You Don't Wanna End Up Like Me", "value": 0, "hp": 0, "rarity": RARE,
     "areas": [CITY], 
     "desc": "He's right - you definitely don't wanna end up like him."},

# ================================================================================================

    # ============================
    #         LEGENDARY
    # ============================

    {"pre": "an", "name": "Alien Fugitive", "value": 350, "hp": 0, "rarity": LEGENDARY,
     "areas": [CAVE], 
     "desc": "Wanted by the galactic federation."},

    {"pre": None, "name": "Captain Hole's Unused Sheepskin", "value": 100, "hp": 0, "rarity": LEGENDARY,
     "areas": [CAVE], 
     "desc": "Would be a shame to let a perfectly good sheepskin go to waste..."},

    {"pre": None, "name": "Chula's Naval Ring", "value": 150, "hp": 0, "rarity": LEGENDARY,
     "areas": [FOREST], 
     "desc": "It's a lot bigger than other naval rings you've seen..."},

    {"pre": "a", "name": "Handwritten Draft of Santa's Unreleased Memoirs", "value": 277, "hp": 0, "rarity": LEGENDARY,
     "areas": [CITY], 
     "desc": "Mostly sexual in nature."},

    {"pre": "a", "name": "Fossilized Hohkken", "value": 404, "hp": 0, "rarity": LEGENDARY,
     "areas": [CAVE], 
     "desc": "Truly magnificent to behold - the closest known creature to God."},

    {"pre": "a", "name": "Gold Bar", "value": 250, "hp": 0, "rarity": LEGENDARY,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "A high-value item, no way around it."},

    {"pre": "a", "name": "Tench Monolith", "value": 265, "hp": 0, "rarity": LEGENDARY,
     "areas": [CAVE, FOREST], 
     "desc": "A towering structure dating back countless millennia. Your jines quiver in its presence."},

    {"pre": None, "name": "The Mayor's Secret Stash", "value": 310, "hp": 0, "rarity": LEGENDARY,
     "areas": [CITY], 
     "desc": "Guns, drugs, body parts, chewed up fetuses - you name it."},

    {"pre": "a", "name": "Treasure Chest", "value": 425, "hp": 0, "rarity": LEGENDARY,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "Full of gold coins, jewelry, and tench scales. Numerous sheepskins too."},

    {"pre": "a", "name": "Wormhole", "value": 311, "hp": 0, "rarity": LEGENDARY,
     "areas": [CAVE, CITY, FOREST], 
     "desc": "Just a darn-cool thing to find. Better not step in lest you be ripped into a billion pieces."},

    # === MYTHIC === p only
    {"pre": None, "name": "Chulaean Petroglyphs", "value": 1000, "hp": 0, "rarity": MYTHIC,
     "areas": [CAVE, FOREST, SWAMP], 
     "desc": "Petroglyphs carved by Chula, the Champion's mother and maiden."},

    {"pre": None, "name": "Denny Biltmore's Lost Pinky Ring", "value": 1200, "hp": 0, "rarity": MYTHIC,
     "areas": [CITY], 
     "desc": "This is probably the highest-dollar pinky ring you'll ever find."},

    {"pre": "a", "name": "Primordial Being", "value": 950, "hp": 0, "rarity": MYTHIC,
     "areas": [CAVE], 
     "desc": "It is beyond description. Language was not made for this being."},

    {"pre": None, "name": "The Book of Tench", "value": 1500, "hp": 0, "rarity": MYTHIC,
     "areas": [CAVE], 
     "desc": "The only piece of literature needed in the universe."},

    {"pre": "an", "name": "Undiscovered Nonhuman Civilization", "value": 1350, "hp": 0, "rarity": MYTHIC,
     "areas": [FOREST], 
     "desc": "A staggeringly large civilization of completely unique creatures. Marvelous."},

]
