from stw_functions import main_menu
from colorama import init

from stw_audio import stop_all_sounds

if __name__ == "__main__":
    try:
        init(autoreset=True)
        main_menu()
    except Exception as e:
        print("Game crashed:", e)
        raise e
    finally:
        stop_all_sounds()