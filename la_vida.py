#!/usr/env python

import sys, os, os.path, soya
from GameApp.game_app_3d import GameApp3d
from lavida_config import getDataPath
from game_config import GameConfig


if __name__ == "__main__":
    DataPath = getDataPath()
    soya.path.append( DataPath )
    config_file = GameConfig( "%s/la_vida.cfg" % DataPath.replace("/data", "" ) )
    # get config file
    # use config file for screen resolution
    # use config file for screen mode (full screen or not)
    # make scene instance
    # use library loop structure
    screen_resolution = config_file.ScreenResolution()
    fullscreen = config_file.ScreenMode()
    la_vida = GameApp3d()
    la_vida.run()
