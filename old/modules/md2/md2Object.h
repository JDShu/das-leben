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

#ifndef MD2OBJECT_H
#define MD2OBJECT_H

#include "md2Model.h"

enum MD2OBJECT_ANIMATION_TYPES  {
  MD2OBJECT_ANIMATION_IMMEDIATE = 0
, MD2OBJECT_ANIMATION_GLCOMMANDS
};

enum MD2OBJECT_RENDER_TYPE {
  MD2OBJECT_RENDER_DISPLAYLIST,
  MD2OBJECT_RENDER_VBO
};

class md2Object
{
  public:
    md2Object();
    md2Object(md2Model* a_Model);

    void SetModel(md2Model* a_Model);
    const md2Model* AccessModel() const { return m_Model; }

    void SetScale(GLfloat a_Scale)  { m_Scale = a_Scale; m_Model->SetScale( m_Scale ); }
    GLfloat Scale() const { return m_Scale; }

    void SetAnimation(string a_Animation);
    const string &GetCurrentAnimation() const { return m_CurrentAnimation; }

    void SetRenderMode(int a_RenderMode)  { m_RenderMode = a_RenderMode; }
    int GetRenderMode() { return m_RenderMode; }

    void Animate( int a_StartFrame, int a_EndFrame, GLfloat a_Percentage);
    void Animate( GLfloat a_Percentage );

    void DrawInterpolated(bool a_Animated);

    void PrintAnimations();

    ~md2Object();
  protected:
    md2Model *m_Model;
    int m_CurrentFrame;
    int m_NextFrame;
    float m_FPS;
    GLfloat m_Interpolation;
    GLfloat m_Percentage;
    GLfloat m_Scale;
    md2AnimationRange m_AnimationRange;
    string m_CurrentAnimation;
    int m_RenderMode;
};

#endif // MD2OBJECT_H
