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
import pygame
import sys

class LoadingScreen:
    ''' A screen to display the title screen and progress bar'''
    def __init__(self, a_ScreenWidth, a_ScreenHieght):
        self.m_Width = a_ScreenWidth
        self.m_Height = a_ScreenHieght
        
    def Draw(self):
        '''Draw the loading screen'''