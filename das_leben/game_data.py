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

import os

import house_objects
import wall_layout
import floor_layout
import characters

SAVE_DIRECTORY = os.path.join("data","games")

def load_objects_data(filename):
    house_data = house_objects.ObjectCatalog()
    filepath = os.path.join(SAVE_DIRECTORY, filename + ".objects")
    house_data.load_textfile(filepath)
    return house_data.get_catalog()


def load_wall_data(filename):
    wall_data = wall_layout.WallLayout()
    filepath = os.path.join(SAVE_DIRECTORY, filename + ".wall")
    wall_data.load_textfile(filepath)
    return wall_data

    
def load_floor_data(filename):
    floor_data = floor_layout.FloorLayout()
    filepath = os.path.join(SAVE_DIRECTORY, filename + ".floor")
    floor_data.load_textfile(filepath)
    return floor_data

def load_characters_data(filename):
    character_data = characters.CharacterCatalog()
    filepath = os.path.join(SAVE_DIRECTORY, filename + "_characters.json")
    character_data.load_textfile(filepath)
    return character_data

class GameData:
    """
    Stores the game state. Any changes to the game must call a function
    from this class. For now, this is the ONLY class that should call
    messenger methods.
    """
    def __init__(self, filename):
        self.floor_data = load_floor_data(filename)
        self.map_dimensions = self.floor_data.dimensions
        self.map_width, self.map_height = self.map_dimensions
        self.object_catalog = load_objects_data(filename)
        self.wall_data = load_wall_data(filename)
        self.character_catalog = load_characters_data(filename)

        self.selected_character = None

    def select_character(self, character_id):
        self.selected_character = character_id
        messenger.send('SelectCharacter', [character_id])

    def click_point(self, coords):
        if self.selected_character != None:
            messenger.send('MoveCharacter', [self.selected_character, coords])

    def step_character(self, character_id, next_node):
        messenger.send('StepCharacter', [character_id, next_node])
