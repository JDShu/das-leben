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
from ogl_vbo import *
from ogl_va import *
from collisions import BoundingBox3d
import random
from ctypes import *
from numpy import array
from buildings import *

REGION_NORMAL = 1
REGION_EDITING = 2

QUAD_FLOOR_SQUARE = 50
QUAD_FLOOR_NONE = 51

# --------------------------------------------------------------------

class RegionQuad( BoundingBox3d ):
    '''
    A class to define what is contained inside a chopped up regions squares
    '''
    def __init__( self, a_X=0.0, a_Y=0.0, a_Z=0.0, a_Size=0.5, a_Type='#' ):
        '''
        Create a RegionQuad instance
        @param a_X Float : the x coord of the quad
        @param a_Y Float : the y coord of the quad
        @param a_Z Float : the z coord of the quad
        '''
        BoundingBox3d.__init__( self, a_X + (a_Size / 2.0), a_Y, a_Z + (a_Size / 2.0), a_Size )
        
        # y values for quad
        self.ul = None
        self.ur = None
        self.ll = None
        self.lr = None
        
        # a type of quad for working with floorplanns
        self.quadType = a_Type
        
        # vertex array index for when we are shaping the region later
        self.va_index = 0
        self.i = 0
        
        # quad size
        self.size = a_Size
        
        self.selected = False
        self.compiled = False
        self.oldListID = 0
        self.listID = 0     
        
        self.obj = None
        self.extra = [];
        
        self.colour_adjust = random.random()
        
       
    def CreateQuad( self, model, altitude, material=None ):
        radius = self.size / 2.0
        x, y, z, w = self.GetPosition()
        
        soya.Face( model, 
                   [ soya.Vertex( model, x - radius, altitude, z + radius, 0.0, 0.0 ),
                     soya.Vertex( model, x + radius, altitude, z + radius, 1.0, 0.0 ),
                     soya.Vertex( model, x + radius, altitude, z - radius, 1.0, 1.0 ),
                     soya.Vertex( model, x - radius, altitude, z - radius, 0.0, 1.0 ) ], 
                   material )
                     
    def CreateNormals( self, normals, offset, altitude ):
        normals[ offset ][ 0 ] = 0.0
        normals[ offset ][ 1 ] = 1.0
        normals[ offset ][ 2 ] = 0.0
        
        normals[ offset + 1 ][ 0 ] = 0.0
        normals[ offset + 1 ][ 1 ] = 1.0
        normals[ offset + 1 ][ 2 ] = 0.0
        
        normals[ offset + 2 ][ 0 ] = 0.0
        normals[ offset + 2 ][ 1 ] = 1.0
        normals[ offset + 2 ][ 2 ] = 0.0
        
        normals[ offset + 3 ][ 0 ] = 0.0
        normals[ offset + 3 ][ 1 ] = 1.0
        normals[ offset + 3 ][ 2 ] = 0.0
        
    def CreateTexCoords( self, texCoords, offset, altitude ):
        texCoords[ offset ][ 0 ] = 0.0
        texCoords[ offset ][ 1 ] = 0.0
        
        texCoords[ offset + 1 ][ 0 ] = 1.0
        texCoords[ offset + 1 ][ 1 ] = 0.0
        
        texCoords[ offset + 2 ][ 0 ] = 1.0
        texCoords[ offset + 2 ][ 1 ] = 1.0
                
        texCoords[ offset + 3 ][ 0 ] = 0.0
        texCoords[ offset + 3 ][ 1 ] = 1.0

    def CreateLBQuad( self, vertexes, offset, altitude ):
        radius = self.size / 2.0
        x, y, z, w = self.GetPosition()

        vertexes[ offset ][ 0 ] = x 
        vertexes[ offset ][ 1 ] = altitude
        vertexes[ offset ][ 2 ] = z 
        
        vertexes[ offset + 1 ][ 0 ] = x + radius
        vertexes[ offset + 1 ][ 1 ] = altitude
        vertexes[ offset + 1 ][ 2 ] = z - radius
        
        vertexes[ offset + 2 ][ 0 ] = x + radius
        vertexes[ offset + 2 ][ 1 ] = altitude
        vertexes[ offset + 2 ][ 2 ] = z + radius
        
        vertexes[ offset + 3 ][ 0 ] = x - radius
        vertexes[ offset + 3 ][ 1 ] = altitude
        vertexes[ offset + 3 ][ 2 ] = z + radius
        
    def CreateRBQuad( self, vertexes, offset, altitude ):
        radius = self.size / 2.0
        x, y, z, w = self.GetPosition()

        vertexes[ offset ][ 0 ] = x - radius
        vertexes[ offset ][ 1 ] = altitude
        vertexes[ offset ][ 2 ] = z - radius
        
        vertexes[ offset + 1 ][ 0 ] = x 
        vertexes[ offset + 1 ][ 1 ] = altitude
        vertexes[ offset + 1 ][ 2 ] = z 
        
        vertexes[ offset + 2 ][ 0 ] = x + radius
        vertexes[ offset + 2 ][ 1 ] = altitude
        vertexes[ offset + 2 ][ 2 ] = z + radius
        
        vertexes[ offset + 3 ][ 0 ] = x - radius
        vertexes[ offset + 3 ][ 1 ] = altitude
        vertexes[ offset + 3 ][ 2 ] = z + radius
        
    def CreateRTQuad( self, vertexes, offset, altitude ):
        radius = self.size / 2.0
        x, y, z, w = self.GetPosition()

        vertexes[ offset ][ 0 ] = x - radius
        vertexes[ offset ][ 1 ] = altitude
        vertexes[ offset ][ 2 ] = z - radius
        
        vertexes[ offset + 1 ][ 0 ] = x + radius
        vertexes[ offset + 1 ][ 1 ] = altitude
        vertexes[ offset + 1 ][ 2 ] = z - radius
        
        vertexes[ offset + 2 ][ 0 ] = x 
        vertexes[ offset + 2 ][ 1 ] = altitude
        vertexes[ offset + 2 ][ 2 ] = z 
        
        vertexes[ offset + 3 ][ 0 ] = x - radius
        vertexes[ offset + 3 ][ 1 ] = altitude
        vertexes[ offset + 3 ][ 2 ] = z + radius
        
    def CreateLTQuad( self, vertexes, offset, altitude ):
        radius = self.size / 2.0
        x, y, z, w = self.GetPosition()

        vertexes[ offset ][ 0 ] = x - radius
        vertexes[ offset ][ 1 ] = altitude
        vertexes[ offset ][ 2 ] = z - radius
        
        vertexes[ offset + 1 ][ 0 ] = x + radius
        vertexes[ offset + 1 ][ 1 ] = altitude
        vertexes[ offset + 1 ][ 2 ] = z - radius
        
        vertexes[ offset + 2 ][ 0 ] = x + radius
        vertexes[ offset + 2 ][ 1 ] = altitude
        vertexes[ offset + 2 ][ 2 ] = z + radius
        
        vertexes[ offset + 3 ][ 0 ] = x
        vertexes[ offset + 3 ][ 1 ] = altitude
        vertexes[ offset + 3 ][ 2 ] = z
        
    def SetAsObject( self, a_Object3d ):
        '''
        make this quad a 3d object 
        @param a_Object3d Object3d : instance of Object3d
        '''
        self.ObjectToRender = a_Object3d
        self.ObjectToRender.SetPosition( self.GetX(), self.GetY(), self.GetY() )
        
    def GetGLName( self ):
        '''
        Return the GLName of this object
        @return GLName Integer : a OpenGL ID to assist in picking objects
        '''
        return self.ObjectToRender.GetGLName()
        
    def Draw( self ):
        '''
        render the contents of this quad
        '''
        if self.obj:
            self.obj.Draw()
        if len( self.extra ) > 0:
            for obj in self.extra:
                obj.Draw()
    
    
