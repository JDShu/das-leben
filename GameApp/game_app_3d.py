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

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import CardMaker
from direct.task import Task

from math import pi, sin, cos

import wall_layout

#old stuff
import sys
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

os.environ['SDL_VIDEO_CENTERED'] = '1'

NORMAL_MODE = 1
EDIT_MODE = 2

MAP_SIZE = 20


class GameApp3d(ShowBase):
    """
    The main game class which manages all other processes
    """
    def __init__(self):
                
        ShowBase.__init__(self)
        #initialize camera
        #self.disableMouse()
        self.load_graphics()
        self.camera.setPos(-15,-15,10)
        self.camera.setHpr(-40,-25,0)
        
        #initialize screen
        #initialize gui
        
        self.selected_object = None
        self.edit_terrain = False
        #self.SetupLighting()
        #self.SetupFog()
        #self.SetupKeyBuffer()
        #self.SetupEventQueue()
        #self.SetupGUI()

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

    def load_graphics( self ):
        '''load all 3d objects and models'''
        # floor terrain
        cm = CardMaker("floor")
        cm.setFrame(0, MAP_SIZE, 0, MAP_SIZE)
        card = cm.generate()
        floor = self.render.attachNewNode(card)
        floor.setP(270)
        grass_texture = self.loader.loadTexture("./data/images/grass.png")
        floor.setTexture(grass_texture)

        # TODO: system to load all objects as specified from a file
        self.oven = self.loader.loadModel("./data/egg/oven")
        self.oven.reparentTo(self.render)
        self.oven.setScale(0.49, 0.49, 0.49)
        self.oven.setPos(1.495, 1.495, 0.495)

        # TODO: encapsulate wall generation
        walls = wall_layout.WallLayout()
        walls.load_textfile("./data/games/sample.wall")

        for x, row in enumerate(walls.get_layout()):
            for y, wall in enumerate(row):
                if wall == wall_layout.EMPTY:
                    pass
                elif wall == wall_layout.HORIZONTAL:
                    self.make_horizontal_wall((x,y))
                elif wall == wall_layout.VERTICAL:
                    self.make_vertical_wall((x,y))
                elif wall == wall_layout.BOTH:
                    self.make_horizontal_wall((x,y))
                    self.make_vertical_wall((x,y))
                    
        # TODO: system to load floors
        
        # TODO: characters

    def make_horizontal_wall(self, pos):
        x, y = pos
        cm = CardMaker("wall")
        cm.setFrame(0, 1, 0, 2)
        front_card = cm.generate()
        front = self.render.attachNewNode(front_card)
        front.setH(90)
        front.setPos(x,y,0)
        back_card = cm.generate()
        back = self.render.attachNewNode(back_card)
        back.setH(270)
        back.setPos(x,y+1,0)

    def make_vertical_wall(self, pos):
        x, y = pos
        cm = CardMaker("wall")
        cm.setFrame(0, 1, 0, 2)
        front_card = cm.generate()
        front = self.render.attachNewNode(front_card)
        front.setH(0)
        front.setPos(x,y,0)
        back_card = cm.generate()
        back = self.render.attachNewNode(back_card)
        back.setH(180)
        back.setPos(x+1,y,0)

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
                if event[1] == soya.sdlconst.BUTTON_LEFT:
                    self.pie_menu.visible = 0
                if event[1] == soya.sdlconst.BUTTON_RIGHT:
                    self.pie_menu.visible = 1
                    self.pie_menu.move( event[2], event[3] )
                    
            
            for event in self.m_EventQueue.events:
                if event.category == ACTION:
                    if not event.prepared:
                        self.PrepareActionEvent( event )

    def PrepareActionEvent( self, event ):
        if event.name == "move_to":
            data = event.GetCurrentAction().data[ 0 ]
            mouse = self.m_Camera.coord2d_to_3d( data[0], data[1] )
            result = self.raypick( self.m_Camera, self.m_Camera.vector_to( mouse ) )
            impact, normal = result
            event.GetCurrentAction().data[ 0 ] = impact
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

    def PrintToConsole(self, a_Message, a_LineNumber ):
        '''
        Print a message to the console on a specific line
        @param a_Message String : a message to display
        @param a_LineNumber Integer: the line to pront your message
        '''

    def AddMessage( self, a_Message ):
        '''
        Add a message to the console message queue
        @param a_Message String : a message to display
        '''
        print "%s\n" % a_Message


