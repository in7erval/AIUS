import os
import sys

import pygame

from common.Actions import Actions
from common.GameInterface import GameInterface
from common.Snake import Snake
from graphical.sprites.Food import Food
from graphical.sprites.SnakeHead import SnakeHead
from graphical.sprites.SnakeTail import SnakeTail

FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
BACKGROUND_COLORS = [BLACK, WHITE, GRAY]
INFO_TEXTS = ['G - show/hide this info',
              'R - reset',
              'F - snake color animation',
              'T - change bg color',
              'Q - exit']
KEYS_TO_COMMANDS = {
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
        self.headimage = get_image('headsnake.png' if not fun else 'andrew.png', block_size)
        self.foodimage = get_image('cake.png' if not fun else 'beer.png', block_size)
        self.background_image = get_image('background.png', block_size * size)

    def pygame_init(self):
        pygame.init()
        pygame.font.init()
        self.font_game_over = pygame.font.SysFont('menlo', self.block_size // 2)
        self.font = pygame.font.SysFont('menlo', 15)
        self.screen = pygame.display.set_mode((self.size * self.block_size, self.size * self.block_size))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.clock.tick(FPS)

    def fill_background(self):
        if self.background == 0:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(BACKGROUND_COLORS[self.background - 1])

    def draw(self, snake: Snake, lose: bool, food_coords: tuple):
        self.all_sprites.empty()
        self.fill_background()
        self.all_sprites.add(SnakeHead(snake.head_coords, self.block_size, lose, self.headimage))
        self.all_sprites.add(Food(food_coords, self.block_size, lose, self.foodimage))
        for i in range(1, len(snake.nodes)):
            percent = 1 - i / (len(snake.nodes) - 1)
            snake_tail = SnakeTail(snake.nodes[i], self.block_size, percent, self.animation_color, lose)
            self.all_sprites.add(snake_tail)
        self.all_sprites.draw(self.screen)
        self.place_info(len(snake.nodes))
        if lose:
            self.place_game_over_text()
        pygame.display.flip()

    def place_info(self, score):
        score_text = self.font.render("Snake's length: " + str(score), True, (255, 255, 0), (0, 0, 0))
        self.screen.blit(score_text, (self.size * self.block_size - score_text.get_size()[0], 0))
        self.screen.blit(self.font.render(INFO_TEXTS[0], True, (100, 100, 100), (30, 30, 30)), (0, 0))
        if self.show_info:
            for i in range(1, len(INFO_TEXTS)):
                y = self.font.size(INFO_TEXTS[i])[1] * i  # высота текста * номер
                self.screen.blit(self.font.render(INFO_TEXTS[i], True, (100, 100, 100), (30, 30, 30)), (0, y))

    def place_game_over_text(self):
        text = self.font_game_over.render('Game over!', False, (255, 0, 255))
        x = self.size * (self.block_size // 2) - text.get_size()[0] // 2
        y = self.size * (self.block_size // 2) - text.get_size()[1] // 2
        self.screen.blit(text, (x, y))

    def parse_inner_actions(self, event):
        if event.key == pygame.K_g:
            self.show_info = not self.show_info
        if event.key == pygame.K_f:
            self.animation_color = not self.animation_color
        if event.key == pygame.K_t:
            self.background = (self.background + 1) % (len(BACKGROUND_COLORS) + 1)

    def parse_input(self, lose: bool) -> Actions:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return Actions.EXIT
            if event.type == pygame.KEYDOWN:
                self.parse_inner_actions(event)
                if event.key == pygame.K_q:
                    return Actions.EXIT
                if event.key == pygame.K_r:
                    return Actions.RESET
                if not lose and event.key in KEYS_TO_COMMANDS.keys():
                    return KEYS_TO_COMMANDS[event.key]
        return Actions.UNKNOWN_COMMAND

    def exit_game(self):
        pygame.quit()
        sys.exit()
