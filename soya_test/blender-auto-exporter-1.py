#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- indent-tabs-mode: t -*-

# Soya 3D tutorial
# Copyright (C) 2004 Jean-Baptiste LAMY
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


# blender-auto-exporter-1: Blender auto-exporter : how to export models automatically

# This lesson is similar to basic-2.py, but it loads a Blender model !
# You NEED Blender to run this lesson.

# The Soya auto-exporter feature currently support the following file formats :
#  - Blender model (Both static models, and Cal3D ones)
#  - OBJ/MTL model (thanks David PHAM-VAN)
#  - .png images
#  - .jpeg images 


# Imports and inits Soya (see lesson basic-1.py).

import sys, os, os.path, soya

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

# Creates the scene.

scene = soya.World()

# Loads the knife model.

# To use auto-exporter, simply put your Blender models in {soya.path}/blender/ , your
# OBJ/MTL models in {soya.path}/obj/ and your textures in {soya.path}/images/ .
# Soya will automatically exports models to Soya worlds ans models, and textures to
# materials, if the corresponding Soya doesn't exist OR is not up-to-date.

# Here, the knife model doesn't exist as a Soya model yet, but the original Blender model
# is in {soya.path}/blender/knife.blender ; so Soya will find it, export it to
# a world and then compile the world into a model.

# Soya will save the exported world and model, so if you run the lesson again, the model
# won't be exported again. If you want so, just modify the model and/or the texture.

knife_model = soya.Model.get("knife")

# The Blender model has a Text buffer called "soya_params".
# This buffer is analyzed and gives additionnal information ; here it contains
# "cellshading=1" and thus enable cell_shading for the model.

# The list of ATTR=VALUE code usable in the text buffer corresponds to the options
# available at the beginning of the blender2soya.py script (see this script), e.g. :
#     scale=1.0
#     shadow=1
#     cellshading=1
#     cellshading_shader=shader_name
#     cellshading_outline_width=5.0
#     =5.0
#     =5.0
#     
# The MATERIAL_MAP option has a different syntax. E.g. the following will replace the
# material called "old_material_name" by the one called "new_material_name".
#     material_old_material_name=new_material_name
# 
# You can also make curent a specific position of an animation (called Action by Blender)
# as following :
#     animation=animation_name
#     animation_time=1

# If you want to generate SEVERAL different models from a SINGLE Blender file,
# you can use alternative text buffers. For example the following :

#knife_model2 = soya.Model.get("knife@with_sword_material")

# will read the Blender text buffer "with_sword_material" in the model in addition to
# "soya_params". Here is contains "material_knife=epee_turyle", which replace the knife
# material by the sword one (In French, epee=sword).


# The rest of the script is the same than lesson-2.

# Creates a rotating body class.

class RotatingBody(soya.Body):
	def advance_time(self, proportion):
		soya.Body.advance_time(self, proportion)
		self.rotate_y(proportion * 5.0)


knife    = RotatingBody(scene, knife_model )
knife.x  = -1

##knife2   = RotatingBody(scene, knife_model2)
##knife2.x = 1

# Creates a light.

light = soya.Light(scene)
light.set_xyz(0.5, 0.0, 2.0)

# Creates a camera.

camera = soya.Camera(scene)
camera.z = 3.0
soya.set_root_widget(camera)

soya.MainLoop(scene).main_loop()

