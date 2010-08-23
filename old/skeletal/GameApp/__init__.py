'''__all__ = []

for subpackage in ['game_app_3d']:
    try:
        exec 'import %s' % subpackage
        __all__.append( subpackage )
    except:
        print "Cant find module %s" % subpackage'''
        
from game_app_3d import *


