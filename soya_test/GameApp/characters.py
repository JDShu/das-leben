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
from buildings import *

DUDE = 1
DUDETTE = 2
DUDELE = 3

AVATAR_IDLE = 1
AVATAR_WALKING = 2

AVATAR_EATING = 3
AVATAR_REACHED_DESTINATION = 4
AVATAR_VELOCITY = 2.0

class AttachedItem:
    def __init__( self, a_ItemName, a_Instance ):
        self.name = a_ItemName
        self.instance = a_Instance

class Avatar( soya.World ):
    def __init__( self, a_Scene, a_Type=DUDE, a_AssetManager=None ):
        soya.World.__init__( self, a_Scene )
        if a_Type == DUDE:
            avatar_filename = "dude" 
        elif a_Type == DUDETTE:
            avatar_filename = "dudette"
            
        avatar_filename = "balazar"
        # model = a_AssetManager.GetAnimatedModel( avatar_filename )

        model = soya.AnimatedModel.get( avatar_filename )
        model.shadow = 1
        self.avatar = soya.Body( self, model )
        self.avatar.animate_blend_cycle("attente")

        self.current_animation = "attente"

        self.attachments = []
        self.travelling = False

        self.speed          = soya.Vector(self)
        self.rotation_speed = 0.0

        # We need radius * sqrt(2)/2 < max speed (here, 0.35)
        self.radius         = 0.5
        self.radius_y       = 1.0
        self.center         = soya.Point(self, 0.0, self.radius_y, 0.0)
        
        self.m_Behaviour = AVATAR_IDLE
        self.m_Scene = a_Scene
        
        self.m_ExecuteQueue = []

    def begin_round( self ):
        soya.Model.begin_round( self )
        
    def AddAction( self, action ):
        self.m_ExecuteQueue.append( action )
        
    def GetNextAction( self ):
        if self.m_ExecuteQueue != []:
            del self.m_ExecuteQueue[ 0 ]
        return self.m_ExecuteQueue != [] and self.m_ExecuteQueue[ 0 ] or None

    def PlayAnimation( self, animation ):
        if self.current_animation != animation:

            # Stops previous animation
            self.avatar.animate_clear_cycle(self.current_animation, 0.2)

            # Starts the new one
            self.avatar.animate_blend_cycle(animation, 1.0, 0.2)

            self.current_animation = animation

    def advance_time( self, proportion ):
        soya.World.advance_time( self, proportion )

        self.DoBehaviours( proportion )

        # self.rotate_y( proportion * self.rotation_speed )


    def AttachItem( self, a_ItemName, a_BoneName, a_AssetManager ):
        item = soya.World( self )
        self.attach_to_bone( item, a_BoneName )
        positioning = a_AssetManager.GetPositioningInfo( a_ItemName )
        item_body = soya.Body( item, a_AssetManager.GetModel( a_ItemName ) )
        item_body.rotate_x( positioning[ 'rotate_x' ] )
        item_body.rotate_y( positioning[ 'rotate_y' ] )
        item_body.rotate_z( positioning[ 'rotate_z' ] )
        item_body.set_xyz( positioning[ 'x' ], positioning[ 'y' ], positioning[ 'z' ] )

        attachment = AttachedItem( a_ItemName, item_body )
        self.attachments.append( attachment )

    def DetachItem( self, a_ItemName, a_BoneName ):
        for i, attachment in enumerate( self.attachments ):
            if a_ItemName == attachment.name: 
                self.detach_from_bone( attachment.instance, a_BoneName )
                del attachment.instance
                del self.attachments[ i ]

    def DoBehaviours(self, proportion ):
        if self.m_Behaviour == AVATAR_WALKING:
            self.MoveToDestination( proportion )
        elif self.m_Behaviour == AVATAR_REACHED_DESTINATION:
            action = self.GetNextAction()
            if action:
                pass
            else:
                self.m_Behaviour = AVATAR_IDLE
                self.PlayAnimation( "attente" )

    def UseWaypoints( self, path ):
        self.PlayAnimation( "marche" )
        self.m_Behaviour = AVATAR_WALKING
        self.destination = path[ -1 ]
        self.path = path[ : ]
        
        self.destination_x = ( self.path[ len( self.path ) - 1 ][ 0 ] * 3 ) + 1.5
        self.destination_z = ( self.path[ len( self.path ) - 1 ][ 1 ] * 3 ) + 1.5
        src = soya.Vector( self.m_Scene,  self.x, 0, self.z ) 
        dest = soya.Vector( self.m_Scene,  self.destination_x, 0, self.destination_z ) 
        
        self.speed = src >> dest
        self.speed.set_length( 1.0 )
        
        self.speed /= 10.0
        
        del self.path[ len( self.path ) - 1 ]

    def Arrived( self ):
        THRESHOLD = 0.5
    
        if self.x >= ( self.destination_x - THRESHOLD ) and self.x <= ( self.destination_x + THRESHOLD ):
            if self.z >= ( self.destination_z - THRESHOLD ) and self.z <= ( self.destination_z + THRESHOLD ):
                return True

        return False

    def MoveToDestination( self, proportion ):
        if not self.Arrived():
            self.add_mul_vector(proportion, self.speed)
        else:
            if self.path != []:
                self.destination_x = ( self.path[ len( self.path ) - 1 ][ 0 ] * 3 ) + 1.5
                self.destination_z = ( self.path[ len( self.path ) - 1 ][ 1 ] * 3 ) + 1.5
                src = soya.Vector( self.m_Scene,  self.x, 0, self.z ) 
                dest = soya.Vector( self.m_Scene,  self.destination_x, 0, self.destination_z ) 
                
                self.speed = src >> dest
                self.speed.set_length( 1.0 )
                
                self.speed /= 10.0
                del self.path[ len( self.path ) - 1 ]
                self.look_at( soya.Point( self.m_Scene, self.destination_x, 0.0, self.destination_z ) )
            else:
                self.m_Behaviour = AVATAR_REACHED_DESTINATION
