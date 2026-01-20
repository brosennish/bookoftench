from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Settings:
    enable_audio: bool
    music_volume: int
    sfx_volume: int

    @classmethod
    def defaults(cls) -> Settings:
        return Settings(enable_audio=True, music_volume=100, sfx_volume=100)


_SETTINGS = Settings.defaults()


def set_settings(settings: Settings) -> None:
    global _SETTINGS
    _SETTINGS = settings


def is_audio_enabled() -> bool:
    return _SETTINGS.enable_audio


def enable_audio() -> None:
    _SETTINGS.enable_audio = True


def disable_audio() -> None:
    _SETTINGS.enable_audio = False


def get_music_volume() -> int:
    return _SETTINGS.music_volume


def set_music_volume(volume: int) -> None:
    _SETTINGS.music_volume = volume


def get_sfx_volume() -> int:
    return _SETTINGS.sfx_volume


def set_sfx_volume(volume: int) -> None:
    _SETTINGS.sfx_volume = volume
