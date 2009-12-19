# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.36
#
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _md2
import new
new_instancemethod = new.instancemethod
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


class PySwigIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, PySwigIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, PySwigIterator, name)
    def __init__(self, *args, **kwargs): raise AttributeError, "No constructor defined"
    __repr__ = _swig_repr
    __swig_destroy__ = _md2.delete_PySwigIterator
    __del__ = lambda self : None;
    def value(*args): return _md2.PySwigIterator_value(*args)
    def incr(*args): return _md2.PySwigIterator_incr(*args)
    def decr(*args): return _md2.PySwigIterator_decr(*args)
    def distance(*args): return _md2.PySwigIterator_distance(*args)
    def equal(*args): return _md2.PySwigIterator_equal(*args)
    def copy(*args): return _md2.PySwigIterator_copy(*args)
    def next(*args): return _md2.PySwigIterator_next(*args)
    def previous(*args): return _md2.PySwigIterator_previous(*args)
    def advance(*args): return _md2.PySwigIterator_advance(*args)
    def __eq__(*args): return _md2.PySwigIterator___eq__(*args)
    def __ne__(*args): return _md2.PySwigIterator___ne__(*args)
    def __iadd__(*args): return _md2.PySwigIterator___iadd__(*args)
    def __isub__(*args): return _md2.PySwigIterator___isub__(*args)
    def __add__(*args): return _md2.PySwigIterator___add__(*args)
    def __sub__(*args): return _md2.PySwigIterator___sub__(*args)
    def __iter__(self): return self
PySwigIterator_swigregister = _md2.PySwigIterator_swigregister
PySwigIterator_swigregister(PySwigIterator)

