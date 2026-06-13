from bookoftench.data import areas as a
from bookoftench.ui import green

# ================================================================================================

# Special Events
ALIEN_ABDUCTION_1 = "Alien Abduction 1"
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
    {'name': ALIEN_ABDUCTION_1, 'color': green, 'theme': None,
     'areas': [a.CITY, a.FOREST, a.SWAMP], 'time': [NIGHT], 'moon': None, 'season': None,
     'text': 'Friendly aliens have abducted you.\nThey give you three options:',
     'choices': ['Increase strength by 0.05', 'Increase luck by 2', 'Decrease level by 1'],
     'method': 'alien_abduction_1'}
]
