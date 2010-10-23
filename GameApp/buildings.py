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
from game_assets import *

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
    
    def __init__(self, a_Filename=None):
        '''
        Create a Floor instance
        @param objects List : a list of game objects on this floor
        '''
        
        if a_Filename:
            f = open( a_Filename, "r" )
            lines = f.readlines()
            
            
        self.m_Objects = []
        self.m_Visible = True
        
        self.asset_manager = AssetManager()
        
        if objects:
            self.m_Objects.extend( objects )
        else:
            self.MakeDefaultFloor()
        
        self.m_GLName = random.randint( 1, 1000 )
        
    def Save( self, a_Filename ):
        pass
        
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
            
            
WALL_CLOSED = 1
WALL_OPEN = 2
WALL_CORNER = 3

WALL_FRONT = 1
WALL_BACK = 2
WALL_LEFT = 3
WALL_RIGHT = 4

WALL_INNER_TOP_LEFT = 5
WALL_INNER_TOP_RIGHT = 6
WALL_INNER_BOTTOM_LEFT = 7
WALL_INNER_BOTTOM_RIGHT = 8

WALL_OUTER_TOP_LEFT = 9
WALL_OUTER_TOP_RIGHT = 10
WALL_OUTER_BOTTOM_LEFT = 11
WALL_OUTER_BOTTOM_RIGHT = 12

WALL_WIDTH = 1.0 * 3

