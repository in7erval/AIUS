import random

import pygame.sprite


def calculate_width(block_size: int, percentile: float) -> int:
    percentile = 1 - percentile
    width = int(block_size // 2 * percentile)
    if width < block_size // 5:
        return block_size // 5
    return width


GRADIENTS = (((255, 255, 0), (255, 0, 0)),
             ((255, 255, 0), (0, 255, 0)),
             ((255, 255, 0), (0, 0, 255)))


class SnakeBetween(pygame.sprite.Sprite):

    def __init__(self, coords: tuple, block_size: int, percentile: float, animation: bool, lose: bool):
        pygame.sprite.Sprite.__init__(self)
        self.colors = random.Random().choice(GRADIENTS) if animation else GRADIENTS[0]
        self.image = pygame.Surface((block_size, block_size))
        self.create_color(percentile)
        if not lose:
            self.rect = pygame.draw.circle(self.image, self.color, (block_size // 2, block_size // 2),
                                           block_size // 2, width=calculate_width(block_size, percentile))
        else:
            self.rect = pygame.draw.circle(self.image, (255, 0, 0), (block_size // 2, block_size // 2),
                                           block_size // 2, width=calculate_width(block_size, percentile))
        self.rect.topleft = (coords[0] * block_size, coords[1] * block_size)

    def create_color(self, percentile):
        color_from = self.colors[0]
        color_to = self.colors[1]
        calculate_component = lambda fr, to: int(to - percentile * (to - fr))
        self.color = ([calculate_component(color_from[i], color_to[i]) for i in range(3)])
