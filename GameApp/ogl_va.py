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

import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from ctypes import *

import sys

try:
    from OpenGL.GL.ARB.vertex_buffer_object import *
except: 
    print "You need PyOpenGL >= 3.0 to run this program, your current version is %s" % (OpenGL.__version__)
    sys.exit(1)

from numpy import *
import pygame

class VA:
    '''A vertex array handling class'''
    def __init__( self, a_Vertexes, a_Normals=None, a_Indices=None, a_TexCoords=None, a_Colours=None, a_Quads=True ):
        '''
        create a vbo from a list of face points, normals, texture coords and colours
        '''
        self.vertxCount = len( a_Vertexes )
        self.vertexes = zeros( ( len( a_Vertexes ), 3 ), dtype=float32 ) 
        
        for i, vert in enumerate( a_Vertexes ):
            self.vertexes[ i ][ 0 ] = vert.GetX()
            self.vertexes[ i ][ 1 ] = vert.GetY()
            self.vertexes[ i ][ 2 ] = vert.GetZ()
        
        self.useNormals = a_Normals != None and True or False
        if self.useNormals:
            self.normals = zeros( ( len( a_Normals ), 3 ), dtype=float32 ) 
            for i, vert in enumerate( a_Normals ):
                self.normals[ i ][ 0 ] = vert.GetX()
                self.normals[ i ][ 1 ] = vert.GetY()
                self.normals[ i ][ 2 ] = vert.GetZ()
                
        self.useIndices = a_Indices != None and True or False
        if self.useIndices:
            self.indices = a_Indices
            
        self.useTexCoords = a_TexCoords != None and True or False
        if self.useTexCoords:
            self.texCoords = zeros( ( len( a_TexCoords ), 3 ), dtype=float32 ) 
            for i, vert in enumerate( a_TexCoords ):
                self.texCoords[ i ][ 0 ] = vert.GetX()
                self.texCoords[ i ][ 1 ] = vert.GetY()
                self.texCoords[ i ][ 2 ] = vert.GetZ()
                            
        self.useColoursCoords = a_Colours != None and True or False
        if self.useColoursCoords:
            self.coloursCoords = zeros( ( len( a_Colours ), 3 ), dtype=float32 ) 
            for i, vert in enumerate( a_Colours ):
                self.coloursCoords[ i ][ 0 ] = vert[ 0 ]
                self.coloursCoords[ i ][ 1 ] = vert[ 1 ]
                self.coloursCoords[ i ][ 2 ] = vert[ 2 ]
            
        self.Facetype = a_Quads == True and GL_QUADS or GL_TRIANGLES
            
    def Draw( self ):
        
        glEnableClientState( GL_VERTEX_ARRAY )
        if self.useNormals: glEnableClientState( GL_NORMAL_ARRAY )
        if self.useTexCoords: glEnableClientState( GL_TEXTURE_COORD_ARRAY )
        if self.useColoursCoords: glEnableClientState( GL_COLOR_ARRAY )
        
        if self.useNormals: glNormalPointer( GL_FLOAT, 0, self.normals )
        if self.useTexCoords: glTexCoordPointer( 2, GL_FLOAT, 0, self.texCoords )
        if self.useColoursCoords:glColorPointer( 3, GL_FLOAT, 0, self.coloursCoords )
        glVertexPointer(3, GL_FLOAT, 0, self.vertexes )
        
        if not self.useIndices:
            glDrawArrays( self.Facetype, 0, self.vertxCount )
        else:
            glDrawElements( self.Facetype, len( self.indices ), GL_UNSIGNED_SHORT, self.indices )

        glDisableClientState( GL_VERTEX_ARRAY )
        
        if self.useNormals: glDisableClientState( GL_NORMAL_ARRAY )
            
        if self.useTexCoords: glDisableClientState( GL_TEXTURE_COORD_ARRAY )
        
        if self.useColoursCoords: glDisableClientState( GL_COLOR_ARRAY )
        
    Render = Draw
    
    def GetVertexArray( self ):
        return self.vertexes
    
    def GetVertexPoint( self, offset ):
        return self.vertexes[ offset ]
    
    def SetVertex( self, start_offset, vertex ):
        self.vertexes[ start_offset ] = vertex
        
        