import time
from random import Random

from common.Actions import Actions
from common.GameInterface import GameInterface
from common.Snake import Snake
from console.ConsoleInterface import ConsoleInterface

MAX_SPEED = 10
MIN_SPEED = 1


class Game:

    def __init__(self, interface: GameInterface):
        self.size = interface.size
        self.interface = interface
        self.snake = Snake(self.size)
        self.random = Random()
        self.food_coords = None
        self.lose = False
        self.running = True
        self.snake_moving = None
        self.snake_speed = 5
        self.win = False
        self.cheat_mode = interface.cheat_mode
        # !!! ужасный костыль, консольный вариант не работает с постоянным движением
        self.is_single_key_mode = True if isinstance(interface, ConsoleInterface) else False
        self.clock = time.time()
        self.commands_to_funcs = {
            Actions.MOVE_DOWN: self.move_down,
            Actions.MOVE_UP: self.move_up,
            Actions.MOVE_LEFT: self.move_left,
            Actions.MOVE_RIGHT: self.move_right,
            Actions.SINGLE_KEY_MODE: self.single_key_mode,
            Actions.SPEED_UP: self.speed_up,
            Actions.SPEED_DOWN: self.speed_down,
            Actions.RESET: self.reset,
            Actions.EXIT: self.exit,
            Actions.UNKNOWN_COMMAND: self.unknown_command
        }

    def start(self):
        self.generate_food_coords()
        self.interface.draw(self.snake, self.lose, self.food_coords, self.snake_speed, self.is_single_key_mode,
                            self.win)
        while self.running:
            self.move_snake_if_not_single_key_mode()
            command = self.interface.parse_input(self.lose, self.win)
            self.parse_command(command)
            self.interface.draw(self.snake, self.lose, self.food_coords, self.snake_speed, self.is_single_key_mode,
                                self.win)

    def move_snake_if_not_single_key_mode(self):
        if not self.is_single_key_mode:
            new_time = time.time()
            if self.snake_moving is not None and new_time - self.clock > (MAX_SPEED + 1 - self.snake_speed) * 0.05:
                self.clock = new_time
                self.snake_moving()

    def parse_command(self, command: Actions):
        func = self.commands_to_funcs[command]
        if not self.is_single_key_mode and func in (self.move_down, self.move_up, self.move_left, self.move_right):
            self.snake_moving = func
        else:
            func()

    def generate_food_coords(self):
        if len(self.snake.nodes) == self.size * self.size:
            self.win = True
        else:
            # >>>>>> ЧИТЫ!!!!!! <<<<<<
            if self.cheat_mode:
                potential_food = [(self.snake.head_coords[0] + 1, self.snake.head_coords[1]),
                                  (self.snake.head_coords[0], self.snake.head_coords[1] + 1),
                                  (self.snake.head_coords[0] - 1, self.snake.head_coords[1]),
                                  (self.snake.head_coords[0], self.snake.head_coords[1] - 1)]
                for food in potential_food:
                    if food not in self.snake.nodes and 0 <= food[0] < self.size and 0 <= food[1] < self.size:
                        self.food_coords = food
            else:
                self.food_coords = None
                while self.food_coords is None or self.food_coords in self.snake.nodes:  # пока координаты вкусняшки на змейке
                    self.food_coords = (self.random.randint(0, self.size - 1), self.random.randint(0, self.size - 1))

    def move_up(self):
        self.move(self.get_new_coords(dy=-1))

    def move_down(self):
        self.move(self.get_new_coords(dy=1))

    def move_left(self):
        self.move(self.get_new_coords(dx=-1))

    def move_right(self):
        self.move(self.get_new_coords(dx=1))

    def get_new_coords(self, dx: int = 0, dy: int = 0) -> tuple:
        curr_coords = self.snake.head_coords
        return curr_coords[0] + dx, curr_coords[1] + dy

    def move(self, new_head_coords: tuple):
        if not self.check_new_coords(new_head_coords):
            self.lose = True
        else:
            is_food = new_head_coords == self.food_coords  # съели вкусняшку?
            self.snake.move(new_head_coords, is_food=is_food)
            if is_food:
                self.generate_food_coords()

    def reset(self):
        self.snake = Snake(self.size)
        self.generate_food_coords()
        self.lose = False
        self.running = True
        self.snake_moving = None
        self.win = False

    def check_new_coords(self, new_coords: tuple) -> bool:
        return (0 <= new_coords[0] < self.size and  # не вышли по ширине
                0 <= new_coords[1] < self.size and  # не вышли по высоте
                new_coords not in self.snake.nodes)  # не упёрлись в себя

    def exit(self):
        self.interface.exit_game()
        self.running = False

    def single_key_mode(self):
        self.is_single_key_mode = not self.is_single_key_mode
        self.snake_moving = None

    def speed_up(self):
        self.snake_speed = MAX_SPEED if (self.snake_speed + 1) > MAX_SPEED else self.snake_speed + 1

    def speed_down(self):
        self.snake_speed = MIN_SPEED if (self.snake_speed - 1) < MIN_SPEED else self.snake_speed - 1

    def unknown_command(self):
        """ Just ignore unknown command """
        pass
