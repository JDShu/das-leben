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
from numpy import *
from ogl_va import *
from vector_3d import Vector3d

def MTL( path, filename ):
    contents = {}
    mtl = None
    for line in open( os.path.join( path, filename ), "r" ):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError, "mtl file doesn't start with newmtl stmt"
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]
            surf = pygame.image.load( os.path.join( path, mtl['map_Kd'] ))
            image = pygame.image.tostring(surf, 'RGBA', 1)
            ix, iy = surf.get_rect().size
            texid = mtl['texture_Kd'] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                            GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                            GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                         GL_UNSIGNED_BYTE, image)
        else:
            mtl[values[0]] = array( map(float, values[1:]), dtype=float32 )
    return contents

class OBJ( Vector3d ):
    def __init__(self, filename, swapyz=False, outline=False):
        """Loads a Wavefront OBJ file. """
        self.filename = filename
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.mtl = None
        self.scale = 1.0
        material = None
        path = os.path.split(filename)[0]
        use_texture = False
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = array( map(float, values[1:4]), dtype=float32 )
                if swapyz:
                    v = array( [ v[0], v[2], v[1] ], dtype=float32 )
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = array( map(float, values[1:4]), dtype=float32 )
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append( array( map(float, values[1:3]), dtype=float32 ) )
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = MTL( path, values[1]  )
                for name in self.mtl:
                    if 'texture_Kd' in self.mtl[ name ]:
                        use_texture = True
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    vert = int(w[0])
                    if vert < 0:
                        # refers to -ve indexed verts defined up to this
                        # point
                        vert += len(self.vertices)
                    face.append(vert)
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))
            else:
                #print 'UNHANDLED', values
                continue
    
        self.textureID = 0
        va_vertexes = []; vadd = va_vertexes.append
        va_normals = []; nadd = va_normals.append
        va_texcoords = []; tadd = va_texcoords.append
        va_colours = []; cadd = va_colours.append
        
        for face in self.faces:
            vertices, normals, texture_coords, material = face
    
            if material:
                mtl = self.mtl[material]
                if 'texture_Kd' in mtl:
                    # use diffuse texmap
                    self.textureID = mtl['texture_Kd']
                else:
                    # just use diffuse colour
                    if len( mtl[ 'Kd' ] ):
                        cadd( mtl['Kd'] )
                    else:
                        cadd( array( [1.0,1.0,1.0], dtype=float32) )
            else:
                cadd( array( [1.0,1.0,1.0], dtype=float32) )
    
            
            for i in range(0, len(vertices)):
                if normals[i]:
                    nadd( self.normals[normals[i] - 1] )
                if texture_coords[i]:
                    tadd( self.texcoords[texture_coords[i] - 1] )
                vadd( self.vertices[vertices[i] - 1] )
        
        if va_colours == []: va_colours = None
        
        self.va = VA( va_vertexes, va_normals, None, va_texcoords, va_colours, False )

    def __repr__(self):
        x, y, z = self.va.GetDimensions()
        return '<OBJ %r> %s, %s, %s' % ( self.filename, x, y, z )
    
    def SetScale( self, a_Scale ):
        self.scale = a_Scale
        
    def GetScale( self ):
        return self.scale
    
    def draw( self ):
        glPushMatrix()
        glScale( self.scale, self.scale, self.scale )
        
        if self.textureID:
            glEnable( GL_TEXTURE_2D )
            glBindTexture( GL_TEXTURE_2D, self.textureID )
            
        self.va.Draw()
        
        if self.textureID:
            glDisable( GL_TEXTURE_2D )
        
        
        glPopMatrix() 
