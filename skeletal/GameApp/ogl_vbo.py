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
from OpenGL.arrays import vbo
from ctypes import *
from vector_3d import Vector3d
from numpy import *
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

        min_x = 1000000.0
        max_x = -1000000.0
        min_y = 1000000.0
        max_y = -1000000.0
        min_z = 1000000.0
        max_z = -1000000.0

        for i, vert in enumerate( a_Vertexes ):
            if hasattr( vert, "GetX" ):
                vertexes[ i ][ 0 ] = vert.GetX()
                vertexes[ i ][ 1 ] = vert.GetY()
                vertexes[ i ][ 2 ] = vert.GetZ()
            else:
                vertexes[ i ] = vert

            if vertexes[ i ][0] < min_x: min_x = vertexes[ i ][ 0 ]
            if vertexes[ i ][0] > max_x: max_x = vertexes[ i ][ 0 ]
            if vertexes[ i ][1] < min_y: min_y = vertexes[ i ][ 1 ]
            if vertexes[ i ][1] > max_y: max_y = vertexes[ i ][ 1 ]
            if vertexes[ i ][2] < min_z: min_z = vertexes[ i ][ 2 ]
            if vertexes[ i ][2] > max_z: max_z = vertexes[ i ][ 2 ]

        self.m_Dimensions = array( [ max_x - min_y, max_y - min_y, max_z - min_z ], dtype=float32 )
        self.vboVertArray = glGenBuffersARB( 1 )
        glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.vboVertArray )
        glBufferDataARB( GL_ARRAY_BUFFER_ARB, vertexes, a_BufferType )

        self.useNormals = a_Normals != None and True or False
        if self.useNormals:
            normals = zeros( ( len( a_Normals ), 3 ), dtype=float32 ) 
            for i, vert in enumerate( a_Normals ):
                if hasattr( vert, "GetX" ):
                    normals[ i ][ 0 ] = vert.GetX()
                    normals[ i ][ 1 ] = vert.GetY()
                    normals[ i ][ 2 ] = vert.GetZ()
                else:
                    normals[ i ] = vert

            self.vboNormalArray = glGenBuffersARB( 1 )
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.vboNormalArray )
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, normals, a_BufferType )

        self.useTexCoords = a_TexCoords != None and True or False
        if self.useTexCoords:
            texCoords = zeros( ( len( a_TexCoords ), 2 ), dtype=float32 ) 
            for i, vert in enumerate( a_TexCoords ):
                if hasattr( vert, "GetX" ):
                    texCoords[ i ][ 0 ] = vert.GetX()
                    texCoords[ i ][ 1 ] = vert.GetY()
                else:
                    texCoords[ i ] = vert

            self.vboTexCoordArray = glGenBuffersARB( 1 )
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.vboTexCoordArray )
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, texCoords, GL_STATIC_DRAW_ARB )

        self.useColoursCoords = a_Colours != None and True or False
        if self.useColoursCoords:
            coloursCoords = zeros( ( len( a_Colours ), 3 ), dtype=float32 ) 
            for i, vert in enumerate( a_Colours ):
                if hasattr( vert, "GetX" ):
                    coloursCoords[ i ][ 0 ] = vert[ 0 ]
                    coloursCoords[ i ][ 1 ] = vert[ 1 ]
                    coloursCoords[ i ][ 2 ] = vert[ 2 ]
                else:
                    coloursCoords[ i ] = vert

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
        vp = glMapBufferARB( GL_ARRAY_BUFFER_ARB, GL_READ_WRITE_ARB )
        buffer = func( 
            ctypes.c_void_p(vp), self.vertxCount * 3 
        )
        array = frombuffer( buffer, dtype=float32 )
        return array

    def SetVertex( self, start_offset, vertexes ):
        glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
        offset = start_offset * 12
        glBufferSubData( GL_ARRAY_BUFFER, offset, numpy.array([0.5, 1.5, 1.5], 'f' ) )


    def FinishUsingVertexArray( self ):
        glUnmapBufferARB( GL_ARRAY_BUFFER_ARB )
        glPopClientAttrib()  

    def GetDimensions( self ):
        return self.m_Dimensions

    def __del__( self ):
        glDeleteBuffersARB( 1, self.vboVertArray )
        if self.useNormals: glDeleteBuffersARB( 1, self.vboNormalArray )
        if self.useTexCoords: glDeleteBuffersARB( 1, self.vboTexCoordArray )
        if self.useColoursCoords: glDeleteBuffersARB( 1, self.vbocColourCoordsArray )

class NewVBO( Vector3d ):
    def __init__( self, a_X=0.0, a_Y=0.0, a_Z=0.0, a_W=1.0, data=None):
        Vector3d.__init__( self, a_X, a_Y, a_Z, a_W )

        if not data == None:
            self.vbo = vbo.VBO( array( data ,'f' ) )
        else:
            self.vbo = vbo.VBO(
                array( [
                    [  0, 1, 0 ],
                    [ -1,-1, 0 ],
                    [  1,-1, 0 ],
                    [  2,-1, 0 ],
                    [  4,-1, 0 ],
                    [  4, 1, 0 ],
                    [  2,-1, 0 ],
                    [  4, 1, 0 ],
                    [  2, 1, 0 ],
                    ],'f')

            )

    def Draw( self ):

        self.vbo.bind()
        stride = 9*4
##	glVertexAttribPointer( 
##                        self.position_location, 
##                        3, GL_FLOAT,False, stride, self.vbo 
##                )
##	glVertexAttribPointer( 
##                        self.tweened_location, 
##                        3, GL_FLOAT,False, stride, self.vbo+12
##                )
##	glVertexAttribPointer( 
##                        self.color_location, 
##                        3, GL_FLOAT,False, stride, self.vbo+24
##                )

        glEnableClientState( GL_VERTEX_ARRAY )
        glVertexPointerf( self.vbo )
        glDrawArrays(GL_TRIANGLES, 0, 9)

        self.vbo.unbind()
        glDisableClientState( GL_VERTEX_ARRAY )