from typing import Tuple
import pygame
import math
import os
from player import Player
from terrain import Platform
import time
from enemies import Enemy , FlyingEnemy

SCREEN_SIZE = (1280, 720)
FLOOR_HEIGHT = 50

'''
Class for a single section of the whole map

backgroundFileName = file name of the background
player = player object
spawnPoint = (x, y) coordinates for player to be spawned
'''
class Section():
    def __init__ (self, backgroundFileName, spawnPoint: tuple):
        #load background as pygame Surface object
        self.background = pygame.image.load(os.path.join('game_assets', backgroundFileName))
        self.background = pygame.transform.scale(self.background, SCREEN_SIZE)
        self.spawnPoint = spawnPoint
        #sets player pos to spawnpoint
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.flyingEnemies = pygame.sprite.Group()

    '''
    initializes section by changing character position to the section's spawn

    player: the player object
    '''
    def start_section(self, player: Player,):
        player.rect.x = self.spawnPoint[0]
        player.rect.y = self.spawnPoint[1]

    '''
    adds a platform to the map

    coordinates: (x, y) of the top left of the platform
    length: length of the platform
    '''
    def add_platform(self, coordinates:tuple, length):
        self.platforms.add(Platform(coordinates, length))

    '''
    adds an enemy to the map

    spawn: (x, y) spawnpoint for the top left of the enemy model
    '''
    def add_enemy(self, spawn):
        enemy = Enemy(spawn)
        self.enemies.add(enemy)

    def add_flying_enemy(self, spawn):
        enemy = FlyingEnemy(spawn)
        self.flyingEnemies.add(enemy)

    '''
    draws section

    screen: pygame screen object
    '''
    def draw(self, screen):
        screen.blit(self.background, (0,0))
        self.platforms.draw(screen)
        self.enemies.draw(screen)
        self.flyingEnemies.draw(screen)

'''
Class for a map or level as a whole
each map has multiple sections that the player can travel between

FPS: frames per second limit of the game
'''
class Map():
    def __init__ (self, FPS):
        #list of sections
        self.sections = []
        #current section index
        self.currentSection = 0

        #sets screen size
        self.screenSize = SCREEN_SIZE
        #game fps
        self.FPS = FPS

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

            #when a key is released
            if event.type == pygame.KEYUP:
                #stops movement in left direction when the left key is released
                if event.key==pygame.K_LEFT:
                    self.player.stopLeft()
                #stops movement in right direction when the right key is released
                elif event.key==pygame.K_RIGHT:
                    self.player.stopRight()
            
            #when a key is pressed down
            if event.type == pygame.KEYDOWN:
                #player movement in x axis using left and right arrow keys
                if event.key==pygame.K_LEFT:
                    self.player.walkLeft()
                elif event.key==pygame.K_RIGHT:
                    self.player.walkRight()
                #player jumps when spacebar
                if event.key == pygame.K_SPACE:
                    self.player.startJump()

            #quits game if x clicked on top right of screen
            if event.type == pygame.QUIT: 
                return True

        #updates player
        platformsTouching = pygame.sprite.spritecollide(self.player, self.sections[self.currentSection].platforms, False)
        self.player.update(FLOOR_HEIGHT, SCREEN_SIZE, platformsTouching)

        #updates all enemies
        for enemy in self.sections[self.currentSection].enemies:
            platformsTouching = pygame.sprite.spritecollide(enemy, self.sections[self.currentSection].platforms, False)
            enemy.update(FLOOR_HEIGHT, SCREEN_SIZE, platformsTouching)

        for flyingEnemy in self.sections[self.currentSection].flyingEnemies:
            platformsTouching = pygame.sprite.spritecollide(flyingEnemy, self.sections[self.currentSection].platforms, False)
            flyingEnemy.update(self.player)

        #draws map
        self.draw()
        #sets constant fps
        self.clock.tick(self.FPS)
        #updates screen
        pygame.display.flip()

    '''
    adds a section to the map
    '''
    def add_section(self, section):
        self.sections.append(section)

    '''
    starts/initializes the map and first section
    '''
    def map_start(self):
        self.sections[0].start_section(self.player)


    