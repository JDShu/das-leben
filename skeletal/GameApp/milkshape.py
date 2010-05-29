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
import pygame
import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from struct import *
from numpy import array, zeros, matrix
import os

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


# trims a string by removing ending 0 and everything after it
def CleanString( s ):
     try:
	  return s[ :s.index('\0') ]
     except:
	  return s
	

# Converts ms3d euler angles to a rotation matrix
def EulerToMatrix( a ):
     sy = sin( a[ 2 ] )
     cy = cos( a[ 2 ] )
     sp = sin( a[ 1 ] )
     cp = cos( a[ 1 ] )
     sr = sin( a[ 0 ] )
     cr = cos( a[ 0 ] )
     
     m = "%f %f %f; %f %f %f; %f %f %f" % ( cp*cy, cp*sy, -sp, 
                                            sr*sp*cy+cr*-sy, sr*sp*sy+cr*cy, sr*cp, 
                                            cr*sp*cy+-sr*-sy, cr*sp*sy+-sr*cy, cr*cp )
     return matrix( m )


class MS3dModel:
     def __init__( self, a_Filename ):


          try:
               f = open( a_Filename, 'rb' )
          except IOError:
               return "Failed to open the file!"

          # get the file size
          f.seek(0, os.SEEK_END)
          fileSize = f.tell()
          f.seek(0, os.SEEK_SET)

          self.header = MS3DHeader()

          self.header.ID = f.read( 10 ) 

          self.header.version = unpack( 'i', f.read( 4 ) )[0]

          if not self.header.ID == "MS3D000000":
               print "Not a valid Milkshape model\n"
               return False

          if self.header.version < 3 or self.header.version > 4:
               print "Only version 3 Milkshape models are supported\n"
               return False

          # ============================ VERTEXES ============================================
          self.vertexCount = unpack( 'H', f.read( 2 ) )[0]

          self.vertexes = []; vadd = self.vertexes.append        
          self.boneIDs = []; badd = self.boneIDs.append
          for i in xrange( self.vertexCount ):
               f.read( 1 ) # ignore flags

               vadd( unpack( 'fff', f.read( 3 * 4 ) ) )

               badd( unpack( 'b', f.read( 1 ) )[0] )

               f.read( 1 ) # ignore refCount


          # ============================== TRIANGLES =========================================    
          self.triangleCount = unpack( 'H', f.read( 2 ) )[0]

          self.faces = []; fadd = self.faces.append   
          self.uvs = []; tadd = self.uvs.append
          self.normals = []; nadd = self.normals.append
          for i in xrange( self.triangleCount ):
               f.read( 1 ) # ignore flags

               fadd( unpack( 'HHH', f.read( 3 * 2 ) ) )

               for j in xrange( 3 ):
                    nadd( unpack( 'fff', f.read( 3 * 4 ) ) )

               s = unpack( "fff", f.read( 3 * 4 ) )
               t = unpack( "fff", f.read( 3 * 4 ) )

               tadd( [ s[0], 1-t[0]], [s[1], 1-t[1]], [s[2], 1-t[2] ] )

               if self.faces[-1][2] == 0: # Cant have zero at the third index
                    self.faces[-1] = self.faces[-1][1], self.faces[-1][2], self.faces[-1][0]
                    self.uvs[-1] = self.uvs[-1][1], self.uvs[-1][2], self.uvs[-1][0]

               f.read( 1 ) # ignore smooth group

               f.read( 1 ) # ignore group

          # ================================ Groups =========================================
          # NOTE: in a editor program we might want this data but not in our game
          #       so we're just going to load the data to maintain the file position

          # read number of groups
          numGroups = unpack( "H", f.read( 2 ) )[0]

          # read groups
          for i in xrange(numGroups):
               # ignore flags
               f.read( 1 )

               # ignore name
               f.read( 32 )

               # read the number of triangles in the group
               numGroupTriangles = unpack( "H", f.read( 2 ) )[0]

               # read the group triangles
               if numGroupTriangles > 0:
                    # ignore the group triangles
                    unpack( "%sH" % str( numGroupTriangles ), f.read( 2 * numGroupTriangles ) )

               # read material
               material = unpack( "b", f.read( 1 ) )[0]



          # ================================ Materials ======================================
          # read the number of materials
          numMaterials = unpack( "H", f.read(2) )[ 0 ]

          # read materials
          for i in xrange( numMaterials ):
               # read name
               name = f.read( 32 )

               # read ambient color
               ambient = unpack( "ffff", f.read( 4 * 4 ) )[ 0:3 ]

               # read diffuse color
               diffuse = unpack( "ffff", f.read( 4 * 4 ) )[ 0:3 ]

               # read specular color
               specular = unpack( "ffff", f.read( 4 * 4 ))[ 0:3 ]

               # read emissive color
               emissive = unpack( "ffff", f.read( 4 * 4 ))[ 0:3 ]

               # read shininess
               shininess = unpack( "f", f.read( 4 ) )[ 0 ]

               # read transparency		
               transparency = unpack( "f", f.read( 4 ) )[ 0 ]

               # read mode
               mode = unpack( "B", f.read( 1 ) )[ 0 ]

               # read texturemap
               texturemap = CleanString( f.read( 128 ) )
               if len(texturemap)>0:
                    textureSurface = pygame.image.load(texture)

                    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        
                    width = textureSurface.get_width()
                    height = textureSurface.get_height()
        
                    self.texture = glGenTextures(1)
                    glBindTexture(GL_TEXTURE_2D, self._texture)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
		                 GL_UNSIGNED_BYTE, textureData)

               # read alphamap
               f.read( 128 )  
	       
	  # ================================ Animations ====================================
	  
	  # read animation
	  fps = unpack( "f", f.read( 4 ) )[ 0 ]
	  time = unpack( "f", f.read( 4 ) )[ 0 ]
	  frames = unpack( "i", f.read( 4 ) )[ 0 ]
   
	  # read the number of joints
	  numJoints = unpack( "H", f.read( 2 ) )[ 0 ]
	  
	  
	  
	  