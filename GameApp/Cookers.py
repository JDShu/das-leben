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
        
        btn = UseCookerButton( self, event_queue )
        
        self.SetupIcons()
        
class UseCookerButton( LavidaActionButton ):
    def __init__( self, parent, event_queue ):
        LavidaActionButton.__init__( self, parent, event_queue=event_queue )
        self.material = soya.Material( soya.Image.get( "go_here.png" ) )
        self.x = -80
        self.y = 0
        