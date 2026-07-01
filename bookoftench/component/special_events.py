import random

from bookoftench import event_logger
from bookoftench.audio import play_music, play_sound
from bookoftench.component import functional_component, \
    LabeledSelectionComponent, ReprBinding, NoOpComponent, SelectionBinding, register_component, SwapFoundItemYN, \
    OfficerEncounter, set_special_boss, Battle
from bookoftench.data.audio import PUNCH, POSITIVE, MONSTER_ATTACK, PISTOL, BLADE, COINS, PURCHASE
from bookoftench.data.components import SPECIAL_EVENT
from bookoftench.data.enemies import OILY_DOILY, BASTA_SHERMAN, DEATH_WORM, CYCLOPS, SABERTOOTH_LIGER, \
    GIANT_MUTANT_RAT, SEWER_GATOR, LUCKY_THE_LEPRECHAUN, FAIRY_CODMOTHER, MOTHMAN, SASQUATCH, SKUNK_APE, OGRE, HODAG
from bookoftench.data.illnesses import HERPES
from bookoftench.data.items import TENCH_FILET, SWAMP, FOREST, CITY, CAVE
from bookoftench.data.perks import BEER_GOGGLES
from bookoftench.data.special_events import Special_Events, LOST_GOLD_P2
from bookoftench.model import GameState
from bookoftench.model.events import PlayerDeathEvent
from bookoftench.model.investment import load_investment, Investment
from bookoftench.model.item import load_items
from bookoftench.model.perk import load_perks, perk_is_active
from bookoftench.model.special_event import SpecialEvent, load_special_event
from bookoftench.ui import red, purple, cyan, yellow, green, blue
from bookoftench.util import print_and_sleep

# ================================================================================================

@register_component(SPECIAL_EVENT)
class DiscoverSpecial(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        game_state = self.game_state
        player = self.game_state.player
        area = game_state.current_area.name
        season = game_state.season
        time = game_state.time_of_day
        moon = game_state.moon

        # --- filter out expired special events ---
        expired_names = [i.name for i in game_state.expired_special_events]

        fresh = [
            i for i in Special_Events
            if i['name'] not in expired_names
        ]

        # --- filter by criteria ---
        expired_opps = player.expired_investment_opportunities
        filtered = [
            i for i in fresh
            if area in i['areas']
               and time in i['time']
               and (i['moon'] is None or moon in i['moon'])
               and (i['season'] is None or season in i['season']
               and i['investment'] is None or i['investment'] not in expired_opps)
        ]

        if not filtered:
            print("Filtered came up dry.")
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
        if special_event.investment:
            invest_obj = load_investment(special_event.investment)
        else:
            invest_obj = None

        if not special_event.replayable:
            game_state.expired_special_events.append(special_event)

        return SpecialEventComponent(self.game_state, special_event, invest_obj).run()

# ================================================================================================

class SpecialEventComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState, event: SpecialEvent,
                 invest_obj: Investment | None):

        self.special_event = event
        self.leave = False
        self.investment = invest_obj

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
        if self.investment:
            self.game_state.player.expired_investment_opportunities.append(self.investment.name)

        self.leave = True

    def can_exit(self) -> bool:
        return self.leave or not self.game_state.player.is_alive()

    def display_options(self) -> None:
        if self.special_event.color:
            print_and_sleep(
                self.special_event.color(self.special_event.text),
                self.special_event.sleep
            )
        else:
            print_and_sleep(
                self.special_event.text,
                self.special_event.sleep
            )

        for binding in self.binding_map.values():
            if binding.key.lower() == "r":
                print()

            print(f"[{binding.key}] : {binding.name}")

# ============================================================================================

    def _handle_selection_component(self, special_event: SpecialEvent, choice: int):
        def selection_component():
            if not special_event.method:
                return self.game_state

            method = getattr(self, special_event.method)

            if self.investment:
                if not self.can_afford_investment(choice):
                    print_and_sleep(yellow("Need more coin."), 1)
                    return self.game_state

                purchased = method(self.game_state, choice, self.investment)

                if purchased:
                    self.leave = True

                return self.game_state

            method(self.game_state, choice)
            self.leave = True

            return self.game_state

        return functional_component()(selection_component)

