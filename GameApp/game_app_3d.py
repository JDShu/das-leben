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

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import CardMaker
from direct.task import Task

import wall_layout
import floor_layout

MAP_SIZE = 20

class GameApp3d(ShowBase):
    """
    The main game class which manages all other processes.
    Currently handles graphics.
    """
    def __init__(self):
                
        ShowBase.__init__(self)
        #TODO: our own camera, currently using the Panda3D default
        self.load_graphics()
        
        #TODO: screen options
        #TODO: make some kind of gui
        
        self.selected_object = None
        self.edit_terrain = False

    def load_graphics( self ):
        '''load all 3d objects and models'''
        # floor terrain
        cm = CardMaker("floor")
        cm.setFrame(0, 1, 0, 1)
        card = cm.generate()
        
        grass_texture = self.loader.loadTexture("./data/images/grass.png")
        wood_texture = self.loader.loadTexture("./data/images/floor_wood_0.png")
        
        floor_tiles = floor_layout.FloorLayout()
        floor_tiles.load_textfile("./data/games/sample.floor")
        
        for x, row in enumerate(floor_tiles.get_layout()):
            for y, tile in enumerate(row):
                floor = self.render.attachNewNode(cm.generate())
                floor.setP(270)
                floor.setPos(x,y,0)                
                if tile == floor_layout.GRASS:
                    floor.setTexture(grass_texture)
                elif tile == floor_layout.WOOD:
                    floor.setTexture(wood_texture)
                
        # TODO: system to load all objects as specified from a file
        self.oven = self.loader.loadModel("./data/egg/oven")
        self.oven.reparentTo(self.render)
        self.oven.setScale(0.49, 0.49, 0.49)
        self.oven.setPos(1.495, 1.495, 0.495)

        # TODO: encapsulate wall generation
        walls = wall_layout.WallLayout()
        walls.load_textfile("./data/games/sample.wall")

        for x, row in enumerate(walls.get_layout()):
            for y, wall in enumerate(row):
                if wall == wall_layout.EMPTY:
                    pass
                elif wall == wall_layout.HORIZONTAL:
                    self.make_horizontal_wall((x,y))
                elif wall == wall_layout.VERTICAL:
                    self.make_vertical_wall((x,y))
                elif wall == wall_layout.BOTH:
                    self.make_horizontal_wall((x,y))
                    self.make_vertical_wall((x,y))
                    
        # TODO: system to load floors
        
        # TODO: characters

    def make_horizontal_wall(self, pos):
        x, y = pos
        cm = CardMaker("wall")
        cm.setFrame(0, 1, 0, 2)
        front_card = cm.generate()
        front = self.render.attachNewNode(front_card)
        front.setH(90)
        front.setPos(x,y,0)
        back_card = cm.generate()
        back = self.render.attachNewNode(back_card)
        back.setH(270)
        back.setPos(x,y+1,0)

    def make_vertical_wall(self, pos):
        x, y = pos
        cm = CardMaker("wall")
        cm.setFrame(0, 1, 0, 2)
        front_card = cm.generate()
        front = self.render.attachNewNode(front_card)
        front.setH(0)
        front.setPos(x,y,0)
        back_card = cm.generate()
        back = self.render.attachNewNode(back_card)
        back.setH(180)
        back.setPos(x+1,y,0)

    # TODO: Event handling
