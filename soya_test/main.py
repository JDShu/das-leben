#!/usr/env python

import sys, os, os.path, soya

soya.init()

soya.path.append( os.path.join( os.path.dirname( sys.argv[ 0 ] ), "data" ) )

scene = soya.World()

chair = soya.Model.get( "chair_70th" )
b = soya.Body( scene, chair )
b.rotate_y( 60.0 )
light = soya.Light(scene)
light.set_xyz(2.0, 5.0, 0.0)

camera = soya.Camera(scene)
camera.z = 10.0
soya.set_root_widget(camera)

soya.MainLoop( scene ).main_loop()
