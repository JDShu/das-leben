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
        # start pygame
        pygame.init()
        self.m_Clock = pygame.time.Clock()

        # start glut
        # @warning may be removed later as glut isnt really needed now
        glutInit()

        self.DATA_PATH = a_DataPath != None and a_DataPath or path.join( getcwd(), "data" )

        # create the camera
        self.m_Camera = oglCamera( a_ViewPortWidth, a_ViewPortHeight)
        self.m_Camera.SetPosition(0, -4, 3.0)
        self.m_Camera.m_XRot += 31
        self.m_Camera.m_YRot += 157
        
        # set the display mode
        if a_Fullscreen:
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
        
        # set some OpenGL options
        glEnable(GL_CULL_FACE)
        glCullFace( GL_BACK )
        glShadeModel(GL_SMOOTH)
        glClearColor( 0.5, 0.5, 1.0, 1.0 )
        glEnable(GL_COLOR_MATERIAL)
        glMaterial( GL_FRONT, GL_SHININESS, 5.0 )
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

        self.m_UseShader = False
        self.m_Shader = ogl_shader.oglBumpyShader()

        self.m_SelectedObject = None

        self.m_EditTerrain = False

        self.SetupLighting()

        self.SetupFog()

        # init the keyboard input processing
        self.SetupKeyBuffer()

        # init the messaging system console
        self.LoadConsole()

        # start loading basic assets
        self.StartMusicTrack( "01_every_thought_has_been_thought.ogg" )
        self.m_SplashBg = TexturedRect( "%s/gui/graphics/background_light_clouds.png" % self.DATA_PATH, Vector3d( 0, 0, 1.0 ), 
                                       self.m_Camera.m_ViewportWidth, self.m_Camera.m_ViewportHeight )

        self.m_SplashLogo = TexturedRect( "%s/gui/graphics/logo_la_vida.png" % self.DATA_PATH, Vector3d( 200, 311, 1.0 ), 676, 200 )
        pos_x = self.m_Camera.m_ViewportWidth - 130
        pos_y = -15 - ( self.m_Camera.m_ViewportHeight / 2 )
        self.m_WingIDELogo = TexturedRect( "%s/gui/graphics/logo_wing_ide.png" % 
                                           self.DATA_PATH, 
                                           Vector3d( pos_x, pos_y, 1.0 ),
                                           217, 80 )
        
        self.UpdateSplash( "Loading ..." )

        self.LoadObjects()
        
        self.UpdateSplash( "Loading ..." )
        
        self.SetupUI()
        
        # setup the game timers
        self.SetupTiming()
        
        # setup the process pipelining
        # @warning Not yet implemented
        self.SetupExecutionCycles()
        
    def SetupExecutionCycles( self ):
        self.m_ProcessCycles = { "Behaviours": 2, "Events": 3 }
                
    def SetupUI( self ):
        self.m_SelectedArea = SelectedRegion( 0.5, 0.0, Vector3d(), Vector3d(), pygame.time.get_ticks() )
        self.m_SelectedStart = 0
        self.m_SelectStartTicks = 0
        self.m_GroundLevel.insert( 1, self.m_SelectedArea )
        self.m_Mode = EDIT_MODE
        
    def SetupTiming( self ):
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
        
    def StartMusicTrack( self, a_Filename ):
        try:
            if os.path.exists( "%s/music/%s" % ( self.DATA_PATH, a_Filename ) ):
                pygame.mixer.music.load( "%s/music/%s" % ( self.DATA_PATH, a_Filename ) )
                pygame.mixer.music.play( -1 )
                pygame.mixer.music.set_volume( 0.05 )
        except IOError, e:
            raise Exception, "Unable to load %s: %s" ( a_Filename, e )

    def SetupLighting( self ):
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
        density = 0.05
        fogColor = [0.5, 0.5, 1.0, 1.0] 
        glEnable(GL_FOG)
        glFogi(GL_FOG_MODE, GL_EXP2)
        glFogfv(GL_FOG_COLOR, fogColor)
        glFogf(GL_FOG_DENSITY, density)
        glHint(GL_FOG_HINT, GL_NICEST)
        glDisable( GL_FOG )
    

    def SetupKeyBuffer( self ):
        self.m_KeyBuffer = []
        for i in range(320):
            self.m_KeyBuffer.append( False )

    def LoadConsole( self ):
        self.font = glFreeType.font_data( "%s/gui/fonts/body.ttf" % self.DATA_PATH, 16 )
        self.Titlefont = glFreeType.font_data( "%s/gui/fonts/head.ttf" % self.DATA_PATH, 72 )
        self.m_Messages = []

    def LoadObjects( self ):
        '''load all 3d objects and models'''
        
        #self.UpdateSplash( "Loading Skybox..." )
        #self.m_SkyBox = SkyBox("%s/environment/nature/skies/open fields" % self.DATA_PATH )
        self.m_GroundLevel = []; gadd = self.m_GroundLevel.append
        self.m_Grids = []; gradd = self.m_Grids.append
        self.m_Objects = []; obadd = self.m_Objects.append
        
        self.UpdateSplash( "Loading Terrain..." )
        Ground = TerrainRegion( 0.0, 0.0, 0.0, 50, 50, 0.5 )

        gadd( Ground )
        
        Ground = TerrainGridedRegion( 0.0, 0.0, 0.0, 50, 50, 0.5 )

        self.m_GroundGrid = Ground
        gradd( Ground )
        gadd( Ground )
        
        self.m_GroundFloorObjects = []; oadd = self.m_GroundFloorObjects.append
        
        self.UpdateSplash( "Loading lighting sphere..." )
        self.m_Light = Object3d(None, None, 20, OBJECT_3D_SPHERE )
        self.m_Light.SetPosition( 10.0, 50.0, 30 )
        oadd( self.m_Light )
        obadd( self.m_Light )

        ##        self.UpdateSplash( "Loading character model..." )