# ============================================================================================

    def can_afford_investment(self, choice) -> bool:
        player = self.game_state.player

        if choice == 1:
            investment = 10
        elif choice == 2:
            investment = 25
        elif choice == 3:
            investment = 50
        else:
            investment = 100

        if player.coins >= investment:
            return True

        return False

# ============================================================================================

    @staticmethod
    def greedy_bastard(game_state: GameState, choice: int):
        player = game_state.player
        woman_coins = random.randint(1, 50)
        request = choice * 10

        print_and_sleep(purple(f"...\n"), 1.5)

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
            special_event_death_check(player)

# ================================================================================================

    @staticmethod
    def herpes_kiss(game_state: GameState, choice: int):
        player = game_state.player

        if player.illness:
            print_and_sleep(purple("Sensuous Being: Wait... are you sick?"), 1.5)
            print_and_sleep(purple(f"Do you have... {player.illness.name}?"), 1.5)
            print_and_sleep(purple("GROSS! I can't believe I almost let you kiss me."), 1.5)
            return game_state

        if choice == 1:
            kisses = 1
        elif choice == 2:
            kisses = 3
        elif choice == 3:
            kisses = 5
        else:
            kisses = 10

        for i in range(kisses):
            if i == 0:
                print_and_sleep("You kiss the sensuous being...", 1.5)
            else:
                print_and_sleep("You kiss the sensuous being again...", 1.5)

            player.gain_or_lose_luck(0.1)
            player.gain_coins(8)

            if random.random() < 0.10:
                print_and_sleep(yellow("Your lips feel tingly all of a sudden..."), 1.5)
                print_and_sleep(yellow("The Sensuous Being covers its mouth and giggles..."), 1.5)
                print_and_sleep(yellow("The Sensuous Being gave you Herpes!"), 1.5)
                player.acquire_illness(HERPES)
                player.gain_or_lose_luck(-0.1)
                break

        print_and_sleep(purple("You kiss like a fish... hehehe."), 1.5)

        return game_state

# ================================================================================================

    @staticmethod
    def lost_gold_p1(game_state: GameState, choice: int):
        gold_location = random.choice([CAVE, CITY, FOREST, SWAMP])

        if choice == 1:
            choice = CAVE
        elif choice == 2:
            choice = CITY
        elif choice == 3:
            choice = FOREST
        else:
            choice = SWAMP

        print_and_sleep(yellow(f"You tell the pirate that he will find his gold in the {choice}..."), 1.5)

        if choice == gold_location:  # Remove part two if player is correct
            lost_gold_p2 = load_special_event(LOST_GOLD_P2)
            game_state.expired_special_events.append(lost_gold_p2)

    @staticmethod
    def lost_gold_p2(game_state: GameState, choice: int):
        player = game_state.player
        if choice == 1:  # Give Coin
            if player.coins >= 50:  # Give 50 Coin
                player.coins -= 50
                play_sound(COINS)
                print_and_sleep(yellow("You gave 50 of coin to the pirate.\n"), 1.5)
                return

            coins = player.coins
            player.coins -= player.coins
            play_sound(COINS)
            print_and_sleep(yellow(f"You forfeited {coins} of coin to the pirate.\n"), 1.5)

            # Make Up Diff w/ HP
            play_sound(BLADE)
            hp = player.hp
            player.hp -= min(hp, 50 - coins)
            print_and_sleep(red(f"The Pirate slashed you with his cutlass for {hp - player.hp} damage!\n"), 1.5)
            print_and_sleep(red(f"Pirate: Argh, that's for comin' up dry on me, matey.\n"), 1.5)

        elif choice == 2:  # Give Tench Filet
            if TENCH_FILET in player.items:
                del player.items[TENCH_FILET]
                print_and_sleep(yellow(f"You forfeit your Tench Filet to the Pirate.\n"), 1.5)
                print_and_sleep(blue(f"Pirate: Aye, we're square, matey.\n"), 1.5)
            else:
                play_sound(BLADE)
                hp = player.hp
                player.hp -= min(hp, 50)
                damage = hp - player.hp
                print_and_sleep(red(f"The Pirate slashed you with his cutlass for {damage} damage!"), 1.5)
                print_and_sleep(red(f"Pirate: Argh, that's for comin' up dry on me, matey.\n"), 1.5)

        else:  # Beg for Mercy
            if random.random() < 0.25:
                print_and_sleep(blue(f"Pirate: Argh, yer' off the hook this time, matey."
                                     f"Me wench tells me I need to be kinder to folks.\n"), 1.5)
            else:
                hp = player.hp
                damage = random.randint(25, 50)
                player.hp -= min(hp, damage)
                actual_damage = hp - player.hp
                print_and_sleep(red(f"The Pirate slashed you with his cutlass for {actual_damage} damage!"), 1.5)
                print_and_sleep(red(f"Pirate: Argh, that's for comin' up dry on me, matey.\n"), 1.5)

        special_event_death_check(player)

