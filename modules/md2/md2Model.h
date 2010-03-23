/*
 * This file is part of La Vida
 * Copyright (C) 2009/10 Mike Hibbert
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
 */

// Credit for this should go to David Henry as its based heavily on his excellent tutorial
// thanks David Henry for the great info. All I did really is write this using his info and
// used my own vector classes and texture loaders etc.

#ifndef MD2MODEL_H
#define MD2MODEL_H

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <GL/gl.h>
#include <GL/glu.h>
#include <sdl.h>

// #include "../sdlApp/Vector3d.h"
// #include "../OpenGL/oglTexture.h"
// typedefs / enums / structs
// Md2 header

using std::map;
using std::string;
using std::vector;

typedef GLfloat md2Vector3d[3];

typedef struct
{
  int m_ID;          // Model type ID should be "IDP2"
  int m_Version;        // Md2 format version, should be 8

  int m_SkinWidth;      // Texture width
  int m_SkinHeight;     // Texture height

  int m_Framesize;      // Size of a frame, in bytes

  int m_NumSkins;      // Number of skins
  int m_NumVertices;   // Number of vertices per frame
  int m_NumTextureCoords;         // Number of texture coords
  int m_NumTriangles;       // Number of triangles
  int m_NumGLCommands;     // Number of OpenGL commands
  int m_NumFrames;     // Number of frames

  int m_OffsetToSkins;   // offset to skin data
  int m_OffsetToTextureCoords;      // offset to texture coords
  int m_OffsetToTriangles;    // offset to triangle data
  int m_OffsetToFrames;  // offset to frame data
  int m_OffsetToGLCommands;  // offset to OpenGL commands
  int m_OffsetToEOF;     // offset to the end of the file
}md2Header;

// Skin data
struct md2Skin
{
  char m_Name[64];  // Texture's filename
};

// Texture Coords.
struct md2TextureCoord
{
  short u;
  short v;
};

// Triangle data
struct md2Triangle
{
  unsigned short m_Vertex[3];  // Triangle's vertex indices
  unsigned short m_UV[3];      // Texture coords. indices
};

// Vertex data
struct md2Vertex
{
  unsigned char m_Values[3];         // Compressed vertex position
  unsigned char m_NormalIndex;  // Normal vector index
};

// Frame data
struct md2Frame
{
  ~md2Frame () { delete [] m_Verts; }

  md2Vector3d* m_Scale;        // Scale factors
  md2Vector3d* m_Translate;    // Translation vector
  char m_Name[16];       // Frame name
  struct md2Vertex* m_Verts;  // Frames's vertex list
  int m_DisplayList;
  GLint m_VBOID;
  GLint m_VBOTexID;
  GLint m_VBONormalsID;
};

struct md2GLCommand
{
  float m_U;    // U texture coord.
  float m_V;    // V texture coord.
  int m_VertexIndex;  // Vertex index
};

struct md2AnimationRange
{
  int m_StartFrame;  // first frame index
  int m_EndFrame;    // last frame index
  int m_FPS;
};

typedef map <string, md2AnimationRange> AnimationRange;

#define MD2MODEL_VERSION                  8
#define MD2MODEL_VERSION_ID             'I' + ('D'<<8) + ('P'<<16) + ('2'<<24)



// classes

class md2Model  {
  public:
    md2Model(string a_Filename);
    void CreateAnimationRanges();

    GLfloat* CalculateFaceNormal( GLfloat* v1, GLfloat* v2, GLfloat* v3 );
    void Draw(int a_Frame);

    void SetModel(md2Model * a_Model);

    void SetScale(GLfloat a_Scale);

    AnimationRange* AccessAnimationRanges() { return m_AnimationRanges; }

    bool Success() { return m_Success; }

    void SetAnimationRangeFPS( string a_Animation, float a_FPS ) {
      m_AnimationRanges[ a_Animation ].m_FPS = ( int ) a_FPS * 1000.0;
    }

    void CreateVBO(void);

    ~md2Model();
  protected:

    md2Model();

    bool m_Success;
    md2Header m_Header;
    md2Skin* m_Skins;
    md2TextureCoord* m_TextureCoords;
    md2Triangle* m_Triangles;
    GLint *m_VBOIDS;
    static md2Vector3d m_Normals[162];
    md2Frame* m_Frames;
    int m_FramesNum;
    int *m_GLCommands;
    GLfloat m_Scale;
    AnimationRange* m_AnimationRanges;

};

void InitMD2(void);

#endif