class md2Header(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, md2Header, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, md2Header, name)
    __repr__ = _swig_repr
    __swig_setmethods__["m_ID"] = _md2.md2Header_m_ID_set
    __swig_getmethods__["m_ID"] = _md2.md2Header_m_ID_get
    if _newclass:m_ID = _swig_property(_md2.md2Header_m_ID_get, _md2.md2Header_m_ID_set)
    __swig_setmethods__["m_Version"] = _md2.md2Header_m_Version_set
    __swig_getmethods__["m_Version"] = _md2.md2Header_m_Version_get
    if _newclass:m_Version = _swig_property(_md2.md2Header_m_Version_get, _md2.md2Header_m_Version_set)
    __swig_setmethods__["m_SkinWidth"] = _md2.md2Header_m_SkinWidth_set
    __swig_getmethods__["m_SkinWidth"] = _md2.md2Header_m_SkinWidth_get
    if _newclass:m_SkinWidth = _swig_property(_md2.md2Header_m_SkinWidth_get, _md2.md2Header_m_SkinWidth_set)
    __swig_setmethods__["m_SkinHeight"] = _md2.md2Header_m_SkinHeight_set
    __swig_getmethods__["m_SkinHeight"] = _md2.md2Header_m_SkinHeight_get
    if _newclass:m_SkinHeight = _swig_property(_md2.md2Header_m_SkinHeight_get, _md2.md2Header_m_SkinHeight_set)
    __swig_setmethods__["m_Framesize"] = _md2.md2Header_m_Framesize_set
    __swig_getmethods__["m_Framesize"] = _md2.md2Header_m_Framesize_get
    if _newclass:m_Framesize = _swig_property(_md2.md2Header_m_Framesize_get, _md2.md2Header_m_Framesize_set)
    __swig_setmethods__["m_NumSkins"] = _md2.md2Header_m_NumSkins_set
    __swig_getmethods__["m_NumSkins"] = _md2.md2Header_m_NumSkins_get
    if _newclass:m_NumSkins = _swig_property(_md2.md2Header_m_NumSkins_get, _md2.md2Header_m_NumSkins_set)
    __swig_setmethods__["m_NumVertices"] = _md2.md2Header_m_NumVertices_set
    __swig_getmethods__["m_NumVertices"] = _md2.md2Header_m_NumVertices_get
    if _newclass:m_NumVertices = _swig_property(_md2.md2Header_m_NumVertices_get, _md2.md2Header_m_NumVertices_set)
    __swig_setmethods__["m_NumTextureCoords"] = _md2.md2Header_m_NumTextureCoords_set
    __swig_getmethods__["m_NumTextureCoords"] = _md2.md2Header_m_NumTextureCoords_get
    if _newclass:m_NumTextureCoords = _swig_property(_md2.md2Header_m_NumTextureCoords_get, _md2.md2Header_m_NumTextureCoords_set)
    __swig_setmethods__["m_NumTriangles"] = _md2.md2Header_m_NumTriangles_set
    __swig_getmethods__["m_NumTriangles"] = _md2.md2Header_m_NumTriangles_get
    if _newclass:m_NumTriangles = _swig_property(_md2.md2Header_m_NumTriangles_get, _md2.md2Header_m_NumTriangles_set)
    __swig_setmethods__["m_NumGLCommands"] = _md2.md2Header_m_NumGLCommands_set
    __swig_getmethods__["m_NumGLCommands"] = _md2.md2Header_m_NumGLCommands_get
    if _newclass:m_NumGLCommands = _swig_property(_md2.md2Header_m_NumGLCommands_get, _md2.md2Header_m_NumGLCommands_set)
    __swig_setmethods__["m_NumFrames"] = _md2.md2Header_m_NumFrames_set
    __swig_getmethods__["m_NumFrames"] = _md2.md2Header_m_NumFrames_get
    if _newclass:m_NumFrames = _swig_property(_md2.md2Header_m_NumFrames_get, _md2.md2Header_m_NumFrames_set)
    __swig_setmethods__["m_OffsetToSkins"] = _md2.md2Header_m_OffsetToSkins_set
    __swig_getmethods__["m_OffsetToSkins"] = _md2.md2Header_m_OffsetToSkins_get
    if _newclass:m_OffsetToSkins = _swig_property(_md2.md2Header_m_OffsetToSkins_get, _md2.md2Header_m_OffsetToSkins_set)
    __swig_setmethods__["m_OffsetToTextureCoords"] = _md2.md2Header_m_OffsetToTextureCoords_set
    __swig_getmethods__["m_OffsetToTextureCoords"] = _md2.md2Header_m_OffsetToTextureCoords_get
    if _newclass:m_OffsetToTextureCoords = _swig_property(_md2.md2Header_m_OffsetToTextureCoords_get, _md2.md2Header_m_OffsetToTextureCoords_set)
    __swig_setmethods__["m_OffsetToTriangles"] = _md2.md2Header_m_OffsetToTriangles_set
    __swig_getmethods__["m_OffsetToTriangles"] = _md2.md2Header_m_OffsetToTriangles_get
    if _newclass:m_OffsetToTriangles = _swig_property(_md2.md2Header_m_OffsetToTriangles_get, _md2.md2Header_m_OffsetToTriangles_set)
    __swig_setmethods__["m_OffsetToFrames"] = _md2.md2Header_m_OffsetToFrames_set
    __swig_getmethods__["m_OffsetToFrames"] = _md2.md2Header_m_OffsetToFrames_get
    if _newclass:m_OffsetToFrames = _swig_property(_md2.md2Header_m_OffsetToFrames_get, _md2.md2Header_m_OffsetToFrames_set)
    __swig_setmethods__["m_OffsetToGLCommands"] = _md2.md2Header_m_OffsetToGLCommands_set
    __swig_getmethods__["m_OffsetToGLCommands"] = _md2.md2Header_m_OffsetToGLCommands_get
    if _newclass:m_OffsetToGLCommands = _swig_property(_md2.md2Header_m_OffsetToGLCommands_get, _md2.md2Header_m_OffsetToGLCommands_set)
    __swig_setmethods__["m_OffsetToEOF"] = _md2.md2Header_m_OffsetToEOF_set
    __swig_getmethods__["m_OffsetToEOF"] = _md2.md2Header_m_OffsetToEOF_get
    if _newclass:m_OffsetToEOF = _swig_property(_md2.md2Header_m_OffsetToEOF_get, _md2.md2Header_m_OffsetToEOF_set)
    def __init__(self, *args): 
        this = _md2.new_md2Header(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _md2.delete_md2Header
    __del__ = lambda self : None;
md2Header_swigregister = _md2.md2Header_swigregister
md2Header_swigregister(md2Header)

class md2Skin(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, md2Skin, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, md2Skin, name)
    __repr__ = _swig_repr
    __swig_setmethods__["m_Name"] = _md2.md2Skin_m_Name_set
    __swig_getmethods__["m_Name"] = _md2.md2Skin_m_Name_get
    if _newclass:m_Name = _swig_property(_md2.md2Skin_m_Name_get, _md2.md2Skin_m_Name_set)
    def __init__(self, *args): 
        this = _md2.new_md2Skin(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _md2.delete_md2Skin
    __del__ = lambda self : None;
md2Skin_swigregister = _md2.md2Skin_swigregister
md2Skin_swigregister(md2Skin)

class md2TextureCoord(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, md2TextureCoord, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, md2TextureCoord, name)
    __repr__ = _swig_repr
    __swig_setmethods__["u"] = _md2.md2TextureCoord_u_set
    __swig_getmethods__["u"] = _md2.md2TextureCoord_u_get
    if _newclass:u = _swig_property(_md2.md2TextureCoord_u_get, _md2.md2TextureCoord_u_set)
    __swig_setmethods__["v"] = _md2.md2TextureCoord_v_set
    __swig_getmethods__["v"] = _md2.md2TextureCoord_v_get
    if _newclass:v = _swig_property(_md2.md2TextureCoord_v_get, _md2.md2TextureCoord_v_set)
    def __init__(self, *args): 
        this = _md2.new_md2TextureCoord(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _md2.delete_md2TextureCoord
    __del__ = lambda self : None;
md2TextureCoord_swigregister = _md2.md2TextureCoord_swigregister
md2TextureCoord_swigregister(md2TextureCoord)

class md2Triangle(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, md2Triangle, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, md2Triangle, name)
    __repr__ = _swig_repr
    __swig_setmethods__["m_Vertex"] = _md2.md2Triangle_m_Vertex_set
    __swig_getmethods__["m_Vertex"] = _md2.md2Triangle_m_Vertex_get
    if _newclass:m_Vertex = _swig_property(_md2.md2Triangle_m_Vertex_get, _md2.md2Triangle_m_Vertex_set)
    __swig_setmethods__["m_UV"] = _md2.md2Triangle_m_UV_set
    __swig_getmethods__["m_UV"] = _md2.md2Triangle_m_UV_get
    if _newclass:m_UV = _swig_property(_md2.md2Triangle_m_UV_get, _md2.md2Triangle_m_UV_set)
    def __init__(self, *args): 
        this = _md2.new_md2Triangle(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _md2.delete_md2Triangle
    __del__ = lambda self : None;
md2Triangle_swigregister = _md2.md2Triangle_swigregister
md2Triangle_swigregister(md2Triangle)

class md2Vertex(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, md2Vertex, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, md2Vertex, name)
    __repr__ = _swig_repr
    __swig_setmethods__["m_Values"] = _md2.md2Vertex_m_Values_set
    __swig_getmethods__["m_Values"] = _md2.md2Vertex_m_Values_get
    if _newclass:m_Values = _swig_property(_md2.md2Vertex_m_Values_get, _md2.md2Vertex_m_Values_set)
    __swig_setmethods__["m_NormalIndex"] = _md2.md2Vertex_m_NormalIndex_set
    __swig_getmethods__["m_NormalIndex"] = _md2.md2Vertex_m_NormalIndex_get
    if _newclass:m_NormalIndex = _swig_property(_md2.md2Vertex_m_NormalIndex_get, _md2.md2Vertex_m_NormalIndex_set)
    def __init__(self, *args): 
        this = _md2.new_md2Vertex(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _md2.delete_md2Vertex
    __del__ = lambda self : None;
md2Vertex_swigregister = _md2.md2Vertex_swigregister
md2Vertex_swigregister(md2Vertex)

class md2Frame(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, md2Frame, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, md2Frame, name)
    __repr__ = _swig_repr
    __swig_destroy__ = _md2.delete_md2Frame
    __del__ = lambda self : None;
    __swig_setmethods__["m_Scale"] = _md2.md2Frame_m_Scale_set
    __swig_getmethods__["m_Scale"] = _md2.md2Frame_m_Scale_get
    if _newclass:m_Scale = _swig_property(_md2.md2Frame_m_Scale_get, _md2.md2Frame_m_Scale_set)
    __swig_setmethods__["m_Translate"] = _md2.md2Frame_m_Translate_set
    __swig_getmethods__["m_Translate"] = _md2.md2Frame_m_Translate_get
    if _newclass:m_Translate = _swig_property(_md2.md2Frame_m_Translate_get, _md2.md2Frame_m_Translate_set)
    __swig_setmethods__["m_Name"] = _md2.md2Frame_m_Name_set
    __swig_getmethods__["m_Name"] = _md2.md2Frame_m_Name_get
    if _newclass:m_Name = _swig_property(_md2.md2Frame_m_Name_get, _md2.md2Frame_m_Name_set)
    __swig_setmethods__["m_Verts"] = _md2.md2Frame_m_Verts_set
    __swig_getmethods__["m_Verts"] = _md2.md2Frame_m_Verts_get
    if _newclass:m_Verts = _swig_property(_md2.md2Frame_m_Verts_get, _md2.md2Frame_m_Verts_set)
    __swig_setmethods__["m_DisplayList"] = _md2.md2Frame_m_DisplayList_set
    __swig_getmethods__["m_DisplayList"] = _md2.md2Frame_m_DisplayList_get
    if _newclass:m_DisplayList = _swig_property(_md2.md2Frame_m_DisplayList_get, _md2.md2Frame_m_DisplayList_set)
    def __init__(self, *args): 
        this = _md2.new_md2Frame(*args)
        try: self.this.append(this)
        except: self.this = this
md2Frame_swigregister = _md2.md2Frame_swigregister
md2Frame_swigregister(md2Frame)

class md2GLCommand(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, md2GLCommand, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, md2GLCommand, name)
    __repr__ = _swig_repr
    __swig_setmethods__["m_U"] = _md2.md2GLCommand_m_U_set
    __swig_getmethods__["m_U"] = _md2.md2GLCommand_m_U_get
    if _newclass:m_U = _swig_property(_md2.md2GLCommand_m_U_get, _md2.md2GLCommand_m_U_set)
    __swig_setmethods__["m_V"] = _md2.md2GLCommand_m_V_set
    __swig_getmethods__["m_V"] = _md2.md2GLCommand_m_V_get
    if _newclass:m_V = _swig_property(_md2.md2GLCommand_m_V_get, _md2.md2GLCommand_m_V_set)
    __swig_setmethods__["m_VertexIndex"] = _md2.md2GLCommand_m_VertexIndex_set
    __swig_getmethods__["m_VertexIndex"] = _md2.md2GLCommand_m_VertexIndex_get
    if _newclass:m_VertexIndex = _swig_property(_md2.md2GLCommand_m_VertexIndex_get, _md2.md2GLCommand_m_VertexIndex_set)
    def __init__(self, *args): 
        this = _md2.new_md2GLCommand(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _md2.delete_md2GLCommand
    __del__ = lambda self : None;
md2GLCommand_swigregister = _md2.md2GLCommand_swigregister
md2GLCommand_swigregister(md2GLCommand)

class md2AnimationRange(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, md2AnimationRange, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, md2AnimationRange, name)
    __repr__ = _swig_repr
    __swig_setmethods__["m_StartFrame"] = _md2.md2AnimationRange_m_StartFrame_set
    __swig_getmethods__["m_StartFrame"] = _md2.md2AnimationRange_m_StartFrame_get
    if _newclass:m_StartFrame = _swig_property(_md2.md2AnimationRange_m_StartFrame_get, _md2.md2AnimationRange_m_StartFrame_set)
    __swig_setmethods__["m_EndFrame"] = _md2.md2AnimationRange_m_EndFrame_set
    __swig_getmethods__["m_EndFrame"] = _md2.md2AnimationRange_m_EndFrame_get
    if _newclass:m_EndFrame = _swig_property(_md2.md2AnimationRange_m_EndFrame_get, _md2.md2AnimationRange_m_EndFrame_set)
    def __init__(self, *args): 
        this = _md2.new_md2AnimationRange(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _md2.delete_md2AnimationRange
    __del__ = lambda self : None;
md2AnimationRange_swigregister = _md2.md2AnimationRange_swigregister
md2AnimationRange_swigregister(md2AnimationRange)

MD2MODEL_VERSION = _md2.MD2MODEL_VERSION
MD2MODEL_VERSION_ID = _md2.MD2MODEL_VERSION_ID
class md2Model(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, md2Model, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, md2Model, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _md2.new_md2Model(*args)
        try: self.this.append(this)
        except: self.this = this
    def CreateAnimationRanges(*args): return _md2.md2Model_CreateAnimationRanges(*args)
    def LoadTexture(*args): return _md2.md2Model_LoadTexture(*args)
    def SetTexture(*args): return _md2.md2Model_SetTexture(*args)
    def SetFromExistingTexture(*args): return _md2.md2Model_SetFromExistingTexture(*args)
    def DrawImmediate(*args): return _md2.md2Model_DrawImmediate(*args)
    def DrawImmediateWithInterpolation(*args): return _md2.md2Model_DrawImmediateWithInterpolation(*args)
    def DrawGLCommandsWithInterpolation(*args): return _md2.md2Model_DrawGLCommandsWithInterpolation(*args)
    def SetModel(*args): return _md2.md2Model_SetModel(*args)
    def SetScale(*args): return _md2.md2Model_SetScale(*args)
    def AccessAnimationRanges(*args): return _md2.md2Model_AccessAnimationRanges(*args)
    def Success(*args): return _md2.md2Model_Success(*args)
    __swig_destroy__ = _md2.delete_md2Model
    __del__ = lambda self : None;
md2Model_swigregister = _md2.md2Model_swigregister
md2Model_swigregister(md2Model)

MD2OBJECT_ANIMATION_IMMEDIATE = _md2.MD2OBJECT_ANIMATION_IMMEDIATE
MD2OBJECT_ANIMATION_GLCOMMANDS = _md2.MD2OBJECT_ANIMATION_GLCOMMANDS
class md2Object(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, md2Object, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, md2Object, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _md2.new_md2Object(*args)
        try: self.this.append(this)
        except: self.this = this
    def SetModel(*args): return _md2.md2Object_SetModel(*args)
    def AccessModel(*args): return _md2.md2Object_AccessModel(*args)
    def SetScale(*args): return _md2.md2Object_SetScale(*args)
    def Scale(*args): return _md2.md2Object_Scale(*args)
    def SetAnimation(*args): return _md2.md2Object_SetAnimation(*args)
    def GetCurrentAnimation(*args): return _md2.md2Object_GetCurrentAnimation(*args)
    def SetRenderMode(*args): return _md2.md2Object_SetRenderMode(*args)
    def GetRenderMode(*args): return _md2.md2Object_GetRenderMode(*args)
    def Animate(*args): return _md2.md2Object_Animate(*args)
    def DrawInterpolated(*args): return _md2.md2Object_DrawInterpolated(*args)
    def PrintAnimations(*args): return _md2.md2Object_PrintAnimations(*args)
    __swig_destroy__ = _md2.delete_md2Object
    __del__ = lambda self : None;
md2Object_swigregister = _md2.md2Object_swigregister
md2Object_swigregister(md2Object)