class Wall:
    def __init__( self, x=0.0, z=0.0, world=None,  wall_type=WALL_OPEN, 
                  wall_position=WALL_FRONT, wall_position_extras=None, 
                  front_material=None, back_material=None ):

        HEIGHT = 1.62 * 3
        WIDTH = 1.0 * 3
        DEPTH = 0.2
        
        if not front_material:
            front_material = self.MakeDefaultMaterial()
            
        if not back_material:
            back_material = self.MakeDefaultMaterial()
            
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.DEPTH = DEPTH
       
        
        if wall_position == WALL_FRONT:
            fbl = soya.Vertex( world,  x, 0.0, z, 0.0, 0.0 )
            fbr = soya.Vertex( world,  x + WIDTH, 0.0, z, 1.0, 0.0 )
            ftr = soya.Vertex( world,  x + WIDTH, HEIGHT, z, 1.0, 1.0 )
            ftl = soya.Vertex( world,  x , HEIGHT, z, 0.0, 1.0 )
            
            bbl = soya.Vertex( world,  x , 0.0, z + DEPTH, 0.0, 0.0 )
            bbr = soya.Vertex( world,  x + WIDTH, 0.0, z + DEPTH, 1.0, 0.0 )
            btr = soya.Vertex( world,  x + WIDTH, HEIGHT, z + DEPTH, 1.0, 1.0 )
            btl = soya.Vertex( world,  x , HEIGHT, z + DEPTH, 0.0, 1.0 )
            
            front_face = [ fbr, fbl, ftl, ftr ]
            back_face = [ bbl, bbr, btr, btl ]
            top_face = [ btl, btr, ftr, ftl ]
            if wall_position_extras == WALL_INNER_TOP_LEFT:
                bbr.x = x + WIDTH + DEPTH
                btr.x = x + WIDTH + DEPTH 
                
            elif wall_position_extras == WALL_INNER_TOP_RIGHT:          
                bbl.x = x - DEPTH
                btl.x = x - DEPTH
            
        elif wall_position == WALL_BACK:
            fbl = soya.Vertex( world,  x, 0.0, z + WIDTH + DEPTH, 0.0, 0.0 )
            fbr = soya.Vertex( world,  x + WIDTH, 0.0, z + WIDTH + DEPTH , 1.0, 0.0 )
            ftr = soya.Vertex( world,  x + WIDTH, HEIGHT, z + WIDTH + DEPTH, 1.0, 1.0 )
            ftl = soya.Vertex( world,  x , HEIGHT, z + WIDTH + DEPTH, 0.0, 1.0 )
            
            bbl = soya.Vertex( world,  x , 0.0, z + WIDTH, 0.0, 0.0 )
            bbr = soya.Vertex( world,  x + WIDTH, 0.0, z + WIDTH, 1.0, 0.0 )
            btr = soya.Vertex( world,  x + WIDTH, HEIGHT, z + WIDTH, 1.0, 1.0 )
            btl = soya.Vertex( world,  x , HEIGHT, z + WIDTH, 0.0, 1.0 )
            
            front_face = [ fbl, fbr, ftr, ftl ]
            back_face = [ bbr, bbl, btl, btr ]
            top_face = [ btl, ftl, ftr, btr ]
            
            if wall_position_extras == WALL_INNER_BOTTOM_RIGHT:
                bbl.x = x - DEPTH
                btl.x = x - DEPTH
            elif wall_position_extras == WALL_INNER_TOP_RIGHT:          
                bbr.x = x + WIDTH + DEPTH
                btr.x = x + WIDTH + DEPTH 

        elif wall_position == WALL_RIGHT:
            bbl = soya.Vertex( world,  x + WIDTH - DEPTH, 0.0, z, 0.0, 0.0 )
            bbr = soya.Vertex( world,  x + WIDTH - DEPTH, 0.0, z + WIDTH, 1.0, 0.0 )
            btr = soya.Vertex( world,  x + WIDTH - DEPTH, HEIGHT, z + WIDTH, 1.0, 1.0 )
            btl = soya.Vertex( world,  x + WIDTH - DEPTH, HEIGHT, z, 0.0, 1.0 )
            
            fbl = soya.Vertex( world,  x + WIDTH, 0.0, z , 0.0, 0.0 )
            fbr = soya.Vertex( world,  x + WIDTH, 0.0, z + WIDTH, 1.0, 0.0 )
            ftr = soya.Vertex( world,  x + WIDTH, HEIGHT, z + WIDTH, 1.0, 1.0 )
            ftl = soya.Vertex( world,  x + WIDTH, HEIGHT, z, 0.0, 1.0 )
            
            front_face = [ fbr, fbl, ftl, ftr ]
            back_face = [ bbl, bbr, btr, btl ]
            top_face = [ btl, btr, ftr, ftl ]
            
            if wall_position_extras == WALL_INNER_TOP_RIGHT:
                bbr.z = z + WIDTH + DEPTH
                btr.z = z + WIDTH + DEPTH
            elif wall_position_extras == WALL_INNER_BOTTOM_RIGHT:          
                fbl.z = z + DEPTH
                ftl.z = z + DEPTH 
            elif wall_position_extras == WALL_OUTER_TOP_LEFT:
                fbr.z = z + WIDTH + DEPTH
                ftr.z = z + WIDTH + DEPTH
            
        elif wall_position == WALL_LEFT:
            fbl = soya.Vertex( world,  x, 0.0, z, 0.0, 0.0 )
            fbr = soya.Vertex( world,  x, 0.0, z + WIDTH, 1.0, 0.0 )
            ftr = soya.Vertex( world,  x, HEIGHT, z + WIDTH, 1.0, 1.0 )
            ftl = soya.Vertex( world,  x , HEIGHT, z, 0.0, 1.0 )
            
            bbl = soya.Vertex( world,  x + DEPTH, 0.0, z, 0.0, 0.0 )
            bbr = soya.Vertex( world,  x + DEPTH, 0.0, z + WIDTH, 1.0, 0.0 )
            btr = soya.Vertex( world,  x + DEPTH, HEIGHT, z + WIDTH, 1.0, 1.0 )
            btl = soya.Vertex( world,  x + DEPTH, HEIGHT, z, 0.0, 1.0 )
            
            front_face = [ fbl, fbr, ftr, ftl ]
            back_face = [ bbr, bbl, btl, btr ]
            top_face = [ btl, ftl, ftr, btr ]
            
            if wall_position_extras == WALL_INNER_TOP_LEFT:
                bbr.z = z + WIDTH + DEPTH
                btr.z = z + WIDTH + DEPTH
            elif wall_position_extras == WALL_INNER_BOTTOM_LEFT:          
                fbl.z = z + DEPTH 
                ftl.z = z + DEPTH           
            elif wall_position_extras == WALL_OUTER_TOP_RIGHT:
                fbr.z = z + WIDTH + DEPTH
                ftr.z = z + WIDTH + DEPTH
        
        if wall_type == WALL_OPEN or wall_type == WALL_CLOSED:
            
            # front wall
            f = soya.Face( world, front_face, front_material )
            # back wall
            f = soya.Face( world, back_face, back_material )
            # top of wall
            f = soya.Face( world, top_face )
            # bottom of wall
            f = soya.Face( world, [ fbr, ftr, btr, bbr ], front_material )
                
            f = soya.Face( world, [ btl, ftl, fbl, bbl ], front_material )
            
            if wall_type == WALL_CLOSED:
                # make side faces
                f = soya.Face( world, [ fbr, ftr, btr, bbr ] )
                
                f = soya.Face( world, [ btl, ftl, fbl, bbl ] )
                
        elif wall_type == WALL_CORNER:
            if wall_position == WALL_INNER_TOP_LEFT:
                pass
            elif wall_position == WALL_INNER_TOP_RIGHT:
                pass
            elif wall_position == WALL_INNER_BOTTOM_LEFT:
                fbl = soya.Vertex( world,  x, 0.0, z + DEPTH, 0.0, 0.0 )
                fbr = soya.Vertex( world,  x + DEPTH, 0.0, z + DEPTH, 1.0 * ( front_material.texture.width / DEPTH ), 0.0 )
                ftr = soya.Vertex( world,  x + DEPTH, HEIGHT, z + DEPTH, 1.0 * ( front_material.texture.width / DEPTH ), 1.0 )
                ftl = soya.Vertex( world,  x, HEIGHT, z + DEPTH, 0.0, 1.0 )
                
                bbl = soya.Vertex( world,  x + DEPTH, 0.0, z, 0.0, 0.0 )
                bbr = soya.Vertex( world,  x + DEPTH, 0.0, z + DEPTH, 1.0 * ( front_material.texture.width / DEPTH ), 0.0 )
                btr = soya.Vertex( world,  x + DEPTH, HEIGHT, z + DEPTH, 1.0 * ( front_material.texture.width / DEPTH ) , 1.0)
                btl = soya.Vertex( world,  x + DEPTH, HEIGHT, z, 0.0, 1.0 )
            
                front_face = [ fbl, fbr, ftr, ftl ]
                back_face = [ bbr, bbl, btl, btr ]
                top_face = [ btl, ftl, ftr, btr ]
                
            elif wall_position == WALL_INNER_BOTTOM_RIGHT:
                pass
            
            # front corner wall
            f = soya.Face( world, front_face, back_material )
            # back corner wall ( the side when its a inner corner )
            f = soya.Face( world, back_face, back_material )
            # top of wall
            f = soya.Face( world, top_face )
            # bottom of wall
            
