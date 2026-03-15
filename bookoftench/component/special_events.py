import random

from bookoftench.component import RandomChoiceComponent, register_component, ProbabilityBinding, \
    get_registered_component, functional_component
from bookoftench.data import Items
from bookoftench.data.components import DISCOVER_SPECIAL
from bookoftench.model import GameState
from bookoftench.ui import yellow, dim
from bookoftench.util import print_and_sleep


@register_component(DISCOVER_SPECIAL)
class DiscoverSpecial(RandomChoiceComponent):
    def __init__(self, game_state: GameState):
        evp = game_state.current_area.event_probabilities
        super().__init__(game_state, bindings=[ProbabilityBinding(prob, get_registered_component(name))
                                               for name, prob in evp.items()])

    @staticmethod
    @register_component(THREE_HOLES)
    @functional_component(state_dependent=True)
    def _discover_discoverable(game_state: GameState):
        player = game_state.player
        area = game_state.current_area
        good_hole = random.choice([i for i in Items if game_state.current_area in i.areas])
        bad_hole = random.randint(1, 20)
        dry_hole = print_and_sleep(yellow(dim("You came up dry.")), 1)


