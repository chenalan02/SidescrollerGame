import pygame
import os

'''
Platform object that player can stand on and pass through from the underside

coordinates: (x,y) - top left corner of platform
length: length of platform
'''
class Platform(pygame.sprite.Sprite):
    def __init__(self, coordinates:tuple, length):
        super().__init__()

        #load and scale image
        self.image = pygame.image.load(os.path.join(("game_assets"), "platform.png"))
        self.image = pygame.transform.scale(self.image, (length, 10))

        #sets rect and coordinates
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
    
'''
Sprite for the spawn and exit portals of a section

coordinates: (x,y) of the top left corner of portal
'''
class Portal(pygame.sprite.Sprite):
    def __init__(self, coordinates):
        super().__init__()
        #load sprite as pygame Surface object
        self.image = pygame.image.load(os.path.join('game_assets', "portal.png"))
        self.image = pygame.transform.scale(self.image, (50, 100))

        #set position
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]

