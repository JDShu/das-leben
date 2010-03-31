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
    '''
    A House objects manager
    '''
    def __init__(self, filename=None, floors=1):
        '''
        Create a House() instance
        @param filename String : a path to an existing house definition file
        @param floors Integer : how many floors hight the house is
        '''
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
        '''
        Render the house
        '''
        for floor in self.m_Floors:
            if floor.Visible():
                floor.Draw()
                
    def DrawSelectMode( self ):
        '''
        Render whilst adding object IDs to OpenGL to support object picking
        '''
        for floor in self.m_Floors:
            if floor.Visible():
                glPushName( floor.GetGLName() )
                floor.Draw()
                glPopName()
                
    def GetGLName( self ):
        '''
        Get the object IDs ( GLName ) of this houses objects
        @return Names List : a list of object GLNames
        '''
        Names = []; nadd = Names.append;
        for floor in self.m_Floors:
            nadd( floor.GetGLName() )
            
        return Names
    
    def SetFloorVisible( self, a_Floor ):
        '''
        Set a floor as visible
        @param a_Floor Integer : the floor to make visible
        '''
        self.m_Floors[ a_Floor ].m_Visible = True
        
    def SetFloorInvisible( self, a_Floor ):
        '''
        Set a floor as invisible
        @param a_Floor Integer : the floor to make invisible
        '''
        self.m_Floors[ a_Floor ].m_Visible = False
        
class Floor:
    """
       defines a floor of a building which is the 
       walls + floor + objects NOT the actual floor
    """
    
    def __init__(self, objects=None):
        '''
        Create a Floor instance
        @param objects List : a list of game objects on this floor
        '''
        self.m_Objects = []
        self.m_Visible = True
        
        if objects:
            self.m_Objects.extend( objects )
        else:
            self.MakeDefaultFloor()
        
        self.m_GLName = random.randint( 1, 1000 )
        
    def GetGLName( self ):
        '''
        Get the floors GLName fpr picking
        @return Integer : the GLName or ID number
        '''
        return self.m_GLName
            
    def Visible(self):
        '''
        Is this Floor visible?
        
        @return Boolean : The current visiblilty state
        '''
        return self.m_Visible
    
    def SetPosition( self, a_X, a_Y, a_Z ):
        '''
        Set the position of this FLoor and all object within it
        @param a_X Float : the x position
        @param a_Y Float : the y position
        @param a_Z Float : the z position
        '''
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
        '''
        Create a Default floor layout etc
        '''
        oadd = self.m_Objects.append
        
        # ------- wall one ------------
        for i in xrange( 14 ):
            Wall = Object3d(object_type=OBJECT_3D_WALL, scale=200)
            oadd( Wall )

        Wall = Object3d(object_type=OBJECT_3D_WALL, scale=400)
        oadd( Wall )
        
        self.SetPosition( 0, 0, 0 )
        
    def Draw(self):
        '''
        Render all objects on this floor
        '''
        for item in self.m_Objects:
            item.Draw()
            