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
        // Vertex program
        // Vertex program
        varying vec3 normal;
        void main() {
            normal = gl_NormalMatrix * gl_Normal;
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        }
        ''', '''
        // Fragment program
        varying vec3 normal;
        void main() {
            float intensity;
            vec4 color;
            vec3 n = normalize(normal);
            vec3 l = normalize(gl_LightSource[0].position).xyz;
     
            // quantize to 5 steps (0, .25, .5, .75 and 1)
            intensity = (floor(dot(l, n) * 4.0) + 1.0)/4.0;
            color = vec4(intensity*1.0, intensity*0.5, intensity*0.5,
                intensity*1.0);
     
            gl_FragColor = color;
        }
        ''')
        
    def compile_shader(source, shader_type):
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
    
    def compile_program(vertex_source, fragment_source):
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
        
        