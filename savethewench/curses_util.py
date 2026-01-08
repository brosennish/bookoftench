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

def c_print(stdscr, line: int, offset: int, text: str, color: int = curses.COLOR_WHITE,
            highlight: bool = False, underline: bool = False, bold: bool = False):
    color_pair = curses.color_pair(color)
    if highlight:
        color_pair |= curses.A_REVERSE
    if underline:
        color_pair |= curses.A_UNDERLINE
    if bold:
        color_pair |= curses.A_BOLD
    stdscr.addstr(line, offset, text, color_pair)