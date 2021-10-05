import pygame
import math
import os

'''
Class for enemy object

coordinates = (x, y)
'''
class Enemy(pygame.sprite.Sprite):
    def __init__(self, spawn:tuple):
        super().__init__()
        #loads image as pygame Surface object
        self.image = pygame.image.load(os.path.join(("game_assets"), "mario.png"))
        self.image = pygame.transform.scale(self.image, (50, 70))
        self.rect = self.image.get_rect()
        self.velocityX = 3
        self.rect.x = spawn[0]
        self.rect.y = spawn[1]

    def walkLeft(self):
        self.velocityX = -3
    
    def walkRight(self):
         self.velocityX = 3
    
    def update(self, screenSize,):
        #does not allow player to leave boundaries of screen
        if self.rect.x + self.rect.width > screenSize[0]:
            self.walkLeft()

        elif self.rect.x < 0:
            self.walkRight()
        
        self.rect.x += self.velocityX 
    