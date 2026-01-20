import curses


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
