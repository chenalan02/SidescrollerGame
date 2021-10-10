from map import Map
from section import Section
from map_creation_tool import edit_map

if __name__ == "__main__":
    map = Map()
    map.load_map('map1.json')
 
    done = False
    while not done:
        done = map.update()
