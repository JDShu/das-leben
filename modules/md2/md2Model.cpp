/*
 * This file is part of La Vida
 * Copyright (C) 2009/2010 Mike Hibbert
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
#include <Python.h>
#include <GL/gl.h>
#include <iostream>
#include <fstream>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>

#include "md2Model.h"

using std::cout;
using std::endl;


bool FileExists(string strFilename) {
  struct stat stFileInfo;
  bool blnReturn;
  int intStat;

  // Attempt to get the file attributes
  intStat = stat(strFilename.c_str(),&stFileInfo);
  if(intStat == 0) {
    // We were able to get the file attributes
    // so the file obviously exists.
    blnReturn = true;
    //cout << "File " << strFilename << " found " <<  endl;
    } else {
    // We were not able to get the file attributes.
    // This may mean that we don't have permission to
    // access the folder which contains this file. If you
    // need to do that level of checking, lookup the
    // return values of stat which will give you
    // more details on why stat failed.
    blnReturn = false;
  }

  return(blnReturn);
}



md2Model::md2Model(string a_Filename)
{
  std::ifstream l_File;
  if(FileExists(a_Filename))  {
    l_File.open( a_Filename.c_str(), std::ios::binary );
  } else {
    cout << "File does not exist: " << a_Filename << endl;
    return;
  }

  m_Success = false;

  if( l_File.fail() ) {
    cout << "Unable to load md2 model: " << a_Filename << " Error: " << (l_File.rdstate() & std::ios::badbit) << endl;
    return;
  } else {
    cout << "Loading md2 model: " << a_Filename << endl;
    l_File.read( (char *)&m_Header, sizeof(md2Header) );

  }
  int l_ExpectedID = MD2MODEL_VERSION_ID;

  if( m_Header.m_ID != l_ExpectedID ) {
    cout << a_Filename << " is not a valid MD2 file: ID was " << m_Header.m_ID << endl;
  }

  if( m_Header.m_Version != MD2MODEL_VERSION )  {
    cout << a_Filename << " is the wrong version, must be version " << MD2MODEL_VERSION << " Version was " << m_Header.m_Version << endl;
  }

  m_Success = true;
  // now the header is loaded  we cal allocate the memory for the data in the file
  m_Skins = new md2Skin[ m_Header.m_NumSkins ];
  m_TextureCoords = new md2TextureCoord[ m_Header.m_NumTextureCoords ];
  m_Triangles = new md2Triangle[ m_Header.m_NumTriangles ];
  m_Frames = new md2Frame[ m_Header.m_NumFrames ];
  m_GLCommands = new int[ m_Header.m_NumGLCommands ];

  // now we load it all in starting with the skin names
  l_File.seekg( m_Header.m_OffsetToSkins, std::ios::beg );
  l_File.read( reinterpret_cast<char *>(m_Skins), sizeof( md2Skin ) * m_Header.m_NumSkins );

  // texture coords
  l_File.seekg( m_Header.m_OffsetToTextureCoords, std::ios::beg );
  l_File.read( reinterpret_cast<char *>(m_TextureCoords),
                      sizeof( md2TextureCoord ) * m_Header.m_NumTextureCoords );

  // triangles
  l_File.seekg( m_Header.m_OffsetToTriangles, std::ios::beg );
  l_File.read( reinterpret_cast<char *>(m_Triangles)
                    , sizeof( md2Triangle ) * m_Header.m_NumTriangles );

  // frames
  l_File.seekg( m_Header.m_OffsetToFrames, std::ios::beg );
  GLfloat l_Temp[3];
  int i;
  for(i = 0; i < m_Header.m_NumFrames; i++) {
    // add a new memory area fro this frames verts

    m_Frames[i].m_Verts = new md2Vertex[ m_Header.m_NumVertices ];
    m_Frames[i].m_DisplayList = 0;

    l_File.read( reinterpret_cast<char *>(&l_Temp), sizeof(GLfloat) * 3);
    m_Frames[i].m_Scale = Vector3d( l_Temp[0], l_Temp[1], l_Temp[2] );

    l_File.read( reinterpret_cast<char *>(&l_Temp), sizeof(GLfloat) * 3);
    m_Frames[i].m_Translate = Vector3d( l_Temp[0], l_Temp[1], l_Temp[2] );

    l_File.read( reinterpret_cast<char *>(&m_Frames[i].m_Name), sizeof(char) * 16);
    l_File.read( reinterpret_cast<char *>(m_Frames[i].m_Verts), sizeof(md2Vertex) * m_Header.m_NumVertices);
  }

  // load in the GL commands
  l_File.seekg( m_Header.m_OffsetToGLCommands, std::ios::beg );
  l_File.read( reinterpret_cast<char *>(m_GLCommands), sizeof(int) * m_Header.m_NumGLCommands );

  l_File.close();

  CreateAnimationRanges();
}

void md2Model::CreateAnimationRanges()
{
  string l_CurrentAnimation;
  md2AnimationRange l_AnimationRange = { 0, 0};

  for(int i = 0; i < m_Header.m_NumFrames; i++) {
    string l_FrameName = m_Frames[ i ].m_Name;
    string l_AnimationName;

    string::size_type l_Lenght = l_FrameName.find_first_of("0123456789");
    if((l_Lenght == l_FrameName.length() - 3) && (l_FrameName[ l_Lenght ] != '0'))  {
      l_Lenght++;
    }

    if(l_CurrentAnimation != l_AnimationName) {
      if(i > 0) {
        m_AnimationRanges.insert(AnimationRange::value_type(l_CurrentAnimation, l_AnimationRange));
      }

      l_AnimationRange.m_StartFrame = i;
      l_AnimationRange.m_EndFrame = i;

      l_CurrentAnimation = l_AnimationName;
    } else {
      l_AnimationRange.m_EndFrame = i;
    }
  }
  // and finally the last one
  m_AnimationRanges.insert(AnimationRange::value_type(l_CurrentAnimation, l_AnimationRange));
}

bool md2Model::LoadTexture(string a_Filename)
{
  bool l_ReturnVal = false;

  oglTexture* l_Texture = new oglTexture();
  if(l_Texture->Load(a_Filename, OGL_TEXTURE_DESTROY_IMAGEDATA) )  {
    l_ReturnVal = true;
    m_Textures.insert( SkinMap::value_type( a_Filename, l_Texture ));
  } else {
    cout << "Cant load texture " << a_Filename << endl;
  }
  SetTexture(a_Filename);
  return l_ReturnVal;
}

void md2Model::SetTexture(string a_Filename)
{
  SkinMap::iterator l_Itor;
  l_Itor = m_Textures.find(a_Filename);
  if(l_Itor != m_Textures.end() )  {
    m_Texture = l_Itor->second;
  } else {
    m_Texture = NULL;
  }
}

void md2Model::SetFromExistingTexture(
  string a_Filename
, oglTexture* a_Texture
)
{
  m_Textures.insert( SkinMap::value_type( a_Filename, a_Texture ));
  SetTexture(a_Filename);
}

void md2Model::DrawImmediate(
  int a_Frame
)
{
  int l_MaximumFrames = m_Header.m_NumFrames - 1;

  if(m_Texture) {
    glBindTexture( GL_TEXTURE_2D, m_Texture->GetTextureID() );
  }
  md2Frame* l_Frame = &m_Frames[ a_Frame ];

  if(l_Frame->m_DisplayList == 0) {
    //l_Frame->m_DisplayList = glGenLists(1);
    //cout << "Display list is " << l_Frame->m_DisplayList << endl;
    //glNewList(l_Frame->m_DisplayList, GL_COMPILE_AND_EXECUTE);
      glBegin( GL_TRIANGLES );
        for(int i = 0; i < m_Header.m_NumTriangles; ++i)  {
          for(int j = 0; j < 3; j++)  {
            md2Vertex* l_Vertex = &l_Frame->m_Verts[ m_Triangles[i].m_Vertex[j] ];

            md2TextureCoord* l_TextureCoord = &m_TextureCoords[ m_Triangles[i].m_UV[j] ];
            GLfloat l_U = static_cast<GLfloat>(l_TextureCoord->u) / m_Header.m_SkinWidth;
            GLfloat l_V = static_cast<GLfloat>(l_TextureCoord->v) / m_Header.m_SkinHeight;

            glTexCoord2f( l_U, 1.0 - l_V );

            glNormal3fv(m_Normals[ l_Vertex->m_NormalIndex ] );

            md2Vector3d l_Vector;
            l_Vector[0] = (l_Frame->m_Scale.GetX()  * l_Vertex->m_Values[0]  + l_Frame->m_Translate.GetX()) * m_Scale;
            l_Vector[1] = (l_Frame->m_Scale.GetY()  * l_Vertex->m_Values[1]  + l_Frame->m_Translate.GetY()) * m_Scale;
            l_Vector[2] = (l_Frame->m_Scale.GetZ()  * l_Vertex->m_Values[2]  + l_Frame->m_Translate.GetZ()) * m_Scale;

            /*l_Vector[0] = (GLfloat) l_Vertex->m_Values[0];
            l_Vector[1] = (GLfloat) l_Vertex->m_Values[1];
            l_Vector[2] = (GLfloat) l_Vertex->m_Values[2];*/

            glVertex3fv( l_Vector );
          }
        }
      glEnd();
    //glEndList();
  } else {
    glCallList(l_Frame->m_DisplayList);
  }
}

