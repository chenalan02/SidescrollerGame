import pygame
import math
import os
from player import Player
import time

SCREEN_SIZE = (1280, 720)
FLOOR_HEIGHT = 50

'''
Class for a single section of the whole map

backgroundFileName = file name of the background
player = player object
spawnPoint = (x, y) coordinates for player to be spawned
'''
class Section():
    def __init__ (self, backgroundFileName, player, spawnPoint):
        #load background as pygame Surface object
        self.background = pygame.image.load(os.path.join('game_assets', backgroundFileName))
        self.background = pygame.transform.scale(self.background, SCREEN_SIZE)
        #sets player pos to spawnpoint
        player.rect.x = spawnPoint[0]
        player.rect.y = spawnPoint[1]

    '''
    draws section

    screen = pygame screen object
    '''
    def draw(self, screen):
        screen.blit(self.background, (0,0))

'''
Class for a map or level as a whole
'''
class Map():
    def __init__ (self):
        #list of sections
        self.sections = []
        #current section index
        self.currentSection = 0

        #sets screen size
        self.screenSize = SCREEN_SIZE

        self.player = Player()
        #pygame sprite list required for printing and collision detection
        self.playersList = pygame.sprite.Group()
        self.playersList.add(self.player)

        #pygame setup
        pygame.init()
        pygame.display.set_caption('SideScroller')
        self.screen = pygame.display.set_mode(self.screenSize)
        self.clock = pygame.time.Clock()

    '''
    draws current section and player
    '''
    def draw(self):
        self.sections[self.currentSection].draw(self.screen)
        self.playersList.draw(self.screen)

    '''
    updates game frame by frame
    processes pygame events(keyboard inputs)
    '''
    def update(self):
        #event detection for keyboard input
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_LEFT:
                    self.player.stop(direction="left")
                elif event.key==pygame.K_RIGHT:
                    self.player.stop(direction="right")
            
            if event.type == pygame.KEYDOWN:
                #player movement in x axis using left and right arrow keys
                if event.key==pygame.K_LEFT:
                    self.player.walk(direction="left")
                elif event.key==pygame.K_RIGHT:
                    self.player.walk(direction="right")
                #player jumps when spacebar
                if event.key == pygame.K_SPACE:
                    self.player.startJump()

            #quits game if x clicked on top right of screen
            if event.type == pygame.QUIT: 
                return True

        #updates player
        self.player.update(FLOOR_HEIGHT, SCREEN_SIZE)
        #draws map
        self.draw()
        #updates screen
        time.sleep(0.005)
        pygame.display.flip()

    '''
    adds a section to the map
    '''
    def add_section(self, backgroundFileName, spawnPoint):
        section = Section(backgroundFileName, self.player, spawnPoint)
        self.sections.append(section)


    