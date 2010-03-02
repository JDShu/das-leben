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
import pygame

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
        