# ================================================================================================

    @staticmethod
    def probing(game_state: GameState, choice: int):
        player = game_state.player

        if choice == 1:  # Accept Probe
            if random.random() < 0.5 + (player.luck * 0.1):
                print_and_sleep(green("The aliens went easy on you.\n"), 1.5)
                old_hp = player.hp
                damage = random.randint(5, 10)
                player.hp -= min(old_hp, damage)
                print_and_sleep(red(f"You lost {old_hp - player.hp} HP."), 1.5)
            else:
                print_and_sleep(yellow("The aliens didn't hold back...\n"), 1.5)
                old_hp = player.hp
                damage = random.randint(5, 10)
                player.hp -= min(old_hp, damage)
                print_and_sleep(red(f"You lost {old_hp - player.hp} HP."), 1.5)

        elif choice == 2:  # Attempt to Probe the Aliens
            if random.random() < 0.5 * player.strength:
                print_and_sleep(green("You probed the aliens!"), 1.5)
                valid = [i for i in load_perks() if not i.active]
                if valid:
                    print_and_sleep(green("They gave you a perk to thank you for the pleasure."), 1.5)
                    perk = random.choice(valid)
                    player.add_perk(perk)
                else:
                    print_and_sleep(green("They gave you some coin to thank you for the pleasure."), 1.5)
                    player.gain_coins(25)
            else:
                print_and_sleep(yellow("You were unable to probe the aliens...\n"), 1.5)
                print_and_sleep(yellow("They probed you extra hard as punishment.\n"), 1.5)
                old_hp = player.hp
                damage = random.randint(5, 10)
                player.hp -= min(old_hp, damage)
                print_and_sleep(red(f"You lost {old_hp - player.hp} HP."), 1.5)

        elif choice == 3:  # Try to Escape
            if random.random() < 0.5 + (player.luck * 0.1):
                old_hp = player.hp
                damage = random.randint(5, 10)

                print_and_sleep(green("You were able to find the exit and jump from the ship!"), 1.5)
                play_sound(PUNCH)

                player.hp -= min(old_hp, damage)
                actual_damage = old_hp - player.hp

                print_and_sleep(red(f"You lost {actual_damage} HP upon landing."), 1.5)
            else:
                print_and_sleep(green("You were unable to evade the aliens..."), 1.5)
                print_and_sleep(red("They probed you extra hard for trying to escape.\n"), 1.5)
                old_hp = player.hp
                damage = random.randint(5, 10)
                player.hp -= min(old_hp, damage)
                print_and_sleep(red(f"You lost {old_hp - player.hp} HP."), 1.5)

        special_event_death_check(player)

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
                    special_event_death_check(player)
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

        print_and_sleep(purple(f"...\n"), 1.5)

        if offer >= woman_desired_coins:
            play_sound(COINS)
            print_and_sleep(purple(f"You're not a stingy bastard. Good for you.\n"), 1.5)

            overpaid = offer - woman_desired_coins
            player.coins -= overpaid

            if overpaid > 0:
                print_and_sleep(yellow(f"You handed over {overpaid} extra coins."), 1.5)
                player.gain_xp_other(overpaid)

            player.gain_or_lose_luck(0.1)

        else:
            damage = min(woman_desired_coins - offer, player.hp)
            player.hp -= damage
            play_sound(PUNCH)
            print_and_sleep(red(f"The woman slapped you for {damage} damage!"), 1)
            print_and_sleep(purple(f"That's for being a stingy bastard!\n"), 2)
            player.gain_or_lose_luck(-0.1)
            special_event_death_check(player)

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
            player.gain_or_lose_luck(0.1)
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
            print_and_sleep(red(f"You took {damage} damage."), 1.5)
            player.gain_or_lose_luck(-0.1)

            special_event_death_check(player)

        # --- dry ---
        else:
            print_and_sleep(yellow("Your hole was dry."), 1)