class Region( soya.World ):
    '''
    A region of terrain
    '''
    def __init__( self, a_Scene, a_Width, a_Height ):
        '''
        Create a Region
        @param a_X Float : the bottom left x coord of the region
        @param a_Y Float : the bottom left y coord of the region
        @param a_Z Float : the bottom left z coord of the region
        @param a_Width Integer : the width in squares
        @param a_Height Integer : the height in squares
        @param a_Size Float : the width and height of each square, ( RegionQuad )
        @param a_Colour Float : the overall colour of the rendered RegionQuads
        '''
        
        soya.World.__init__( self )
        self.quads = []; qadd = self.quads.append
        self.quadIDS = []; iadd = self.quadIDS.append
        
        self.m_Width = a_Width
        self.m_Height = a_Height
        self.m_Size = a_Size = WALL_WIDTH
        
        
        
        self.textureID = 0
        self.wallTextureID = 0
        
##        for z in xrange( a_Height ):
##            for x in xrange( a_Width ):
##                rq = RegionQuad( ( float( x ) * a_Size ), 
##                                  2, 
##                                  ( float( z ) * a_Size ),
##                                  a_Size ) 
##                rq.CreateQuad( self, 2 )
        self.mode = REGION_NORMAL
        
        self.selected_quads = []
        
        self.m_ObjectType = OBJECT_3D_MESH
        self.listID = None
