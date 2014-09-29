import operator
import math
from ROOT import TLorentzVector, Double
from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from CMGTools.RootTools.analyzers.DiLeptonAnalyzer import DiLeptonAnalyzer
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle
from CMGTools.RootTools.statistics.Counter import Counter, Counters
from CMGTools.RootTools.physicsobjects.PhysicsObjects import Muon, Tau, GenParticle, Jet
from CMGTools.RootTools.physicsobjects.HTauTauElectron import HTauTauElectron as Electron
from CMGTools.RootTools.utils.DeltaR import cleanObjectCollection, matchObjectCollection, bestMatch
from CMGTools.RootTools.utils.TriggerMatching import triggerMatched


####################################################################3
#
# 11 Nov 2013 Y.Takahashi
# This analyzer is for WH, EMuTau-channel
#
####################################################################3

class WHMMTAnalyzer(Analyzer):

    # Class needed for the object selections
    LeptonClass = Muon
    OtherLeptonClass = Electron
    TauClass = Tau


    # Init
    def __init__(self, cfg_ana, cfg_comp, looperName):
#        print 'Init for the WHMMTAnalyzer'
        super(WHMMTAnalyzer,self).__init__(cfg_ana, cfg_comp, looperName)


    # beginLoop
    def beginLoop(self):
