from direct.gui.DirectGui import *
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import TextNode

class MainMenu:
    def __init__(self):
        self.menu_gui = MenuGui()

    def run(self):
        self.menu_gui.run()

class MenuGui(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.title = OnscreenText(text="Das Leben")