##        
    def compile_list( self ):
        self.listID = glGenLists( 1 )
        glNewList( self.listID, GL_COMPILE )
        for quad in self.quads:
            quad.Draw()
        glEndList()
        
    def recompile_list( self ):
        glDeleteLists( self.listID, 1 )
        self.compile_list()
        
    def Save( self, a_Filename ):
        f = open( a_Filename, "w" )
        for quad in self.quads:
            f.writelines( quad )
            
        f.close()
        
    def Load( self, a_Filename, a_AssetManager ):
        
        f = open( a_Filename, "r" )
        lines = f.readlines()
        if lines[ 0 ].startswith( "DIMENSIONS" ):
            dims = lines[ 0 ].split( ":" )[ 1 ].split( "x" )
            self.m_Width = int( dims[ 0 ] )
            self.m_Height = int( dims[ 1 ] )
            del lines[ 0 ]
        else:
            raise Exception, "unable to load dimensions of floor plan %s" % a_Filename
        
        if lines[ 0 ].startswith( "FLOOR" ):
            parts = lines[ 0 ].split( ":" )
            self.floor_material = a_AssetManager.GetTexture( parts[ 1 ].replace( "\n", "" ) )
            del lines[ 0 ]
            
        if lines[ 0 ].startswith( "WALL_INNER" ):
            parts = lines[ 0 ].split( ":" )
            self.wall_inner_material = a_AssetManager.GetTexture( parts[ 1 ].replace( "\n", "" ) )
            del lines[ 0 ]
            
        if lines[ 0 ].startswith( "WALL_OUTER" ):
            parts = lines[ 0 ].split( ":" )
            self.wall_outer_material = a_AssetManager.GetTexture( parts[ 1 ].replace( "\n", "" ) )
            del lines[ 0 ]
            
        self.CreateFromFloorPlan( lines )
        
    def CreateFromFloorPlan( self, lines ):
        self.DeleteAllQuads()
        
        self.quads = []; qadd = self.quads.append
        
        for z in xrange( self.m_Width ):
            for x in xrange( self.m_Height):
                quad = lines[ z ][ x ].replace( "\n", "" )
                
                rq = RegionQuad( self.x + ( float( x ) * self.m_Size ), 
                                  self.y, 
                                  self.z + ( float( z ) * self.m_Size ),
                                  self.m_Size,
                                  quad ) 
                
                qadd( rq )
                
        size = len( self.quads )

        for i, quad in enumerate( self.quads ):
            if quad.quadType != '?':
                quad.CreateQuad( self, 0.0, self.floor_material )

