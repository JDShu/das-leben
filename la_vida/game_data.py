import os
import house_objects
import wall_layout
import floor_layout

class GameData:
    def __init__(self, filename):
        self.object_catalog = load_objects_data(filename)
        self.wall_data = load_wall_data(filename)
        self.floor_data = load_floor_data(filename)

def load_objects_data(filename):
    house_data = house_objects.ObjectCatalog()
    house_data.load_textfile(os.path.join("data","games",filename + ".objects"))
    return house_data.get_catalog()

def load_wall_data(filename):
    wall_data = wall_layout.WallLayout()
    wall_data.load_textfile(os.path.join("data","games",filename + ".wall"))
    return wall_data.get_layout()
    
def load_floor_data(filename):
    floor_data = floor_layout.FloorLayout()
    floor_data.load_textfile(os.path.join("data","games",filename + ".floor"))
    return floor_data.get_layout()
