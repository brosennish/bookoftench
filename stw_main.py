from stw_functions import run_game
from colorama import init

from stw_audio import stop_all_sounds

if __name__ == "__main__":
    try:
        init(autoreset=True)
        run_game()
    except Exception as e:
        print("Game crashed:", e)
        raise
    finally:
        stop_all_sounds()
