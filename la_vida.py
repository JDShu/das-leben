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

import GameApp
from GameApp.game_app_3d import GameApp3d
from lavida_config import getDataPath

def main():

    l_Game = GameApp3d(a_AppName="La Vida", a_DataPath=getDataPath() )

    Running = True

    while Running:
        Running = l_Game.ProcessEvents()
        l_Game.ProcessBehaviours()
        l_Game.Draw()

    l_Game.Exit()

if __name__ == "__main__": main()
