import curses
import random

from Snake import Snake


def initscr():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr


class Game:

    def __init__(self, size: int):
        self.size = size
        self.stdscr = initscr()
        self.snake = Snake(size)
        self.random = random.Random()
        self.food_coords = None
        self.lose = False
        self.stop_game = False
        self.keys_to_funcs = {
            curses.KEY_DOWN: self.move_down,
            curses.KEY_UP: self.move_up,
            curses.KEY_LEFT: self.move_left,
            curses.KEY_RIGHT: self.move_right,
            ord('s'): self.move_down,
            ord('w'): self.move_up,
            ord('a'): self.move_left,
            ord('d'): self.move_right
        }

    def start(self):
        self.generate_food_coords()
        while not self.stop_game:
            self.display_field()
            self.parse_input(self.stdscr.getch())
            self.stdscr.clear()
        self.exit_game()

    def parse_input(self, ch):
        if ch == ord('q'):
            self.stop_game = True
        elif not self.lose:
            if ch in self.keys_to_funcs.keys():
                self.keys_to_funcs[ch]()

    def generate_food_coords(self):
        self.food_coords = None
        while self.food_coords is None or self.food_coords in self.snake.nodes:
            self.food_coords = (self.random.randint(0, self.size - 1), self.random.randint(0, self.size - 1))

    def display_field(self):
        for i in range(self.size):
            for j in range(self.size):
                self.stdscr.addstr(i, j, self.get_sign((j, i)))
        if self.lose:
            self.stdscr.addstr(self.size, 0, "You lose! Press 'q' to exit")

    def get_sign(self, coords) -> str:
        if self.snake.head_coords == coords:
            return '🐲'
        elif self.snake.last_coords == coords:
            return '💠'
        elif coords in self.snake.nodes:
            return '🐍'
        elif self.food_coords == coords:
            return '🍺'
        else:
            return '🏴‍' if self.lose else '🏳️'

    def move_up(self):
        self.move(self.get_new_coords(dy=-1))

    def move_down(self):
        self.move(self.get_new_coords(dy=1))

    def move_left(self):
        self.move(self.get_new_coords(dx=-1))

    def move_right(self):
        self.move(self.get_new_coords(dx=1))

    def get_new_coords(self, dx=0, dy=0) -> tuple:
        curr_coords = self.snake.head_coords
        return curr_coords[0] + dx, curr_coords[1] + dy

    def move(self, new_head_coords):
        if not self.check_new_coords(new_head_coords):
            self.lose = True
        else:
            if new_head_coords == self.food_coords:
                self.snake.move(new_head_coords, is_food=True)
                self.generate_food_coords()
            else:
                self.snake.move(new_head_coords)

    def check_new_coords(self, new_coords: tuple) -> bool:
        return (0 <= new_coords[0] < self.size and
                0 <= new_coords[1] < self.size and
                new_coords not in self.snake.nodes)

    def exit_game(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

