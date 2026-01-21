import curses
from dataclasses import dataclass
from typing import List


def init_colors():
    curses.start_color()
    curses.init_pair(curses.COLOR_WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_MAGENTA, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)


def combine_attrs(*flags: tuple[bool, int]) -> int:
    return sum(attr for flag, attr in flags if flag)


def c_print(stdscr, line: int, offset: int, text: str, color: int = curses.COLOR_WHITE,
            highlight: bool = False, underline: bool = False, bold: bool = False, dim: bool = False):
    attrs = combine_attrs(
        (highlight, curses.A_REVERSE),
        (underline, curses.A_UNDERLINE),
        (bold, curses.A_BOLD),
        (dim, curses.A_DIM)
    )
    stdscr.addstr(line, offset, text, curses.color_pair(color) | attrs)


@dataclass
class LinePart:
    text: str
    color: int = curses.COLOR_WHITE
    underline: bool = False
    highlight: bool = False
    bold: bool = False
    dim: bool = False
    offset: int = 0

    def add_to_line(self, stdscr, line: int, offset: int):
        c_print(stdscr, line, offset, self.text, self.color,
                underline=self.underline, highlight=self.highlight, bold=self.bold, dim=self.dim)


@dataclass
class Line:
    parts: List[LinePart]
    line_number: int = 0

    def add_to_screen(self, stdscr):
        for part in self.parts:
            c_print(stdscr, self.line_number, offset=part.offset, text=part.text, color=part.color,
                    highlight=part.highlight, underline=part.underline, bold=part.bold, dim=part.dim)


class SimpleWindow:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self._current_line = 0
        self._lines = []

    def add_line(self, line: Line):
        line.line_number = self._current_line
        self._lines.append(line)
        self.add_newlines(1)

    def add_newlines(self, newlines: int):
        self._current_line += newlines

    def flush(self):
        self.stdscr.erase()
        for line in self._lines:
            line.add_to_screen(self.stdscr)
        self.stdscr.noutrefresh()
        curses.doupdate()
        self._lines.clear()
        self._current_line = 0