void md2Model::DrawImmediateWithInterpolation(
  int a_FromFrame
, int a_ToFrame
, GLfloat a_Interpolation
)
{
  int l_MaximumFrames = m_Header.m_NumFrames - 1;

  if(m_Texture) {
    glBindTexture( GL_TEXTURE_2D, m_Texture->GetTextureID() );
  }

  glBegin( GL_TRIANGLES );
  for(int i = 0; i < m_Header.m_NumTriangles; ++i)  {
    for(int j = 0; j < 3; j++)  {
      md2Frame* l_FromFrame = &m_Frames[ a_FromFrame ];
      md2Frame* l_ToFrame = &m_Frames[ a_ToFrame ];

      md2Vertex* l_FromVertex = &l_FromFrame->m_Verts[ m_Triangles[i].m_Vertex[j] ];
      md2Vertex* l_ToVertex = &l_ToFrame->m_Verts[ m_Triangles[i].m_Vertex[j] ];

      md2TextureCoord* l_TextureCoord = &m_TextureCoords[ m_Triangles[i].m_UV[j] ];

      GLfloat l_U = static_cast<GLfloat>(l_TextureCoord->u) / m_Header.m_SkinWidth;
      GLfloat l_V = static_cast<GLfloat>(l_TextureCoord->v) / m_Header.m_SkinHeight;

      glTexCoord2f( l_U, 1.0 - l_V );

      GLfloat *l_FromNormal = m_Normals[ l_FromVertex->m_NormalIndex ];
      GLfloat *l_ToNormal = m_Normals[ l_ToVertex->m_NormalIndex ];

      md2Vector3d l_Normal;
      l_Normal[0] = l_FromNormal[0] + a_Interpolation * ( l_ToNormal[0] - l_FromNormal[0] );
      l_Normal[1] = l_FromNormal[1] + a_Interpolation * ( l_ToNormal[1] - l_FromNormal[1] );
      l_Normal[2] = l_FromNormal[2] + a_Interpolation * ( l_ToNormal[2] - l_FromNormal[2] );

      glNormal3fv((const GLfloat *) &l_Normal );

      md2Vector3d l_FromVector;
      l_FromVector[0] = l_FromFrame->m_Scale.GetX() * l_FromVertex->m_Values[0] + l_FromFrame->m_Translate.GetX();
      l_FromVector[1] = l_FromFrame->m_Scale.GetY() * l_FromVertex->m_Values[1] + l_FromFrame->m_Translate.GetY();
      l_FromVector[2] = l_FromFrame->m_Scale.GetZ() * l_FromVertex->m_Values[2] + l_FromFrame->m_Translate.GetZ();

      md2Vector3d l_ToVector;
      l_ToVector[0] = l_ToFrame->m_Scale.GetX() * l_ToVertex->m_Values[0] + l_ToFrame->m_Translate.GetX();
      l_ToVector[1] = l_ToFrame->m_Scale.GetY() * l_ToVertex->m_Values[1] + l_ToFrame->m_Translate.GetY();
      l_ToVector[2] = l_ToFrame->m_Scale.GetZ() * l_ToVertex->m_Values[2] + l_ToFrame->m_Translate.GetZ();

      md2Vector3d l_Vector;
      l_Vector[0] = (l_FromVector[0] + a_Interpolation *( l_ToVector[0] - l_FromVector[0])) * m_Scale;
      l_Vector[1] = (l_FromVector[1] + a_Interpolation *( l_ToVector[1] - l_FromVector[1])) * m_Scale;
      l_Vector[2] = (l_FromVector[2] + a_Interpolation *( l_ToVector[2] - l_FromVector[2])) * m_Scale;

      glVertex3fv( l_Vector );
    }
  }
  glEnd();
}

