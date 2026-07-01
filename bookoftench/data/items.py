from .audio import DRINK, WHIFF, POSITIVE, MAGIC, SPRAY, EAT, BOOMERANG_SFX

# ================================================================================================

CAVE = "Cave"
CITY = "City"
FOREST = "Forest"
SWAMP = "Swamp"

# ================================================================================================

ABANDONED_EYEBALLS = "Abandoned Eyeballs"
ACCURACY_SEARUM = "Accuracy Searum"
ALIEN_REMAINS = "Alien Remains"
ANCIENT_CLOAK = "Ancient Cloak"
ANTS_ON_A_LOG = "Ants On A Log"
ASHWAGANDHA_GUMMIES = "Ashwagandha Gummies"
BABY = "Baby"
BAT_MATTER ="Bat Matter"
BERRIES = "Berries"
BONE_MEAL = "Bone Meal"
BOOMERANG = "Boomerang"
CAMPBELLS_GOOP = "Campbell's Goop"
CANNED_HORSE = "Canned Horse"
CARP_FILET = "Carp Filet"
CATFISH_FILET = "Catfish Filet"
CENTAURIAN_HOOF = "Centaurian Hoof"
CHILDS_LOST_LUNCH = "Child's Lost Lunch"
CRABS_ON_RYE = "Crabs on Rye"
CRAY = "Cray"
CRISPY_DANIELS_BLOOD_SOAKED_BANDANA = "Crispy Daniels Blood-soaked Bandana"
CRITICAL_BASS = "Critical Bass"
CUSTOM_INFLATABLE_SUIT = "Custom Inflatable Suit"
CYCLOPS_EYE = "Cyclops Eye"
DEATH_BRAIN = "Death Brain"
EAGLE_EGG = "Eagle Egg"
EGG_ON_EGGS = "Egg on Eggs"
EGGS_ON_EGG = "Eggs on Egg"
ENERGY_CRYSTAL = "Energy Crystal"
FAIRY_WINGS = "Fairy Wings"
FERMENTED_CELERY_MILK = "Fermented Celery Milk"
FLACCID_ACID = "Flaccid Acid"
FROZEN_WAFFLE = "Frozen Waffle"
GATOR_TESTICLES = "Gator Testicles"
GIANT_TENTACLE = "Giant Tentacle"
GIZZARDS_AND_LIVERS = "Gizzards and Livers"
GOBY = "Goby"
HALF_DIGESTED_DIAMOND_NECKLACE = "Half-Digested Diamond Necklace"
HODAG_TOOTH = "Hodag Tooth"
HOG_LOINS = "Hog Loins"
HTH = "HTH"
HYDRA_HEAD = "Hydra Head"
IOU = "IOU"
KRILL = "Krill"
LACED_HONEY = "Laced Honey"
LOST_SAUCE = "Lost Sauce"
MINOTAUR_NOSE_RING = "Minotaur Nose Ring"
MISCELLANEOUS_TREASURED_ITEMS = "Miscellaneous Treasured Items"
MOON_RUNE = "Moon Rune"
MOONSHINE = "Moonshine"
MOREL = "Morel"
MOTHMAN_DNA = "Mothman DNA"
MUSKRAT_SKEWER = "Muskrat Skewer"
MYSTERY_MEAT = "Mystery Meat"
MYSTICAL_MUSHROOMS = "Mystical Mushrooms"
nPnG = "nPnG"
ORGANIC_SLUDGE = "Organic Sludge"
OWL_EGG = "Owl Egg"
OXYGENATED_BIOFILM = "Oxygenated Biofilm"
PANTHER_LOINS = "Panther Loins"
PHOTOSYNTHOPHYL = "Photosynthophyl"
ROUGAROU_TAIL = "Rougarou Tail"
SABERTOOTH_LIGER_FILET = "Sabertooth Liger Filet"
SASQUATCH_FOOT = "Sasquatch Foot"
SEWER_GATOR_SKULL = "Sewer Gator Skull"
SKUNK_APE_PELT = "Skunk Ape Pelt"
SMOKE_BOMB = "Smoke Bomb"
SOMEWHAT_SPICY_NOODLES = "Somewhat Spicy Noodles"
SOUR_MILK = "Sour Milk"
STALE_GREENS = "Stale Greens"
SUSPICIOUS_GUMBO = "Suspicious Gumbo"
SAPIENT_BURRO = "Sapient Burro"
TENCH_FILET = "Tench Filet"
TENCHTOSTERONE = "Tenchtosterone"
TOAD_STOOL = "Toad Stool"
TROLL_SACK = "Troll Sack"
UNIDENTIFIED_MUSHROOMS = "Unidentified Mushrooms"
UNWANTED_PROTEIN = "Unwanted Protein"
VERY_SPICY_NOODLES = "Very Spicy Noodles"
WENDIGO_ANTLER = "Wendigo Antler"
WORMHOLE = "Wormhole"

