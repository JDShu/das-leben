from pandac.PandaModules import TextNode
from direct.gui.DirectGui import *

import global_functions

class GuiManager:
    
    def __init__(self):
        self.onscreen_title = OnscreenText(text="Das Leben", pos=(0.95,-0.95), 
                                  scale=0.07, fg=(1,0.5,0.5,1),
                                  align=TextNode.ACenter)

        self.quit_dialog = YesNoDialog(dialogName="YesNoCancelDialog",
                                       text="Do you want to quit?",
                                       command=self.quit_confirm)
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
