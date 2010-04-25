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
#include <math.h>
#include <cmath>
#include <limits>

#include "Vector3d.h"
#include "Angle.h"

float const m_pi = 2 * acos(0.0);

using namespace std;

Vector3d::Vector3d()
{
    m_Values[0] = 0;
    m_Values[1] = 0;
    m_Values[2] = 0;
    m_Values[3] = 1;
}

Vector3d::Vector3d(
  float x
, float y
, float z
)
{
    m_Values[0] = x;
    m_Values[1] = y;
    m_Values[2] = z;
    m_Values[3] = 1;
}

Vector3d::Vector3d(
  float x
, float y
, float z
, float w
)
{
    m_Values[0] = x;
    m_Values[1] = y;
    m_Values[2] = z;
    m_Values[3] = w;
}

Vector3d& Vector3d::operator=(const Vector3d &rhs)
{
    if(this != &rhs)    {
        m_Values[0] = rhs.m_Values[0];
        m_Values[1] = rhs.m_Values[1];
        m_Values[2] = rhs.m_Values[2];
        m_Values[3] = rhs.m_Values[3];
    }

    return *this;
}

void Vector3d::SetVectorFromAngles(
  Angle* a_AngleY
, Angle* a_AngleX
, float a_Length
)
{
  m_Values[ VECTOR3D_X_COORD ] = cos(a_AngleY->InRadians());
  m_Values[ VECTOR3D_Z_COORD ] = sin(a_AngleY->InRadians());

  m_Values[ VECTOR3D_Y_COORD ] = cos(a_AngleX->InRadians());
  m_Values[ VECTOR3D_W_COORD ] = 1.0;

  for(int i = 0; i < VECTOR3D_W_COORD; i++) {
    m_Values[i] *= a_Length;
  }
}

float& Vector3d::operator[](const int a_Index)
{
    return m_Values[a_Index];
}

float* Vector3d::Access()
{
    return m_Values;
}

Vector3d& Vector3d::operator+=(const Vector3d &rhs)
{

    m_Values[0] += rhs.m_Values[0];
    m_Values[1] += rhs.m_Values[1];
    m_Values[2] += rhs.m_Values[2];
    m_Values[3] += rhs.m_Values[3];

    return *this;
}

const Vector3d Vector3d::operator+(const Vector3d &rhs) const
{
    Vector3d result = *this;
    result += rhs;

    return result;
}

Vector3d& Vector3d::operator-=(const Vector3d &rhs)
{

    m_Values[0] -= rhs.m_Values[0];
    m_Values[1] -= rhs.m_Values[1];
    m_Values[2] -= rhs.m_Values[2];
    m_Values[3] -= rhs.m_Values[3];

    return *this;
}

const Vector3d Vector3d::operator-(const Vector3d &rhs) const
{
    Vector3d result = *this;
    result -= rhs;

    return result;
}

Vector3d& Vector3d::operator/=(const Vector3d &rhs)
{

    m_Values[0] /= rhs.m_Values[0];
    m_Values[1] /= rhs.m_Values[1];
    m_Values[2] /= rhs.m_Values[2];
    m_Values[3] /= rhs.m_Values[3];

    return *this;
}

Vector3d& Vector3d::operator/=(const float rhs)
{

    m_Values[0] /= rhs;
    m_Values[1] /= rhs;
    m_Values[2] /= rhs;
    m_Values[3] /= rhs;

    return *this;
}

const Vector3d Vector3d::operator/(const Vector3d &rhs) const
{
    Vector3d result = *this;
    result /= rhs;

    return result;
}

const Vector3d Vector3d::operator/(const float rhs) const
{
    Vector3d result = *this;
    result /= rhs;

    return result;
}

void Vector3d::PrintMe()
{
    cout << "x = " << m_Values[0] << endl;
    cout << "y = " << m_Values[1] << endl;
    cout << "z = " << m_Values[2] << endl;
    cout << "lenght = " << Length() << endl;

    cout << endl;


}

const float Vector3d::Length()
{
    float lenght_squared;
    lenght_squared = m_Values[0] * m_Values[0];
    lenght_squared += m_Values[1] * m_Values[1];
    lenght_squared += m_Values[2] * m_Values[2];

    return sqrt(lenght_squared);
}

const float Vector3d::LengthSquared()
{
    float lenght_squared;
    lenght_squared = m_Values[0] * m_Values[0];
    lenght_squared += m_Values[1] * m_Values[1];
    lenght_squared += m_Values[2] * m_Values[2];

    return sqrt(lenght_squared);
}

Vector3d Vector3d::CrossProduct(Vector3d &rhs)
{
    Vector3d l_CrossProduct;

    float l_Value = GetY() * rhs.GetZ() - GetZ() * rhs.GetY();
    l_CrossProduct.SetX(l_Value);

    l_Value = GetX() * rhs.GetZ() - GetZ() * rhs.GetX();
    l_CrossProduct.SetY(l_Value);

    l_Value = GetY() * rhs.GetX() - GetX() * rhs.GetY();
    l_CrossProduct.SetZ(l_Value);

    return l_CrossProduct;
}

float Vector3d::Dot(Vector3d &rhs)
{
    float l_ReturnVal = 0;

    for( int i = 0; i < 3; i++) {
        l_ReturnVal += m_Values[i] * rhs[i];
    }

    return l_ReturnVal;
}

Angle Vector3d::AngleTo(Vector3d &a_Vector)
{
    Vector3d l_FromVector = *this;
    Vector3d l_ToVector = a_Vector;
    l_FromVector.Normalise();
    l_ToVector.Normalise();
    float l_Dot = l_FromVector.Dot(l_ToVector);
    Angle l_Angle;
    l_Angle.SetWithRadians( acos( l_Dot ) );
    return l_Angle;
}

float Vector3d::AngleToVectorInDegrees(Vector3d &a_Vector)
{
    Angle l_Angle = AngleTo(a_Vector);
    return (l_Angle.InDegrees());
}

void Vector3d::Normalise()
{
    float l_Lenght = Length();
    m_Values[0] = m_Values[0] / l_Lenght;
    m_Values[1] = m_Values[1] / l_Lenght;
    m_Values[2] = m_Values[2] / l_Lenght;
}

void Vector3d::RotateToAngle(
  Angle* a_AngleXY
, Angle* a_AngleXZ
)
{
  float l_Lenght = Length();
  m_Values[ VECTOR3D_X_COORD ] = l_Lenght * a_AngleXY->GetAcrossValue();
  m_Values[ VECTOR3D_Y_COORD ] = l_Lenght * a_AngleXY->GetUpValue();
  m_Values[ VECTOR3D_Z_COORD ] = l_Lenght * a_AngleXZ->GetUpValue(); // z is actually the up coord in the XZ plane
  m_Values[ VECTOR3D_W_COORD ] = 1.0;
}

void Vector3d::Negate()
{
  for(int i = 0; i < VECTOR3D_W_COORD; i++ )  {
    m_Values[i] = -m_Values[i];
  }
}


