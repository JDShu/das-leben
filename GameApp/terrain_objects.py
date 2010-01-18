'''
 * This file is part of La Vida
 * Copyright (C) 2009 Mike Hibbert
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
'''

from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import pygame
from pygame.locals import *
from vector_3d import *
from object_3d import *
from collisions import BoundingBox3d

class RegionQuad( Vector3d, BoundingBox3d ):
    def __init__( self, a_X=0.0, a_Y=0.0, a_Z=0.0, a_Size=1.0 ):
        Vector3d.__init__( self, a_X, a_Y, a_Z )
        BoundingBox3d.__init__( self, a_X, a_Y, a_Z, a_Size )
        
    def SetAsObject( self, a_Object3d ):
        self.ObjectToRender = a_Object3d
        self.ObjectToRender.SetPosition( self.GetX(), self.GetY(), self.GetY() )
        
    def Draw( self ):
        self.ObjectToRender.Draw()
    
    
class Region( Vector3d ):
    def __init__( self, a_X=0.0, a_Y=0.0, a_Z=0.0, a_Width=64, a_Size=1.0 ):
        Vector3d.__init__( self, a_X, a_Y, a_Z )
        self.quads = []; qadd = self.quads.append
        for x in xrange( a_Width ):
            for z in xrange( a_Width ):
                qadd( RegionQuad( a_X + ( a_Size / 2 ) + ( float( x ) * a_Size ), 
                                  a_Y + ( a_Size / 2 ), 
                                  a_Z + ( a_Size / 2 ) + ( float( z ) * a_Size ),
                                  a_Size ) )
                
        
        
        