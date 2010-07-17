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

DUDE = 1
DUDETTE = 2
DUDELE = 3

AVATAR_IDLE = 1
AVATAR_WALKING = 2
AVATAR_EATING = 3

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

        self.model = a_AssetManager.GetAnimatedModel( avatar_filename )
        
        self.attachments = []
        
    def begin_round( self ):
        soya.Model.begin_round( self )
        
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
                
    def DoBehaviours(self):
        if self.m_Behavior == AVATAR_WALKING:
            self.MoveToDestination()
            

    def MoveToDestination( self ):
        pass
    