import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Callable

from data.colors import blue as b, dim as d, reset as rst
from model.game_state import GameState


class Component(ABC):
    def __init__(self, game_state: GameState):
        self.game_state = game_state

    @abstractmethod
    def run(self) -> GameState:
        pass


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


class SelectionComponent(Component):
    @abstractmethod
    def display_options(self):
        pass

    @abstractmethod
    def handle_selection(self) -> GameState:
        pass

    @abstractmethod
    def can_exit(self):
        pass

    def run(self) -> GameState:
        while not self.can_exit():
            self.display_options()
            self.game_state = self.handle_selection()
        return self.game_state


class LabeledSelectionComponent(SelectionComponent):
    def __init__(self, game_state: GameState, bindings: List[SelectionBinding],
                 top_level_prompt_callback: Callable[[GameState], None] = lambda _: None):
        super().__init__(game_state)
        self.binding_map = dict((bnd.key.lower(), bnd) for bnd in bindings)
        self.top_level_prompt_callback = top_level_prompt_callback
        self.success = False

    def display_options(self):
        self.top_level_prompt_callback(self.game_state)
        for _, v in self.binding_map.items():
            print(f"{v.key}: {v.format()}")
        print()

    def run_selected_component(self, binding: SelectionBinding) -> GameState:
        return binding.component(self.game_state).run()

    def handle_selection(self) -> GameState:
        selection = input("Please enter a selection: ").strip().lower()
        if selection not in self.binding_map:
            print("Invalid selection")
            return self.game_state
        else:
            self.success = True
            return self.run_selected_component(self.binding_map[selection])

    def can_exit(self):
        return self.success


class LinearComponent(Component):
    def __init__(self, game_state: GameState, next_component: type[Component], should_proceed: bool = True):
        super().__init__(game_state)
        self.next_component = next_component
        self.should_proceed = should_proceed

    @abstractmethod
    def execute_current(self) -> GameState:
        pass

    def run(self) -> GameState:
        self.game_state = self.execute_current()
        if self.should_proceed:
            return self.next_component(self.game_state).run()
        return self.game_state


class BinarySelectionComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState, query: str, yes_component: type[Component], no_component: type[Component]):
        super().__init__(game_state,
                         bindings=[SelectionBinding('y', '', yes_component),
                                   SelectionBinding('n', '', no_component)])
        self.query = query

    def display_options(self):
        print(f"{self.query.strip()} (y/n)?\n{b}>{rst} ")


class TextDisplayingComponent(LinearComponent):
    def __init__(self, game_state: GameState, display_callback: Callable[[GameState], None],
                 next_component: type[Component] = NoOpComponent, should_proceed: bool = True):
        super().__init__(game_state, next_component, should_proceed)
        self.display_callback = display_callback

    def execute_current(self) -> GameState:
        self.display_callback(self.game_state)
        input("Press Enter to continue...")
        return self.game_state


class FunctionExecutingComponent(Component):
    def __init__(self, game_state: GameState, function: Callable[[GameState], GameState]):
        super().__init__(game_state)
        self.function = function

    def run(self) -> GameState:
        return self.function(self.game_state)


@dataclass
class FunctionalSelectionBinding(SelectionBinding):
    component: type[FunctionExecutingComponent]
    function: Callable[[GameState], GameState]


class FunctionalSelectionComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState, bindings: List[FunctionalSelectionBinding]):
        super().__init__(game_state, bindings)

    def run_selected_component(self, binding: FunctionalSelectionBinding) -> GameState:
        return binding.component(self.game_state, binding.function).run()


@dataclass
class ThresholdBinding:
    upper_threshold: float
    component: type[Component]

    def __post_init__(self):
        if not (0 <= self.upper_threshold <= 1):
            raise ValueError("upper_threshold must be between 0 and 1")


class RandomThresholdComponent(Component):
    def __init__(self, game_state: GameState, bindings: List[ThresholdBinding], failed_message: str = f"{d}You came up dry."):
        super().__init__(game_state)
        self.ordered_thresholds = sorted(bindings, key=lambda t: t.upper_threshold)
        self.failed_message = failed_message

    def run(self) -> GameState:
        roll = random.random()
        for binding in self.ordered_thresholds:
            if roll < binding.upper_threshold:
                return binding.component(self.game_state).run()
        print(self.failed_message)
        return self.game_state