# ================================================================================================

    @staticmethod
    def triple_tench_dare(game_state: GameState, choice: int):
        if perk_is_active(BEER_GOGGLES):
            print_and_sleep(yellow("Nice try, cheater. I know Beer Goggles when I see 'em'."), 1)
            return

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

        print_and_sleep(
            yellow(f"You have been blinded by the Sun. Accuracy down {round(player.blind_effect * 100)}% for "
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

                special_event_death_check(player)

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

    @staticmethod
    def oily_doily_intro(game_state: GameState, choice: int):
        player = game_state.player
        game_state.current_area.special_bosses.append(OILY_DOILY)

        if choice == 1:
            print_and_sleep(red(f"Oily floats you into his tower..."), 1.5)
            set_special_boss(game_state, OILY_DOILY)
            Battle(game_state).run()
        else:
            if random.random() < 0.5:
                print_and_sleep(yellow(f"You manage to escape, for now..."), 1.5)
                player.gain_or_lose_luck(0.25)
            else:
                print_and_sleep(red(f"You turn and run, but oily floats much faster..."), 1.5)
                player.gain_or_lose_luck(-0.25)
                set_special_boss(game_state, OILY_DOILY)
                Battle(game_state).run()

# ================================================================================================

    @staticmethod
    def basta_intro(game_state: GameState, choice: int):
        player = game_state.player
        game_state.current_area.special_bosses.append(BASTA_SHERMAN)

        if choice == 1:
            if player.coins >= 50:
                player.coins -= 50
                play_sound(COINS)
                print_and_sleep(yellow("You handed over 50 coins."), 1.5)
                print_and_sleep(green(f"Basta Sherman: Smooth move, boy. You're free to live, for now."), 1.5)
            else:
                print_and_sleep(yellow(f"Basta Sherman: Oh, you're dry? The Mayor won't miss you anyway."), 1.5)
                set_special_boss(game_state, BASTA_SHERMAN)
                Battle(game_state).run()
        else:
            if random.random() < 0.5:
                print_and_sleep(yellow(f"You manage to escape, for now..."), 1.5)
                player.gain_or_lose_luck(0.25)
            else:
                print_and_sleep(yellow(f"You try to run, but Basta is much too fast..."), 1.5)
                player.gain_or_lose_luck(-0.25)
                set_special_boss(game_state, BASTA_SHERMAN)
                Battle(game_state).run()

# ================================================================================================

    @staticmethod
    def death_worm_intro(game_state: GameState, choice: int):
        if choice:
            game_state.current_area.special_bosses.append(DEATH_WORM)
            set_special_boss(game_state, DEATH_WORM)
            Battle(game_state).run()

# ================================================================================================

    @staticmethod
    def cyclops_intro(game_state: GameState, choice: int):
        player = game_state.player
        game_state.current_area.special_bosses.append(CYCLOPS)

        if choice == 1:
            set_special_boss(game_state, CYCLOPS)
            Battle(game_state).run()
        else:
            if random.random() < 0.5:
                print_and_sleep(yellow(f"You throw a rock and hit it directly in its pupil..."), 1.5)
                print_and_sleep(yellow(f"It flinches just long enough for you to escape."), 1.5)
                print_and_sleep(yellow(f"You have a feeling that it is not done with you..."), 1.5)
                player.gain_or_lose_luck(0.25)
            else:
                print_and_sleep(yellow(f"You throw a rock at its eye but its just a bit outside..."), 1.5)
                player.gain_or_lose_luck(-0.25)
                set_special_boss(game_state, CYCLOPS)
                Battle(game_state).run()

# ================================================================================================

    @staticmethod
    def sabertooth_liger_intro(game_state: GameState, choice: int):
        if choice:
            game_state.current_area.special_bosses.append(SABERTOOTH_LIGER)
            set_special_boss(game_state, SABERTOOTH_LIGER)
            Battle(game_state).run()

# ================================================================================================

    @staticmethod
    def giant_mutant_rat_intro(game_state: GameState, choice: int):
        if choice:
            game_state.current_area.special_bosses.append(GIANT_MUTANT_RAT)
            set_special_boss(game_state, GIANT_MUTANT_RAT)
            Battle(game_state).run()

# ================================================================================================

    @staticmethod
    def sewer_gator_intro(game_state: GameState, choice: int):
        if choice:
            game_state.current_area.special_bosses.append(SEWER_GATOR)
            set_special_boss(game_state, SEWER_GATOR)
            Battle(game_state).run()

# ================================================================================================

    @staticmethod
    def lucky_the_leprechaun_intro(game_state: GameState, choice: int):
        if choice:
            game_state.current_area.special_bosses.append(LUCKY_THE_LEPRECHAUN)
            set_special_boss(game_state, LUCKY_THE_LEPRECHAUN)
            Battle(game_state).run()

# ================================================================================================

    @staticmethod
    def fairy_codmother_intro(game_state: GameState, choice: int):
        if choice:
            game_state.current_area.special_bosses.append(FAIRY_CODMOTHER)
            set_special_boss(game_state, FAIRY_CODMOTHER)
            Battle(game_state).run()

# ================================================================================================

    @staticmethod
    def mothman_intro(game_state: GameState, choice: int):
        if choice:
            game_state.current_area.special_bosses.append(MOTHMAN)
            set_special_boss(game_state, MOTHMAN)
            Battle(game_state).run()

# ================================================================================================

    @staticmethod
    def sasquatch_intro(game_state: GameState, choice: int):
        if choice:
            game_state.current_area.special_bosses.append(SASQUATCH)
            set_special_boss(game_state, SASQUATCH)
            Battle(game_state).run()

# ================================================================================================

    @staticmethod
    def skunk_ape_intro(game_state: GameState, choice: int):
        if choice:
            game_state.current_area.special_bosses.append(SKUNK_APE)
            set_special_boss(game_state, SKUNK_APE)
            Battle(game_state).run()

# ================================================================================================

    @staticmethod
    def ogre_intro(game_state: GameState, choice: int):
         if choice:
            game_state.current_area.special_bosses.append(OGRE)
            set_special_boss(game_state, OGRE)
            Battle(game_state).run()

# ================================================================================================

    @staticmethod
    def hodag_intro(game_state: GameState, choice: int):
        if choice:
            game_state.current_area.special_bosses.append(HODAG)
            set_special_boss(game_state, HODAG)
            Battle(game_state).run()

# ================================================================================================

    @staticmethod
    def make_investment(game_state: GameState, choice: int, invest_obj: Investment) -> bool:
        player = game_state.player
        buy_in = invest_obj.buy_ins[choice - 1]

        player.coins -= buy_in
        play_sound(PURCHASE)

        invest_obj.maturity_lvl = player.lvl + invest_obj.levels_to_maturity
        invest_obj.value = buy_in
        invest_obj.active = True

        player.investments.append(invest_obj)
        player.expired_investment_opportunities.append(invest_obj.name)

        print_and_sleep(green(f"You invested {buy_in} of coin in {invest_obj.name}."), 1.5)
        print_and_sleep(green(f"It should mature around level {invest_obj.maturity_lvl}."), 1.5)

        return True

# ================================================================================================

def special_event_death_check(player):
    if player.hp <= 0:
        player.hp = 0
        player.lives -= 1
        event_logger.log_event(PlayerDeathEvent(player.lives))

# ================================================================================================
