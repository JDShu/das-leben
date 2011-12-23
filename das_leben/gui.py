from pandac.PandaModules import TextNode
from direct.gui.DirectGui import *

import global_functions

class GuiManager:
    
    def __init__(self, game_data):
        self.onscreen_title = OnscreenText(text="Das Leben", pos=(0.95,-0.95), 
                                  scale=0.07, fg=(1,0.5,0.5,1),
                                  align=TextNode.ACenter)
        self.quit_dialog = YesNoDialog(dialogName="Quit",
                                       text="Do you want to quit?",
                                       command=self.quit_confirm)
        self.main_panel = DirectFrame(frameColor=(0.5, 0.2, 0, 1),
                                      frameSize=(0, 2.2, 0, 0.3),
                                      pos=(-1.1, 0, -1))
        self.character_buttons = []
        catalog = game_data.character_catalog.get_catalog()
        self.generate_character_buttons(catalog)

    def generate_character_buttons(self, catalog):
        position_id = 0
        x = 0.3
        z = 0.15
        for character_id, character in catalog.items():
            button = DirectButton(text = character.profile.name,
                                  pos=(x,0,z),
                                  frameSize=(-2,2,-1,1),
                                  scale=0.1)
            button.reparentTo(self.main_panel)
            self.character_buttons.append(button)
            x += 0.4
            position_id += 1
                    
        self.quit_dialog.hide()
        self.dialogs_open = False
    
    def quit_confirm(self, confirmed):
        if confirmed:
            global_functions.quit()
        else:
            self.quit_dialog.hide()
            self.dialogs_open = False

    def escape_command(self):
        if self.dialogs_open:
            self.close_all_dialogs()
        else:
            self.open_quit_dialog()

    def open_quit_dialog(self):
        self.quit_dialog.show()
        self.dialogs_open = True

    def close_all_dialogs(self):
        self.quit_dialog.hide()
        self.dialogs_open = False
