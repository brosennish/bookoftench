import subprocess
from dataclasses import dataclass
from subprocess import Popen
from typing import Optional, List

from savethewench import settings
from .data.audio import get_audio_path


# --- Tracking state ---
@dataclass
class AudioProcess:
    process: Optional[Popen] = None
    file_name: Optional[str] = None
    volume: Optional[float] = None

    def is_playing(self) -> bool:
        if self.process is not None:
            return self.process.poll() is None
        return False

    def terminate(self) -> None:
        if self.process is not None:
            self.process.terminate()
        self.process = None
        self.file_name = None
        self.volume = None

_current_music: AudioProcess = AudioProcess()
ACTIVE_SOUNDS: List[AudioProcess] = []


# --- SFX ---

def play_sound(file_name: str) -> None:
    """Fire-and-forget sound effect, tracked so we can stop it later."""
    if not settings.is_audio_enabled():
        return

    path = get_audio_path(file_name)

    proc = subprocess.Popen(["afplay", "-v", str(settings.get_sfx_volume()), path])
    ACTIVE_SOUNDS.append(AudioProcess(proc, file_name, settings.get_sfx_volume()))


# --- Music ---

def is_track_playing(file_name: str, volume: float) -> bool:
    if _current_music.file_name != file_name or _current_music.volume != volume:
        return False
    return _current_music.is_playing()


def play_music(file_name: str) -> None:
    """Stop current music (if any) and start a new looping track."""
    global _current_music

    if not settings.is_audio_enabled():
        return

    # OPTIONAL: don't restart if same track is already playing
    if is_track_playing(file_name, settings.get_music_volume()):
        return

    path = get_audio_path(file_name)

    stop_music()

    proc = subprocess.Popen(
        ["afplay", "-v", str(settings.get_music_volume()), path]
    )
    _current_music = AudioProcess(proc, file_name, settings.get_music_volume())


def stop_music() -> None:
    """Stop only the current music track."""
    _current_music.terminate()


# --- Global cleanup ---

def stop_all_sounds() -> None:
    """Stop music and all tracked SFX processes."""
    # Stop music
    stop_music()

    # Stop SFX
    for p in ACTIVE_SOUNDS:
        p.terminate()

    ACTIVE_SOUNDS.clear()
