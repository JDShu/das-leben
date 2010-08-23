#!/usr/env python

import GameApp
from GameApp.game_app_3d import GameApp3d

def main():

    l_Game = GameApp3d( a_AppName="Skeletal Animation" )

    Running = True

    while Running:
        Running = l_Game.ProcessEvents()
        l_Game.Draw()

    l_Game.Exit()

if __name__ == "__main__": main()
