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

ANGLE_PI = 3.141592654

class Angle:
    '''Angle class'''
    def __init__(self, a_Angle=0.0):
        if isinstance( a_Angle, Angle ):
            self.m_Angle = a_Angle.GetAngle()

        elif type( a_Angle ) is int or float:
            self.m_Angle = a_Angle
            # print "is a float or int : %s = %s = %s \n" % ( type( a_Angle ), a_Angle , self.m_Angle )

        else:
            return NotImplemented

    def __eq__(self, rhs):
        l_ReturnVal = False
        if isinstance( rhs, Angle ):
            l_ReVal = ( self.m_Angle == rhs.GetAngle() )        
        elif type( rhs ) is int or float:
            l_RetVal = ( self.m_Angle == rhs )
        
        else:
            return NotImplemented

        return l_RetVal

    def __ne__(self, rhs):
        l_ReturnVal = False
        if isinstance( rhs, Angle ):
            l_ReVal = ( self.m_Angle != rhs.GetAngle() )        
        elif type( rhs ) is int or float:
            l_RetVal = ( self.m_Angle != rhs )
        
        else:
            return NotImplemented

        return l_RetVal

    def __gt__(self, rhs):
        l_ReturnVal = False
        if isinstance( rhs, Angle ):
            l_ReVal = ( self.m_Angle > rhs.GetAngle() )        
        elif type( rhs ) is int or float:
            l_RetVal = ( self.m_Angle > rhs )
        
        else:
            return NotImplemented

        return l_RetVal

    def __lt__(self, rhs):
        l_ReturnVal = False
        if isinstance( rhs, Angle ):
            l_ReVal = ( self.m_Angle < rhs.GetAngle() )        
        elif type( rhs ) is int or float:
            l_RetVal = ( self.m_Angle < rhs )
        
        else:
            return NotImplemented

        return l_RetVal


    def __add__(self, rhs):
        
        if isinstance( rhs, Angle ):
            self.m_Angle += rhs.GetAngle()        
        elif type( rhs ) is int or float:
            self.m_Angle += rhs
        
        else:
            return NotImplemented

        if self.m_Angle > 360.0:
            self.m_Angle -= 360.0

        return Angle(self)

    def __sub__(self, rhs):
        
        if isinstance( rhs, Angle ):
            self.m_Angle -= rhs.GetAngle()        
        elif type( rhs ) is int or float:
            self.m_Angle -= rhs
        
        else:
            return NotImplemented
        
        if self.m_Angle < 0.0:
            self.m_Angle += 360.0

        return Angle(self)

    def __radd__(self, rhs):
        return self.__add__( rhs )

    def __rsub__(self, rhs):
        return self.__sub__( rhs )

    def GetAngle(self):
        return self.m_Angle

    def GetAngleInRadians(self):
        return (self.m_Angle / 180.0 * ANGLE_PI)

    def SetAngle(self, a_Angle):
        self.m_Angle = a_Angle
    
    def Print(self):
        print "Angle is %s" % self.m_Angle
