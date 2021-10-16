from common.Actions import Actions
from common.Snake import Snake


class GameInterface:

    def __init__(self, size: int):
        self.size = size

    def draw(self, snake: Snake, lose: bool, food_coords: tuple):
        pass

    def parse_input(self, lose: bool) -> Actions:
        pass
