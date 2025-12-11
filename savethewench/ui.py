from colorama import Fore, Style


def _format(ansi_code, text) -> str:
    if not isinstance(text, str):
        return _format(ansi_code, str(text))
    return f"{ansi_code}{text}{Style.RESET_ALL}"


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
