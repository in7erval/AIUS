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


class SnakeTail(pygame.sprite.Sprite):

    def __init__(self, coords: tuple, block_size: int, percentile: float, animation: bool, lose: bool):
        pygame.sprite.Sprite.__init__(self)
        self.colors = random.Random().choice(GRADIENTS) if animation else GRADIENTS[0]
        self.image = pygame.Surface((block_size, block_size))
        self.image.set_alpha(255)
        self.color = create_color(self.colors[0], self.colors[1], percentile)
        if not lose:
            self.rect = pygame.draw.circle(self.image, self.color, (block_size // 2, block_size // 2),
                                           block_size // 2, width=calculate_width(block_size, percentile))
        else:
            self.rect = pygame.draw.polygon(self.image, self.color, [(0, 0), (block_size // 2, block_size // 2),
                                                                     (0, block_size),
                                                                     (block_size // 2, block_size // 2),
                                                                     (block_size, block_size),
                                                                     (block_size // 2, block_size // 2),
                                                                     (block_size, 0),
                                                                     (block_size // 2, block_size // 2)],
                                            width=calculate_width(block_size, percentile))
        self.rect.topleft = (coords[0] * block_size, coords[1] * block_size)
