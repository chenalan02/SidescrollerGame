import os
import pygame

from player import Player
from terrain import Platform, Portal
from enemies import WalkingEnemy, FlyingEnemy, Spikes

SCREEN_SIZE = (1280, 720)
FLOOR_HEIGHT = 50

'''
Class for a single section of the whole map

backgroundFileName: file name of the background
player: player object
spawnPoint: (x, y) coordinates for player to be spawned
'''
class Section():
    def __init__ (self, backgroundFileName, spawnPoint: tuple, exitPortalPos: tuple):
        #load background as pygame Surface object
        
        self.background = pygame.image.load(os.path.join('game_assets', 'backgrounds', backgroundFileName))
        self.background = pygame.transform.scale(self.background, SCREEN_SIZE)

        self.ground = pygame.image.load(os.path.join('game_assets', "ground.jpg"))

        #saves background file name for map saving purposes
        self.backgroundFileName = backgroundFileName

        #pygame groups for sprites
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        #creates portal objects for spawn and exit of section
        self.spawnPortal = Portal(spawnPoint)
        self.exitPortal = Portal(exitPortalPos)
        self.portals = pygame.sprite.Group(self.spawnPortal, self.exitPortal) 

    '''
    initializes section by changing character position to the section's spawn

    player: the player object
    '''
    def start_section(self, player: Player,):
        player.rect.x = self.spawnPortal.rect.x
        player.rect.y = self.spawnPortal.rect.y

    '''
    adds a platform to the map

    coordinates: (x, y) of the top left of the platform
    length: length of the platform
    '''
    def add_platform(self, coordinates:tuple, length):
        self.platforms.add(Platform(coordinates, length))

    '''
    Methods to add walking enemies to the section

    spawn: (x, y) spawnpoint for the top left of the enemy model
    '''
    def add_walking_enemy(self, spawn):
        enemy = WalkingEnemy(spawn)
        self.enemies.add(enemy)

    def add_flying_enemy(self, spawn):
        enemy = FlyingEnemy(spawn)
        self.enemies.add(enemy)

    def add_spikes(self, spawn):
        enemy = Spikes(spawn)
        self.enemies.add(enemy)

    '''
    draws everything in the section

    screen: pygame screen object
    '''
    def draw(self, screen):
        screen.blit(self.background, (0,0))
        screen.blit(self.ground, (0, SCREEN_SIZE[1] - FLOOR_HEIGHT))
        self.platforms.draw(screen)
        self.enemies.draw(screen)
        self.portals.draw(screen)
