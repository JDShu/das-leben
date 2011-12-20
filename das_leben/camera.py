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

CAMERA_SPEED = 0.3
CAMERA_TURN_SPEED = 0.3

class CameraHandler:
    
    def __init__(self, camera, map_size):
        self.camera = camera
        self.map_width, self.map_height = map_size
        self.map_center = (self.map_width/2, self.map_height/2, 0)
        
        # Default camera view
        self.north_preset()
    
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
        self.camera.setPos(-self.map_center[0],
                           -self.map_center[1],
                           2*self.map_width)
        self.camera.lookAt(self.map_center)

    def south_preset(self):
        self.camera.setPos(self.map_center[0] + self.map_width,
                           self.map_center[1] + self.map_height,
                           2*self.map_width)
        self.camera.lookAt(self.map_center)

    def west_preset(self):
        self.camera.setPos(self.map_center[0] + self.map_width,
                           -self.map_center[1],
                           2*self.map_width)
        self.camera.lookAt(self.map_center)

    def east_preset(self):
        self.camera.setPos(-self.map_center[0],
                           self.map_center[1] + self.map_height,
                           2*self.map_width)
        self.camera.lookAt(self.map_center)

    def front_preset(self):
        self.camera.setPos(self.map_center[0],-2*self.map_width,0.5)
        self.camera.lookAt(self.map_center)

    def back_preset(self):
        self.camera.setPos(self.map_center[0],3*self.map_width,0.5)
        self.camera.lookAt(self.map_center)

    def left_preset(self):
        self.camera.setPos(-2*self.map_height,self.map_center[1],0.5)
        self.camera.lookAt(self.map_center)

    def right_preset(self):
        self.camera.setPos(3*self.map_height,self.map_center[1],0.5)
        self.camera.lookAt(self.map_center)
