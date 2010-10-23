#!/usr/env python

import sys, os, os.path, soya
import GameApp
from GameApp.game_app_3d import GameApp3d
from lavida_config import *
from game_config import *


if __name__ == "__main__":
    DataPath = getDataPath()
    soya.path.append( DataPath )
    config_file = GameConfig( "%s/la_vida.cfg" % DataPath.replace("/data", "" ) )
    scrn_res = config_file.ScreenResolution()
    fullscreen = config_file.ScreenMode()
    scene = GameApp3d( scrn_res[ 0 ], scrn_res[ 1 ], fullscreen, 
                       a_AppName="La Vida", a_DataPath=DataPath )
    soya.MainLoop( scene ).main_loop()
