# -*- indent-tabs-mode: t -*-

# Soya 3D tutorial
# Copyright (C) 2001-2004 Jean-Baptiste LAMY
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


# character-animation-1: Character animation with Cal3D : here comes Balazar the Sorcerer !


# Or how to write a Cal3D viewer in less that 20 lines...

# For information, this character has been created in Blender and exported to Cal3D
# with my Blender2Cal3D script: http://oomadness.nekeme.net/en/blender2cal3d/index.html

# See Cal3D documentation for more info, and AnimatedModel and Body docstrings for
# advanced info on materials loading (e.g, how to substitute Cal3D materials by Soya ones).


# Imports and inits Soya.

import sys, os, os.path, soya, soya.widget as widget

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

# Creates the scene.

scene = soya.World()

# Load a Cal3D model.
# Cal3D models are saved in the 'models' subdirectory of soya.path ; each cal3d model
# is a subdirectory and not a file (see tutorial/data/models/balazar). It contains
# skeleton, animation, mesh and material files, and a ".cfg" file with the same name
# that the subdirectory.

# You can also use cal3d.parse_cfg_file(filename).

sorcerer_model = soya.AnimatedModel.get("MoCap3")

# You can get the list of available mesh and animation names
# as following:

print "Available meshes    :", sorcerer_model.meshes    .keys()
print "Available animations:", sorcerer_model.animations.keys()

# Creates a Cal3D body, using the sorcerer_model.
# See the docstrings of the soya.cal3d module to learn about mesh attachment and
# detachment possibilities (see Body.__init__, Body.attach and Body.detach).
# It can be used e.g. for dismembering, or changing the weapon of a character.

sorcerer = soya.Body(scene, sorcerer_model)

# Rotates Balazar the sorcerer

sorcerer.rotate_y(-120.0)

# Starts playing the animation called "marche" in cycle ("marche" is the French for walk).

sorcerer.animate_blend_cycle("Action")

# To stop playing the animation:
#
#sorcerer.animate_clear_cycle("marche")
#
# For non-cyclic movment, do:
#
#sorcerer.animate_execute_action("marche")
#
# See the cal3d.Body.animate* docstrings for more info about optional arguments


# Adds a camera, an FPS label, a light and starts the main loop.

camera = soya.Camera(scene)
camera.set_xyz(0.0, 1.5, 30.0)

soya.set_root_widget(widget.Group())
soya.root_widget.add(camera)
soya.root_widget.add(widget.FPSLabel())

soya.Light(scene).set_xyz(5.0, 5.0, 2.0)


# import time
# main_loop = soya.MainLoop(scene)
# for i in range(3):
# 	for j in range(10):
# 		time.sleep(0.1)
# 		main_loop.update()
# 	soya.render()
# 	print "."
# 	soya.screenshot().resize((320, 240)).save(os.path.join(os.path.dirname(sys.argv[0]), "results", os.path.basename(sys.argv[0])[:-3] + "_%s.jpeg" % i))

soya.MainLoop(scene).main_loop()

