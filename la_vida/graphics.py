import os

from pandac.PandaModules import PandaNode, CardMaker
from direct.showbase.ShowBase import ShowBase

import camera
import floor_layout
import wall_layout
import house_objects

class GfxManager(ShowBase):

    def __init__(self, game_map):
        ShowBase.__init__(self)
        self.wall_data = game_map.wall_data
        self.floor_data = game_map.floor_data
        self.object_catalog = game_map.object_catalog
        self.disableMouse()
        self.camera_handler = camera.CameraHandler(self.camera)
                
    def load_graphics(self):
        '''load all 3d objects and models'''
        
        self.load_floor()
        self.load_walls()
        self.load_objects()
        
    def load_objects(self):
        for key in self.object_catalog:
            house_object = self.object_catalog[key]
            object_model = self.loader.loadModel(os.path.join("data","egg", house_object.name))
            object_model.reparentTo(self.render)
            object_model.setScale(house_object.scale, house_object.scale, house_object.scale)
            x_coord, y_coord = house_object.map_coords
            scale = house_object.scale
            object_model.setPos(x_coord + scale, y_coord + scale, scale)

    def load_walls(self):
        for x, row in enumerate(self.wall_data):
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

    def load_floor(self):
        cm = CardMaker("floor")
        cm.setFrame(0, 1, 0, 1)
        card = cm.generate()

        grass_texture = self.loader.loadTexture(os.path.join("data", "images", "grass.png"))
        wood_texture = self.loader.loadTexture(os.path.join("data", "images", "floor_wood_0.png"))
        
        for x, row in enumerate(self.floor_data):
            for y, tile in enumerate(row):
                floor = self.render.attachNewNode(cm.generate())
                floor.setP(270)
                floor.setPos(x,y,0)                
                if tile == floor_layout.GRASS:
                    floor.setTexture(grass_texture)
                elif tile == floor_layout.WOOD:
                    floor.setTexture(wood_texture)
