import os
import sys

import pygame

from common.Actions import Actions
from common.GameInterface import GameInterface
from common.Snake import Snake
from graphical.sprites.Food import Food
from graphical.sprites.SnakeBetween import SnakeBetween
from graphical.sprites.SnakeHead import SnakeHead

FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
BACKGROUND_COLORS = [BLACK, WHITE, GRAY]
INFO_TEXTS = ['G - show/hide this info',
              'R - reset',
              'F - color animation',
              'T - change bg color',
              'Q - exit']


def get_image(picname: str, block_size: int) -> pygame.Surface:
    this_folder = os.path.dirname(__file__)
    img_folder = os.path.join(this_folder, 'pics')
    image = pygame.image.load(os.path.join(img_folder, picname)).convert()
    image.set_alpha(255)
    return pygame.transform.scale(image, (block_size, block_size))


class GraphicalInterface(GameInterface):

    def __init__(self, size: int, block_size: int = 50, fun: bool = False):
        super().__init__(size)
        self.block_size = block_size
        self.pygame_init()
        self.animation_color = False
        self.background = 0
        self.show_info = False
        self.keys_to_funcs = {
            pygame.K_s: Actions.MOVE_DOWN,
            pygame.K_w: Actions.MOVE_UP,
            pygame.K_a: Actions.MOVE_LEFT,
            pygame.K_d: Actions.MOVE_RIGHT,
            pygame.K_DOWN: Actions.MOVE_DOWN,
            pygame.K_UP: Actions.MOVE_UP,
            pygame.K_LEFT: Actions.MOVE_LEFT,
            pygame.K_RIGHT: Actions.MOVE_RIGHT,
            pygame.K_r: Actions.RESET,
            pygame.K_q: Actions.EXIT
        }
        self.headimage = get_image('andrew.png' if fun else 'headsnake.png', block_size)
        self.foodimage = get_image('beer.png' if fun else 'cake.png', block_size)
        self.background_image = get_image('background.png', block_size * size)

    def pygame_init(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.font_game_over = pygame.font.SysFont('menlo', self.block_size // 2)
        self.font = pygame.font.SysFont('menlo', 15)
        self.screen = pygame.display.set_mode((self.size * self.block_size, self.size * self.block_size))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()

    def fill_background(self):
        if self.background == 0:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(BACKGROUND_COLORS[self.background - 1])

    def draw(self, snake: Snake, lose: bool, food_coords: tuple):
        self.clock.tick(FPS)
        self.all_sprites.empty()
        self.fill_background()
        self.all_sprites.add(SnakeHead(snake.head_coords, self.block_size, lose, self.headimage))
        for i in range(1, len(snake.nodes)):
            self.all_sprites.add(SnakeBetween(snake.nodes[i], self.block_size, 1 - i / (len(snake.nodes) - 1),
                                              self.animation_color, lose))
        self.all_sprites.add(Food(food_coords, self.block_size, lose, self.foodimage))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        self.place_info()
        if lose:
            self.place_game_over_text()
        pygame.display.flip()

    def place_info(self):
        self.screen.blit(self.font.render(INFO_TEXTS[0], False, (100, 100, 100)), (0, 0))
        if self.show_info:
            for i in range(1, len(INFO_TEXTS)):
                y = self.font.size(INFO_TEXTS[i])[1] * i  # высота текста * номер
                self.screen.blit(self.font.render(INFO_TEXTS[i], False, (100, 100, 100)), (0, y))

    def place_game_over_text(self):
        x = self.size * (self.block_size // 2) - int(self.block_size * 1.5)
        y = x + self.block_size // 2
        self.screen.blit(self.font_game_over.render('Game over!', False, (255, 0, 255)), (x, y))

    def parse_input(self, lose: bool) -> Actions:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return Actions.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    self.show_info = not self.show_info
                if event.key == pygame.K_f:
                    self.animation_color = not self.animation_color
                if event.key == pygame.K_t:
                    self.background = (self.background + 1) % (len(BACKGROUND_COLORS) + 1)
                if event.key == pygame.K_q:
                    return Actions.EXIT
                if event.key == pygame.K_r:
                    return Actions.RESET
                if not lose and event.key in self.keys_to_funcs.keys():
                    return self.keys_to_funcs[event.key]
        return Actions.UNKNOWN_COMMAND

    def exit_game(self):
        pygame.quit()
        sys.exit()
