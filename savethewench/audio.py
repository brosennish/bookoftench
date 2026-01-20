import subprocess
from dataclasses import dataclass
from subprocess import Popen
from typing import Optional, List

from savethewench import settings
from .data.audio import get_audio_path


# --- Tracking state ---
@dataclass
class AudioProcess:
    file_name: Optional[str] = None
    volume: Optional[float] = None
    _process: Optional[Popen] = None

    def is_playing(self) -> bool:
        if self._process is not None:
            return self._process.poll() is None
        return False

    def play(self):
        if self._process is not None:
            if self.is_playing():
                self.terminate()
        if self.file_name is not None and self.volume is not None:
            self._process = subprocess.Popen(
                ["afplay", "-v", str(self.volume), get_audio_path(self.file_name)],
                stderr=subprocess.DEVNULL)

    def terminate(self) -> None:
        if self._process is not None:
            self._process.terminate()
        self._process = None


_current_music: AudioProcess = AudioProcess()
ACTIVE_SOUNDS: List[AudioProcess] = []


def get_music_volume() -> float:
    return float(settings.get_music_volume()) / 100


def get_sfx_volume() -> float:
    return float(settings.get_sfx_volume()) / 100


# --- SFX ---

def play_sound(file_name: str) -> None:
    """Fire-and-forget sound effect, tracked so we can stop it later."""
    if not settings.is_audio_enabled():
        return

    sound = AudioProcess(file_name, get_sfx_volume())
    ACTIVE_SOUNDS.append(sound)
    sound.play()


# --- Music ---

def is_track_playing(file_name: str, volume: float) -> bool:
    if _current_music.file_name != file_name or _current_music.volume != volume:
        return False
    return _current_music.is_playing()


def play_music(file_name: str) -> None:
    """Stop current music (if any) and start a new looping track."""
    global _current_music

    # OPTIONAL: don't restart if same track is already playing
    if is_track_playing(file_name, get_music_volume()):
        return

    _current_music.file_name = file_name
    _current_music.volume = get_music_volume()

    # only play if audio is enabled, but track state in case it is re-enabled later
    if settings.is_audio_enabled():
        # TODO log/print some message if this fails and disable audio
        _current_music.play()


def stop_music() -> None:
    """Stop only the current music track."""
    _current_music.terminate()


def restart_music() -> None:
    _current_music.volume = get_music_volume()
    if settings.is_audio_enabled():
        _current_music.play()


# --- Global cleanup ---

def stop_all_sounds() -> None:
    """Stop music and all tracked SFX processes."""
    # Stop music
    stop_music()

    # Stop SFX
    for p in ACTIVE_SOUNDS:
        p.terminate()

    ACTIVE_SOUNDS.clear()
