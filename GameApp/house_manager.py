class House:
    def __init__( self ):
        self.floors = [Floor(None)]

    def add_floor( self ):
        self.floors += [Floor(self.floors[-1])]
        
    def remove_floor( self ):
        self.floors.pop()
        
    def add_item_type(self, item, floor):
        self.floors[floor].add_item_type(item)

    def remove_item_type(self, item, floor):
        self.floors[floor].remove_item_type(item)

    #returns which floor the closest item exists or False if it doesn't exists anywhere.
    def item_exists(self, item, floor):
        distance = 0
        while distance < len(self.floors):
            if floor - distance >= 0 and self.floors[floor - distance].item_exists(item):
                return floor - distance
            if floor + distance < len(self.floors) and self.floors[floor + distance].item_exists(item):
                return floor + distance
            distance += 1
        return False

    def print_items( self ):
        x = 0
        for f in self.floors:
            print x, ":",
            for k in f.inventory:
                print k,
            print ""
            x += 1
                
            
class Floor:
    def __init__( self, lower):
        self.inventory = {}

    def set_upper(self, floor):
        self.upper = floor

    def add_item_type(self, item_type):
        self.inventory[item_type] = True
        
    def remove_item_type(self, item_type):
        if item_type in self.inventory:
            self.inventory[item_type] = False

    def item_exists( self, item_type):
        if item_type in self.inventory:
            return self.inventory[item_type]
        else:
            return False