##        else:
##            fbl = soya.Vertex( world,  x, 0.0, z, diffuse = (1.0, 1.0, 1.0, 1.0) )
##            fbr = soya.Vertex( world,  x + WIDTH, 0.0, z, diffuse = (1.0, 1.0, 1.0, 1.0) )
##            ftr = soya.Vertex( world,  x + WIDTH, HEIGHT, z, diffuse = (1.0, 1.0, 1.0, 1.0) )
##            ftl = soya.Vertex( world,  x , HEIGHT, z, diffuse = (1.0, 1.0, 1.0, 1.0) )
##            
##            bbl = soya.Vertex( world,  x , 0.0, z + DEPTH, diffuse = (1.0, 1.0, 1.0, 1.0) )
##            bbr = soya.Vertex( world,  x + WIDTH - DEPTH, 0.0, z + DEPTH, diffuse = (1.0, 1.0, 1.0, 1.0) )
##            btr = soya.Vertex( world,  x + WIDTH - DEPTH, HEIGHT, z + DEPTH, diffuse = (1.0, 1.0, 1.0, 1.0) )
##            btl = soya.Vertex( world,  x , HEIGHT, z + DEPTH, diffuse = (1.0, 1.0, 1.0, 1.0) )
##            
##            far_fbr = soya.Vertex( world,  x + WIDTH, 0.0, z + WIDTH, diffuse = (1.0, 1.0, 1.0, 1.0) )
##            far_ftr = soya.Vertex( world,  x + WIDTH, HEIGHT, z + WIDTH, diffuse = (1.0, 1.0, 1.0, 1.0) )
##            far_fbr = soya.Vertex( world,  x + WIDTH - DEPTH, 0.0, z + WIDTH, diffuse = (1.0, 1.0, 1.0, 1.0) )
##            far_ftr = soya.Vertex( world,  x + WIDTH - DEPTH, HEIGHT, z + WIDTH, diffuse = (1.0, 1.0, 1.0, 1.0) )
            
    def MakeDefaultMaterial( self ):
        material = soya.Material()
        material.diffuse = (1.0, 1.0, 1.0, 1.0)
        material.shininess = 0.5
        material.specular = (0.5, 0.5, 0.5, 1.0)
        material.separate_specular = 1

        return material
    