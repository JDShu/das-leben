CAMERA_SPEED = 0.2
CAMERA_TURN_SPEED = 0.1

class CameraHandler:
    
    def __init__(self, camera):
        self.camera = camera
        self.camera.setPos(5,-5,5)
        self.camera.setHpr(0,-40,-4)
    
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
