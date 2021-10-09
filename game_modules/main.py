import pygame
from map import Map, Section

if __name__ == "__main__":
    map = Map(FPS=200)

    section = Section(backgroundFileName='forest_background.jpg', spawnPoint=(500,500))
    section.add_platform(coordinates=(700, 500), length=250)
    section.add_enemy(spawn=(700, 200))
    section.add_flying_enemy(spawn=(700, 200))
    map.add_section(section)
 
    


    map.map_start()

 
    done = False
    while not done:
        done = map.update()