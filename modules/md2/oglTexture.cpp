/*
 * This file is part of iSoccer
 * Copyright (C) 2008/9 Mike Hibbert
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

#include <iostream>
#include "oglTexture.h"

using std::cout;
using std::endl;
using std::string;

//=============================================================================
//
//
//
oglTexture::oglTexture()
//-----------------------------------------------------------------------------
{

}

//=============================================================================
//
//
//
bool oglTexture::Load(
  string a_Filename
, bool a_KeepImageData
)
//-----------------------------------------------------------------------------
{
  bool l_ReturnVal = true;

  SDL_Surface* l_ImageLoaded = IMG_Load(a_Filename.c_str());
  if( !l_ImageLoaded )  {
    cout << "Unable to load image " << a_Filename << endl;
    l_ReturnVal = false;
  }
  SDL_Surface* l_Image = SDL_DisplayFormatAlpha(l_ImageLoaded);
  SDL_FreeSurface( l_ImageLoaded );

  CreateFromSurface( l_Image, a_KeepImageData );
  return l_ReturnVal;
}


//=============================================================================
//
//
//
void oglTexture::CreateFromSurface(
  SDL_Surface* a_Surface
, bool a_KeepImageData
)
//-----------------------------------------------------------------------------
{
  m_ID = AddSurfaceToTexturePool( a_Surface );

  if(a_KeepImageData) {
    m_Image = a_Surface;
  } else {
      SDL_FreeSurface( a_Surface );
  }

}

//=============================================================================
//
//
//
GLuint oglTexture::AddSurfaceToTexturePool(
  SDL_Surface* a_Surface
)
//-----------------------------------------------------------------------------
{
  GLuint l_ReturnID = 0;
  glGenTextures(1, &l_ReturnID);
  glBindTexture(GL_TEXTURE_2D, l_ReturnID);

  if( a_Surface->format->BitsPerPixel == 32 || a_Surface->format->BitsPerPixel == 24 )  {
    /*glTexImage2D(
      GL_TEXTURE_2D
    , 0, 4
    , a_Surface->w
    , a_Surface->h
    , 0, GL_BGRA
    , GL_UNSIGNED_BYTE
    , a_Surface->pixels
    );*/
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, a_Surface->w, a_Surface->h, GL_BGRA, GL_UNSIGNED_BYTE, a_Surface->pixels);
  } else {
    glTexImage2D(
      GL_TEXTURE_2D
    , 0, 4
    , a_Surface->w
    , a_Surface->h
    , 0, GL_RGBA
    , GL_UNSIGNED_BYTE
    , a_Surface->pixels
    );
  }

  glTexParameteri(
    GL_TEXTURE_2D
  , GL_TEXTURE_MIN_FILTER
  , GL_LINEAR
  );

  glTexParameteri(
    GL_TEXTURE_2D
  , GL_TEXTURE_MAG_FILTER
  , GL_LINEAR
  );

  return l_ReturnID;
}

//=============================================================================
//
//
//
void oglTexture::UpdateTextureData()
//-----------------------------------------------------------------------------
{

}

//=============================================================================
//
//
//
void oglTexture::CreateAsRenderTexture(
  int a_Width,
  int a_Height
)
{
  m_Width = a_Width;
  m_Height = a_Height;
  glGenTextures(1, &m_ID);
	glBindTexture(GL_TEXTURE_2D, m_ID );
	glTexImage2D(	GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, m_Width, m_Height, 0,
					GL_DEPTH_COMPONENT, GL_UNSIGNED_BYTE, NULL);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
}
//=============================================================================
//
//
//
oglTexture::~oglTexture()
//-----------------------------------------------------------------------------
{
  if(m_Image) {
    SDL_FreeSurface( m_Image );
  }
}
