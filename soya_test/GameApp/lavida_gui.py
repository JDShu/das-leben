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

import soya, soya.gui

class LaVidaMenuStyle( soya.gui.style.Style ):
    def __init__( self ):
        soya.gui.style.Style.__init__( self )
        
        self.materials[0].diffuse = (0.8, 0.0, 0.0, 1.0) # Base
	self.materials[1].diffuse = (1.0, 0.2, 0.2, 1.0) # Selected
	self.materials[2].diffuse = (0.8, 0.0, 0.0, 1.0) # Window title
	self.materials[3].diffuse = (1.0, 0.0, 0.0, 1.0) # Selected window title
	self.materials[4].diffuse = (1.0, 1.0, 1.0, 0.9) # Window background
	self.corner_colors = [
                (0.0, 0.0, 0.0, 1.0), # Base
                (0.0, 0.0, 0.0, 1.0), # Selected
                (0.0, 0.0, 0.0, 1.0), # Window title
                (0.0, 0.0, 0.0, 1.0), # Selected window title
                (0.5, 0.5, 0.5, 0.5), # Window background
                ]
	self.line_colors = [
                (0.0, 0.0, 0.0, 1.0), # Base
                (0.0, 0.0, 0.0, 1.0), # Selected
                (0.0, 0.0, 0.0, 1.0), # Window title
                (0.0, 0.0, 0.0, 1.0), # Selected window title
                (0.0, 0.0, 0.0, 1.0), # Window background
                ]
	self.text_colors = [
                (0.0, 0.0, 0.0, 1.0), # Base
                (0.0, 0.2, 0.0, 1.0), # Selected
                (1.0, 1.0, 1.0, 1.0), # Window title
                ]
	self.line_width = 1
	
	
	self.materials[0].diffuse = (1.0, 0.9, 0.4, 1.0) # Base
	self.materials[1].diffuse = (1.0, 1.0, 0.7, 1.0) # Selected
	self.materials[2].diffuse = (1.0, 0.9, 0.4, 1.0) # Window title
	self.materials[3].diffuse = (1.0, 1.0, 0.5, 1.0) # Selected window title
	
	self.materials[2].diffuse = (1.0, 0.7, 0.2, 1.0) # Window title
	self.materials[3].diffuse = (1.0, 0.9, 0.4, 1.0) # Selected window title
	self.materials[4].diffuse = (1.0, 1.0, 1.0, 0.9) # Window background
	b  = (0.9, 0.6, 0.0, 1.0)
	b2 = (0.9, 0.5, 0.0, 1.0)
	self.corner_colors = [
                b, # Base
                b, # Selected
                b2, # Window title
                b2, # Selected window title
                (1.0, 0.9, 0.4, 0.9), # Window background
                ]
	self.line_colors = [
                b, # Base
                b, # Selected
                b2, # Window title
                b2, # Selected window title
                b, # Window background
                ]
	self.text_colors = [
                (0.0, 0.0, 0.0, 1.0), # Base
                #(0.0, 0.2, 0.0, 1.0), # Selected
                (0.4, 0.4, 0.0, 1.0), # Selected
                (0.7, 0.4, 0.0, 1.0), # Window title
                ]
	self.line_width = 1