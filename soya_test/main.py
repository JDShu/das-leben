#!/usr/env python

import sys, os, os.path, soya, soya.sphere

soya.init( "test", width=1024, height=768 )
r = soya.get_renderer()

soya.path.append( os.path.join( os.path.dirname( sys.argv[ 0 ] ), "data" ) )

scene = soya.World()

##chair = soya.Model.get( "chair_70th" )
##b = soya.Body( scene, chair )
##b.rotate_y( 60.0 )
##b.scale( 0.25, 0.25, 0.25 )

model_builder = soya.SimpleModelBuilder()
model_builder.shadow = 1

knife = soya.World.get( "knife" )
knife.model_builder = model_builder
knife_model = knife.to_model()

class RotatingBody(soya.Body):
	def advance_time(self, proportion):
		soya.Body.advance_time(self, proportion)
		self.rotate_y(proportion * 5.0)
		
knife = RotatingBody( scene, knife_model )
knife.rotate_y( 60.0 )
knife.rotate_x( 45.0 )
knife.x = 10
knife.z = 10
knife.y = 2


ball_s = soya.sphere.Sphere()
ball_s.model_builder = model_builder
ball = soya.Body( scene, ball_s.to_model() )
ball.x = 20
ball.y = 4
ball.z = 20



terrain_size = 129
t = soya.Terrain( scene, terrain_size, terrain_size )

t2 = soya.Terrain( scene, terrain_size, terrain_size )
t.y = 10

grass = soya.Material.get( "grass" )

t.set_material_layer( grass, 0.0, 1.0 )
t.patch_size = 10.0

t2.set_material_layer( grass, 0.0, 1.0 )
t2.patch_size = 10.0

light2 = soya.Light(scene)
light2.set_xyz(10.0, 130.0, 10.0)
light2.diffuse = (0.0, 0.2, 0.7, 1.0)

class MovableCamera(soya.Camera):
	def __init__(self, parent):
		soya.Camera.__init__(self, parent)
		
		self.speed = soya.Vector(self)
		self.rotation_y_speed = 0.0
		self.rotation_x_speed = 0.0
		
	def begin_round(self):
		soya.Camera.begin_round(self)
		
		for event in soya.MAIN_LOOP.events:
			if event[0] == soya.sdlconst.KEYDOWN:
				if   event[1] == soya.sdlconst.K_e:     self.speed.z = -1.0
				elif event[1] == soya.sdlconst.K_d:   self.speed.z =  1.0
				elif event[1] == soya.sdlconst.K_DOWN:     self.rotation_x_speed = 10.0
				elif event[1] == soya.sdlconst.K_UP:   self.rotation_x_speed = -10.0
				elif event[1] == soya.sdlconst.K_LEFT:   self.rotation_y_speed =  10.0
				elif event[1] == soya.sdlconst.K_RIGHT:  self.rotation_y_speed = -10.0
				elif event[1] == soya.sdlconst.K_q:      soya.MAIN_LOOP.stop()
				elif event[1] == soya.sdlconst.K_ESCAPE: soya.MAIN_LOOP.stop()
			if event[0] == soya.sdlconst.KEYUP:
				if   event[1] == soya.sdlconst.K_e:     self.speed.z = 0.0
				elif event[1] == soya.sdlconst.K_d:   self.speed.z = 0.0
				elif event[1] == soya.sdlconst.K_DOWN:     self.rotation_x_speed = 0.0
				elif event[1] == soya.sdlconst.K_UP:   self.rotation_x_speed = 0.0
				elif event[1] == soya.sdlconst.K_LEFT:   self.rotation_y_speed = 0.0
				elif event[1] == soya.sdlconst.K_RIGHT:  self.rotation_y_speed = 0.0
			
	def advance_time(self, proportion):
		self.add_mul_vector(proportion, self.speed)
		self.turn_y(self.rotation_y_speed * proportion)
		self.turn_x(self.rotation_x_speed * proportion)
		

camera = MovableCamera(scene)
camera.set_xyz(16.0, 4.0, 0.0)
camera.look_at( soya.Point(scene, 16.0, -6.0, 10.0) )

soya.set_root_widget(camera)

scene.atmosphere = soya.Atmosphere()
scene.atmosphere.fog = 1
scene.atmosphere.fog_start = 30.0
scene.atmosphere.fog_end = 40.0
scene.atmosphere.fog_color = ( 0.85, 0.85, 1.0, 1.0 )
scene.atmosphere.bg_color= ( 0.85, 0.85, 1.0, 1.0 )
scene.atmosphere.ambient = ( 0.85, 0.85, 1.0, 1.0 )

import soya.widget
soya.set_root_widget(soya.widget.Group())
soya.root_widget.add(camera)
soya.root_widget.add(soya.widget.FPSLabel())

soya.MainLoop( scene ).main_loop()
