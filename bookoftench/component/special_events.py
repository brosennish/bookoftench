import random

from bookoftench.audio import play_music
from bookoftench.component import functional_component, Component, \
    LabeledSelectionComponent, ReprBinding, NoOpComponent, SelectionBinding, register_component
from bookoftench.data.components import SPECIAL_EVENT
from bookoftench.data.special_events import Special_Events
from bookoftench.model import GameState
from bookoftench.model.special_event import SpecialEvent, load_special_event
from bookoftench.util import print_and_sleep

# ================================================================================================

@register_component(SPECIAL_EVENT)
class DiscoverSpecial(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        game_state = self.game_state
        area = game_state.current_area
        season = game_state.season
        time = game_state.time_of_day
        moon = game_state.moon

        # --- filter out expired special events ---
        expired_names = [i.name for i in game_state.expired_special_events]

        fresh = [
            i for i in Special_Events
            if i['name'] not in expired_names
        ]

        # --- filter by conditions ---
        filtered = [
            i for i in fresh
            if area.name in i['areas']
               and time in i['time']
               and (i['moon'] is None or moon in i['moon'])
               and (i['season'] is None or season in i['season'])
        ]

        if not filtered:
            return game_state

        # --- select special event ---
        selected_data = random.choice(filtered)
        selected_event = load_special_event(selected_data['name'])

        # --- force sequential stage order ---
        if selected_event.stage > 1:
            for related_name in selected_event.related:
                related_event = load_special_event(related_name)

                if related_event.stage == selected_event.stage - 1:
                    if related_event.name not in expired_names:
                        selected_event = related_event
                    break

        special_event = selected_event

        return SpecialEventComponent(self.game_state, special_event).run()

# ================================================================================================

class SpecialEventComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState, event: SpecialEvent):

        self.special_event = event
        self.leave = False

        special_event_bindings = [
            ReprBinding(
                str(i + 1),
                choice,
                self._handle_selection_component(event, i + 1),
                choice
            )
            for i, choice in enumerate(event.choices)
        ]

        if event.optional:
            return_binding = SelectionBinding(
                "R",
                "Return",
                functional_component()(lambda: self._return())
            )
            bindings = [*special_event_bindings, return_binding]
        elif not event.choices:
            return_binding = SelectionBinding(
                "R",
                "Return",
                functional_component()(lambda: self._return())
            )
            bindings = [return_binding]
        else:
            bindings = special_event_bindings

        super().__init__(
            game_state,
            refresh_menu=False,
            bindings=bindings
        )

    def play_theme(self) -> None:
        if self.special_event.theme:
            play_music(self.special_event.theme)

    def _return(self):
        self.leave = True

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

    def display_options(self) -> None:
        print_and_sleep(self.special_event.color(self.special_event.text), self.special_event.sleep)
        super().display_options()

    # ============================================================================================

    def _handle_selection_component(
        self,
        special_event: SpecialEvent,
        choice: int
    ) -> type[Component]:

        @functional_component(state_dependent=True)
        def selection_component(game_state: GameState):
            method = getattr(special_event, special_event.method)
            method(game_state, choice)

            self.leave = True
            return game_state

        return selection_component
