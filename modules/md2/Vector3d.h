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

#ifndef VECTOR3D_H
#define VECTOR3D_H

#include "Angle.h"

enum VECTOR3D_VALUES {
  VECTOR3D_X_COORD = 0
, VECTOR3D_Y_COORD
, VECTOR3D_Z_COORD
, VECTOR3D_W_COORD
};

class Vector3d {
    public:
        Vector3d();
        Vector3d(float x, float y, float z);
        Vector3d(float x, float y, float z, float w);

        Vector3d& operator=(const Vector3d &rhs);
        Vector3d& operator+=(const Vector3d &rhs);
        const Vector3d operator+(const Vector3d &rhs) const;
        Vector3d& operator-=(const Vector3d &rhs);
        const Vector3d operator-(const Vector3d &rhs) const;
        Vector3d& operator/=(const Vector3d &rhs);
        const Vector3d operator/(const Vector3d &rhs) const;
        Vector3d& operator/=(const float rhs);
        const Vector3d operator/(const float rhs) const;
        float& operator[](const int a_Index);
        const float Length();
        const float LengthSquared();
        void Normalise();
        Vector3d CrossProduct(Vector3d &rhs);
        float Dot(Vector3d &rhs);
        float* Access();

        void RotateToAngle(
          Angle* a_AngleXY
        , Angle* a_AngleXZ
        );

        Angle AngleTo(Vector3d &a_Vector);
        float AngleToVectorInDegrees(Vector3d &a_Vector);

        void SetX(float x) { m_Values[0] = x; }
        const float GetX() { return m_Values[0]; }

        void SetY(float y) { m_Values[1] = y; }
        const float GetY() { return m_Values[1]; }

        void SetZ(float z) { m_Values[2] = z; }
        const float GetZ() { return m_Values[2]; }

        void SetW(float w) { m_Values[3] = w; }
        const float GetW() { return m_Values[3]; }

        void SetVectorFromAngles(
          Angle* a_AngleY
        , Angle* a_AngleX
        , float a_Length
        );

        void Negate();

        void PrintMe();

        operator float* () const {return (float*) this;}
        operator const float* () const {return (const float*) this;}

    protected:
        float m_Values[4];

};

#endif
