from direct.showbase import DirectObject

class CameraHandler(DirectObject.DirectObject):
    def __init__(self, camera):
        self.camera = camera
        self.camera.setPos(5,-5,5)
        self.camera.setHpr(0,-40,-4)
        self.accept('w-repeat', self.forward)
        self.accept('s-repeat', self.backward)
        self.accept('a-repeat', self.leftward)
        self.accept('d-repeat', self.rightward)
        self.accept('z-repeat', self.zoom_in)
        self.accept('x-repeat', self.zoom_out)
        
    def forward(self):
        self.camera.setP(self.camera, 0.1)
        
    def backward(self):
        pass

    def leftward(self):
        self.camera.setPos(self.camera, -0.1,0,0)

    def rightward(self):
        self.camera.setPos(self.camera, 0.1,0,0)

    def zoom_in(self):
        self.camera.setPos(self.camera, 0,0.1,0)

    def zoom_out(self):
        self.camera.setPos(self.camera, 0,-0.1,0)