##                if quad.quadType == "A":
##                    quad.CreateLBQuad( va_vertexes, i * 4, 0.0 )
##                elif quad.quadType == "B":
##                    quad.CreateRBQuad( va_vertexes, i * 4, 0.0 )
##                elif quad.quadType == "C":
##                    quad.CreateRTQuad( va_vertexes, i * 4, 0.0 )
##                elif quad.quadType == "D":
##                    quad.CreateLTQuad( va_vertexes, i * 4, 0.0 )
                
                        
        
        
    def DeleteAllQuads( self ):
        for quad in self.quads:
            del quad
            
    def ClearSelection( self ):
        self.selected_quads = []
        
    def SelectWithPoint( self, a_Point ):
        for quad in self.quads:
            if quad.PointInside( a_Point ):
                self.selected_quads.append( quad )
        
    def SetMode( self, a_Mode ):
        self.mode = a_Mode
                
    def _draw( self ):
        glPushMatrix()
        glCullFace( GL_FRONT )
        glTranslatef( self.GetX(), self.GetY(), self.GetZ() )

        if self.textureID:
            glEnable( GL_TEXTURE_2D )
            glBindTexture( GL_TEXTURE_2D, self.textureID )
            
        self.va.Draw()
        
        if self.textureID:
            glDisable( GL_TEXTURE_2D )
            
        glCullFace( GL_BACK )
        glPopMatrix()      
    
        
    def GetGLNames( self ):
        quads = []; qadd = quads.append
        for quad in self.quads:
            qadd( quad.GetGLName() )
            
        return quads
    
    def raiseQuad( self, a_Location ):
        x, y, z, w = a_Location.GetPosition()
        ix = int( x / self.m_Size )
        iz = int( z / self.m_Size )
        
        
        va_vertexes = self.va.GetVertexArray()
        
        if ix > 0 and ix < self.m_Width:
            if iz > 0 and iz < self.m_Height:
                quad = self.quads[ ( iz * self.m_Width ) + ix ]
                xco, yco, zco, wco = quad.GetPosition() 
                yco += float( self.m_Size ) / 2.0 
                quad.SetPosition( xco, yco, zco )
                
                xco, temp_yco, zco, wco = self.vertexes[ quad.ll ].GetPosition() 
                self.vertexes[ quad.ll ].SetPosition( xco, yco, zco )
                
                xco, temp_yco, zco, wco = self.vertexes[ quad.lr ].GetPosition() 
                self.vertexes[ quad.lr ].SetPosition( xco, yco, zco )
                
                xco, temp_yco, zco, wco = self.vertexes[ quad.ur ].GetPosition() 
                self.vertexes[ quad.ur ].SetPosition( xco, yco, zco )
                
                xco, temp_yco, zco, wco = self.vertexes[ quad.ul ].GetPosition() 
                self.vertexes[ quad.ul ].SetPosition( xco, yco, zco )
                
                cur_x = ix - 1
                cur_z = iz + 1
                
                
                # apply 9 quad patch to the VA
                
                for u in xrange( 3 ):
                    for v in xrange( 3 ):
                        try:
                            rq = self.quads[ ( cur_z * self.m_Width ) + cur_x ]
                            
                            tmp = self.vertexes[ rq.ll ].GetNumpyPosition() 
                            va_vertexes[ rq.va_index ] = tmp
                            
                            tmp = self.vertexes[ rq.lr ].GetNumpyPosition()
                            va_vertexes[ rq.va_index + 1 ] = tmp 
                            
                            tmp = self.vertexes[ rq.ur ].GetNumpyPosition()
                            va_vertexes[ rq.va_index + 2 ] = tmp 
                            
                            tmp = self.vertexes[ rq.ul ].GetNumpyPosition()
                            va_vertexes[ rq.va_index + 3 ] = tmp 
                            
                        except:
                            pass
                        
                        cur_x += 1
                        
                    cur_x -= 3
                    cur_z -= 1
                        
      
    def lowerQuads( self, a_Begin, a_End ):
        pass

        
    def getQuad( self, a_X, a_Z ):
        try:
            self.quads[ ( a_X * self.m_Width ) + a_Z ]
        except:
            pass
        return quad
        
        
