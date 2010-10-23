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

from numpy import array, matrix

class Bone:
    def __init__( self, a_Name, a_Parent, a_Matrix ):
        self.m = a_Matrix
        self.name = a_Name
        self.parent = a_Parent
        
class Skeleton:
    def __init__( self ):
        self.bones = {}
        self.bone_matices = [];
        
    def AddBone( self, a_Bone ):
        self.bones[ a_Bone.name ] = a_Bone
        self.bone_matices.append( a_Bone.m )