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

#ifndef ISOCCERTEXTURE_H_INCLUDED
#define ISOCCERTEXTURE_H_INCLUDED

#include <SDL/SDL.h>
#include <SDL/SDL_opengl.h>
#include <GL/glu.h>
#include <GL/gl.h>
#include <SDL/SDL_image.h>
#include <vector>
#include <iostream>

using std::string;
using std::vector;

const int OGL_TEXTURE_MAX = 512;
const bool OGL_TEXTURE_KEEP_IMAGEDATA = true;
const bool OGL_TEXTURE_DESTROY_IMAGEDATA = false;

class oglTexture {
  public:
    oglTexture();
    bool Load(
      string a_Filename
    , bool a_KeepImageData
    );

    GLuint AddSurfaceToTexturePool(SDL_Surface* a_Surface);

    void CreateFromSurface(
      SDL_Surface* a_Surface
    , bool a_KeepImageData
    );

    void UpdateTextureData();

    GLuint GetTextureID() { return m_ID; }

    void CreateAsRenderTexture(int a_Width, int a_Height);

    float GetWidth() { return m_Width; }
    float GetHeight() { return m_Height; }

    ~oglTexture();
  protected:
    GLuint m_ID;
    double m_Width;
    double m_Height;
    SDL_Surface* m_Image;
};

#endif // ISOCCERTEXTURE_H_INCLUDED
