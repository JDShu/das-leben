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

from math import sqrt
       
class Vector3d:
    '''3d Vector'''

    def __init__(self):
        self.m_Values = [0.0, 0.0, 0.0, 1.0]
        
    def __repr__( self ):
        return "Setting Position : %s, %s, %s, %s\n" % ( self.m_Values[0], self.m_Values[1], 
                                                        self.m_Values[2], self.m_Values[3] )

    def SetPosition(self, a_X, a_Y, a_Z, a_W=1.0):
        self.m_Values[0] = a_X
        self.m_Values[1] = a_Y
        self.m_Values[2] = a_Z
        self.m_Values[3] = a_W
        
    def Print( self ):
        print "Setting Position : %s, %s, %s, %s\n" % ( self.m_Values[0], self.m_Values[1], 
                                                        self.m_Values[2], self.m_Values[3] )

    def GetPosition(self):
        return self.m_Values    

    def GetX(self):
        return self.m_Values[0]

    def GetY(self):
        return self.m_Values[1]

    def GetZ(self):
        return self.m_Values[2]

    def GetW(self):
        return self.m_Values[3]
    
    def Length(self):
        return sqrt(( self.m_Values[0] * self.m_Values[0] ) + 
                    ( self.m_Values[1] * self.m_Values[1] ) +
                    ( self.m_Values[2] * self.m_Values[2] ) )

    def Normalise(self):
        l_Length = self.Length()
        #print "Lenght = %s\n" % l_Length
        if l_Length == 0:
            self.m_Values[0] = 0.0
            self.m_Values[1] = 0.0
            self.m_Values[2] = 0.0
        else:
            self.m_Values[0] /= l_Length
            self.m_Values[1] /= l_Length
            self.m_Values[2] /= l_Length

    def Dot(self, rhs):
        return (self.m_Values[0] * rhs.GetX() + 
                self.m_Values[1] * rhs.GetY() +
                self.m_Values[2] * rhs.GetZ())
    
    def CrossProduct(self, rhs):
        l_Vector = Vector3d()
        l_Vector.SetPosition( self.m_Values[1] * rhs.GetZ() - self.m_Values[2] * rhs.GetZ() ,
                              self.m_Values[2] * rhs.GetX() - self.m_Values[0] * rhs.GetZ() ,
                              self.m_Values[0] * rhs.GetY() - self.m_Values[1] * rhs.GetX() )
        return l_Vector
                              