import random

from bookoftench import event_logger
from bookoftench.audio import play_music, play_sound
from bookoftench.component import LinearComponent
from bookoftench.component.base import functional_component, GatekeepingComponent, \
    LabeledSelectionComponent, ReprBinding, SelectionBinding, Component, NoOpComponent
from bookoftench.data.fish import Fish_Species, LEGENDARY, RARE, UNCOMMON, COMMON, SPOOKED, ENRAGED, CALM, AGITATED, \
    possible_observations, SPECIES, VARIANT, STRENGTH, SPEED, STAMINA, RAGE_FACTOR, TENCH
from bookoftench.data.boat import FISHING_BATTLE_OPTIONS, GIVE_LINE, OBSERVE, PULL, REEL
from bookoftench.data.fishing_areas import WET_SEASON_BITE_CHANCE_EFFECT, DRY_SEASON_BITE_CHANCE_EFFECT, WET_SEASON
from bookoftench.model import GameState
from bookoftench.model.fish import load_fishes, load_fish
from bookoftench.model.util import display_fishing_battle_header
from bookoftench.ui import yellow, dim, blue, white, green, red, purple, cyan
from bookoftench.util import print_and_sleep

# ================================================================================================

class DryCastCheck(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        dry = self.dry_check()
        if not dry:
            SpawnFish(self.game_state).run()
        else:
            print_and_sleep(yellow("You came up dry."), 1.5)

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

class SpawnFish(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, next_component=LaunchFishBattle)

    def execute_current(self) -> GameState:
        return self.spawn_fish()

    def spawn_fish(self) -> GameState:
        self.game_state.current_fish = load_fish(TENCH)
        return self.game_state

        fishing_area = self.game_state.current_fishing_area
        time = self.game_state.time_of_day
        moon = self.game_state.moon
        bait = self.game_state.player.current_bait

        filtered = [
            i['name']
            for i in Fish_Species
            if fishing_area.name in i['areas']
               and time in i['time']
               and (i['moon'] is None or moon in i['moon'])
               and bait in i['preferred_bait']
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

class LaunchFishBattle(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: self.game_state.current_fish is not None,
                         accept_component=FishBattle,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             dim("You came up dry."), 1.5)))

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
                self.game_state.current_fishing_area.casts == 0 or not self.game_state.current_fish)

    def display_options(self) -> None:
        for component in self.selection_components:
            component.display_options()

# ================================================================================================

    @staticmethod
    def _handle_selection_component(selection: str) -> type[Component]:
        @functional_component(state_dependent=True)
        def selection_component(game_state: GameState):

            if selection == PULL:
                 Pull(game_state).run()
            elif selection == REEL:
                Reel(game_state).run()
            elif selection == GIVE_LINE:
                GiveLine(game_state).run()
            elif selection == OBSERVE:
                ObserveFish(game_state).run()
            else:
                return selection_component(game_state)

        return selection_component

# ================================================================================================
# ================================================================================================

