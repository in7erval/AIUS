import pygame.sprite


class SnakeTail(pygame.sprite.Sprite):
    def __init__(self, coords, block_size, lose):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((block_size, block_size))
        if not lose:
            self.rect = pygame.draw.circle(self.image, (218, 187, 74), (block_size // 2, block_size // 2),
                                           block_size // 2, width=0)
        else:
            self.rect = pygame.draw.circle(self.image, (255, 0, 0), (block_size // 2, block_size // 2),
                                           block_size // 2, width=0)
        self.rect.topleft = (coords[0] * block_size, coords[1] * block_size)
