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

from ctypes import *
import sys
 
import pygame
from pygame.locals import *
 
try:
    # For OpenGL-ctypes
    from OpenGL import platform
    gl = platform.OpenGL
except ImportError:
    try:
        # For PyOpenGL
        gl = cdll.LoadLibrary('libGL.so')
    except OSError:
        # Load for Mac
        from ctypes.util import find_library
        # finds the absolute path to the framework
        path = find_library('OpenGL')
        gl = cdll.LoadLibrary(path)
 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
 
glCreateShader = gl.glCreateShader
glShaderSource = gl.glShaderSource
glShaderSource.argtypes = [c_int, c_int, POINTER(c_char_p), POINTER(c_int)]
glCompileShader = gl.glCompileShader
glGetShaderiv = gl.glGetShaderiv
glGetShaderiv.argtypes = [c_int, c_int, POINTER(c_int)]
glGetShaderInfoLog = gl.glGetShaderInfoLog
glGetShaderInfoLog.argtypes = [c_int, c_int, POINTER(c_int), c_char_p]
glDeleteShader = gl.glDeleteShader
glCreateProgram = gl.glCreateProgram
glAttachShader = gl.glAttachShader
glLinkProgram = gl.glLinkProgram
glGetError = gl.glGetError
glUseProgram = gl.glUseProgram
 
GL_FRAGMENT_SHADER = 0x8B30
GL_VERTEX_SHADER = 0x8B31
GL_COMPILE_STATUS = 0x8B81
GL_LINK_STATUS = 0x8B82
GL_INFO_LOG_LENGTH = 0x8B84

'''
NOTE: The following is just a copy of th eshader stuff from pygames 
website but packed up so I can use it the way I want
'''

class oglShader:
    '''basic shader'''
    def __init__( self ):
        '''default cartoon shader'''
        self._program = self.compile_program('''
        varying vec3 pos;
        void main() {
            pos = gl_Vertex.xyz;
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        }''', '''
        varying vec3 pos;
        void main() {
            gl_FragColor.rgb = pos.xyz;
        }''')
        
    def compile_shader( self, source, shader_type ):
        shader = glCreateShader(shader_type)
        source = c_char_p(source)
        length = c_int(-1)
        glShaderSource(shader, 1, byref(source), byref(length))
        glCompileShader(shader)
        
        status = c_int()
        glGetShaderiv(shader, GL_COMPILE_STATUS, byref(status))
        if not status.value:
            glDeleteShader(shader)
            raise ValueError, 'Shader compilation failed'
        return shader
    
    def compile_program( self, vertex_source, fragment_source=None):
        vertex_shader = None
        fragment_shader = None
        program = glCreateProgram()
     
        if vertex_source:
            vertex_shader = self.compile_shader(vertex_source, GL_VERTEX_SHADER)
            glAttachShader(program, vertex_shader)
        if fragment_source:
            fragment_shader = self.compile_shader(fragment_source, GL_FRAGMENT_SHADER)
            glAttachShader(program, fragment_shader)
     
        glLinkProgram(program)
     
        if vertex_shader:
            glDeleteShader(vertex_shader)
        if fragment_shader:
            glDeleteShader(fragment_shader)
     
        return program
        
    def StartShader( self ):
        glUseProgram( self._program )
        
class oglWavyShader( oglShader ):
    def __init__( self ):
        self._program = self.compile_program('''
        uniform float waveTime;
        uniform float waveWidth;
        uniform float waveHeight;
         
        void main(void)
        {
	        vec4 v = vec4(gl_Vertex);
	
	        v.z = sin(waveWidth * v.x + waveTime) * cos(waveWidth * v.y + waveTime) * waveHeight;
	
	        gl_Position = gl_ModelViewProjectionMatrix * v;
        }''', '''
        void main()
        {
	        gl_FragColor[0] = gl_FragCoord[0] / 400.0;
	        gl_FragColor[1] = gl_FragCoord[1] / 400.0;
	        gl_FragColor[2] = 1.0;
        }''')

class oglBumpyShader( oglShader ):
    def __init__( self ):
        self._program = self.compile_program('''
        varying vec3 N;
        varying vec3 L;
        varying vec3 v;
        varying float pattern;             
        
        const vec3 lightPos = vec3(0.0,5.0,5.0); // make this uniform
        
        void main(void)
        {
           v = vec3(gl_ModelViewMatrix * gl_Vertex);
           L = normalize(lightPos - v);
           N = normalize(gl_NormalMatrix * gl_Normal);
        
           pattern=fract(4.0*(gl_Vertex.y+gl_Vertex.x+gl_Vertex.z));
           gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        }''', '''
        varying vec3 N;
        varying vec3 L;
        varying vec3 v;
        varying float pattern;
        
        uniform vec4 color0; // Diffuse Color: 0.8, 0.0, 0.0, 1.0
        uniform vec4 color1; // Ambient Color
        uniform vec4 color2; // Specular Color: 0.8, 0.0, 0.0, 1.0
        uniform vec3 eyePos; // Eye Position
        
        #define shininess 10.0
        
        void main (void)
        {
        vec3 E = normalize(eyePos - v);
        vec3 R = normalize(2.0 * dot(N,L) * N-L); // R = normalize(-reflect(L,N));
        
        float spec = pow(max(dot(R,E),0.0), shininess);
        float spec2= pattern*spec;
        
        float diffuse = max(dot(N,L),0.0);
        diffuse = smoothstep(diffuse, 0.0, 0.5);
        
        gl_FragColor = color0*diffuse + color1 + color2*(spec+spec2);
        }''')
        
