import pygame.sprite


def calculate_width(block_size: int, percentile: float) -> int:
    width = int(block_size // 2 * percentile)
    if width == 0:
        return 1
    return width

  
class SnakeBetween(pygame.sprite.Sprite):
    def __init__(self, coords: tuple, block_size: int, percentile: float, lose=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((block_size, block_size))
        if not lose:
            self.rect = pygame.draw.circle(self.image, (251, 207, 54), (block_size // 2, block_size // 2),
                                           block_size // 2, width=calculate_width(block_size, percentile))
        else:
            self.rect = pygame.draw.circle(self.image, (255, 0, 0), (block_size // 2, block_size // 2),
                                           block_size // 2, width=calculate_width(block_size, percentile))
        self.rect.topleft = (coords[0] * block_size, coords[1] * block_size)
