import random

from bookoftench.audio import play_sound, stop_music, play_music
from bookoftench.component.base import functional_component, GatekeepingComponent, \
    LabeledSelectionComponent, ReprBinding, SelectionBinding, Component, NoOpComponent, LinearComponent, \
    TextDisplayingComponent
from bookoftench.data.audio import COINS, CATCH_FISH, GOLF_CLAP, FISH_ON, CAST, ENEMY_APPEARS, \
    OCEAN_THEME, BAY_THEME, SHALLOWS_THEME, FISH, WHIFF
from bookoftench.data.environment import CLEAR, MURKY
from bookoftench.data.fish import Fish_Species, LEGENDARY, RARE, UNCOMMON, COMMON, SPOOKED, ENRAGED, CALM, AGITATED, \
    SPECIES, VARIANT, STRENGTH, SPEED, RAGE_FACTOR, RARITY, STAMINA, SHALLOWS, BAY, MYTHIC, possible_observations
from bookoftench.data.boat import FISHING_BATTLE_OPTIONS, GIVE_LINE, OBSERVE, PULL, REEL, USE_ITEM
from bookoftench.data.fishing_areas import WET_SEASON_BITE_CHANCE_EFFECT, DRY_SEASON_BITE_CHANCE_EFFECT, WET_SEASON
from bookoftench.data.fishing_items import BARB_HOOK, RAGE
from bookoftench.model import GameState
from bookoftench.model.fish import load_fishes
from bookoftench.model.player import Player
from bookoftench.model.util import display_fishing_battle_header, display_fishing_actions, display_fishing_info
from bookoftench.ui import yellow, dim, blue, white, green, red, purple, cyan, orange
from bookoftench.util import print_and_sleep

# ================================================================================================

class DryCastCheck(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self) -> GameState:
        if self.game_state.current_fishing_area.casts == 0:
            return self.game_state

        player = self.game_state.player

        if not player.current_bait or player.current_bait.casts == 0:
            return self.game_state

        self.game_state.current_fishing_area.casts -= 1
        player.current_bait.casts -= 1

        if self.dry_check():
            print_and_sleep("You came up dry.", 1)
            return self.game_state

        return SpawnFish(self.game_state).run()

    def dry_check(self) -> bool:
        bite_chance = self.game_state.get_bite_chance()

        if random.random() < bite_chance:
            value = random.randint(1, 3)
            self.waiting_display(value)
            return False
        else:
            self.waiting_display(3)
            return True

    @staticmethod
    def waiting_display(value: int):
        play_sound(CAST)
        for i in range(value):
            print_and_sleep(blue("..."), 0.8)

# ================================================================================================
# ================================================================================================

class SpawnFish(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, next_component=LaunchFishBattle)

    def execute_current(self) -> GameState:
        self.spawn_fish()
        return self.game_state

    def spawn_fish(self) -> None:
        player = self.game_state.player
        fishing_area = self.game_state.current_fishing_area
        bait = player.current_bait

        if bait.casts == 0:
            player.current_bait = None
            return

        if self.game_state.all_fish:
            valid = Fish_Species
        else:
            caught = [fish.name for fish in player.caught_fish]
            valid = [fish for fish in Fish_Species if fish["name"] not in caught]

        filtered = self.get_filtered(valid)
        fishes = load_fishes(filtered)

        rarity = self.get_rarity(player.luck)
        available = [fish for fish in fishes if fish.rarity == rarity]

        # --- check one lower rarity for match if needed ---
        if not available:
            rarity_order = [MYTHIC, LEGENDARY, RARE, UNCOMMON, COMMON]
            current_index = rarity_order.index(rarity)

            if current_index < len(rarity_order) - 1:
                fallback_rarity = rarity_order[current_index + 1]
                available = [fish for fish in fishes if fish.rarity == fallback_rarity]

        if not available:
            self.game_state.current_fish = None
            print_and_sleep(dim("You got a bite, but nothing took the bait."), 1)
            return

        selection = random.choice(available)
        selection.distance = random.randint(
            fishing_area.min_hook_distance,
            fishing_area.max_hook_distance,
        )

        self.game_state.current_fish = selection

        stop_music()
        play_sound(FISH_ON)
        play_sound(ENEMY_APPEARS)
        print_and_sleep(orange("Fish on!"), 1.5)

    def get_filtered(self, valid: list[dict]) -> list[str]:
        fishing_area = self.game_state.current_fishing_area
        time_of_day = self.game_state.time_of_day
        bait = self.game_state.player.current_bait
        moon = self.game_state.moon

        filtered = [
            fish["name"]
            for fish in valid
            if fishing_area.name in fish["areas"]
               and time_of_day in fish["time"]
               and (fish["moon"] is None or moon in fish["moon"])
               and bait.name in fish["preferred_bait"]
        ]

        return filtered

