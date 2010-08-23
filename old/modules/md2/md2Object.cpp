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

#include "md2Object.h"

#include <string.h>
#include <iostream>
#include <map>
#include <utility>

using namespace std;


md2Object::md2Object()
{
    m_CurrentFrame = 0;
    m_NextFrame = 0;
    m_Interpolation = 0.0;
    m_Percentage = 0.0;
    m_Scale = 1.0;
    m_FPS = 6.0;
    m_RenderMode = MD2OBJECT_RENDER_VBO;
}

md2Object::md2Object(
  md2Model* a_Model
)
{
  m_CurrentFrame = 0;
  m_NextFrame = 0;
  m_Interpolation = 0.0;
  m_Percentage = 0.0;
  m_Scale = 2.0;
  m_RenderMode = MD2OBJECT_ANIMATION_IMMEDIATE;
  SetModel(a_Model);
}

void md2Object::SetModel(
  md2Model* a_Model
)
{
  m_Model = a_Model;
  m_AnimationRange = m_Model->AccessAnimationRanges()->begin()->second;
  m_CurrentAnimation = m_Model->AccessAnimationRanges()->begin()->first;
  m_Model->SetScale( m_Scale );
}

void md2Object::Animate(
  int a_StartFrame
, int a_EndFrame
, int a_Ticks
)
{



}

void md2Object::Animate(
  GLfloat a_Percentage
)
{
  Animate( m_AnimationRange.m_StartFrame, m_AnimationRange.m_EndFrame, a_Percentage );
}

void md2Object::SetAnimation(
  string a_Animation
)
{
  AnimationRange::const_iterator l_Itor;
  l_Itor = m_Model->AccessAnimationRanges()->find( a_Animation );

  if( l_Itor != m_Model->AccessAnimationRanges()->end() ) {
    m_AnimationRange = l_Itor->second;
    m_CurrentAnimation = a_Animation;
  }
}

void md2Object::DrawInterpolated(
  bool a_Animated
)
{
  //glPushMatrix();
  // put the model the right way up for OpenGL


  m_Model->SetScale( m_Scale );

  //glPushAttrib (GL_POLYGON_BIT);
  //glFrontFace (GL_CW);

  //m_Model->DrawImmediateWithInterpolation( 0, 0, m_Interpolation );
  //m_Model->DrawGLCommandsWithInterpolation( m_CurrentFrame, m_NextFrame, m_Interpolation );
  m_Model->DrawImmediate(0);
  //glPopAttrib();
  //glPopMatrix();

  if(a_Animated)  {
    m_Interpolation += m_Percentage;
  }
}

void md2Object::PrintAnimations()   {
    AnimationRange::iterator iter = m_Model->AccessAnimationRanges()->begin();
    cout << "======== ANIMATION RANGES ===========" << endl;
    for(;iter != m_Model->AccessAnimationRanges()->end(); iter++)   {
        cout << (*iter).first << endl;
    }
}

md2Object::~md2Object()
{
  //dtor
}
