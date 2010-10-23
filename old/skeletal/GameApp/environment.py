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

class SkyBox:
    def __init__(self, texturePath=None):
        self.m_Skybox = []; sadd = self.m_Skybox.append
        
     
        self.m_Textures = glGenTextures(6)
        for i in range(6):
            self.LoadTexture( "%s/section_%s.bmp" % ( texturePath, ( i + 1 ) ), i )
            
    def LoadTexture(self, filename, textur_id):
        textureSurface = pygame.image.load(filename)
 
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
     
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        
        glBindTexture(GL_TEXTURE_2D, self.m_Textures[ textur_id ])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        
    def Draw(self, camera):
        # Store the current matrix
        glPushMatrix()
    
        # Reset and transform the matrix.
        glLoadIdentity()
        '''gluLookAt( 0,0,0,
                   camera.GetX(),camera.GetY(),camera.GetZ(),
                   0,1,0)'''
        glRotatef(camera.m_XRot.GetAngle(), 1.0, 0, 0 )
        glRotatef(camera.m_YRot.GetAngle(), 0, 1.0, 0 )
        
        # Enable/Disable features
        glPushAttrib(GL_ENABLE_BIT)
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_BLEND)
        
        # Just in case we set all vertices to white.
        glColor4f(1,1,1,1)
        
        # Render the front quad
        glBindTexture(GL_TEXTURE_2D, self.m_Textures[2])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0) 
        glVertex3f(  0.5, -0.5, -0.5 )
        glTexCoord2f(1, 0) 
        glVertex3f( -0.5, -0.5, -0.5 )
        glTexCoord2f(1, 1) 
        glVertex3f( -0.5,  0.5, -0.5 )
        glTexCoord2f(0, 1) 
        glVertex3f(  0.5,  0.5, -0.5 )
        glEnd()
        
        # Render the left quad
        glBindTexture(GL_TEXTURE_2D, self.m_Textures[5])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0) 
        glVertex3f(  0.5, -0.5,  0.5 )
        glTexCoord2f(1, 0) 
        glVertex3f(  0.5, -0.5, -0.5 )
        glTexCoord2f(1, 1) 
        glVertex3f(  0.5,  0.5, -0.5 )
        glTexCoord2f(0, 1) 
        glVertex3f(  0.5,  0.5,  0.5 )
        glEnd()
        
        # Render the back quad
        glBindTexture(GL_TEXTURE_2D, self.m_Textures[3])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0) 
        glVertex3f( -0.5, -0.5,  0.5 )
        glTexCoord2f(1, 0) 
        glVertex3f(  0.5, -0.5,  0.5 )
        glTexCoord2f(1, 1) 
        glVertex3f(  0.5,  0.5,  0.5 )
        glTexCoord2f(0, 1) 
        glVertex3f( -0.5,  0.5,  0.5 )
        
        glEnd()
        
        # Render the right quad
        glBindTexture(GL_TEXTURE_2D, self.m_Textures[1])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0) 
        glVertex3f( -0.5, -0.5, -0.5 )
        glTexCoord2f(1, 0) 
        glVertex3f( -0.5, -0.5,  0.5 )
        glTexCoord2f(1, 1) 
        glVertex3f( -0.5,  0.5,  0.5 )
        glTexCoord2f(0, 1) 
        glVertex3f( -0.5,  0.5, -0.5 )
        glEnd()
        
        # Render the top quad
        glBindTexture(GL_TEXTURE_2D, self.m_Textures[4])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1) 
        glVertex3f( -0.5,  0.5, -0.5 )
        glTexCoord2f(0, 0) 
        glVertex3f( -0.5,  0.5,  0.5 )
        glTexCoord2f(1, 0) 
        glVertex3f(  0.5,  0.5,  0.5 )
        glTexCoord2f(1, 1) 
        glVertex3f(  0.5,  0.5, -0.5 )
        glEnd()
        
        # Render the bottom quad
        glBindTexture(GL_TEXTURE_2D, self.m_Textures[0])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0) 
        glVertex3f( -0.5, -0.5, -0.5 )
        glTexCoord2f(0, 1) 
        glVertex3f( -0.5, -0.5,  0.5 )
        glTexCoord2f(1, 1) 
        glVertex3f(  0.5, -0.5,  0.5 )
        glTexCoord2f(1, 0) 
        glVertex3f(  0.5, -0.5, -0.5 )
        glEnd()
        
        # Restore enable bits and matrix
        glPopAttrib()
        glPopMatrix()