#       print 'Init for the beginLoop'
        super(WHMMTAnalyzer, self).beginLoop()
        self.counters.addCounter('MMT')
        count = self.counters.counter('MMT')
        count.register('all events')
        count.register('step1')
        count.register('step2')
        count.register('step3')
        
    def declareHandles(self):
        super(WHMMTAnalyzer, self).declareHandles()

        self.handles['electrons'] = AutoHandle(
            ('cmgElectronSel','','PAT'), 'std::vector<cmg::Electron>')


        self.handles['muons'] = AutoHandle(
            ('cmgMuonSel','','PAT'), 'std::vector<cmg::Muon>')


        self.handles['jets'] = AutoHandle( 'cmgPFJetSel',
                                           'std::vector<cmg::PFJet>' )

        self.handles['taus'] = AutoHandle(
#            ('cmgTauSel','','PAT'), 'std::vector<cmg::Tau>')
#            ('cmgTauSel','','MUTAUTAU'), 'std::vector<cmg::Tau>')
            ('cmgTauSel','','DIMUTAU'), 'std::vector<cmg::Tau>')





    # Muon
    #################################################
    
    def buildLooseLeptons(self, cmgLeptons, event):
        '''Build loose muons'''

        leptons = []
            
        for index, lep in enumerate(cmgLeptons):

            pyl = self.__class__.LeptonClass(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.flag_id = False
            pyl.flag_iso = False
            pyl.trig_match = False

            if pyl.pt() > 10. and abs(pyl.eta()) < 2.4 and \
                   pyl.looseId() and abs(pyl.dz()) < 0.2 and \
                   pyl.sourcePtr().innerTrack().hitPattern().numberOfValidPixelHits()>0:

                leptons.append( pyl )
                
        return leptons

    def muid(self, pyl):
        '''check muon ID'''
        return pyl.tightId()


    def muiso(self, pyl):
        '''check muon isolation'''

        relIso = False
        if abs(pyl.eta()) < 1.479 and self.testLeg2Iso(pyl, 0.15):
            relIso = True
        if abs(pyl.eta()) > 1.479 and self.testLeg2Iso(pyl, 0.1):
            relIso = True

        return relIso


    def buildVetoLeptons(self, cmgLeptons, event):
        '''Build muons'''

        leptons = []
        for index, lep in enumerate(cmgLeptons):
            pyl = self.__class__.LeptonClass(lep)
            pyl.associatedVertex = event.goodVertices[0]

            if pyl.pt() > 5. and  abs(pyl.eta()) < 2.3 and \
                   self.muid(pyl) and abs(pyl.dz()) < 0.2 and self.testLeg2Iso(pyl, 0.15) and abs(pyl.dB3D()) < 0.2:

                leptons.append( pyl )
                
        return leptons




    # Electron
    #################################################

    def buildLooseOtherLeptons(self, cmgOtherLeptons, event):
        '''Build loose electrons'''

        otherLeptons = []

        for index, lep in enumerate(cmgOtherLeptons):
            pyl = self.__class__.OtherLeptonClass(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.flag_id = False
            pyl.flag_iso = False
            pyl.trig_match = False
            
            if pyl.pt() > 10. and abs(pyl.eta()) < 2.5 and \
                   pyl.loosestIdForTriLeptonVeto() and abs(pyl.dz()) < 0.2 and pyl.sourcePtr().isGsfCtfScPixChargeConsistent():
                
                otherLeptons.append( pyl )

        return otherLeptons

    def eid(self, pyl):
        '''check electron ID'''
        return pyl.mvaForLeptonVeto()


    def eiso(self, pyl):
        '''check electron ID'''

        relIso = False
        if abs(pyl.eta()) < 1.479 and self.testLeg2Iso(pyl, 0.15):
            relIso = True
        if abs(pyl.eta()) > 1.479 and self.testLeg2Iso(pyl, 0.1):
            relIso = True
            
        return relIso


    def buildVetoOtherLeptons(self, cmgOtherLeptons, event):
        '''Build electrons for third lepton veto, associate best vertex.
        '''
        otherLeptons = []
        for index, lep in enumerate(cmgOtherLeptons):
            pyl = self.__class__.OtherLeptonClass(lep)
            pyl.associatedVertex = event.goodVertices[0]

            if pyl.pt() > 10. and abs(pyl.eta()) < 2.5 and \
                   pyl.mvaForLeptonVeto() and abs(pyl.dz()) < 0.2 and self.testLeg2Iso(pyl, 0.3):

                otherLeptons.append( pyl )

        return otherLeptons




    # Tau
    #################################################

    def buildLooseTau(self, cmgLeptons, event):
        '''Build taus.'''
        leptons = []
        
        for index, lep in enumerate(cmgLeptons):
            pyl = self.__class__.TauClass(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.flag_id = False
            pyl.flag_iso = False
            pyl.decaymode = -999
            pyl.ep = -999
            pyl.againstELooseArmin = False
            pyl.againstETight = False
            pyl.againstELoose = False
            pyl.againstEMedium = False
            pyl.againstE2Loose = False
            pyl.againstE2Medium = False
#            pyl.againstE0Loose = False
#            pyl.againstE0Medium = False
            pyl.againstERaw = -999
            pyl.againstE2Raw = -999
            pyl.againstE0Raw = -999
            pyl.againstECat = -999
            pyl.againstE2Cat = -999
#            pyl.againstE0Cat = -999
            pyl.againstMuLoose = False
            pyl.againstMuTight = False
            pyl.mvaisolation = -999
            pyl.mvaisolation_loose = False
            pyl.dBisolation = -999


            ### new tau ID ###

            pyl.byLooseCombinedIsolationDeltaBetaCorr3Hits = False
            pyl.byMediumCombinedIsolationDeltaBetaCorr3Hits = False
            pyl.byTightCombinedIsolationDeltaBetaCorr3Hits = False
            pyl.byCombinedIsolationDeltaBetaCorrRaw3Hits = -999
            pyl.againstMuonLoose2 = False
            pyl.againstMuonMedium2 = False
            pyl.againstMuonTight2 = False
            pyl.againstElectronMVA5category = False
            pyl.againstElectronLooseMVA5 = False
            pyl.againstElectronMediumMVA5 = False
            pyl.againstElectronTightMVA5 = False
            pyl.againstElectronVTightMVA5 = False
            pyl.againstMuonLoose3 = False
            pyl.againstMuonTight3 = False
            pyl.againstMuonMVALoose = False
            pyl.againstMuonMVAMedium = False
            pyl.againstMuonMVATight = False
            pyl.againstMuonMVARaw = -999
            pyl.byIsolationMVA3oldDMwoLTraw = -999
            pyl.byLooseIsolationMVA3oldDMwoLT =  False
            pyl.byMediumIsolationMVA3oldDMwoLT = False
            pyl.byTightIsolationMVA3oldDMwoLT = False
            pyl.byVTightIsolationMVA3oldDMwoLT = False
            pyl.byVVTightIsolationMVA3oldDMwoLT = False
            pyl.byIsolationMVA3oldDMwLTraw = -999
            pyl.byLooseIsolationMVA3oldDMwLT = False
            pyl.byMediumIsolationMVA3oldDMwLT = False
            pyl.byTightIsolationMVA3oldDMwLT = False
            pyl.byVTightIsolationMVA3oldDMwLT = False
            pyl.byVVTightIsolationMVA3oldDMwLT = False
            pyl.byIsolationMVA3newDMwoLTraw = -999
            pyl.byLooseIsolationMVA3newDMwoLT = False
            pyl.byMediumIsolationMVA3newDMwoLT = False
            pyl.byTightIsolationMVA3newDMwoLT = False
            pyl.byVTightIsolationMVA3newDMwoLT = False
            pyl.byVVTightIsolationMVA3newDMwoLT = False
            pyl.byIsolationMVA3newDMwLTraw = -999
            pyl.byLooseIsolationMVA3newDMwLT = False
            pyl.byMediumIsolationMVA3newDMwLT = False
            pyl.byTightIsolationMVA3newDMwLT = False
            pyl.byVTightIsolationMVA3newDMwLT = False
            pyl.byVVTightIsolationMVA3newDMwLT = False


            # old tau ID
            
            pyl.decayModeFinding = False
            pyl.byVLooseCombinedIsolationDeltaBetaCorr = False
            pyl.byLooseCombinedIsolationDeltaBetaCorr = False
            pyl.byMediumCombinedIsolationDeltaBetaCorr =  False
            pyl.byTightCombinedIsolationDeltaBetaCorr =  False
            pyl.againstElectronLoose =  False
            pyl.againstElectronMedium =  False
            pyl.againstElectronTight =  False
            pyl.againstElectronDeadECAL =  False
            pyl.againstMuonLoose =  False
            pyl.againstMuonMedium =  False
            pyl.againstMuonTight =  False


            

            if pyl.pt() > 20 and abs(pyl.eta()) < 2.3 and \
                   pyl.tauID("decayModeFinding") and abs(pyl.dz()) < 0.2:
                
                leptons.append( pyl )                

        return leptons


    def tauid(self, pyl):
        '''check tau ID.'''

#        print 'inside_check', pyl.tauID("againstMuonLoose"), pyl.tauID("againstElectronLooseMVA3")
        if pyl.tauID("againstMuonLoose") > 0.5 and pyl.tauID("againstElectronLooseMVA3"):
#            print 'This becomes true !!'
            return True
        else:            
            return False


    def tauiso(self, pyl):
        '''check tau isolation.'''

        return self.testLeg1Iso(pyl, None)


        
    def buildVetoTau(self, cmgLeptons, event):
        '''Build taus.'''
        leptons = []

        for index, lep in enumerate(cmgLeptons):
            pyl = self.__class__.TauClass(lep)
            pyl.associatedVertex = event.goodVertices[0]

            if pyl.pt() > 20 and abs(pyl.eta()) < 2.5 and \
                   pyl.tauID("decayModeFinding") and self.testLeg1Iso(pyl, None) and abs(pyl.dz()) < 0.2:

                leptons.append( pyl )

        return leptons




    # process
    #####################################################

    def process(self, iEvent, event):

#        print 'process ongoing!'
#        import pdb; pdb.set_trace()
	
#	import pdb; pdb.set_trace()
        self.readCollections(iEvent)
        self.counters.counter('MMT').inc('all events')
        
        event.muoncand     = self.buildLooseLeptons(self.handles['muons'].product(), event)
        event.electroncand = self.buildLooseOtherLeptons(self.handles['electrons'].product(), event)
        event.taucand      = self.buildLooseTau(self.handles['taus'].product(), event)

        cmgJets = self.handles['jets'].product()

        event.CSVjet = []

        for cmgJet in cmgJets:
            jet = Jet( cmgJet )
            if self.testVetoBJet(jet):
                event.CSVjet.append(jet)


        event.electroncand, dummpy = cleanObjectCollection(event.electroncand,
                                                           masks = event.muoncand,
                                                           deltaRMin = 0.5)

        
        
        # CSV veto
        electroncand_removebjet = []
        muoncand_removebjet = []
        
        for ielectron in event.electroncand:
            bm, dr2min = bestMatch(ielectron, event.CSVjet)
            if dr2min > 0.25:
                electroncand_removebjet.append(ielectron)

        for imuon in event.muoncand:
            bm, dr2min = bestMatch(imuon, event.CSVjet)
            if dr2min > 0.25:
                muoncand_removebjet.append(imuon)

        event.electroncand = electroncand_removebjet
        event.muoncand = muoncand_removebjet
        
        
#        event.flag_trigmatched = False
#        


#        if not event.flag_trigmatched:
#            return False

    
#        event.cleanelectron = []
#        event.cleanmuon = []



        for ii in event.electroncand:                                               
            ii.flag_id = self.eid(ii)
            ii.flag_iso = self.eiso(ii)

            ii.trig_match = True
#            if self.triggerCheck(event, event.hltPaths, ii):
#                ii.trig_match = True


#
#            for jj in event.muoncand:
#                if self.returnMass(jj, ii) > 20. and \
#                       ii.charge()*jj.charge()==1. and \
#                       self.returnDR(ii, jj) > 0.5:
#
#                    flag_add = True
#
#            if flag_add:
#                ii.flag_id = self.eid(ii)
#                ii.flag_iso = self.eiso(ii)
#                event.cleanelectron.append(ii)
#
#
#
        for ii in event.muoncand:
            ii.flag_id = self.muid(ii)
            ii.flag_iso = self.muiso(ii)


            ii.trig_match = True
#            if self.triggerCheck(event, event.hltPaths, ii):
#                ii.trig_match = True


#                continue
#                
#            for jj in event.electroncand:
#                if self.returnMass(jj, ii) > 20. and \
#                       ii.charge()*jj.charge()==1. and \
#                       self.returnDR(ii, jj) > 0.5:
#
#                    flag_add = True
#
#            if flag_add:
#                ii.flag_id = self.muid(ii)
#                ii.flag_iso = self.muiso(ii)
#                event.cleanmuon.append(ii)



#        event.electroncand = event.cleanelectron
#        event.muoncand = event.cleanmuon

        


#        idiso_electron = [ie for ie in event.electroncand if self.eid(ie) and self.eiso(ie)]
#        idiso_muon = [im for im in event.muoncand if self.muid(im) and self.muiso(im)]

#        if idiso_electron[0].pt() > idiso_muon[0].pt():
            


#        if not (len(event.muoncand)>=1 and len(event.electroncand)>=1 and len(event.taucand)>=1):
#            print 'YCheck : (m,e,t) = ', len(event.muoncand), len(event.electroncand), len(event.taucand)
#            return False

        
#        lepton1 = [] # Leading lepton
#        lepton2 = [] # 2nd leading lepton


#        if not (len(id_electron)>=1 and len(id_muon)>=1):
#            return False
            

#        lepton_type = ''
#
#        if id_electron[0].pt() > id_muon[0].pt(): #e-mu
#            lepton1 = [ie for ie in id_electron if ie.pt() > 20.]
#            lepton2 = [im for im in id_muon if im.pt() > 10.]
#            lepton_type = 'electron'
#        elif id_electron[0].pt() < id_muon[0].pt():
#            lepton1 = [im for im in id_muon if im.pt() > 20.]
#            lepton2 = [ie for ie in id_electron if ie.pt() > 10.]
#            lepton_type = 'muon'



#            import pdb; pdb.set_trace()        
#        if not (len(lepton1)==1 and len(lepton2)==1):
#            return False

#        self.counters.counter('MMT').inc('1mu + 1e')
#        
#
#        event.muon = ''
#        event.electron = ''
#        
#        if lepton_type=='muon':
#            event.muon = lepton1[0]
#            event.electron = lepton2[0]
#        elif lepton_type=='electron':
#            event.electron = lepton1[0]
#            event.muon = lepton2[0]




        event.loosetau = []

        for itau in event.taucand:

            itau.decaymode = itau.decayMode()
            itau.ep = itau.calcEOverP()
            itau.flag_iso = self.tauiso(itau)
            itau.flag_id = self.tauid(itau)

            itau.againstERaw = itau.tauID('againstElectronMVA3raw')
            itau.againstE2Raw = itau.tauID('againstElectronMVA2raw')
            itau.againstE0Raw = itau.tauID('againstElectronMVA')
            itau.againstECat = int(round(itau.tauID('againstElectronMVA3category')))
            itau.againstE2Cat = int(round(itau.tauID('againstElectronMVA2category')))
#            itau.againstE0Cat = int(round(itau.tauID('againstElectronMVAcategory')))
            itau.againstELooseArmin = itau.tauID("againstElectronLoose")
            itau.againstETight = itau.tauID("againstElectronTightMVA3")
            itau.againstELoose = itau.tauID("againstElectronLooseMVA3")
            itau.againstEMedium = itau.tauID("againstElectronMediumMVA3")
            itau.againstE2Loose = itau.tauID("againstElectronLooseMVA2")
            itau.againstE2Medium = itau.tauID("againstElectronMediumMVA2")
#            itau.againstE0Loose = itau.tauID("againstElectronLooseMVA")
#            itau.againstE0Medium = itau.tauID("againstElectronMediumMVA")
            itau.againstMuLoose = itau.tauID("againstMuonLoose")
            itau.againstMuTight = itau.tauID("againstMuonTight")
            itau.dBisolation = itau.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")
            itau.mvaisolation = itau.tauID("byRawIsoMVA")
            itau.mvaisolation_loose = itau.tauID('byLooseIsoMVA')

            # new tau ID 
            itau.byLooseCombinedIsolationDeltaBetaCorr3Hits  = itau.tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits")
            itau.byMediumCombinedIsolationDeltaBetaCorr3Hits  = itau.tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits")
            itau.byTightCombinedIsolationDeltaBetaCorr3Hits  = itau.tauID("byTightCombinedIsolationDeltaBetaCorr3Hits")
            itau.byCombinedIsolationDeltaBetaCorrRaw3Hits = itau.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")
            itau.againstMuonLoose2  = itau.tauID("againstMuonLoose2")
            itau.againstMuonMedium2  = itau.tauID("againstMuonMedium2")
            itau.againstMuonTight2  = itau.tauID("againstMuonTight2")
            itau.againstElectronMVA5category  = itau.tauID("againstElectronMVA5category")
            itau.againstElectronLooseMVA5  = itau.tauID("againstElectronLooseMVA5")
            itau.againstElectronMediumMVA5  = itau.tauID("againstElectronMediumMVA5")
            itau.againstElectronTightMVA5  = itau.tauID("againstElectronTightMVA5")
            itau.againstElectronVTightMVA5  = itau.tauID("againstElectronVTightMVA5")
            itau.againstMuonLoose3  = itau.tauID("againstMuonLoose3")
            itau.againstMuonTight3  = itau.tauID("againstMuonTight3")
            itau.againstMuonMVALoose  = itau.tauID("againstMuonMVALoose")
            itau.againstMuonMVAMedium  = itau.tauID("againstMuonMVAMedium")
            itau.againstMuonMVATight  = itau.tauID("againstMuonMVATight")
            itau.againstMuonMVARaw = itau.tauID("againstMuonMVARaw")
            itau.byIsolationMVA3oldDMwoLTraw = itau.tauID("byIsolationMVA3oldDMwoLTraw")
            itau.byLooseIsolationMVA3oldDMwoLT = itau.tauID("byLooseIsolationMVA3oldDMwoLT")
            itau.byMediumIsolationMVA3oldDMwoLT  = itau.tauID("byMediumIsolationMVA3oldDMwoLT")
            itau.byTightIsolationMVA3oldDMwoLT  = itau.tauID("byTightIsolationMVA3oldDMwoLT")
            itau.byVTightIsolationMVA3oldDMwoLT  = itau.tauID("byVTightIsolationMVA3oldDMwoLT")
            itau.byVVTightIsolationMVA3oldDMwoLT  = itau.tauID("byVVTightIsolationMVA3oldDMwoLT")
            itau.byIsolationMVA3oldDMwLTraw = itau.tauID("byIsolationMVA3oldDMwLTraw")
            itau.byLooseIsolationMVA3oldDMwLT  = itau.tauID("byLooseIsolationMVA3oldDMwLT")
            itau.byMediumIsolationMVA3oldDMwLT  = itau.tauID("byMediumIsolationMVA3oldDMwLT")
            itau.byTightIsolationMVA3oldDMwLT  = itau.tauID("byTightIsolationMVA3oldDMwLT")
            itau.byVTightIsolationMVA3oldDMwLT  = itau.tauID("byVTightIsolationMVA3oldDMwLT")
            itau.byVVTightIsolationMVA3oldDMwLT  = itau.tauID("byVVTightIsolationMVA3oldDMwLT")
            itau.byIsolationMVA3newDMwoLTraw = itau.tauID("byIsolationMVA3newDMwoLTraw")
            itau.byLooseIsolationMVA3newDMwoLT  = itau.tauID("byLooseIsolationMVA3newDMwoLT")
            itau.byMediumIsolationMVA3newDMwoLT  = itau.tauID("byMediumIsolationMVA3newDMwoLT")
            itau.byTightIsolationMVA3newDMwoLT  = itau.tauID("byTightIsolationMVA3newDMwoLT")
            itau.byVTightIsolationMVA3newDMwoLT  = itau.tauID("byVTightIsolationMVA3newDMwoLT")
            itau.byVVTightIsolationMVA3newDMwoLT  = itau.tauID("byVVTightIsolationMVA3newDMwoLT")
            itau.byIsolationMVA3newDMwLTraw = itau.tauID("byIsolationMVA3newDMwLTraw")
            itau.byLooseIsolationMVA3newDMwLT  = itau.tauID("byLooseIsolationMVA3newDMwLT")
            itau.byMediumIsolationMVA3newDMwLT  = itau.tauID("byMediumIsolationMVA3newDMwLT")
            itau.byTightIsolationMVA3newDMwLT  = itau.tauID("byTightIsolationMVA3newDMwLT")
            itau.byVTightIsolationMVA3newDMwLT  = itau.tauID("byVTightIsolationMVA3newDMwLT")
            itau.byVVTightIsolationMVA3newDMwLT  = itau.tauID("byVVTightIsolationMVA3newDMwLT")

            # old tau ID

            itau.decayModeFinding = itau.tauID("decayModeFinding")
            itau.byVLooseCombinedIsolationDeltaBetaCorr = itau.tauID("byVLooseCombinedIsolationDeltaBetaCorr")
            itau.byLooseCombinedIsolationDeltaBetaCorr = itau.tauID("byLooseCombinedIsolationDeltaBetaCorr")
            itau.byMediumCombinedIsolationDeltaBetaCorr =  itau.tauID("byMediumCombinedIsolationDeltaBetaCorr")
            itau.byTightCombinedIsolationDeltaBetaCorr =  itau.tauID("byTightCombinedIsolationDeltaBetaCorr")
            itau.againstElectronLoose =  itau.tauID("againstElectronLoose")
            itau.againstElectronMedium =  itau.tauID("againstElectronMedium")
            itau.againstElectronTight =  itau.tauID("againstElectronTight")
            itau.againstElectronDeadECAL =  itau.tauID("againstElectronDeadECAL")
            itau.againstMuonLoose =  itau.tauID("againstMuonLoose")
            itau.againstMuonMedium =  itau.tauID("againstMuonMedium")
            itau.againstMuonTight =  itau.tauID("againstMuonTight")




#            print 'dB, raw, loose', itau.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits"), itau.tauID("byRawIsoMVA"), itau.tauID('byLooseIsoMVA')
#            print 'ID_check', itau.tauID("againstMuonLoose"), itau.tauID("againstElectronLooseMVA3")
#            print 'mu_loose, e_loose, e_medium', itau.tauID("againstMuonLoose"), itau.tauID("againstElectronLooseMVA3"),  itau.tauID("againstElectronMediumMVA3"), itau.flag_id
            
#            if flag_mu_mass and  and \
#                   ((itau.decayMode()==0 and itau.calcEOverP() > 0.2) or (itau.decayMode()!=0)):
#                itau.flag_id = True
#
#            
#            if flag_e_mass==False and flag_mu_mass==False and self.tauid(itau):
#                itau.flag_id = True





#            flag_e_overlap = False
#            flag_e_mass = False
#
#            for ii in idiso_electron:
#                mass_et = self.returnMass(ii, itau)
#                if mass_et > 71.2 and mass_et < 111.2:
#                    flag_e_mass = True
#                
#                if self.returnDR(itau, ii) < 0.5:
#                    flag_e_overlap = True
#
#            if flag_e_overlap:
#                continue
#            
#
#            flag_mu_overlap = False
#            flag_mu_mass = False
#
#            for ii in idiso_muon:
#                mass_mt = self.returnMass(ii, itau)
#                if mass_mt > 71.2 and mass_mt < 111.2:
#                    flag_mu_mass = True
#                
#                if self.returnDR(itau, ii) < 0.5:
#                    flag_mu_overlap = True
#
#            if flag_mu_overlap:
#                continue


#            if self.tauiso(itau):
#                itau.flag_iso = True
#
#            
#            if flag_e_mass and itau.tauID("againstElectronMediumMVA3"):
#                itau.flag_id = True
#
#
#            if flag_mu_mass and itau.tauID("againstMuonTight") and \
#                   ((itau.decayMode()==0 and itau.calcEOverP() > 0.2) or (itau.decayMode()!=0)):
#                itau.flag_id = True
#
#            
#            if flag_e_mass==False and flag_mu_mass==False and self.tauid(itau):
#                itau.flag_id = True


            event.loosetau.append(itau)


        event.taucand = event.loosetau

        # Additional tau veto
        event.vetotaucand = self.buildVetoTau(self.handles['taus'].product(), event)
        event.vetomuoncand = self.buildVetoLeptons(self.handles['muons'].product(), event)
        event.vetoelectroncand = self.buildVetoOtherLeptons(self.handles['electrons'].product(), event)

        flag_plus = 0
        flag_minus = 0
        
        for im in event.muoncand:
            if im.charge()==1:
                flag_plus +=1
            else:
                flag_minus +=1


        self.counters.counter('MMT').inc('step1')
        
        if not (flag_plus >= 2 or flag_minus >= 2):
            return False

        self.counters.counter('MMT').inc('step2')

        if not (len(event.muoncand)>=2 and len(event.taucand)>=1):
#        if not (len(event.taucand)>=1 and len(event.muoncand)>=1 and len(event.electroncand)>=1):
            return False

        self.counters.counter('MMT').inc('step3')

#        idiso_tau = [it for it in event.taucand if (it.flag_id and it.flag_iso)]
#        if not len(idiso_tau)>=1 :
#            return False





#        if not len(lepton3) == 1:
#            return False

#        self.counters.counter('MMT').inc('1 e/mu/tau')
#        event.tau = lepton3[0]




#        event.M_l2t = self.returnMass(lepton2[0], event.tau)

#        if self.returnMass(event.muon, event.electron) < 20.:
#            return False
#        if self.returnMass(lepton2[0], event.tau) < 20.:
#            return False

        

        # charge requirement
        # SS for two light leptons

#        if event.electron.charge()*event.muon.charge()==-1.:
#            return False


#        if event.tau.charge()*event.muon.charge()!=-1.:
#            return False


        # dR separation 
#        if self.returnDR(event.tau, event.muon) < 0.5:
#            return False
#        if self.returnDR(event.tau, event.electron) < 0.5:
#            return False
#        if self.returnDR(event.electron, event.muon) < 0.5:
#            return False

        

#        event.loosetaucand, dummpy = cleanObjectCollection(event.loosetaucand,
#                                                           masks = [event.muon],
##                                                           masks = event.muoncand,
#                                                           deltaRMin = 0.4)
#
#        event.loosetaucand, dummpy = cleanObjectCollection(event.loosetaucand,
#                                                           masks = [event.electron],
##                                                           masks = event.electroncand,
#                                                           deltaRMin = 0.4)
#
#        event.loosetaucand, dummpy = cleanObjectCollection(event.loosetaucand,
#                                                           masks = [event.tau],
#                                                           deltaRMin = 0.4)
#
#
#        event.loosemuoncand, dummpy = cleanObjectCollection(event.loosemuoncand,
#                                                           masks = [event.muon],
#                                                           deltaRMin = 0.4)
#
#        event.loosemuoncand, dummpy = cleanObjectCollection(event.loosemuoncand,
#                                                           masks = [event.electron],
#                                                           deltaRMin = 0.4)
#
#        event.loosemuoncand, dummpy = cleanObjectCollection(event.loosemuoncand,
#                                                           masks = [event.tau],
#                                                           deltaRMin = 0.4)
#
#        event.looseelectroncand, dummpy = cleanObjectCollection(event.looseelectroncand,
#                                                           masks = [event.muon],
#                                                           deltaRMin = 0.4)
#
#        event.looseelectroncand, dummpy = cleanObjectCollection(event.looseelectroncand,
#                                                           masks = [event.electron],
#                                                           deltaRMin = 0.4)
#
#        event.looseelectroncand, dummpy = cleanObjectCollection(event.looseelectroncand,
#                                                           masks = [event.tau],
#                                                           deltaRMin = 0.4)

        
        
#        NadditionalLepton = len(event.loosetaucand) + len(event.loosemuoncand) + len(event.looseelectroncand)
#        if NadditionalLepton>=1:
#            return False



#        print 'All events passed : ', event.run, event.lumi, event.eventId
        
        return True

        

    def returnMass(self, obj1, obj2):

        e4 = TLorentzVector()
        t4 = TLorentzVector()

        e4.SetPtEtaPhiM(Double(obj1.pt()),
                        Double(obj1.eta()),
                        Double(obj1.phi()),
                        Double(obj1.mass()))

        t4.SetPtEtaPhiM(Double(obj2.pt()),
                        Double(obj2.eta()),
                        Double(obj2.phi()),
                        Double(obj2.mass()))

        return (e4 + t4).M()
            
    def returnDR(self, obj1, obj2):
        deta = obj1.eta() - obj2.eta()
        dphi = obj1.phi() - obj2.phi()
        dr2 = deta*deta + dphi*dphi
        return math.sqrt(dr2)

    def triggerCheck(self, event, hltPaths, leg):

        flag_pass = False
    
        for itrig in hltPaths:
          
            if self.trigMatched(event, itrig, leg):
                flag_pass = True

        return flag_pass


    def testLeg1Iso(self, tau, isocut):
        '''if isocut is None, returns true if three-hit iso cut is passed.
        Otherwise, returns true if iso MVA > isocut.'''
        if isocut is None:
#            print 'check tau ID ', tau.tauID('byCombinedIsolationDeltaBetaCorrRaw3Hits')
#            return tau.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits") < 1.5
#            return tau.tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits")
            return tau.tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits")
        else:
            return tau.tauID("byRawIsoMVA")>isocut


    def testVertex(self, lepton):
        '''Tests vertex constraints, for mu and tau'''
        return abs(lepton.dxy()) < 0.045 and \
               abs(lepton.dz()) < 0.2 


    def testLeg2ID(self, muon):
        '''Tight muon selection, no isolation requirement'''
        return muon.tightId() and \
               self.testVertex( muon )
               

    def testLeg2Iso(self, muon, isocut):
        '''Tight muon selection, with isolation requirement'''
        if isocut is None:
            isocut = self.cfg_ana.iso2
#        print muon.relIsoAllChargedDB05, isocut
#        return muon.relIsoAllChargedDB05()<isocut
#        print 'relative_isolation = ',muon.relIso(0.5), 'cut = ', isocut    
        return muon.relIso(0.5, 1)<isocut    


    def thirdLeptonVeto(self, leptons, otherLeptons, ptcut = 10, isocut = 0.3) :
        '''The tri-lepton veto. returns False if > 2 leptons (e or mu).'''
        vleptons = [lep for lep in leptons if
                    self.testLegKine(lep, ptcut=ptcut, etacut=2.4) and 
                    self.testLeg2ID(lep) and
                    self.testLeg2Iso(lep, isocut) ]
        # count electrons
        votherLeptons = [olep for olep in otherLeptons if 
                         self.testLegKine(olep, ptcut=ptcut, etacut=2.5) and \
                         olep.looseIdForTriLeptonVeto()           and \
                         self.testVertex( olep )           and \
                         olep.relIsoAllChargedDB05() < isocut
                        ]
        if len(vleptons) + len(votherLeptons)> 1:
            return False
        else:
            return True


    def leptonAccept(self, leptons):
        '''The di-lepton veto, returns false if > one lepton.
        e.g. > 1 mu in the mu tau channel'''
        looseLeptons = [muon for muon in leptons if
                        self.testLegKine(muon, ptcut=15, etacut=2.4) and
                        muon.isGlobalMuon() and
                        muon.isTrackerMuon() and
                        muon.sourcePtr().userFloat('isPFMuon') and
                        #COLIN Not sure this vertex cut is ok... check emu overlap
                        #self.testVertex(muon) and
                        # JAN: no dxy cut
                        abs(muon.dz()) < 0.2 and
                        self.testLeg2Iso(muon, 0.3)
                        ]
        isPlus = False
        isMinus = False
        # import pdb; pdb.set_trace()
        for lepton in looseLeptons:
            if lepton.charge()<0: isMinus=True
            elif lepton.charge()>0: isPlus=True
            else:
                raise ValueError('Impossible!')
        veto = isMinus and isPlus
        return not veto

    def testVetoBJet(self, jet):
        # medium csv working point
        # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BTagPerformanceOP#B_tagging_Operating_Points_for_3

        jet.btagMVA = jet.btag("combinedSecondaryVertexBJetTags")

        return jet.pt()>12. and \
               abs( jet.eta() ) < 2.4 and \
               jet.btagMVA > 0.8



#    def testBJet(self, jet):
#        # medium csv working point
#        # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BTagPerformanceOP#B_tagging_Operating_Points_for_3
#        jet.btagMVA = jet.btag("combinedSecondaryVertexBJetTags")
#
#        return jet.pt()>20. and \
#               abs( jet.eta() ) < 2.4 and \
#               jet.btagMVA > 0.898 and \
#               self.testJetID(jet)
#
#
#    def testJetID(self, jet):
#        jet.puJetIdPassed = jet.puJetId(wp53x=True)
#        jet.pfJetIdPassed = jet.looseJetId()
#
#        return jet.puJetIdPassed and jet.pfJetIdPassed


###    def trigMatched(self, event, leg, legName):
###        '''Returns true if the leg is matched to a trigger object as defined in the
###        triggerMap parameter'''
###        if not hasattr( self.cfg_ana, 'triggerMap'):
###            return True
####        else:
####            print 'Trigger OK'
###
###
###        path = event.hltPath
###        print 'path = ', path
###        
###        triggerObjects = event.triggerObjects
###        print 'triggerObjects = ', triggerObjects
###
###        filters = self.cfg_ana.triggerMap[ path ]
###        print 'filters = ', filters
###        
###        filter = None
###        print 'filter = ', filter
###
###
####        import pdb; pdb.set_trace()
###        
###        if legName == 'leg1':
###            filter = filters[0]
###        elif legName == 'leg2':
###            filter = filters[1]
###        else:
###            raise ValueError( 'legName should be leg1 or leg2, not {leg}'.format(
###                leg=legName )  )
###
###        # JAN: Need a hack for the embedded samples: No trigger matching in that case
###        if filter == '':
####            print 'Jan filter'
###            return True
###
###        for it in triggerObjects:
###            print '(path, filter, obj, hasPath, hasSelection = ', path, filter, it, it.hasPath(path), it.hasSelection(filter)
###
###
###        # the dR2Max value is 0.3^2
###        pdgIds = None
###        if len(filter) == 2:
###            filter, pdgIds = filter[0], filter[1]
###        return triggerMatched(leg, triggerObjects, path, filter,
###                              dR2Max=0.089999,
####                              dR2Max=0.25,
###                              pdgIds=pdgIds )






#    def trigMatched(self, event, trigpath, leg1, leg2):
#        '''Returns true if the leg is matched to a trigger object as defined in the
#        triggerMap parameter'''
#        if not hasattr( self.cfg_ana, 'triggerMap'):
#            return True
#
#
#
#        triggerObjects = event.triggerObjects
#        filters = self.cfg_ana.triggerMap[ trigpath ]
#        filter = filters[0]
#        pdgIds = None
#
#
##        print 'trigger path = ', trigpath
##        for it in triggerObjects:
##            print '(filter, obj, hasPath, hasSelection = ', filter, it.hasPath(path), it.hasSelection(filter), it
#
#        
#
#        triggerMatched1 = triggerMatched(leg1, triggerObjects, trigpath, filter,
#                                         dR2Max=0.089999,
#                                         pdgIds=pdgIds )
#
#
#        triggerMatched2 = triggerMatched(leg2, triggerObjects, trigpath, filter,
#                                         dR2Max=0.089999,
#                                         pdgIds=pdgIds )
#
#
##        import pdb; pdb.set_trace();
#
#
#        if filter.find('Mu8_Ele17')!=-1:
#            return triggerMatched1 and triggerMatched2 and leg1.pt() > 10. and leg2.pt() > 20.
#        elif filter.find('Mu17_Ele8')!=-1:
#            return triggerMatched1 and triggerMatched2 and leg1.pt() > 20. and leg2.pt() > 10.
#        else:
#            print 'Unexpected Trigger !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'
#            return False




    def trigMatched(self, event, trigpath, leg):
        '''Returns true if the leg is matched to a trigger object'''
        if not hasattr( self.cfg_ana, 'triggerMap'):
            return True

#        print trigpath

        triggerObjects = event.triggerObjects
        filters = self.cfg_ana.triggerMap[ trigpath ]
        filter = filters[0]
        pdgIds = None


        flag = triggerMatched(leg, triggerObjects, trigpath, filter,
                              dR2Max=0.089999,
                              pdgIds=pdgIds )


        if filter.find('Mu8_Ele17')!=-1 or filter.find('Mu17_Ele8')!=-1:
            return flag
        else:
            return False

