from dataclasses import dataclass

@dataclass
class Settings:
    enable_audio: bool = True
    music_volume: int = 100
    sfx_volume: int = 100

_SETTINGS = Settings()

def set_settings(settings: Settings):
    global _SETTINGS
    _SETTINGS = settings

def is_audio_enabled():
    return _SETTINGS.enable_audio

def disable_audio():
    _SETTINGS.enable_audio = False

def get_music_volume():
    return float(_SETTINGS.music_volume)/100

def get_sfx_volume():
    return float(_SETTINGS.sfx_volume)/100