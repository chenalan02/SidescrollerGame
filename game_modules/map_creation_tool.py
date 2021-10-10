import os
import sys
import pygame

from map import Map
from section import Section
from player import Player
from terrain import Platform, Portal
from enemies import WalkingEnemy, FlyingEnemy, Spikes

SCREEN_SIZE = (1280, 720)
FLOOR_HEIGHT = 50

'''
starts map creator tool if mapName doesnt exist

overwrite: bool for whether the named file is to be overwritten if it already exists
*backgroundFileNames: args for each section to be made
mapName: name of map
'''
def create_map(mapName, overwrite:bool, *backgroundFileNames):
    #shows error message if the file name already exits

    #only proceeds with map creation if the file doesnt already exit or if it is to be overwritten
    savePath = os.path.join('game_assets', 'maps', mapName+'.json')
    if not os.path.exists(savePath) or overwrite == True:
        #test if all paths are valid
        backgroundPaths = list(map(lambda x:os.path.join('game_assets', 'backgrounds', x), backgroundFileNames))
        validPaths = list(map(lambda x:os.path.exists(x), backgroundPaths))
        if all(validPaths):

            pygame.init()
            pygame.display.set_caption('Map Creator')
            screen = pygame.display.set_mode(SCREEN_SIZE)

            #current and total number of sections
            numSections = len(backgroundFileNames)
            currentSection = 1
            createdMap = Map()

            #creates a section and adds content for each file name
            for backgroundFileName in backgroundFileNames:
                section = init_section(backgroundFileName, screen, numSections, currentSection)
                add_platforms(screen, section, numSections, currentSection)
                add_spikes(screen, section, numSections, currentSection)
                add_walking_enemies(screen, section, numSections, currentSection)
                add_flying_enemies(screen, section, numSections, currentSection)
                createdMap.add_section(section)
                currentSection += 1

            #saves the map to a json file
            createdMap.save_map(mapName+".json")

        else:
            print("One or more of the background file names are invalid")
    else:
        print("This file already exits. To overwrite it, set overwrite parameter to True")

def edit_map(map, mapFileName, overwrite:bool):

    savePath = os.path.join('game_assets', 'maps', mapFileName)
    if not os.path.exists(savePath) or overwrite == True:

        #current and total number of sections
        numSections = len(map.sections)
        currentSection = 1

        #creates a section and adds content for each file name
        for section in map.sections:
            add_platforms(map.screen, section, numSections, currentSection)
            add_spikes(map.screen, section, numSections, currentSection)
            add_walking_enemies(map.screen, section, numSections, currentSection)
            add_flying_enemies(map.screen, section, numSections, currentSection)
            currentSection += 1

        #saves the map to a json file
        map.save_map(mapFileName+".json")

    else:
        print("This file already exits. To overwrite it, set overwrite parameter to True")

'''
shows background of a section until spawn and exit portal positions are chosen, then returns section object

backgroundFileName: file name of background
screen: pygame screen surface
numSections: number of sections to be created
currentSection: number of current section being created
'''    
def init_section(backgroundFileName, screen, numSections, currentSection):
    spawnPortalPos = None
    exitPortalPos = None

    background = pygame.image.load(os.path.join('game_assets', 'backgrounds', backgroundFileName))
    background = pygame.transform.scale(background, SCREEN_SIZE)

    #creates a sprite to hover around the mouse for more accurate placement
    portalMouseHover = Portal((0,0))
    ground = pygame.image.load(os.path.join('game_assets', "ground.jpg"))

    done = False
    while not done:
        mousePos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            #creates a portal when mouse clicked
            if event.type==pygame.MOUSEBUTTONDOWN:
                if spawnPortalPos == None:
                    spawnPortalPos = mousePos
                else:
                    exitPortalPos = mousePos
                    done = True
            #ends program when window closed
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

        #displays background
        screen.blit(background, (0,0))
        #displays instruction
        if spawnPortalPos == None:
            display_message(screen, "Click to add Spawn Portal")
        else:
             display_message(screen, "Click to add Exit Portal")
        #displays section number
        display_section_num(screen, numSections, currentSection)

        screen.blit(ground, (0, SCREEN_SIZE[1] - FLOOR_HEIGHT))
        screen.blit(portalMouseHover.image, mousePos)
        if spawnPortalPos != None:
            screen.blit(portalMouseHover.image, spawnPortalPos)

        pygame.display.flip()

    del portalMouseHover
    return Section(backgroundFileName, spawnPortalPos, exitPortalPos)

