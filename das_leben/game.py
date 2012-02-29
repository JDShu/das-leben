'''
* This file is part of Das Leben.
* Copyright (C) 2009 Mike Hibbert
* Copyright (C) 2011 Hans Lo
*
* Das Leben is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* Das Leben is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Das Leben.  If not, see <http://www.gnu.org/licenses/>.
'''

import os

from game_graphics import GameGfx
from game_handler import GameHandler
from gui import GuiManager
from audio import Audio

def setup(node, data):
    gfx = GameGfx(node, data)
    gui = GuiManager(data, gfx)
    handler = GameHandler(gfx, gui, data)