class TerrainRegion( Region ):
    def __init__( self, a_X=0.0, a_Y=0.0, a_Z=0.0, a_Width=50, a_Height=50, a_Size=0.5 ):
        Region.__init__( self, a_X, a_Y, a_Z, a_Width, a_Height, a_Size )
        
    def Draw( self ):
        #glEnable( GL_FOG )
        self._draw()
        #glDisable( GL_FOG ) 
        
    
class TerrainGridedRegion( Region ):
    def __init__( self, a_X=0.0, a_Y=0.0, a_Z=0.0, a_Width=50, a_Height=50, a_Size=0.5 ):
        Region.__init__( self, a_X, a_Y, a_Z, a_Width, a_Height, a_Size, a_Colour=0.8 )
        self.m_ShowGrid = False
        
    def ToggleGrid( self, a_Value=True ):
        self.m_ShowGrid = a_Value
        
    def Draw( self ):

        if self.m_ShowGrid:
            glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
            glLineWidth( 2 )
            glEnable( GL_LINE_SMOOTH )
            glDisable( GL_DEPTH_TEST )
            self._draw()
            glEnable( GL_DEPTH_TEST )
            glDisable( GL_LINE_SMOOTH )
            glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
        
class FloorRegion( Region ):
    def __init__( self, a_X=0.0, a_Y=0.0, a_Z=0.0, a_Width=50, a_Height=50, a_Size=0.5, a_Colour=1.0, a_AssetManager=None ):
        Region.__init__( self, a_X, a_Y, a_Z, a_Width, a_Height, a_Size, a_Colour )
       
        if a_AssetManager: 
            self.m_AssetManager = a_AssetManager
        else:
            raise Exception, "No asset manager instance supplied; create one and fill it with Object3d instances"
            
        self.m_ShowFloor = True
        self.m_ShowWalls = True
        
        self.textureID = 0
        top_row = ( a_Height - 1 ) * a_Width 
        # make the top and bottom rows
        
        for x in xrange( a_Width ):
            quad = self.quads[ x ]
            if x == 0:
                quad.m_WallType = WALL_BOTTOM_LEFT
            elif x == ( a_Width - 1 ):
                quad.m_WallType = WALL_BOTTOM_RIGHT
            else:
                quad.m_WallType = WALL_BOTTOM
                
            quad = self.quads[ top_row + x ]
            if x == 0:
                quad.m_WallType = WALL_TOP_LEFT
            elif x == ( a_Width - 1 ):
                quad.m_WallType = WALL_TOP_RIGHT
            else:
                quad.m_WallType = WALL_TOP
                
        for z in xrange( 1, a_Height - 2 ):
            quad = self.quads[ z * a_Width ]
            quad.m_WallType = WALL_LEFT
                
            quad = self.quads[ ( z * a_Width ) + a_Width ]
            quad.m_WallType = WALL_RIGHT
            
        self.CreateWalls()
        
    def CreateWalls( self ):
        pass
                            
    def ShowFloor( self, a_Value ):
        self.m_ShowFloor = a_Value
        
    def ShowWalls( self, a_Value ):
        self.m_ShowWalls = a_Value
        
    def SetFloorTexture( self, a_TextureID ):
        self.textureID = a_TextureID
        
    def SetWallTexture( self, a_TextureID, a_QuadIndex, a_ObjID ):
        for obj in self.quads[ a_QuadIndex ].objs:
            if obj.GetGLName() == a_ObjID:
                if hasattr( obj, "_texture" ): 
                    glDeleteTextures( 1, obj._texture )
                    obj._texture = a_TextureID
                else:
                    glDeleteTextures( 1, obj.textureID )
                    obj.textureID = a_TextureID
        
    def Draw( self ):
                
        if self.m_ShowFloor:
            if not self.textureID == 0:
                glEnable( GL_TEXTURE_2D )
            glDisable( GL_DEPTH_TEST )
            self._draw()
            glEnable( GL_DEPTH_TEST )
            
            if not self.textureID == 0:
                glDisable( GL_TEXTURE_2D )
                
        if self.m_ShowWalls:
            for quad in self.quads:
                quad.Draw()
        
