import random

import pygame.sprite

GRADIENTS = (((255, 255, 0), (255, 0, 0)),
             ((255, 255, 0), (0, 255, 0)),
             ((255, 255, 0), (0, 0, 255)))


def calculate_gradient_component(fr: int, to: int, percent: float) -> int:
    return int(to - percent * (to - fr))


def calculate_width(block_size: int, percentile: float) -> int:
    return calculate_gradient_component(10, block_size // 2, percentile)


def create_color(color_from, color_to, percentile) -> tuple:
    return tuple([calculate_gradient_component(color_from[i], color_to[i], percentile) for i in range(3)])


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class SnakeTail(pygame.sprite.Sprite):

    def __init__(self, coords: tuple, block_size: int, percentile: float, animation: bool, lose: bool, len: int,
                 tail_pallette: int):
        pygame.sprite.Sprite.__init__(self)
        self.colors = random.Random().choice(GRADIENTS) if animation else GRADIENTS[tail_pallette % 3]
        self.image = pygame.Surface((block_size, block_size))
        self.image.set_alpha(255)
        self.color = create_color(self.colors[0], self.colors[1], percentile)
        if not lose:
            if tail_pallette == 0:
                self.circles(block_size, percentile)
            elif tail_pallette == 1:
                self.circles(block_size, percentile)
            elif tail_pallette == 2:
                self.circles(block_size, percentile)
            elif tail_pallette == 3:
                self.hypnotic_circles(block_size, len)
            elif tail_pallette == 4:
                self.hypnotic_squares(block_size, len)
        else:
            self.rect = pygame.draw.polygon(self.image, self.color, [(0, 0), (block_size // 2, block_size // 2),
                                                                     (0, block_size),
                                                                     (block_size // 2, block_size // 2),
                                                                     (block_size, block_size),
                                                                     (block_size // 2, block_size // 2),
                                                                     (block_size, 0),
                                                                     (block_size // 2, block_size // 2)],
                                            width=calculate_width(block_size, percentile))
        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] * block_size, coords[1] * block_size)

    def hypnotic_circles(self, block_size: int, len: int):
        for i in range(1, len + 1):
            self.rect = pygame.draw.circle(self.image, BLACK if i % 2 == 0 else WHITE,
                                           (block_size // 2, block_size // 2),
                                           block_size * (len - i + 1) // (2 * len), width=2)
            self.rect.topleft = (0, 0)

    def hypnotic_squares(self, block_size: int, len: int):
        dx = block_size / (2 * len)
        for i in range(1, len + 1):
            self.rect = pygame.draw.rect(self.image, BLACK if i % 2 == 0 else WHITE,
                                         [int((i - 1) * dx), int((i - 1) * dx),
                                          block_size * (len - i + 1) // len, block_size * (len - i + 1) // len],
                                         width=0)
            self.rect.topleft = (0, 0)

    def circles(self, block_size: int, percentile: float):
        self.rect = pygame.draw.circle(self.image, self.color, (block_size // 2, block_size // 2),
                                       block_size // 2, width=calculate_width(block_size, percentile))
