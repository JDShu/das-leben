import pygame

MOUSE = 1

class Event():
    def __init__( self, category ):
        self.category = category        

class MouseEvent( Event ):
    def __init__( self ):
        Event.__init__( self, MOUSE )
        self.x, self.y = pygame.mouse.get_pos()
        self.l_click, self.m_click, self.r_click = pygame.mouse.get_pressed()
