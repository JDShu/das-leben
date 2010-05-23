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
from struct import *
from numpy import array, zeros

# max values
MAX_VERTICES  =  65534
MAX_TRIANGLES =  65534
MAX_GROUPS    =  255
MAX_MATERIALS =  128
MAX_JOINTS    =  128


# flags
SELECTED   = 1
HIDDEN     = 2
SELECTED2  = 4
DIRTY      = 8


class MS3DHeader:
    def __init__( self ):
        self.ID = "MS3D000000"
        self.version = 3

class MS3DVertex:
    def __init__( self ):
        self.flags = None
        self.vertex = array( [ 0.0, 0.0, 0.0 ], "f" )
        self.boneID = 0
        self.refCount = 0

class MS3DTriangle:
    def __init__( self ):
        self.flags = None
        self.vertexIndices = [ 0, 0, 0 ]
        self.vertexNormals = array( ( 3, 3 ), "f" )
        self.s = array( [ 0.0, 0.0, 0.0 ], "f" )
        self.t = array( [ 0.0, 0.0, 0.0 ], "f" )
        self.smoothingGroup = 0
        self.groupIndex = 0


class MS3DMaterial:
    def __init__( self ):
        self.name = ""
        self.ambient = array( [ 0.0, 0.0, 0.0, 0.0 ], "f" )
        self.diffuse  = array( [ 0.0, 0.0, 0.0, 0.0 ], "f" )
        self.specular = array( [ 0.0, 0.0, 0.0, 0.0 ], "f" )
        self.emissive = array( [ 0.0, 0.0, 0.0, 0.0 ], "f" )
        self.shininess = 0.0
        self.transparency = 1.0
        self.mode = 0
        self.texture = ""
        self.alphamap = ""



class MS3DJoint:
    def __init__( self ):
        self.flags = None
        self.name = ""
        self.parentName = ""
        self.rotation = array( [ 0.0, 0.0, 0.0 ], "f" )
        self.translation  = array( [ 0.0, 0.0, 0.0 ], "f" )
        self.numRotationKeyframes = 0
        self.numTranslationKeyframes = 0



class MS3DKeyframe:
    def __init__( self ):
        self.time = 0.0
        self.parameter = array( [ 0.0, 0.0, 0.0 ], "f" )


class MS3dModel:
    def __init__( self, a_Filename ):
        f = open( a_Filename, 'rb' )
        fileData = f.read()
        f.close()

        offset = 0
        self.header = MS3DHeader()
        
        self.header.ID = ( unpack( '10B', fileData[ offset:10 ] ) )[0]
        offset += 10
        self.header.version = ( unpack( 'i', fileData[ offset:offset + 4 ] ) )[0]
        offset += 4
        if not self.header.ID == "MS3D000000":
            print "Not a valid Milkshape model\n"
            return False
        
        if self.header.version < 3 or self.header.version > 4:
            print "Only version 3 Milkshape models are supported\n"
            return False

        # ============================ VERTEXES ============================================
        self.vertexCount = ( unpack( 'i', fileData[ offset:offset + 2 ] ) )[0]
        offset += 2
        self.vertexes = []; vadd = self.vertexes.append        
        for i in xrange( self.vertexCount ):
            v = MS3DVertex()
            
            v.flags = ( unpack( 'b', fileData[ offset:offset + 1 ] ) )[0]
            offset += 1
            
            for j in xrange( 3 ):
                v.vertex[ j ] = ( unpack( 'f', fileData[ offset:offset + 4 ] ) )[0]
                offset += 4
                
            v.boneID = ( unpack( 'i', fileData[ offset:offset + 1 ] ) )[0]
            offset += 1
            
            v.refCount = ( unpack( 'i', fileData[ offset:offset + 1 ] ) )[0]
            offset += 1
            
            vadd( v )
            
        # ============================== TRIANGLES =========================================    
        self.triangleCount = ( unpack( 'i', fileData[ offset:offset + 2 ] ) )[0]
        offset += 2
        self.triangles = []; tadd = self.triangles.append        
        for i in xrange( self.triangleCount ):
            t = MS3DTriangle()
            
            t.flags = ( unpack( 'i', fileData[ offset:offset + 2 ] ) )[0]
            offset += 2
            
            for j in xrange( 3 ):
                t.vertexIndices[ j ] = ( unpack( 'i', fileData[ offset:offset + 2 ] ) )[0]
                offset += 2
                
            for j in xrange( 3 ):
                for k in xrange( 3 ):
                    t.vertexNormals[ j ][ k ] = ( unpack( 'f', fileData[ offset:offset + 4 ] ) )[0]
                    offset += 4
                    
            for j in xrange( 3 ):
                t.s[ j ] = ( unpack( 'f', fileData[ offset:offset + 4 ] ) )[0]
                offset += 4
                
            for j in xrange( 3 ):
                t.t[ j ] = ( unpack( 'f', fileData[ offset:offset + 4 ] ) )[0]
                offset += 4 
                
            t.smoothingGroup = ( unpack( 'i', fileData[ offset:offset + 1 ] ) )[0]
            offset += 1
            
            t.groupIndex = ( unpack( 'i', fileData[ offset:offset + 1 ] ) )[0]
            offset += 1
            
            tadd( t )
            
        # ================================ Materials ======================================
        self.materialCount = ( unpack( 'i', fileData[ offset:offset + 2 ] ) )[0]
        offset += 2
        self.materials = []; madd = self.materials.append 
        for i in xrange( self.materialCount ):
            m = MS3DMaterial()
            