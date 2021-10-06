import pygame
import math
import os

'''
Class for player object

coordinates: (x, y) position of the top left of the player model
'''
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #loads image as pygame Surface object
        self.image = pygame.image.load(os.path.join(("game_assets"), "mario.png"))
        self.image = pygame.transform.scale(self.image, (50, 70))

        #rect = [left, top, width, height]
        self.rect = self.image.get_rect()

        #rect.x refers to left, rect.y refers to top
        self.velocityX = 0
        #boolean for whether the player is grounded
        self.grounded = False

        #boolean for whether the player is currently in a jump animation
        self.jump_bool = False
        #pixel values for addition to y value for each frame in the jump animation
        self.jumpList = [15, 15, 10, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                        1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -3, -3, -3, -3, -4, -4, -4, -4]
        #index in the current jump animation list
        self.jumpIndex = 0

    '''
    Methods to walk left and right by changing velocity
    '''
    def walkLeft(self):
        self.velocityX = -3

    def walkRight(self):
        self.velocityX = 3

    '''
    Method to stop walking by resetting velocity to 0
    specific to directions since we do not want to stop moving right when the player let go of the left key
    '''
    def stopLeft(self):
        if self.velocityX < 0:
            self.velocityX = 0


    def stopRight(self):
        if self.velocityX > 0:
            self.velocityX = 0

    '''
    Method to start a jump animation
    '''
    def startJump(self):
        #only start a jump when grounded
        if self.grounded:
            self.jump_bool = True

    '''
    Method to perform jump animation
    adds to y value of player from a predefined list of values 
    '''
    def jump(self):
        #adds to y value if during jump animation
        if self.jump_bool == True:
            self.rect.y -= self.jumpList[self.jumpIndex]
            self.jumpIndex += 1

            #end of jump animation
            if self.jumpIndex > len(self.jumpList) - 1:
                self.jump_bool = False
                self.jumpIndex = 0

    '''
    Method to fall at a constant rate of 5 pixels per frame

    floorHeight: height of floor in pixels from bottom of screen
    platformsTouching: list of platforms that are colliding with the player
    '''
    def fall(self, floorHeight, platformsTouching):
        #test if player is above floor level to determine if grounded
        if self.rect.y + self.rect.height < 720 - floorHeight and platformsTouching == []:
            #falls by 5 pixels per inch when not during jump animation
            if not self.jump_bool:
                self.rect.y += 5
            self.grounded = False
        #grounded when not above floor
        else:
            self.grounded = True
        
    '''
    Updates position of player by falling and sideways movement depending on velocity

    floorHeight: height of floor in pixels from bottom of screen
    screenSize: (width, height) of game screen
    platformsTouching: list of platforms that are colliding with the player
    '''
    def update(self, floorHeight, screenSize, platformsTouching):
        self.fall(floorHeight, platformsTouching)
        #does not allow player to leave boundaries of screen
        if self.rect.x + self.rect.width > screenSize[0]:
            self.rect.x = screenSize[0] - self.rect.width
        elif self.rect.x < 0:
            self.rect.x = 0

        self.jump()
        self.rect.x += self.velocityX 
    

    

    

    
    