# ================================================================================================

    @staticmethod
    def get_rarity(luck):
        roll = random.random()
        luck_bonus = min((luck - 1) / 100, 0.08)

        if roll < 0.001 + luck_bonus:
            return MYTHIC
        if roll < 0.02 + luck_bonus:
            return LEGENDARY
        if roll < 0.10 + luck_bonus:
            return RARE
        if roll < 0.30 + luck_bonus:
            return UNCOMMON
        return COMMON

# ================================================================================================

class LaunchFishBattle(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         decision_function=self._fish_is_hooked,
                         accept_component=FishBattle,
                         deny_component=no_fish_hooked)

    def _fish_is_hooked(self) -> bool:
        return self.game_state.current_fish is not None


@functional_component(state_dependent=True)
def no_fish_hooked(game_state: GameState) -> GameState:
    return game_state

# ================================================================================================
# ================================================================================================

class FishBattle(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        options = [i['name'] for i in FISHING_BATTLE_OPTIONS.copy()]

        fishing_battle_option_bindings = [ReprBinding(str(i + 1), option,
                                       self._handle_selection_component(option), option) for
                          i, option in enumerate(options)]

        view_actions_binding = SelectionBinding('V', "View Actions", ViewFishingActions)
        view_info_binding = SelectionBinding('M', "More Info", ViewFishingInfo)
        return_binding = SelectionBinding(
            "R",
            "Return",
            self._make_return_component(),
        )

        super().__init__(game_state, refresh_menu=True,
                         bindings=[*fishing_battle_option_bindings, view_actions_binding,
                                   view_info_binding, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                fishing_battle_option_bindings,
            ),
            LabeledSelectionComponent(
                game_state,
                [view_actions_binding, view_info_binding, return_binding]
            ),
        ]
        self.leave = False

    def play_theme(self) -> None:
        play_sound(FISH)

        if self.game_state.current_fishing_area == SHALLOWS:
            play_music(SHALLOWS_THEME)
        elif self.game_state.current_fishing_area == BAY:
            play_music(BAY_THEME)
        else:
            play_music(OCEAN_THEME)

    def _return(self) -> GameState:
        self.leave = True
        return self.game_state

    def _make_return_component(self) -> type[Component]:
        @functional_component()
        def return_component() -> GameState:
            return self._return()

        return return_component

    def can_exit(self) -> bool:
        no_active_fish = self.game_state.current_fish is None

        return (
                self.leave
                or not self.game_state.player.is_alive()
                or no_active_fish
        )

    def display_options(self) -> None:
        display_fishing_battle_header(self.game_state)

        for component in self.selection_components:
            component.display_options()

# ================================================================================================

    @staticmethod
    def _handle_selection_component(selection: str) -> type[Component]:
        @functional_component(state_dependent=True)
        def selection_component(game_state: GameState) -> GameState:
            from bookoftench.component import FishingItemBox

            if selection == PULL:
                return Pull(game_state).run()

            if selection == REEL:
                return Reel(game_state).run()

            if selection == GIVE_LINE:
                return GiveLine(game_state).run()

            if selection == OBSERVE:
                return ObserveFish(game_state).run()

            if selection == USE_ITEM:
                return FishingItemBox(game_state).run()

            return game_state

        return selection_component

# ================================================================================================

class ViewFishingActions(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_fishing_actions)

class ViewFishingInfo(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_fishing_info)

# ================================================================================================

class EndFishBattle(NoOpComponent):
    def run(self) -> GameState:
        fish = self.game_state.current_fish

        if fish is None:
            return self.game_state

        if fish.caught:
            self.display_catch()
            self.award_xp()
            self.sell_fish()
            self.update_log()

        self.game_state = self.reset_state()
        return self.game_state

    def reset_state(self) -> GameState:
        from bookoftench.component import OfficerEncounter

        if self.game_state.current_fish.protected:
            if random.random() < 0.25:
                self.game_state = OfficerEncounter(self.game_state).run()

        self.game_state.current_fish = None
        self.game_state.player.active_fishing_items.clear()

        return self.game_state

    def display_catch(self):
        player = self.game_state.player
        fish = self.game_state.current_fish
        rarity = fish.get_rarity_text()

        caught = [i.base_name for i in player.caught_fish]
        if fish.base_name not in caught:
            new = green("[NEW SPECIES]")
        else:
            new = ""

        play_sound(CATCH_FISH)
        play_sound(GOLF_CLAP)

        print_and_sleep("\n".join([
            cyan(f"You caught a {fish.name}! {new}"),
            "",
            dim(f"{fish.description}"),
            "",
            f"Rarity: {rarity}",
            f"Length: {yellow(f'{fish.length} in')}",
            f"Weight: {yellow(f'{round(fish.weight, 2)} lbs')}",
            f"Value: {green(f'{fish.value} coins')}",
            "",
            f"Strength: {yellow(round(fish.strength, 2))}",
            f"Speed: {cyan(round(fish.speed, 2))}",
            f"Rage Factor: {red(round(fish.rage_factor, 2))}",
            f"Max Stamina: {green(fish.max_stamina)}",
        ]), 4)

    def award_xp(self):
        player = self.game_state.player
        fish = self.game_state.current_fish
        xp = max(1, round(fish.value ** 0.5))
        player.gain_fishing_xp(xp)

    def sell_fish(self):
        player = self.game_state.player
        area = self.game_state.current_area.name
        fish = self.game_state.current_fish
        value = fish.value

        if value > 0:
            play_sound(COINS)
            print_and_sleep(green(f"You received {value} coins for the {fish.name}!"), 1)
            player.coins += value
        else:
            print_and_sleep(blue(f"You released the {fish.name} back into the {area}."), 1)


    def update_log(self):
        fish = self.game_state.current_fish
        fish.catch_location = self.game_state.current_fishing_area.name
        self.game_state.player.caught_fish.append(fish)

# ================================================================================================
# ================================================================================================

class FishTurn(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self) -> GameState:
        fish = self.game_state.current_fish
        player = self.game_state.player
        fishing_area = self.game_state.current_fishing_area

        # --- did the fish spit the hook ---
        self.spit_hook(player, fish)

        # --- did player lose the fish ---
        if fish.lost:
            return EndFishBattle(self.game_state).run()

        # --- fish turn and outcome ---
        run = self.fish_runs(fish, fishing_area)
        self.fish_gains_rage(fish, run)
        self.update_fish_state(fish)
        self.apply_fish_turn_outcome()

        # --- fishing items ---
        self.stamina_items(player, fish)
        self.rage_items(player, fish)
        self.speed_items(player, fish)

        # --- check if fish got away after its turn ---
        if fish.lost:
            return EndFishBattle(self.game_state).run()

        if random.random() < 0.15:
            play_sound(FISH)

        self.adrenaline_rush(fish)
        return self.game_state

# ================================================================================================

    @staticmethod
    def adrenaline_rush(fish) -> None:
        if not fish.adrenaline_ready:
            return

        stamina_percentage = (fish.stamina / fish.max_stamina) * 100
        if stamina_percentage > 10:
            return

        name = fish.name if fish.species_known else "Unknown Fish"
        stamina_gain_pct = random.randint(10, 20)
        stamina_gain = round(fish.max_stamina * stamina_gain_pct / 100)

        fish.stamina += stamina_gain
        fish.adrenaline_ready = False

        print_and_sleep(
            yellow(f"The {name} found a second wind and gained {stamina_gain} stamina!")
        )

    @staticmethod
    def spit_hook(player, fish) -> None:
        if fish.barb_hook_active:
            barb_hook = next(
                (item for item in player.active_fishing_items if item.name == BARB_HOOK),
                None,
            )

            if barb_hook:
                barb_hook.turns -= 1

                if barb_hook.turns <= 0:
                    player.active_fishing_items.remove(barb_hook)
                    fish.barb_hook_active = False

                return

        if random.random() < fish.spit_hook_chance:
            name = fish.name if fish.species_known else "Unknown Fish"
            play_sound(WHIFF)
            play_sound(FISH)
            print_and_sleep(yellow(f"The {name} dropped the hook and swam away!"))
            fish.lost = True

# ================================================================================================

    @staticmethod
    def stamina_items(player, fish) -> None:
        item = next(
            (item for item in player.active_fishing_items if item.type == STAMINA),
            None,
        )

        if item is None:
            return

        item.turns -= 1

        if item.turns <= 0:
            player.active_fishing_items.remove(item)
            fish.stamina_multiplier = 1

    @staticmethod
    def rage_items(player, fish) -> None:
        item = next(
            (item for item in player.active_fishing_items if item.type == RAGE),
            None,
        )

        if item is None:
            return

        item.turns -= 1

        if item.turns <= 0:
            player.active_fishing_items.remove(item)
            fish.rage_multiplier = 1

    @staticmethod
    def speed_items(player, fish) -> None:
        item = next(
            (item for item in player.active_fishing_items if item.type == SPEED),
            None,
        )

        if item is None:
            return

        item.turns -= 1

        if item.turns <= 0:
            player.active_fishing_items.remove(item)
            fish.speed_multiplier = 1

# ================================================================================================

    @staticmethod
    def fish_runs(fish, fishing_area) -> int:
        stamina_ratio = fish.stamina / fish.max_stamina
        run_mult = fishing_area.run_mult

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

        # --- burst ---
        burst_chance = min(0.15, (fish.speed * fish.speed_multiplier) * 0.08)
        burst = random.random() < burst_chance

        # --- run ---
        run = random.randint(2, 5)
        run *= fish.speed
        run *= stamina_modifier
        run *= state_modifier
        run *= run_mult

        if burst:
            total_run = max(1, round(run * 2))

            if total_run > 5:
                play_sound(WHIFF)
                print_and_sleep(yellow("The fish had a burst of speed!"))
        else:
            total_run = max(1, round(run * fish.speed_multiplier))

        fish.distance += total_run

        return total_run

    @staticmethod
    def fish_gains_rage(fish, run: int) -> None:
        stamina_ratio = fish.stamina / fish.max_stamina

        # --- state ---
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

        original_rage = fish.rage

        rage_gain = random.randint(1, 3)
        rage_gain *= fish.rage_factor
        rage_gain *= state_modifier
        rage_gain *= stamina_modifier
        rage_gain *= fish.rage_multiplier

        fish.rage += round(rage_gain)
        fish.rage = min(100, fish.rage)

        rage_delta = fish.rage - original_rage
        print_fish_turn_results(run, rage_delta)

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

    def apply_fish_turn_outcome(self) -> None:
        fish = self.game_state.current_fish
        area = self.game_state.current_fishing_area
        name = fish.name if fish.species_known else "Unknown Fish"

        break_chance = min(
            0.025,
            ((fish.weight / 1000) + (fish.strength * 0.01))
            * (fish.rage / 100),
        )

        if fish.distance >= area.escape_distance:
            fish.lost = True
            print_and_sleep(red(f"The {name} gained too much distance and escaped!"), 1.5)
            return

        if fish.rage >= 100:
            fish.lost = True
            print_and_sleep(red(f"The enraged {name} broke free and escaped!"), 1.5)
            return

        if fish.rage >= 80 and random.random() < break_chance:
            fish.lost = True
            print_and_sleep(red("The fish snapped the line and escaped!"), 1.5)

# ================================================================================================
# ================================================================================================

class Pull(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self) -> GameState:
        fish = self.game_state.current_fish

        pull = self.get_pull()
        self.apply_pull(pull)
        self.apply_pull_outcome()

        if fish.caught or fish.lost:
            return EndFishBattle(self.game_state).run()

        return FishTurn(self.game_state).run()

    def get_pull(self) -> int:
        # --- variables ---
        player = self.game_state.player
        pull_mult = self.game_state.current_fishing_area.pull_mult
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
        pull *= get_rod_modifier(player)
        pull *= pull_mult
        pull = max(1, pull)

        return round(pull)

    def apply_pull(self, pull: int) -> None:
        fish = self.game_state.current_fish

        stamina_loss = pull + random.randint(1, 3)
        rage_gain = random.randint(1, 3) + pull / 2

        # --- distance ---
        original_distance = fish.distance
        fish.distance -= round(pull)
        fish.distance = max(0, fish.distance)

        # --- stamina ---
        original_stamina = fish.stamina
        fish.stamina -= round(stamina_loss * fish.stamina_multiplier)
        fish.stamina = max(0, fish.stamina)

        # --- rage ---
        original_rage = fish.rage
        rage_gain *= fish.rage_factor
        fish.rage += round(rage_gain * fish.rage_multiplier)
        fish.rage = min(100, fish.rage)
        FishTurn.update_fish_state(fish)

        print_action_results(fish, PULL, original_distance, original_stamina, original_rage)

    def apply_pull_outcome(self) -> None:
        fish = self.game_state.current_fish
        location = self.game_state.current_fishing_area.name
        name = fish.name if fish.species_known else "Unknown Fish"

        if fish.distance <= 0:
            fish.caught = True
            fish.catch_location = location
            return

        if fish.stamina <= 0:
            fish.caught = True
            fish.catch_location = location
            return

        if fish.rage >= 100:
            fish.lost = True
            print_and_sleep(red(f"The raging {name} got away!"), 1.5)

# ================================================================================================
# ================================================================================================

class Reel(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self) -> GameState:
        fish = self.game_state.current_fish
        player = self.game_state.player

        reel = self.get_reel(fish, player)
        self.apply_reel(reel, fish)
        self.apply_reel_outcome(fish)

        if fish.caught or fish.lost:
            return EndFishBattle(self.game_state).run()

        return FishTurn(self.game_state).run()

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
        reel *= get_rod_modifier(player)
        reel = max(1, reel)

        return round(reel)

    @staticmethod
    def apply_reel(reel: int, fish) -> None:
        stamina_loss = max(1, round(reel / 2)) + random.randint(0, 1)
        rage_gain = random.randint(0, 1) + reel / 3

        # --- distance ---
        original_distance = fish.distance
        fish.distance -= round(reel)
        fish.distance = max(0, fish.distance)

        # --- stamina ---
        original_stamina = fish.stamina
        fish.stamina -= round(stamina_loss * fish.stamina_multiplier)
        fish.stamina = max(0, fish.stamina)

        # --- rage ---
        original_rage = fish.rage
        rage_gain *= fish.rage_factor
        fish.rage += round(rage_gain * fish.rage_multiplier)
        fish.rage = min(100, fish.rage)
        FishTurn.update_fish_state(fish)

        print_action_results(fish, REEL, original_distance, original_stamina, original_rage)

    def apply_reel_outcome(self, fish) -> None:
        location = self.game_state.current_fishing_area.name
        name = fish.name if fish.species_known else "Unknown Fish"

        if fish.distance <= 0:
            fish.caught = True
            fish.catch_location = location
            return

        if fish.stamina <= 0:
            fish.caught = True
            fish.catch_location = location
            return

        if fish.rage >= 100:
            fish.lost = True
            print_and_sleep(red(f"The raging {name} got away!"), 1.5)

# ================================================================================================

class GiveLine(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self) -> GameState:
        fish = self.game_state.current_fish
        player = self.game_state.player

        line = self.get_give_line(fish)
        self.apply_give_line(fish, line, player)
        self.apply_give_line_outcome(fish)

        if fish.caught or fish.lost:
            return EndFishBattle(self.game_state).run()

        return self.game_state

    @staticmethod
    def get_give_line(fish) -> int:
        line = random.randint(2, 4)
        line *= round(fish.speed * fish.speed_multiplier)

        if fish.state == AGITATED:
            line += 1
        elif fish.state == SPOOKED:
            line += 2
        elif fish.state == ENRAGED:
            line += 4

        return round(line)

    @staticmethod
    def apply_give_line(fish, line: int, player) -> None:
        # --- distance ---
        original_distance = fish.distance
        fish.distance += line

        # --- stamina unaffected ---
        original_stamina = fish.stamina

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
        rage_loss += min(player.rod_lvl - 1, 3)

        fish.rage -= rage_loss
        fish.rage = max(0, fish.rage)
        FishTurn.update_fish_state(fish)

        print_action_results(fish, GIVE_LINE, original_distance, original_stamina, original_rage)

    def apply_give_line_outcome(self, fish) -> None:
        location = self.game_state.current_fishing_area.name
        name = fish.name if fish.species_known else "Unknown Fish"

        if fish.distance <= 0:
            fish.caught = True
            fish.catch_location = location
            return

        if fish.rage >= 100:
            fish.lost = True
            print_and_sleep(red(f"The raging {name} got away!"), 1.5)

# ================================================================================================

class ObserveFish(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self) -> GameState:
        fish = self.game_state.current_fish

        # --- stamina can be checked multiple times ---
        observation = self.get_observation(fish)
        self.apply_observation(fish, observation)

        return FishTurn(self.game_state).run()

    @staticmethod
    def get_observation(fish) -> str | None:
        valid = [
            observation
            for observation in possible_observations
            if observation not in fish.observed_characteristics
        ]

        if not valid:
            return None

        return random.choice(valid)

    def apply_observation(self, fish, observation: str | None) -> None:
        if observation is None:
            print_and_sleep(blue("There is nothing more to learn from observation."), 1.5)
            return

        fish.observed_characteristics.append(observation)

        if observation == SPECIES:
            color = white
            word = SPECIES
            value = fish.base_name
            fish.species_observed = True
            fish.species_known = True
        elif observation == VARIANT:
            color = purple
            word = VARIANT
            value = fish.variant if fish.variant else "None"
            fish.variant_observed = True
        elif observation == RARITY:
            color = fish.get_rarity_color()
            word = RARITY
            value = fish.rarity
            fish.rarity_observed = True
        elif observation == STRENGTH:
            color = yellow
            word = STRENGTH
            value = str(round(fish.strength, 2))
            fish.strength_observed = True
        elif observation == STAMINA:
            color = yellow
            word = STAMINA
            value = yellow(f"{fish.stamina}/{fish.max_stamina}")
        elif observation == SPEED:
            color = cyan
            word = SPEED
            value = str(round(fish.speed, 2))
            fish.speed_observed = True
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
        print_and_sleep(blue("You observe the fish to learn more..."), 1.5)
        print_and_sleep(f"{color(word)}: {value}", 1.5)

# ================================================================================================

def print_action_results(
        fish,
        action: str,
        original_distance: int,
        original_stamina: int,
        original_rage: int,
) -> None:
    distance_delta = fish.distance - original_distance
    stamina_delta = fish.stamina - original_stamina
    rage_delta = fish.rage - original_rage
    action_display = get_action_color(action)

    parts = []

    if distance_delta != 0:
        color = green if distance_delta < 0 else yellow
        parts.append(f"Distance {color(f'{distance_delta:+}')}")

    if stamina_delta != 0:
        color = green if stamina_delta < 0 else yellow
        parts.append(f"Stamina {color(f'{stamina_delta:+}')}")

    if rage_delta != 0:
        color = red if rage_delta > 0 else green
        parts.append(f"Rage {color(f'{rage_delta:+}')}")

    if parts:
        print_and_sleep(f"{action_display}: {' | '.join(parts)}", 1.5)


def get_action_color(action: str) -> str:
    if action == PULL:
        return orange(PULL)

    if action == REEL:
        return green(REEL)

    if action == GIVE_LINE:
        return purple(GIVE_LINE)

    return white(action)


def print_fish_turn_results(run: int, rage_delta: int) -> None:
    fish = blue("Fish")
    parts = []

    if run != 0:
        color = yellow if run > 0 else green
        parts.append(f"Distance {color(f'{run:+}')}")

    if rage_delta != 0:
        color = red if rage_delta > 0 else green
        parts.append(f"Rage {color(f'{rage_delta:+}')}")

    if parts:
        print_and_sleep(f"{fish}: {' | '.join(parts)}", 1.5)


def get_rod_modifier(player: Player) -> float:
    return 1 + ((player.rod_lvl - 1) * 0.10)