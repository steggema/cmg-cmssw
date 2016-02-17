from CMGTools.TTHAnalysis.treeReAnalyzer import *

class EventVars2LSS1T:
    def __init__(self):
        self.branches = ["m_lep1_tau", "m_lep2_tau"]
        # self.branches = [ "mindr_lep1_jet", "mindr_lep2_jet",
        #                    "avg_dr_jet",
        #                    "MT_met_lep1", "MT_met_leplep",
        #                    "sum_abspz", "sum_sgnpz" ]
    def listBranches(self):
        return self.branches[:]
    def __call__(self,event):
        # make python lists as Collection does not support indexing in slices
        leps = [l for l in Collection(event,"LepGood","nLepGood",4)]
        # jets = [j for j in Collection(event,"Jet","nJet25",8)]
        taus = [t for t in Collection(event, 'TauGood', 'nTauGood', 2)]

        # (met, metphi)  = event.met_pt, event.met_phi
        # njet = len(jets)
        nlep = len(leps)
        ntau = len(taus)

        # prepare output
        ret = dict([(name,0.0) for name in self.branches])
        # fill output
        import pdb; pdb.set_trace()
        if ntau >= 1:
            tau = taus[0]
            if nlep >= 1:
                ret['m_lep1_tau'] = (tau.p4() + leps[0].p4()).mass()
            if nlep >= 2:
                ret['m_lep2_tau'] = (tau.p4() + leps[1].p4()).mass()

        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("ttHLepTreeProducerBase")
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVars2LSS1T()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

        
