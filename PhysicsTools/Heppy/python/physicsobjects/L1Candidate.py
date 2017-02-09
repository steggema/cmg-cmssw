from PhysicsTools.Heppy.physicsobjects.PhysicsObject import *

class L1Candidate(PhysicsObject):
    '''
    Wrapper of http://cmslxr.fnal.gov/source/DataFormats/L1Trigger/interface/L1Candidate.h
    
    Adds a nice printout and useful attributes:
        bx     = None  # bunch crossing
        type   = None  # further type convention
        dR     = None  # dR to the object it's matched to
        goodID = None  # true if the types of the offline and self objects equal 
    '''
    
    def __init__(self, *args, **kwargs):
        super(L1Candidate, self).__init__(*args, **kwargs)    
        self._reset()
        
#         for i, attr in enumerate([self.bx, self.type, self.dR, self.goodID][:len(args)]):
#             attr = args[i]
#         
#         if 'bx'     in kwargs.keys(): self.bx     = kwargs['bx'     ]   
#         if 'type'   in kwargs.keys(): self.type   = kwargs['type'   ]   
#         if 'dR'     in kwargs.keys(): self.dR     = kwargs['dR'     ]   
#         if 'goodID' in kwargs.keys(): self.goodID = kwargs['goodID' ]   

    def _reset(self):
        self.bx     = None
        self.type   = None
        self.dR     = None
        self.goodID = None

    def __str__(self):
        base = super(L1Candidate, self).__str__()

        return base + \
               'type %s\n'\
               '\tpt  %.1f\n'\
               '\teta %.3f\n'\
               '\tphi %.3f\n'\
               '\tiso %d\n'\
               '\tqual %d\n'\
               '\tbx  %d\n'\
               '\tdR  %.4f\n'\
               '\tmatches offline type  %d\n'\
               %(str(self.type),   
                 self.pt(), self.eta(), self.phi(), 
                 self.hwIso(), self.hwQual(),
                 self.bx,    
                 self.dR,    
                 self.goodID)
