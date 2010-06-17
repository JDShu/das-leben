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

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from vector_3d import *
from angle import *
import soya

class oglCamera( soya.Camera ):
    def __init__( self, a_Scene ):
        soya.Camera.__init__( self, a_Scene )
        self.speed = soya.Vector( self )
        self.rot_y = 0.0
        self.rot_x = 0.0

    def begin_round( self ):
        soya.Camera.begin_round( self )

    def advance_time( self, proportion ):
        self.add_xyz( self.speed.x * proportion,
                      self.speed.y * proportion,
                      self.speed.z * proportion )
        self.rotate_y( self.rot_y * proportion )
        self.rotate_x( self.rot_x * proportion )

    def Fly ( self, relative_y_angle, relative_x_angle, speed, multiyplier ):
        pass
##        x, y, z, w = self.GetPosition()
##        roh = radians(self.m_YRot.GetAngle() + relative_y_angle)
##        theta = radians(relative_x_angle)
##        x -= speed * cos(theta) * sin(roh)
##        z += speed * cos(theta) * cos(roh)
##        y += speed * sin(theta)
##
##        self.SetPosition( x, y, z, w )




    def MoveForward( self ):
        self.Fly(0,0,1)

    def MoveBackward( self ):
        self.Fly(180,0,0.25)

    def MoveLeft( self ):
        self.Fly(-90,0,0.25)

    def MoveRight( self ):
        self.Fly(90,0,0.25)

    def ZoomIn( self ):
        self.Fly(0,self.m_XRot.GetAngle(),0.25)

    def ZoomOut( self ):
        self.Fly(180,-self.m_XRot.GetAngle(),0.25)
