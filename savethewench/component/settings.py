from typing import List, Callable, Tuple

from savethewench import settings
from savethewench.audio import restart_music, stop_all_sounds
from savethewench.data.components import SETTINGS
from savethewench.model import GameState
from savethewench.ui import yellow
from savethewench.util import safe_input, print_and_sleep
from .base import PaginatedMenuComponent, functional_component, Component, SelectionBinding
from .registry import register_component


@register_component(SETTINGS)
class SettingsMenu(PaginatedMenuComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, return_only=True)

    def construct_pages(self) -> List[List[SelectionBinding]]:
        page: List[Tuple[str, type[Component]]] = []
        if settings.is_audio_enabled():
            page.append(("Disable Audio", self._disable_audio))
        else:
            page.append(("Enable Audio", self._enable_audio))
        page.append((f'Adjust Music Volume ({settings.get_music_volume()}%)',
                     self.adjust_volume_setting(settings.set_music_volume, do_restart=True)))
        page.append((f'Adjust SFX Volume ({settings.get_sfx_volume()}%)',
                     self.adjust_volume_setting(settings.set_sfx_volume)))
        return [[SelectionBinding(str(i), name, component) for i, (name, component) in enumerate(page, 1)]]

    @staticmethod
    @functional_component()
    def _enable_audio():
        settings.enable_audio()
        restart_music()

    @staticmethod
    @functional_component()
    def _disable_audio():
        settings.disable_audio()
        stop_all_sounds()

    @staticmethod
    def adjust_volume_setting(setter: Callable[[int], None], do_restart=False) -> type[Component]:
        @functional_component()
        def _component():
            while True:
                val = safe_input("Enter a setting [0-100]")
                if val.isdigit() and 0 <= int(val) <= 100:
                    setter(int(val))
                    if do_restart:
                        restart_music()
                    break
                if not val.isdigit():
                    print_and_sleep(yellow("invalid setting"))
                else:
                    print_and_sleep(yellow("must be between 0 and 100"))

        return _component
