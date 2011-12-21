import os

class Audio:
    def __init__(self, loader):
        music = loader.loadSfx(os.path.join("data","music", "alexandra.mp3"))
        music.setLoop(True)
        music.play()
