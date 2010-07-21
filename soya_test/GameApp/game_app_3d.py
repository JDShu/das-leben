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
import soya, soya.widget

os.environ['SDL_VIDEO_CENTERED'] = '1'

NORMAL_MODE = 1
EDIT_MODE = 2

def random_terrain_border(terrain):
  out_of_map_vertex_options = (1, 1)
  TERRAIN_SIZE = 129
  fall_length  = 2
  afall_length = 0
  for i in range(TERRAIN_SIZE):
    for j in range(fall_length):
      terrain.set_vertex_option(i, j, *out_of_map_vertex_options)
      #terrain.set_vertex_color(i, j, (0.0, 0.0, 0.0, 0.0))
      terrain.set_height(i, j, 0.0)
    terrain.set_height(i, j + 1, 0.92 * terrain.get_height(i, j + 1))
    if i % 2:
      fall_length = max(1, fall_length + afall_length)
      if (fall_length == 1) and (afall_length == -1): afall_length = 0
      else: afall_length = max(-1, min(1, afall_length + random.randint(-1, 1)))
      
  fall_length  = 2
  afall_length = 0
  for i in range(TERRAIN_SIZE):
    for j in range(TERRAIN_SIZE - 1, TERRAIN_SIZE - fall_length - 1, -1):
      terrain.set_vertex_option(i, j, *out_of_map_vertex_options)
      #terrain.set_vertex_color(i, j, (0.0, 0.0, 0.0, 0.0))
      terrain.set_height(i, j, 0.0)
    terrain.set_height(i, j - 1, 0.92 * terrain.get_height(i, j - 1))
    if i % 2:
      fall_length = max(1, fall_length + afall_length)
      if (fall_length == 1) and (afall_length == -1): afall_length = 0
      else: afall_length = max(-1, min(1, afall_length + random.randint(-1, 1)))

  fall_length  = 2
  afall_length = 0
  for j in range(TERRAIN_SIZE):
    for i in range(fall_length):
      terrain.set_vertex_option(i, j, *out_of_map_vertex_options)
      #terrain.set_vertex_color(i, j, (0.0, 0.0, 0.0, 0.0))
      terrain.set_height(i, j, 0.0)
    terrain.set_height(i + 1, j, 0.92 * terrain.get_height(i + 1, j))
    if j % 2:
      fall_length = max(1, fall_length + afall_length)
      if (fall_length == 1) and (afall_length == -1): afall_length = 0
      else: afall_length = max(-1, min(1, afall_length + random.randint(-1, 1)))
      
  fall_length  = 2
  afall_length = 0
  for j in range(TERRAIN_SIZE):
    for i in range(TERRAIN_SIZE - 1, TERRAIN_SIZE - fall_length - 1, -1):
      terrain.set_vertex_option(i, j, *out_of_map_vertex_options)
      #terrain.set_vertex_color(i, j, (0.0, 0.0, 0.0, 0.0))
      terrain.set_height(i, j, 0.0)
    terrain.set_height(i - 1, j, 0.92 * terrain.get_height(i - 1, j))
    if j % 2:
      fall_length = max(1, fall_length + afall_length)
      if (fall_length == 1) and (afall_length == -1): afall_length = 0
      else: afall_length = max(-1, min(1, afall_length + random.randint(-1, 1)))



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
        #soya.set_quality( 1 )

        soya.World.__init__( self )

        self.DATA_PATH = a_DataPath != None and a_DataPath or path.join( getcwd(), "data" )

        self.m_Camera = oglCamera( self )
        self.m_Camera.set_xyz( 16.0, 6.0, 0.0 )
        self.m_Camera.look_at( soya.Point( self, 16.0, -6.0, 10.0) )

        self.m_Camera.add_vector( soya.Vector( None, 10.0, 0.0, 0.0 ) )

        self.m_Camera.back = 100
        soya.set_root_widget( self.m_Camera )

        soya.set_root_widget( soya.widget.Group() )
        soya.root_widget.add( self.m_Camera )
        soya.root_widget.add( soya.widget.FPSLabel() )


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
        terrain_size = 256
        self.terrain = soya.Terrain( self, terrain_size, terrain_size )
        random_terrain_border( self.terrain )
		  
		  
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
        
        g = f.CreateGrid()
        
        g.print_grid()
        
        p = PathFinder( g, ( 25, 37 ), [( 30, 30 )] )
        
        path = p.Draw( self, 3 , 2.0, 1.5 )
        
        # g.save_file( "%s/map.txt" % self.DATA_PATH, p.path )
        
        # s = LoadableRegion( self, a_AssetManager=self.AssetManager )
##        pickle_file = open( "%s/environment/floors/first.pkl" % self.DATA_PATH, "r" )
##        s = pickle.load( pickle_file )
##        pickle_file.close()
        # s.Load( "%s/environment/floors/first.flr" % self.DATA_PATH )

       
        model_builder = soya.SimpleModelBuilder()
        model_builder.shadow = 1
        
        b = soya.Body( self, f.to_model() )
        b.y = 0.01 
        
##        b = soya.Body( self, s.to_model() )
##        b.y = 4.85 

        sorcerer_model = soya.AnimatedModel.get("balazar")
        tex = soya.Material( soya.Image.get( "balazar.png" ) )
        sorcerer_model.material = tex
        sorcerer_model.shadow = 1
        sorcerer = soya.Body(self, sorcerer_model)
        sorcerer.animate_blend_cycle("attente")
        # sorcerer.y = 5
        sorcerer.x = ( 25 * 3 ) + 1.5
        sorcerer.z = ( 36 * 3 ) + 1.5

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


