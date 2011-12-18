'''
* This file is part of La Vida.
* Copyright (C) 2011 Hans Lo
*
* La Vida is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* La Vida is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Touhou SRPG.  If not, see <http://www.gnu.org/licenses/>.
'''

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
