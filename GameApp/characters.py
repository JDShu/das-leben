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

from object_3d import *

DUDE = 1
DUDETTE = 2
DUDELE = 3

class Avatar( Object3d ):
    def __init__( self, a_DataPath, a_Type ):
        if a_Type == DUDE:
            Object3d.__init__( self, "%s/data/avatar/tris.md2" % a_DataPath, 
                               "%s/data/avatar/REI.PCX" % a_DataPath, 
                               object_type=OBJECT_3D_ANIMATED_MESH )
        elif a_Type == DUDETTE:
            Object3d.__init__( self, "%s/data/avatar/tris.md2" % a_DataPath, 
                               "%s/data/avatar/REI.PCX" % a_DataPath, 
                               object_type=OBJECT_3D_ANIMATED_MESH )
            
        self.m_XRot.SetAngle( -90 )
	self.m_ZRot.SetAngle( -90 )
	self.SetAnimation( IDLE1 )
	self.SetScale( 2 )
            
        self.m_Speed = 2.0 # units per second
            
    def MoveTo( self, a_X, a_Y, a_Z ):
        pass 