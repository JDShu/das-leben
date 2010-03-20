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

import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import random

try:
   from OpenGL.GL.ARB.vertex_buffer_object import *
except: 
   print "You need PyOpenGL >= 3.0 to run this program, your current version is %s" % (OpenGL.__version__)
   sys.exit(1)
   
from numpy import *
import sys
import pygame
from pygame.locals import *
from vector_3d import *
from angle import *
from md2 import *
from wavefront import *
from OGLExt import *



OBJECT_3D_SPHERE = 1
OBJECT_3D_BOX = 2
OBJECT_3D_WALL = 3
OBJECT_3D_MESH = 4
OBJECT_3D_ANIMATED_MESH = 5

OBJECT_3D_DRAW_SOLID = 1
OBJECT_3D_DRAW_WIREFRAME = 2
OBJECT_3D_DRAW_HIGHLIGHTED = 3

class Object3d( Vector3d ):
   """A 3d object"""   
   def __init__(self, filename=None, texture=None, scale=100.0, object_type=2, a_Colour=[1.0,1.0,1.0]):
      Vector3d.__init__(self)
      
      self.m_ObjectType = object_type
      self.m_Colour = a_Colour

      if filename == None:
         if object_type == OBJECT_3D_BOX or object_type == OBJECT_3D_SPHERE:
            self.sphere = gluNewQuadric()
            self._model = None
            self.m_Scale = scale / 100.0
            
         elif object_type == OBJECT_3D_WALL:
            self.wall = Wall()
            self._model = None
            self.m_Scale = scale / 100.0
            
      elif self.GetExtensionType( filename ) == "MD2":
         self._model = MD2Model()
         self.m_ObjectType = OBJECT_3D_ANIMATED_MESH
         self._model.SetScale( scale )
         self._model.load( filename, texture, True )
         
      elif self.GetExtensionType( filename ) == "OBJ":
         self._model = OBJ( filename )
         self.m_ObjectType = OBJECT_3D_MESH
         self._model.SetScale( scale )
         
         
      self.m_XRot = Angle()
      self.m_YRot = Angle()
      self.m_ZRot = Angle()
      
      self.m_GLName = random.randint( 1, 1000 )
      
      self.drawmode = OBJECT_3D_DRAW_SOLID
      
   def Clone( self ):
      cloned_object3d = Object3d()
      cloned_object3d.m_Colour = self.m_Colour
      cloned_object3d.m_ObjectType = self.m_ObjectType
      cloned_object3d.SetPosition( self.GetX(), self.GetY(), self.GetZ() )
      cloned_object3d._model = self._model.Clone()
      
      return cloned_object3d
      
   def GetExtensionType( self, filename ):
      return filename.split(".")[1].upper()
      
   def SetScale( self, scale ):
      if self._model:
         self._model.SetScale( scale )
      
   def Animate(self, ticks=0):
      if self.m_ObjectType == OBJECT_3D_ANIMATED_MESH:
         self._model.Animate( True, ticks )
      
   def SetAnimation( self, animation=0 ):
      if self.m_ObjectType == OBJECT_3D_ANIMATED_MESH:
         self._model.SetAnimation( animation )
       
   def SetDrawMode( self, a_DrawMode ):
      self.drawmode = a_DrawMode
      
   def Draw(self):
      glPushMatrix()
      if self.drawmode == OBJECT_3D_DRAW_WIREFRAME:
         glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
      glTranslatef( self.GetX(), self.GetY(), self.GetZ() )
      glRotatef( self.m_XRot.GetAngle() , 1.0, 0, 0 )
      glRotatef( self.m_YRot.GetAngle() , 0, 1.0, 0 )
      glRotatef( self.m_ZRot.GetAngle() , 0, 0, 1.0 )
      glColor3f( self.m_Colour[0],self.m_Colour[1], self.m_Colour[2] )      
            
      if self._model:
         self._model.draw()
         
      else:
         if self.m_ObjectType == OBJECT_3D_SPHERE:
            gluSphere(self.sphere, 1.0 * self.m_Scale, 100, 100)
         elif self.m_ObjectType == OBJECT_3D_BOX:
            glutSolidCube(1.0 * self.m_Scale)  
         elif self.m_ObjectType == OBJECT_3D_WALL:
            self.wall.render(self.m_Scale)  
            
      glPopMatrix()  
   
   def GetGLName( self ):
      return self.m_GLName
      
