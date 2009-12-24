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

class OBJModel:
	triangles = []
	normals = []
	listname = 0
	def __init__(self,filepath):
		self.scale = 1.0
		self.loadObj(filepath)
		self.makeNormals()
		self.createList()
		
		
	def createList(self):
		self.listname = glGenLists(1)
		glNewList(self.listname,GL_COMPILE)
		self.rawDraw()
		glEndList()
	
	def loadObj(self,filepath):
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
		glScale( self.scale, self.scale, self.scale )
		glCallList(self.listname)
		
	def SetScale( self, scale ):
		self.scale = scale / 100.0
	
	def rawDraw(self):
		
		glBegin(GL_TRIANGLES)
		i = 0
		for triangle in self.triangles:
			glNormal3f(self.normals[i][0],self.normals[i][1],self.normals[i][2])
			glVertex3f(triangle[0][0],triangle[0][1],triangle[0][2])
			glVertex3f(triangle[1][0],triangle[1][1],triangle[1][2])
			glVertex3f(triangle[2][0],triangle[2][1],triangle[2][2])
			i+=1
		glEnd()