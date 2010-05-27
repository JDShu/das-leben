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
from characters import *
from md2 import *
from environment import *
from buildings import *
from OGLExt import *
from terrain_objects import *
from object_3d import *
from vector_3d import *
import ogl_shader 
import glFreeType
import os
from copy import deepcopy
from os import getcwd, path
from constants import *
from misc_ui import *
from game_assets import *
from ogl_vbo import NewVBO

os.environ['SDL_VIDEO_CENTERED'] = '1'

NORMAL_MODE = 1
EDIT_MODE = 2

class GameApp3d:
    """
    The main game class which manages all other processes
    @breif A 3d GameApp
    """
    def __init__(self, a_ViewPortWidth=1024, a_ViewPortHeight=768, a_Fullscreen=False, a_AppName="GameApp3d", a_DataPath=None):
        '''
        Construct the Game app object and load game assets for startup
        @param a_ViewPortWidth Int: the width of the viewport
        @param a_ViewPortHeight Int: the height of the viewport
        @param a_Fullscreen Boolean: Display full screen True or False
        @param a_AppName String: The title to show on the window in windowed mode
        @param a_DataPath String: The path to the data directory
        @return returns a GameApp3d instance
        '''
        
        pygame.init()
        self.m_Clock = pygame.time.Clock()
        glutInit()

        self.DATA_PATH = a_DataPath != None and a_DataPath or path.join( getcwd(), "data" )

        self.m_Camera = oglCamera( a_ViewPortWidth, a_ViewPortHeight)
        self.m_Camera.SetPosition( 0, 0, -7.5 )
        
        if 0:
            video_options = OPENGL|DOUBLEBUF|FULLSCREEN
            modes = self.m_Camera.GetModesList()
            for mode in modes:
                print "%sx%s" % (mode[0], mode[1]) 
        else:
            video_options = OPENGL|DOUBLEBUF

        screen = pygame.display.set_mode((a_ViewPortWidth, a_ViewPortHeight), video_options)
        pygame.display.set_caption(a_AppName)
        self.Resize((a_ViewPortWidth, a_ViewPortHeight))


        if (not glInitVertexBufferObjectARB ()):
            print "Help!  No GL_ARB_vertex_buffer_object"
            sys.exit(1)
            return False
        
        #glEnable(GL_CULL_FACE)
        #glCullFace( GL_BACK )
        glShadeModel(GL_SMOOTH)
        glClearColor( 0.7, 0.7, 1.0, 1.0 )
        glEnable(GL_COLOR_MATERIAL)
        glMaterial( GL_FRONT, GL_SHININESS, 128.0 )
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

        self.m_UseShader = True
        self.m_Shader = ogl_shader.oglBumpyShader()

        self.m_SelectedObject = None

        self.m_EditTerrain = False

        self.SetupLighting()

        self.SetupFog()

        self.SetupKeyBuffer()

        self.LoadObjects()
                   
        self.SetupTiming()

        self.waveTime = 0.0
        self.waveWidth = 0.5
        self.waveHeight = 5.0
        self.waveFreq = 0.1
        
                               
    def SetupTiming( self ):
        '''
        Setup the game timer and initialise all timing variables
        '''
        self.m_Ticks = 0
        self.m_oldTicks = 0
        self.m_currentTicks = 0
        self.m_FrameTicks = 0
        # FPS Limiting
        self.m_FPSTicks = 0
        self.m_FPSLimit = int( 1000 / 30 ) # 30 FPS
        # set up process execution tracking counter
        self.m_ProcessCounter = 1
        self.m_ProcessCounterThreshhold = 3
        
    def SetupLighting( self ):
        '''
        Setup OpenGL and some variable relating to lighting
        '''
        LightAmbient  = [ 0.2, 0.2, 0.2, 1.0 ]
        LightDiffuse  = [ 0.8, 0.8, 0.8, 1.0 ]
        self.LightPosition = [ 10.0, 50.0, 30, 1.0 ]
        LightSpecular = [ 1.0, 1.0, 1.0, 1.0 ]

        glEnable( GL_LIGHTING )
        glEnable( GL_LIGHT0 )

        glLightModelfv( GL_LIGHT_MODEL_AMBIENT, LightAmbient )
        glLightfv( GL_LIGHT0, GL_AMBIENT, LightAmbient )
        glLightfv( GL_LIGHT0, GL_DIFFUSE, LightDiffuse )
        glLightfv( GL_LIGHT0, GL_SPECULAR, LightSpecular )
        glLightfv( GL_LIGHT0, GL_POSITION, self.LightPosition )


    def SetupFog( self ):
        '''
        Setup OpenGL fog
        '''
        density = 1.2
        fogColor = [0.7, 0.7, 1.0, 1.0] 
        glEnable(GL_FOG)
        glFogfv(GL_FOG_COLOR, fogColor)
        glFogf(GL_FOG_DENSITY, density)
        glHint(GL_FOG_HINT, GL_NICEST)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogf(GL_FOG_START, 15.0)
        glFogf(GL_FOG_END, 20.0)
    

    def SetupKeyBuffer( self ):
        '''
        Setup the keyboard buffer
        '''
        self.m_KeyBuffer = []
        for i in range(320):
            self.m_KeyBuffer.append( False )

    def LoadObjects( self ):
        '''load all 3d objects and models'''
        self.objects = []; oadd = self.objects.append

        cube = NewVBO()
        cube.SetPosition( 0, 0, 5 )

        #oadd( cube )

    def TimerUpdate(self):
        '''
        Update all timer variables
        '''
        self.m_oldTicks = self.m_currentTicks
        self.m_currentTicks = pygame.time.get_ticks()
        self.m_Ticks = self.m_currentTicks - self.m_oldTicks
        self.m_FPSTicks += self.m_Ticks

    def ProcessEvents(self):
        '''
        Process all game events
        '''
        self.TimerUpdate()
        
        self.m_ProcessCounter += 1
        if self.m_ProcessCounter > self.m_ProcessCounterThreshhold: self.m_ProcessCounter = 1
        
        events = pygame.event.get()
        
        l_X, l_Y = pygame.mouse.get_pos()
                
        
        for event in events:
            if event.type == KEYDOWN:
                self.m_KeyBuffer[ event.key ] = True

            elif event.type == KEYUP:
                self.m_KeyBuffer[ event.key ] = False

            elif event.type == MOUSEBUTTONDOWN:
                l_Position = self.m_Camera.GetOpenGL3dMouseCoords( l_X, l_Y )
                if event.button == LEFT_MOUSE:
                    pass
                    
            elif event.type == MOUSEBUTTONUP:
                if event.button == LEFT_MOUSE:
                    pass

            elif event.type == QUIT:
                return False

                    
        return self.ProccessKeys()


    def Resize(self, (width, height)):
        '''
        Handle resizing of the OpenGL viewport
        @param (width, height) list : width & height of the new viewport
        '''
        if height==0:
            height=1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 0.95*width/height, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def ProccessKeys( self ):
        '''
        Process the assigned keys and trigger behaviours
        '''
        if self.m_FPSTicks < self.m_FPSLimit: return True
        
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
            x, y, z, w = self.m_Ground.GetPosition()
            y += 0.25
            self.m_Ground.SetPosition( x, y, z, w )
            glLightfv( GL_LIGHT0, GL_POSITION, [ x, y, z ] )
            self.AddMessage( "Position: %s,%s,%s" % ( x, y, z ) )

        elif self.m_KeyBuffer[ K_j ]:
            x, y, z, w = self.m_Ground.GetPosition()
            y -= 0.25
            self.m_Ground.SetPosition( x, y, z, w )
            glLightfv( GL_LIGHT0, GL_POSITION, [ x, y, z ] )
            self.AddMessage( "Position: %s,%s,%s" % ( x, y, z ) )

        elif self.m_KeyBuffer[ K_w ]:
            self.m_Camera.MoveForward()

        elif self.m_KeyBuffer[ K_s ]:
            self.m_Camera.MoveBackward()

        elif self.m_KeyBuffer[ K_a ]:
            self.m_Camera.MoveLeft()
            
        elif self.m_KeyBuffer[ K_d ]:
            self.m_Camera.MoveRight()

        elif self.m_KeyBuffer[ K_z ]:
            self.m_Camera.ZoomIn()

        elif self.m_KeyBuffer[ K_x ]:
            self.m_Camera.ZoomOut()

        elif self.m_KeyBuffer[ K_c ]:
            x, y, z, w = self.m_Camera.GetPosition()
            self.AddMessage( "Camera Position: %s,%s,%s" % ( x, y, z ) )
            self.AddMessage( "angles: %s,%s,%s" % ( self.m_Camera.m_XRot.GetAngle() , 
                                                    self.m_Camera.m_YRot.GetAngle(), 
                                                    self.m_Camera.m_ZRot.GetAngle() ) )

        elif self.m_KeyBuffer[ K_r ]:
            x, y, z, w = self.m_Camera.GetPosition()
            y -= 0.25
            self.m_Camera.SetPosition( x, y, z, w )

        elif self.m_KeyBuffer[ K_f ]:
            x, y, z, w = self.m_Camera.GetPosition()
            y += 0.25
            self.m_Camera.SetPosition( x, y, z, w )
            
        elif self.m_KeyBuffer[ K_e ]:
            self.m_Mode = EDIT_MODE
            
        elif self.m_KeyBuffer[ K_q ]:
            self.m_Mode = NORMAL_MODE
            
        elif self.m_KeyBuffer[ K_t ]:
            self.rgn.ToggleWalls()
            
        return True

    def PrintToConsole(self, a_Message, a_LineNumber ):
        '''
        Print a message to the console on a specific line
        @param a_Message String : a message to display
        @param a_LineNumber Integer: the line to pront your message
        '''
        self.font.glPrint( 10 , self.m_Camera.m_ViewportHeight - ( 17 * a_LineNumber ), a_Message )

    def Draw(self):
        '''
        Render the current scene
        '''
        if self.m_FPSTicks < self.m_FPSLimit: 
            self.m_FrameTicks += self.m_Ticks
            return
        else: self.m_FPSTicks = 0
        self.m_Clock.tick()
        
        self.m_Camera.BeginDrawing()
        
        
        if self.m_UseShader: 
            
            self.m_Shader.StartShader()
        
            color0 = glGetUniformLocation(self.m_Shader._program, "color0")
            color1 = glGetUniformLocation(self.m_Shader._program, "color1")
            color2 = glGetUniformLocation(self.m_Shader._program, "color2")
            eyePos = glGetUniformLocation(self.m_Shader._program, "eyePos")

            glUniform4f( color0, 0.0, 0.0, 1.0, 1.0 )
            glUniform4f( color1, 1.0, 0.0, 0.0, 1.0 )
            glUniform4f( color2, 0.0, 0.0, 0.4, 1.0 )
            glUniform3f( eyePos, self.m_Camera.GetX(), self.m_Camera.GetY(), self.m_Camera.GetZ() )
            

        for Object in self.objects:
            Object.Draw()

        glutSolidTeapot( 1.0 )
        
        self.waveTime += self.waveFreq

        self.m_Camera.EndDrawing()
       
        self.m_Camera.Flip()

    def AddMessage( self, a_Message ):
        '''
        Add a message to the console message queue
        @param a_Message String : a message to display
        '''
        print "%s\n" % a_Message


    def Exit(self):
        '''
        Perform system shutdown
        '''
##        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()