class LoadableRegion( Region ):
        def __init__( self, a_Scene, a_X=0.0, a_Y=0.0, a_Z=0.0, a_AssetManager=None, a_Width=50, a_Height=50, a_Size=0.5, a_FirstFloor=True ):
            if not a_Scene: 
                raise Exception, "Loadable Regions require a soya.World instance" 
            
            Region.__init__( self, a_Scene, a_Width, a_Height )
            self.AssetManager = a_AssetManager
            self.ShowWalls = True
            self.FirstFloor = a_FirstFloor
            self.Scene = a_Scene
            
        def Load( self, a_Filename ):
            Region.Load( self, a_Filename, self.AssetManager )
            
            if self.FirstFloor:
                altitude = 0.40
            else:
                altitude = -0.41
                
            wall_front_material = self.AssetManager.GetTexture( "DEFAULT_WALL" )
            wall_back_material = self.AssetManager.GetTexture( "LIGHT_WALL_PAPER" )
                
            for i in xrange( 1, len( self.quads ) ):
                quad = self.quads[ i ]
                if quad.quadType == "a":
                    w = Wall( quad.GetX() - ( quad.size / 1.975 ), 
                              quad.GetZ() - ( quad.size / 1.75 ), 
                              self.Scene,
                              front_material=wall_front_material,
                              back_material=wall_back_material )
                                        
                    w = Wall( quad.GetX() - ( quad.size / 1.975 ), 
                              quad.GetZ() - ( quad.size / 1.75 ), 
                              self.Scene,
                              wall_position=WALL_LEFT,
                              
                              front_material=wall_front_material,
                              back_material=wall_back_material)

                    
                elif quad.quadType == "b":
                    w = Wall( quad.GetX() - ( quad.size / 1.975 ), 
                              quad.GetZ() - ( quad.size / 1.75 ), 
                              self.Scene,
                              front_material=wall_front_material,
                              back_material=wall_back_material )
                                        
                    w = Wall( quad.GetX() - ( quad.size / 1.975 ), 
                              quad.GetZ() - ( quad.size / 1.75 ), 
                              self.Scene,
                              wall_position=WALL_RIGHT,
                              
                              front_material=wall_front_material,
                              back_material=wall_back_material)
                elif quad.quadType == "c":
                    if hasattr( self, "walls"):
                        pass
##                        ConcatenateObject( quad + Vector3d( -0.001, altitude, 0.225 ), w, self.AssetManager.GetObject( "WALL0" ) )
##                        ConcatenateObject( quad + Vector3d( 0.225, altitude, -0.001 ), w, self.AssetManager.GetObject( "WALL90" ) )
                    else:
                        pass
##                        self.walls = w = self.AssetManager.GetObject( "WALL0" ).Clone()
##                        TranslateVertexArray( self.walls, quad + Vector3d( 0.0, 0.0, 0.0 ) )
                elif quad.quadType == "d":
                    if hasattr( self, "walls"):
                        pass
