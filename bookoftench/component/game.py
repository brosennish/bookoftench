import sys

from bookoftench.audio import play_sound, stop_all_sounds, play_music
from bookoftench.component import BuildTypeSelection
from bookoftench.component.base import GatekeepingComponent, TextDisplayingComponent, BinarySelectionComponent, \
    LinearComponent, Component
from bookoftench.component.menu import ActionMenu
from bookoftench.component.menu import StartMenu
from bookoftench.component.registry import register_component
from bookoftench.data.audio import DEVIL_THUNDER, GREAT_JOB, INTRO_THEME, VICTORY_THEME, START_THEME
from bookoftench.data.components import QUIT_GAME, NEW_GAME, BUILD_SELECTION
from bookoftench.model import GameState
from bookoftench.model.util import display_game_stats
from bookoftench.ui import red, green
from bookoftench.util import print_and_sleep, safe_input

# ================================================================================================

class InitGame(GatekeepingComponent):
    def __init__(self, _: GameState = None):
        super().__init__(GameState(),
                         decision_function=self._decision_function,
                         accept_component=VictoryOrDeathHandler,
                         deny_component=StartMenu)

    def _decision_function(self):
        return self.game_state.victory or not self.game_state.player.is_alive()

    def run(self) -> GameState:
        while True:
            self.game_state = super().run()


class VictoryOrDeathHandler(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         decision_function=self._decision_function,
                         accept_component=VictoryHandler,
                         deny_component=DeathHandler)

    def _decision_function(self):
        if self.game_state.victory:
            return True
        if not self.game_state.player.is_alive():
            return False
        raise Exception(f"{VictoryOrDeathHandler} invoked but neither victory nor death occurred.")


class VictoryHandler(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         display_callback=self._display,
                         next_component=ViewStatsDecision)

    @staticmethod
    def _display(_: GameState):
        print_and_sleep(f"You defeated the evil Denny Biltmore and rescued Chula!\n", 1)
        play_sound(GREAT_JOB)
        print_and_sleep(green("You win!"), 10)
        play_music(VICTORY_THEME)


class DeathHandler(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         decision_function=lambda: game_state.player.lives > 0,
                         accept_component=ContinueGame,
                         deny_component=GameOver)


@register_component(NEW_GAME)
class NewGame(LinearComponent):
    def __init__(self, _: GameState):
        super().__init__(GameState(), BuildSelect)

    def execute_current(self) -> GameState:
        stop_all_sounds()
        return self.game_state


@register_component(BUILD_SELECTION)
class BuildSelect(LinearComponent):
    def __init__(self, _: GameState):
        super().__init__(GameState(), TutorialDecision)

    def execute_current(self) -> None:
        stop_all_sounds()
        play_music(START_THEME)
        player = self.game_state.player
        while not player.name:
            player.name = safe_input("What is your name?")
        BuildTypeSelection(self.game_state).run()
        return self.game_state


@register_component(QUIT_GAME)
class QuitGame(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self) -> GameState:
        print_and_sleep(red("You'll be back.\nOh... yes.\nYou'll be back."), 1)
        sys.exit()


class TutorialDecision(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Need an overview?",
                         yes_component=Tutorial,
                         no_component=Intro)

    def play_theme(self) -> None:
        play_music(INTRO_THEME)


