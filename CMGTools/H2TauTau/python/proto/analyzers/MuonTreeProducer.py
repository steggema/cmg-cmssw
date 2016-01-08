from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase
from CMGTools.H2TauTau.proto.analyzers.DYJetsFakeAnalyzer import DYJetsFakeAnalyzer

class MuonTreeProducer(H2TauTauTreeProducerBase):
    ''' Tree producer for muon POG study.
    '''

    def __init__(self, *args):
        super(MuonTreeProducer, self).__init__(*args)
        self.maxNmuons = 100

    def declareHandles(self):
        super(MuonTreeProducer, self).declareHandles()

    def declareVariables(self, setup):

        self.bookMuon(self.tree, 'muon')
        self.bookGenParticle(self.tree, 'gen')
        self.var(self.tree, 'pf_iso05_pt')
        self.var(self.tree, 'pf_iso04_pt')
        self.var(self.tree, 'pf_iso03_pt')

        for dr in ['03', '04', '05']:
            self.var(self.tree, 'det'+dr+'emEt')
            self.var(self.tree, 'det'+dr+'hadEt')
            self.var(self.tree, 'det'+dr+'sumPt')
            self.var(self.tree, 'det'+dr+'hoEt')
            self.var(self.tree, 'det'+dr+'nTracks')
            self.var(self.tree, 'det'+dr+'emVetoEt')
            self.var(self.tree, 'det'+dr+'hadVetoEt')
            self.var(self.tree, 'det'+dr+'trackerVetoPt')
            self.var(self.tree, 'det'+dr+'hoVetoEt')

            self.var(self.tree, 'pf'+dr+'sumChargedHadronPt')
            self.var(self.tree, 'pf'+dr+'sumChargedParticlePt')
            self.var(self.tree, 'pf'+dr+'sumNeutralHadronEt')
            self.var(self.tree, 'pf'+dr+'sumPhotonEt')
            self.var(self.tree, 'pf'+dr+'sumPUPt')

    def process(self, event):
        # needed when doing handle.product(), goes back to
        # PhysicsTools.Heppy.analyzers.core.Analyzer
        self.readCollections(event.input)

        if not eval(self.skimFunction):
            return False


        ptcut = 8.
        ptSelGenmuonleps = [lep for lep in event.gentauleps if lep.pt() > ptcut]
        ptSelGenleps = [lep for lep in event.genleps if lep.pt() > ptcut]
        ptSelGenSummary = [p for p in event.generatorSummary if p.pt() > ptcut and abs(p.pdgId()) not in [6, 23, 24, 25, 35, 36, 37]]

        for muon in event.muons:
            DYJetsFakeAnalyzer.genMatch(event, muon, ptSelGenmuonleps,
                                        ptSelGenleps, ptSelGenSummary, matchAll=False)

        for i_muon, muon in enumerate(event.muons):
            muon.associatedVertex = event.vertices[0]
            if muon.pt() < 15.:
                continue
            if not muon.muonID('POG_ID_Medium'):
                continue
            if i_muon < self.maxNmuons:
                self.tree.reset()
                self.fillMuon(self.tree, 'muon', muon)
                self.fill(self.tree, 'pf_iso05_pt', muon.pf_iso_pt)
                self.fill(self.tree, 'pf_iso04_pt', muon.pf_iso04_pt)
                self.fill(self.tree, 'pf_iso03_pt', muon.pf_iso03_pt)
                if muon.genp:
                    self.fillGenParticle(self.tree, 'gen', muon.genp)

                for dr in ['03', '04', '05']:
                    if dr != '04':
                        self.fill(self.tree, 'det'+dr+'emEt', getattr(muon, 'isolationR'+dr)().emEt)
                        self.fill(self.tree, 'det'+dr+'hadEt', getattr(muon, 'isolationR'+dr)().hadEt)
                        self.fill(self.tree, 'det'+dr+'sumPt',getattr(muon, 'isolationR'+dr)().sumPt)
                        self.fill(self.tree, 'det'+dr+'hoEt', getattr(muon, 'isolationR'+dr)().hoEt )
                        self.fill(self.tree, 'det'+dr+'nTracks', getattr(muon, 'isolationR'+dr)().nTracks)
                        self.fill(self.tree, 'det'+dr+'emVetoEt', getattr(muon, 'isolationR'+dr)().emVetoEt)
                        self.fill(self.tree, 'det'+dr+'hadVetoEt', getattr(muon, 'isolationR'+dr)().hadVetoEt)
                        self.fill(self.tree, 'det'+dr+'trackerVetoPt', getattr(muon, 'isolationR'+dr)().trackerVetoPt)
                        self.fill(self.tree, 'det'+dr+'hoVetoEt', getattr(muon, 'isolationR'+dr)().hoVetoEt )
                    else:
                        self.fill(self.tree, 'det'+dr+'emEt', muon.ecalIso())
                        self.fill(self.tree, 'det'+dr+'hadEt', muon.hcalIso())
                        self.fill(self.tree, 'det'+dr+'sumPt', muon.trackIso())
                    
                    if dr != '05':
                        self.fill(self.tree, 'pf'+dr+'sumChargedHadronPt', getattr(muon, 'pfIsolationR'+dr)().sumChargedHadronPt)
                        self.fill(self.tree, 'pf'+dr+'sumChargedParticlePt', getattr(muon, 'pfIsolationR'+dr)().sumChargedParticlePt)
                        self.fill(self.tree, 'pf'+dr+'sumNeutralHadronEt', getattr(muon, 'pfIsolationR'+dr)().sumNeutralHadronEt)
                        self.fill(self.tree, 'pf'+dr+'sumPhotonEt', getattr(muon, 'pfIsolationR'+dr)().sumPhotonEt)
                        self.fill(self.tree, 'pf'+dr+'sumPUPt', getattr(muon, 'pfIsolationR'+dr)().sumPUPt)

                self.fillTree(event)
