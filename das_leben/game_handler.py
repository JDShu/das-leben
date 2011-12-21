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
import sys

from direct.showbase import DirectObject

class GameHandler(DirectObject.DirectObject):

    def __init__(self, gfx=None, gui=None, data=None):
        self.setup_gfx_events(gfx)
        self.setup_game_events(data)
        self.setup_gui_events(gui)

    def setup_gfx_events(self, gfx_manager):
        camera = gfx_manager.camera_handler
        self.accept('a-repeat', camera.leftward)
        self.accept('d-repeat', camera.rightward)
        self.accept('z-repeat', camera.zoom_in)
        self.accept('x-repeat', camera.zoom_out)
        self.accept('arrow_up-repeat', camera.tilt_up)
        self.accept('arrow_down-repeat', camera.tilt_down)
        self.accept('arrow_left-repeat', camera.rotate_clockwise)
        self.accept('arrow_right-repeat', camera.rotate_counterclockwise)
        self.accept('1', camera.north_preset)
        self.accept('2', camera.east_preset)
        self.accept('3', camera.south_preset)
        self.accept('4', camera.west_preset)
        self.accept('5', camera.front_preset)
        self.accept('6', camera.back_preset)
        self.accept('7', camera.left_preset)
        self.accept('8', camera.right_preset)

    def setup_game_events(self, game_data):
        '''stub'''

    def setup_gui_events(self, gui):
        self.accept('escape', gui.escape_command)
