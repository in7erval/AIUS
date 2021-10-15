class Snake:

    def __init__(self, size: int):
        self.head_coords = (size // 2, size // 2)
        self.length = 1
        self.nodes = [self.head_coords]
        self.last_coords = self.nodes[-1]

    def move(self, new_head_coords, is_food=False):
        self.head_coords = new_head_coords
        self.nodes.insert(0, self.head_coords)
        if not is_food:
            self.nodes.pop()
            self.last_coords = self.nodes[-1]