void md2Model::DrawGLCommandsWithInterpolation(
  int a_FromFrame
, int a_ToFrame
, GLfloat a_Interpolation
)
{
  int l_MaximumFrames = m_Header.m_NumFrames - 1;

  if(m_Texture) {
    glBindTexture( GL_TEXTURE_2D, m_Texture->GetTextureID() );
  }
  int *l_GLCommands = m_GLCommands;
  int i = 0;
  while((i = *(l_GLCommands++)) != 0) {

    if( i < 0 ) {
      glBegin(GL_TRIANGLE_FAN);
      i = -i;
    } else {
      glBegin(GL_TRIANGLE_STRIP);
    }

    for( ; i > 0; --i, l_GLCommands += 3)  {  // weird way of incrementing!
      md2GLCommand* l_GLCommand = reinterpret_cast<md2GLCommand *>(l_GLCommands);
      md2Frame* l_FromFrame = &m_Frames[ a_FromFrame ];
      md2Frame* l_ToFrame = &m_Frames[ a_ToFrame ];

      md2Vertex* l_FromVertex = &l_FromFrame->m_Verts[ l_GLCommand->m_VertexIndex ];
      md2Vertex* l_ToVertex = &l_ToFrame->m_Verts[ l_GLCommand->m_VertexIndex ];



      glTexCoord2f( l_GLCommand->m_U, 1.0 - l_GLCommand->m_V );

      GLfloat *l_FromNormal = m_Normals[ l_FromVertex->m_NormalIndex ];
      GLfloat *l_ToNormal = m_Normals[ l_ToVertex->m_NormalIndex ];

      md2Vector3d l_Normal;
      l_Normal[0] = l_FromNormal[0] + a_Interpolation * ( l_ToNormal[0] - l_FromNormal[0] );
      l_Normal[1] = l_FromNormal[1] + a_Interpolation * ( l_ToNormal[1] - l_FromNormal[1] );
      l_Normal[2] = l_FromNormal[2] + a_Interpolation * ( l_ToNormal[2] - l_FromNormal[2] );

      glNormal3fv((const GLfloat *) &l_Normal );

      md2Vector3d l_FromVector;
      l_FromVector[0] = l_FromFrame->m_Scale.GetX() * l_FromVertex->m_Values[0] + l_FromFrame->m_Translate.GetX();
      l_FromVector[1] = l_FromFrame->m_Scale.GetY() * l_FromVertex->m_Values[1] + l_FromFrame->m_Translate.GetY();
      l_FromVector[2] = l_FromFrame->m_Scale.GetZ() * l_FromVertex->m_Values[2] + l_FromFrame->m_Translate.GetZ();

      md2Vector3d l_ToVector;
      l_ToVector[0] = l_ToFrame->m_Scale.GetX() * l_ToVertex->m_Values[0] + l_ToFrame->m_Translate.GetX();
      l_ToVector[1] = l_ToFrame->m_Scale.GetY() * l_ToVertex->m_Values[1] + l_ToFrame->m_Translate.GetY();
      l_ToVector[2] = l_ToFrame->m_Scale.GetZ() * l_ToVertex->m_Values[2] + l_ToFrame->m_Translate.GetZ();

      md2Vector3d l_Vector;
      l_Vector[0] = (l_FromVector[0] + a_Interpolation *( l_ToVector[0] - l_FromVector[0])) * m_Scale;
      l_Vector[1] = (l_FromVector[1] + a_Interpolation *( l_ToVector[1] - l_FromVector[1])) * m_Scale;
      l_Vector[2] = (l_FromVector[2] + a_Interpolation *( l_ToVector[2] - l_FromVector[2])) * m_Scale;

      glVertex3fv( l_Vector );
    }
    glEnd();
  }

}


