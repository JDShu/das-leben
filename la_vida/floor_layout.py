import copy

GRASS = 0
WOOD = 1

class FloorLayout:
    """
    This stores the layout of walls during a session. We represent
    this by squares and what each square is.
    """
    def __init__(self):
        pass
    
    def load_empty(self, map_size):
        width, height = map_size
        self.floor_layout = []
        for x in range(width):
            row = []
            for y in range(height):
                row.append(EMPTY)
            self.floor_layout.append(row)

    def get_layout(self):
        return copy.deepcopy(self.floor_layout)

    def load_textfile(self, filename):
        # Load a text file to define wall layout
        text_file = open(filename, 'r')
        self.floor_layout = []
        for line in text_file:
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
            self.floor_layout.append(row)
