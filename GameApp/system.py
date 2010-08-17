import pygame
from heapq import heappush, heappop
import soya

MOUSE = 1
TIME = 2
ACTION = 3

PATHFINDER_RESOLUTION = 1


class EventQueue:
    def __init__( self ):
        self.events = []
        
    def Push( self, event ):
        self.events.append( event )
        
    def Flush( self ):
        self.events = []
        
    def GetCurrentEvent( self ):
        return self.events[ 0 ]
    
    def ClearCurrentEvent( self ):
        self.events[ 0 ] = None
        del self.events[ 0 ]
        
    

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
    def __init__( self, time_type ):
        Event.__init__( self, TIME )
        self.time_type = time_type
        
class ActionEvent( Event ):
    def __init__( self, name ):
        Event.__init__( self, ACTION )
        self.name = name
        self.actions = []
        self.prepared = False
        
    def AddAction( self, action ):
        self.actions.append( action )
        
    def GetCurrentAction( self ):
        return self.actions[ 0 ]
    
    def GetNextAction( self ):
        del self.actions[ 0 ]
        return self.actions[ 0 ]
    
    def IsPrepared( self ):
        return self.prepared
    
class AvatarAction:
    def __init__( self, name, action=None, target=None ):
        self.name = name
        self.data = []
        if action:
            self.data.append( action )
        
        self.target_avatar = target
    
    def AddAction( self, action ):
        self.data.append( action )
        
    def GetNextAction( self ):
        del self.data[ 0 ]
        action = self.data[ 0 ]
        if action:
            return action
        
        return None

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

    def h_function( self, goal):
        temp = [ ( abs( g[0] - self.x) + abs(g[1] - self.y ) ) for g in goal ]
        return min( temp )

    def print_coordinates( self ):
        print ( x, y )

BLOCKED = 1
#2D list data structure for pathfinding
class Grid():
    def __init__( self , width=50, height=50):

        self.grid = []
        self.width = width
        self.height = height
        for y in xrange(height):
            line = []
            for x in xrange(width):
                line.append( None )
            self.grid.append( line )

    def insert_block( self, x, y ):
        self.grid[x][y] = BLOCKED
        
    def clear_nodes( self ):
        for y in xrange(self.width):
            for x in xrange(self.height):
                if isinstance( self.grid[y][x], Node ):
                    self.grid[y][x] = None

    def insert_node( self, x, y, node):
        self.grid[x][y] = node
        
                    
    def print_grid( self ):
        for y in xrange(self.width):
            for x in xrange(self.height):
                if self.grid[y][x] == None:
                    print "0",
                elif self.grid[y][x] == "X":
                    print "X",
                elif self.grid[y][x] == 1:
                    print "W",
                else:
                    print "?",
            print " "
            
    def save_file( self, filename, path ):
        for sq in path:
            self.grid[sq[0]][sq[1]] = "X"
            
        f = open( filename, "w" )
        
        for y in xrange(self.width):
            line = ""
            for x in xrange(self.height):
                if self.grid[x][y] == None:
                    line += "_"
                elif self.grid[x][y] == "X":
                    line += "X"
                elif self.grid[x][y] == 1:
                    line += "W"
                else:
                    line += "_"
            line += "\n"
            f.write( line )
        
        f.close()
        
    def draw_path( self, path ):
        for sq in path:
            self.grid[sq[0]][sq[1]] = "X"
        self.print_grid()
        
    def GridSpaceCoords( self, x, y, tile_width=1, tile_offset=0 ):
        return ( int( ( x - tile_offset ) / tile_width ), int( ( y - tile_offset ) / tile_width ) )

#generates list of grid coordinates leading from goal to start according to a simple A* algorithm
class PathFinder():
    def __init__( self, input_grid, start, goal ):
        self.start = start
        self.goal = goal
        self.grid = input_grid
        self.grid.clear_nodes()
        start_node = Node(*start)
        start_node.set_g(0)
        self.grid.insert_node(start[0], start[1], start_node)
        heap = []
        heappush( heap, (0,start) )
        current = heappop(heap)[1]
        reached_goal = False
        if start in goal:
            reached_goal = True
        while not reached_goal:
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
            #print current
            current = heappop(heap)[1]
            for g in goal:
                if current == g:
                    goal_node = Node(*g)
                    goal_node.set_parent((c_x, c_y),)
                    self.grid.insert_node(g[0], g[1], goal_node)
                    reached_goal = True
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
        if self.start == goal:
            return [goal]
        path = []
        current = goal
        x, y = current
        while current != self.start:
            path.append( current )
            current = self.grid.grid[x][y].parent
            x, y = current
       
        return path
    
    def Draw( self, a_Scene, a_Scale, a_Altitude, a_Offset=0 ):
        w = soya.World()
        last = self.path[ 0 ]
        for point in self.path:
            if not last == point:
                x1 = ( last[ 0 ] * a_Scale ) + a_Offset
                z1 = ( last[ 1 ] * a_Scale ) + a_Offset
                x2 = ( point[ 0 ] * a_Scale ) + a_Offset
                z2 = ( point[ 1 ] * a_Scale ) + a_Offset
                
                p1 = soya.Vertex( a_Scene, x1, a_Altitude, z1 )
                p2 = soya.Vertex( a_Scene, x2, a_Altitude, z2 )
                
                f = soya.Face( a_Scene, [ p1, p2 ] )
                
                last = point
##               
##        # 
##        b = soya.Body( a_Scene, w.to_model() )
        
                
##        return b


                
