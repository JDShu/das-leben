'''
 * This file is part of La Vida
 * Copyright (C) 2009 Mike Hibbert
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
'''

__la_vida_data_path__ = "data/"

import os


def getDataPath():
    
    # get pathname absolute or relative
    if __la_vida_data_path__.startswith('/'):
        pathname = __la_vida_data_path__
    else:
        pathname = "%s/%s" % ( os.path.dirname(__file__), __la_vida_data_path__ )

    abs_data_path = os.path.abspath(pathname)
    if os.path.exists(abs_data_path):
        return abs_data_path
    else:
        raise Exception, "Cant find La Vida data folder"
    