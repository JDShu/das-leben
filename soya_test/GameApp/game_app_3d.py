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

import sys
from ogl_camera import *
from characters import *
from environment import *
from buildings import *
from terrain_objects import *
from object_3d import *
import os
from os import getcwd, path
from constants import *
from misc_ui import *
from game_assets import *
import soya

os.environ['SDL_VIDEO_CENTERED'] = '1'

NORMAL_MODE = 1
EDIT_MODE = 2

class GameApp3d( soya.World ):
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

        soya.init( a_AppName, a_ViewPortWidth, a_ViewPortHeight, a_Fullscreen )
        soya.World.__init__( self )
        
        self.DATA_PATH = a_DataPath != None and a_DataPath or path.join( getcwd(), "data" )

        camera = soya.Camera( self )
        camera.set_xyz( 16.0, 4.0, 0.0 )
        camera.look_at( soya.Point( self, 16.0, -6.0, 10.0) )

        camera.add_vector( soya.Vector( None, 10.0, 0.0, 0.0 ) )
         
        soya.set_root_widget(camera)


        self.m_SelectedObject = None

        self.m_EditTerrain = False

        self.SetupLighting()

        self.SetupFog()

        self.SetupKeyBuffer()

        self.LoadObjects()
      
        
    def SetupLighting( self ):
        '''
        Setup OpenGL and some variable relating to lighting
        '''
        LightAmbient  = ( 0.2, 0.2, 0.2, 1.0 )
        LightDiffuse  = ( 0.8, 0.8, 0.8, 1.0 )
        self.LightPosition = [ 10.0, 50.0, 30, 1.0 ]
        LightSpecular = ( 1.0, 1.0, 1.0, 1.0 )

        self.light = soya.Light( self )
        self.light.set_xyz( 10.0, 50.0, 30 )
        self.light.ambient = LightAmbient
        self.light.diffuse = LightDiffuse
        self.light.specular = LightSpecular


    def SetupFog( self ):
        '''
        Setup OpenGL fog
        '''       
        self.atmosphere = soya.Atmosphere()
        self.atmosphere.fog = 1
        self.atmosphere.fog_start = 30.0
        self.atmosphere.fog_end = 40.0
        self.atmosphere.fog_color = ( 0.7, 0.7, 1.0, 1.0 )
        self.atmosphere.bg_color= ( 0.7, 0.7, 1.0, 1.0 )
        self.atmosphere.ambient = ( 1.0, 1.0, 1.0, 1.0 )
    

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
        
        # floor terrain
        terrain_size = 129
        self.terrain = soya.Terrain( self, terrain_size, terrain_size )
        grass = soya.Material.get( "grass" )

        self.terrain.set_material_layer( grass, 0.0, 1.0 )
        self.terrain.patch_size = 10.0
        
        self.AssetManager = AssetManager("%s/manifests/default.man" % self.DATA_PATH )

    def begin_round( self ):
        self.ProcessEvents()
        self.ProccessKeys()

    def ProcessEvents(self):
        '''
        Process all game events
        '''           
        
        for event in soya.MAIN_LOOP.events:
            if event[ 0 ] == soya.sdlconst.KEYDOWN:
                self.m_KeyBuffer[ event[ 1 ] ] = True

            elif event[0] == soya.sdlconst.KEYUP:
                self.m_KeyBuffer[ event[ 1 ] ] = False

            elif event[ 0 ] == soya.sdlconst.QUIT:
                soya.MAIN_LOOP.stop()

            '''elif event.type == MOUSEBUTTONDOWN:
                l_Position = self.m_Camera.GetOpenGL3dMouseCoords( l_X, l_Y )
                if event.button == LEFT_MOUSE:
                    pass
                    
            elif event.type == MOUSEBUTTONUP:
                if event.button == LEFT_MOUSE:
                    pass'''

            


    def ProccessKeys( self ):
        '''
        Process the assigned keys and trigger behaviours
        '''
       
        if self.m_KeyBuffer[ soya.sdlconst.K_ESCAPE ]:
            soya.MAIN_LOOP.stop()
        '''elif self.m_KeyBuffer[ soya.sdlconst.K_UP ]:
            self.m_Camera.m_XRot += 1.0

        elif self.m_KeyBuffer[ soya.sdlconst.K_DOWN ]:
            self.m_Camera.m_XRot -= 1.0

        elif self.m_KeyBuffer[ soya.sdlconst.K_LEFT ]:
            self.m_Camera.m_YRot -= 1.0

        elif self.m_KeyBuffer[ soya.sdlconst.K_RIGHT ]:
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
        '''

    def PrintToConsole(self, a_Message, a_LineNumber ):
        '''
        Print a message to the console on a specific line
        @param a_Message String : a message to display
        @param a_LineNumber Integer: the line to pront your message
        '''
        #self.font.glPrint( 10 , self.m_Camera.m_ViewportHeight - ( 17 * a_LineNumber ), a_Message )


    def AddMessage( self, a_Message ):
        '''
        Add a message to the console message queue
        @param a_Message String : a message to display
        '''
        print "%s\n" % a_Message


