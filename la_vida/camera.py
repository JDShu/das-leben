from direct.showbase import DirectObject

CAMERA_SPEED = 0.2

class CameraHandler(DirectObject.DirectObject):
    def __init__(self, camera):
        self.camera = camera
        self.camera.setPos(5,-5,5)
        self.camera.setHpr(0,-40,-4)
        self.accept('w-repeat', self.tilt_up)
        self.accept('s-repeat', self.tilt_down)
        self.accept('a-repeat', self.leftward)
        self.accept('d-repeat', self.rightward)
        self.accept('z-repeat', self.zoom_in)
        self.accept('x-repeat', self.zoom_out)
        
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
