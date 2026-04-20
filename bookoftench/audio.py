import os
import pygame
from dataclasses import dataclass
from typing import Optional, List

from bookoftench import settings
from .data.audio import get_audio_path


# --- Init mixer (low latency) ---
pygame.mixer.init(buffer=256)


# --- Cache ---
_SOUND_CACHE = {}
_INITIALIZED = False

def preload_all_audio() -> None:
    """Preload all audio files from the audio directory."""
    import os
    from .data.audio import get_audio_path

    global _INITIALIZED
    if _INITIALIZED:
        return

    audio_dir = os.path.dirname(get_audio_path(""))

    for file in os.listdir(audio_dir):
        if file.lower().endswith((".wav", ".mp3")):
            _preload_sound(file)

    _INITIALIZED = True


def _preload_sound(file_name: str):
    if file_name not in _SOUND_CACHE:
        _SOUND_CACHE[file_name] = pygame.mixer.Sound(
            get_audio_path(file_name)
        )


# --- Tracking state ---
@dataclass
class AudioProcess:
    file_name: Optional[str] = None
    volume: Optional[float] = None
    _channel: Optional[pygame.mixer.Channel] = None

    def is_playing(self) -> bool:
        return self._channel is not None and self._channel.get_busy()

    def play(self, loop: bool = False) -> None:
        if self.file_name is None or self.volume is None:
            return

        if self.is_playing():
            self.terminate()

        # --- MUST already be preloaded ---
        sound = _SOUND_CACHE.get(self.file_name)
        if sound is None:
            # fallback (shouldn't happen if preloaded properly)
            sound = pygame.mixer.Sound(get_audio_path(self.file_name))
            _SOUND_CACHE[self.file_name] = sound

        sound.set_volume(self.volume)

        loops = -1 if loop else 0
        self._channel = sound.play(loops=loops)

    def terminate(self) -> None:
        if self._channel is not None:
            self._channel.stop()
        self._channel = None


_current_music: AudioProcess = AudioProcess()
ACTIVE_SOUNDS: List[AudioProcess] = []


def get_music_volume() -> float:
    return float(settings.get_music_volume()) / 100


def get_sfx_volume() -> float:
    return float(settings.get_sfx_volume()) / 100


# --- SFX ---

def play_sound(file_name: str) -> None:
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
    if not settings.is_audio_enabled():
        return

    path = get_audio_path(file_name)

    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(get_music_volume())
    pygame.mixer.music.play(-1)  # infinite loop


def stop_music() -> None:
    pygame.mixer.music.stop()


def restart_music() -> None:
    if settings.is_audio_enabled():
        pygame.mixer.music.play(-1)


# --- Global cleanup ---

def stop_all_sounds() -> None:
    stop_music()

    for p in ACTIVE_SOUNDS:
        p.terminate()

    ACTIVE_SOUNDS.clear()