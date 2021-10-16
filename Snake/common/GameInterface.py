from common.Actions import Actions
from common.Snake import Snake


class GameInterface:

    def __init__(self, size: int):
        self.size = size

    def draw(self, snake: Snake, lose: bool, food_coords: tuple):
        """ Draw current game state """
        pass

    def parse_input(self, lose: bool) -> Actions:
        """ Parse input event """
        pass

    def exit_game(self):
        """ Exit game and close interface """
        pass
