from CMGTools.RootTools.analyzers.GenParticleAnalyzer import *
from CMGTools.RootTools.utils.DeltaR import matchObjectCollection
from CMGTools.RootTools.physicsobjects.genutils import *

class GenTopAnalyzer( GenParticleAnalyzer ):

    def process(self, iEvent, event):
        # event.W = None
        # event.Z = None
        if not self.cfg_comp.isMC:
            return True
        result = super(GenTopAnalyzer, self).process(iEvent, event)
        
        event.top = [GenParticle(part) for part in event.genParticles if part.status()==3 and part.pdgId()==6]
        event.atop = [GenParticle(part) for part in event.genParticles if part.status()==3 and part.pdgId()==-6]

        event.genlep = [GenParticle(part) for part in event.genParticles if part.status()==3 and abs(part.pdgId()) in [11, 13, 15]]

        
#        import pdb; pdb.set_trace()

#        if len(event.top)==1 and len(event.atop)==1:
#            print 'OK'
#        else:
#            print 'Not ttbar!!'
        