##                        ConcatenateObject( quad + Vector3d( -0.225, altitude, -0.005 ), w, self.AssetManager.GetObject( "WALL90" ) )
##                        ConcatenateObject( quad + Vector3d( 0.01, altitude, 0.225 ), w, self.AssetManager.GetObject( "WALL0" ) )
                    else:
                        pass
##                        self.walls = w = self.AssetManager.GetObject( "WALL_CORNER_BL" ).Clone()
##                        TranslateVertexArray( self.walls, quad + Vector3d( 0.0, 0.0, 0.0 ) )
                elif quad.quadType == "A":
                    if hasattr( self, "walls"):
                        pass
##                        ConcatenateObject( quad , w, self.AssetManager.GetObject( "WALL0" ) )
                    else:
                        pass
##                        self.walls = w = self.AssetManager.GetObject( "WALL0" ).Clone()
##                        TranslateVertexArray( self.walls, quad + Vector3d( 0.0, 0.0, 0.0 ) )
                elif quad.quadType == "B":
                    if hasattr( self, "walls"):
                        pass
##                        ConcatenateObject( quad , w, self.AssetManager.GetObject( "WALL0" ) )
                    else:
                        pass
##                        self.walls = w = self.AssetManager.GetObject( "WALL0" ).Clone()
##                        TranslateVertexArray( self.walls, quad + Vector3d( 0.0, 0.0, 0.0 ) )
                elif quad.quadType == "C":
                    if hasattr( self, "walls"):
                        pass
##                        ConcatenateObject( quad , w, self.AssetManager.GetObject( "WALL0" ) )
                    else:
                        pass
##                        self.walls = w = self.AssetManager.GetObject( "WALL0" ).Clone()
##                        x, y, z, w_pos = self.GetPosition()
##                        TranslateVertexArray( self.walls, quad + Vector3d( 0.0, 0.0, 0.0 ) )
                elif quad.quadType == "D":
                    if hasattr( self, "walls"):
                        pass
##                        ConcatenateObject( quad , w, self.AssetManager.GetObject( "WALL0" ) )
                    else:
                        pass
##                        self.walls = w = self.AssetManager.GetObject( "WALL0" ).Clone()
##                        x, y, z, w_pos = self.GetPosition()
##                        TranslateVertexArray( self.walls, quad + Vector3d( 0.0, 0.0, 0.0 ) )
                elif quad.quadType == "L":
                    w = Wall( quad.GetX() - ( quad.size / 1.975 ), 
                              quad.GetZ() - ( quad.size / 1.75 ), 
                              self.Scene,
                              wall_position=WALL_RIGHT,
                              
                              front_material=wall_front_material,
                              back_material=wall_back_material)
                    
                elif quad.quadType == "R":
                    w = Wall( quad.GetX() - ( quad.size / 1.975 ), 
                              quad.GetZ() - ( quad.size / 1.75 ), 
                              self.Scene,
                              wall_position=WALL_LEFT,
                              
                              front_material=wall_front_material,
                              back_material=wall_back_material)
                    
                elif quad.quadType == "l":
                    w = Wall( quad.GetX() - ( quad.size / 1.975 ), 
                              quad.GetZ() - ( quad.size / 1.75 ), 
                              self.Scene,
                              front_material=wall_front_material,
                              back_material=wall_back_material )
                    
                elif quad.quadType == "h":
                    w = Wall( quad.GetX() - ( quad.size / 1.975 ), 
                              quad.GetZ() - ( quad.size / 1.75 ), 
                              self.Scene,
                              wall_position=WALL_BACK,
                              
                              front_material=wall_front_material,
                              back_material=wall_back_material)
##            x, y, z, w = self.GetPosition()
##            self.walls.SetPosition( x, y, z )
##            
##            if self.wallTextureID: self.walls.SetTexture( self.wallTextureID )
                           
        def Draw( self ):
            self._draw()
            if self.ShowWalls:
                self.walls.Draw()
                
        def ToggleWalls( self ):
            self.ShowWalls = not self.ShowWalls
        
                
            
        