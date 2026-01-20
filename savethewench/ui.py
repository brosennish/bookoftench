from colorama import Fore, Style


def _format(ansi_code, text) -> str:
    return f"{ansi_code}{str(text)}{Style.RESET_ALL}"


# --- Colors ---

def blue(text):
    return _format(Fore.BLUE, text)


def cyan(text):
    return _format(Fore.CYAN, text)


def green(text):
    return _format(Fore.GREEN, text)


def orange(text):
    return _format("\033[38;5;208m", text)


def purple(text):
    return _format(Fore.MAGENTA, text)


def red(text):
    return _format(Fore.RED, text)


def white(text):
    return _format(Fore.WHITE, text)


def yellow(text):
    return _format(Fore.YELLOW, text)


# Color Constants
class Colors:
    BLUE = "Blue"
    CYAN = "Cyan"
    GREEN = "Green"
    ORANGE = "Orange"
    PURPLE = "Purple"
    RED = "Red"
    WHITE = "White"
    YELLOW = "Yellow"


def color_text(color: str, text: str) -> str:
    match color:
        case Colors.BLUE:
            return blue(text)
        case Colors.CYAN:
            return cyan(text)
        case Colors.GREEN:
            return green(text)
        case Colors.ORANGE:
            return orange(text)
        case Colors.PURPLE:
            return purple(text)
        case Colors.RED:
            return red(text)
        case Colors.WHITE:
            return white(text)
        case Colors.YELLOW:
            return yellow(text)
        case _:
            raise NotImplementedError


# --- Styles ---

def bright(text):
    return _format(Style.BRIGHT, text)


def dim(text):
    return _format(Style.DIM, text)


# TODO - does it even make sense to have these last two?
def normal(text):
    return _format(Style.NORMAL, text)


def reset(text):
    return _format(Style.RESET_ALL, text)
