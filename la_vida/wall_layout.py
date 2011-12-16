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
