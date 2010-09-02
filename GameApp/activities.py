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

from system import ActionEvent, AvatarAction

class MoveTo( ActionEvent ):
    def __init__( self, **kwargs ):
        ActionEvent.__init__( self, "move to" )
        action = AvatarAction( "move to", [ kwargs[ 'x' ], kwargs[ 'y' ] ], "selected_avatar" )
        self.AddAction( action )
        
    @classmethod
    def IsActivityHandler( self, name ):
        return name == "move to"

def Activity( activity_name, **kwargs ):
    for cls in ActionEvent.__subclasses__():
        if cls.IsActivityHandler( activity_name ):
            return cls( **kwargs )
        
    return None