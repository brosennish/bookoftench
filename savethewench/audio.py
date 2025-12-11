import subprocess

from .data.audio import get_audio_path

ENABLE_SOUNDS = True  # or False to mute everything


# --- Tracking state ---
_current_music_process = None
_current_music = None   # <--- add this
ACTIVE_SOUNDS = []


# --- SFX ---

def play_sound(file_name: str, v: float = 1.0) -> None:
    """Fire-and-forget sound effect, tracked so we can stop it later."""
    if not ENABLE_SOUNDS:
        return

    path = get_audio_path(file_name)

    try:
        proc = subprocess.Popen(["afplay", "-v", str(v), path])
        ACTIVE_SOUNDS.append(proc)
    except Exception:
        # Don't crash the game if sound fails
        pass


# --- Music ---

def get_current_music() -> str | None:
    return _current_music

def play_music(file_name: str) -> None:
    """Stop current music (if any) and start a new looping track."""
    global _current_music_process, _current_music

    if not ENABLE_SOUNDS:
        return

    # OPTIONAL: don't restart if same track is already playing
    if _current_music == file_name:
        return

    path = get_audio_path(file_name)

    stop_music()

    try:
        v = 1.0  # or whatever volume logic you use
        _current_music_process = subprocess.Popen(
            ["afplay", "-v", str(v), path]
        )
        _current_music = file_name
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