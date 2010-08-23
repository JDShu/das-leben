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
import os

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
   def __init__(self, filename=None, texture=None, a_Name=None, scale=100.0, object_type=2, a_Colour=[1.0,1.0,1.0]):
      Vector3d.__init__(self)
      
      self.m_ObjectType = object_type
      self.m_Colour = a_Colour
      self.model_file = ''
      self.texture_file = ''
      self.name = a_Name
      self.extentions = {}

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
         self.model_file = filename
         self.texture_file = texture 
         
      elif self.GetExtensionType( filename ) == "OBJ":
         self._model = OBJ( filename )
         self.m_ObjectType = OBJECT_3D_MESH
         self._model.SetScale( scale )
         self.model_file = filename
         self.texture_file = self._model.texture_path
         
      self.m_XRot = Angle()
      self.m_YRot = Angle()
      self.m_ZRot = Angle()
      
      self.m_GLName = random.randint( 1, 1000 )
      
      self.drawmode = OBJECT_3D_DRAW_SOLID
      
   def Save( self, a_Filename ):
      '''
      Save the object properties
      @param a_Filename String : the location to save the file
      '''
      try:
         if os.path.isfile( a_Filename ): os.remove( a_Filename )
         f = open( a_Filename, "w" )
         lines = []
         lines.append( "%s\n" % str( self.model_file ) )
         lines.append( "%s\n" % str( self.texture_file ) )
         lines.append( "%s\n" % str( self.name ) )
         if len( self.extentions ) > 0:
            lines.append( "[EXTENDED OBJECTS]" )
            for extention in self.extentions:
               lines.append( "EXT:%s, POS:%s, ANGLES:%s %s %s\n" % ( extention[ 0 ], 
                                                                   str( extention[ 1 ].GetPosition() ),
                                                                   str( extention[ 1 ].m_XRot.GetAngle() ),
                                                                   str( extention[ 1 ].m_YRot.GetAngle() ),
                                                                   str( extention[ 1 ].m_ZRot.GetAngle() ) ) )
                                                                   
         f.writelines( lines )
         f.close()
         
      except IOError:
         raise Exception, "Unable to save object file %s : %s" % ( a_Filename, e )
      
   def GetWidth( self ):
      return self._model.va.GetDimensions()[ 0 ] * self._model.GetScale() * 0.25
      
   def GetHeight( self ):
      return self._model.va.GetDimensions()[ 1 ] * self._model.GetScale() * 0.5
   
   def GetDepth( self ):
      return self._model.va.GetDimensions()[ 2 ] * self._model.GetScale() * 0.25
   
   def Clone( self ):
      cloned_object3d = Object3d()
      cloned_object3d.m_Colour = self.m_Colour
      cloned_object3d.m_ObjectType = self.m_ObjectType
      cloned_object3d.SetPosition( self.GetX(), self.GetY(), self.GetZ() )
      cloned_object3d._model = self._model.Clone()
      cloned_object3d.SetScale( self._model.GetScale() )
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
      
   def SetTexture( self, a_TextureID ):
      self._model.textureID = a_TextureID
      
   def Draw(self):
      glPushMatrix()
      glEnable(GL_CULL_FACE)
      glCullFace( GL_BACK )
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
            
      glDisable(GL_CULL_FACE)
      glPopMatrix()  
   
   def GetGLName( self ):
      return self.m_GLName
      
     
         

def MultiplyObject( a_Multiple, a_Direction, a_Object ):
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
      

