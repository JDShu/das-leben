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
try:
    from OpenGL.GL.ARB.vertex_buffer_object import *
except: 
    print "bum no VBO"
import sys
import pygame
from pygame.locals import *
from ogl_camera import *
from object_3d import *
from md2 import *
from environment import *
from buildings import *
from OGLExt import *
import os
from os import getcwd

DATA_PATH = getcwd()
 
os.environ['SDL_VIDEO_CENTERED'] = '1'

class GameApp3d:
    """A 3d GameApp"""
    def __init__(self, a_ViewPortWidth=1024, a_ViewPortHeight=768, a_Fullscreen=False, a_AppName="GameApp3d"):
        
        pygame.init()
        
	self.m_Camera = oglCamera()
        self.m_Camera.SetPosition(0, -40, -40.0)
        self.m_Camera.m_XRot += 45
	
        if a_Fullscreen:
            video_options = OPENGL|DOUBLEBUF|FULLSCREEN
            modes = self.m_Camera.GetModesList()
            for mode in modes:
                self.PrintToConsole( "%sx%s" % (mode[0], mode[1]) )
        else:
            video_options = OPENGL|DOUBLEBUF
        
        screen = pygame.display.set_mode((a_ViewPortWidth, a_ViewPortHeight), video_options)
        pygame.display.set_caption(a_AppName)
        self.Resize((a_ViewPortWidth, a_ViewPortHeight))
	
	 
	if (not glInitVertexBufferObjectARB ()):
	    print "Help!  No GL_ARB_vertex_buffer_object"
	    sys.exit(1)
	    return False
		    
	glShadeModel(GL_SMOOTH)
	
	
        
        #glEnable(GL_TEXTURE_2D)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        
        LightAmbient  = [ 0.2, 0.2, 0.2, 1.0]
        LightDiffuse  = [ 1.0, 1.0, 1.0, 1.0]
        LightPosition = [ 0.0, 100.0, 0.0, 1.0]
        
        glLightfv( GL_LIGHT1, GL_AMBIENT, LightAmbient )
        glLightfv( GL_LIGHT1, GL_DIFFUSE, LightDiffuse )
        glLightfv( GL_LIGHT1, GL_POSITION, LightPosition )
        glEnable( GL_LIGHT1 )
        
        glEnable( GL_LIGHTING )
        
        density = 0.0001
        fogColor = [0.5, 0.5, 0.5, 1.0] 
        glEnable(GL_FOG)
        glFogi(GL_FOG_MODE, GL_EXP2)
        glFogfv(GL_FOG_COLOR, fogColor)
        glFogf(GL_FOG_DENSITY, density)
        glHint(GL_FOG_HINT, GL_NICEST)
                
        self.m_KeyBuffer = []
        for i in range(320):
            self.m_KeyBuffer.append( False )
        
        self.m_SkyBox = SkyBox("%s/data/skybox" % DATA_PATH )
        self.m_Objects = []; oadd = self.m_Objects.append
        Model = Object3d( "%s/data/avatar/tris.md2" % DATA_PATH, 
	                  "%s/data/avatar/grid.tga" % DATA_PATH, 
	                  object_type=OBJECT_3D_ANIMATED_MESH )
        Model.m_XRot.SetAngle( -90 )
	Model.SetAnimation( IDLE1 )
        oadd( Model )
        Ground = Object3d( "%s/data/ground/tris.md2" % DATA_PATH, "%s/data/ground/grass.png" % DATA_PATH, 120 )
        Ground.m_ZRot.SetAngle( -90 )
        oadd( Ground )
        house = House( floors = 2 )
        oadd( house )
        
        
        self._currentTicks = self._oldTicks = pygame.time.get_ticks()
        self._ticks = 0
    
        
    def TimerUpdate(self):
        self._oldTicks = self._currentTicks
        self._currentTicks = pygame.time.get_ticks()
        self._ticks = self._currentTicks - self._oldTicks
        
    def ProcessEvents(self):
        self.TimerUpdate()
        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                self.m_KeyBuffer[ event.key ] = True
                
            elif event.type == KEYUP:
                self.m_KeyBuffer[ event.key ] = False
                
	    elif event.type == MOUSEBUTTONDOWN:
		l_X, l_Y = pygame.mouse.get_pos()
		print self.GetSelectedObject( l_X, l_Y )
		l_Position = self.m_Camera.GetOpenGL3dMouseCoords( l_X, l_Y )
		l_Position.Print()
		
            elif event.type == QUIT:
                return False
                
        return self.ProccessKeys()

    def GetSelectedObject( self, a_X, a_Y ):
	return "The Selected Object ID is %s" % self.m_Camera.GetObjectSelected( a_X, a_Y, self.m_Objects )

    def Resize(self, (width, height)):
        if height==0:
            height=1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 0.95*width/height, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def ProccessKeys( self ):
        if self.m_KeyBuffer[ K_ESCAPE ]:
            return False
        elif self.m_KeyBuffer[ K_UP ]:
            self.m_Camera.m_XRot += 1.0
            
        elif self.m_KeyBuffer[ K_DOWN ]:
            self.m_Camera.m_XRot -= 1.0
            
        elif self.m_KeyBuffer[ K_LEFT ]:
            self.m_Camera.m_YRot -= 1.0
            
        elif self.m_KeyBuffer[ K_RIGHT ]:
            self.m_Camera.m_YRot += 1.0
            
        elif self.m_KeyBuffer[ K_u ]:
            x, y, z, w = self.m_Model.GetPosition()
            z += 1
            self.m_Model.SetPosition( x, y, z, w )
            
        elif self.m_KeyBuffer[ K_j ]:
            x, y, z, w = self.m_Model.GetPosition()
            z -= 1
            self.m_Model.SetPosition( x, y, z, w )
            
        elif self.m_KeyBuffer[ K_w ]:
            x, y, z, w = self.m_Camera.GetPosition()
            z -= 1
            self.m_Camera.SetPosition( x, y, z, w )
            
        elif self.m_KeyBuffer[ K_s ]:
            x, y, z, w = self.m_Camera.GetPosition()
            z += 1
            self.m_Camera.SetPosition( x, y, z, w )
	    
	elif self.m_KeyBuffer[ K_a ]:
            x, y, z, w = self.m_Camera.GetPosition()
            x -= 1
            self.m_Camera.SetPosition( x, y, z, w )
            
        elif self.m_KeyBuffer[ K_d ]:
            x, y, z, w = self.m_Camera.GetPosition()
            x += 1
            self.m_Camera.SetPosition( x, y, z, w )

	elif self.m_KeyBuffer[ K_r ]:
            x, y, z, w = self.m_Camera.GetPosition()
            y -= 1
            self.m_Camera.SetPosition( x, y, z, w )
            
        elif self.m_KeyBuffer[ K_f ]:
            x, y, z, w = self.m_Camera.GetPosition()
            y += 1
            self.m_Camera.SetPosition( x, y, z, w )
	    
        return True
                    
    def PrintToConsole(self, a_Message):
	print a_Message

    def Draw(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # self.m_Camera.LookAt( self.m_Sphere )
        self.m_SkyBox.Draw( self.m_Camera )
        self.m_Camera.BeginDrawing()
        
        for Object in self.m_Objects:
	   #if Object.__module__ == "GameApp.object_3d":
		#Object.Animate(self._ticks)
            Object.Draw()
            
        self.m_Camera.EndDrawing()
        

    def Exit(self):
        pygame.quit()
        sys.exit()

    
if __name__ == "__main__": 
    game_app = GameApp3d()
    game_app.Exit()

