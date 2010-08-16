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
from buildings import *
from system import *
from lavida_gui import * 
from Cookers import Oven
import soya, soya.widget
import soya.pudding as pudding
import soya.pudding.ext.fpslabel


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

        self.m_Camera = oglCamera( self )
        self.m_Camera.set_xyz( 37.0, 10.0, 23.0 )
        self.m_Camera.look_at( soya.Point( self, 16.0, -6.0, 10.0) )

        self.m_Camera.add_vector( soya.Vector( None, 10.0, 0.0, 0.0 ) )

        self.m_Camera.back = 100
        
        self.root = soya.gui.RootLayer(None)
        soya.gui.CameraViewport( self.root, self.m_Camera )

        soya.set_root_widget( self.root )
                
        #pudding.ext.fpslabel.FPSLabel( soya.root_widget, position = pudding.TOP_RIGHT )

        self.m_SelectedObject = None

        self.m_EditTerrain = False

        self.SetupLighting()

        self.SetupFog()

        self.SetupKeyBuffer()
        
        self.SetupEventQueue()
        
        self.SetupGUI()

        self.LoadObjects()
        
        
    def SetupGUI( self ):
        self.pie_menu = StandardActionsMenu( self.root, self.m_EventQueue )
        self.pie_menu.visible = 0

    def SetupEventQueue( self ):
        self.m_EventQueue = EventQueue()
        
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
        self.atmosphere.fog_start = 70.0
        self.atmosphere.fog_end = 100.0
        self.atmosphere.fog_color = ( 0.7, 0.7, 1.0, 1.0 )
        self.atmosphere.bg_color= ( 0.7, 0.7, 1.0, 1.0 )
        self.atmosphere.ambient = ( 0.3, 0.3, 0.3, 1.0 )


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
        terrain_size = 50 * 3
        
        self.terrain = soya.Terrain( self, terrain_size, terrain_size )		  
		  
        grass = soya.Material.get( "grass" )
        grass.mip_map = 1
        self.terrain.set_material_layer( grass, 0.0, 1.0 )
        self.terrain.patch_size = 10.0
        self.terrain.texture_factor = 0.50
        
        

        self.AssetManager = AssetManager( self, "environment/manifests/default.man", self.DATA_PATH )

##        f = LoadableRegion( self, a_AssetManager=self.AssetManager )
##        f.Load( "%s/environment/floors/first.flr" % self.DATA_PATH )
        #f.Save( "%s/environment/floors/first.pkl" % self.DATA_PATH )
        pickle_file = open( "%s/environment/floors/first.pkl" % self.DATA_PATH, "r" )
        f = pickle.load( pickle_file )
        pickle_file.close()
        
        self.grid = g = f.CreateGrid()
             
        model_builder = soya.SimpleModelBuilder()
        model_builder.shadow = 1
        
        b = soya.Body( self, f.to_model() )
        b.y = 0.01 
        

        self.sorcerer = Avatar( self, DUDE, self.AssetManager, self.m_EventQueue, [ self.grid ] )
        self.sorcerer.selected = True
        self.sorcerer.x = ( 25 * 3 ) + 1.5
        self.sorcerer.z = ( 37 * 3 ) + 1.5
        
        p = PathFinder( g, g.GridSpaceCoords( self.sorcerer.x, self.sorcerer.z, WALL_WIDTH, 1.5 ) , [( 30, 30 )] )
               
        self.sorcerer.UseWaypoints( p.path )
        
        self.m_Camera.look_at( self.sorcerer )
        
        self.oven = Oven( self, self.root , self.m_EventQueue )
        
        self.oven.SetPosition( ( 25 * 3 ) + 1.5, 0, ( 25 * 3 ) + 1.5 )

    def begin_round( self ):
        soya.Body.begin_round( self )
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

            elif event[0] == soya.sdlconst.MOUSEMOTION:
                self.mouse_pos = self.m_Camera.coord2d_to_3d( event[1], event[2], -15.0 )
                self.move( self.mouse_pos )
              
            elif event[0] == soya.sdlconst.MOUSEBUTTONDOWN:
                self.pie_menu.on_mouse_pressed( event[1], event[2], event[3] )
                if event[1] == soya.sdlconst.BUTTON_LEFT:
                    self.pie_menu.visible = 0
                if event[1] == soya.sdlconst.BUTTON_RIGHT:
                    self.pie_menu.visible = 1
                    self.pie_menu.move( event[2], event[3] )
                    
            
            for event in self.m_EventQueue.events:
                if event.category == ACTION:
                    if not event.prepared:
                        self.PrepareActionEvent( event )
