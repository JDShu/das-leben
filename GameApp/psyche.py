import pickle
from os import path

class Psyche_Tables: #defines which emotions are affected by each noesis and by how much
    def __init__( self ):
        self.NE_table = {} #dict of list - noesis: [(emotion, modvalue), ...] (how a noesis affects emotions)
        self.IN_table = {} #dict of list - interactions: [noesis, ...] (which noesis' affect interactions)
        self.load_NE_table("default.ne")
        self.load_IN_table("default.in")
        
    def load_NE_table( self, NE_table_file):
        F = open(NE_table_file, 'rb')
        self.NE_table.update(pickle.load(F))
        F.close()
        
    def load_IN_table( self, IN_table_file):
        F = open(IN_table_file, 'rb')
        self.IN_table.update(pickle.load(F))
        F.close()
        
class Psyche:
    def __init__( self ):
        self.state = {} #dict of ints - emotion name : emotion value
        self.noesis = {} #dict - records whether noesis' are active - noesis : boolean
        self.load_state_file("default.state")
        self.load_noesis_file("default.noesis")
        
    def interact( self, interaction, psyche_tables ):
        for n in psyche_tables.IN_table[ interaction ]:
            if self.noesis[n]:
                for e in psyche_tables.NE_table[ n ]:
                    self.state[ e[0] ] += e[1]

    def add_noesis( self, n):
        self.noesis[n] = True

    def remove_noesis(self, n):
        self.noesis[n] = False

    def load_noesis_file( self, noesis_file):
        F = open(noesis_file, 'rb')
        self.noesis.update(pickle.load(F))
        F.close()

    def load_state_file( self, state_dict):
        F = open(state_dict, 'rb')
        self.state.update(pickle.load(F))
        F.close()
        
