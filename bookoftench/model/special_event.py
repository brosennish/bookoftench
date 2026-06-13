import random
from dataclasses import dataclass
from typing import Callable, List

from bookoftench import event_logger
from bookoftench.audio import play_sound
from bookoftench.component import SwapFoundItemYN, OfficerEncounter
from bookoftench.data.audio import MONSTER_ATTACK, POSITIVE, PUNCH, PISTOL
from bookoftench.data.special_events import Special_Events
from bookoftench.model import GameState
from bookoftench.model.events import PlayerDeathEvent
from bookoftench.model.item import load_items
from bookoftench.ui import green, red, yellow, cyan, purple
from bookoftench.util import print_and_sleep

# ================================================================================================

@dataclass
class SpecialEvent:
    name: str
    color: Callable[[str], str]
    sleep: int
    theme: str
    areas: list[str]
    time: list[str]
    moon: list[str] | None
    season: list[str] | None
    text: str
    choices: list[str]
    optional: bool
    method: str

# ================================================================================================

    @staticmethod
    def friendly_aliens(game_state: GameState, choice: int):
        player = game_state.player

        if choice == 1:
            player.strength += 0.03
            print_and_sleep(green("The aliens increased your strength!"), 1.5)
        elif choice == 2:
            player.acc += 0.03
            print_and_sleep(green("The aliens increased your accuracy!"), 1.5)
        elif choice == 3:
            player.luck += 2
            if player.luck > 10:
                player.luck = 10
            print_and_sleep(green("The aliens increased your luck!"), 1.5)

# ================================================================================================

    @staticmethod
    def greedy_bastard(game_state: GameState, choice: int):
        player = game_state.player
        woman_coins = random.randint(1, 50)
        request = choice * 10

        if request <= woman_coins:
            print_and_sleep(purple(f"You're not a greedy bastard. Good for you.\n"), 2)
            player.gain_coins(request)
            if woman_coins > request:
                player.gain_xp_other(woman_coins - request)
            player.gain_or_lose_luck(0.1)
        else:
            damage = min(request - woman_coins, player.hp)
            player.hp -= damage
            play_sound(PUNCH)
            print_and_sleep(red(f"The woman slapped you for {damage} damage!"), 1)
            print_and_sleep(purple(f"That's for being a greedy bastard!\n"), 2)
            player.gain_or_lose_luck(-0.1)
            if player.hp == 0:
                player.lives -= 1
                event_logger.log_event(PlayerDeathEvent(player.lives))

# ================================================================================================

    @staticmethod
    def shebokken_roulette(game_state: GameState, choice: int):
        print_and_sleep(purple("You have the honors, partner."), 1.5)

        player = game_state.player
        wager = choice * 10

        chamber = [0, 0, 0, 0, 0, 1]
        random.shuffle(chamber)

        chamber_index = 0
        shooter = player
        while True:
            if chamber[chamber_index] == 1:
                if shooter == player:
                    play_sound(PISTOL)
                    print_and_sleep(cyan(f"You shot the man and collected {wager} coins!"), 3)
                    player.gain_coins(wager)
                    player.gain_xp_other(min(wager, 10))
                    player.gain_or_lose_luck(0.1)
                    return
                else:
                    damage = random.randint(1, min(wager, 50))
                    actual_damage = min(damage, player.hp)
                    player.hp -= actual_damage
                    play_sound(PISTOL)
                    print_and_sleep(red(f"The man shot you for {actual_damage} damage!"), 2)
                    print_and_sleep(yellow(f"You lost your wager of {wager} coins."), 2)
                    player.coins -= wager
                    player.gain_xp_other(damage)
                    player.gain_or_lose_luck(-0.1)
                    if player.hp == 0:
                        player.lives -= 1
                        event_logger.log_event(PlayerDeathEvent(player.lives))
                    return
            else:
                if shooter == player:
                    print_and_sleep(yellow(f"You shot but the chamber was empty."), 2)
                else:
                    print_and_sleep(yellow(f"The man shot but the chamber was empty."), 2)

            chamber_index += 1
            if shooter == player:
                shooter = "man"
            elif shooter == "man":
                shooter = player

