from random import Random

from common.Actions import Actions
from common.Interface import Interface
from common.Snake import Snake


class Game:
    def __init__(self, interface: Interface):
        self.size = interface.size
        self.interface = interface
        self.snake = Snake(self.size)
        self.random = Random()
        self.food_coords = None
        self.lose = False
        self.running = True
        self.keys_to_funcs = {
            Actions.MOVE_DOWN: self.move_down,
            Actions.MOVE_UP: self.move_up,
            Actions.MOVE_LEFT: self.move_left,
            Actions.MOVE_RIGHT: self.move_right,
            Actions.EXIT: self.exit,
            Actions.UNKNOWN_COMMAND: self.unknown_command
        }

    def start(self):
        self.generate_food_coords()
        while self.running:
            command = self.interface.parse_input(self.lose)
            self.parse_command(command)
            self.interface.draw(self.snake, self.lose, self.food_coords)

    def parse_command(self, command: Actions):
        self.keys_to_funcs[command]()

    def generate_food_coords(self):
        self.food_coords = None
        while self.food_coords is None or self.food_coords in self.snake.nodes:
            self.food_coords = (self.random.randint(0, self.size - 1), self.random.randint(0, self.size - 1))

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

    def exit(self):
        self.running = False

    def unknown_command(self):
        pass
