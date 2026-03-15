from bookoftench.component import RandomChoiceComponent, register_component


@register_component(SPECIAL_EVENTS)
class SpecialEvents(RandomChoiceComponent):
    def __init__(self, game_state: GameState):
        ep = game_state.current_area.search_probabilities
        super().__init__(game_state, bindings=[ProbabilityBinding(prob, get_registered_component(name))
                                               for name, prob in ep.items()])