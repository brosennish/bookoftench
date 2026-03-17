import os
from typing import AnyStr

# Themes
AREA_BOSS_THEME = "area_boss_theme.wav"
BANK_THEME = "bank_theme.wav"
BATTLE_THEME = "battle_theme.wav"
CASINO_THEME = "casino_theme.wav"
CAVE_THEME = "cave_theme.wav"
CITY_THEME = "city_theme.wav"
COFFEE_THEME = "coffee_theme.wav"
CRYPTO_THEME = "crypto_theme.wav"
FINAL_BOSS_THEME = "final_boss_theme.wav"
FOREST_THEME = "forest_theme.wav"
HOSPITAL_THEME = "hospital_theme.wav"
INTRO_THEME = "intro_theme.wav"
LAB_THEME = "lab_theme.wav"
OCCULTIST_THEME = "occultist_theme.wav"
OFFICER_THEME = "officer_theme.wav"
ROULETTE_THEME = "roulette_theme.wav"
SHAMAN_THEME = "shaman_theme.wav"
SHOP_THEME = "shop_theme.wav"
START_THEME = "start_theme.wav"
SWAMP_THEME = "swamp_theme.wav"
TRAVEL_THEME = "travel_theme.wav"
VICTORY_THEME = "victory_theme.wav"
WIZARD_THEME = "wizard_theme.wav"

# Weapon Sounds
ARROW = "arrow.wav"
AXE = "axe.wav"
BLADE = "blade.wav"
BLUNT = "blunt.wav"
CHAINSAW = "chainsaw.wav"
MAGIC = "magic.wav"
PISTOL = "pistol.wav"
PUNCH = "punch.wav"
RIFLE = "rifle.wav"
SHOTGUN = "shotgun.wav"
WEAPON_BROKE = "weapon_broke.wav"

# Misc Sounds
DEVIL_THUNDER = "devil_thunder.wav"
DRINKING = "drinking.wav"
GATOR = "gator.wav"
GOLF_CLAP = "golf_clap.wav"
GREAT_JOB = "great_job.wav"
HOHKKEN = "hohkken.wav"
KIDS_CHEER = "kids_cheer.wav"
PURCHASE = "purchase.wav"
WELCOME_TO_HELL = "welcome_to_hell.wav"


# TODO make sure this works regardless of cwd
def get_audio_path(filename) -> AnyStr:
    return os.path.abspath(os.path.join('bookoftench/data/audio', filename))
