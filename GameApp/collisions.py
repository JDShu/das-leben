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

from vector_3d import *

class BoundingBox3d( Vector3d ):
    ''' this is a AAB type bounding box '''
    def __init__( self, a_X=0.0, a_Y=0.0, a_Z=0.0, a_Size=1.0 ):
        Vector3d.__init__( self, a_X, a_Y, a_Z )
        self.m_Width = a_Size / 2.0
        
    def PointInside( self, a_Vector3d=None ):
        inside = False
        match_count = 0
        
        x, y, z, w = self.GetPosition()
        
        if a_Vector3d.GetX() >= ( x - self.m_Width ) and a_Vector3d.GetX() <= ( x + self.m_Width ):
            match_count += 1
        if a_Vector3d.GetY() >= ( y - self.m_Width ) and a_Vector3d.GetY() <= ( y + self.m_Width ):
            match_count += 1
        if a_Vector3d.GetZ() >= ( z - self.m_Width ) and a_Vector3d.GetZ() <= ( z + self.m_Width ):
            match_count += 1
            
        if match_count > 2:
            inside = True
            
        return inside
    
##    def CollidesWithBoundingBox( self, a_BoundingBox ):
##        collides = False
##        collides_count = 0
##        for point in a_BoundingBox:
##            collides_count =+ self.PointInside( point ) and 1 or 0
##            
##        if collides_count > 0:
##            collides = True
##            
##        return collides
    