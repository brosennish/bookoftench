import random

from bookoftench import event_logger
from bookoftench.component import RandomChoiceComponent, register_component, ProbabilityBinding, \
    get_registered_component, functional_component
from bookoftench.data import Items
from bookoftench.data.components import DISCOVER_SPECIAL, THREE_HOLES
from bookoftench.model import GameState
from bookoftench.model.events import PlayerDeathEvent
from bookoftench.ui import yellow, dim, purple, red
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
        They are far too deep, and too dark, to see what they are hiding.
        A ghastly man whispers to you that you may only reach into one of the holes.
        Choose wisely."""), 2)

        while True:
            choice = input("[1] Hole 1\n[2] Hole 2\n[3] Hole 3\n\nPlease enter a selection (r to return)\n> ").strip().lower()
            if choice in ["1", "2", "3"]:
                break
            elif choice == "r":
                print_and_sleep(purple("You decide against your better judgement."), 1)
                return
            else:
                print_and_sleep(yellow("Invalid choice."), 1)
                continue


        if choice == 1:
            choice = hole_1
        elif choice == 2:
            choice = hole_2
        elif choice == 3:
            choice = hole_3

        if choice == "good":
            item = random.choice([i for i in Items if game_state.current_area in i.areas])
            player.add_item(item)
        elif choice == "bad":
            original = player.hp
            damage = min(random.randint(1, 15), original)
            player.hp -= damage
            print_and_sleep(red(f"You were ravaged by an unnatural creature causing {damage} damage."), 1)
            if player.hp == 0:
                player.lives -= 1
                event_logger.log_event(PlayerDeathEvent(player.lives))

        else:
            print_and_sleep(yellow(dim("You came up dry.")), 1)


