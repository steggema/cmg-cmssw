from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

from PhysicsTools.Heppy.physicsobjects.Muon import Muon

from PhysicsTools.HeppyCore.utils.deltar import deltaR

class MuonIsolationCalculator(Analyzer):

    '''Calculates different muon isolation values'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(MuonIsolationCalculator, self).__init__(cfg_ana, cfg_comp, looperName)

    def attachPFIso(self, muon, puppi):
        pf_iso_pt = []
        pf_iso_pt_04 = []
        pf_iso_pt_03 = []

        muon_eta = muon.eta()
        muon_phi = muon.phi()

        for c_p in puppi:
            pdgId = c_p.pdgId()

            if abs(pdgId) not in [22, 130, 211]:
                continue

            pt = c_p.pt()
            eta = c_p.eta()
            phi = c_p.phi()
            # Neutral hadrons or photons
            inner_cone = 0.02
            if abs(pdgId) in [211]:
                inner_cone = 0.0001
            # elif pt < 0.5:
            #     continue

            if abs(muon_eta - eta) < 0.5:
                dr = deltaR(eta, phi, muon_eta, muon_phi)
                if inner_cone < dr:
                    if dr < 0.5:
                        pf_iso_pt.append(pt)
                    if dr < 0.4:
                        pf_iso_pt_04.append(pt)
                    if dr < 0.3:
                        pf_iso_pt_03.append(pt)


        setattr(muon, 'pf_iso_pt', sum(pf_iso_pt))
        setattr(muon, 'pf_iso04_pt', sum(pf_iso_pt_04))
        setattr(muon, 'pf_iso03_pt', sum(pf_iso_pt_03))

    def declareHandles(self):

        super(MuonIsolationCalculator, self).declareHandles()
        self.handles['pf'] = AutoHandle('packedPFCandidates', 'std::vector<pat::PackedCandidate>')
        self.handles['muons'] = AutoHandle('slimmedMuons', 'std::vector<pat::Muon>')


    def beginLoop(self, setup):
        print self, self.__class__
        super(MuonIsolationCalculator, self).beginLoop(setup)

    def process(self, event):
        self.readCollections(event.input)
        pf_cands = self.handles['pf'].product()
        event.muons = self.handles['muons'].product()
        event.muons = [Muon(muon) for muon in event.muons]
        for muon in event.muons:
            muon.rho = event.rho
            self.attachPFIso(muon, pf_cands)

        return True
