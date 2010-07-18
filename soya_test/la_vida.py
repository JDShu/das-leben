#!/usr/env python

import sys, os, os.path, soya
import GameApp
from GameApp.game_app_3d import GameApp3d


if __name__ == "__main__":
    DataPath = os.path.join( os.path.dirname( sys.argv[ 0 ] ), "data" )
    soya.path.append( DataPath )
    scene = GameApp3d( a_AppName="La Vida", a_DataPath=DataPath )
    soya.MainLoop( scene ).main_loop()
