import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Callable, Any, Optional

from savethewench.model import GameState
from savethewench.ui import dim, yellow
from savethewench.util import print_and_sleep, safe_input


class Component(ABC):
    def __init__(self, game_state: GameState):
        self.game_state = game_state

    def play_theme(self):
        pass

    @abstractmethod
    def run(self) -> GameState:
        pass


def functional_component(state_dependent=False) -> Callable[[Callable], type[Component]]:
    def decorator(func: Callable):
        class FunctionalComponent(Component):
            def run(self) -> GameState:
                if state_dependent:
                    func(self.game_state)
                else:
                    func()
                return self.game_state

        return FunctionalComponent

    return decorator


class NoOpComponent(Component):
    def run(self) -> GameState:
        return self.game_state


@dataclass
class SelectionBinding:
    key: str
    name: str
    component: type[Component]

    def format(self):
        return self.name


@dataclass
class ReprBinding(SelectionBinding):
    repr_object: Any

    def format(self):
        return self.repr_object


class SelectionComponent(Component):
    def __init__(self, game_state: GameState, refresh_menu: bool = False):
        super().__init__(game_state)
        self.refresh_menu = refresh_menu

    @abstractmethod
    def display_options(self):
        pass

    @abstractmethod
    def handle_selection(self) -> GameState:
        pass

    @abstractmethod
    def can_exit(self) -> bool:
        pass

    def run(self) -> GameState:
        while not self.can_exit():
            if self.refresh_menu:
                self.__init__(
                    game_state=self.game_state)  # re-init to update listings (should find a way to do this more efficiently)
            self.play_theme()
            self.display_options()
            self.game_state = self.handle_selection()
        return self.game_state


class LabeledSelectionComponent(SelectionComponent):
    def __init__(self, game_state: GameState, bindings: List[SelectionBinding],
                 top_level_prompt_callback: Callable[[GameState], None] = lambda _: None,
                 quittable: bool = False, refresh_menu: bool = False):
        super().__init__(game_state, refresh_menu)
        self.binding_map = dict((bnd.key.lower(), bnd) for bnd in bindings)
        self.top_level_prompt_callback = top_level_prompt_callback
        self.quittable = quittable
        self.made_selection = False

    def display_options(self):
        self.top_level_prompt_callback(self.game_state)
        print_and_sleep(f"{'\n'.join(f"{f"[{v.key}]":<4}: {v.format()}" for _, v in self.binding_map.items())}")

    def run_selected_component(self, binding: SelectionBinding) -> GameState:
        return binding.component(self.game_state).run()

    def handle_selection(self) -> GameState:
        selection = safe_input(f"Please enter a selection{' (q to exit)' if self.quittable else ''}").strip().lower()
        if selection not in self.binding_map:
            if self.quittable and selection == 'q':
                self.made_selection = True
            else:
                print_and_sleep(yellow("Invalid selection"), 0.5)
            return self.game_state
        else:
            self.made_selection = True
            return self.run_selected_component(self.binding_map[selection])

    def can_exit(self):
        return self.made_selection

class PaginatedMenuComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState,
                 top_level_prompt_callback: Callable[[GameState], None] = lambda _: None,
                 main_menu_component: Optional[type[Component]] = None):
        super().__init__(game_state, bindings=[]) # dynamically set self.binding_map depending on page
        self.top_level_prompt_callback = top_level_prompt_callback
        self.main_menu_component = main_menu_component
        self.pages = self.construct_pages()
        self.current_page = 0

    @abstractmethod
    def construct_pages(self) -> List[List[SelectionBinding]]:
        pass

    def _next_page(self) -> type[Component]:
        def _component() -> None:
            if self.current_page < len(self.pages) - 1:
                self.current_page += 1
            else:
                raise RuntimeError("No next page exists")
        return functional_component()(_component)

    def _previous_page(self) -> type[Component]:
        def _component() -> None:
            if self.current_page > 0:
                self.current_page -= 1
            else:
                raise RuntimeError("No previous page exists")
        return functional_component()(_component)

    def construct_control_component(self) -> LabeledSelectionComponent:
        previous_page_binding = SelectionBinding('P', 'Previous Page', self._previous_page())
        next_page_binding = SelectionBinding('N', 'Next Page', self._next_page())
        res = []
        if self.current_page > 0:
            res.append(previous_page_binding)
        if self.current_page < len(self.pages) - 1:
            res.append(next_page_binding)
        if self.main_menu_component is not None:
            res.append(SelectionBinding('M', 'Main Menu', self.main_menu_component))
        return LabeledSelectionComponent(self.game_state, res)

    def construct_components(self) -> List[LabeledSelectionComponent]:
        self.pages = self.construct_pages()
        if not (0 <= self.current_page <= len(self.pages) - 1):
            raise RuntimeError(f"Invalid page {self.current_page}. Must be between 0 and {len(self.pages) - 1}")
        page = self.pages[self.current_page]
        return [LabeledSelectionComponent(self.game_state, page, self.top_level_prompt_callback),
                self.construct_control_component()]

    def display_options(self):
        for component in self.construct_components():
            component.display_options()

    def handle_selection(self) -> GameState:
        self.binding_map = {}
        for component in self.construct_components():
            self.binding_map |= component.binding_map
        return super().handle_selection()


class LinearComponent(Component):
    def __init__(self, game_state: GameState, next_component: type[Component]):
        super().__init__(game_state)
        self.next_component = next_component

    @abstractmethod
    def execute_current(self) -> GameState:
        pass

    def run(self) -> GameState:
        self.play_theme()
        self.game_state = self.execute_current()
        return self.next_component(self.game_state).run()


class BinarySelectionComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState, query: str, yes_component: type[Component],
                 no_component: type[Component]):
        super().__init__(game_state,
                         bindings=[SelectionBinding('y', '', yes_component),
                                   SelectionBinding('n', '', no_component)])
        self.query = query

    def display_options(self):
        print_and_sleep(f"{self.query.strip()} (y/n)?")


class TextDisplayingComponent(LinearComponent):
    def __init__(self, game_state: GameState, display_callback: Callable[[GameState], None],
                 next_component: type[Component] = NoOpComponent):
        super().__init__(game_state, next_component)
        self.display_callback = display_callback

    def execute_current(self) -> GameState:
        self.display_callback(self.game_state)
        safe_input()
        return self.next_component(self.game_state).run()


@dataclass
class ProbabilityBinding:
    percent_chance: int
    component: type[Component]

    def __post_init__(self):
        if not (0 <= self.percent_chance <= 100):
            raise ValueError(f"percent_chance must be between 0 and 100, got {self.percent_chance}.")


class RandomChoiceComponent(Component):
    def __init__(self, game_state: GameState, bindings: List[ProbabilityBinding],
                 failed_message: str = dim("You came up dry.")):
        super().__init__(game_state)
        self.bindings = bindings
        self.failed_message = failed_message
        if sum(b.percent_chance for b in self.bindings) > 100:
            raise ValueError(f"Probability bindings must sum to between 0 and 100, "
                             f"got {sum(b.percent_chance for b in self.bindings)}.")

    def run(self) -> GameState:
        roll = random.random()
        current = 0
        for binding in self.bindings:
            probability = binding.percent_chance / 100.0
            if roll < current + probability:
                return binding.component(self.game_state).run()
            current += probability
        print_and_sleep(self.failed_message, 1)
        return self.game_state


class GatekeepingComponent(Component):
    def __init__(self, game_state: GameState, decision_function: Callable[[], bool],
                 accept_component: type[Component], deny_component: type[Component]):
        super().__init__(game_state)
        self.decision_function = decision_function
        self.accept_component = accept_component
        self.deny_component = deny_component

    def run(self) -> GameState:
        if self.decision_function():
            return self.accept_component(self.game_state).run()
        else:
            return self.deny_component(self.game_state).run()


@dataclass
class ColoredNameSelectionBinding(SelectionBinding):
    color: Callable[[str], str]

    def format(self):
        return self.color(self.name)