##        Model = Avatar( self.DATA_PATH, DUDETTE )
##        Model.SetPosition( 4.0,
##                           Model.GetAltitude( 0.0 ),
##                           4.5 )
##        
##        self.m_Model = Model
##        oadd( Model )

        self.UpdateSplash( "Loading Furniture..." )
        chair = Object3d( "%s/environment/manmade/furniture/chair_70th.obj" % self.DATA_PATH, 
                          None, 
                          object_type=OBJECT_3D_MESH)
        
        chair.SetScale( 0.1 )
        chair.SetPosition( 4.0, 
                           chair._model.va.GetDimensions()[ 1 ] 
                           * chair._model.GetScale() * 0.5, 
                           2.0 )
        oadd( chair )
        obadd( chair )
        
        oven = Object3d( "%s/environment/manmade/furniture/oven.obj" % self.DATA_PATH, 
                          None, 
                          object_type=OBJECT_3D_MESH)
        
        oven.SetScale( 0.15 )
        oven.SetPosition( 3.0, 
                           oven._model.va.GetDimensions()[ 1 ] 
                           * oven._model.GetScale() * 0.5, 
                           3.0 )
        oadd( oven )
        obadd( oven )
        
        self.UpdateSplash( "Loading Wall..." )
        wall = Object3d( "%s/environment/manmade/walls/wall.obj" % self.DATA_PATH, 
                          None, 
                          object_type=OBJECT_3D_MESH)
        
        wall.SetScale( 0.25 )
        wall.SetPosition( 2.75, wall._model.va.GetDimensions()[ 1 ] * wall._model.GetScale() * 0.5 , 2.0 )
        self.m_FloorHeight = wall._model.va.GetDimensions()[ 1 ] * wall._model.GetScale() * 0.5
        oadd( wall )
        obadd( wall )
        self.m_Wall = wall
        
        new_wall = wall.Clone()
        new_wall.SetScale( 0.25 )
        new_wall.SetPosition( 4, self.m_FloorHeight, 4 )
        ObjectMultiplier( 6, Vector3d( 1, 0, 0), new_wall )
        oadd( new_wall )
        
        self.UpdateSplash( "Loading Wall with window..." )
        wall = Object3d( "%s/environment/manmade/walls/wall_with_small_window.obj" % self.DATA_PATH, 
                          None, 
                          object_type=OBJECT_3D_MESH)
        
        wall.SetScale( 0.25 )
        wall.SetPosition( 2.25, wall._model.va.GetDimensions()[ 1 ] * wall._model.GetScale() * 0.5 , 2.0 )
        oadd( wall )
        obadd( wall )
        
        door = Object3d( "%s/environment/manmade/doors/door.obj" % self.DATA_PATH, 
                          None, 
                          object_type=OBJECT_3D_MESH)
        
        door.SetScale( 0.22 )
        door.SetPosition( 6.0, 
                           door._model.va.GetDimensions()[ 1 ] 
                           * door._model.GetScale() * 0.5, 
                           3.0 )
        oadd( door )
        obadd( door )
        
        self.m_FirstFloorLevel = []; fadd = self.m_FirstFloorLevel.append
        
        Ground = TerrainGridedRegion( 0.0, self.m_FloorHeight, 0.0, 50, 50, 0.5 )

        self.m_FirstFloorGrid = Ground
        gradd( Ground )
        fadd( Ground )