##              mouse = self.m_Camera.coord2d_to_3d(event[2], event[3])
##              result = self.raypick( self.m_Camera, self.m_Camera.vector_to( mouse ) )
##              
##              impact, normal = result
##              g = self.grid
##              g_coord = g.GridSpaceCoords
##              p = PathFinder( g, g_coord( self.sorcerer.x, self.sorcerer.z, WALL_WIDTH ),
##                              [ g_coord( impact.x, impact.z, WALL_WIDTH ) ] )
##              
##              self.sorcerer.UseWaypoints( p.path )




    def PrepareActionEvent( self, event ):
        if event.name == "move_to":
            data = event.GetCurrentAction().data[ 0 ]
            mouse = self.m_Camera.coord2d_to_3d( data[0], data[1] )
            result = self.raypick( self.m_Camera, self.m_Camera.vector_to( mouse ) )
            impact, normal = result
            data[ 0 ] = impact
            event.prepared = True

    def ProccessKeys( self ):
        '''
        Process the assigned keys and trigger behaviours
        '''

        if self.m_KeyBuffer[ soya.sdlconst.K_ESCAPE ]:
            soya.MAIN_LOOP.stop()

        if self.m_KeyBuffer[ soya.sdlconst.K_d ]:
            self.m_Camera.speed.x = 1.0
        elif self.m_KeyBuffer[ soya.sdlconst.K_a ]:
            self.m_Camera.speed.x = -1.0
        else:
            self.m_Camera.speed.x /= 2.0

        if self.m_KeyBuffer[ soya.sdlconst.K_s ]:
            self.m_Camera.speed.z = 1.0
        elif self.m_KeyBuffer[ soya.sdlconst.K_w ]:
            self.m_Camera.speed.z = -1.0
        else:
            self.m_Camera.speed.z /= 2.0

        if self.m_KeyBuffer[ soya.sdlconst.K_f ]:
            self.m_Camera.speed.y = -0.3
        elif self.m_KeyBuffer[ soya.sdlconst.K_r ]:
            self.m_Camera.speed.y = 0.3
        else:
            self.m_Camera.speed.y /= 2.0

        if self.m_KeyBuffer[ soya.sdlconst.K_DOWN ]:
            self.m_Camera.rot_x = -3.0
        elif self.m_KeyBuffer[ soya.sdlconst.K_UP ]:
            self.m_Camera.rot_x = 3.0
        else:
            self.m_Camera.rot_x /= 1.5

        if self.m_KeyBuffer[ soya.sdlconst.K_LEFT ]:
            self.m_Camera.rot_y = 3.0
        elif self.m_KeyBuffer[ soya.sdlconst.K_RIGHT ]:
            self.m_Camera.rot_y = -3.0
        else:
            self.m_Camera.rot_y /= 1.5

        if self.m_KeyBuffer[ soya.sdlconst.K_z ]:
            self.m_Camera.rot_z = 3.0
        elif self.m_KeyBuffer[ soya.sdlconst.K_x ]:
            self.m_Camera.rot_z = -3.0
        else:
            self.m_Camera.rot_z /= 1.5

##        if self.m_KeyBuffer[ soya.sdlconst.K_d ]:
##            self.m_Camera.speed.x = -1.0
##        elif self.m_KeyBuffer[ soya.sdlconst.K_a ]:
##            self.m_Camera.speed.x = 1.0
##        else:
##            self.m_Camera.speed.x = 0.0
##
##        if self.m_KeyBuffer[ soya.sdlconst.K_s ]:
##            self.m_Camera.MoveBackward()
##        elif self.m_KeyBuffer[ soya.sdlconst.K_w ]:
##            self.m_Camera.MoveForward()
##        else:
##            self.m_Camera.speed.z = 0.0
##
##        if self.m_KeyBuffer[ soya.sdlconst.K_f ]:
##            self.m_Camera.speed.y = -1.0
##        elif self.m_KeyBuffer[ soya.sdlconst.K_r ]:
##            self.m_Camera.speed.y = 1.0
##        else:
##            self.m_Camera.speed.y = 0.0
##
##        if self.m_KeyBuffer[ soya.sdlconst.K_DOWN ]:
##            self.m_Camera.rot_x = -10.0
##        elif self.m_KeyBuffer[ soya.sdlconst.K_UP ]:
##            self.m_Camera.rot_x = 10.0
##        else:
##            self.m_Camera.rot_x = 0.0
##
##        if self.m_KeyBuffer[ soya.sdlconst.K_LEFT ]:
##            self.m_Camera.rot_y = -10.0
##        elif self.m_KeyBuffer[ soya.sdlconst.K_RIGHT ]:
##            self.m_Camera.rot_y = 10.0
##        else:
##            self.m_Camera.rot_y = 0.0

        '''elif self.m_KeyBuffer[ soya.sdlconst.K_DOWN ]:
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