class Wall:
   def __init__(self, useVBO=True):
      self.num_faces = 6
           
      self.m_UseVBO = useVBO
      
      self.vertices = array([ [-2.0, 0.0, 0.2],
                        [2.0, 0.0, 0.2],
                        [2.0, 5.0, 0.2],
                        [-2.0, 5.0, 0.2],
                        [-2.0, 0.0, 0.0],
                        [2.0, 0.0, 0.0],
                        [2.0, 5.0, 0.0],
                        [-2.0, 5.0, 0.0] ], dtype=float32)
          
      self.normals = array([ [0.0, 0.0, +1.0],  # front
                       [0.0, 0.0, -1.0],  # back
                       [+1.0, 0.0, 0.0],  # right
                       [-1.0, 0.0, 0.0],  # left 
                       [0.0, +1.0, 0.0],  # top
                       [0.0, -1.0, 0.0] ], dtype=float32) # bottom
      
      self.vertex_indices = array([ [0, 1, 2, 3],  # front
                              [4, 5, 6, 7],  # back
                              [1, 5, 6, 2],  # right
                              [0, 4, 7, 3],  # left
                              [3, 2, 6, 7],  # top
                              [0, 1, 5, 4] ], dtype=int32) # bottom  
      
      if self.m_UseVBO:  
         l_Verts = zeros( ( ( self.num_faces * 4 ), 3 ), dtype=float32 )
         l_Normals = zeros( ( ( self.num_faces * 4 ), 3 ), dtype=float32 )
         for face_no in xrange(self.num_faces):
                                   
            v1, v2, v3, v4 = self.vertex_indices[face_no]
            
            l_Normals[ ( face_no * 4 ) + 0 ] = self.normals[face_no]
            l_Normals[ ( face_no * 4 ) + 1 ] = self.normals[face_no]
            l_Normals[ ( face_no * 4 ) + 2 ] = self.normals[face_no]
            l_Normals[ ( face_no * 4 ) + 3 ] = self.normals[face_no]
            
            l_Verts[ ( face_no * 4 ) + 0 ] = self.vertices[v1]
            l_Verts[ ( face_no * 4 ) + 1 ] = self.vertices[v2]
            l_Verts[ ( face_no * 4 ) + 2 ] = self.vertices[v3]
            l_Verts[ ( face_no * 4 ) + 3 ] = self.vertices[v4]
            
         self.m_VBOVertices = glGenBuffersARB( 1 )      
         glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.m_VBOVertices );
         glBufferDataARB( GL_ARRAY_BUFFER_ARB, l_Verts, GL_STATIC_DRAW_ARB );
         
         self.m_VBONormals = glGenBuffersARB( 1 )
         glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.m_VBONormals );
         glBufferDataARB( GL_ARRAY_BUFFER_ARB, l_Normals, GL_STATIC_DRAW_ARB );
         
   
   def render(self, scale):                
      glColor3f( 1.0, 1.0, 1.0 )
      glDisable( GL_TEXTURE_2D )
      # Draw all 6 faces of the cube
      if not self.m_UseVBO:
         glBegin(GL_QUADS)
         
         for face_no in xrange(self.num_faces):
                         
            glNormal3dv( self.normals[face_no] )
            
            v1, v2, v3, v4 = self.vertex_indices[face_no]
            
            x, y, z = self.vertices[v1]
            glVertex3f( x * scale, y * scale, z * scale)
            x, y, z = self.vertices[v2]
            glVertex3f( x * scale, y * scale, z * scale)
            x, y, z = self.vertices[v3]
            glVertex3f( x * scale, y * scale, z * scale)
            x, y, z = self.vertices[v4]
            glVertex3f( x * scale, y * scale, z * scale)
        
         glEnd()
      else:
         glScalef( scale, scale, scale )
         glEnableClientState( GL_VERTEX_ARRAY )
         glEnableClientState( GL_NORMAL_ARRAY )
                  
         glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.m_VBOVertices )
         glVertexPointer( 3, GL_FLOAT, 0, None )
         glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.m_VBONormals )
         glNormalPointer( GL_FLOAT, 0, None )
         
         glDrawArrays( GL_QUADS, 0, 24 )
      
         glDisableClientState( GL_VERTEX_ARRAY )
         glDisableClientState( GL_NORMAL_ARRAY )
         
      def __del__(self):
         glDeleteBuffers( 1, GL.GLuint( self.m_VBOVertices ) )
         glDeleteBuffers( 1, GL.GLuint( self.m_VBONormals ) )
         
         
