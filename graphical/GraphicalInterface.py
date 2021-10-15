import os

import pygame

from common.Actions import Actions
from common.GameInterface import GameInterface
from common.Snake import Snake
from graphical.sprites.Food import Food
from graphical.sprites.SnakeBetween import SnakeBetween
from graphical.sprites.SnakeHead import SnakeHead
from graphical.sprites.SnakeTail import SnakeTail


def get_image(picname: str, block_size: int) -> pygame.Surface:
    this_folder = os.path.dirname(__file__)
    img_folder = os.path.join(this_folder, 'pics')
    image = pygame.image.load(os.path.join(img_folder, picname)).convert()
    return pygame.transform.scale(image, (block_size, block_size))


class GraphicalInterface(GameInterface):

    def __init__(self, size, block_size=50, fun=False):
        super().__init__(size)
        self.block_size = block_size
        self.pygame_init()
        self.keys_to_funcs = {
            pygame.K_s: Actions.MOVE_DOWN,
            pygame.K_w: Actions.MOVE_UP,
            pygame.K_a: Actions.MOVE_LEFT,
            pygame.K_d: Actions.MOVE_RIGHT,
            pygame.K_DOWN: Actions.MOVE_DOWN,
            pygame.K_UP: Actions.MOVE_UP,
            pygame.K_LEFT: Actions.MOVE_LEFT,
            pygame.K_RIGHT: Actions.MOVE_RIGHT,
            pygame.K_q: Actions.EXIT
        }
        self.headimage = get_image('andrew.png' if fun else 'headsnake.png', block_size)
        self.foodimage = get_image('beer.png' if fun else 'cake.png', block_size)

    def pygame_init(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.screen = pygame.display.set_mode((self.size * self.block_size, self.size * self.block_size))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()

    def draw(self, snake: Snake, lose: bool, food_coords: tuple):
        self.clock.tick(60)
        self.all_sprites.empty()
        self.all_sprites.add(SnakeTail(snake.nodes[-1], self.block_size, lose))
        self.all_sprites.add(SnakeHead(snake.head_coords, self.block_size, lose, self.headimage))
        for i in range(1, len(snake.nodes) - 1):
            self.all_sprites.add(SnakeBetween(snake.nodes[i], self.block_size, 1 - i / len(snake.nodes), lose))
        self.all_sprites.add(Food(food_coords, self.block_size, lose, self.foodimage))
        self.all_sprites.update()
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        if lose:
            self.place_text('Game over!')
        pygame.display.flip()

    def place_text(self, text):
        text = self.font.render(text, False, (255, 255, 255))
        x = self.size * self.block_size // 2 - self.block_size
        y = x
        self.screen.blit(text, (x, y))

    def parse_input(self, lose: bool) -> Actions:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return Actions.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return Actions.EXIT
                if not lose and event.key in self.keys_to_funcs.keys():
                    return self.keys_to_funcs[event.key]
        return Actions.UNKNOWN_COMMAND
