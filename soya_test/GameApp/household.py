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

import soya
from system import ActionEvent, AvatarAction

class HouseholdItem( soya.World ):
    def __init__( self, parent, menu_root, a_Filename, event_queue=None, model_builder=None ):
        soya.World.__init__( self, parent )
        
        m = soya.Model.get( a_Filename )
        if model_builder:
            m.model_builder = model_builder
            
        
            
        self.body = soya.Body( self, m )
        
        
        self.event_queue = event_queue
        self.menu_root = menu_root
        self.menu = None
        self.menu_items = []
        self.actions = []
        cancel = ActionEvent( "cancel_event" )
        cancel.AddAction( AvatarAction( "cancel_action" ) )
        self.actions.append( { "cancel" : cancel } )
        
    def GetAction( self, name ):
        for action in self.actions:
            if action.keys() == name:
                return action[ name ]
            
        return None
            
    def BuildMenu( self ): pass
    
    def SetPosition( self, x, y, z ): 
        self.body.x = x
        self.body.y = y
        self.body.z = z
    
            
        
        
        
        