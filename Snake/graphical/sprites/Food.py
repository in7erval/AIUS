import pygame.sprite


class Food(pygame.sprite.Sprite):
    def __init__(self, coords, block_size, lose, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        if lose:
            self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] * block_size, coords[1] * block_size)