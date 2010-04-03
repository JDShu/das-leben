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

class AssetManager:
    '''
    A asset manager class for keeping collections of game objects
    '''
    def __init__( self ):
        '''
        Create and instance of AssetManager
        '''
        self.assets = {}
        
    def AddObject( self, a_Name, a_Object3d ):
        '''
        Add a Object3d to the managers dict
        @param a_Name String : the unique name of this object in the asset collection
        @param a_Object3d Object3d : an instance of a Object3d to be added
        '''
        if a_Name not in self.assets.keys():
            self.assets[ a_Name ] = a_Object3d
        else:
            raise Exception, "The name %s is already assigned to an object in this collection" % a_Name
        
    def GetObject( self, a_Name ):
        '''
        Return a Object3d referrenced by name
        @param a_Name String : the name of this object in the collection
        @return Object3d instance
        '''
        if a_Name in self.assets.keys():
            return self.assets[ a_Name ]
        else:
            raise Exception, "The name %s is not in this collection" % a_Name
        
        
    