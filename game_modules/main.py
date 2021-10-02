import pygame
from map import Map, Section

if __name__ == "__main__":
    map = Map()
    map.add_section(backgroundFileName='forest_background.jpg', spawnPoint=(0,0))

    done = False
    while not done:
        done = map.update()