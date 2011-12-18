'''
 * This file is part of La Vida
 * Copyright (C) 2009 Mike Hibbert
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
'''
import os

from game_data import GameData
from game_handler import GameHandler
from graphics import GfxManager

MAP_SIZE = 20

class Game:
    """
    Load map data from specified filename and run a game session.
    """
    def __init__(self, data_filename):
        self.game_data = GameData(data_filename)
        self.gfx_manager = GfxManager(self.game_data)
        self.gfx_manager.load_graphics()
        self.game_handler = GameHandler(self.gfx_manager, self.game_data)

    def run(self):
        self.gfx_manager.run()
