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
    '''
    The main loop of the La Vida framework
    @author Mike Hibbert
    @version 0.1
    '''

    # Create the game object 
    l_Game = GameApp3d(a_AppName="La Vida", a_DataPath=getDataPath() )

    Running = True

    while Running:
        # Process event
        Running = l_Game.ProcessEvents()
        # Process behaviours for game objects
        l_Game.ProcessBehaviours()
        # Render the game scene and objects
        l_Game.Draw()

    # shut down all video, audio and anything else on exit
    l_Game.Exit()

if __name__ == "__main__": main()
