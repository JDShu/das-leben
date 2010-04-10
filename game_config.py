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

	def Save( self, file_path, ResWidth, ResHeight, Mode, MusicOn, MusicVolume, Music ):
		f = open( file_path, "w" )
		if not self.config_parser.has_section( "Video" ): self.config_parser.add_section( "Video" )
		self.config_parser.set( "Video", "ResWidth", ResWidth )
		self.config_parser.set( "Video", "ResHeight", ResHeight )
		self.config_parser.set( "Video", "Mode", Mode)
		if not self.config_parser.has_section( "Audio" ): self.config_parser.add_section( "Audio" )
		self.config_parser.set( "Audio", "MusicOn", MusicOn )
		self.config_parser.set( "Audio", "Track", Music )
		self.config_parser.set( "Audio", "Track", MusicVolume )
		self.config_parser.write( f )
		f.close()

	def Load( self, game_config_file_path ):
		self.config_parser.read( game_config_file_path )
		self.screen_resolution_x = self.config_parser.get("Video", "ResWidth")
		self.screen_resolution_y = self.config_parser.get("Video", "ResHeight")
		self.screen_mode = self.config_parser.get("Video", "Mode")
		self.game_music = self.config_parser.get("Audio", "Music")

	def ScreenResolution( self ):
		return ( self.screen_resolution_x, self.screen_resolution_y )

	def ScreenMode( self ):
		return self.screen_mode

	
if __name__ == "__main__":

	o_game_config = GameConfig( "la-vida.cfg" )

	o_game_config.Save( "la-vida.cfg", "1024", "768", "Fullscreen", True, "sometrack", 50 )

	o_game_config.Load( "la-vida.cfg" )
