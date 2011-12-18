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

import copy

EMPTY = 0
HORIZONTAL = 1
VERTICAL = 2
BOTH = 3

class WallLayout:
    """
    This stores the layout of walls during a session. We represent
    this by vertices and whether a vertex has a wall going either
    horizontal or vertical or if it is empty. Walls always go from
    lower indices to higher indices.
    """
    def __init__(self):
        pass
    
    def load_empty(self, map_size):
        width, height = map_size
        self.wall_layout = []
        for x in range(width):
            row = []
            for y in range(height):
                row.append(EMPTY)
            self.wall_layout.append(row)

    def get_layout(self):
        return copy.deepcopy(self.wall_layout)

    def load_textfile(self, filename):
        # Load a text file to define wall layout
        text_file = open(filename, 'r')
        self.wall_layout = []
        for line in text_file:
            row = []
            for character in line:
                if character == '0':
                    row.append(EMPTY)
                elif character == '|':
                    row.append(VERTICAL)
                elif character == '-':
                    row.append(HORIZONTAL)
                elif character == '+':
                    row.append(BOTH)
                elif character == '\n':
                    continue
                else:
                    print "Unexpected character in text file: ", character
                    raise BaseException
            self.wall_layout.append(row)