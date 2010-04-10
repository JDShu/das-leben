import os, ConfigParser

class GameConfig:
	def __init__( self, game_config_file_path ):
		self.config_parser = ConfigParser.ConfigParser()
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

################################################################################

o_game_config = GameConfig( "la-vida.cfg" )

o_game_config.Save( "la-vida.cfg", "1024", "768", "Fullscreen", True, "sometrack", 50 )

o_game_config.Load( "la-vida.cfg" )
