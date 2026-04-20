import os
import sys
import time as t

from bookoftench.ui import blue


# --- Platform-specific input handling ---

if os.name == "nt":
    import msvcrt

    def get_key():
        return msvcrt.getch().decode(errors="ignore")

    def flush_input():
        while msvcrt.kbhit():
            msvcrt.getch()

    def skippable_sleep(seconds) -> None:
        end = t.time() + seconds
        while t.time() < end:
            if msvcrt.kbhit():
                msvcrt.getch()
                return
            t.sleep(0.05)

else:
    import termios
    import tty
    import select

    def get_key():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def flush_input():
        if sys.stdin.isatty():
            termios.tcflush(sys.stdin, termios.TCIFLUSH)

    def skippable_sleep(seconds) -> None:
        end = t.time() + seconds
        while t.time() < end:
            r, _, _ = select.select([sys.stdin], [], [], 0)
            if r:
                sys.stdin.readline()
                return
            t.sleep(0.05)


# --- Shared helpers ---

def print_and_sleep(text: str, seconds: float = 0, newline_prefix: bool = True):
    print(f"{'\n' if newline_prefix else ''}{text}")
    skippable_sleep(seconds)


def carrot(color) -> str:
    if not color:
        color = blue
    return color("\n> ")


def safe_input(prompt=""):
    flush_input()
    return input(f"{f'\n{prompt}\n' if len(prompt) > 0 else ''}{blue('>')} ")