'''
function to add platforms to asection
shows contents of section until space is pressed, click twice to create a platform

section: section object
screen: pygame screen surface
numSections: number of sections to be created
currentSection: number of current section being created
'''  
def add_platforms(screen, section, numSections, currentSection):

    leftEnd = None
    rightEnd = None
    done = False
    while not done:

        for event in pygame.event.get():
            #specifies a end of the platform when clicked
            if event.type==pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if leftEnd == None:
                    leftEnd = mousePos
                else:
                    rightEnd = mousePos
                    #determines which point is the left and right
                    if leftEnd[0] > rightEnd[0]:
                        temp = leftEnd
                        leftEnd = rightEnd
                        rightEnd = temp
                    #adds a platform based on 2 edges specified
                    section.add_platform(coordinates= leftEnd, length= rightEnd[0]-leftEnd[0])
                    leftEnd = None
                    rightEnd = None

            #ends platform adding process when space pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True

            #ends program when window closed    
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

        section.draw(screen)
        #displays instructions and section number
        display_message(screen, "Add Platforms by clicking both sides. Press Space to finish")
        display_section_num(screen, numSections, currentSection)
        pygame.display.flip()


def add_spikes(screen, section, numSections, currentSection):
    #creates a sprite to hover around the mouse for more accurate placement
    spikesMouseHover = Spikes((0,0))

    done = False
    while not done:
        mousePos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            #specifies a end of the platform when clicked
            if event.type==pygame.MOUSEBUTTONDOWN:
                section.add_spikes(mousePos)

            #ends enemy adding process when space pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True

            #ends program when window closed    
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

        section.draw(screen)
        screen.blit(spikesMouseHover.image, mousePos)
        #displays instructions and section number
        display_message(screen, "Click to add spikes. Press Space to finish")
        display_section_num(screen, numSections, currentSection)
        pygame.display.flip()
    
    del spikesMouseHover

'''
add walking enemies to a section
shows contents of section until space is pressed, click to place a walking enemy

section: section object
screen: pygame screen surface
numSections: number of sections to be created
currentSection: number of current section being created
'''  
def add_walking_enemies(screen, section, numSections, currentSection):
    #creates a sprite to hover around the mouse for more accurate placement
    enemyMouseHover = WalkingEnemy((0,0))

    done = False
    while not done:
        mousePos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            #specifies a end of the platform when clicked
            if event.type==pygame.MOUSEBUTTONDOWN:
                section.add_walking_enemy(mousePos)

            #ends enemy adding process when space pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True

            #ends program when window closed    
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

        section.draw(screen)
        screen.blit(enemyMouseHover.image, mousePos)
        #displays instructions and section number
        display_message(screen, "Add walking enemies. Press Space to finish")
        display_section_num(screen, numSections, currentSection)
        pygame.display.flip()
    
    del enemyMouseHover
    
'''
add flying enemies to a section
shows contents of section until space is pressed, click to place a flying enemy

section: section object
screen: pygame screen surface
numSections: number of sections to be created
currentSection: number of current section being created
'''  
def add_flying_enemies(screen, section, numSections, currentSection):
    #creates a sprite to hover around the mouse for more accurate placement
    enemyMouseHover = FlyingEnemy((0,0))

    done = False
    while not done:
        mousePos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            #specifies a end of the platform when clicked
            if event.type==pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                section.add_flying_enemy(mousePos)
        
            #ends enemy adding process when space pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True

            #ends program when window closed
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

        section.draw(screen)
        screen.blit(enemyMouseHover.image, mousePos)
        #displays instructions and section number
        display_message(screen, "Add flying enemies. Press Space to finish")
        display_section_num(screen, numSections, currentSection)
        pygame.display.flip()
    
    del enemyMouseHover

'''
displays a message on top left of screen

message: the message to be shown
'''  
def display_message(screen, message):
    font= pygame.font.SysFont('Calibri', 40, True, False)
    text= font.render(message, True, (0,0,0))
    screen.blit(text, [5,1])

'''
displays the current section and total number of sections

screen: screen object
numSections: number of sections to be created
currentSection: number of current section being created
'''  
def display_section_num(screen, numSections, currentSection):
    font= pygame.font.SysFont('Calibri', 40, True, False)
    text= font.render("Section " + str(currentSection) + " of " + str(numSections), True, (0,0,0))
    screen.blit(text, [5,40])
