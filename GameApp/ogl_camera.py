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
import pygame
from pygame.locals import *
from vector_3d import *
from angle import *

class oglCamera( Vector3d ):
    def __init__( self, a_ViewportWidth=800, a_ViewportHeight=600 ):
        Vector3d.__init__( self )
        self.m_XRot = Angle()
        self.m_YRot = Angle()
        self.m_ZRot = Angle()
        self.m_ViewportWidth = a_ViewportWidth
        self.m_ViewportHeight = a_ViewportHeight

    def BeginDrawing( self ):
        glLoadIdentity()
        glPushMatrix()
        glRotatef( self.m_XRot.GetAngle(), 1.0,   0,   0 )
        glRotatef( self.m_YRot.GetAngle(),   0, 1.0,   0 )
        glTranslatef( self.m_Values[0], self.m_Values[1], self.m_Values[2] )


    def EndDrawing( self ):        
        glPopMatrix()

    def Flip( self ):
        pygame.display.flip()

    def LookAt(self, a_Point):
        x, y, z, w = a_Point.GetPosition()
        gluLookAt(self.m_Values[0], self.m_Values[1], self.m_Values[2],
                  x, y, z,
                  0, 1, 0)

    def GetModesList( self ):
        return pygame.display.list_modes()

    def GetObjectSelected( self, a_X, a_Y, a_Objects ):
        l_Buffer = glSelectBuffer( 512 )        
        l_Viewport = glGetIntegerv( GL_VIEWPORT )

        glRenderMode( GL_SELECT )
        glInitNames()
        glPushName( 0 )
        glMatrixMode( GL_PROJECTION )
        glPushMatrix()
        glLoadIdentity()
        gluPickMatrix( a_X, l_Viewport[ 3 ] - a_Y, 1.0, 1.0, l_Viewport )
        gluPerspective( 45, self.m_ViewportWidth / self.m_ViewportHeight, 0.0001, 100000.0 )

        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        glRotatef( self.m_XRot.GetAngle(), 1.0,   0,   0 )
        glRotatef( self.m_YRot.GetAngle(),   0, 1.0,   0 )
        glTranslatef( self.m_Values[0], self.m_Values[1], self.m_Values[2] )        

        for Object in a_Objects:
            if hasattr( Object, "DrawSelectMode" ):
                Object.DrawSelectMode()
            else:
                if hasattr( Object, "GetGLName" ):
                    glPushName( Object.GetGLName() )
                Object.Draw()
                glPopName()

        l_Hits = glRenderMode( GL_RENDER )
        glMatrixMode( GL_PROJECTION )
        glPopMatrix()
        glMatrixMode( GL_MODELVIEW )
        return l_Hits

    def GetOpenGL3dMouseCoords( self, a_X, a_Y ):
        '''get the 3d space coords of where the mouse has clicked on the viewport'''
        l_ModelMatrix = glGetDoublev( GL_MODELVIEW_MATRIX )
        l_ProjectionMatrix = glGetDoublev( GL_PROJECTION_MATRIX );
        l_Viewport = glGetIntegerv( GL_VIEWPORT )

        l_WindowX = float( a_X )
        l_WindowY = float( l_Viewport[ 3 ] ) - float( a_Y )
        l_WindowZ = glReadPixels( a_X, int( l_WindowY ), 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT )
        l_Position = gluUnProject( l_WindowX, l_WindowY, l_WindowZ, l_ModelMatrix, l_ProjectionMatrix, l_Viewport )

        l_RetVal = Vector3d()
        l_RetVal.SetPosition( l_Position[ 0 ], l_Position[ 1 ], l_Position[ 2 ] )
        return l_RetVal
    
    def BeginDrawing2d( self ):
        glPushMatrix()
        glDisable(GL_DEPTH_TEST)
        glMatrixMode( GL_PROJECTION )
        glPushMatrix()        
        viewport = glGetIntegerv( GL_VIEWPORT )
        glOrtho( viewport[0],viewport[2],viewport[1],viewport[3], -1, 1 )
        glMatrixMode( GL_MODELVIEW )
        glPushMatrix()
        glLoadIdentity()
        
    def EndDrawing2d( self ):
        glMatrixMode( GL_PROJECTION )
        glPopMatrix()
    
        glMatrixMode( GL_MODELVIEW )
        glPopMatrix()
    
        glEnable( GL_DEPTH_TEST )
        glPopMatrix()