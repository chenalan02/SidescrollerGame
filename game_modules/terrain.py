import pygame
import os

class Platform(pygame.sprite.Sprite):
    def __init__(self, coordinates:tuple, length):
        super().__init__()

        self.image = pygame.image.load(os.path.join(("game_assets"), "platform.png"))
        self.image = pygame.transform.scale(self.image, (length, 50))

        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
