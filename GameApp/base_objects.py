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

from household import HouseholdItem

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class CookerBase( HouseholdItem ):
    def __init__( self, parent, menu_root, a_Filename, event_queue=None, model_builder=None ):
        HouseholdItem.__init__( self, parent, menu_root, a_Filename, event_queue, model_builder )
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class SeatBase( HouseholdItem ):
    def __init__( self, parent, menu_root, a_Filename, event_queue=None, model_builder=None ):
        HouseholdItem.__init__( self, parent, a_Filename, event_queue, model_builder )
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class BedBase( HouseholdItem ):
    def __init__( self, parent, menu_root, a_Filename, event_queue=None, model_builder=None ):
        HouseholdItem.__init__( self, parent, menu_root, a_Filename, event_queue, model_builder )
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class PlantBase( HouseholdItem ):
    def __init__( self, parent, a_Filename, event_queue=None, model_builder=None ):
        HouseholdItem.__init__( self, parent, menu_root, a_Filename, event_queue, model_builder )
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class FeatureBase( HouseholdItem ):
    def __init__( self, parent, menu_root, a_Filename, event_queue=None, model_builder=None ):
        HouseholdItem.__init__( self, parent, menu_root, a_Filename, event_queue, model_builder )
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class ElectricalBase( HouseholdItem ):
    def __init__( self, parent, menu_root, a_Filename, event_queue=None, model_builder=None ):
        HouseholdItem.__init__( self, parent, menu_root, a_Filename, event_queue, model_builder )
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class GameActivityBase( HouseholdItem ):
    def __init__( self, parent, menu_root, a_Filename, event_queue=None, model_builder=None ):
        HouseholdItem.__init__( self, parent, menu_root, a_Filename, event_queue, model_builder )
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class CommunicatorBase( HouseholdItem ):
    def __init__( self, parent, menu_root, a_Filename, event_queue=None, model_builder=None ):
        HouseholdItem.__init__( self, parent, menu_root, a_Filename, event_queue, model_builder )
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class InformationBase( HouseholdItem ):
    def __init__( self, parent, menu_root, a_Filename, event_queue=None, model_builder=None ):
        HouseholdItem.__init__( self, parent, menu_root, a_Filename, event_queue, model_builder )