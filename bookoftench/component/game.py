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
                         next_component=PlayAgainDecision)

    @staticmethod
    def _display(_: GameState):
        print_and_sleep(f"You defeated the evil Denny Biltmore and rescued Chula!\n", 1)
        play_sound(GREAT_JOB)
        print_and_sleep(green("You win!"), 10)
        play_sound(VICTORY_THEME)


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
    - Your mission is to find and rescue Chula
    - She is being held in one of four areas and is guarded by
      a number of enemies and multiple bosses
    - Find Chula and defeat everyone who stands in your way
      to fulfill the prophecy and win the game
      
    GAMEPLAY
    - Travel between areas as needed
    - You may encounter the Hohkken while traveling,
      especially at night
    - Search to find discoverables, items, weapons, perks,
      special events, and enemies
    - Shop to buy/sell items and weapons or purchase perks;
      shoplifting is also an option
      
    CITY
    - The Casino offers two games where you can take a chance
      and push your luck
    - Visit the Coffee Shop for a quick HP boost at the risk
      of catching what the owner has
    - You may visit the Hospital when sick to purchase 
      treatments of questionable efficacy
    - The Bank offers a safe place for your coins to grow
      without risk of being lost
    
    FOREST
    - Visit the Blacksmith to upgrade your weapons
    - Pay the Wizard to conjure a random item or weapon
    
    SWAMP
    - The Shaman offers special items to heal HP, 
      blindness, and illness 
      
    CAVE
    - Earn coins at the Lab for participating in experiments 
    - The Occultist can perform ritual sacrifices, potentially 
      to your benefit

    ELEMENTS
    - HP is the player's health
    - If the player runs out of HP, they die and lose
      a Life
    - If the player runs out of Lives, the game is over
    - The player levels up as XP (experience) is gained 
    - Coins are the game's currency
    - Weapons are used to battle enemies
    - Items are either used to heal, become stronger,
      or assist in battle
    - Perks are permanent upgrades that have special benefits
    
    WEAPON
    - Dmg represents the base weapon damage 
    - In battle, dmg reflects base damage multiplied by
      the player or enemy's strength value
    - Acc represents the base weapon accuracy
    - In battle, acc reflects base accuracy multiplied by
      the player or enemy's accuracy value
    - Var represents the weapon's variance or spread
      Ex. Dmg: 10, Var: 5 - Damage will be between 5-15
    - Crit represents the weapon's odds for delivering a 
      critical hit (1.5x damage)
    - Uses represents the number of attacks the weapon is
      able to deliver
    - When no uses remain, the weapon breaks and is removed
      from your inventory
      
    BATTLE
    - The player and enemy take turns attacking during battle
    - The player always goes first in the turn
    - Each turn, the player has the option to either: 
      Attack, Use an Item, Switch their Weapon, Flee,
      or View player and enemy info
    - If the player wins, they are awarded coins and xp,
      and they may receive the enemy's weapon
    - Battles may be affected by the enemy Traits, which
      can be viewed in View during battle
    
    MAIN MENU
    - Save your game, load your game, and adjust sound and sfx
"""))


class Intro(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         next_component=ActionMenu,
                         display_callback=lambda _: print_and_sleep(red("""
You wash ashore on a deserted beach outside of Shebokken.
The champion has informed you that his mother, Chula, was taken in the night.
The prophecy has foretold that you shall find and return her to the champion.
Fulfill the prophecy, before her life runs dry...
""")))

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
                         next_component=BuildTypeSelection)

    def execute_current(self) -> GameState:
        new_game_state = GameState()
        return new_game_state
