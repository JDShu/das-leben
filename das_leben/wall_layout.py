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

EMPTY = 0
HORIZONTAL = 1
VERTICAL = 2
POINT = 3
OPEN_POINT = 4

class WallLayout:
    """
    This stores the layout of walls during a session. We represent
    this by vertices and whether a vertex has a wall going either
    horizontal or vertical or if it is empty. Walls always go from
    lower indices to higher indices.
    """

    def load_empty(self, map_size):
        self.layout = []
        for x in range(self.width):
            row = []
            for y in range(self.height):
                row.append(EMPTY)
            self.layout.append(row)        

    def load_textfile(self, filename):
        # Load a text file to define wall layout
        wall_file = open(filename, 'r')
        self.layout = []
        for line in wall_file:
            row = []
            for character in line:
                if character == '0':
                    row.append(EMPTY)
                elif character == '|':
                    row.append(VERTICAL)
                elif character == '-':
                    row.append(HORIZONTAL)
                elif character == '+':
                    row.append(POINT)
                elif character == '*':
                    row.append(OPEN_POINT)
                elif character == '\n':
                    continue
                else:
                    print "Unexpected character in text file: ", character
                    raise BaseException
            row.append(EMPTY)
            self.layout.append(row)
        self.layout.append([EMPTY]*len(self.layout[0]))
        wall_file.close()
