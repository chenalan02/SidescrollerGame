import pygame
import math
import os

'''
Class for player object

coordinates = (x, y)
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
        self.velocity = 0

        self.jump_bool = False
        self.jumpList = [30, 20, 20, 20, 15, 15, 15, 10, 10]
        self.jumpIndex = 0

    '''
    Method to walk left and right by changing velocity

    direction = "left" or "right"
    '''
    def walk(self, direction):
        if direction == 'left':
            self.velocity = -1
        elif direction == 'right':
            self.velocity = 1

    '''
    Method to stop walking by resetting velocity to 0
    '''
    def stop(self, direction):
        if direction == "right" and self.velocity > 0:
            self.velocity = 0
        elif direction == "left" and self.velocity < 0:
            self.velocity = 0

    '''
    Method to jump

    TO BE REVISED
    '''
    def startJump(self):
        self.jump_bool = True

    def jump(self):
        if self.jump_bool == True:
            self.rect.y -= self.jumpList[self.jumpIndex]
            self.jumpIndex += 1

            if self.jumpIndex > len(self.jumpList) - 1:
                self.jump_bool = False
                self.jumpIndex = 0

    '''
    Method to fall at a constant rate of 3 pixels per frame
    '''
    def fall(self, floorHeight):
        #falls by 3 pixels per inch when above floor
        if self.rect.y + self.rect.height < 720 - floorHeight and not self.jump_bool:
            self.rect.y += 2
        #sets height on floor when not above floor
        else:
            pass
            #self.rect.y = 720 - floorHeight - self.rect.height
        
    '''
    Updates position of player by falling and sideways movement depending on velocity
    '''
    def update(self, floorHeight, screenSize):
        self.fall(floorHeight)
        #does not allow player to leave boundaries of screen
        if self.rect.x + self.rect.width > screenSize[0]:
            self.rect.x = screenSize[0] - self.rect.width
        elif self.rect.x < 0:
            self.rect.x = 0

        self.jump()
        self.rect.x += self.velocity 
    

    

    

    
    
