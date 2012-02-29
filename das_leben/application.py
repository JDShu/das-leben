from session import Session
from game_data import GameData

class Application:
    """
    Determines which sub-application to run:
    * Menu Screen
    * The Actual Game
    """
    def __init__(self):
        self.session = Session()

    def run(self):
        game_data = GameData("sample") # For now run the game on startup.
        self.session.run_game(game_data)
        self.session.run()
