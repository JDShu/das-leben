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

try:
    from OpenGL.GL.ARB.vertex_buffer_object import *
except: 
    print "You need PyOpenGL >= 3.0 to run this program, your current version is %s" % (OpenGL.__version__)
    sys.exit(1)

from numpy import *
import pygame
from pygame.locals import *
from struct import *
from math import sqrt

# ID value for MD2 model files
MD2_ID = 844121161

# The states available for MD2 models
IDLE1 = 0
RUN = 1
SHOT_STAND = 2
SHOT_SHOULDER = 3
JUMP = 4
IDLE2 = 5
SHOT_FALLDOWN = 6
IDLE3 = 7
IDLE4 = 8
CROUCH = 9
CROUCH_CRAWL = 10
CROUCH_IDLE = 11
CROUCH_DEATH = 12
DEATH_FALL_BACK = 13
DEATH_FALL_FORWARD = 14
DEATH_FALL_BACK_SLOW = 15

# Frame ranges for the states
IDLE1_START = 0
IDLE1_END = 38
RUN_START = 40
RUN_END = 44
SHOT_STAND_START = 47
SHOT_STAND_END = 60
SHOT_SHOULDER_START = 61
SHOT_SHOULDER_END = 64
JUMP_START = 65
JUMP_END = 73
IDLE2_START = 74
IDLE2_END = 95
SHOT_FALLDOWN_START = 96
SHOT_FALLDOWN_END = 112
IDLE3_START = 113
IDLE3_END = 122
IDLE4_START = 123
IDLE4_END = 135
CROUCH_START = 136
CROUCH_END = 154
CROUCH_CRAWL_START = 155
CROUCH_CRAWL_END = 161
CROUCH_IDLE_START = 162
CROUCH_IDLE_END = 169
CROUCH_DEATH_START = 170
CROUCH_DEATH_END = 177
DEATH_FALL_BACK_START = 178
DEATH_FALL_BACK_END = 185
DEATH_FALL_FORWARD_START = 186
DEATH_FALL_FORWARD_END = 190
DEATH_FALL_BACK_SLOW_START = 191
DEATH_FALL_BACK_SLOW_END = 198


# ---------------------------------------------------------------------------

class MD2Vertex:
    """ Vertex data """
    def __init__(self):
        self.vertex = array([0.0, 0.0, 0.0], dtype=float32)
        self.lightNormal = 0

class MD2Animation:
    def __init__(self, id, start, end, fps=12):
        self._id = id
        self._start = start
        self._end = end
        self._fps = 1000 / fps

    def GetStart(self):
        return self._start

    def GetEnd(self):
        return self._end

    def GetFps(self):
        return self._fps

class MD2Frame:
    """ Frame data """
    def __init__(self):
        self.scale = array([0.0, 0.0, 0.0], dtype=float32)
        self.translate = array([0.0, 0.0, 0.0], dtype=float32)
        self.name = ''
        self.vertices  = []

class MD2Face:
    def __init__(self):
        self.p1 = 0
        self.p2 = 0
        self.p3 = 0
        self.uv1 = 0
        self.uv2 = 0
        self.uv3 = 0
        self.Normal = None

class MD2Mesh:
    """ Mesh data """
    def __init__(self):
        self.pos = array([0.0, 0.0, 0.0], dtype=float32)
        self.u = 0.0
        self.v = 0.0


class MD2Header:
    """ Information for an MD2 file header """
    def __init__(self):
        self.id = 0
        self.version = 0
        self.skinWidth = 0
        self.skinHeight = 0
        self.frameSize = 0
        self.numSkins = 0
        self.numVerts = 0
        self.numTexCoords = 0
        self.numTriangles = 0
        self.numGLCmds = 0
        self.numFrames = 0
        self.offsetSkins = 0
        self.offsetTexCoords = 0
        self.offsetTriangles = 0
        self.offsetFrames = 0
        self.offsetGLCmds = 0
        self.offsetEnd = 0

class MD2TexCoord:
    def __init__(self):
        self.u = 0.0
        self.v = 0.0
        

