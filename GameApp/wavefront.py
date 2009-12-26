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

from OpenGL.GL import *
from math3D import *
import pygame

class OBJModel:
	triangles = []
	normals = []
	listname = 0
	def __init__(self,filepath, texture=None, a_Colour=[1.0,1.0,1.0]):
		self.scale = 1.0
		self._texture = None
		self.loadObj(filepath, texture)
		self.makeNormals()
		self.createList(a_Colour)
		
	def createList(self, a_Colour):
		self.listname = glGenLists(1)
		glDisable( GL_TEXTURE_2D )
		glNewList(self.listname,GL_COMPILE)
		self.rawDraw(a_Colour)
		glColor3f( 1.0, 1.0, 1.0 )
		glEndList()
	
	def loadObj(self,filepath, texture=None):
		if texture:
			textureSurface = pygame.image.load(texture)
	    
			textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
	    
			width = textureSurface.get_width()
			height = textureSurface.get_height()
	    
			self._texture = glGenTextures(1)
			glBindTexture(GL_TEXTURE_2D, self._texture)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
		
		modelFile = open(filepath,"r")
		triangles = []
		vertices = []
		for line in modelFile.readlines():
			line = line.strip()
			if len(line)==0 or line.startswith("#"):
				continue
			data = line.split(" ")
			
			if data[0]=="v":
				if data[ 1 ] == "":
					data = [ data[ 0 ], data[ 2 ], data[ 3 ], data[ 4 ] ]
				vertices.append((float(data[1]),float(data[2]),float(data[3])))
			if data[0]=="f":
				vertex1 = vertices[int(data[1].split("/")[0])-1]
				vertex2 = vertices[int(data[2].split("/")[0])-1]
				vertex3 = vertices[int(data[3].split("/")[0])-1]
				triangles.append((vertex1,vertex2,vertex3))
			#if data[0]=='vn':
				#self.normals.append((float(data[1]),float(data[2]),float(data[3])))
		self.triangles = triangles
	
	def makeNormals(self):
		normals = []
		for triangle in self.triangles:
			arm1 = sub3(triangle[1],triangle[0])
			arm2 = sub3(triangle[2],triangle[0])
			normals.append(normalize3(cross3(arm1,arm2)))
		self.normals = normals
	
	def draw(self):
		glPushMatrix()
		glDisable( GL_TEXTURE_2D )
		
		if self._texture:
			glEnable( GL_TEXTURE_2D )
			glBindTexture( GL_TEXTURE_2D, self._texture )
		
		glScale( self.scale, self.scale, self.scale )
		glCallList(self.listname)
		
		if self._texture: glDisable( GL_TEXTURE_2D )
		glPopMatrix()
		
	def SetScale( self, scale ):
		self.scale = scale / 100.0
	
	def rawDraw(self, a_Colour):
		
		glBegin(GL_TRIANGLES)
		i = 0
		for triangle in self.triangles:
			glColor3f( a_Colour[ 0 ], a_Colour[ 1 ], a_Colour[ 2 ] )
			glNormal3f(self.normals[i][0],self.normals[i][1],self.normals[i][2])
			glVertex3f(triangle[0][0],triangle[0][1],triangle[0][2])
			glColor3f( a_Colour[ 0 ], a_Colour[ 1 ], a_Colour[ 2 ] )
			glNormal3f(self.normals[i][0],self.normals[i][1],self.normals[i][2])
			glVertex3f(triangle[1][0],triangle[1][1],triangle[1][2])
			glColor3f( a_Colour[ 0 ], a_Colour[ 1 ], a_Colour[ 2 ] )
			glNormal3f(self.normals[i][0],self.normals[i][1],self.normals[i][2])
			glVertex3f(triangle[2][0],triangle[2][1],triangle[2][2])
			i+=1
		glEnd()
		