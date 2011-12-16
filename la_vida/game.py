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
import os

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import CardMaker
from direct.task import Task

import wall_layout
import floor_layout
import camera

MAP_SIZE = 20

class Game(ShowBase):
    """
    The main game class which manages all other processes.
    Currently handles graphics.
    """
    def __init__(self):
                
        ShowBase.__init__(self)
        self.disableMouse()
        self.camera_handler = camera.CameraHandler(self.camera)
        self.load_graphics()
        #TODO: screen options
        #TODO: make some kind of gui
        
        self.selected_object = None
        self.edit_terrain = False

    def load_graphics( self ):
        '''load all 3d objects and models'''
        
        self.load_floor()
        self.load_walls()
        self.load_objects()

        # TODO: characters

    def load_floor(self):
        cm = CardMaker("floor")
        cm.setFrame(0, 1, 0, 1)
        card = cm.generate()

        # TODO: Somehow move texture information somewhere else.
        grass_texture = self.loader.loadTexture(os.path.join("data", "images", "grass.png"))
        wood_texture = self.loader.loadTexture(os.path.join("data", "images", "floor_wood_0.png"))
        
        floor_tiles = floor_layout.FloorLayout()
        floor_tiles.load_textfile(os.path.join("data","games","sample.floor"))
        
        for x, row in enumerate(floor_tiles.get_layout()):
            for y, tile in enumerate(row):
                floor = self.render.attachNewNode(cm.generate())
                floor.setP(270)
                floor.setPos(x,y,0)                
                if tile == floor_layout.GRASS:
                    floor.setTexture(grass_texture)
                elif tile == floor_layout.WOOD:
                    floor.setTexture(wood_texture)
        
    def load_objects(self):
        object_file = open(os.path.join("data","games","sample.objects"), 'r')
        for line in object_file:
            object_data = line.split(" ")
            object_name = object_data[0]
            x_coord = int(object_data[1])
            y_coord = int(object_data[2])
            scale = float(object_data[3])
            object_model = self.loader.loadModel(os.path.join("data","egg", object_name))
            object_model.reparentTo(self.render)
            object_model.setScale(scale, scale, scale)
            object_model.setPos(x_coord + scale, y_coord + scale, scale)

    def load_walls(self):
        walls = wall_layout.WallLayout()
        walls.load_textfile(os.path.join("data","games","sample.wall"))

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
