import os
import json
import pygame

from player import Player
from section import Section
from terrain import Platform
from enemies import *

SCREEN_SIZE = (1280, 720)
FLOOR_HEIGHT = 50

'''
Class for a map or level as a whole
each map has multiple sections that the player can travel between

fps: frames per second limit of the game
'''
class Map():
    def __init__ (self):
        #list of sections
        self.sections = []
        #current section index
        self.currentSection = 0

        #sets screen size
        self.screenSize = SCREEN_SIZE
        #game fps
        self.fps = 200

        self.player = Player()
        #pygame sprite list required for printing and collision detection
        self.playersList = pygame.sprite.Group()
        self.playersList.add(self.player)

        #pygame setup
        pygame.init()
        pygame.display.set_caption('Side Scroller')
        self.screen = pygame.display.set_mode(self.screenSize)
        self.clock = pygame.time.Clock()

    '''
    draws current section and player
    '''
    def draw(self):
        self.sections[self.currentSection].draw(self.screen)
        self.playersList.draw(self.screen)

    '''
    check if player touched the exit portal

    player: player object
    '''
    def check_exit(self, player):
        currentSection = self.sections[self.currentSection]
        if pygame.sprite.collide_rect(player, currentSection.exitPortal):
            return True
        else:
            return False

    '''
    changes the section of the map to the next one
    '''
    def change_section(self):
        self.currentSection += 1
        if self.currentSection >= len(self.sections):
            self.game_win()

        self.sections[self.currentSection].start_section(self.player)

    '''
    restarts game when the game is over
    TO CHANGE MAYBE
    '''
    def game_win(self):
        self.restart_game()

    '''
    checks if the player has died by colliding with an enemy or hazard
    '''
    def check_death(self):
        if pygame.sprite.spritecollide(self.player, self.sections[self.currentSection].enemies, False) != []:
            self.restart_game()


    '''
    restarts the game
    '''
    def restart_game(self):
        #resets current section to the first
        self.currentSection = 0
        #restarts all enemy objects in every section to their default/spawn states
        for section in self.sections:
            for enemy in section.enemies:
                enemy.reinitialize()

        #restarts the map at the first section
        self.start()

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

        #updates all walking enemies
        for enemy in self.sections[self.currentSection].enemies:
            platformsTouching = pygame.sprite.spritecollide(enemy, self.sections[self.currentSection].platforms, False)
            enemy.update(floorHeight=FLOOR_HEIGHT, screenSize=SCREEN_SIZE, platformsTouching=platformsTouching, player=self.player)

        #checks if the player has touched the exit portal to change sections
        if self.check_exit(self.player):
            self.change_section()

        #checks if the player has died
        self.check_death()

        #draws map
        self.draw()
        #sets constant fps
        self.clock.tick(self.fps)
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
    def start(self):
        self.sections[0].start_section(self.player)

    '''
    changes fps of the map
    '''
    def change_fps(self, fps):
        self.fps = fps

    '''
    saves the map to a json file in the game_assets/maps folder

    fileName: name of the file including .json tag
    '''
    def save_map(self, fileName):
        map = {}
        sectiondict = {}

        for section in self.sections:
            sectiondict = {}

            backgroundFileName = section.backgroundFileName
            sectiondict["backgroundFileName"] = backgroundFileName

            spawnPortal = section.spawnPortal.rect.topleft
            sectiondict["spawnPortal"] = spawnPortal
            exitPortal = section.exitPortal.rect.topleft
            sectiondict["exitPortal"] = exitPortal

            enemies = [(enemy.rect.topleft, enemy.type) for enemy in section.enemies]
            sectiondict["enemies"] = enemies

            platforms = [(platform.rect.topleft, platform.length) for platform in section.platforms]
            sectiondict["platforms"] = platforms

            key = self.sections.index(section)+1
            map[key] = sectiondict

        path = os.path.join('game_assets', 'maps', fileName)
        with open(path, 'w') as file:
            json.dump(map, file)

    '''
    loads a map saved to a json file in the game_assets/maps folder

    fileName: name of the file including .json tag
    '''
    def load_map(self, fileName):

        path = os.path.join('game_assets', 'maps', fileName)
        with open(path, 'r') as file:
            map = json.load(file)
            
            for section in map.values():
                sectionToAdd = Section(section['backgroundFileName'], section['spawnPortal'], section['exitPortal'])

                for enemy in section['enemies']:
                    if enemy[1] == 'walking':
                        sectionToAdd.add_walking_enemy(enemy[0])
                    if enemy[1] == 'flying':
                        sectionToAdd.add_flying_enemy(enemy[0])
                    if enemy[1] == 'spikes':
                        sectionToAdd.add_spikes(enemy[0])

                for platform in section['platforms']:
                    sectionToAdd.add_platform(platform[0], platform[1])

                self.add_section(sectionToAdd)