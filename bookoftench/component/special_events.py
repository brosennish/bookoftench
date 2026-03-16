import random

from bookoftench import event_logger
from bookoftench.component import RandomChoiceComponent, register_component, ProbabilityBinding, \
    get_registered_component, functional_component, SwapFoundItemYN
from bookoftench.data.components import DISCOVER_SPECIAL, THREE_HOLES, TRIPLE_TENCH_DARE
from bookoftench.model import GameState
from bookoftench.model.events import PlayerDeathEvent
from bookoftench.model.item import load_items
from bookoftench.ui import yellow, dim, purple, red, cyan
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
    def _three_holes(game_state: GameState):
        player = game_state.player
        holes = ["good", "bad", "dry"]
        random.shuffle(holes)
        hole_1 = holes[0]
        hole_2 = holes[1]
        hole_3 = holes[2]

        print_and_sleep(purple("""You come upon three holes in the ground.
They are far too deep, and too dark, to see what's inside.
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
    def _three_holes(game_state: GameState):
        player = game_state.player

        print_and_sleep(purple("""A boy approaches you, dad's wallet in hand.
He triple-tench-dares you to stare at the sun.
He offers to pay 5 of coin per second.
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