class MD2Model(object):
    """ Data for an MD2 model """
    def __init__(self):
        object.__init__(self)

        self._fileName = None
        self._numFrames = 0
        self._frameSize = 0
        self._frames = []
        self._vertList = []
        self._numGLCmds = 0
        self._glCmds = []
        self._numTriangles = 0
        self.m_SkinWidth = 0
        self.m_SkinHeight = 0
        self.m_VBO = False
        self.m_VBOFrames = []
        self.m_VBOFrameNormals = []
        self.m_VBOFrameTextureCoords = None
        self.m_VBOFrameVertsNum = []
        self.m_TexCoords = []

        msh_add = self._vertList.append
        for i in xrange(120):
            msh_add(MD2Mesh())

        self._lists = 0
        self._texture = None
        self._currentAnimation = IDLE1
        self._currentFrame = IDLE1_START
        self._currentTicks = 0
        self._Animations = []
        self._Animations.append( MD2Animation( IDLE1, IDLE1_START, IDLE1_END, 6 ) )
        self._Animations.append( MD2Animation( RUN, RUN_START, RUN_END, 6 ) )

        self._scale = 1.0

    def load(self, fileName, texture=None, VBO=False):
        """ Load the model data """
        self.m_VBO = VBO
        f = open(fileName, 'rb')
        fileData = f.read()
        f.close()


        header = MD2Header()

        # Read in the header information
        header.id = (unpack('i', fileData[0:4]))[0]
        if header.id != MD2_ID:
            return False

        header.version = (unpack('i', fileData[4:8]))[0]
        if header.version != 8:
            return False

        self._fileName = fileName

        self.m_SkinWidth = header.skinWidth = (unpack('i', fileData[8:12]))[0]
        self.m_SkinHeight = header.skinHeight = (unpack('i', fileData[12:16]))[0]
        header.frameSize = (unpack('i', fileData[16:20]))[0]
        header.numSkins = (unpack('i', fileData[20:24]))[0]
        header.numVerts = (unpack('i', fileData[24:28]))[0]
        header.numTexCoords = (unpack('i', fileData[28:32]))[0]
        header.numTriangles = (unpack('i', fileData[32:36]))[0]
        header.numGLCmds = (unpack('i', fileData[36:40]))[0]
        header.numFrames = (unpack('i', fileData[40:44]))[0]
        header.offsetSkins = (unpack('i', fileData[44:48]))[0]
        header.offsetTexCoords = (unpack('i', fileData[48:52]))[0]
        header.offsetTriangles = (unpack('i', fileData[52:56]))[0]
        header.offsetFrames = (unpack('i', fileData[56:60]))[0]
        header.offsetGLCmds = (unpack('i', fileData[60:64]))[0]
        header.offsetEnd = (unpack('i', fileData[64:68]))[0]

        # Read in the frame data
        for i in xrange(header.numFrames):
            frameInfo = fileData[header.offsetFrames + (i * header.frameSize):header.offsetFrames + 
                                 ((i + 1) * header.frameSize)]

            frame = MD2Frame()

            frame.scale[0] = (unpack('f', frameInfo[0:4]))[0]
            frame.scale[1] = (unpack('f', frameInfo[4:8]))[0]
            frame.scale[2] = (unpack('f', frameInfo[8:12]))[0]

            frame.translate[0] = (unpack('f', frameInfo[12:16]))[0]
            frame.translate[1] = (unpack('f', frameInfo[16:20]))[0]
            frame.translate[2] = (unpack('f', frameInfo[20:24]))[0]

            name = unpack('16B', frameInfo[24:40])
            for c in xrange(16):
                frame.name = frame.name + chr(name[c])

            fadd = self._frames.append
            fv_add = frame.vertices.append
            for j in xrange(40, len(frameInfo), 4):
                vertex = MD2Vertex()

                vertex.vertex[0] = (unpack('B', frameInfo[j]))[0]
                vertex.vertex[1] = (unpack('B', frameInfo[j + 1]))[0]
                vertex.vertex[2] = (unpack('B', frameInfo[j + 2]))[0]

                vertex.lightNormal = (unpack('B', frameInfo[j + 3]))[0]

                fv_add(vertex)

            fadd(frame)

        cmdInfo = fileData[header.offsetGLCmds:header.offsetGLCmds + (header.numGLCmds * 4)]

        self.triangles = []; tadd = self.triangles.append

        face_size = calcsize("<3h3h")

        for i in xrange(header.numTriangles):
            TriData = fileData[ header.offsetTriangles + (i * face_size) : header.offsetTriangles + ((i + 1) * face_size) ]
            data = unpack("<3h3h", TriData)
            face = MD2Face()
            face.p1 = data[0]
            face.p2 = data[1]
            face.p3 = data[2]
            face.uv1 = data[3]
            face.uv2 = data[4]
            face.uv3 = data[5]
            tadd( face )

        i = 0

        textureCoord_size = calcsize("<2h")
        
        tc_add = self.m_TexCoords.append
        for i in xrange(header.numTexCoords):
            TextCoordData = fileData[ header.offsetTexCoords + (i * textureCoord_size) : header.offsetTexCoords + ((i + 1) * textureCoord_size) ]
            u, v = unpack( '<2h', TextCoordData )
            tc = MD2TexCoord()
            tc.u = u / float(self.m_SkinWidth)
            tc.v = v / float(self.m_SkinHeight)
            tc_add( tc )

        i = 0
        # Read in the vertex data
        '''glcmd_add = self._glCmds.append
        while i < len(cmdInfo):
            # Number of vertices
            numVerts = (unpack('=l', cmdInfo[i:i + 4]))[0]
            glcmd_add(numVerts)

            i += 4

            if numVerts < 0:
                numVerts = -numVerts

            # Texture coordinates
            for j in xrange(numVerts):
                tu = (unpack('f', cmdInfo[i:i + 4]))[0]
                tv = (unpack('f', cmdInfo[i + 4:i + 8]))[0]

                glcmd_add(tu)
                glcmd_add(tv)

                # Vertex index
                glcmd_add((unpack('=l', cmdInfo[i + 8:i + 12]))[0])

                i += 12'''

        self._numFrames = header.numFrames
        self._numGLCmds = header.numGLCmds
        self._frameSize = header.frameSize
        self._numTriangles = header.numTriangles

        # load the texture
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

        if VBO:
            # create Vertex Buffer Objects instead of display lists
            for i in xrange( self._numFrames ):
                self.compileVBO( i )


        else:
            # Compile the model vertex data into display lists    
            self._lists = glGenLists( self._numFrames )

            for i in xrange( self._numFrames ):
                glNewList( self._lists + i, GL_COMPILE )

                self.compileList( i )
                glEndList()

        return True

    def CalculateNormal(self, v1, v2, v3 ):
        # Calculate vectors
        v1x = v1[0] - v2[0]
        v1y = v1[1] - v2[1]
        v1z = v1[2] - v2[2]

        v2x = v2[0] - v3[0]
        v2y = v2[1] - v3[1]
        v2z = v2[2] - v3[2]

        # Get cross product of vectors

        nx = (v1y * v2z) - (v1z * v2y)
        ny = (v1z * v2x) - (v1x * v2z)
        nz = (v1x * v2y) - (v1y * v2x)

        # Normalise final vector
        lenSqr = float( (nx * nx) + (ny * ny) + (nz * nz) )
        vLen = sqrt( lenSqr )
        Result = zeros(3, dtype=float32)
        Result[0] = float(nx / vLen) * -1.0
        Result[1] = float(ny / vLen) * -1.0
        Result[2] = float(nz / vLen) * -1.0

        return Result

    def compileList(self, frame):
        """ Compile a frame's data into a display list """
        texCoord = [0.0, 0.0]

        glDisable(GL_CULL_FACE)
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glEnable( GL_TEXTURE_2D )

        if self._texture:
            glBindTexture( GL_TEXTURE_2D, self._texture )

        glCmd = 0
        while self._glCmds[glCmd] != 0:
            if self._glCmds[glCmd] > 0:
                numVert = self._glCmds[glCmd]
                glCmd += 1
                type = 0
            else:
                numVert = -self._glCmds[glCmd]
                glCmd += 1
                type = 1

            if numVert < 0:
                numVert = -numVert

            index = 0

            l_Frames = self._frames
            for i in xrange(numVert):
                self._vertList[index].u = self._glCmds[glCmd]
                glCmd += 1
                self._vertList[index].v = self._glCmds[glCmd]
                glCmd += 1

                vertIndex = self._glCmds[glCmd]
                glCmd += 1

                # make the vertex
                self._vertList[index].pos[0] = (l_Frames[frame].vertices[vertIndex].vertex[0] * 
                                                l_Frames[frame].scale[0]) + l_Frames[frame].translate[0] * self._scale
                self._vertList[index].pos[1] = (l_Frames[frame].vertices[vertIndex].vertex[1] * 
                                                l_Frames[frame].scale[1]) + l_Frames[frame].translate[1] * self._scale
                self._vertList[index].pos[2] = (l_Frames[frame].vertices[vertIndex].vertex[2] * 
                                                l_Frames[frame].scale[2]) + l_Frames[frame].translate[2] * self._scale
                index += 1



            if type == 0:
                glBegin(GL_TRIANGLE_STRIP)

                for i in xrange(index):
                    vert = self._vertList[i].pos

                    texCoord[0] = self._vertList[i].u
                    texCoord[1] = self._vertList[i].v

                    glTexCoord2f(texCoord[0], texCoord[1])

                    glVertex3f(vert[0] * self._scale , vert[1] * self._scale, vert[2] * self._scale)

                glEnd()

            else:
                glBegin(GL_TRIANGLE_FAN)
                for i in xrange(index):
                    vert = self._vertList[i].pos

                    texCoord[0] = self._vertList[i].u
                    texCoord[1] = self._vertList[i].v

                    glTexCoord2f(texCoord[0], texCoord[1])

                    glVertex3f(vert[0], vert[1], vert[2])

                glEnd()
        glDisable( GL_TEXTURE_2D )


    def compileVBO(self, frame):
        """ Compile a frame's data into a Vertex buffer object """

        num_verts = 3 * self._numTriangles
        vbof_add = self.m_VBOFrames.append
        vbofn_add = self.m_VBOFrameNormals.append
        vertexes = zeros( ( 3 * self._numTriangles , 3 ), dtype=float32 ) 
        texCoords = zeros( ( 3 * self._numTriangles, 2 ), dtype=float32 ) 
        #texCoords = [( 3 * self._numTriangles, 2 )]
        normals = zeros( ( 3 * self._numTriangles, 3 ), dtype=float32 ) 
        index = 0
        
        l_Frames = self._frames
        scale = l_Frames[ frame ].scale
        translate = l_Frames[ frame ].translate
        l_ObjectScale = self._scale
            
        
        for i in xrange(self._numTriangles):
            face = self.triangles[ i ];
            vertex1 = zeros( 3, dtype=float32 )
            vertex2 = zeros( 3, dtype=float32 )
            vertex3 = zeros( 3, dtype=float32 )
            # vertex 1
            vertex = l_Frames[ frame ].vertices[ face.p1 ].vertex
            
            vertex1[0] = ( vertex[0] * scale[0]) + translate[0] * l_ObjectScale
            vertex1[1] = ( vertex[1] * scale[1]) + translate[1] * l_ObjectScale
            vertex1[2] = ( vertex[2] * scale[2]) + translate[2] * l_ObjectScale

            vertexes[ (i * 3) ][0] = vertex1[0]
            vertexes[ (i * 3) ][1] = vertex1[1]
            vertexes[ (i * 3) ][2] = vertex1[2]
            # vertex 2
            vertex = l_Frames[ frame ].vertices[ face.p2 ].vertex
            
            '''vertex2[0] = ( l_Frames[ frame ].vertices[ face.p2 ].vertex[0] * l_Frames[ frame ].scale[0]) + l_Frames[ frame ].translate[0] * self._scale
            vertex2[1] = ( l_Frames[ frame ].vertices[ face.p2 ].vertex[1] * l_Frames[ frame ].scale[1]) + l_Frames[ frame ].translate[1] * self._scale
            vertex2[2] = ( l_Frames[ frame ].vertices[ face.p2 ].vertex[2] * l_Frames[ frame ].scale[2]) + l_Frames[ frame ].translate[2] * self._scale
            '''
            vertex2[0] = ( vertex[0] * scale[0]) + translate[0] * l_ObjectScale
            vertex2[1] = ( vertex[1] * scale[1]) + translate[1] * l_ObjectScale
            vertex2[2] = ( vertex[2] * scale[2]) + translate[2] * l_ObjectScale
            
            vertexes[ (i * 3) + 1 ][0] = vertex2[0]
            vertexes[ (i * 3) + 1 ][1] = vertex2[1]
            vertexes[ (i * 3) + 1 ][2] = vertex2[2]
            # vertex 3
            vertex = l_Frames[ frame ].vertices[ face.p3 ].vertex
            '''
            vertex3[0] = ( l_Frames[ frame ].vertices[ face.p3 ].vertex[0] * l_Frames[ frame ].scale[0]) + l_Frames[ frame ].translate[0] * self._scale
            vertex3[1] = ( l_Frames[ frame ].vertices[ face.p3 ].vertex[1] * l_Frames[ frame ].scale[1]) + l_Frames[ frame ].translate[1] * self._scale
            vertex3[2] = ( l_Frames[ frame ].vertices[ face.p3 ].vertex[2] * l_Frames[ frame ].scale[2]) + l_Frames[ frame ].translate[2] * self._scale
            '''
            vertex3[0] = ( vertex[0] * scale[0]) + translate[0] * l_ObjectScale
            vertex3[1] = ( vertex[1] * scale[1]) + translate[1] * l_ObjectScale
            vertex3[2] = ( vertex[2] * scale[2]) + translate[2] * l_ObjectScale
            
            vertexes[ (i * 3) + 2 ][0] = vertex3[0]
            vertexes[ (i * 3) + 2 ][1] = vertex3[1]
            vertexes[ (i * 3) + 2 ][2] = vertex3[2]            


            nx, ny, nz = self.CalculateNormal( vertex1, vertex2, vertex3 )

            normal = zeros( 3, dtype=float32 )
            normal[0] = nx
            normal[1] = ny
            normal[2] = nz
            # add a normal for each vertex
            for j in xrange(3):
                normals[ (i * 3) + j ] = normal 
            
            l_TexCoords = self.m_TexCoords
            if not self.m_VBOFrameTextureCoords:
                texCoord1 = zeros( 2, dtype=float32 )
                texCoord2 = zeros( 2, dtype=float32 )
                texCoord3 = zeros( 2, dtype=float32 )

                texCoord1[0] = l_TexCoords[ face.uv1 ].u
                texCoord1[1] = l_TexCoords[ face.uv1 ].v
                texCoord2[0] = l_TexCoords[ face.uv2 ].u
                texCoord2[1] = l_TexCoords[ face.uv2 ].v
                texCoord3[0] = l_TexCoords[ face.uv3 ].u
                texCoord3[1] = l_TexCoords[ face.uv3 ].v

                '''texCoords.append(texCoord1)
                texCoords.append(texCoord2)
                texCoords.append(texCoord3)'''
                texCoords[ (i * 3) ][0] = texCoord1[0] 
                texCoords[ (i * 3) ][1] = texCoord1[1]

                texCoords[ (i * 3) + 1 ][0] = texCoord2[0]
                texCoords[ (i * 3) + 1 ][1] = texCoord2[1]

                texCoords[ (i * 3) + 2 ][0] = texCoord3[0] 
                texCoords[ (i * 3) + 2 ][1] = texCoord3[1]

            index += 3

        vbof_add( glGenBuffersARB( 1 ) )      
        glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.m_VBOFrames[ frame ] );
        glBufferDataARB( GL_ARRAY_BUFFER_ARB, vertexes, GL_STATIC_DRAW_ARB );

        vbofn_add( glGenBuffersARB( 1 ) )
        glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.m_VBOFrameNormals[ frame ] );
        glBufferDataARB( GL_ARRAY_BUFFER_ARB, normals, GL_STATIC_DRAW_ARB );

        if not self.m_VBOFrameTextureCoords:
            self.m_VBOFrameTextureCoords = glGenBuffersARB( 1 )
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.m_VBOFrameTextureCoords );
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, texCoords, GL_STATIC_DRAW_ARB );
            # print texCoords
        self.m_VBOFrameVertsNum.append( index )

    # Draw the current frame
    def draw(self):
        if self.m_VBO:
            glEnable(GL_DEPTH_TEST)
            glEnable( GL_TEXTURE_2D )

            if self._texture:
                glBindTexture( GL_TEXTURE_2D, self._texture )
            glScale( self._scale, self._scale, self._scale )
            glEnableClientState( GL_VERTEX_ARRAY )
            glEnableClientState( GL_NORMAL_ARRAY )
            glEnableClientState( GL_TEXTURE_COORD_ARRAY )

            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.m_VBOFrames[ self._currentFrame - 1] )
            glVertexPointer( 3, GL_FLOAT, 0, None )

            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.m_VBOFrameNormals[ self._currentFrame ] )
            glNormalPointer( GL_FLOAT, 0, None )

            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.m_VBOFrameTextureCoords )
            glTexCoordPointer( 2, GL_FLOAT, 0, None )

            glDrawArrays( GL_TRIANGLES, 0, self.m_VBOFrameVertsNum[ self._currentFrame ] )

            glDisableClientState( GL_VERTEX_ARRAY )
            glDisableClientState( GL_NORMAL_ARRAY )
            glDisableClientState( GL_TEXTURE_COORD_ARRAY )
            glDisable( GL_TEXTURE_2D )
        else:
            glCallList(self._lists + self._currentFrame) 

    def SetAnimation(self, animation):
        self._currentAnimation = animation
        self._currentFrame = self._Animations[ self._currentAnimation ].GetStart()

    def Animate(self, forward=True, ticks=0):
        self._currentTicks += ticks
        if self._currentTicks > self._Animations[ self._currentAnimation ].GetFps():
            if forward:
                self._currentFrame += 1
            else:
                self._currentFrame -= 1

            self._currentTicks = 0

        if self._currentFrame < self._Animations[ self._currentAnimation ].GetStart():
            self._currentFrame = self._Animations[ self._currentAnimation ].GetEnd() - 1

        if self._currentFrame >= self._Animations[ self._currentAnimation ].GetEnd():
            self._currentFrame = self._Animations[ self._currentAnimation ].GetStart() - 1

    def SetScale(self, percent):
        self._scale = percent / 100.0



