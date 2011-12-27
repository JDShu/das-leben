'''
* This file is part of Das Leben.
* Copyright (C) 2011 Hans Lo
*
* Das Leben is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* Das Leben is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Das Leben.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import math

from pandac.PandaModules import PandaNode, CardMaker, DirectionalLight,AmbientLight, VBase4, CollisionTraverser
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

import camera
import floor_layout
import wall_layout
from ai import AI

class GfxManager(ShowBase):

    def __init__(self, game_data):
        ShowBase.__init__(self)
        self.wall_data = game_data.wall_data
        self.floor_data = game_data.floor_data
        self.object_catalog = game_data.object_catalog
        self.character_catalog = game_data.character_catalog
        self.load_3d_gui()
        
        self.disableMouse()
        self.camera_handler = camera.CameraHandler(self.camera, game_data.map_dimensions)
        self.set_lighting()

        self.load_graphics()
        self.ai = AI(game_data, self.character_models, self.object_models)

    def set_lighting(self):
        dlight = DirectionalLight('dlight')
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(45,-45,0)
        self.render.setLight(dlnp)

        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor(VBase4(0.5, 0.5, 0.5, 1))
        ambientLightNP = render.attachNewNode(ambientLight)
        self.render.setLight(ambientLightNP)
        
    def load_graphics(self):
        '''load all 3d objects and models'''
        
        self.load_floor()
        self.load_walls()
        self.load_objects()
        self.load_characters()

    def load_objects(self):
        self.object_models = {}
        for key in self.object_catalog:
            house_object = self.object_catalog[key]
            object_model = self.loader.loadModel(os.path.join("data","egg", house_object.name))
            object_model.reparentTo(self.render)
            x_coord, y_coord = house_object.map_coords
            object_model.setPos(x_coord-0.5, y_coord-0.5, 0)
            self.object_models[key] = object_model

    def load_walls(self):
        for x, row in enumerate(self.wall_data.layout):
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

    def load_characters(self):
        self.character_models = {}
        catalog = self.character_catalog.get_catalog()
        for key in catalog:
            character_model = Actor(os.path.join("data","egg","placeholder_character"))
            x,y = catalog[key].position
            character_model.setPos(x-0.5,y-0.5,0)
            character_model.reparentTo(self.render)
            self.character_models[key] = character_model

    def load_3d_gui(self):
        self.selector = self.loader.loadModel(os.path.join("data","egg", "selected"))
        self.selector.setPos(0,0,3)
        self.selector.hide()
        self.selector.reparentTo(self.render)        

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
        
        for x, row in enumerate(self.floor_data.layout):
            for y, tile in enumerate(row):
                floor = self.render.attachNewNode(cm.generate())
                floor.setP(270)
                floor.setPos(x,y,0)                
                if tile == floor_layout.GRASS:
                    floor.setTexture(grass_texture)
                elif tile == floor_layout.WOOD:
                    floor.setTexture(wood_texture)

    def select_character(self, character_id):
        self.selector.show()
        self.selector.reparentTo(self.character_models[character_id])
        
    def move_character(self, character_id, destination):
        self.ai.begin_move(character_id, destination)

    def step_character(self, character_id, next_node):
        model = self.character_models[character_id]
        x, y, z = model.getPos()
        step = calculate_step((x,y),next_node)

        model.setPos(model, step[0], step[1], 0)
        model_pos = model.getPos()
        if (abs(next_node[0] - model_pos[0]) < 0.5
            and abs(next_node[1] - model_pos[1]) < 0.5):
            self.ai.character_catalog[character_id].pop_front()


def calculate_step(current, destination):
    v1, v2 = current, destination
    x, y = v1[0]-v2[0], v1[1]-v2[1]
    length = math.hypot(x,y)
    return (-x*0.1/length, -y*0.1/length)
