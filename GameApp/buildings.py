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

class House:
    def __init__(self, filename=None, floors=1):
        self.m_Floors = []
        
        if filename:
            self.LoadLayout( filename )
        else:
            self.BuildDebugHouse( floors )
            
        self.SetFloorInvisible( 1 )
    
    def LoadLayout(self, filename):
        '''loads a house lyaout file'''
        
    def BuildDebugHouse(self, floors):
        '''Builds a default layout'''
        for floor in xrange( floors ):
            self.m_Floors.append( Floor() )
            self.m_Floors[ floor ].SetPosition( 0, -2 + (floor * 10), 0 )
        
    def Draw(self):
        for floor in self.m_Floors:
            if floor.Visible():
                floor.Draw()
                
    def DrawSelectMode( self ):
        for floor in self.m_Floors:
            if floor.Visible():
                glPushName( floor.GetGLName() )
                floor.Draw()
                glPopName()
                
    def GetGLName( self ):
        Names = []; nadd = Names.append;
        for floor in self.m_Floors:
            nadd( floor.GetGLName() )
            
        return Names
    
    def SetFloorVisible( self, a_Floor ):
        self.m_Floors[ a_Floor ].m_Visible = True
        
    def SetFloorInvisible( self, a_Floor ):
        self.m_Floors[ a_Floor ].m_Visible = False
        
class Floor:
    """
       defines a floor of a building which is the 
       walls + floor + objects NOT the actual floor
    """
    
    def __init__(self, objects=None):
        self.m_Objects = []
        self.m_Visible = True
        
        if objects:
            self.m_Objects.extend( objects )
        else:
            self.MakeDefaultFloor()
        
        self.m_GLName = random.randint( 1, 1000 )
        
    def GetGLName( self ):
        return self.m_GLName
            
    def Visible(self):
        return self.m_Visible
    
    def SetPosition( self, a_X, a_Y, a_Z ):
        xoffset = 0
        for i in xrange( 0, 4 ):
            self.m_Objects[ i ].SetPosition( a_X + xoffset, a_Y, a_Z, 1.0 )
            xoffset += 5
          
        xoffset = 0
        for i in xrange( 4, 8 ):
            self.m_Objects[ i ].SetPosition( a_X + xoffset, a_Y, a_Z + 24, 1.0 )
            xoffset += 7
            
        xoffset = -5
        for i in xrange( 8, 11 ):
            self.m_Objects[ i ].SetPosition( a_X + xoffset, a_Y, a_Z - 4, 1.0 )
            self.m_Objects[ i ].m_YRot.SetAngle( 90 )
            xoffset -= 7
          
        xoffset = -5
        for i in xrange( 11, 14 ):
            self.m_Objects[ i ].SetPosition( a_X + xoffset, a_Y, a_Z + 27, 1.0 )
            self.m_Objects[ i ].m_YRot.SetAngle( 90 )
            xoffset -= 7
            
        self.m_Objects[ 14 ].SetPosition( a_X + 14, a_Y, a_Z + 27, 1.0 )
        self.m_Objects[ 14 ].m_ZRot.SetAngle( 90 )
        self.m_Objects[ 14 ].m_XRot.SetAngle( 90 )
            
    def MakeDefaultFloor(self):
        oadd = self.m_Objects.append
        
        # ------- wall one ------------
        for i in xrange( 14 ):
            Wall = Object3d(object_type=OBJECT_3D_WALL, scale=200)
            oadd( Wall )

        Wall = Object3d(object_type=OBJECT_3D_WALL, scale=400)
        oadd( Wall )
        
        self.SetPosition( 0, 0, 0 )
        
    def Draw(self):
        for item in self.m_Objects:
            item.Draw()
            