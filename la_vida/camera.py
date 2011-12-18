'''
* This file is part of La Vida.
* Copyright (C) 2011 Hans Lo
*
* La Vida is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* La Vida is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Touhou SRPG.  If not, see <http://www.gnu.org/licenses/>.
'''

CAMERA_SPEED = 0.3
CAMERA_TURN_SPEED = 0.3

class CameraHandler:
    
    def __init__(self, camera):
        self.camera = camera
        self.camera.setPos(-3,-3,9)
        self.camera.setHpr(-45,-50,0)
    
    def tilt_up(self):
        self.camera.setP(self.camera, CAMERA_SPEED)
        
    def tilt_down(self):
        self.camera.setP(self.camera, -CAMERA_SPEED)

    def leftward(self):
        self.camera.setPos(self.camera, -CAMERA_SPEED,0,0)

    def rightward(self):
        self.camera.setPos(self.camera, CAMERA_SPEED,0,0)

    def zoom_in(self):
        self.camera.setPos(self.camera, 0,CAMERA_SPEED,0)

    def zoom_out(self):
        self.camera.setPos(self.camera, 0,-CAMERA_SPEED,0)

    def rotate_clockwise(self):
        self.camera.setH(self.camera, CAMERA_TURN_SPEED)

    def rotate_counterclockwise(self):
        self.camera.setH(self.camera, -CAMERA_TURN_SPEED)

    def north_preset(self):
        self.camera.setPos(-3,-3,9)
        self.camera.setHpr(-45,-50,0)

    def south_preset(self):
        self.camera.setPos(9,9,9)
        self.camera.setHpr(135,-50,0)

    def west_preset(self):
        self.camera.setPos(9,-3,9)
        self.camera.setHpr(45,-50,0)

    def east_preset(self):
        self.camera.setPos(-3,9,9)
        self.camera.setHpr(225,-50,0)
