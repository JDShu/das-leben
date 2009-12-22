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
    
    def compile_program( self, vertex_source, fragment_source):
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
        
        