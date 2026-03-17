import random

from bookoftench import event_logger
from bookoftench.audio import play_sound, play_music
from bookoftench.component import RandomChoiceComponent, register_component, ProbabilityBinding, \
    get_registered_component, functional_component, SwapFoundItemYN
from bookoftench.data.audio import PISTOL, ROULETTE_THEME
from bookoftench.data.components import DISCOVER_SPECIAL, THREE_HOLES, TRIPLE_TENCH_DARE, SHEBOKKEN_ROULETTE
from bookoftench.model import GameState
from bookoftench.model.events import PlayerDeathEvent
from bookoftench.model.item import load_items
from bookoftench.ui import yellow, dim, purple, red, cyan, green
from bookoftench.util import print_and_sleep


@register_component(DISCOVER_SPECIAL)
class DiscoverSpecial(RandomChoiceComponent):
    def __init__(self, game_state: GameState):
        evp = game_state.current_area.event_probabilities
        super().__init__(game_state, bindings=[ProbabilityBinding(prob, get_registered_component(name))
                                               for name, prob in evp.items()])

    @staticmethod
    @register_component(SHEBOKKEN_ROULETTE)
    @functional_component(state_dependent=True)
    def _shebokken_roulette(game_state: GameState):
        play_music(ROULETTE_THEME)
        player = game_state.player

        print_and_sleep(purple("A man approaches with a revolver...\n"), 2)

        print_and_sleep(purple("""He looks you up and down, and then again.
May I interest you in a good, old-fashioned game of Shebokken Roulette?\n\n"""), 3)

        wager = 0
        while True:
            choice = input(
                "[#] Yes (enter wager)\n[N] Not this time\n\nPlease enter a selection (r to return)\n> ").strip().lower()
            if choice.isdigit():
                if int(choice) > 100 or int(choice) < 1:
                    print_and_sleep(yellow("Please enter a value between 1-100.\n"), 1)
                    continue
                if int(choice) > player.coins:
                    print_and_sleep(yellow(f"You only have {player.coins} coins.\n"), 1)
                    continue
                else:
                    wager = int(choice)
                    print_and_sleep(green(f"You wagered {wager} coins.\n"), 1)
                    break
            elif choice == "n":
                print_and_sleep(purple("You decide against your better judgement."), 1)
                return None
            else:
                print_and_sleep(yellow("Invalid choice.\n"), 1)
                continue

        while True:
            pick = input(
                "[H] Heads\n[T] Tails\n\nPlease enter a selection (r to return)\n> ").strip().lower()
            if pick == "h":
                print_and_sleep(purple("You chose heads."), 2)
                break
            elif pick == "t":
                print_and_sleep(purple("You chose tails."), 2)
                break
            else:
                print_and_sleep(yellow("Invalid choice.\n"), 1)
                continue

        result = random.choice(["h", "t"])
        if result == pick:
            player_1 = player
            player_2 = "The man"
            print_and_sleep(purple("You go first!"), 1)
        else:
            player_1 = "The man"
            player_2 = player
            print_and_sleep(purple("You go second..."), 1)

        chamber = [0, 0, 0, 0, 0, 1]
        random.shuffle(chamber)

        chamber_index = 0
        shooter = player_1
        while True:
            if chamber[chamber_index] == 1:
                if shooter == player:
                    play_sound(PISTOL)
                    print_and_sleep(cyan(f"You shot the man and collected {wager} coins!"), 2)
                    player.gain_coins(wager)
                    player.gain_xp_other(min(wager, 20))
                    return None
                else:
                    damage = random.randint(5, 50)
                    player.hp -= min(damage, player.hp)
                    play_sound(PISTOL)
                    print_and_sleep(red(f"The man shot you for {damage} damage!"), 2)
                    print_and_sleep(yellow(f"You lost your wager of {wager} coins."), 2)
                    player.coins -= wager
                    if player.hp == 0:
                        player.lives -= 1
                        event_logger.log_event(PlayerDeathEvent(player.lives))
                    return None
            else:
                if shooter == player:
                    print_and_sleep(purple(f"You shot but the chamber was empty."), 2)
                else:
                    print_and_sleep(purple(f"The man shot but the chamber was empty."), 2)

            chamber_index += 1
            if shooter == player_2:
                shooter = player_1
            elif shooter == player_1:
                shooter = player_2

    @staticmethod
    @register_component(THREE_HOLES)
    @functional_component(state_dependent=True)
    def _three_holes(game_state: GameState):
        player = game_state.player
        holes = ["good", "bad", "dry"]
        random.shuffle(holes)
        hole_1 = holes[0]
        hole_2 = holes[1]
        hole_3 = holes[2]

        print_and_sleep(purple("You come upon three holes in the ground...\n"), 2)

        print_and_sleep(purple("""They are far too deep, and too dark, to see what's inside.
A ghastly man whispers that you may only reach into one of the holes.
Choose wisely.\n\n"""), 3)

        while True:
            choice = input("[1] Hole 1\n[2] Hole 2\n[3] Hole 3\n\nPlease enter a selection (r to return)\n> ").strip().lower()
            if choice in ["1", "2", "3"]:
                break
            elif choice == "r":
                print_and_sleep(purple("You decide against your better judgement."), 1)
                return None
            else:
                print_and_sleep(yellow("Invalid choice.\n"), 1)
                continue

        if choice == "1":
            choice = hole_1
        elif choice == "2":
            choice = hole_2
        elif choice == "3":
            choice = hole_3

        if choice == "good":
            item = random.choice([i for i in load_items() if game_state.current_area.name in i.areas])
            print_and_sleep(cyan(f"You found {item.name}!"), 1)

            if player.add_item(item):
                print_and_sleep(cyan(f"{item.name} added to sack."), 1)
                return None
            else:
                return SwapFoundItemYN(game_state).run()

        elif choice == "bad":
            original = player.hp
            damage = min(random.randint(1, 20), original)
            player.hp -= damage
            print_and_sleep(red(f"You were ravaged by an unseen creature and lost {damage} hp."), 2)
            if player.hp == 0:
                player.lives -= 1
                event_logger.log_event(PlayerDeathEvent(player.lives))
            return None

        else:
            print_and_sleep(dim("You came up dry."), 1)
            return None


    @staticmethod
    @register_component(TRIPLE_TENCH_DARE)
    @functional_component(state_dependent=True)
    def _triple_tench_dare(game_state: GameState):
        player = game_state.player

        print_and_sleep(purple("A boy approaches you, dad's wallet in hand...\n"), 2)

        print_and_sleep(purple("""He triple-tench-dares you to stare at the sun.
For every second, he will give you 5 of coin.
What do you say?\n\n"""), 3)

        seconds = 0
        while True:
            choice = input(
                "[#] Yes (enter # of seconds)\n[M] Maybe next time\n\nPlease enter a selection (r to return)\n> ").strip().lower()
            if choice.isdigit():
               if int(choice) > 100 or int(choice) < 1:
                   print_and_sleep(yellow("Please enter a value between 1-100.\n"), 1)
               else:
                   seconds = int(choice)
                   break
            elif choice == "m":
                print_and_sleep(purple("You decide against your better judgement."), 1)
                return None
            else:
                print_and_sleep(yellow("Invalid choice.\n"), 1)
                continue

        print_and_sleep(yellow("..."), seconds)

        sun_effect = random.uniform(0.25, 0.75)
        if player.blind:
            player.blind_turns += seconds
            player.blind_effect = sun_effect if sun_effect > player.blind_effect else player.blind_effect
        else:
            player.blind = True
            player.blind_turns = seconds
            player.blind_effect = sun_effect


        print_and_sleep(
            purple(
                f"You have been blinded by the Sun. Accuracy down {round(player.blind_effect * 100)}% for "
                f"{player.blind_turns} turns"), 1)

        payment = seconds * 5
        player.gain_coins(payment)
        return None