# ================================================================================================

BOSS = "boss"      # valuable item acquired from a boss
CRIT = "crit"      # affects player attack critical hit odds
DMG = "dmg"        # affects player attack damage
ENEMY = "enemy"    # used against enemy
FLEE = "flee"      # used to escape from battle
HEALTH = "health"  # non-normal item used to restore HP
NORMAL = "normal"  # normal item used to restore HP
STAT = "stat"      # used to mutate one or more player stats

# ================================================================================================

Items = [

    # ============================
    #       TIER 1 (10 HP)
    # ============================

    {'name': ANTS_ON_A_LOG, 'type': NORMAL, 'hp': 10, 'cost': 10, 'sell_value': 4, 'areas': [FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': BERRIES, 'type': NORMAL, 'hp': 10, 'cost': 9, 'sell_value': 4, 'areas': [FOREST], 'desc': None,
     'sound': EAT},
    {'name': BONE_MEAL, 'type': NORMAL, 'hp': 10, 'cost': 12, 'sell_value': 5, 'areas': [CAVE, CITY], 'desc': None,
     'sound': EAT},
    {'name': FROZEN_WAFFLE, 'type': NORMAL, 'hp': 10, 'cost': 12, 'sell_value': 4, 'areas': [CITY], 'desc': None,
     'sound': EAT},
    {'name': GOBY, 'type': NORMAL, 'hp': 10, 'cost': 10, 'sell_value': 4, 'areas': [CAVE, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': KRILL, 'type': NORMAL, 'hp': 10, 'cost': 12, 'sell_value': 4, 'areas': [CITY], 'desc': None,
     'sound': EAT},
    {'name': SOUR_MILK, 'type': NORMAL, 'hp': 10, 'cost': 10, 'sell_value': 4, 'areas': [CITY, FOREST, SWAMP], 'desc': None,
     'sound': DRINK},
    {'name': STALE_GREENS, 'type': NORMAL, 'hp': 10, 'cost': 9, 'sell_value': 5, 'areas': [CAVE, CITY], 'desc': None,
     'sound': EAT},
    {'name': TOAD_STOOL, 'type': NORMAL, 'hp': 10, 'cost': 9, 'sell_value': 4, 'areas': [FOREST, SWAMP], 'desc': None,
     'sound': EAT},

    # ============================
    #      TIER 2 (16-20 HP)
    # ============================

    {'name': BAT_MATTER, 'type': NORMAL, 'hp': 15, 'cost': 16, 'sell_value': 6, 'areas': [CAVE], 'desc': None,
     'sound': EAT},
    {'name': CAMPBELLS_GOOP, 'type': NORMAL, 'hp': 20, 'cost': 22, 'sell_value': 9, 'areas': [CITY, CAVE, FOREST], 'desc': None,
     'sound': DRINK},
    {'name': CRAY, 'type': NORMAL, 'hp': 20, 'cost': 22, 'sell_value': 8, 'areas': [CAVE, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': EGG_ON_EGGS, 'type': NORMAL, 'hp': 18, 'cost': 20, 'sell_value': 8, 'areas': [CAVE, CITY, FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': EGGS_ON_EGG, 'type': NORMAL, 'hp': 18, 'cost': 20, 'sell_value': 8, 'areas': [CAVE, CITY, FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': MYSTERY_MEAT, 'type': NORMAL, 'hp': 20, 'cost': 22, 'sell_value': 8, 'areas': [CAVE, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': MUSKRAT_SKEWER, 'type': NORMAL, 'hp': 16, 'cost': 17, 'sell_value': 7, 'areas': [SWAMP], 'desc': None,
     'sound': EAT},
    {'name': ORGANIC_SLUDGE, 'type': NORMAL, 'hp': 16, 'cost': 17, 'sell_value': 7, 'areas': [CITY], 'desc': None,
     'sound': DRINK},
    {'name': SOMEWHAT_SPICY_NOODLES, 'type': NORMAL, 'hp': 18, 'cost': 20, 'sell_value': 8, 'areas': [CITY], 'desc': None,
     'sound': EAT},

    # ============================
    #      TIER 3 (24-28 HP)
    # ============================

    {'name': ABANDONED_EYEBALLS, 'type': NORMAL, 'hp': 28, 'cost': 32, 'sell_value': 13, 'areas': [CAVE, CITY, FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': CATFISH_FILET, 'type': NORMAL, 'hp': 26, 'cost': 27, 'sell_value': 11, 'areas': [SWAMP], 'desc': None,
     'sound': EAT},
    {'name': CRABS_ON_RYE, 'type': NORMAL, 'hp': 28, 'cost': 30, 'sell_value': 12, 'areas': [CAVE, CITY], 'desc': None,
     'sound': EAT},
    {'name': GIZZARDS_AND_LIVERS, 'type': NORMAL, 'hp': 26, 'cost': 27, 'sell_value': 11, 'areas': [CITY, FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': LOST_SAUCE, 'type': NORMAL, 'hp': 25, 'cost': 25, 'sell_value': 10, 'areas': [CAVE], 'desc': None,
     'sound': DRINK},
    {'name': MOREL, 'type': NORMAL, 'hp': 24, 'cost': 24, 'sell_value': 10, 'areas': [FOREST], 'desc': None,
     'sound': EAT},
    {'name': OWL_EGG, 'type': NORMAL, 'hp': 25, 'cost': 25, 'sell_value': 10, 'areas': [FOREST], 'desc': None,
     'sound': EAT},
    {'name': UNWANTED_PROTEIN, 'type': NORMAL, 'hp': 24, 'cost': 25, 'sell_value': 10, 'areas': [CAVE, FOREST], 'desc': None,
     'sound': EAT},
    {'name': VERY_SPICY_NOODLES, 'type': NORMAL, 'hp': 24, 'cost': 24, 'sell_value': 10, 'areas': [CITY, FOREST, SWAMP], 'desc': None,
     'sound': EAT},

    # ============================
    #      TIER 4 (30-35 HP)
    # ============================

    {'name': CANNED_HORSE, 'type': NORMAL, 'hp': 35, 'cost': 37, 'sell_value': 15, 'areas': [CITY, CAVE], 'desc': None,
     'sound': EAT},
    {'name': CARP_FILET, 'type': NORMAL, 'hp': 35, 'cost': 35, 'sell_value': 15, 'areas': [CITY], 'desc': None,
     'sound': EAT},
    {'name': EAGLE_EGG, 'type': NORMAL, 'hp': 34, 'cost': 35, 'sell_value': 14, 'areas': [FOREST], 'desc': None,
     'sound': DRINK},
    {'name': GATOR_TESTICLES, 'type': NORMAL, 'hp': 35, 'cost': 34, 'sell_value': 14, 'areas': [SWAMP], 'desc': None,
     'sound': EAT},
    {'name': HOG_LOINS, 'type': NORMAL, 'hp': 35, 'cost': 37, 'sell_value': 15, 'areas': [FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': LACED_HONEY, 'type': NORMAL, 'hp': 33, 'cost': 33, 'sell_value': 14, 'areas': [CAVE, FOREST], 'desc': None,
     'sound': DRINK},
    {'name': MOONSHINE, 'type': NORMAL, 'hp': 34, 'cost': 35, 'sell_value': 14, 'areas': [CAVE, SWAMP], 'desc': None,
     'sound': DRINK},
    {'name': CHILDS_LOST_LUNCH, 'type': NORMAL, 'hp': 34, 'cost': 35, 'sell_value': 13, 'areas': [CITY, FOREST], 'desc': None,
     'sound': EAT},
    {'name': UNIDENTIFIED_MUSHROOMS, 'type': NORMAL, 'hp': 35, 'cost': 35, 'sell_value': 16, 'areas': [CAVE, FOREST, SWAMP], 'desc': None,
     'sound': EAT},

    # ============================
    #      TIER 5 (38-40 HP)
    # ============================

    {'name': ALIEN_REMAINS, 'type': NORMAL, 'hp': 39, 'cost': 40, 'sell_value': 20, 'areas': [FOREST], 'desc': None,
     'sound': EAT},
    {'name': GIANT_TENTACLE, 'type': NORMAL, 'hp': 38, 'cost': 42, 'sell_value': 16, 'areas': [CITY], 'desc': None,
     'sound': EAT},
    {'name': MYSTICAL_MUSHROOMS, 'type': NORMAL, 'hp': 39, 'cost': 38, 'sell_value': 16, 'areas': [CAVE, FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': PANTHER_LOINS, 'type': NORMAL, 'hp': 37, 'cost': 42, 'sell_value': 16, 'areas': [FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': SUSPICIOUS_GUMBO, 'type': NORMAL, 'hp': 39, 'cost': 40, 'sell_value': 16, 'areas': [FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': TENCH_FILET, 'type': NORMAL, 'hp': 40, 'cost': 42, 'sell_value': 17, 'areas': [CITY], 'desc': None,
     'sound': EAT},

    # ============================
    #       TIER 6 (50 HP)
    # ============================

    {'name': ASHWAGANDHA_GUMMIES, 'type': NORMAL, 'hp': 50, 'cost': 55, 'sell_value': 23, 'areas': [CITY, FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': ENERGY_CRYSTAL, 'type': NORMAL, 'hp': 50, 'cost': 55, 'sell_value': 24, 'areas': [CAVE, CITY, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': FERMENTED_CELERY_MILK, 'type': NORMAL, 'hp': 50, 'cost': 55, 'sell_value': 22, 'areas': [CITY, FOREST, SWAMP], 'desc': None,
     'sound': DRINK},
    {'name': OXYGENATED_BIOFILM, 'type': NORMAL, 'hp': 50, 'cost': 55, 'sell_value': 23, 'areas': [CAVE], 'desc': None,
     'sound': EAT},

    # ============================
    #       TIER 7 (51+ HP)
    # ============================

    {'name': BABY, 'type': NORMAL, 'hp': 100, 'cost': 110, 'sell_value': 50, 'areas': [SWAMP], 'desc': None,
     'sound': EAT},

    # ============================
    #       SPECIAL (HP N/A)
    # ============================

    {'name': ACCURACY_SEARUM, 'type': STAT, 'hp': 0, 'cost': 110, 'sell_value': 55, 'areas': [CAVE, FOREST],
     'desc': 'Increase accuracy by 0.03', 'sound': DRINK},
    {'name': BOOMERANG, 'type': ENEMY, 'hp': 0, 'cost': 45, 'sell_value': 14, 'areas': [CITY, FOREST, SWAMP],
     'desc': 'Do X damage to enemy and lose X/2 HP', 'sound': BOOMERANG_SFX},
    {'name': CRITICAL_BASS, 'type': CRIT, 'hp': 0, 'cost': 55, 'sell_value': 18, 'areas': [CAVE, FOREST],
     'desc': 'Make your next attack a critical hit', 'sound': EAT},
    {'name': FLACCID_ACID, 'type': ENEMY, 'hp': 0, 'cost': 75, 'sell_value': 22, 'areas': [CAVE, CITY, SWAMP],
     'desc': 'Lower enemy strength by 25%', 'sound': SPRAY},
    {'name': HTH, 'type': STAT, 'hp': 0, 'cost': 110, 'sell_value': 55, 'areas': [CITY, SWAMP],
     'desc': 'Increase strength by 0.03', 'sound': POSITIVE},
    {'name': IOU, 'type': FLEE, 'hp': 0, 'cost': 10, 'sell_value': 3, 'areas': [CITY],
     'desc': 'Use to escape from battle', 'sound': WHIFF},
    {'name': MOON_RUNE, 'type': ENEMY, 'hp': 0, 'cost': 80, 'sell_value': 24, 'areas': [CAVE, FOREST],
     'desc': 'Do damage to enemy based on the Moon (requires moonlight)', 'sound': MAGIC},
    {'name': PHOTOSYNTHOPHYL, 'type': HEALTH, 'hp': 0, 'cost': 110, 'sell_value': 50, 'areas': [FOREST, SWAMP],
     'desc': 'Fully restore HP (requires sunlight)', 'sound': POSITIVE},
    {'name': SMOKE_BOMB, 'type': FLEE, 'hp': 0, 'cost': 20, 'sell_value': 7, 'areas': [CAVE, CITY, FOREST, SWAMP],
     'desc': 'Use to escape from battle', 'sound': WHIFF},
    {'name': TENCHTOSTERONE, 'type': DMG, 'hp': 0, 'cost': 95, 'sell_value': 45, 'areas': [CITY, SWAMP],
     'desc': 'Double the damage of your next melee attack', 'sound': DRINK},
    {'name': WORMHOLE, 'type': FLEE, 'hp': 0, 'cost': 30, 'sell_value': 11, 'areas': [CAVE, FOREST],
     'desc': 'Use to escape from battle', 'sound': MAGIC},
    {'name': nPnG, 'type': HEALTH, 'hp': 0, 'cost': 105, 'sell_value': 28, 'areas': [CAVE, CITY],
     'desc': 'Lose X HP and increase max HP by X', 'sound': DRINK},

    # ============================
    #     SPECIAL BOSS ITEMS
    # ============================

    {'name': ANCIENT_CLOAK, 'type': BOSS, 'hp': 0, 'cost': 0, 'sell_value': 130, 'areas': None,
     'desc': 'Cloak obtained by the Vampire Overlord in ancient times', 'sound': WHIFF},
    {'name': CENTAURIAN_HOOF, 'type': BOSS, 'hp': 50, 'cost': 0, 'sell_value': 100, 'areas': None,
     'desc': 'One of the four hooves previously utilized by the mighty Centaur', 'sound': EAT},
    {'name': CRISPY_DANIELS_BLOOD_SOAKED_BANDANA, 'type': BOSS, 'hp': 0, 'cost': 0, 'sell_value': 100, 'areas': None,
     'desc': 'The bandana Crispy Daniels was wearing when he was assassinated aboard the S.S. Biltmore.', 'sound': WHIFF},
    {'name': CUSTOM_INFLATABLE_SUIT, 'type': BOSS, 'hp': 0, 'cost': 0, 'sell_value': 80, 'areas': None,
     'desc': 'Used by Oily Doily to float in the air', 'sound': WHIFF},
    {'name': CYCLOPS_EYE, 'type': BOSS, 'hp': 50, 'cost': 0, 'sell_value': 110, 'areas': None,
     'desc': 'A large eye that once belonged to a Cyclops', 'sound': EAT},
    {'name': DEATH_BRAIN, 'type': BOSS, 'hp': 50, 'cost': 0, 'sell_value': 90, 'areas': None,
     'desc': 'The tiny brain of the giant Death Worm', 'sound': EAT},
    {'name': HALF_DIGESTED_DIAMOND_NECKLACE, 'type': BOSS, 'hp': 0, 'cost': 0, 'sell_value': 130, 'areas': None,
     'desc': 'Giant mutant rats will eat anything - especially jines', 'sound': EAT},
    {'name': FAIRY_WINGS, 'type': BOSS, 'hp': 35, 'cost': 0, 'sell_value': 120, 'areas': None,
     'desc': 'Allowed the Fairy Codmother to fly - like a horsefly', 'sound': EAT},
    {'name': HODAG_TOOTH, 'type': BOSS, 'hp': 30, 'cost': 0, 'sell_value': 135, 'areas': None,
     'desc': 'A massive tooth from the mouth of the elusive Hodag', 'sound': EAT},
    {'name': HYDRA_HEAD, 'type': BOSS, 'hp': 120, 'cost': 0, 'sell_value': 180, 'areas': None,
     'desc': 'One of the Hydra\'s many heads', 'sound': EAT},
    {'name': MISCELLANEOUS_TREASURED_ITEMS, 'type': BOSS, 'hp': 0, 'cost': 0, 'sell_value': 90, 'areas': None,
     'desc': 'Various items stolen from poor, unsuspecting saps', 'sound': EAT},
    {'name': MINOTAUR_NOSE_RING, 'type': BOSS, 'hp': 0, 'cost': 0, 'sell_value': 120, 'areas': None,
     'desc': 'A ring that once pierced the nose of the mighty Minotaur', 'sound': WHIFF},
    {'name': MOTHMAN_DNA, 'type': BOSS, 'hp': 0, 'cost': 0, 'sell_value': 150, 'areas': None,
     'desc': 'DNA belonging to the late, great Mothman', 'sound': WHIFF},
    {'name': SKUNK_APE_PELT, 'type': BOSS, 'hp': 0, 'cost': 0, 'sell_value': 100, 'areas': None,
     'desc': 'The worst thing you\'ll ever smell', 'sound': WHIFF},
    {'name': ROUGAROU_TAIL, 'type': BOSS, 'hp': 45, 'cost': 0, 'sell_value': 120, 'areas': None,
     'desc': 'The tail of the ferocious Rougarou', 'sound': EAT},
    {'name': SABERTOOTH_LIGER_FILET, 'type': BOSS, 'hp': 100, 'cost': 0, 'sell_value': 100, 'areas': None,
     'desc': 'A generous cut of Sabertooth Liger Meat', 'sound': EAT},
    {'name': SASQUATCH_FOOT, 'type': BOSS, 'hp': 80, 'cost': 0, 'sell_value': 160, 'areas': None,
     'desc': 'A big foot', 'sound': EAT},
    {'name': SEWER_GATOR_SKULL, 'type': BOSS, 'hp': 0, 'cost': 0, 'sell_value': 100, 'areas': None,
     'desc': 'The skull of the notorious Sewer Gator', 'sound': WHIFF},
    {'name': SAPIENT_BURRO, 'type': BOSS, 'hp': 100, 'cost': 0, 'sell_value': 125, 'areas': None,
     'desc': 'Smells like root vegetables', 'sound': EAT},
    {'name': TROLL_SACK, 'type': BOSS, 'hp': 0, 'cost': 0, 'sell_value': 100, 'areas': None,
     'desc': 'Holds coins for the troll beneath its loins and its hole.', 'sound': WHIFF},
    {'name': WENDIGO_ANTLER, 'type': BOSS, 'hp': 0, 'cost': 0, 'sell_value': 150, 'areas': None,
     'desc': 'One of the two antlers that once adorned the magnificent Wendigo', 'sound': WHIFF},
]