class EndFishBattle(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        return

# ================================================================================================
# ================================================================================================

class FishTurn(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        fish = self.game_state.current_fish

        self.spit_hook(fish)

        if fish.lost:
            EndFishBattle(self.game_state).run()
            return

        self.fish_runs(fish)
        self.fish_gains_rage(fish)
        self.update_fish_state(fish)
        self.apply_fish_turn_outcome()

        if fish.lost:
            EndFishBattle(self.game_state).run()
        else:
            FishBattle(self.game_state).run()

    @staticmethod
    def spit_hook(fish):
        if random.random() < fish.spit_hook_chance:
            fish.lost = True

    @staticmethod
    def fish_runs(fish):
        stamina_ratio = fish.stamina / fish.max_stamina

        # --- stamina ---
        if stamina_ratio < 0.33:
            stamina_modifier = 0.5
        elif stamina_ratio < 0.67:
            stamina_modifier = 0.75
        else:
            stamina_modifier = 1

        # --- state ---
        if fish.state == AGITATED:
            state_modifier = 1.1
        elif fish.state == SPOOKED:
            state_modifier = 1.25
        elif fish.state == ENRAGED:
            state_modifier = 1.5
        else:
            state_modifier = 1

        run = random.randint(2, 5)
        run *= fish.speed
        run *= stamina_modifier
        run *= state_modifier
        run = max(1, round(run))
        fish.distance += run

    @staticmethod
    def fish_gains_rage(fish):
        rage_gain = random.randint(1, 3)
        stamina_ratio = fish.stamina / fish.max_stamina

        if fish.state == AGITATED:
            state_modifier = 1.1
        elif fish.state == SPOOKED:
            state_modifier = 1.25
        elif fish.state == ENRAGED:
            state_modifier = 1.5
        else:
            state_modifier = 1

        # --- stamina ---
        if stamina_ratio < 0.33:
            stamina_modifier = 1.5
        elif stamina_ratio < 0.67:
            stamina_modifier = 1.25
        else:
            stamina_modifier = 1

        rage_gain *= fish.rage_factor
        rage_gain *= state_modifier
        rage_gain *= stamina_modifier
        fish.rage = min(100, fish.rage)
        fish.rage += round(rage_gain)

    @staticmethod
    def update_fish_state(fish):
        if fish.rage >= 75:
            fish.state = ENRAGED
        elif fish.rage >= 50:
            fish.state = SPOOKED
        elif fish.rage >= 25:
            fish.state = AGITATED
        else:
            fish.state = CALM

    def apply_fish_turn_outcome(self):
        fish = self.game_state.current_fish
        area = self.game_state.current_fishing_area
        fishing_level = self.game_state.player.fishing_lvl
        name = fish.name if fishing_level > 2 else "Unknown Fish"

        if fish.distance >= area.escape_distance:
            fish.lost = True
            print_and_sleep(red(f"The fish gained too much distance and escaped!"), 1.5)
        elif fish.rage >= 100:
            fish.lost = True
            print_and_sleep(red(f"The enraged {name} broke free and escaped!"), 1.5)


# ================================================================================================
# ================================================================================================

class Pull(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        fish = self.game_state.current_fish
        
        pull = self.get_pull()
        self.apply_pull(pull)
        self.apply_pull_outcome()
        if fish.caught or fish.lost:
            EndFishBattle(self.game_state).run()
        else:
            FishTurn(self.game_state).run()

    def get_pull(self) -> int:
        # --- variables ---
        player = self.game_state.player
        fish = self.game_state.current_fish
        missing_stamina_ratio = (fish.max_stamina - fish.stamina) / fish.max_stamina
        pull_bonus = missing_stamina_ratio * 5

        # --- logic ---
        pull = random.randint(2, 5)
        pull += pull_bonus
        pull -= fish.strength

        if fish.state == AGITATED:
            pull -= 1
        elif fish.state == SPOOKED:
            pull -= 2
        elif fish.state == ENRAGED:
            pull -= 3

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
        original_stamina = fish.stamina
        fish.stamina -= stamina_loss
        fish.stamina = max(0, fish.stamina)
        self.display_pull_result('Stamina', original_stamina, fish.stamina)

        # --- rage ---
        original_rage = fish.rage
        rage_gain *= fish.rage_factor
        fish.rage += round(rage_gain)
        fish.rage = min(100, fish.rage)
        FishTurn.update_fish_state(fish)

        self.display_pull_result('Rage', original_rage, fish.rage)

    def apply_pull_outcome(self):
        player = self.game_state.player
        fish = self.game_state.current_fish
        location = self.game_state.current_fishing_area.name
        name = fish.name if player.fishing_lvl > 2 else "Unknown Fish"

        if fish.distance <= 0:
            fish.caught = True
            fish.catch_location = location
            print_and_sleep(green(f"You caught a {fish.name}!"), 1.5)
        elif fish.stamina <= 0:
            fish.caught = True
            fish.catch_location = location
            print_and_sleep(green(f"You reeled in an exhausted {fish.name}!"), 1.5)
        elif fish.rage >= 100:
            fish.lost = True
            print_and_sleep(red(f"The raging {name} got away!"), 1.5)
        else:
            pass

# ================================================================================================
# ================================================================================================

class Reel(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        fish = self.game_state.current_fish
        player = self.game_state.player

        reel = self.get_reel(fish, player)
        self.apply_reel(reel, fish)
        self.apply_reel_outcome(fish)
        if fish.caught or fish.lost:
            EndFishBattle(self.game_state).run()
        else:
            FishTurn(self.game_state).run()

    @staticmethod
    def get_reel(fish, player) -> int:
        reel = random.randint(1, 3)
        missing_stamina_ratio = (fish.max_stamina - fish.stamina) / fish.max_stamina

        reel += missing_stamina_ratio * 3
        reel -= fish.strength * 0.5

        if fish.state == AGITATED:
            reel -= 0.25
        elif fish.state == SPOOKED:
            reel -= 0.5
        elif fish.state == ENRAGED:
            reel -= 1

        reel += min(player.fishing_lvl // 2, 3)
        reel *= min(player.strength, 1.15)
        reel = max(1, reel)

        return round(reel)

    def apply_reel(self, reel: int, fish):
        stamina_loss = max(1, round(reel / 2)) + random.randint(0, 1)
        rage_gain = random.randint(0, 1) + reel / 3

        # --- distance ---
        original_distance = fish.distance
        fish.distance -= round(reel)
        fish.distance = max(0, fish.distance)
        display_result('Distance', original_distance, fish.distance)

        # --- stamina ---
        original_stamina = fish.stamina
        fish.stamina -= stamina_loss
        fish.stamina = max(0, fish.stamina)
        display_result('Stamina', original_stamina, fish.stamina)

        # --- rage ---
        original_rage = fish.rage
        rage_gain *= fish.rage_factor
        fish.rage += round(rage_gain)
        fish.rage = min(100, fish.rage)
        FishTurn.update_fish_state(fish)

        display_result('Rage', original_rage, fish.rage)

    def apply_reel_outcome(self, fish):
        player = self.game_state.player
        location = self.game_state.current_fishing_area.name
        name = fish.name if player.fishing_lvl > 2 else "Unknown Fish"

        if fish.distance <= 0:
            fish.caught = True
            fish.catch_location = location
            print_and_sleep(green(f"You caught a {fish.name}!"), 1.5)
        elif fish.stamina <= 0:
            fish.caught = True
            fish.catch_location = location
            print_and_sleep(green(f"You reeled in an exhausted {fish.name}!"), 1.5)
        elif fish.rage >= 100:
            fish.lost = True
            print_and_sleep(red(f"The raging {name} got away!"), 1.5)
        else:
            pass

# ================================================================================================

class GiveLine(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        fish = self.game_state.current_fish
        player = self.game_state.player

        line = self.get_give_line(fish)
        self.apply_give_line(fish, line, player)
        self.apply_give_line_outcome(fish)
        if fish.caught or fish.lost:
            EndFishBattle(self.game_state).run()
        else:
            FishTurn(self.game_state).run()

    @staticmethod
    def get_give_line(fish) -> int:
        line = random.randint(2, 4)
        line *= fish.speed

        if fish.state == AGITATED:
            line += 1
        elif fish.state == SPOOKED:
            line += 2
        elif fish.state == ENRAGED:
            line += 4

        return round(line)

    @staticmethod
    def apply_give_line(self, fish, line, player):
        # --- distance ---
        original_distance = fish.distance
        fish.distance += line
        display_result('Distance', original_distance, fish.distance)

        # --- rage ---
        original_rage = fish.rage
        rage_loss = random.randint(6, 10)

        if fish.state == AGITATED:
            rage_loss += 1
        elif fish.state == SPOOKED:
            rage_loss += 2
        elif fish.state == ENRAGED:
            rage_loss += 4

        rage_loss += min(player.fishing_lvl // 2, 3)
        fish.rage -= rage_loss
        fish.rage = max(0, fish.rage)
        FishTurn.update_fish_state(fish)

        display_result('Rage', original_rage, fish.rage)

    def apply_give_line_outcome(self, fish):
        player = self.game_state.player
        location = self.game_state.current_fishing_area.name
        name = fish.name if player.fishing_lvl > 2 else "Unknown Fish"

        if fish.distance <= 0:
            fish.caught = True
            fish.catch_location = location
            print_and_sleep(green(f"You caught a {fish.name}!"), 1.5)
        elif fish.rage >= 100:
            fish.lost = True
            print_and_sleep(red(f"The raging {name} got away!"), 1.5)
        else:
            pass

# ================================================================================================

class ObserveFish(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        fish = self.game_state.current_fish

        observation = self.get_observation(fish)
        if observation:
            self.apply_observation(fish, observation)
            FishTurn(self.game_state).run()
        else:
            print_and_sleep(yellow(f"You must catch this fish to learn more."), 1.5)

    @staticmethod
    def get_observation(fish) -> str | None:
        valid = [i for i in possible_observations if i not in fish.observed_characteristics]
        if valid:
            observation = random.choice(valid)
        else:
            return None

        return observation

    def apply_observation(self, fish, observation):
        fish.observed_characteristics.append(observation)

        if observation == SPECIES:
            color = white
            word = SPECIES
            value = fish.base_name
            fish.species_observed = True
        elif observation == VARIANT:
            color = purple
            word = VARIANT
            value = fish.variant if fish.variant else "None"
            fish.variant_observed = True
        elif observation == STRENGTH:
            color = yellow
            word = STRENGTH
            value = str(round(fish.strength, 2))
            fish.strength_observed = True
        elif observation == SPEED:
            color = cyan
            word = SPEED
            value = str(round(fish.speed, 2))
            fish.speed_observed = True
        elif observation == STAMINA:
            color = green
            word = STAMINA
            value = f"{round((fish.stamina / fish.max_stamina) * 100)}%"
            fish.stamina_observed = True
        elif observation == RAGE_FACTOR:
            color = red
            word = RAGE_FACTOR
            value = str(round(fish.rage_factor, 2))
            fish.rage_factor_observed = True
        else:
            return

        self.display_observation_result(color, word, value)

    @staticmethod
    def display_observation_result(color, word: str, value: str) -> None:

        print_and_sleep(blue(f"You observe the fish to gain insight..."), 1.5)
        print_and_sleep(f"{color(word)}: {value}", 1.5)

# ================================================================================================

def display_result(variable: str, original: int, new: int):
    if original > new:
        change = "decreased"
    elif original < new:
        change = "increased"
    else:
        change = None

    color = white

    if change:
        if variable in ['Distance', 'Stamina']:
            color = green if change == "decreased" else yellow
        elif variable == 'Rage':
            color = green if change == "decreased" else red
        print_and_sleep(color(f"{variable}: {original} -> {new}"), 1)
    else:
        print_and_sleep(f"{variable}: {original}", 1)
