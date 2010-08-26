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

import os, ConfigParser

class GameConfig:
	def __init__( self, game_config_file_path ):
		self.config_parser = ConfigParser.ConfigParser()
		if os.path.isfile( game_config_file_path ):
			self.Load( game_config_file_path )

	def Save( self, file_path, ResWidth, ResHeight, Fullscreen, MusicOn, MusicVolume, Music ):
		f = open( file_path, "w" )
		if not self.config_parser.has_section( "Video" ): self.config_parser.add_section( "Video" )
		self.config_parser.set( "Video", "width", ResWidth )
		self.config_parser.set( "Video", "height", ResHeight )
		self.config_parser.set( "Video", "fullscreen", Fullscreen)
		if not self.config_parser.has_section( "Audio" ): self.config_parser.add_section( "Audio" )
		self.config_parser.set( "Audio", "MusicOn", MusicOn )
		self.config_parser.set( "Audio", "Track", Music )
		self.config_parser.set( "Audio", "Track", MusicVolume )
		self.config_parser.write( f )
		f.close()

	def Load( self, game_config_file_path ):
		self.config_parser.read( game_config_file_path )
		self.screen_resolution_x = self.config_parser.get("Video", "width")
		self.screen_resolution_y = self.config_parser.get("Video", "height")
		self.fullscreen = self.config_parser.get("Video", "fullscreen") == 'True' and True or False
		self.music = self.config_parser.get("Audio", "music") == 'True' and True or False
		self.music_track = self.config_parser.get("Audio", "track")
		self.music_volume = float( self.config_parser.get("Audio", "volume") )

	def ScreenResolution( self ):
		return ( int( self.screen_resolution_x ), int( self.screen_resolution_y ) )

	def ScreenMode( self ):
		retVal = 1
		if self.fullscreen == False:
			retVal = 0
		return retVal

	
