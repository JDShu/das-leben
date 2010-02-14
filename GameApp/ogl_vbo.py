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

class VBO:
    def __init__( self, a_Vertexes, a_Normals=None, a_TexCoords=None, a_Colours=None, a_Quads=True, a_BufferType=GL_STATIC_DRAW_ARB ):
        '''
        create a vbo from a list of face points, normals, texture coords and colours
        '''
        self.vertxCount = len( a_Vertexes )
        vertexes = zeros( ( len( a_Vertexes ), 3 ), dtype=float32 ) 
        
        for i, vert in enumerate( a_Vertexes ):
            vertexes[ i ][ 0 ] = vert.GetX()
            vertexes[ i ][ 1 ] = vert.GetY()
            vertexes[ i ][ 2 ] = vert.GetZ()
            
        self.vboVertArray = glGenBuffersARB( 1 )
        glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.vboVertArray )
        glBufferDataARB( GL_ARRAY_BUFFER_ARB, vertexes, a_BufferType )
        
        self.useNormals = a_Normals != None and True or False
        if self.useNormals:
            normals = zeros( ( len( a_Normals ), 3 ), dtype=float32 ) 
            for i, vert in enumerate( a_Normals ):
                normals[ i ][ 0 ] = vert.GetX()
                normals[ i ][ 1 ] = vert.GetY()
                normals[ i ][ 2 ] = vert.GetZ()
                
            self.vboNormalArray = glGenBuffersARB( 1 )
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.vboNormalArray )
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, normals, a_BufferType )
            
        self.useTexCoords = a_TexCoords != None and True or False
        if self.useTexCoords:
            texCoords = zeros( ( len( a_TexCoords ), 3 ), dtype=float32 ) 
            for i, vert in enumerate( a_TexCoords ):
                texCoords[ i ][ 0 ] = vert.GetX()
                texCoords[ i ][ 1 ] = vert.GetY()
                texCoords[ i ][ 2 ] = vert.GetZ()
                
            self.vboTexCoordArray = glGenBuffersARB( 1 )
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.vboTexCoordArray )
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, texCoords, GL_STATIC_DRAW_ARB )
            
        self.useColoursCoords = a_Colours != None and True or False
        if self.useColoursCoords:
            coloursCoords = zeros( ( len( a_Colours ), 3 ), dtype=float32 ) 
            for i, vert in enumerate( a_Colours ):
                coloursCoords[ i ][ 0 ] = vert[ 0 ]
                coloursCoords[ i ][ 1 ] = vert[ 1 ]
                coloursCoords[ i ][ 2 ] = vert[ 2 ]
                
            self.vbocColourCoordsArray = glGenBuffersARB( 1 )
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.vbocColourCoordsArray )
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, coloursCoords, GL_STATIC_DRAW_ARB )
            
        self.Facetype = a_Quads == True and GL_QUADS or GL_TRIANGLES
            
    def Draw( self ):
        glEnableClientState( GL_VERTEX_ARRAY )
        glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.vboVertArray )
        glVertexPointer( 3, GL_FLOAT, 0, None )
        
        if self.useNormals: 
            glEnableClientState( GL_NORMAL_ARRAY )
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.vboNormalArray )
            glNormalPointer( GL_FLOAT, 0, None )
            
        if self.useTexCoords: 
            glEnableClientState( GL_TEXTURE_COORD_ARRAY )
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.vboTexCoordArray )
            glTexCoordPointer( 2, GL_FLOAT, 0, None )

        if self.useColoursCoords: 
            glEnableClientState( GL_COLOR_ARRAY )
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.vbocColourCoordsArray )
            glColorPointer(3, GL_FLOAT, 0, None)
            
        glDrawArrays( self.Facetype, 0, self.vertxCount )

        glDisableClientState( GL_VERTEX_ARRAY )
        
        if self.useNormals: glDisableClientState( GL_NORMAL_ARRAY )
            
        if self.useTexCoords: glDisableClientState( GL_TEXTURE_COORD_ARRAY )
        
        if self.useColoursCoords: glDisableClientState( GL_COLOR_ARRAY )
        
    Render = Draw
    
    def GetVertexArray( self ):
        glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.vboVertArray )
        func = ctypes.pythonapi.PyBuffer_FromMemory
        func.restype = ctypes.py_object
        vp = glMapBufferARB( GL_ARRAY_BUFFER_ARB, GL_WRITE_ONLY )
        buffer = func( 
            ctypes.c_void_p(vp), self.vertxCount * 3 
        )
        array = frombuffer( buffer, dtype=float32 )
        return array
    
    def FinishUsingVertexArray( self ):
        glUnmapBufferARB( GL_ARRAY_BUFFER_ARB )
    
    def __del__( self ):
        glDeleteBuffersARB( 1, self.vboVertArray )
        if self.useNormals: glDeleteBuffersARB( 1, self.vboNormalArray )
        if self.useTexCoords: glDeleteBuffersARB( 1, self.vboTexCoordArray )
        if self.useColoursCoords: glDeleteBuffersARB( 1, self.vbocColourCoordsArray )
        