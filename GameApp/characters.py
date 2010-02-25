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
from vector_3d import *
from md2 import IDLE1, RUN

DUDE = 1
DUDETTE = 2
DUDELE = 3

AVATAR_IDLE = 1
AVATAR_WALKING = 2
AVATAR_EATING = 3

AVATAR_VELOCITY = 2.0

class Avatar( Object3d ):
    def __init__( self, a_DataPath, a_Type ):
        if a_Type == DUDE:
            Object3d.__init__( self, "%s/avatar/tris.md2" % a_DataPath, 
                               "%s/avatar/REI.PCX" % a_DataPath, 
                               object_type=OBJECT_3D_ANIMATED_MESH )
        elif a_Type == DUDETTE:
            Object3d.__init__( self, "%s/avatar/tris.md2" % a_DataPath, 
                               "%s/avatar/REI.PCX" % a_DataPath, 
                               object_type=OBJECT_3D_ANIMATED_MESH )

        self.m_XRot.SetAngle( -90 )
        self.m_ZRot.SetAngle( -90 )
        self.SetAnimation( IDLE1 )
        self.SetScale( 2 )

        self.m_Speed = 2.0 # units per second
        self.m_Behavior = AVATAR_IDLE
        self.m_FollowingBehaviours = []
        self.m_Destination = Vector3d()
        self.m_Ticks = 0
        self.m_ModelHeight = 0.5


    def MoveToDestination( self ):
        l_Destination = self.m_Destination
        l_Position = self.GetPositionVector()
        l_Direction = l_Destination - l_Position
        l_Direction.Normalise()
        l_Direction.Scale( float( self.m_Ticks ) / 1000.0 * AVATAR_VELOCITY )
        l_Position = l_Position + l_Direction
        self.SetPosition( l_Position.GetX(), l_Position.GetY(), l_Position.GetZ() )

    def SetBehaviour( self, a_Behaviour, a_FollowingBehaviours=[] ):
        '''set a behaviour and then append any following actions/behaviours'''
        self.m_Behavior = a_Behaviour
        for behaviour in a_FollowingBehaviours:
            self.m_FollowingBehaviours.append( behaviour )

        if a_Behaviour == AVATAR_WALKING:
            self._model.SetAnimation( RUN )
        if a_Behaviour == AVATAR_IDLE:
            self._model.SetAnimation( IDLE1 )

    def SetDestination( self, a_Destination ):
        self.m_Destination.SetPosition( a_Destination.GetX(),
                                        a_Destination.GetY() + self.m_ModelHeight,
                                        a_Destination.GetZ() )

    def UpdateTicks( self, a_Ticks ):
        self.m_Ticks = a_Ticks 

    def DoBehaviours(self):
        if self.m_Behavior == AVATAR_WALKING:
            self.MoveToDestination()
            l_Position = self.GetPositionVector()
            if l_Position == self.m_Destination:
                self.m_Behavior = AVATAR_IDLE
                self._model.SetAnimation( IDLE1 )

