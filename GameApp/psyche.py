import pickle
from os import path

class Mask_Manager:
    def __init__( self ):
        self.masks = {} # double dict mask name: mask object
        self.load_masks("./", "default.msk" )
        
    def load_masks( self, a_DataPath, filename ):
        mask_file = open( path.join( a_DataPath, filename ), "rb" )
        
        while True:
            try:
                self.add_mask( pickle.load( mask_file ) )
            except EOFError:
                break

    def add_mask( self, mask ):
        self.masks[mask.name] = mask
        print mask

class Mask:
    def __init__( self, name, rules ):
        self.name = name
        self.rules = rules #double dict interactions: emotions: modvalue
        
class Psyche:
    def __init__( self ):
        self.emotions = {} #dict of ints - emotion name : emotion value
        self.interactions = {} #double dict interactions: emotions: modvalue
        
    def apply_mask( self, mask, mask_manager ):
        print "lol"
        for m in mask_manager.masks[mask]:
            print "noob"
            for i in m.rules:
                for e in i:
                    self.interactions[i][e] += m.rules[i][e]                

    def remove_mask( self, mask, mask_manager):
        for m in mask_manager.masks[mask]:
            for i in m.rules:
                for e in i:
                    self.interactions[i][e] -= m.rules[i][e]                
                    
    def interact( self, interaction):
        for e in self.interactions[interaction]:
            self.emotions[e] += self.interactions[interaction][e]