class Tutorial(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         next_component=Intro,
                         display_callback=lambda _: print_and_sleep("""
BOOK OF TENCH - OVERVIEW

MISSION
- Rescue Chula and fulfill the prophecy
- Chula is hidden in one of four regions and protected by
  enemies, bosses, and powerful special bosses
- Defeat Denny Biltmore and anyone standing in your way to win

GAMEPLAY
- Travel between the City, Forest, Swamp, and Cave
- Search locations to discover enemies, items, weapons,
  perks, discoverables, special events, and bosses
- Hunt wanted enemies for bounties
- Make choices during special events, some of which may
  have lasting consequences
- Invest in questionable opportunities and hope they pay off
- Beware of the Hohkken while traveling, especially at night
- Respect Officer Hohkken

LOCATIONS

CITY
- Casino games offer high-risk ways to earn coins
- The Coffee Shop restores HP, but illness is always possible
- The Hospital sells treatments of varying effectiveness
- The Bank provides a safe place to store coins

FOREST
- The Blacksmith upgrades weapons
- The Wizard conjures random items and weapons

SWAMP
- The Shaman sells rare healing items and remedies
- The Fishmonger provides access to fishing supplies

CAVE
- The Lab pays volunteers for experiments
- The Occultist performs rituals with unpredictable outcomes

CHARACTER
- HP represents health
- Losing all HP costs a Life
- Losing all Lives ends the game
- Gain XP to level up and become stronger
- Coins are used to purchase goods and services
- Weapons are used in combat
- Items provide healing, utility, and combat effects
- Perks grant permanent bonuses and abilities

COMBAT
- Battles are turn-based and you always act first
- During your turn you may:
  Attack, Use an Item, Switch Weapons, Flee, or View Info
- Winning battles grants XP, coins, and sometimes loot
- Enemies may possess unique Traits that affect combat

WEAPONS
- Dmg: Base damage
- Acc: Base accuracy
- Var: Damage variance
  Example: Dmg 10, Var 5 = 5-15 damage
- Crit: Chance to deal 1.5x damage
- Uses: Number of attacks before the weapon breaks

FISHING
- Visit the Fishmonger to begin fishing
- Travel to different fishing areas to find unique species
- Use bait, tackle, and strategy to catch over 150 creatures
- Build your Fishing Level and complete your Fishing Log
- Rare and legendary catches can be worth a fortune

SPECIAL BOSSES
- Powerful optional enemies with unique encounters
- Often tied to special events, rumors, or discoveries
- Defeating them can yield valuable rewards and bragging rights

INVESTMENTS
- Special events may offer investment opportunities
- Choose how much to invest and wait for the outcome
- Some investments generate large profits
- Others fail spectacularly

MAIN MENU
- Save and load games
- Adjust music and sound effects
- View achievements, statistics, logs, and discoveries
"""))


class Intro(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(
            game_state,
            query=(red(
                "You wash up on a deserted beach outside of Shebokken.\n"
                "The champion tells you that his mother, Chula, was taken in the night.\n"
                "He consecrates you as the chosen spawn who shall rescue his Tench maiden.\n"
                "Fulfill the prophecy, lest Chula's life run dry...\n\n"
                "Do you accept the mission?"
        )),
            yes_component=ActionMenu,
            no_component=GameOver
        )

    def play_theme(self) -> None:
        play_music(INTRO_THEME)


class ContinueGame(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         display_callback=self._display_and_reset,
                         next_component=ActionMenu
                         )

    @staticmethod
    def _display_and_reset(game_state: GameState):
        print_and_sleep(red("""
You awaken in a dumpster behind a Showgirls 3.
You're buried beneath a pile of detritus and covered in slime...
There are parts of another man or men scattered around you."""), 3)
        game_state.player.apply_death_penalties()


class GameOver(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         display_callback=self._display,
                         next_component=ViewStatsDecision)

    @staticmethod
    def _display(_: GameState):
        play_sound(DEVIL_THUNDER)
        print_and_sleep(red("\nGame Over."), 3)
        print_and_sleep(red("\nYou are now in Hell."), 3)


class ViewStatsDecision(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Would you like to view your stats?",
                         yes_component=EndGameViewStats,
                         no_component=PlayAgainDecision)


class EndGameViewStats(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         next_component=PlayAgainDecision)

    def execute_current(self):
        display_game_stats(self.game_state)


class PlayAgainDecision(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Would you like to play again?",
                         yes_component=NewGameReset,
                         no_component=QuitGame)


class NewGameReset(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         next_component=NewGame)

    def execute_current(self) -> GameState:
        new_game_state = GameState()
        return new_game_state
