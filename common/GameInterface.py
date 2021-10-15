from common.Actions import Actions


class GameInterface:

    def __init__(self, size):
        self.size = size

    def draw(self, snake, lose, food_coords):
        pass

    def parse_input(self, lose: bool) -> Actions:
        pass
