import random
from abc import abstractmethod, ABC

from markdown_it.rules_core.replacements import RARE_RE

from bookoftench import event_logger
from bookoftench.audio import play_music, play_sound
from bookoftench.component.base import functional_component, GatekeepingComponent, \
    LabeledSelectionComponent, ReprBinding, SelectionBinding, Component, NoOpComponent
from bookoftench.data.fish import Fish_Species, LEGENDARY, RARE, UNCOMMON, COMMON, SPOOKED, ENRAGED
from bookoftench.data.boat import FISHING_BATTLE_OPTIONS, GIVE_LINE, OBSERVE, PULL, REEL
from bookoftench.data.fishing_areas import WET_SEASON_BITE_CHANCE_EFFECT, DRY_SEASON_BITE_CHANCE_EFFECT, WET_SEASON
from bookoftench.model import GameState
from bookoftench.model.fish import load_fishes, load_fish
from bookoftench.model.util import display_fishing_battle_header
from bookoftench.ui import yellow, dim, blue, white, green, red
from bookoftench.util import print_and_sleep

# ================================================================================================

class DryCastCheck(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: self.dry_check(),
                         accept_component=SpawnFish,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             dim("You came up dry."), 1.5)))

    def run(self):
        self.dry_check()

    def dry_check(self) -> bool:
        bite_chance = self.game_state.current_fishing_area.bite_chance

        season = self.game_state.season
        if season == WET_SEASON:
            bite_chance += WET_SEASON_BITE_CHANCE_EFFECT
        else:
            bite_chance -= DRY_SEASON_BITE_CHANCE_EFFECT

        bite_chance += ((self.game_state.player.fishing_lvl - 1) / 100)

        self.waiting_display()

        if random.random() < bite_chance:
            return False
        else:
            return True

    @staticmethod
    def waiting_display():
        count = random.randint(1, 5)
        for i in range(count):
            print_and_sleep(blue("..."), 2)

# ================================================================================================
# ================================================================================================

class SpawnFish(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: self.game_state.current_fish is not None,
                         accept_component=FishBattle,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             dim("You came up dry."), 1.5)))

    def execute_current(self) -> GameState:
        return self.spawn_fish()

    def spawn_fish(self) -> GameState:
        fishing_area = self.game_state.current_fishing_area
        time = self.game_state.time_of_day
        moon = self.game_state.moon
        bait = self.game_state.player.current_bait

        filtered = [i['name'] for i in Fish_Species if
                    fishing_area.name in i['areas'] and
                    time in i['time'] and
                    not i['moon'] or moon in i['moon'] and
                    bait in i['preferred_bait']
                    ]

        fishes = load_fishes(filtered)

        rarity = self.get_rarity()

        available = [i for i in fishes if i.rarity == rarity]

        if available:
            selection = load_fish(random.choice(available))
            selection.distance = random.randint(fishing_area.min_hook_distance, fishing_area.max_hook_distance)
            self.game_state.current_fish = selection
        else:
            print_and_sleep(yellow("No fish met the criteria. Add more fish bozo."))

        return self.game_state


# ================================================================================================

    @staticmethod
    def get_rarity():
        roll = random.random()

        if roll < 0.02:
            return LEGENDARY
        if roll < 0.10:
            return RARE
        if roll < 0.30:
            return UNCOMMON
        else:
            return COMMON

# ================================================================================================
# ================================================================================================

class FishBattle(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        options = [i['name'] for i in FISHING_BATTLE_OPTIONS.copy()]

        fishing_battle_option_bindings = [ReprBinding(str(i + 1), option,
                                       self._handle_selection_component(option), option) for
                          i, option in enumerate(options)]

        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*fishing_battle_option_bindings, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                fishing_battle_option_bindings,
                top_level_prompt_callback=display_fishing_battle_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [return_binding]
            ),
        ]
        self.leave = False

    def play_theme(self) -> None:
        pass
        # play_music(FISHING_THEME)

    def _return(self):
        self.leave = True

    def can_exit(self) -> bool:
        return (self.leave or not self.game_state.player.is_alive() or
                self.game_state.fishing_area.casts == 0 or not self.game_state.current_fish)

    def display_options(self) -> None:
        for component in self.selection_components:
            component.display_options()

# ================================================================================================

    @staticmethod
    def _handle_selection_component(selection: str) -> type[Component]:
        @functional_component(state_dependent=True)
        def selection_component(game_state: GameState):

            if selection == PULL:
                 PullComponent(game_state).run()
            elif selection == REEL:
                ReelComponent(game_state).run()
            elif selection == GIVE_LINE:
                GiveLineComponent(game_state).run()
            elif selection == OBSERVE:
                ObserveComponent(game_state).run()
            else:
                return selection_component(game_state)

        return selection_component

# ================================================================================================
# ================================================================================================

class PullComponent(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        fish = self.game_state.current_fish
        caught = fish.caught
        lost = fish.lost
        
        pull = self.get_pull()
        self.apply_pull(pull)
        self.apply_pull_outcome()
        if caught or lost:
            pass
            # end fish battle component

    def get_pull(self) -> int:
        player = self.game_state.player
        fish = self.game_state.current_fish

        pull = random.randint(2, 5)
        pull += (100 - fish.stamina) / 20
        pull -= fish.strength
        if fish.state == SPOOKED:
            pull -= 1
        elif fish.state == ENRAGED:
            pull -= 2
        pull *= min(player.strength, 1.25)
        pull = max(1, pull)

        return round(pull)

    def apply_pull(self, pull: int):
        fish = self.game_state.current_fish

        stamina_loss = pull + random.randint(1, 3)
        rage_gain = random.randint(1, 3) + pull / 2

        # --- distance ---
        original_distance = fish.distance
        fish.distance -= round(pull)
        fish.distance = max(0, fish.distance)
        self.display_pull_result('Distance', original_distance, fish.distance)

        # --- stamina ---
        fish.stamina -= stamina_loss
        fish.stamina = max(0, fish.stamina)
        self.display_pull_result('Stamina', original_distance, fish.distance)

        # --- rage ---
        rage_gain *= fish.rage_factor
        fish.rage += round(rage_gain)
        fish.level = min(100, fish.rage)
        self.display_pull_result('Rage', original_distance, fish.distance)

    def apply_pull_outcome(self):
        player = self.game_state.player
        fish = self.game_state.current_fish
        location = self.game_state.current_fishing_area.name
        name = fish.name if player.fishing_lvl > 2 else "Unknown Fish"

        if fish.distance <= 0:
            fish.caught = True
            fish.catch_location = location
            print_and_sleep(green(f"You landed the {fish.name}!"), 1.5)
        elif fish.stamina <= 0:
            fish.caught = True
            fish.catch_location = location
            print_and_sleep(green(f"You reeled in the exhausted {fish.name}!"), 1.5)
        elif fish.rage >= 100:
            fish.lost = True
            print_and_sleep(red(f"The raging {name} got away!"), 1.5)
        else:
            pass

    @staticmethod
    def display_pull_result(variable: str, original: int, new: int):
        change = "increased" if original < new else "decreased"
        color = white

        if variable in ['Distance', 'Stamina']:
            color = green if change == "decreased" else yellow
        elif variable == ['Rage']:
            color = green if change == "increased" else yellow

        print_and_sleep(color(f"{variable}: {original} -> {new}"), 1)


    # fish turn







# ================================================================================================

class ReelComponent(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        pass

# ================================================================================================

class GiveLineComponent(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        pass

# ================================================================================================

class ObserveComponent(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        pass