class Platform( Wall ):
   def __init__( self, useVBO=True):
      self.num_faces = 6
           
      self.m_UseVBO = useVBO
      
      self.vertices = array([ [-2.0, 0.0, 0.5],
                              [2.0, 0.0, 0.5],
                              [2.0, 5.0, 0.5],
                              [-2.0, 5.0, 0.5],
                              [-2.0, 0.0, 0.0],
                              [2.0, 0.0, 0.0],
                              [2.0, 5.0, 0.0],
                              [-2.0, 5.0, 0.0] ], dtype=float32)
          
      self.normals = array([ [0.0, 0.0, +1.0],  # front
                             [0.0, 0.0, -1.0],  # back
                             [+1.0, 0.0, 0.0],  # right
                             [-1.0, 0.0, 0.0],  # left 
                             [0.0, +1.0, 0.0],  # top
                             [0.0, -1.0, 0.0] ], dtype=float32) # bottom
      
      self.vertex_indices = array([ [0, 1, 2, 3],  # front
                                    [4, 5, 6, 7],  # back
                                    [1, 5, 6, 2],  # right
                                    [0, 4, 7, 3],  # left
                                    [3, 2, 6, 7],  # top
                                    [0, 1, 5, 4] ], dtype=int32) # bottom  
      
      if self.m_UseVBO:  
         l_Verts = zeros( ( ( self.num_faces * 4 ), 3 ), dtype=float32 )
         l_Normals = zeros( ( ( self.num_faces * 4 ), 3 ), dtype=float32 )
         for face_no in xrange(self.num_faces):
                                   
            v1, v2, v3, v4 = self.vertex_indices[face_no]
            
            l_Normals[ ( face_no * 4 ) + 0 ] = self.normals[face_no]
            l_Normals[ ( face_no * 4 ) + 1 ] = self.normals[face_no]
            l_Normals[ ( face_no * 4 ) + 2 ] = self.normals[face_no]
            l_Normals[ ( face_no * 4 ) + 3 ] = self.normals[face_no]
            
            l_Verts[ ( face_no * 4 ) + 0 ] = self.vertices[v1]
            l_Verts[ ( face_no * 4 ) + 1 ] = self.vertices[v2]
            l_Verts[ ( face_no * 4 ) + 2 ] = self.vertices[v3]
            l_Verts[ ( face_no * 4 ) + 3 ] = self.vertices[v4]
            
         self.m_VBOVertices = glGenBuffersARB( 1 )      
         glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.m_VBOVertices )
         glBufferDataARB( GL_ARRAY_BUFFER_ARB, l_Verts, GL_STATIC_DRAW_ARB )
         
         self.m_VBONormals = glGenBuffersARB( 1 )
         glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.m_VBONormals )
         glBufferDataARB( GL_ARRAY_BUFFER_ARB, l_Normals, GL_STATIC_DRAW_ARB )
         
         
class ObjectMultiplier:
   def __init__( self, a_Multiple, a_Direction, a_Object ):
      l_Direction = Vector3d()
      l_Direction = a_Direction
      
      va_vertexes = a_Object._model.va.vertexes
      vertexes = zeros( [ len( va_vertexes ) * a_Multiple, 3 ], dtype=float32 )
      
      if hasattr( a_Object._model.va, "normals" ):
         va_normals = a_Object._model.va.normals
         
         normals = zeros( [ len( va_normals ) * a_Multiple, 3 ], dtype=float32 )
      if hasattr( a_Object._model.va, "texCoords" ):
         va_texCoords = a_Object._model.va.texCoords
         texcoords = zeros( [ len( va_texCoords ) * a_Multiple, 2 ], dtype=float32 )
         
      if hasattr( a_Object._model.va, "coloursCoords" ):
         va_coloursCoords = a_Object._model.va.coloursCoords
         colours = zeros( [ len( va_coloursCoords ) * a_Multiple, 3 ], dtype=float32 )
      
      size = len( va_vertexes )
      
      for i in xrange( a_Multiple ):
         for j, values in enumerate( va_vertexes ):
            vertexes[ ( i * size ) + j ][ 0 ] = values[ 0 ] + ( i * l_Direction.GetX() )
            vertexes[ ( i * size ) + j ][ 1 ] = values[ 1 ] + ( i * l_Direction.GetY() )
            vertexes[ ( i * size ) + j ][ 2 ] = values[ 2 ] + ( i * l_Direction.GetZ() )
            
            if hasattr( a_Object._model.va, "normals" ):
               normals[ ( i * size ) + j ] = va_normals[ j ]
            if hasattr( a_Object._model.va, "texCoords" ):
               texcoords[ ( i * size ) + j ] = va_texCoords[ j ]
            if hasattr( a_Object._model.va, "coloursCoords" ):
               colours[ ( i * size ) + j ] = va_coloursCoords[ i ]
            
      a_Object._model.va.vertexes = vertexes
      if hasattr( a_Object._model.va, "normals" ):
         a_Object._model.va.normals = normals
      if hasattr( a_Object._model.va, "texCoords" ):
         a_Object._model.va.texCoords = texcoords
      if hasattr( a_Object._model.va, "coloursCoords" ):
         a_Object._model.va.coloursCoords = colours
      
      a_Object._model.va.vertxCount = len( vertexes )