'''
* This file is part of Das Leben.
* Copyright (C) 2011 Hans Lo
*
* Das Leben is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* Das Leben is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Das Leben.  If not, see <http://www.gnu.org/licenses/>.
'''

import copy

class ObjectCatalog:

    def __init__(self):
        self.data = {}
        self.object_id = 0

    def add(self, house_object):
        self.data[self.object_id] = house_object
        self.object_id += 1

    def get_catalog(self):
        return copy.deepcopy(self.data)

    def  load_textfile(self, filepath):
        object_file = open(filepath, 'r')
        for line in object_file:
            object_data = line.split(" ")
            object_name = object_data[0]
            x_coord = int(object_data[1])
            y_coord = int(object_data[2])
            new_house_object = HouseObject(object_name, (x_coord,y_coord))
            self.add(new_house_object)
        object_file.close()
        
class HouseObject:
    def __init__(self, name, map_coords):
        self.name = name
        self.map_coords = map_coords
