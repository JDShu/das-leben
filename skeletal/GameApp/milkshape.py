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
from numpy import *
import re
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


# returns the next non-empty, non-comment line from the file
def getNextLine(file):
     ready = False
     while ready==False:
          line = file.readline()
          if len(line)==0:
               print "Warning: End of file reached."
               return line
          ready = True
          line = line.strip()
          if len(line)==0 or line.isspace():
               ready = False
          if len(line)>=2 and line[0]=='/' and line[1]=='/':
               ready = False

     return line	



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

# limits
MAX_NUMMESHES = 1000
MAX_NUMVERTS = 100000
MAX_NUMNORMALS = 100000
MAX_NUMTRIS = 100000
MAX_NUMMATS = 16
MAX_NUMBONES = 100
MAX_NUMPOSKEYS = 1000
MAX_NUMROTKEYS = 1000

class MS3dModel:
     def __init__( self, a_Filename ):
          try:
               f = open( a_Filename, "r" )
          except IOError:
               print "Can't open file %s" % a_Filename

          # Read frame info
          try:
               lines = getNextLine( f ).split()
               if len( lines ) != 2 or lines[ 0 ] != "Frames:":
                    raise ValueError
               lines = getNextLine( f ).split()
               if len( lines ) != 2 or lines[ 0 ] != "Frame:":
                    raise ValueError
          except ValueError:
               print "Frame information not invalid!"

          # read the number of meshes
          try:
               lines = getNextLine( f ).split()
               if len( lines )!=2 or lines[ 0 ]!="Meshes:":
                    raise ValueError
               numMeshes = int( lines[ 1 ] )
               if numMeshes < 0 or numMeshes > MAX_NUMMESHES:
                    raise ValueError
          except ValueError:
               print "Number of meshes is invalid!"

          vertexBase = 0
          faceBase = 0
          self.boneIDS = []
          self.coords = []
          self.uvs = []

          for i in xrange( numMeshes ):
               # read name, flags and material
               try:
                    lines = re.findall( r'\".*\"|[^ ]+', getNextLine( f ) )
                    if len( lines ) != 3:
                         raise ValueError
                    material = int( lines[ 2 ] )
               except ValueError:
                    print "Name, flags or material in mesh %s are invalid!" % str( i + 1 )

               # read the number of vertices
               try:
                    numVerts = int( getNextLine( f ) )
                    if numVerts < 0 or numVerts > MAX_NUMVERTS:
                         raise ValueError
               except ValueError:
                    print "Number of vertices in mesh " + str(i+1) + " is invalid!"

               # read vertices
               
               for j in xrange( numVerts ):
                    try:
                         lines = getNextLine( f ).split()
                         if len( lines ) != 7:
                              raise ValueError
                         self.coords.append( [ float( lines[ 1 ] ), float( lines[ 2 ] ), float( lines[ 3 ] ) ] )
                         self.uvs.append( [ float( lines[ 4 ] ), 1.0 - float( lines[ 5 ] ) ] )
                         self.boneIDS.append( int( lines[ 6 ] ) )
                    except ValueError:
                         print "Vertex %d in mesh %d is invalid!" % ( str( j + 1 ), str( i + 1 ) )

               # read number of normals
               try:
                    numNormals = int( getNextLine( f ) )
                    if numNormals < 0 or numNormals > MAX_NUMNORMALS:
                         raise ValueError
               except ValueError:
                    print "Number of normals in mesh %d is invalid!" % str( i + 1 )

               # read normals
               self.normals = []
               for j in xrange( numNormals ):
                    try:
                         lines = getNextLine( f ).split()
                         if len( lines ) != 3:
                              raise ValueError
                         self.normals.append( [ float( lines[ 0 ] ), float( lines[ 1 ] ), float( lines[ 2 ] ) ] )
                    except ValueError:
                         print "Normal %d in mesh %d is invalid!" % ( str( j + 1 ), str( i + 1 ) )

               # read the number of triangles
               try:
                    numTris = int( getNextLine( f ) )
                    if numTris < 0 or numTris > MAX_NUMTRIS:
                         raise ValueError
               except ValueError:
                    print "Number of triangles in mesh %d is invalid!" % str( i + 1 )

               # read triangles
               self.faces = []
               for j in xrange( numTris ):
                    # read the triangle
                    try:
                         lines = getNextLine( f ).split()
                         if len( lines ) != 8:
                              raise ValueError
                         v1 = int( lines[ 1 ] )
                         v2 = int( lines[ 2 ] )
                         v3 = int( lines[ 3 ] )
                         self.faces.append( [ v1 + vertexBase, v2 + vertexBase, v3 + vertexBase ] )
                    except ValueError:
                         print "Triangle %d in mesh %d is invalid!" % ( str( j + 1 ), str( i + 1 ) )

               # increase vertex and face base
               vertexBase = len( self.coords )
               faceBase = len( self.faces )

     
     def CreateVertexArrays( self ):
##          va = zeros( 3 * len( self.faces ) * 3, dtype=float32 )
##          normals = zeros( 3 * len( self.faces ) * 3, dtype=float32 )
##          uvs = zeros( 2 * len( self.faces ) * 3, dtype=float32 )
          
          va = []
          normals = []
          uvs = []
          
          offset = 0
          uv_offset = 0
          
          for face in self.faces:
               
               for index in face:
                    
                    vert = self.coords[ index ]
                    # populate the vertex array
                    va.append( vert )
                    
                    # populate the normals array
                    norm = self.normals[ index ]
                    normals.append( norm )
                    
                    # populate the uv array   
                    uv = self.uvs[ index ]
                    uvs.append( uv )
                    
          return va, normals, uvs
     
     
                    
                    
               