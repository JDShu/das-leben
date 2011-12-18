from direct.showbase.ShowBase import ShowBase
import camera

class GameImplementation(ShowBase):
    """
    The main game class which manages all other processes.
    Currently handles graphics.
    """
    def __init__(self):
        ShowBase.__init__(self)
        self.camera_handler = camera.CameraHandler(self.camera)
