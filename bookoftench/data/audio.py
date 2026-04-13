import os
from typing import AnyStr

# Themes
AREA_BOSS_THEME = "area_boss_theme.wav"
BANK_THEME = "bank_theme.wav"
BATTLE_THEME = "battle_theme.wav"
BLACKSMITH_THEME = "blacksmith_theme.wav"
CASINO_THEME = "casino_theme.wav"
CAVE_THEME = "cave_theme.wav"
CAVE_BATTLE_THEME = "cave_battle_theme.wav" # TODO
CITY_THEME = "city_theme.wav"
CITY_BATTLE_THEME = "city_battle_theme.wav" # TODO
COFFEE_THEME = "coffee_theme.wav"
CRYPTO_THEME = "crypto_theme.wav"
FINAL_BOSS_THEME = "final_boss_theme.wav"
FOREST_THEME = "forest_theme.wav"
FOREST_BATTLE_THEME = "forest_battle_theme.wav" # TODO
HOSPITAL_THEME = "hospital_theme.wav"
INTRO_THEME = "intro_theme.wav"
LAB_THEME = "lab_theme.wav"
MENSCH_THEME = "mensch_theme.wav"
OCCULTIST_THEME = "occultist_theme.wav"
OFFICER_THEME = "officer_theme.wav"
ROULETTE_THEME = "roulette_theme.wav"
SHAMAN_THEME = "shaman_theme.wav"
SHOP_THEME = "shop_theme.wav"
START_THEME = "start_theme.wav"
SWAMP_THEME = "swamp_theme.wav"
SWAMP_BATTLE_THEME = "swamp_battle_theme.wav" # TODO
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
SPRAY = "spray.wav"
SQUEAK = "squeak.wav"
WEAPON_BROKE = "weapon_broke.wav"
WHIFF = "whiff.wav"

# Misc Sounds
AGONY = "agony.wav" # TODO
DEVIL_THUNDER = "devil_thunder.wav"
DRINKING = "drinking.wav"
ENEMY_APPEARS = "enemy_appears.wav"
GATOR = "gator.wav"
GOLF_CLAP = "golf_clap.wav"
GREAT_JOB = "great_job.wav"
HEALING = "healing.wav" # TODO
HOHKKEN = "hohkken.wav"
KIDS_CHEER = "kids_cheer.wav"
POSITIVE = "positive.wav"
PURCHASE = "purchase.wav"
RITUAL = "ritual.wav"
WELCOME_TO_HELL = "welcome_to_hell.wav"
WEREWOLF = "werewolf.wav"


# TODO make sure this works regardless of cwd
def get_audio_path(filename) -> AnyStr:
    return os.path.abspath(os.path.join('bookoftench/data/audio', filename))
