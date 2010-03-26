import os, ConfigParser

class c_game_config:
	def __init__( self, game_name, game_config_file_path, game_resolution_x, game_resolution_y, game_mode, game_effects, game_music ):
		self.a_game_name = game_name
		self.a_game_config_file_path = game_config_file_path
		self.a_game_resolution_x = game_resolution_x
		self.a_game_resolution_y = game_resolution_y
		self.a_game_mode = game_mode
		self.a_game_effects = game_effects
		self.a_game_music = game_music
		self.o_config_parser = ConfigParser.ConfigParser()

	def m_save_game_config( self, ResWidth, ResHeight, Mode, Effects, Music ):
		self.o_config_parser.set("Video", "ResWidth", ResWidth)
		self.o_config_parser.set("Video", "ResHeight", ResHeight)
		self.o_config_parser.set("Video", "Mode", Mode)
		self.o_config_parser.set("Audio", "Effects", Effects)
		self.o_config_parser.set("Audio", "Music", Music)
		self.o_config_parser.write( self.a_game_config_file_path )

	def m_load_game_config( self ):
		self.o_config_parser.read( self.a_game_config_file_path )
		self.o_config_parser.get("Video", "ResWidth")
		self.o_config_parser.get("Video", "ResHeight")
		self.o_config_parser.get("Video", "Mode")
		self.o_config_parser.get("Audio", "Effects")
		self.o_config_parser.get("Audio", "Music")

################################################################################

o_game_config = c_game_config( game_name = "La Vida", game_config_file_path = "~/.la-vida.cfg", game_resolution_x = 1024, game_resolution_y = 768, game_mode = "Windowed", game_effects = 75, game_music = 50 )

print o_game_config.a_game_name

#o_game_config.m_save_game_config( ResWidth = "1024", ResHeight = "768", Mode = "Fullscreen", Effects = "75", Music = "50" )

#o_game_config.m_load_game_config()
