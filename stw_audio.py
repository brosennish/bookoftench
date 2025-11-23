import os
import subprocess

ENABLE_SOUNDS = True  # or False to mute everything

SOUND_DIR = "stw_sounds"  # whatever you're using

# sound map dictionary
SOUND_MAP = {
    # GOOD
    "gator": "gator.wav",
    "purchase": "purchase.wav",
    "great_job": "great_job.wav",
    "welcome_to_hell": "welcome_to_hell.wav",
    "weapon_broke": "weapon_broke.wav",
    "devil_thunder": "devil_thunder.wav",
    "kids_cheer": "kids_cheer.wav",
    "golf_clap": "golf_clap.wav",

    # weapon sfx
    "pistol": "pistol.wav",
    "punch": "punch.wav",
    "blade": "blade.wav",
    "blunt": "blunt.wav",
    "chainsaw": "chainsaw.wav",
    "magic": "magic.wav",
    "rifle": "rifle.wav",
    "shotgun": "shotgun.wav",
    "arrow": "arrow.wav",
    "axe": "axe.wav",

    # music
    "casino_theme": "casino_theme.wav", 
    "shop_theme": "shop_theme.wav",
    "bank_theme": "bank_theme.wav",
    "battle_theme": "battle_theme.wav", 
    "area_boss_theme": "area_boss_theme.wav", 
    "final_boss_theme": "final_boss_theme.wav", 

    # ambience > GOOD
    "intro_theme": "intro_theme.wav",
    "city_theme": "city_theme.wav",
    "forest_theme": "forest_theme.wav",
    "swamp_theme": "swamp_theme.wav",
    "cave_theme": "cave_theme.wav",
    "travel_theme": "travel_theme.wav",
}

# --- Tracking state ---
_current_music_process = None
_current_music = None   # <--- add this
ACTIVE_SOUNDS = []


# --- SFX ---

def play_sound(event: str, v: float = 1.0) -> None:
    """Fire-and-forget sound effect, tracked so we can stop it later."""
    if not ENABLE_SOUNDS:
        return

    filename = SOUND_MAP.get(event)
    if not filename:
        # Unknown event; silently skip
        return

    path = os.path.join(SOUND_DIR, filename)

    try:
        proc = subprocess.Popen(["afplay", "-v", str(v), path])
        ACTIVE_SOUNDS.append(proc)
    except Exception:
        # Don't crash the game if sound fails
        pass


# --- Music ---

def get_current_music() -> str | None:
    return _current_music

def play_music(event: str) -> None:
    """Stop current music (if any) and start a new looping track."""
    global _current_music_process, _current_music

    if not ENABLE_SOUNDS:
        return

    filename = SOUND_MAP.get(event)
    if not filename:
        return

    # OPTIONAL: don't restart if same track is already playing
    if _current_music == event:
        return

    path = os.path.join(SOUND_DIR, filename)

    stop_music()

    try:
        v = 1.0  # or whatever volume logic you use
        _current_music_process = subprocess.Popen(
            ["afplay", "-v", str(v), path]
        )
        _current_music = event
    except Exception:
        _current_music_process = None
        _current_music = None



def stop_music() -> None:
    """Stop only the current music track."""
    global _current_music_process

    if _current_music_process:
        try:
            _current_music_process.terminate()
        except Exception:
            pass

        _current_music_process = None


# --- Global cleanup ---

def stop_all_sounds() -> None:
    """Stop music and all tracked SFX processes."""
    # Stop music
    stop_music()

    # Stop SFX
    for p in ACTIVE_SOUNDS:
        try:
            p.terminate()
        except Exception:
            pass

    ACTIVE_SOUNDS.clear()