void md2Model::SetScale(GLfloat a_Scale)
{
  /*md2Frame* l_Frame = NULL;
  md2Vertex* l_Vertex = NULL;
  cout << "Model Frames : " << m_Header.m_NumFrames << endl;
  for(int i = 0; i < m_Header.m_NumFrames; i++) {
    l_Frame = &m_Frames[ i ];
    for(int j = 0; j < m_Header.m_NumTriangles; ++j)  {
      for(int k = 0; k < 3; k++)  {
        l_Vertex = &l_Frame->m_Verts[ m_Triangles[j].m_Vertex[k] ];

        l_Vertex->m_Values[0] = (l_Frame->m_Scale.GetX()  * l_Vertex->m_Values[0]  + l_Frame->m_Translate.GetX()) * m_Scale;
        l_Vertex->m_Values[1] = (l_Frame->m_Scale.GetY()  * l_Vertex->m_Values[1]  + l_Frame->m_Translate.GetY()) * m_Scale;
        l_Vertex->m_Values[2] = (l_Frame->m_Scale.GetZ()  * l_Vertex->m_Values[2]  + l_Frame->m_Translate.GetZ()) * m_Scale;
      }
    }
  }*/
  m_Scale = a_Scale;
}


void md2Model::SetModel(
  md2Model* a_Model
)
{

}

md2Model::~md2Model()
{
  delete [] m_Skins;
  delete [] m_TextureCoords;
  delete [] m_Triangles;
  delete [] m_Frames;
  delete [] m_GLCommands;
}
