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

class TexturedRect( Vector3d ):
    '''a textured rectangle'''
    def __init__( self, a_TextureFilename, a_Position, a_Width, a_Height ):
        self.m_Values = a_Position.m_Values
        self.m_Width = a_Width
        self.m_Height = a_Height

        if a_TextureFilename.upper.endswith( '.SVG' ):
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
        glMatrixMode( GL_PROJECTION )
        glPushMatrix()
        glLoadIdentity()
        viewport = glGetIntegerv( GL_VIEWPORT )
        gluOrtho2D( viewport[0],viewport[2],viewport[1],viewport[3] )
        glMatrixMode( GL_MODELVIEW )
        glPushMatrix()
        glLoadIdentity()

        glEnable( GL_TEXTURE_2D )
        glBindTexture( self.m_Texture )
        glTranslatef( self.m_Position.GetX(), ( self.m_Position.GetY() - self.m_Height ), self.m_Position.GetZ() )
        glBegin(GL_QUADS)
        glColor4f( 1.0, 1.0, 1.0, 1.0 )
        glVertex2f( self.m_Position.GetX() - self.m_Width/2, ( self.m_Position.GetY() - self.m_Height ) - self.m_Height/2 )
        glVertex2f( self.m_Position.GetX() + self.m_Width/2, ( self.m_Position.GetY() - self.m_Height ) - self.m_Height/2 )
        glVertex2f( self.m_Position.GetX() + self.m_Width/2, ( self.m_Position.GetY() - self.m_Height ) + self.m_Height/2 )
        glVertex2f( self.m_Position.GetX() - self.m_Width/2, ( self.m_Position.GetY() - self.m_Height ) + self.m_Height/2 )
        glEnd()
        glDisable( GL_TEXTURE_2D )
        glMatrixMode( GL_PROJECTION )
        glPopMatrix()
        glMatrixMode( GL_MODELVIEW )
        glPopMatrix()