##
##        self.UpdateSplash( "Loading House..." )
##        house = Object3d( "%s/home/House010.obj" % self.DATA_PATH, 
##                          None, 
##                          object_type=OBJECT_3D_MESH,
##                          a_Colour=[1.0, 1.0, 0.0])
##
##        house.SetScale( 200 )
##        house.m_XRot.SetAngle( -90 )
##        house.SetPosition( 0, 0, -4 )
##        oadd( house )
##        self.house = house

        self.m_currentTicks = self.m_oldTicks = pygame.time.get_ticks()
        self.m_Ticks = 0    

    def UpdateSplash( self, a_Message ):
        glClear( GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT )
        glDisable( GL_LIGHTING )
        self.m_Camera.BeginDrawing2d()
        
        self.m_SplashBg.Draw()
        self.m_SplashLogo.Draw()
        self.m_WingIDELogo.Draw()
        
        self.m_Camera.EndDrawing2d()
        
        self.font.glPrint( 10, 10, a_Message, [ 0.0, 0.0, 0.0 ] )
        pygame.display.flip()
        
        glEnable( GL_LIGHTING )

    def TimerUpdate(self):
        self.m_oldTicks = self.m_currentTicks
        self.m_currentTicks = pygame.time.get_ticks()
        self.m_Ticks = self.m_currentTicks - self.m_oldTicks
        self.m_FPSTicks += self.m_Ticks

    def ProcessEvents(self):
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
                
                self.m_SelectedObject =  self.GetSelectedObject( l_X, l_Y )
                l_Position = self.m_Camera.GetOpenGL3dMouseCoords( l_X, l_Y )
                if event.button == LEFT_MOUSE:
                    self.m_SelectedArea.m_Enabled = True
                    #self.AddMessage( "Started at %s" % l_Position )
                    l_Start = Vector3d()
                    l_Start = l_Position
                    x, y, z, w = l_Start.GetPosition()
                    new_x = int( ( x + 0.5 ) / 0.5 ) * 0.5
                    new_z = int( ( z + 0.5 ) / 0.5 ) * 0.5
                    l_Start.SetPosition( new_x, y, new_z )
                    
                    addVec = Vector3d( 0.5, 0, 0.5 )
                    self.m_SelectedArea.BeginEditing()
                    self.m_SelectedArea.SetBegin( l_Start, l_Start + addVec )
               
                    
            elif event.type == MOUSEBUTTONUP:
                if event.button == LEFT_MOUSE:
                    self.m_SelectedArea.EndEditing()
                    self.m_SelectedArea.m_Enabled = False
                    
                    l_Dimensions = self.m_SelectedArea.GetGranularDimensions( self.m_Grids[ 0 ].m_Size )
                    l_Floor = FloorRegion( self.m_SelectedArea.m_Position.GetX(), 
                                      0.0, 
                                      self.m_SelectedArea.m_Position.GetZ(), 
                                      l_Dimensions.width, 
                                      l_Dimensions.height, 
                                      0.5, 
                                      1.0,
                                      self.m_Wall )
                    
                    self.m_GroundFloorObjects.insert( 1, l_Floor )

            elif event.type == QUIT:
                return False

            
        if self.m_SelectedArea.IsEditing():
            self.m_SelectedObject =  self.GetSelectedObject( l_X, l_Y )
            l_Position = self.m_Camera.GetOpenGL3dMouseCoords( l_X, l_Y )
            #self.AddMessage( "Ending at %s" % l_Position )
            l_End = Vector3d()
            l_End = l_Position
            x, y, z, w = l_End.GetPosition()
            new_x = int( ( x + 0.5 ) / 0.5 ) * 0.5
            new_z = int( ( z + 0.5 ) / 0.5 ) * 0.5
            l_End.SetPosition( new_x, y, new_z )
            self.m_SelectedArea.UpdateEnd( l_End )
                    
        return self.ProccessKeys()

    def ProcessBehaviours( self ):
        for game_object in self.m_Objects:
            if game_object.__module__ == "GameApp.characters":
                if game_object.m_ObjectType == OBJECT_3D_ANIMATED_MESH:
                    game_object.Animate(self.m_Ticks)
                game_object.UpdateTicks( self.m_Ticks )
                game_object.DoBehaviours()
                # self.AddMessage( "Avatar : %s,%s,%s" % ( game_object.GetX(), game_object.GetY(), game_object.GetZ() ) )

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
            x, y, z, w = self.m_Camera.GetPosition()
            z -= 1
            self.m_Camera.SetPosition( x, y, z, w )

        elif self.m_KeyBuffer[ K_s ]:
            x, y, z, w = self.m_Camera.GetPosition()
            z += 0.25
            self.m_Camera.SetPosition( x, y, z, w )

        elif self.m_KeyBuffer[ K_a ]:
            x, y, z, w = self.m_Camera.GetPosition()
            x -= 0.25
            self.m_Camera.SetPosition( x, y, z, w )

        elif self.m_KeyBuffer[ K_d ]:
            x, y, z, w = self.m_Camera.GetPosition()
            x += 0.25
            self.m_Camera.SetPosition( x, y, z, w )

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
            
        return True

    def PrintToConsole(self, a_Message, a_LineNumber ):
        self.font.glPrint( 10 , self.m_Camera.m_ViewportHeight - ( 17 * a_LineNumber ), a_Message )

    def Draw(self):
        if self.m_FPSTicks < self.m_FPSLimit: 
            self.m_FrameTicks += self.m_Ticks
            return
        else: self.m_FPSTicks = 0
        self.m_Clock.tick()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # self.m_Camera.LookAt( self.m_Sphere )
        # self.m_SkyBox.Draw( self.m_Camera )
        self.m_Camera.BeginDrawing()
        if self.m_UseShader: self.m_Shader.StartShader()
        
        # Draw ground level stuff
        for Object in self.m_GroundLevel:
            Object.Draw()
            
        for Object in self.m_GroundFloorObjects:
            Object.Draw()
            
        for Object in self.m_FirstFloorLevel:
            Object.Draw()

        self.m_Camera.EndDrawing()

        # out put messages
        for i, message in enumerate( self.m_Messages ):
            self.PrintToConsole( message, i )
        self.font.glPrint( 900, 10, "FPS:%f" % self.m_Clock.get_fps() )
        
        self.m_Camera.Flip()

    def AddMessage( self, a_Message ):
        self.m_Messages.append( a_Message )
        if len( self.m_Messages ) > 40:
            self.m_Messages = []


    def Exit(self):
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()


if __name__ == "__main__": 
    game_app = GameApp3d()
    game_app.Exit()

