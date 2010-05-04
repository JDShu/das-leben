import pygame
from heapq import heappush, heappop

MOUSE = 1
TIME = 2

class Event():
    def __init__( self, category ):
        self.category = category        

class MouseEvent( Event ):
    def __init__( self, pygame_event ):
        Event.__init__( self, MOUSE )
        self.x, self.y = pygame.mouse.get_pos()
        self.l_click, self.m_click, self.r_click = pygame.mouse.get_pressed()
        self.s_up = False
        self.s_down = False
        
        if pygame_event.button == 4:
            self.s_up = True
        if pygame_event.button == 5:
            self.s_down = True

class TimeEvent( Event ):
    def __init__( self ):
        Event.__init__( self, TIME )

class Node():
    def __init__( self, x, y ):
        self.x = x
        self.y = y
        self.open = True
        
    def open_node( self ):
        self.open = True

    def close_node( self ):
        self.open = False
        
    def set_parent( self, parent ):
        self.parent = parent

    def set_g( self, g_cost ):
        self.g = g_cost

    def set_value( self ):
        self.value = self.g + h_function( self )

    def h_function( self, end):
        return abs( end[0] - self.x) + abs(end[1] - self.y )

    def print_coordinates( self ):
        print ( x, y )

BLOCKED = 1
#2D list data structure for pathfinding
class Grid():
    def __init__( self , width=20, height=20):

        self.grid = []
        self.width = width
        self.height = height
        for x in xrange(width):
            line = []
            for y in xrange(height):
                line.append( None )
            self.grid.append( line )

    def insert_block( self, x, y ):
        self.grid[x][y] = BLOCKED

    def insert_node( self, x, y, node):
        self.grid[x][y] = node
        
    def print_grid( self ):
        for y in xrange(self.width):
            print self.grid[y]
            
    def draw_path( self, path ):
        for sq in path:
            self.grid[sq[0]][sq[1]] = "X"
        self.print_grid()

#generates list of grid coordinates leading from goal to start according to a simple A* algorithm
class Path():
    def __init__( self, input_grid, start, goal ):
        self.start = start
        self.goal = goal
        self.grid = input_grid
        start_node = Node(*start)
        start_node.set_g(0)
        self.grid.insert_node(start[0], start[1], start_node)
        heap = []
        heappush( heap, (0,start) )
        current = heappop(heap)[1]        
        while current != goal:
            c_x, c_y = current
            current_node = self.grid.grid[c_x][c_y]
            current_node.close_node()
            adjacents = self._find_adjacents( current )
            for adj in adjacents:
                a_x, a_y = adj
                node = self.grid.grid[a_x][a_y]
                cost = self._calc_cost( current_node.g, a_x, a_y )
                if node == None:
                    node = Node(*adj)
                    node.set_g( cost )
                    self.grid.insert_node(a_x, a_y, node)
                    value = self._calc_value( node, goal )
                    heappush( heap, (value, adj ) )
                    node.set_parent( current )
                elif node == BLOCKED or not node.open:
                    pass
                elif node.open and cost < node.g:
                    node.close_node()
                    
            current = heappop(heap)[1]
            if current == goal:
                goal_node = Node(*goal)
                goal_node.set_parent((c_x, c_y),)
                self.grid.insert_node(goal[0], goal[1], goal_node)

        self.path = self._construct_path( current )
                
    def _find_adjacents ( self, current ):
        adjacents = []
        if current[0] > 0:
            adjacents.append( ( current[0] - 1, current[1] ) )
        if current[0] < self.grid.width - 1:
            adjacents.append( ( current[0] + 1, current[1] ) )
        if current[1] > 0:
            adjacents.append( ( current[0], current[1] - 1 ) )
        if current[1] < self.grid.height - 1:
            adjacents.append( ( current[0], current[1] + 1 ) )
        return adjacents

    def _calc_cost ( self, current_g, x, y ):
        return 1 + current_g

    def _calc_value(self, node, goal ):
        return node.g + 1.001*node.h_function( goal )

    def _construct_path( self, goal ):
        path = []
        current = goal
        x, y = current
        while current != self.start:
            path.append( current )
            current = self.grid.grid[x][y].parent
            x, y = current
       
        return path