def ConcatenateObject( a_Direction, a_Object, a_ObjectToAdd ):
   '''
   Concatenate an objects geometry onto another object
   @param a_Direction Vector3d : the direction to add the objects geometry
   @param a_Object Object3d : an object to concatenate the geometry to
   @param a_ObjectToAdd Object3d : the object your concatenating
   '''
   l_Direction = Vector3d()
   l_Direction = a_Direction
   
   va_vertexes = a_Object._model.va.vertexes
   src_vertexes = a_ObjectToAdd._model.va.vertexes
   vertexes = zeros( [ len( va_vertexes ) + len( src_vertexes ), 3 ], dtype=float32 )
   
   if hasattr( a_Object._model.va, "normals" ):
      va_normals = a_Object._model.va.normals
      src_normals = a_ObjectToAdd._model.va.normals
      normals = zeros( [ len( va_normals ) + len( src_normals ), 3 ], dtype=float32 )
      
   if hasattr( a_Object._model.va, "texCoords" ):
      va_texCoords = a_Object._model.va.texCoords
      src_texCoords = a_ObjectToAdd._model.va.texCoords
      texcoords = zeros( [ len( va_texCoords ) + len( src_texCoords ), 2 ], dtype=float32 )
      
   if hasattr( a_Object._model.va, "coloursCoords" ):
      va_coloursCoords = a_Object._model.va.coloursCoords
      src_coloursCoords = a_ObjectToAdd._model.va.coloursCoords
      colours = zeros( [ len( va_coloursCoords ) + len( src_coloursCoords ), 3 ], dtype=float32 )
   
   size = len( va_vertexes )
   
   # first object
   for j, values in enumerate( va_vertexes ):
      vertexes[ j ][ 0 ] = values[ 0 ]
      vertexes[ j ][ 1 ] = values[ 1 ]
      vertexes[ j ][ 2 ] = values[ 2 ]
      
      if hasattr( a_Object._model.va, "normals" ):
         normals[ j ] = va_normals[ j ]
      if hasattr( a_Object._model.va, "texCoords" ):
         texcoords[ j ] = va_texCoords[ j ]
      if hasattr( a_Object._model.va, "coloursCoords" ):
         colours[ j ] = va_coloursCoords[ j ]
    
   # concatenate the next object
   obj_end = len( va_vertexes )
   for j, values in enumerate( src_vertexes ):
      vertexes[ obj_end + j ][ 0 ] = values[ 0 ] + l_Direction.GetX() 
      vertexes[ obj_end + j ][ 1 ] = values[ 1 ] + l_Direction.GetY() 
      vertexes[ obj_end + j ][ 2 ] = values[ 2 ] + l_Direction.GetZ() 
      
      if hasattr( a_Object._model.va, "normals" ):
         normals[ obj_end + j ] = va_normals[ j ]
      if hasattr( a_Object._model.va, "texCoords" ):
         texcoords[ obj_end + j ] = va_texCoords[ j ]
      if hasattr( a_Object._model.va, "coloursCoords" ):
         colours[ obj_end + j ] = va_coloursCoords[ j ]
      
         
   a_Object._model.va.vertexes = vertexes
   if hasattr( a_Object._model.va, "normals" ):
      a_Object._model.va.normals = normals
   if hasattr( a_Object._model.va, "texCoords" ):
      a_Object._model.va.texCoords = texcoords
   if hasattr( a_Object._model.va, "coloursCoords" ):
      a_Object._model.va.coloursCoords = colours
   
   a_Object._model.va.vertxCount = len( vertexes )
   
   a_Object.extentions[ a_ObjectToAdd.name ] = a_ObjectToAdd
   
def TranslateVertexArray( a_Object, a_Direction ):
   va_vertexes = a_Object._model.va.vertexes
   
   for values in va_vertexes:
      values[ 0 ] = values[ 0 ] + a_Direction.GetX() 
      values[ 1 ] = values[ 1 ] + a_Direction.GetY() 
      values[ 2 ] = values[ 2 ] + a_Direction.GetZ() 
      
def ScaleVertexArray( a_Object, a_Scale ):
   va_vertexes = a_Object._model.va.vertexes
   
   for values in va_vertexes:
      values[ 0 ] = values[ 0 ] * a_Scale
      values[ 1 ] = values[ 1 ] * a_Scale
      values[ 2 ] = values[ 2 ] * a_Scale
      

   