# ================================================================================================

    @staticmethod
    def stingy_bastard(game_state: GameState, choice: int):
        player = game_state.player
        woman_desired_coins = random.randint(1, 50)
        offer = choice * 10

        if offer >= woman_desired_coins:
            print_and_sleep(purple(f"You're not a stingy bastard. Good for you.\n"), 2)
            player.coins -= offer - woman_desired_coins
            if offer > woman_desired_coins:
                player.gain_xp_other(offer - woman_desired_coins)
            player.gain_or_lose_luck(0.05)
        else:
            damage = min(offer - woman_desired_coins, player.hp)
            player.hp -= damage
            play_sound(PUNCH)
            print_and_sleep(red(f"The woman slapped you for {damage} damage!"), 1)
            print_and_sleep(purple(f"That's for being a stingy bastard!\n"), 2)
            player.gain_or_lose_luck(-0.05)
            if player.hp == 0:
                player.lives -= 1
                event_logger.log_event(PlayerDeathEvent(player.lives))

# ================================================================================================

    @staticmethod
    def three_holes(game_state: GameState, choice: int):
        player = game_state.player

        # --- establish holes ---
        holes = [1, 2, 3]
        random.shuffle(holes)
        good = holes[0]
        bad = holes[1]

        # --- item ---
        if choice == good:
            available_items = [
                i for i in load_items()
                if i.areas is not None and game_state.current_area.name in i.areas
            ]

            item = random.choice(available_items)
            play_sound(POSITIVE)
            player.gain_or_lose_luck(0.05)
            print_and_sleep(cyan(f"You found {'an' if item.name[0].lower() in 'aeiou' else 'a'} {item.name}!"), 1)

            if player.add_item(item):
                print_and_sleep(cyan(f"{item.name} added to sack."), 1)
            else:
                SwapFoundItemYN(game_state).run()

        # --- monster ---
        elif choice == bad:
            original = player.hp
            damage = min(random.randint(1, min(player.lvl * 10, 50)), original)
            player.hp -= damage
            play_sound(MONSTER_ATTACK)
            print_and_sleep(red(f"You were ravaged by an unseen creature."), 2)
            player.gain_or_lose_luck(-0.05)

            if player.hp == 0:
                player.lives -= 1
                event_logger.log_event(PlayerDeathEvent(player.lives))

        # --- dry ---
        else:
            print_and_sleep(yellow("Your hole was dry."), 1)

# ================================================================================================

    @staticmethod
    def triple_tench_dare(game_state: GameState, choice: int):
        player = game_state.player
        seconds = choice * 5

        print_and_sleep(yellow(f"You stare at the sun for {seconds} seconds..."))

        for i in range(seconds):
            print_and_sleep(yellow("..."), 1)

        sun_effect = random.uniform(0.1, 1)
        luck = 1 - sun_effect
        if player.blind:
            player.blind_turns += seconds
            player.blind_effect = sun_effect if sun_effect > player.blind_effect else player.blind_effect
        else:
            player.blind = True
            player.blind_turns = seconds
            player.blind_effect = sun_effect

        print_and_sleep(yellow(f"You have been blinded by the Sun. Accuracy down {round(player.blind_effect * 100)}% for "
        f"{player.blind_turns} turns"), 3)

        payment = seconds * 5
        player.gain_or_lose_luck(luck)
        player.gain_coins(payment)

# ================================================================================================

    @staticmethod
    def zonked(game_state: GameState, choice: int):
        player = game_state.player

        amount = random.randint(1, 25)
        if choice == 1:
            if random.random() < 0.5:
                play_sound(PUNCH)
                print_and_sleep(red(f"You startled the man and he punched you for {amount} damage!"), 3)
                original = player.hp
                player.hp -= min(amount, original)
                player.gain_or_lose_luck(-0.1)
                if player.hp == 0:
                    player.lives -= 1
                    event_logger.log_event(PlayerDeathEvent(player.lives))
            else:
                print_and_sleep(purple(f"""Thanks for waking me up, man.
            I have an appointment today and would've totally bricked.
            I'm scheduled to be buried alive at 6... or was it 8?"""), 3)
                print_and_sleep(green(f"He pays you {amount} of coin and immediately zonks back out."), 3)
                player.gain_coins(amount)
                player.gain_or_lose_luck(0.1)
        else:
            print_and_sleep(purple(f"You bury the man alive..."), 3)
            player.gain_xp_other(amount)
            if random.random() < 0.25:
                player.gain_or_lose_luck(-0.1)
                OfficerEncounter(game_state).run()

# ================================================================================================


# ================================================================================================

def load_special_event(name: str) -> SpecialEvent:
    matches = load_special_events([name])
    if len(matches) == 0:
        raise ValueError(f"Could not find special event data for {name}")
    return matches[0]

def load_special_events(restriction: List[str] = None) -> List[SpecialEvent]:
    return [SpecialEvent(**d) for d in Special_Events if restriction is None or d['name'] in restriction]

# ================================================================================================