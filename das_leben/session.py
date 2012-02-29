from direct.showbase.ShowBase import ShowBase

import game

class Session(ShowBase):
    """
    Does the tree modifications and initializations necessary
    to switch between sub applications. Called by Applications.
    """

    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

    def run_game(self, game_data):
        game_node = self.render.attachNewNode("Game Node")
        game_session = game.setup(game_node, game_data)
        
    def run_main_menu(self):
        pass
