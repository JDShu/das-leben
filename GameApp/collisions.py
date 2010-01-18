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

class BoundingBox3d:
    ''' this is a AAB type bounding box '''
    def __init__( self, a_X=0.0, a_Y=0.0, a_Z=0.0, a_Size=1.0 ):
        self.points = []; padd = self.points.append
        self.Topupperleft = Vector3d(-1.0, 1.0, 1.0 ).Scale( a_Size )
        padd( self.Topupperleft )
        self.Toplowerleft = Vector3d(-1.0, 1.0, -1.0 ).Scale( a_Size )
        padd( self.Toplowerleft )
        self.Topupperright = Vector3d(1.0, 1.0, -1.0 ).Scale( a_Size )
        padd( self.Topupperright )
        self.Toplowerright = Vector3d(1.0, 1.0, 1.0 ).Scale( a_Size )
        padd( self.Toplowerright )
        self.Bottomupperleft = Vector3d(-1.0, -1.0, 1.0 ).Scale( a_Size )
        padd( self.Bottomupperleft )
        self.Bottomlowerleft = Vector3d(-1.0, -1.0, -1.0 ).Scale( a_Size )
        padd( self.Bottomlowerleft )
        self.Bottomupperright = Vector3d(1.0, -1.0, -1.0 ).Scale( a_Size )
        padd( self.Bottomupperright )
        self.Bottomlowerright = Vector3d(1.0, -1.0, 1.0 ).Scale( a_Size )
        padd( self.Bottomlowerright )
        
    def PointInside( self, a_Vector3d=None ):
        inside = False
        match_count = 0
        if a_Vector3d >= self.Bottomlowerleft and a_Vector3d <= self.Bottomlowerright:
            match_count += 1
        if a_Vector3d >= self.Bottomlowerleft and a_Vector3d <= self.Bottomupperleft:
            match_count += 1
        if a_Vector3d >= self.Bottomlowerleft and a_Vector3d <= self.Toplowerleft:
            match_count += 1
            
        if match_count > 2:
            inside = True
            
        return inside
    
    def CollidesWithBoundingBox( self, a_BoundingBox ):
        collides = False
        collides_count = 0
        for point in a_BoundingBox:
            collides_count =+ self.PointInside( point ) and 1 or 0
            
        if collides_count > 0:
            collides = True
            
        return collides
    