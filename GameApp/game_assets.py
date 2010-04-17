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
from os import path

class Manifest:
    '''
    A list of assets and how to load them
    '''
    def __init__( self, a_Filename ):
        '''
        create a Manifest instance
        @param a_Filename String : the location of the manifest file
        '''
        try:
            f = open( a_Filename, "r" )
            
            self.items = f.readlines()
        except IOError, e:
            print "Unable to load %s : %s" % ( a_Filename, e )

    def Save( self, a_Filename ):
        '''
        Save the current Manifest
        @param a_Filename String : the location of the manifest file 
        '''
        try:
            f = open( a_Filename, "w" )
            
            f.writelines( self.items )

        except IOError, e:
            print "Unable to save %s : %s" % ( a_Filename, e )


class AssetManager:
    '''
    A asset manager class for keeping collections of game objects
    '''
    def __init__( self, a_Filename=None, a_DataPath=None ):
        '''
        Create and instance of AssetManager
        '''
        self.assets = []
        self.textures = {}

        self.data_path = a_DataPath

        if a_Filename:
            self.Load( a_Filename )
        
    def Load( self, a_Filename ):
        '''
        Load a asset manifest
        @param a_Filename String : the location of the manifest
        '''
        manifest = Manifest( path.join( self.data_path, a_Filename ) )

        for item in manifest.items:
            if item.startswith( "OBJECT:" ):
                parts = item.split( ":" )
                obj = Object3d( path.join( self.data_path, parts[ 1 ] ) )

                self.AddObject( parts[ 2 ].replace( '\n', '' ) , obj )
            elif item.startswith( "TEXTURE:" ):
                pass

    def AddTexture( self, a_Name, a_TextureID ):
        '''
        Add a texture to the asset manager
        @param a_Name String : the name of this texture
        @param a_TextureID Integer : OpenGL texture ID        
        '''
        if a_Name not in self.textures.keys():
            self.textures[ a_Name ] = a_TextureID
        else:
            raise Exception, "The name %s is already assigned to a texture in this collection" % a_Name
        
        
    def ReplaceTexture( self, a_Name, a_TextureID ):
        '''
        Replace an existing texture with a new ID
        @param a_Name String : the texture to replace
        @param a_TextureID Integer : the OpenGL ID to use
        '''
        self.textures[ a_Name ] = a_TextureID
        
    def GetTexture( self, a_Name ):
        '''
        Return the OpenGL ID of a named texture
        @param a_Name String : the name of the texture in this collection
        @return Integer : the OpenGL ID
        '''
        return self.textures[ a_Name ]
    
    def AddObject( self, a_Name, a_Object3d ):
        '''
        Add a Object3d to the managers dict
        @param a_Name String : the unique name of this object in the asset collection
        @param a_Object3d Object3d : an instance of a Object3d to be added
        '''
        if { a_Name : a_Object3d } not in self.assets:
            self.assets.append( { a_Name : a_Object3d } )
        else:
            raise Exception, "The name %s is already assigned to an object in this collection" % a_Name
        
    def ReplaceObject( self, a_Name, a_Object3d ):
        '''
        Replace an existing object with a new Object3d
        @param a_Name String : the object to replace
        @param a_Object3d Object3d : the Object3d instance to use
        '''
        self.assets[ a_Name ] = a_Object3d
        
    def GetObject( self, a_Name ):
        '''
        Return a Object3d referrenced by name
        @param a_Name String : the name of this object in the collection
        @return Object3d instance
        '''
        for Object in self.assets:
            if a_Name in Object.keys():
                return Object[ a_Name ]
            else:
                raise Exception, "The name %s is not in this collection" % a_Name
        
        
    