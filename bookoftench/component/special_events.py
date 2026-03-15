from bookoftench.component import RandomChoiceComponent, register_component, ProbabilityBinding, \
    get_registered_component
from bookoftench.data.components import SPECIAL_EVENTS
from bookoftench.model import GameState


@register_component(SPECIAL_EVENTS)
class SpecialEvents(RandomChoiceComponent):
    def __init__(self, game_state: GameState):
        evp = game_state.current_area.event_probabilities
        super().__init__(game_state, bindings=[ProbabilityBinding(prob, get_registered_component(name))
                                               for name, prob in evp.items()])