import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

g_Ext = ""

def IsExtensionSupported (TargetExtension):
	global g_Ext
	""" Accesses the rendering context to see if it supports an extension.
		Note, that this test only tells you if the OpenGL library supports
		the extension. The PyOpenGL system might not actually support the extension.
	"""
	
	if not g_Ext:
		Extensions = g_Ext = glGetString (GL_EXTENSIONS)
	else: 
		Extensions = g_Ext
	# python 2.3
	# if (not TargetExtension in Extensions):
	#	gl_supports_extension = False
	#	print "OpenGL does not support '%s'" % (TargetExtension)
	#	return False

	# python 2.2
	Extensions = Extensions.split ()
	found_extension = False
	for extension in Extensions:
		if extension == TargetExtension:
			found_extension = True
			break;
	if (found_extension == False):
		gl_supports_extension = False
		print "OpenGL rendering context does not support '%s'" % (TargetExtension)
		return False

	gl_supports_extension = True

	# Now determine if Python supports the extension
	# Exentsion names are in the form GL_<group>_<extension_name>
	# e.g.  GL_EXT_fog_coord 
	# Python divides extension into modules
	# g_fVBOSupported = IsExtensionSupported ("GL_ARB_vertex_buffer_object")
	# from OpenGL.GL.EXT.fog_coord import *
	if (TargetExtension [:3] != "GL_"):
		# Doesn't appear to following extension naming convention.
		# Don't have a means to find a module for this exentsion type.
		return False

	# extension name after GL_
	afterGL = TargetExtension [3:]
	try:
		group_name_end = afterGL.index ("_")
	except:
		# Doesn't appear to following extension naming convention.
		# Don't have a means to find a module for this exentsion type.
		return False

	group_name = afterGL [:group_name_end]
	extension_name = afterGL [len (group_name) + 1:]
	extension_module_name = "OpenGL.GL.ARB.%s" % (extension_name)

	try:
		__import__ (extension_module_name)
		print "PyOpenGL supports '%s'" % (TargetExtension)
	except:
		print "OpenGL rendering context supports '%s'" % (TargetExtension),
		print "however PyOpenGL (ver %s) does not." % (OpenGL.__version__)
		return False

	return True