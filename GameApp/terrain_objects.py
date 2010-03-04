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

REGION_NORMAL = 1
REGION_EDITING = 2

# which parts of the height values to change
quad_adjustments = []; qadd = quad_adjustments.append
# first row
qadd( { 'ul': 0.0, 'ur': 1.0, 'll': 0.0, 'lr': 0.0, 'name':'top left' } )
qadd( { 'ul': 1.0, 'ur': 1.0, 'll': 0.0, 'lr': 0.0, 'name':'top middle' } )
qadd( { 'ul': 1.0, 'ur': 0.0, 'll': 0.0, 'lr': 0.0, 'name':'top right' } )
# second row
qadd( { 'ul': 0.0, 'ur': 1.0, 'll': 0.0, 'lr': 1.0, 'name':'middle left' } )
qadd( { 'ul': 0.0, 'ur': 0.0, 'll': 0.0, 'lr': 0.0, 'name':'middle middle' } )
qadd( { 'ul': 1.0, 'ur': 0.0, 'll': 1.0, 'lr': 0.0, 'name':'middle right' } )
# third row
qadd( { 'ul': 0.0, 'ur': 0.0, 'll': 0.0, 'lr': 1.0, 'name':'bottom left' } )
qadd( { 'ul': 0.0, 'ur': 0.0, 'll': 1.0, 'lr': 1.0, 'name':'bottom middle' } )
qadd( { 'ul': 0.0, 'ur': 0.0, 'll': 1.0, 'lr': 0.0, 'name':'bottom right' } )

class RegionQuad( BoundingBox3d ):
    def __init__( self, a_X=0.0, a_Y=0.0, a_Z=0.0, a_Size=0.5 ):
        BoundingBox3d.__init__( self, a_X + (a_Size / 2.0), a_Y, a_Z + (a_Size / 2.0), a_Size )
        
        # y values for quad
        self.ul = None
        self.ur = None
        self.ll = None
        self.lr = None
        
        # vertex array index for when we are shaping the region later
        self.va_index = 0
        self.i = 0
        
        # quad size
        self.size = a_Size
        
        self.selected = False
        self.compiled = False
        self.oldListID = 0
        self.listID = 0     
        
        self.colour_adjust = random.random()
        
    def __repr__( self ):
        return "ll:%s,lr:%s,ul:%s,ur:%s" % ( self.ll, self.lr , self.ul, self.ur)
        
       
    def SetAsObject( self, a_Object3d ):
        self.ObjectToRender = a_Object3d
        self.ObjectToRender.SetPosition( self.GetX(), self.GetY(), self.GetY() )
        
    def GetGLName( self ):
        return self.ObjectToRender.GetGLName()
        
    def makeList( self ):
        return [ self.ll, self.lr, self.ur, self.ul ]
        
    def compile_list( self ):
        if not self.compiled:
            self.listID = glGenLists( 1 )
            glNewList( self.listID, GL_COMPILE )
            
            
            self.Draw()
            glEndList()
            
    def recompile_list( self ):
        self.oldListID = self.listID
        glDeleteLists( self.listID, 1 )
        self.compile_list()
        
    def __del__( self ):
        glDeleteLists( self.listID, 1 )
    
    
