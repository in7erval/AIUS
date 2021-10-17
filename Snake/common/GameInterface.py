from common.Actions import Actions
from common.Snake import Snake


class GameInterface:

    def __init__(self, size: int, cheat_mode: bool):
        self.size = size
        self.cheat_mode = cheat_mode

    def draw(self, snake: Snake, lose: bool, food_coords: tuple, snake_speed: int, single_key_mode: bool, win: bool):
        """ Draw current game state """
        pass

    def parse_input(self, lose: bool, win: bool) -> Actions:
        """ Parse input event """
        pass

    def exit_game(self):
        """ Exit game and close interface """
        pass
