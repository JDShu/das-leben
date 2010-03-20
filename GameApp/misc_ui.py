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
from vector_3d import *
from ogl_va import VA
import pygame
import numpy
from numpy import *

class TexturedRect( Vector3d ):
    '''a textured rectangle'''
    def __init__( self, a_TextureFilename, a_Position, a_Width, a_Height ):
        self.m_Values = a_Position.m_Values
        self.m_Width = a_Width
        self.m_Height = a_Height
        
        

        if a_TextureFilename.upper().endswith( '.SVG' ):
            pass
        else:
            textureSurface = pygame.image.load( a_TextureFilename )

            textureData = pygame.image.tostring( textureSurface, "RGBA", 1 )

            width = textureSurface.get_width()
            height = textureSurface.get_height()

            self.m_Texture = glGenTextures( 1 )
            glBindTexture( GL_TEXTURE_2D, self.m_Texture )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
            glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData )
            
    

    def Draw( self ):
        glEnable( GL_TEXTURE_2D )
        glBindTexture( GL_TEXTURE_2D, self.m_Texture )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glEnable(GL_BLEND)
        
        glTranslate( self.GetX(), self.GetY(), self.GetZ() )
        glBegin(GL_QUADS)
        glColor(1, 1, 1, 1)
        glTexCoord2f(0.0, 0.0)
        glVertex2f( 0, 0 )
        glTexCoord2f(1.0, 0.0)
        glVertex2f( self.m_Width, 0 )
        
        glTexCoord2f(1.0, 1.0)
        glVertex2f( self.m_Width, self.m_Height )
        glTexCoord2f(0.0, 1.0)
        glVertex2f( 0, self.m_Height )
        glEnd()
        glDisable( GL_TEXTURE_2D )
        
class SelectedRegion:
    def __init__( self, a_StepWidth, a_Altitude, a_StartPosition, a_EndPosition, a_StartTicks):
        self.m_Start = a_StartPosition
        self.m_End = a_EndPosition
        self.SetStartTicks( a_StartTicks )
        self.m_Enabled = False
        self.m_StepWidth = a_StepWidth
        self.m_Altitude = a_Altitude
        self.m_Editing = False
        self.m_Position = a_StartPosition
        vertexes = self.CreateVertexes( a_StartPosition, a_EndPosition )
        
        normals = []; nadd = normals.append
        nadd( array( [ 0.0, 1.0, 0.0 ], dtype=float32 ) )
        nadd( array( [ 0.0, 1.0, 0.0 ], dtype=float32 ) )
        nadd( array( [ 0.0, 1.0, 0.0 ], dtype=float32 ) )
        nadd( array( [ 0.0, 1.0, 0.0 ], dtype=float32 ) )
        
        texcoords = []; tadd = texcoords.append 
        tadd( array( [ 0.0, 0.0 ], dtype=float32 ) )
        tadd( array( [ 1.0, 0.0 ], dtype=float32 ) )
        tadd( array( [ 1.0, 1.0 ], dtype=float32 ) )
        tadd( array( [ 0.0, 1.0 ], dtype=float32 ) )
        
        colours = []; cadd = colours.append
        cadd( array( [ 0.0, 1.0, 1.0 ], dtype=float32 ) )
        cadd( array( [ 0.0, 1.0, 1.0 ], dtype=float32 ) )
        cadd( array( [ 0.0, 1.0, 1.0 ], dtype=float32 ) )
        cadd( array( [ 0.0, 1.0, 1.0 ], dtype=float32 ) )
        
        self.m_VA = VA( vertexes, normals, None, texcoords, colours )
        
    def BeginEditing(self ):
        self.m_Editing = True
        
    def IsEditing( self ):
        return self.m_Editing
    
    def EndEditing( self ):
        self.m_Editing = False
        
    def GetStartTicks( self ):
        return self.m_StartTicks
    
    def SetStartTicks( self, a_Ticks ):
        self.m_StartTicks = a_Ticks
        
    def CreateVertexes( self, a_StartPosition, a_EndPosition ):
        vertexes = zeros( ( 4, 3 ), dtype=float32 )
        vertexes[ 0 ] = array( [ a_StartPosition.GetX(), self.m_Altitude, a_StartPosition.GetZ() ], dtype=float32 ) 
        vertexes[ 1 ] = array( [ a_EndPosition.GetX(), self.m_Altitude, a_StartPosition.GetZ() ], dtype=float32 ) 
        vertexes[ 2 ] = array( [ a_EndPosition.GetX(), self.m_Altitude, a_EndPosition.GetZ() ], dtype=float32 ) 
        vertexes[ 3 ] = array( [ a_StartPosition.GetX(), self.m_Altitude, a_EndPosition.GetZ() ], dtype=float32 ) 
        
        return vertexes
    
    def UpdateEnd( self, a_EndPosition ):
        self.m_End = a_EndPosition
        vertexes = self.CreateVertexes( self.m_Start, a_EndPosition )
        self.m_VA.vertexes = vertexes
        
    def SetBegin( self, a_StartPosition, a_EndPosition ):
        self.m_Start = a_StartPosition
        vertexes = self.CreateVertexes( a_StartPosition, a_EndPosition )
        self.m_VA.vertexes = vertexes
        
    def GetGranularDimensions( self, a_Granularity ):
        '''
        calculate the width and height of the selected area
        based on how wide the squares are that the area needs 
        chopping into.
        '''
        l_Dimentions = AreaDimensions()
        l_Dimentions.width = abs( int( ( self.m_Start.GetX() - self.m_End.GetX() ) / a_Granularity ) )
        l_Dimentions.height = abs( int( ( self.m_Start.GetZ() - self.m_End.GetZ() ) / a_Granularity ) )
        
        # work out which it the best place to set as the position
        x1, y1, z1, w = self.m_Start.GetPosition()
        x2, y2, z2, w = self.m_End.GetPosition()
        new_x = x1 < x2 and x1 or x2
        new_z = z1 < z2 and z1 or z2
        # now set the best position for a region to be placed
        self.m_Position.SetPosition( new_x, y1, new_z )
        
        return l_Dimentions
        
    def Draw( self ):
        if self.m_Enabled:
            glDisable( GL_DEPTH_TEST )
            self.m_VA.Draw()
            glEnable( GL_DEPTH_TEST )
            
class AreaDimensions:
            width = 0
            height = 0
    