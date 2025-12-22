import select
import sys
import termios
import time as t

from savethewench.ui import blue


# TODO - this only works for mac - extend support to windows
def flush_input():
    if sys.stdin.isatty():  # running in an actual terminal (not PyCharm)
        termios.tcflush(sys.stdin, termios.TCIFLUSH)


def skippable_sleep(seconds):
    end = t.time() + seconds
    while t.time() < end:
        r, _, _ = select.select([sys.stdin], [], [], 0)
        if r:
            sys.stdin.readline()
            return
        t.sleep(0.05)


def print_and_sleep(text: str, seconds: float = 0, newline_prefix: bool = True):
    print(f"{'\n' if newline_prefix else ''}{text}")
    skippable_sleep(seconds)


def safe_input(prompt=""):
    flush_input()
    return input(f"{f"\n{prompt}\n" if len(prompt) > 0 else ''}{blue(">")} ")
