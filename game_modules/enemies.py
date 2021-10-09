import pygame
import math
from math import sin, cos, degrees, atan, pi
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

        #saves spawn for game restart purposes
        self.spawn = spawn

        #default walks to the right on spawn
        self.velocityX = 3

        #sets position to spawn
        self.rect.x = spawn[0]
        self.rect.y = spawn[1]

    '''
    Method to reset state of enemy for when game restarts
    '''
    def reinitialize(self):
        self.rect.x = self.spawn[0]
        self.rect.y = self.spawn[1]
        self.velocityX = 3

    '''
    Methods to walk left and right by changing velocity
    '''
    def walkLeft(self):
        self.velocityX = -3
    
    def walkRight(self):
         self.velocityX = 3
        
    '''
    Method to fall at a constant rate of 5 pixels per frame

    floorHeight: height of floor in pixels from bottom of screen
    platformsTouching: list of platforms that are colliding with the player
    '''
    def fall(self, floorHeight, platformsTouching):
        #test if player is above floor level to determine if grounded
        if self.rect.y + self.rect.height < 720 - floorHeight and platformsTouching == []:
            #falls by 5 pixels per inch when not during jump animation
            self.rect.y += 5
    
    '''
    Updates position of enemy by falling and sideways movement depending on velocity

    floorHeight: height of floor in pixels from bottom of screen
    screenSize: (width, height) of game screen
    platformsTouching: list of platforms that are colliding with the player
    '''
    def update(self, floorHeight, screenSize, platformsTouching):

        #walks left when reaches right boundary
        if self.rect.x + self.rect.width > screenSize[0]:
            self.walkLeft()

        #walks right when reaches left boundary
        elif self.rect.x < 0:
            self.walkRight()
        
        #updates horizontal position due to velocity
        self.rect.x += self.velocityX
        self.fall(floorHeight, platformsTouching)

class FlyingEnemy(pygame.sprite.Sprite):
    def __init__(self, spawn:tuple):
        super().__init__()
        #loads image as pygame Surface object
        self.image = pygame.image.load(os.path.join(("game_assets"), "mario.png"))
        self.image = pygame.transform.scale(self.image, (50, 70))
        self.rect = self.image.get_rect()
    
        #sets position to spawn
        self.rect.x = spawn[0]
        self.rect.y = spawn[1]

        self.velocityX = 0.0
        self.velocityY = 0.0

        self.x = spawn[0]
        self.y = spawn[1]

    def find_angle(self , player):
        #calculating change in x and y axis
        deltaX = player.rect.x - self.rect.x
        deltaY = player.rect.y - self.rect.y
        
        if deltaX == 0:
            deltaX = 1 

        angle = atan(deltaY/deltaX)

        if deltaX < 0:
            angle += pi

        return angle
    
    def update(self, player):
        angle = self.find_angle(player) 
        
        self.velocityX = 1 * cos(angle)
        self.velocityY = 1 * sin(angle)
        
        self.x += self.velocityX
        self.y += self.velocityY
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
