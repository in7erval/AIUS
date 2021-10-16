import curses
import random

from common.Actions import Actions
from common.GameInterface import GameInterface
from common.Snake import Snake


def init_screen():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr


def get_sign(coords: tuple, snake: Snake, lose: bool, food_coords: tuple) -> (str, int):
    if snake.head_coords == coords:
        return '%', curses.A_BOLD
    elif snake.last_coords == coords:
        return '#', curses.A_BOLD
    elif coords in snake.nodes:
        return 'o', curses.A_BOLD
    elif food_coords == coords:
        return '+', curses.A_STANDOUT
    else:
        return ('=', curses.A_DIM) if lose else ('.', curses.A_DIM)


class ConsoleInterface(GameInterface):

    def __init__(self, size):
        super().__init__(size)
        self.stdscr = init_screen()
        self.check_console()
        self.random = random.Random()
        self.keys_to_funcs = {
            curses.KEY_DOWN: Actions.MOVE_DOWN,
            curses.KEY_UP: Actions.MOVE_UP,
            curses.KEY_LEFT: Actions.MOVE_LEFT,
            curses.KEY_RIGHT: Actions.MOVE_RIGHT,
            ord('s'): Actions.MOVE_DOWN,
            ord('w'): Actions.MOVE_UP,
            ord('a'): Actions.MOVE_LEFT,
            ord('d'): Actions.MOVE_RIGHT,
            ord('r'): Actions.RESET
        }

    def parse_input(self, lose: bool) -> Actions:
        ch = self.stdscr.getch()
        if ch == ord('q'):
            return Actions.EXIT
        if ch == ord('r'):
            return Actions.RESET
        elif not lose:
            if ch in self.keys_to_funcs.keys():
                return self.keys_to_funcs[ch]
        return Actions.UNKNOWN_COMMAND

    def check_console(self):
        height, width = self.stdscr.getmaxyx()
        if height < self.size:
            self.exit_game()
            raise RuntimeError("Please, make console higher")
        if width < self.size:
            self.exit_game()
            raise RuntimeError("Please, make console wider")

    def draw(self, snake: Snake, lose: bool, food_coords: tuple):
        self.stdscr.clear()
        for i in range(self.size):
            for j in range(self.size):
                ch, attr = get_sign((j, i), snake, lose, food_coords)
                self.stdscr.addstr(i, j, ch, attr)
        if lose:
            self.stdscr.addstr(self.size, 0, "You lose! Press 'q' to exit")
            self.stdscr.addstr(self.size + 1, 0, "Press 'r' to restart")

    def exit_game(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
