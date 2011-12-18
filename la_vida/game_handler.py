from direct.showbase import DirectObject

class GameHandler(DirectObject.DirectObject):

    def __init__(self, gfx_manager, game_data):
        self.setup_gfx_events(gfx_manager)
        self.setup_game_events(game_data)

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

    def setup_game_events(self, game_data):
        '''stub'''