class Region( Vector3d ):
    def __init__( self, a_X=0.0, a_Y=0.0, a_Z=0.0, a_Width=50, a_Size=0.5, a_Colour=0.5 ):
        Vector3d.__init__( self, a_X, a_Y, a_Z )
        self.quads = []; qadd = self.quads.append
        self.quadIDS = []; iadd = self.quadIDS.append
        
        self.m_Width = a_Width
        self.m_Size = a_Size
        
        for z in xrange( a_Width ):
            for x in xrange( a_Width ):
                rq = RegionQuad( a_X + ( float( x ) * a_Size ), 
                                  a_Y, 
                                  a_Z + ( float( z ) * a_Size ),
                                  a_Size ) 
                rq.SetAsObject( Object3d() )
                
                # rq.compile_list()
                
                qadd( rq )
                iadd( rq.listID )
                
        self.vertexes = []; vadd = self.vertexes.append
        colours = []; cadd = colours.append
        normals = []; nadd = normals.append
        indexes = []; ixadd = indexes.append
        
        for z in xrange( a_Width + 1 ):
            for x in xrange( a_Width + 1):
                extra_light = random.uniform( 0.25, 0.4 )
                vadd( Vector3d( float( x ) * a_Size, a_Y, float( z ) * a_Size ) )
                nadd( Vector3d( 0.0, .737, 0.0 ) )
                cadd( [ a_Colour - extra_light, a_Colour, a_Colour - extra_light ] )
                
                if x < a_Width and z < a_Width:
                    ixadd( int( ( z * ( a_Width + 1 ) ) + x ) )
                    ixadd( int( ( z * ( a_Width + 1 ) ) + ( x + 1 ) ) )
                    ixadd( int( ( ( z + 1 ) * ( a_Width + 1 ) ) + ( x + 1 ) ) )
                    ixadd( int( ( ( z + 1 ) * ( a_Width + 1 ) ) + x ) )
                
        for i, rq in enumerate( self.quads ):
            rq.ll = indexes[ i * 4 ]
            rq.lr = indexes[ ( i * 4 ) + 1 ]
            rq.ur = indexes[ ( i * 4 ) + 2 ]
            rq.ul = indexes[ ( i * 4 ) + 3 ]
            
        
        # now generate a vertex array for opengl
        va_vertexes = []; vadd = va_vertexes.append
        va_colours = []; cadd = va_colours.append
        va_normals = []; nadd = va_normals.append
        f = open( "debug.log", "w" )
        for i, rq in enumerate( self.quads ):
            rq.va_index = i * 4 # index to first vertex of the quad
            rq.i = i
            vadd( self.vertexes[ rq.ll ] )
            vadd( self.vertexes[ rq.lr ] )
            vadd( self.vertexes[ rq.ur ] )
            vadd( self.vertexes[ rq.ul ] )
            f.write( "quad %s: %s, %s, %s, %s\n" % ( i, rq.ll, rq.lr, rq.ur, rq.ul ) )
            #normals
            nadd( normals[ rq.ll ] )
            nadd( normals[ rq.lr ] )
            nadd( normals[ rq.ur ] )
            nadd( normals[ rq.ul ] )
            #colours
            cadd( colours[ rq.ll ] )
            cadd( colours[ rq.lr ] )
            cadd( colours[ rq.ur ] )
            cadd( colours[ rq.ul ] )
            
        f.close()
        
        self.va = VA( va_vertexes, va_normals, None, None, va_colours )
        self.useVBO = True
        self.mode = REGION_NORMAL
        
        self.selected_quads = []
        
        self.m_ObjectType = OBJECT_3D_MESH
        self.listID = None
        #self.compile_list()
        
        self.compiled = False
        
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
        
    def Load( self, a_Filename ):
        self.DeleteAllQuads()
        
        f = open( a_Filename, "r" )
        lines = f.read()
        
        self.quads = []; qadd = self.quads.append
        self.quadIDS = []; iadd = self.quadIDS.append
        for x in xrange( self.m_Width ):
            for z in xrange( self.m_Width ):
                rq = RegionQuad( self.GetX() + ( float( x ) * self.m_Size ), 
                                  self.GetY(), 
                                  self.GetZ() + ( float( z ) * self.m_Size ),
                                  self.m_Size ) 
                rq.SetAsObject( Object3d() )
                line = lines[ ( x * self.m_Width ) + z ]
                parts = line.split(",")
                heights = {}
                for part in parts:
                    key, value = part.split(":")
                    heights[ key ] = value
                    
                rq.SetHeights( heights )
                rq.compile_list()
                
                qadd( rq )
                iadd( rq.listID )
        
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
        glTranslatef( self.GetX(), self.GetY(), self.GetZ() )
        
        if not self.useVBO:
            glCallList( self.listID )
        else:
            self.va.Draw()
        
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
            if iz > 0 and iz < self.m_Width:
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
                        
        
       
##        self.recompile_list()
        
    def lowerQuads( self, a_Begin, a_End ):
        pass
##        for x in xrange( self.m_Width ):
##            for z in xrange( self.m_Width ):
##                quad = self.quads[ ( x * self.m_Width ) + z ]
##                if quad.PointInsideXZPlane( a_Location ):
##                    
##                    quad.colour_adjust = 0.01
##                    xco, yco, zco, wco = quad.GetPosition() 
##                    yco -= float( self.m_Size ) / 5.0 
##                    quad.SetPosition( xco, yco, zco )
##                    
##                    cur_x = x - 1
##                    cur_z = z - 1
##                    
##                    for u in xrange( 3 ):
##                        for v in xrange( 3 ):
##                            try:
##                                adjusted_quad = self.quads[ ( cur_x * self.m_Width ) + cur_z ]
##                                line = adjusted_quad.__repr__()
##                                parts = line.split(",")
##                                heights = {}
##                                adjustment = quad_adjustments[ ( u * 3 ) + v ]
##                                if adjustment[ 'name' ] == "middle middle": 
##                                    adjusted_quad = quad
##                                for part in parts:
##                                    key, value = part.split(":")
##                                    heights[ key ] = float( value ) - ( float( adjustment[ key ] ) * float( self.m_Size / 5.0 ) )
##                                adjusted_quad.SetHeights( heights )
##                                
##                                    
##                                #adjusted_quad.recompile_list()
##                                self.quadIDS[ self.quadIDS.index( adjusted_quad.oldListID ) ] = adjusted_quad.listID
##                            except:
##                                pass
##                            
##                            cur_x += 1
##                            
##                        cur_x -= 3
##                        cur_z += 1
##                        
##                    
##                    #quad.recompile_list()
##                    self.quadIDS[ self.quadIDS.index( quad.oldListID ) ] = quad.listID
##                    
##        
##    
##            
##        
##        self.recompile_list()
        
    def getQuad( self, a_X, a_Z ):
        try:
            self.quads[ ( a_X * self.m_Width ) + a_Z ]
        except:
            pass
        return quad
        
        
class TerrainRegion( Region ):
    def __init__( self, a_X=0.0, a_Y=0.0, a_Z=0.0, a_Width=50, a_Size=0.5 ):
        Region.__init__( self, a_X, a_Y, a_Z, a_Width, a_Size )
        
    def Draw( self ):
        glEnable( GL_FOG )
        self._draw()
        glDisable( GL_FOG ) 
        
    
        
class TerrainGridedRegion( TerrainRegion ):
    def __init__( self, a_X=0.0, a_Y=0.0, a_Z=0.0, a_Width=50, a_Size=0.5 ):
        TerrainRegion.__init__( self, a_X, a_Y, a_Z, a_Width, a_Size )
        self.m_Grid = Region( a_X, a_Y + 0.5, a_Z, a_Width, a_Size, a_Colour=0.8 )
        
    def Draw( self ):
        self.Draw()
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
        self.m_Grid._draw()
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
        