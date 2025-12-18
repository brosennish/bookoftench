import sys
import termios
import time as t

from savethewench.ui import blue


# TODO - this only works for mac - extend support to windows
def flush_input():
    if sys.stdin.isatty():  # running in an actual terminal (not PyCharm)
        termios.tcflush(sys.stdin, termios.TCIFLUSH)


def print_and_sleep(text: str, seconds: float = 0, newline_prefix: bool = True):
    print(f"{'\n' if newline_prefix else ''}{text}")
    t.sleep(seconds)


def safe_input(prompt=""):
    flush_input()
    return input(f"{f"\n{prompt}\n" if len(prompt) > 0 else ''}{blue(">")} ")
