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
INFO_TEXTS = ['E - show/hide this info',
              'R - reset',
              'Z - snake color animation',
              'X - change bg color',
              'Q - exit',
              'F - on/off single key mode',
              'T - speed up',
              'G - speed down',
              '1-5 - change snake color']
TAIL_PALETTE = {
    pygame.K_1: 0,
    pygame.K_2: 1,
    pygame.K_3: 2,
    pygame.K_4: 3,
    pygame.K_5: 4
}
KEYS_TO_COMMANDS = {
    pygame.K_s: Actions.MOVE_DOWN,
    pygame.K_w: Actions.MOVE_UP,
    pygame.K_a: Actions.MOVE_LEFT,
    pygame.K_d: Actions.MOVE_RIGHT,
    pygame.K_DOWN: Actions.MOVE_DOWN,
    pygame.K_UP: Actions.MOVE_UP,
    pygame.K_LEFT: Actions.MOVE_LEFT,
    pygame.K_RIGHT: Actions.MOVE_RIGHT,
    pygame.K_f: Actions.SINGLE_KEY_MODE,
    pygame.K_t: Actions.SPEED_UP,
    pygame.K_g: Actions.SPEED_DOWN,
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

    def __init__(self, size: int, block_size: int = 50, fun: bool = False, cheat: bool = False):
        super().__init__(size, cheat)
        self.block_size = block_size
        self.pygame_init()
        self.animation_color = False
        self.background = 0
        self.tail_palette = 0
        self.show_info = False
        self.headimage = get_image('headsnake.png' if not fun else 'andrew.png', block_size)
        self.foodimage = get_image('cake.png' if not fun else 'beer.png', block_size)
        self.background_image = get_image('background.png', block_size * size)

    def pygame_init(self):
        pygame.init()
        pygame.font.init()
        self.font_game_over = pygame.font.SysFont('menlo', self.block_size // 2)
        self.font = pygame.font.SysFont('menlo', 10)
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

    def draw(self, snake: Snake, lose: bool, food_coords: tuple, snake_speed: int, single_key_mode: bool, win: bool):
        self.all_sprites.empty()
        self.fill_background()
        self.all_sprites.add(SnakeHead(snake.head_coords, self.block_size, lose, self.headimage))
        self.all_sprites.add(Food(food_coords, self.block_size, lose, self.foodimage))
        for i in range(1, len(snake.nodes)):
            percent = 1 - i / (len(snake.nodes) - 1)
            snake_tail = SnakeTail(snake.nodes[i], self.block_size, percent, self.animation_color, lose, i,
                                   self.tail_palette)
            self.all_sprites.add(snake_tail)
        self.show_grid()
        self.all_sprites.draw(self.screen)
        self.place_info(len(snake.nodes), snake_speed, single_key_mode)
        if win:
            self.place_main_text("You win!")
        if lose:
            self.place_main_text("Game over!")
        pygame.display.flip()

    def show_grid(self):
        for i in range(0, self.size):
            pygame.draw.line(self.screen, BLACK, (0, i * self.block_size),
                             (self.block_size * self.size, i * self.block_size))
            pygame.draw.line(self.screen, BLACK, (i * self.block_size, 0),
                             (i * self.block_size, self.block_size * self.size))

    def place_info(self, score: int, snake_speed: int, single_key_mode: bool):
        score_text = self.font.render("Snake's length: " + str(score), True, (255, 255, 0), (0, 0, 0))
        speed_text = self.font.render("Snake's speed: " + self.get_snake_speed_text(snake_speed), True, (255, 255, 0),
                                      (0, 0, 0))
        single_text = self.font.render("Single key mode: " + str(single_key_mode), True, (255, 255, 0), (0, 0, 0))
        self.screen.blit(score_text, (self.size * self.block_size - score_text.get_size()[0], 0))
        self.screen.blit(speed_text, (self.size * self.block_size - speed_text.get_size()[0], score_text.get_size()[1]))
        self.screen.blit(single_text, (self.size * self.block_size - single_text.get_size()[0],
                                       speed_text.get_size()[1] + score_text.get_size()[1]))
        self.screen.blit(self.font.render(INFO_TEXTS[0], True, (100, 100, 100), (30, 30, 30)), (0, 0))
        if self.show_info:
            for i in range(1, len(INFO_TEXTS)):
                y = self.font.size(INFO_TEXTS[i])[1] * i  # ???????????? ???????????? * ??????????
                self.screen.blit(self.font.render(INFO_TEXTS[i], True, (100, 100, 100), (30, 30, 30)), (0, y))

    def get_snake_speed_text(self, snake_speed: int) -> str:
        if snake_speed == 10:
            return "MAX SPEEEED"
        if snake_speed >= 9:
            return "IMPOSSIBLE!1!1!!"
        if snake_speed >= 7:
            return "HARD!"
        if snake_speed >= 5:
            return "COMMON:)"
        if snake_speed >= 3:
            return "SLOW.."
        return "SNAIL....."

    def place_main_text(self, text: str):
        text = self.font_game_over.render(text, False, (255, 0, 255))
        x = self.size * (self.block_size // 2) - text.get_size()[0] // 2
        y = self.size * (self.block_size // 2) - text.get_size()[1] // 2
        self.screen.blit(text, (x, y))

    def parse_inner_actions(self, event):
        if event.key == pygame.K_e:
            self.show_info = not self.show_info
        if event.key == pygame.K_z:
            self.animation_color = not self.animation_color
        if event.key == pygame.K_x:
            self.background = (self.background + 1) % (len(BACKGROUND_COLORS) + 1)
        if event.key in TAIL_PALETTE.keys():
            self.tail_palette = TAIL_PALETTE[event.key]

    def parse_input(self, lose: bool, win: bool) -> Actions:
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
                if not lose and not win and event.key in KEYS_TO_COMMANDS.keys():
                    return KEYS_TO_COMMANDS[event.key]
        return Actions.UNKNOWN_COMMAND

    def exit_game(self):
        pygame.quit()
        sys.exit()
