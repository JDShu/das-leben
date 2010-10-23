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
import soya


OBJECT_3D_SPHERE = 1
OBJECT_3D_BOX = 2
OBJECT_3D_WALL = 3
OBJECT_3D_MESH = 4
OBJECT_3D_ANIMATED_MESH = 5

OBJECT_3D_DRAW_SOLID = 1
OBJECT_3D_DRAW_WIREFRAME = 2
OBJECT_3D_DRAW_HIGHLIGHTED = 3

class Object3d( soya.Body ):
   """A 3d object"""   
   def __init__(self, a_Scene, a_Model, a_ModelName ):
      model = a_Model
      self.name = a_ModelName
      soya.Body.__init__( self, a_Scene, model )
      
      
      
   def begin_round( self ):
      soya.Body.begin_round( self )
      
   
