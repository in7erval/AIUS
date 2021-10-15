from common.Actions import Actions
from common.Interface import Interface
import curses
import random

from common.Snake import Snake


def initscr():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr


class ConsoleInterface(Interface):

    def __init__(self, size):
        super().__init__(size)
        self.stdscr = initscr()
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
            ord('d'): Actions.MOVE_RIGHT
        }

    def parse_input(self, lose: bool) -> Actions:
        ch = self.stdscr.getch()
        if ch == ord('q'):
            return Actions.EXIT
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

    def draw(self, snake, lose, food_coords):
        for i in range(self.size):
            for j in range(self.size):
                self.stdscr.addstr(i, j, self.get_sign((j, i), snake, lose, food_coords))
        if lose:
            self.stdscr.addstr(self.size, 0, "You lose! Press 'q' to exit")

    def get_sign(self, coords: tuple, snake: Snake, lose: bool, food_coords: tuple) -> str:
        if snake.head_coords == coords:
            return '🐲'
        elif snake.last_coords == coords:
            return '🛑'
        elif coords in snake.nodes:
            return '💢'
        elif food_coords == coords:
            return '🍺'
        else:
            return '🏴‍' if lose else self.random.choice(['🌱'])

    def exit_game(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
