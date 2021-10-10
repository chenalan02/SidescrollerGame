from map_creation_tool import create_map, edit_map
from map import Map

if __name__ == "__main__":
    create_map('map1', True, 'forest.jpg', "universe.jpg", "night_sky.jpg", 'cityskyline.jpg')

    '''
    map = Map()
    map.load_map('map1.json')
    edit_map(map, 'map1_edited.json', True)
    '''