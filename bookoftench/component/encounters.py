from bookoftench.component.base import Component
from bookoftench.component.registry import get_registered_component
from bookoftench.model import GameState


class PostKillEncounters(Component):
    def run(self) -> GameState:
        for component_name in self.game_state.current_area.post_kill_components:
            if self.game_state.player.is_alive():
                self.game_state = get_registered_component(component_name)(self.game_state).run()
        return self.game_state
