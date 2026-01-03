from typing import List, Callable

from savethewench import settings
from savethewench.audio import restart_music, stop_all_sounds
from savethewench.model import GameState
from savethewench.ui import yellow
from savethewench.util import safe_input, print_and_sleep
from .base import PaginatedMenuComponent, functional_component, Component, SelectionBinding, LabeledSelectionComponent


class SettingsMenu(PaginatedMenuComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.exit_settings = False

    def construct_pages(self) -> List[List[SelectionBinding]]:
        page = []
        if settings.is_audio_enabled():
            page.append(SelectionBinding('1', "Disable Audio", self._disable_audio))
        else:
            page.append(SelectionBinding('1', "Enable Audio", self._enable_audio))
        page.append(SelectionBinding('2', f'Adjust Music Volume ({settings.get_music_volume()}%)',
                                     self.adjust_volume_setting(settings.set_music_volume)))
        page.append(SelectionBinding('3', f'Adjust SFX Volume ({settings.get_sfx_volume()}%)',
                                     self.adjust_volume_setting(settings.set_sfx_volume)))
        return [page]

    def construct_control_component(self) -> LabeledSelectionComponent:
        return LabeledSelectionComponent(self.game_state, [
            SelectionBinding('R', 'Return', functional_component()(self._return))])

    def can_exit(self):
        return self.exit_settings

    def _return(self):
        self.exit_settings = True

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
    def adjust_volume_setting(setter: Callable[[int], None]) -> type[Component]:
        @functional_component()
        def _component():
            while True:
                val = safe_input("(0-100)")
                if val.isdigit() and 0 <= int(val) <= 100:
                    setter(int(val))
                    break
                if not val.isdigit():
                    print_and_sleep(yellow("invalid setting"))
                else:
                    print_and_sleep(yellow("must from between 0 and 100"))

        return _component
