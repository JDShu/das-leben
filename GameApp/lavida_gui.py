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

import soya, soya.gui
from soya.gui import Group, Widget, HighlightableWidget, Button
import soya.opengl as opengl
from logger import *
from angle import Angle
from math import cos, sin
from system import ActionEvent, AvatarAction

class LaVidaMenuStyle( soya.gui.style.Style ):
    def __init__( self ):
        soya.gui.style.Style.__init__( self )

        self.materials[0].diffuse = (0.5, 0.5, 0.8, 1.0) # Button background
        self.materials[1].diffuse = (0.5, 0.5, 0.9, 1.0) # Selected
        self.materials[3].diffuse = (1.0, 1.0, 0.8, 1.0) # Selected window title

        self.materials[2].diffuse = (0.4, 0.4, 0.8, 1.0) # Window title background
        self.materials[3].diffuse = (0.5, 0.5, 0.8, 1.0) # Selected window title
        self.materials[4].diffuse = (1.0, 1.0, 1.0, 0.9) # Window background
        b  = (0.0, 0.6, 0.8, 1.0)
        b2 = (0.0, 0.5, 0.8, 1.0)
        self.corner_colors = [
            b, # Base
            b, # Selected
            b2, # Window title
            b2, # Selected window title
            (0.4, 0.9, 1.0, 0.9), # Window background
        ]
        self.line_colors = [
            b, # Base
            b, # Selected
            b2, # Window title
            b2, # Selected window title
            b, # Window background
        ]
        self.text_colors = [
            (0.0, 0.0, 0.0, 1.0), # Base
            #(0.0, 0.2, 0.0, 1.0), # Selected
            (0.7, 0.7, 1.0, 1.0), # Selected
            (1, 1, 1, 1.0), # Window title
        ]
        self.line_width = 1

class LavidaGameUI( Group ):
    def __init__( self ):
        soya.gui.Window( self )

class LavidaActionButton( Button, HighlightableWidget ):
    def __init__( self, parent, text = u"", on_clicked=None, event_queue=None ):
        Button.__init__( self, parent, text, on_clicked )
        HighlightableWidget.__init__( self )
        
        self.material = soya.Material()
        
        self.radius = 64 * 0.5 # width in pixels / 2

        self.x1 = -self.radius
        self.y1 = -self.radius
        self.x2 = self.radius
        self.y2 = self.radius
        
        self.event_queue = event_queue

    def render( self ):
        if self.material:
            self.material.activate()
            opengl.glEnable( opengl.GL_BLEND )
            opengl.glBegin   (opengl.GL_QUADS)
            opengl.glTexCoord2f(0.0, 0.0); opengl.glVertex2i(self.x + self.x1, self.y + self.y1)
            opengl.glTexCoord2f(0.0, 1.0); opengl.glVertex2i(self.x + self.x1, self.y + self.y2)
            opengl.glTexCoord2f(1.0, 1.0); opengl.glVertex2i(self.x + self.x2, self.y + self.y2)
            opengl.glTexCoord2f(1.0, 0.0); opengl.glVertex2i(self.x + self.x2, self.y + self.y1)
            opengl.glEnd()
            opengl.glDisable( opengl.GL_BLEND )
            
    def on_highlight( self, highlight ):
        HighlightableWidget.on_highlight( self, highlight )
        self.material.diffuse = ( 1.0, 1.0, 1.0, 1.0 )

class LavidaPieMenu( Group, HighlightableWidget ):
    def __init__( self, parent=None ):
        Group.__init__( self, parent )
        HighlightableWidget.__init__( self )
        self.material = soya.Material( soya.Image.get( "circular_menu.png" ) )

        self.radius = 128

        self.x1 = -self.radius
        self.y1 = -self.radius
        self.x2 = self.radius
        self.y2 = self.radius
 

    def move( self, x, y ):
        Group.move( self, x, y )
        self.x = x
        self.y = y

    def render( self ):
        if self.visible:
            if self.material:
                self.material.activate()
                opengl.glEnable( opengl.GL_BLEND )
                opengl.glBegin   (opengl.GL_QUADS)
                opengl.glTexCoord2f(0.0, 0.0); opengl.glVertex2i(self.x + self.x1, self.y + self.y1)
                opengl.glTexCoord2f(0.0, 1.0); opengl.glVertex2i(self.x + self.x1, self.y + self.y2)
                opengl.glTexCoord2f(1.0, 1.0); opengl.glVertex2i(self.x + self.x2, self.y + self.y2)
                opengl.glTexCoord2f(1.0, 0.0); opengl.glVertex2i(self.x + self.x2, self.y + self.y1)
                opengl.glEnd()
                opengl.glDisable( opengl.GL_BLEND )
        Group.render(self)

    def on_highlight( self, highlight ):
        HighlightableWidget.on_highlight( self, highlight )

    def on_mouse_pressed(self, button, x, y):
        widget = self.widget_at(x, y)
        if widget:
            widget.on_mouse_pressed( button, x, y )
        
    def widget_at( self, x, y ):
        for widget in self.widgets:
            if x >= ( widget.x - widget.radius ) and x <= ( widget.x + widget.radius ):
                if y >= ( widget.y - widget.radius ) and y <= ( widget.y + widget.radius ):
                    return widget
                
        return None
        
        
class StandardActionsMenu( LavidaPieMenu ):
    def __init__( self, parent, event_queue ):
        LavidaPieMenu.__init__( self, parent )
        
        btn = MoveToButton( self, event_queue )
        btn = UseStairsButton( self, event_queue )
        btn = TalkToAvatar( self, event_queue )
        
        step = 360 / len( self.widgets ) # step in degrees
        
        angle = Angle( step )
        
        for i, widget in enumerate( self.widgets ):
            widget.y = -80
            widget.x = 0
            
            theta = angle.GetAngleInRadians()
            widget.x = ( widget.x * cos( theta ) ) - ( widget.y * sin( theta ) )
            widget.y = ( widget.x * sin( theta ) ) + ( widget.y * cos( theta ) )
            
            angle += step
            

class MoveToButton( LavidaActionButton ):
    def __init__( self, parent, event_queue ):
        LavidaActionButton.__init__( self, parent, event_queue=event_queue )
        self.material = soya.Material( soya.Image.get( "go_here.png" ) )
        self.event_queue = event_queue
        
    def on_mouse_pressed( self, button, x, y ):
        LOG_DBG( self, "goto button clicked" )
        
        event = ActionEvent( "move_to" )
        actions = AvatarAction( "move_to", [ self.parent.x, self.parent.y ], "selected_avatar" )
        event.AddAction( actions )
        
        self.event_queue.Push( event )
        
        self.parent.visible = 0
        
        
class UseStairsButton( LavidaActionButton ):
    def __init__( self, parent, event_queue ):
        LavidaActionButton.__init__( self, parent, event_queue=event_queue )
        self.material = soya.Material( soya.Image.get( "use_stairs.png" ) )
        #self.material.diffuse = ( 0.8, 0.8, 0.8, 1.0 )
        
class TalkToAvatar( LavidaActionButton ):
    def __init__( self, parent, event_queue ):
        LavidaActionButton.__init__( self, parent, event_queue=event_queue )
        self.material = soya.Material( soya.Image.get( "talk_to.png" ) )
        #self.material.diffuse = ( 0.8, 0.8, 0.8, 1.0 )
        
        