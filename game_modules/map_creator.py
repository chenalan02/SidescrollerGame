import os
import json
import pygame
from map import Map
from section import Section

SCREEN_SIZE = (1280, 720)
FLOOR_HEIGHT = 50

def create_map(mapName, *backgroundFileNames):

    pygame.init()
    pygame.display.set_caption('Map Creator')
    screen = pygame.display.set_mode(SCREEN_SIZE)

    numSections = len(backgroundFileNames)
    currentSection = 1
    map = Map()

    for backgroundFileName in backgroundFileNames:
        section = init_section(backgroundFileName, screen, numSections, currentSection)
        add_platforms(screen, section, numSections, currentSection)
        add_walking_enemies(screen, section, numSections, currentSection)
        add_flying_enemies(screen, section, numSections, currentSection)
        map.add_section(section)
        
def init_section(backgroundFileName, screen, numSections, currentSection):
    spawnPortalPos = None
    exitPortalPos = None
    background = pygame.image.load(os.path.join('game_assets', 'backgrounds', backgroundFileName))
    background = pygame.transform.scale(background, SCREEN_SIZE)
    done = False
    while not done:

        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if spawnPortalPos == None:
                    spawnPortalPos = mousePos
                else:
                    exitPortalPos = mousePos
                    done = True

            if event.type == pygame.QUIT: 
                return True

        screen.blit(background, (0,0))
        if spawnPortalPos == None:
            display_message(screen, "Add Spawn Portal")
        else:
             display_message(screen, "Add Exit Portal")
        display_section_num(screen, numSections, currentSection)
        pygame.display.flip()

    return Section(backgroundFileName, spawnPortalPos, exitPortalPos)

def add_platforms(screen, section, numSections, currentSection):

    leftEnd = None
    rightEnd = None
    done = False
    while not done:

        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if leftEnd == None:
                    leftEnd = mousePos
                else:
                    rightEnd = mousePos
                    section.add_platform(coordinates= leftEnd, length= rightEnd[0]-leftEnd[0])
                    leftEnd = None
                    rightEnd = None
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True
                
            if event.type == pygame.QUIT: 
                return True

        section.draw(screen)
        display_message(screen, "Add Platform by clicking twice for left and right ends. Press Space to finish")
        display_section_num(screen, numSections, currentSection)
        pygame.display.flip()

def add_walking_enemies(screen, section, numSections, currentSection):

    done = False
    while not done:

        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                section.add_walking_enemy(mousePos)
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True
                
            if event.type == pygame.QUIT: 
                return True

        section.draw(screen)
        display_message(screen, "Add walking enemies. Press Space to finish")
        display_section_num(screen, numSections, currentSection)
        pygame.display.flip()
    
def add_flying_enemies(screen, section, numSections, currentSection):

    done = False
    while not done:

        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                section.add_flying_enemy(mousePos)
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True

            if event.type == pygame.QUIT: 
                return True

        section.draw(screen)
        display_message(screen, "Add flying enemies. Press Space to finish")
        display_section_num(screen, numSections, currentSection)
        pygame.display.flip()

def display_message(screen, message):
    font= pygame.font.SysFont('Calibri', 40, True, False)
    text= font.render(message, True, (0,0,0))
    screen.blit(text, [5,1])

def display_section_num(screen, numSections, currentSection):
    font= pygame.font.SysFont('Calibri', 40, True, False)
    text= font.render("Section " + str(currentSection) + " of " + str(numSections), True, (0,0,0))
    screen.blit(text, [5,40])

if __name__ == "__main__":
    create_map("map1", "forest.jpg", "forest.jpg")