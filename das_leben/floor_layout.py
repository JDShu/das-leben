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

GRASS = 0
WOOD = 1

class FloorLayout:
    """
    This stores the layout of floor tiles during a session. We represent
    this by squares and what each square is.
    """

    def load_empty(self, map_size):
        self.dimensions = self.width, self.height = map_size
        width, height = map_size
        self.layout = []
        for x in range(width):
            row = []
            for y in range(height):
                row.append(EMPTY)
            self.layout.append(row)

    def load_textfile(self, filename):
        # Load a text file to define floor layout
        floor_file = open(filename, 'r')
        self.layout = []
        for line in floor_file:
            row = []
            for character in line:
                if character == 'G':
                    row.append(GRASS)
                elif character == 'W':
                    row.append(WOOD)
                elif character == '\n':
                    continue
                else:
                    print "Unexpected character in text file: ", character
                    raise BaseException
            self.layout.append(row)
        floor_file.close()
        self.width = len(self.layout)
        self.height = len(self.layout[0])
        self.dimensions = self.width, self.height