class oglSkeletalShader( oglShader ):
    def __init__( self ):
        self._program = self.compile_program('''       
        attribute vec4 Vertex;
        attribute vec3 Normal;
        attribute vec2 TexCoord;
        attribute vec2 Index;
        attribute vec2 Weight;
        uniform mat4 ModelviewMatrix;
        uniform mat4 ProjectionModelviewMatrix;
        uniform mat4 Bone[10];  //Array of bones that you compute (animate) on the CPU and you upload to the shader
       
        varying vec2 TexCoord0;
        varying vec3 EyeNormal;
       
        void main()
        {
          vec4 newVertex;
          vec4 newNormal;
          int index;
       
          index=int(Index.x);    //Cast to int
          newVertex = (Bone[index] * Vertex) * Weight.x;
          newNormal = (Bone[index] * vec4(Normal, 0.0)) * Weight.x;
          index=int(Index.y);    //Cast to int
          
          newVertex = (Bone[index] * Vertex) * Weight.y + newVertex;
          newNormal = (Bone[index] * vec4(Normal, 0.0)) * Weight.y + newNormal;
          EyeNormal = vec3(ModelviewMatrix * newNormal);
          
          newVertex = (Bone[index] * Vertex) * Weight.z + newVertex;
          newNormal = (Bone[index] * vec4(Normal, 0.0)) * Weight.z + newNormal;
          
          EyeNormal = vec3(ModelviewMatrix * newNormal);
          gl_Position = ProjectionModelviewMatrix * newVertex;
          TexCoord0 = TexCoord;
        }''')

        
'''
// Author:		Aaron Eady
// Purpose:		this vertex shader will take in an animation matrix and do the transforms to keep this from the CPU

uniform mat4 bones[40];		// arbitrary number of bones in the animation
attribute vec4 influences;	// the 4 influences per vertex
attribute vec3 weight;		// the 3 weights per vertex

void main(void)
{
	// get the vertex
	vec4 outVert;				// used to hold results of vertex calcs
	vec4 curVert = gl_Vertex;	// used to hold the current vertex we're on
	float totalWeight;			// used to keep the addition of each weight so we can do the last weight
	
	// loop through the number of influences for each bone matrix
	// the forth one is done outside of the loop
	for(int i = 0; i < 3; i++)
	{
		// multiply the bone matrix to the current position and the weight
		outVert += weight[i] * (vec4(bones[int(influences[i])] * curVert));	
		
		// accumulate the weights
		totalWeight += weight[i];
	}

	// do the final weight outside the loop
	outVert += (1.0 - totalWeight) * (vec4(bones[int(influences[3])] * curVert));	
	
	// set the texture coordinate to keep the texture on the model
	gl_TexCoord[0] = gl_MultiTexCoord0;
	
	// set the vertex position
	// we're changing the vertex position so instead of gl_ModelViewProjectionMatrix * gl_Vertex (ftransform()) we use the new vertex position
	gl_Position = vec4(gl_ModelViewProjectionMatrix * outVert);
}

// draw using vbo's
// the vbo pointer should have the 3 generated buffers from the SetupOptimize function
// we have to bind the vertex, normal, and texcoord data before each glDrawElements call
			
// bind the verts
glBindBuffer(GL_ARRAY_BUFFER, this->m_unVbos[nIndex]);
glVertexPointer(3, GL_FLOAT, 0, 0);
nIndex++;
// bind the normals
glBindBuffer(GL_ARRAY_BUFFER, this->m_unVbos[nIndex]);
glNormalPointer(GL_FLOAT, 0, 0);
nIndex++;
// bind the texcoords
glBindBuffer(GL_ARRAY_BUFFER, this->m_unVbos[nIndex]);
glTexCoordPointer(2, GL_FLOAT, 0, 0);
nIndex++;

glBindTexture(GL_TEXTURE_2D, this->Meshs[i].hTexture);

// using an animation shader
glUseProgram(this->m_unAnim);

	unsigned short * index = (unsigned short *)Meshs[i].uIdxs.pIndices;
	TMdfVertSkn * MeshData = (TMdfVertSkn *)(Meshs[i].uVtxs.pVertices);

	// pass the shader the whole body matrix (pAnimator->m_vpJoints)
	// glUniformMatrix4fv(GLint location, GLsizei count, GLboolean transpose, GLfloat *value)
	glUniformMatrix4fv(this->m_unMat4Loc, 40, false, &this->m_pAnimation->m_vpJoints->fArray[0]);

	// no need to pass the shader the current position b/c gl_Vertex will take care of that
	// no need to pass the shader the current normal b/c gl_Normal will take care of that

	// pass the shader the 4 influences
	// this will need to change per vertex so it needs to be an attribute variable
	glVertexAttrib4fv(this->m_unInfLoc, (GLfloat *)MeshData[*index].bones);
	// pass the shader the weights for the vertex as an attribute
	glVertexAttrib3fv(this->m_unWeightLoc, &MeshData[*index].weights[0]);

	glDrawElements(GL_TRIANGLES, this->Meshs[i].nNumIndices, GL_UNSIGNED_SHORT, (unsigned short *)this->Meshs[i].uIdxs.pIndices);

// turn off the shader
glUseProgram(0);


'''
