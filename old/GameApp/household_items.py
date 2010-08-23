'''
 * This file is part of La Vida
 * Copyright (C) 2010 Ben Beverly
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

from object_3d import *

APPLIANCE_OFF = 0
APPLIANCE_ON = 1

class Household_Item ( Object3d ):
    def __init__( self, a_filename=None, a_name=None, a_price = 0):

        Object3d.__init__(self, a_filename,a_Name = a_name)
                                
        self.m_actionList = []      # A list of actions that can be taken by a Dude  
        self.m_price = a_price      # The Price of said item     

    def PerformInteraction(self):
        '''
        Have the Dude perform an action on the object
        '''
        pass            
          
class Furniture ( Household_Item ):
    def __init__(self, a_filename, a_name=None, a_price=0):
        Household_Item.__init__(self, a_filename, a_name, a_price)
        # Create the initial list of actions that can be taken with furniture by a Dude 
        self.m_actionList.append("Sit")
        
    def PerformInteraction(self):
        #Have the Dude perform an action on the object
        pass   

class Appliance( Household_Item ):
    def __init__(self, a_filename=None, a_name=None, a_price=0):
        Household_Item.__init__(self, a_filename, a_name, a_price)
        
        self.m_behavior = APPLIANCE_OFF
        # Create the initial list of actions that can be taken with appliances by a Dude
        self.m_actionList.append("Turn On") 
        
        
    def SetBehaviour( self ):
        if self.m_Behavior == APPLIANCE_OFF:
            self.m_Behavior = APPLIANCE_ON
        else:
            self.m_Behavior = APPLIANCE_OFF
            
        if m_Behaviour == APPLIANCE_ON:
            self._model.SetAnimation( ON )
        if a_Behaviour == APPLIANCE_OFF:
            self._model.SetAnimation( OFF )

    def DoBehaviours(self):
        if self.m_Behavior == APPLIANCE_ON:
            self.PeformInteraction()

    def PerformInteraction(self):
        '''
        Have the Dude perform an action on the object
        '''
        self.SetBehaviour()
        pass
            
class Cooker ( Appliance ):
    def __init__(self, a_filename, a_name=None, a_price=0):
        Appliance.__init__(self, a_filename, a_name, a_price)
        

    def PerformInteraction(self):
        '''
        Have the Dude perform an action on the object
        '''
        pass
        
