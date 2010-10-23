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
from base_objects import CookerBase
from lavida_gui import LavidaPieMenu, LavidaActionButton
from system import ActionEvent, AvatarAction
from activities import Activity
import soya

class Oven( CookerBase ):
    def __init__( self, parent, menu_root, event_queue=None, model_builder=None ):
        CookerBase.__init__( self, parent, menu_root, "oven", event_queue, model_builder )
        
        self.body.y = 1.0
        
    def SetPosition( self, x, y, z ):
        CookerBase.SetPosition( self, x, y + 1.0, z )
        
    def GetMenu( self ):
        if not self.menu:
            self.menu = CookerActionsMenu( self.parent.root, self.event_queue )
            
        return self.menu

class CookerActionsMenu( LavidaPieMenu ):
    def __init__( self, parent, event_queue ):
        LavidaPieMenu.__init__( self, parent )
        
        btn = CookMealButton( self, event_queue )
        
        self.SetupIcons()
        
class CookMealButton( LavidaActionButton ):
    def __init__( self, parent, event_queue ):
        LavidaActionButton.__init__( self, parent, event_queue=event_queue )
        self.material = soya.Material( soya.Image.get( "go_here.png" ) )
        self.x = -80
        self.y = 0
        
    def on_mouse_pressed( self, button, x, y ):
        LavidaActionButton.on_mouse_pressed( self, button, x, y )
        
        event = Activity( "cook meal", x=self.parent.x, y=self.parent.y )
        
        self.event_queue.Push( event )
        
class CookMealActivity( ActionEvent ):
    def __init__( self, **kwargs ):
        ActionEvent.__init__( self, "cook meal" )
        # travel to the cooker
        action = AvatarAction( "move to", [ kwargs[ 'x' ], kwargs[ 'y' ] ], "selected_avatar" )
        self.AddAction( action )
        
        # use the cooker
        
        # eat meal
        
    @classmethod
    def IsActivityHandler( self, name ):
        return name == "cook meal"
        