from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducer import H2TauTauTreeProducer
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes

class H2TauTauTreeProducerTauMu(H2TauTauTreeProducer):

    '''Tree producer for the H->tau tau analysis.'''

    def declareVariables(self, setup):

        super(H2TauTauTreeProducerTauMu, self).declareVariables(setup)

        self.bookTau(self.tree, 'l2')
        self.bookMuon(self.tree, 'l1')

        self.bookGenParticle(self.tree, 'l2_gen')
        self.var(self.tree, 'l2_gen_lepfromtau', int)
        self.bookGenParticle(self.tree, 'l1_gen')
        self.var(self.tree, 'l1_gen_lepfromtau', int)

        self.bookParticle(self.tree, 'l2_gen_vis')
        self.var(self.tree, 'l2_gen_decaymode', int)

        self.var(self.tree, 'l2_gen_nc_ratio')
        self.var(self.tree, 'l2_nc_ratio')
        self.var(self.tree, 'l2_pt_charged')
        self.var(self.tree, 'l2_pt_neutral')

        self.var(self.tree, 'l2_mass_chargedup')
        self.var(self.tree, 'l2_mass_chargeddown')
        self.var(self.tree, 'l2_mass_neutralup')
        self.var(self.tree, 'l2_mass_neutraldown')

        self.var(self.tree, 'mvis_chargedup')
        self.var(self.tree, 'mvis_chargeddown')
        self.var(self.tree, 'mvis_neutralup')
        self.var(self.tree, 'mvis_neutraldown')

        self.var(self.tree, 'l2_weight_fakerate')
        self.var(self.tree, 'l2_weight_fakerate_up')
        self.var(self.tree, 'l2_weight_fakerate_down')

        if hasattr(self.cfg_ana, 'addIsoInfo') and self.cfg_ana.addIsoInfo:
            self.var(self.tree, 'l1_puppi_iso_pt')
            self.var(self.tree, 'l1_puppi_iso04_pt')
            self.var(self.tree, 'l1_puppi_iso03_pt')

            self.var(self.tree, 'l1_puppi_no_muon_iso_pt')
            self.var(self.tree, 'l1_puppi_no_muon_iso04_pt')
            self.var(self.tree, 'l1_puppi_no_muon_iso03_pt')

            self.var(self.tree, 'l2_puppi_iso_pt')
            self.var(self.tree, 'l2_puppi_iso04_pt')
            self.var(self.tree, 'l2_puppi_iso03_pt')

            self.var(self.tree, 'l1_mini_iso')
            self.var(self.tree, 'l1_mini_reliso')

    def process(self, event):

        super(H2TauTauTreeProducerTauMu, self).process(event)

        tau = event.diLepton.leg2()
        muon = event.diLepton.leg1()

        self.fillTau(self.tree, 'l2', tau)
        self.fillMuon(self.tree, 'l1', muon)

        if hasattr(tau, 'genp') and tau.genp:
            self.fillGenParticle(self.tree, 'l2_gen', tau.genp)
            self.fill(self.tree, 'l2_gen_lepfromtau', tau.isTauLep)

        if hasattr(muon, 'genp') and muon.genp:
            self.fillGenParticle(self.tree, 'l1_gen', muon.genp)
            self.fill(self.tree, 'l1_gen_lepfromtau', muon.isTauLep)

        # save the p4 of the visible tau products at the generator level
        if tau.genJet() and hasattr(tau, 'genp') and tau.genp and abs(tau.genp.pdgId()) == 15:
            self.fillParticle(self.tree, 'l2_gen_vis', tau.physObj.genJet())
            tau_gen_dm = tauDecayModes.translateGenModeToInt(tauDecayModes.genDecayModeFromGenJet(tau.physObj.genJet()))
            self.fill(self.tree, 'l2_gen_decaymode', tau_gen_dm)
            if tau_gen_dm in [1, 2, 3, 4]:
                pt_neutral = 0.
                pt_charged = 0.
                for daughter in tau.genJet().daughterPtrVector():
                    id = abs(daughter.pdgId())
                    if id in [22, 11]:
                        pt_neutral += daughter.pt()
                    elif id not in [11, 13, 22] and daughter.charge():
                        if daughter.pt() > pt_charged:
                            pt_charged = daughter.pt()
                if pt_charged > 0.:
                    self.fill(self.tree, 'l2_gen_nc_ratio', (pt_charged - pt_neutral)/(pt_charged + pt_neutral))


        tau_scale_unc = 0.03

        if tau.gen_match != 5:
            tau_scale_unc = 0.

        s_up = 1 + tau_scale_unc
        s_down = 1 - tau_scale_unc

        if tau.decayMode() in [0, 1, 2, 3, 4]:
            pt_neutral = 0.
            pt_charged = 0.
            p4_neutral = None
            p4_charged = None
            # for cand_ptr in tau.signalChargedHadrCands(): # THIS CRASHES
            for i_cand in xrange(len(tau.signalChargedHadrCands())):
                cand = tau.signalChargedHadrCands()[i_cand]
                if cand.pt() > pt_charged:
                    pt_charged = cand.pt()
                p4_charged = p4_charged + cand.p4() if p4_charged else cand.p4()
                
            for i_cand in xrange(len(tau.signalGammaCands())):
                cand = tau.signalGammaCands()[i_cand]
                pt_neutral += cand.pt()
                p4_neutral = p4_neutral + cand.p4() if p4_neutral else cand.p4()

            if tau.decayMode() == 0 and pt_neutral:

                import pdb; pdb.set_trace()

            self.fill(self.tree, 'l2_pt_charged', pt_charged)
            self.fill(self.tree, 'l2_pt_neutral', pt_neutral)

            if p4_charged and p4_neutral:
                self.fill(self.tree, 'l2_mass_chargedup', (p4_charged*s_up + p4_neutral).mass())
                self.fill(self.tree, 'l2_mass_chargeddown', (p4_charged*s_down + p4_neutral).mass())
                self.fill(self.tree, 'l2_mass_neutralup', (p4_charged + p4_neutral*s_up).mass())
                self.fill(self.tree, 'l2_mass_neutraldown', (p4_charged + p4_neutral*s_down).mass())
                self.fill(self.tree, 'mvis_chargedup', (event.l1.p4() + p4_charged*s_up + p4_neutral).mass())
                self.fill(self.tree, 'mvis_chargeddown', (event.l1.p4() + p4_charged*s_down + p4_neutral).mass())
                self.fill(self.tree, 'mvis_neutralup', (event.l1.p4() + p4_charged + p4_neutral*s_up).mass())
                self.fill(self.tree, 'mvis_neutraldown', (event.l1.p4() + p4_charged + p4_neutral*s_down).mass())
            else:
                self.fill(self.tree, 'l2_mass_chargedup', tau.mass()*s_up)
                self.fill(self.tree, 'l2_mass_chargeddown', tau.mass()*s_down)
                self.fill(self.tree, 'l2_mass_neutralup', tau.mass())
                self.fill(self.tree, 'l2_mass_neutraldown', tau.mass())
                self.fill(self.tree, 'mvis_chargedup', (event.l1.p4() + tau.p4()*s_up ).mass())
                self.fill(self.tree, 'mvis_chargeddown', (event.l1.p4() + tau.p4()*s_down).mass())
                self.fill(self.tree, 'mvis_neutralup', (event.l1.p4() + tau.p4()).mass())
                self.fill(self.tree, 'mvis_neutraldown', (event.l1.p4() + tau.p4()).mass())

            if pt_charged > 0.:
                self.fill(self.tree, 'l2_nc_ratio', (pt_charged - pt_neutral)/(pt_charged + pt_neutral))
        else:
            self.fill(self.tree, 'l2_pt_charged', tau.pt())
            self.fill(self.tree, 'l2_pt_neutral', 0.)
            self.fill(self.tree, 'l2_mass_chargedup', tau.mass()*s_up)
            self.fill(self.tree, 'l2_mass_chargeddown', tau.mass()*s_down)
            self.fill(self.tree, 'l2_mass_neutralup', tau.mass())
            self.fill(self.tree, 'l2_mass_neutraldown', tau.mass())
            self.fill(self.tree, 'mvis_chargedup', (event.l1.p4() + tau.p4()*s_up ).mass())
            self.fill(self.tree, 'mvis_chargeddown', (event.l1.p4() + tau.p4()*s_down).mass())
            self.fill(self.tree, 'mvis_neutralup', (event.l1.p4() + tau.p4()).mass())
            self.fill(self.tree, 'mvis_neutraldown', (event.l1.p4() + tau.p4()).mass())


        self.fill(self.tree, 'l2_weight_fakerate', event.tauFakeRateWeightUp)
        self.fill(self.tree, 'l2_weight_fakerate_up', event.tauFakeRateWeightDown)
        self.fill(self.tree, 'l2_weight_fakerate_down', event.tauFakeRateWeight)

        if hasattr(self.cfg_ana, 'addIsoInfo') and self.cfg_ana.addIsoInfo:
            self.fill(self.tree, 'l1_puppi_iso_pt', muon.puppi_iso_pt)
            self.fill(self.tree, 'l1_puppi_iso04_pt', muon.puppi_iso04_pt)
            self.fill(self.tree, 'l1_puppi_iso03_pt', muon.puppi_iso03_pt)
            self.fill(self.tree, 'l1_puppi_no_muon_iso_pt', muon.puppi_no_muon_iso_pt)
            self.fill(self.tree, 'l1_puppi_no_muon_iso04_pt', muon.puppi_no_muon_iso04_pt)
            self.fill(self.tree, 'l1_puppi_no_muon_iso03_pt', muon.puppi_no_muon_iso03_pt)
            self.fill(self.tree, 'l2_puppi_iso_pt', tau.puppi_iso_pt)
            self.fill(self.tree, 'l2_puppi_iso04_pt', tau.puppi_iso04_pt)
            self.fill(self.tree, 'l2_puppi_iso03_pt', tau.puppi_iso03_pt)
            self.fill(self.tree, 'l1_mini_iso', muon.miniAbsIso)
            self.fill(self.tree, 'l1_mini_reliso', muon.miniRelIso)

        self.fillTree(event)
