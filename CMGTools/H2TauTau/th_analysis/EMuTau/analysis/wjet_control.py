#################################
# 
# 12 Nov 2013
# Y.Takahashi (Yuta.Takahashi@cern.ch)
# 
# This is the analyzer to obtain control samples for the kNN training
# python analysis_antiTau.py --mode (antiMu, antiE, antiEMu, signal)
#
#################################

import array
import numpy as num
from ROOT import TFile, gDirectory, TMVA, TTree
import optparse
#import config as tool
import CMGTools.H2TauTau.config as tool
from CMGTools.RootTools.utils.DeltaR import deltaR,deltaPhi
#import config as tool

import os, ROOT
if "/smearer_cc.so" not in ROOT.gSystem.GetLibraries(): 
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/smearer.cc+" % os.environ['CMSSW_BASE']);
if "/mcCorrections_cc.so" not in ROOT.gSystem.GetLibraries(): 
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/mcCorrections.cc+" % os.environ['CMSSW_BASE']);


### For options
parser = optparse.OptionParser()
parser.add_option('--channel', action="store", dest="channel", default='muon') # muon means jet->muon fake sample
parser.add_option('--phys', action="store", dest="phys", default='data') # muon means jet->muon fake sample
options, args = parser.parse_args()

print 
print '[INFO] Analysis channel = ', options.channel


process = [options.phys]

db = tool.ReadFile(process, 'emt')
filedict = db.returnFile()

#mva_muon_barrel = 0.0089
#mva_electron_barrel = 0.0649
#
#mva_muon_endcap = 0.0621
#mva_electron_endcap = 0.0891

mva_muon_barrel = 0.0833
mva_electron_barrel = 0.0599

mva_muon_endcap = 0.0851
mva_electron_endcap = 0.0801


mva_muonreader = TMVA.Reader("!Color:Silent=T:Verbose=F")
mva_electronreader = TMVA.Reader("!Color:Silent=T:Verbose=F")        
mva_mvar_map   = {}
mva_evar_map   = {}

for var in ['bdt_muon_dxy','bdt_muon_dz','bdt_muon_mva_ch_iso','bdt_muon_mva_neu_iso','bdt_muon_mva_jet_dr','bdt_muon_mva_ptratio','bdt_muon_mva_csv']:
    mva_mvar_map[var] = array.array('f',[0])
    mva_muonreader.AddVariable(var, mva_mvar_map[var])

for var in ['bdt_electron_mva_score','bdt_electron_mva_ch_iso','bdt_electron_mva_neu_iso','bdt_electron_mva_jet_dr','bdt_electron_mva_ptratio','bdt_electron_mva_csv']:
    mva_evar_map[var] = array.array('f',[0])
    mva_electronreader.AddVariable(var, mva_evar_map[var])

mva_muonreader.BookMVA('mva_muon_data', 'training/weights/TMVAClassification_BDT_muon.weights.xml')
mva_electronreader.BookMVA('mva_electron_data', 'training/weights/TMVAClassification_BDT_electron.weights.xml')

    
if __name__ == '__main__':

    for index, ifile in enumerate(filedict):

        pname = ifile[0]
        filename = ifile[1]
        lum_weight = ifile[2]
        ptype = ifile[3]
        
#        outputfile = '/afs/cern.ch/user/y/ytakahas/public/forJan/kNN_training/Wjet_' + options.channel + '_training_' + pname[index] + '.root'
        outputfile = 'root_aux/Wjet_' + options.channel + '_training_' + pname + '.root'
        ofile = TFile(outputfile, 'recreate')
        t = TTree('kNNTrainingTree','kNNTrainingTree')

        variables = [('lepton_pt', float), ('lepton_eta', float), ('lepton_phi', float), ('lepton_mass', float), ('lepton_jetpt', float), ('lepton_kNN_jetpt', float), ('lepton_njet', int), ('lepton_id', int), ('lepton_iso', int), ('lepton_reliso', float), ('lepton_MT', float), ('lepton_charge', int), ('lepton_dpt', float), ('lepton_mva', float), ('lepton_mva_threshold', float), ('slepton_pt', float), ('slepton_eta', float), ('slepton_phi', float), ('slepton_mass', float), ('slepton_jetpt', float), ('slepton_kNN_jetpt', float), ('slepton_njet', int), ('slepton_id', int), ('slepton_iso', int), ('slepton_reliso', float), ('slepton_MT', float), ('slepton_charge', int), ('slepton_dpt', float), ('slepton_mva', float), ('evt_weight_raw', float), ('evt_weight_muid', float), ('evt_weight_mutrig', float), ('evt_weight_eid', float), ('evt_weight_etrig', float), ('evt_run', int), ('evt_evt', int), ('evt_lum', int), ('evt_njet', int), ('evt_nbjet', int), ('evt_isMC', int), ('evt_isMCw', float), ('evt_id', int), ('evt_met', float), ('evt_weight', float), ('evt_Mem', float), ('lepton_pdgid', int), ('lepton_pdgid_dr', float), ('slepton_pdgid', int), ('slepton_pdgid_dr', float)]
    
        var_dict = {}
        for var in variables:
            if var[0] in var_dict:
                print 'Duplicate variable definition!', var[0]
                continue
            v_a = var_dict[var[0]] = num.zeros(1, dtype=var[1])
            t.Branch(var[0], v_a, var[0]+'/'+('D' if var[1]==float else 'I'))
            
            
        ###################

        print '[INFO] ', index, filename, 'is processing => ', outputfile

        myfile = TFile(filename)

        main = gDirectory.Get('H2TauTauTreeProducerEMT2')
        mchain = gDirectory.Get('H2TauTauTreeProducerEMT2_muon')
        echain = gDirectory.Get('H2TauTauTreeProducerEMT2_electron')
        tchain = gDirectory.Get('H2TauTauTreeProducerEMT2_tau')
        vmchain = gDirectory.Get('H2TauTauTreeProducerEMT2_vetomuon')
        vechain = gDirectory.Get('H2TauTauTreeProducerEMT2_vetoelectron')
        vtchain = gDirectory.Get('H2TauTauTreeProducerEMT2_vetotau')
        bchain = gDirectory.Get('H2TauTauTreeProducerEMT2_bjet')
        gchain = gDirectory.Get('H2TauTauTreeProducerEMT2_gen')

        ptr_m = 0        
        ptr_e = 0
        ptr_t = 0
        
        ptr_vm = 0      
        ptr_ve = 0
        ptr_vt = 0

        ptr_nb = 0
        ptr_ng = 0


        
        total = main.GetEntries()
        passed = 0

        counter = [0 for ii in range(11)]
        
#        for jentry in xrange(10000):
        for jentry in xrange(main.GetEntries()):

            ientry = main.LoadTree(jentry)
            nb = main.GetEntry(jentry)
            counter[0] += 1
            
            if jentry%10000==0:
                print '[INFO]', jentry, '/', main.GetEntries() #nmuon, nelectron, ntau, nvmuon, nvelectron, nvtau

            nmuon      = int(main.nmuon)
            nelectron  = int(main.nelectron)
            ntau       = int(main.ntau)
            
            nvmuon     = int(main.nvmuon)
            nvelectron = int(main.nvelectron)
            nvtau      = int(main.nvtau)

            nbjets     = int(main.nBJets)
            if pname != 'data':
                ngen = int(main.nGen)

            gp = []
            if pname != 'data':
                for igen in xrange(ptr_ng, ptr_ng+ngen):
                    
                    gchain.LoadTree(igen)
                    gchain.GetEntry(igen)
                    
                    gj = tool.easyobj_gen(gchain.gen_pt,
                                          gchain.gen_eta,
                                          gchain.gen_phi,
                                          gchain.gen_pdgid)
                    gp.append(gj)



            # for real Leptons
            signal_muon = []
            signal_electron = []
            signal_tau = []
            
            for im in xrange(ptr_m, ptr_m + nmuon):
                mchain.LoadTree(im)
                mchain.GetEntry(im)
                
                muon_ipdg = -99
                muon_min_dr = 100

                for gen in gp:
                    _dr_ = deltaR(gen.eta, gen.phi, mchain.muon_eta, mchain.muon_phi)
                    if _dr_ < 0.5 and muon_min_dr > _dr_:
                        muon_min_dr = _dr_
                        muon_ipdg = gen.pdgid

                matchid = 0
                matchany = 0
                if abs(muon_ipdg)==5:
                    matchany = 2


#                mva_mvar_map['bdt_muon_dxy'][0] = mchain.muon_dxy
#                mva_mvar_map['bdt_muon_dz'][0] = mchain.muon_dz
                mva_mvar_map['bdt_muon_mva_ch_iso'][0] = mchain.muon_mva_ch_iso
                mva_mvar_map['bdt_muon_mva_neu_iso'][0] = mchain.muon_mva_neu_iso
#                mva_mvar_map['bdt_muon_mva_jet_dr'][0] = mchain.muon_mva_jet_dr
#                mva_mvar_map['bdt_muon_mva_ptratio'][0] = mchain.muon_mva_ptratio
                mva_mvar_map['bdt_muon_mva_csv'][0] = mchain.muon_mva_csv


                cor_dxy = mchain.muon_mva_dxy
                cor_dz = mchain.muon_mva_dz
                cor_jet_dr = mchain.muon_mva_jet_dr
                cor_ptratio = mchain.muon_mva_ptratio

                if pname != 'data':
                    cor_dxy = ROOT.scaleDxyMC(mchain.muon_mva_dxy, int(muon_ipdg), mchain.muon_pt, mchain.muon_eta, matchid, matchany)
                    cor_dz = ROOT.scaleDzMC(mchain.muon_mva_dz, int(muon_ipdg), mchain.muon_pt, mchain.muon_eta, matchid, matchany)
                    cor_jet_dr = ROOT.correctJetDRMC(mchain.muon_mva_jet_dr, int(muon_ipdg), mchain.muon_pt, mchain.muon_eta, matchid, matchany)
                    cor_ptratio = ROOT.correctJetPtRatioMC(mchain.muon_mva_ptratio, int(muon_ipdg), mchain.muon_pt, mchain.muon_eta, matchid, matchany)
                
                mva_mvar_map['bdt_muon_dxy'][0] = cor_dxy
                mva_mvar_map['bdt_muon_dz'][0] = cor_dz
                mva_mvar_map['bdt_muon_mva_jet_dr'][0] = cor_jet_dr
                mva_mvar_map['bdt_muon_mva_ptratio'][0] = cor_ptratio

                    
                
                mva_iso_muon = mva_muonreader.EvaluateMVA('mva_muon_data')
#
#                mva_mvar_map['bdt_muon_dxy'][0] = mchain.muon_dxy
#                mva_mvar_map['bdt_muon_dz'][0] = mchain.muon_dz
#                mva_mvar_map['bdt_muon_mva_ch_iso'][0] = mchain.muon_mva_ch_iso
#                mva_mvar_map['bdt_muon_mva_neu_iso'][0] = mchain.muon_mva_neu_iso
#                mva_mvar_map['bdt_muon_mva_jet_dr'][0] = mchain.muon_mva_jet_dr
#                mva_mvar_map['bdt_muon_mva_ptratio'][0] = mchain.muon_mva_ptratio
#                mva_mvar_map['bdt_muon_mva_csv'][0] = mchain.muon_mva_csv
#                
#                mva_iso_muon = mva_muonreader.EvaluateMVA('mva_muon_data')

#                if ((options.channel=='muon' and mchain.muon_MT < 35.) or \
#                    (options.channel=='electron' and mchain.muon_id and mchain.muon_reliso < 0.15 and mchain.muon_MT > 35)):

                if ((options.channel=='muon' and mchain.muon_MT < 35.) or \
                    (options.channel=='electron' and \
                     mchain.muon_id and \
                     mchain.muon_MT > 35 and \
                     ((abs(mchain.muon_eta) < 1.479 and mva_iso_muon > mva_muon_barrel) or \
                      (abs(mchain.muon_eta) > 1.479 and mva_iso_muon > mva_muon_endcap)))):


                    muon = tool.mobj(mchain.muon_pt,
                                     mchain.muon_eta,
                                     mchain.muon_phi,
                                     mchain.muon_mass,
                                     mchain.muon_jetpt,
                                     mchain.muon_njet,
                                     mchain.muon_charge,
                                     mchain.muon_trigmatch,
                                     mchain.muon_trig_weight,
                                     mchain.muon_id_weight,
                                     mchain.muon_id,
                                     mchain.muon_iso,
                                     mchain.muon_reliso,
                                     mchain.muon_MT,
#                                     mchain.muon_dxy,
                                     ROOT.scaleDxyMC(mchain.muon_mva_dxy, int(muon_ipdg), mchain.muon_pt, mchain.muon_eta, matchid, matchany),
#                                     mchain.muon_dz,
                                     ROOT.scaleDzMC(mchain.muon_mva_dz, int(muon_ipdg), mchain.muon_pt, mchain.muon_eta, matchid, matchany),
                                     mchain.muon_dB3D,
                                     mchain.muon_jetcsv,
                                     mchain.muon_jetcsv_10,
                                     mchain.muon_mva,
                                     mchain.muon_mva_ch_iso,
                                     mchain.muon_mva_neu_iso,
#                                     mchain.muon_mva_jet_dr,
                                     ROOT.correctJetDRMC(mchain.muon_mva_jet_dr, int(muon_ipdg), mchain.muon_pt, mchain.muon_eta, matchid, matchany),
#                                     mchain.muon_mva_ptratio,
                                     ROOT.correctJetPtRatioMC(mchain.muon_mva_ptratio, int(muon_ipdg), mchain.muon_pt, mchain.muon_eta, matchid, matchany),
                                     mchain.muon_mva_csv,
                                     mva_iso_muon
                                    )
#
#
#                    muon = tool.mobj(mchain.muon_pt,
#                                     mchain.muon_eta,
#                                     mchain.muon_phi,
#                                     mchain.muon_mass,
#                                     mchain.muon_jetpt,
#                                     mchain.muon_njet,
#                                     mchain.muon_charge,
#                                     mchain.muon_trigmatch,
#                                     mchain.muon_trig_weight,
#                                     mchain.muon_id_weight,
#                                     mchain.muon_id,
#                                     mchain.muon_iso,
#                                     mchain.muon_reliso,
#                                     mchain.muon_MT,
#                                     mchain.muon_dxy,
#                                     mchain.muon_dz,
#                                     mchain.muon_dB3D,
#                                     mchain.muon_jetcsv,
#                                     mchain.muon_jetcsv_10,
#                                     mchain.muon_mva,
#                                     mchain.muon_mva_ch_iso,
#                                     mchain.muon_mva_neu_iso,
#                                     mchain.muon_mva_jet_dr,
#                                     mchain.muon_mva_ptratio,
#                                     mchain.muon_mva_csv,
#                                     mva_iso_muon
#                                    )

                        
                    signal_muon.append(muon)


            for ie in xrange(ptr_e, ptr_e + nelectron):
                echain.LoadTree(ie)
                echain.GetEntry(ie)

                electron_ipdg = -99
                electron_min_dr = 100

                for gen in gp:
                    _dr_ = deltaR(gen.eta, gen.phi, echain.electron_eta, echain.electron_phi)
                    if _dr_ < 0.5 and electron_min_dr > _dr_:
                        electron_min_dr = _dr_
                        electron_ipdg = gen.pdgid

                matchid = 0
                matchany = 0
                if abs(electron_ipdg)==5:
                    matchany = 2

#                mva_evar_map['bdt_electron_mva_score'][0] = echain.electron_mva_score
#                mva_evar_map['bdt_electron_mva_ch_iso'][0] = echain.electron_mva_ch_iso
#                mva_evar_map['bdt_electron_mva_neu_iso'][0] = echain.electron_mva_neu_iso
#                mva_evar_map['bdt_electron_mva_jet_dr'][0] = echain.electron_mva_jet_dr
#                mva_evar_map['bdt_electron_mva_ptratio'][0] = echain.electron_mva_ptratio
#                mva_evar_map['bdt_electron_mva_csv'][0] = echain.electron_mva_csv
#                
#                mva_iso_electron = mva_electronreader.EvaluateMVA('mva_electron_data')



                mva_evar_map['bdt_electron_mva_score'][0] = echain.electron_mva_score
                mva_evar_map['bdt_electron_mva_ch_iso'][0] = echain.electron_mva_ch_iso
                mva_evar_map['bdt_electron_mva_neu_iso'][0] = echain.electron_mva_neu_iso
                mva_evar_map['bdt_electron_mva_csv'][0] = echain.electron_mva_csv


                cor_jet_dr = echain.electron_mva_jet_dr
                cor_ptratio = echain.electron_mva_ptratio

#                print 'before', cor_jet_dr
                if pname != 'data':
                    cor_jet_dr = ROOT.correctJetDRMC(echain.electron_mva_jet_dr, int(electron_ipdg), echain.electron_pt, echain.electron_eta, matchid, matchany)
                    cor_ptratio = ROOT.correctJetPtRatioMC(echain.electron_mva_ptratio, int(electron_ipdg), echain.electron_pt, echain.electron_eta, matchid, matchany)
#                print 'after', cor_jet_dr
                                
                
                mva_evar_map['bdt_electron_mva_jet_dr'][0] = cor_jet_dr
                mva_evar_map['bdt_electron_mva_ptratio'][0] = cor_ptratio


                mva_iso_electron = mva_electronreader.EvaluateMVA('mva_electron_data')




#                import pdb; pdb.set_trace()

                if ((options.channel=='electron' and echain.electron_MT < 35.) or \
                    (options.channel=='muon' and \
                     echain.electron_id and \
                     echain.electron_MT > 35. and \
                     ((abs(echain.electron_eta) < 1.479 and mva_iso_electron > mva_electron_barrel) or \
                      (abs(echain.electron_eta) > 1.479 and mva_iso_electron > mva_electron_endcap)))):

                    
                    electron = tool.eobj(echain.electron_pt,
                                         echain.electron_eta,
                                         echain.electron_phi,
                                         echain.electron_mass,
                                         echain.electron_jetpt,
                                         echain.electron_njet,
                                         echain.electron_charge,
                                         echain.electron_trigmatch,
                                         echain.electron_trig_weight,
                                         echain.electron_id_weight,
                                         echain.electron_id,
                                         echain.electron_iso,
                                         echain.electron_reliso,
                                         echain.electron_MT,
                                         echain.electron_mva_dxy,
                                         echain.electron_mva_dz,
                                         echain.electron_dB3D,
                                         echain.electron_jetcsv,
                                         echain.electron_jetcsv_10,
                                         echain.electron_mva,
                                         echain.electron_mva_ch_iso,
                                         echain.electron_mva_neu_iso,
 #                                         echain.electron_mva_jet_dr,
                                         ROOT.correctJetDRMC(echain.electron_mva_jet_dr, int(electron_ipdg), echain.electron_pt, echain.electron_eta, matchid, matchany),
#                                         echain.electron_mva_ptratio,
                                         ROOT.correctJetPtRatioMC(echain.electron_mva_ptratio, int(electron_ipdg), echain.electron_pt, echain.electron_eta, matchid, matchany),
                                         echain.electron_mva_csv,
                                         echain.electron_mva_score,
                                         echain.electron_mva_numberOfHits,
                                         mva_iso_electron
                                   )

#                    electron = tool.eobj(echain.electron_pt,
#                                         echain.electron_eta,
#                                         echain.electron_phi,
#                                         echain.electron_mass,
#                                         echain.electron_jetpt,
#                                         echain.electron_njet,
#                                         echain.electron_charge,
#                                         echain.electron_trigmatch,
#                                         echain.electron_trig_weight,
#                                         echain.electron_id_weight,
#                                         echain.electron_id,
#                                         echain.electron_iso,
#                                         echain.electron_reliso,
#                                         echain.electron_MT,
#                                         echain.electron_dxy,
#                                         echain.electron_dz,
#                                         echain.electron_dB3D,
#                                         echain.electron_jetcsv,
#                                         echain.electron_jetcsv_10,
#                                         echain.electron_mva,
#                                         echain.electron_mva_ch_iso,
#                                         echain.electron_mva_neu_iso,
#                                         echain.electron_mva_jet_dr,
#                                         echain.electron_mva_ptratio,
#                                         echain.electron_mva_csv,
#                                         echain.electron_mva_score,
#                                         echain.electron_mva_numberOfHits,
#                                         mva_iso_electron
#                                         )

#                    electron = tool.obj(echain.electron_pt,
#                                   echain.electron_eta,
#                                   echain.electron_phi,
#                                   echain.electron_mass,
#                                   echain.electron_jetpt,
#                                   echain.electron_njet,
#                                   echain.electron_charge,
#                                   echain.electron_trigmatch,
#                                   echain.electron_trig_weight,
#                                   echain.electron_id_weight,
#                                   echain.electron_id,
#                                   echain.electron_iso,
#                                   echain.electron_reliso,
#                                   echain.electron_MT                                   
#                                   )
                    
                    signal_electron.append(electron)


            # e and mu should be 1

            if not (len(signal_muon)>=1 and len(signal_electron)>=1):
                ptr_m += nmuon
                ptr_e += nelectron
                ptr_t += ntau
                ptr_vm += nvmuon
                ptr_ve += nvelectron
                ptr_vt += nvtau
                ptr_nb += nbjets
                if pname != 'data': ptr_ng += ngen
                continue

            counter[1] += 1

            lepton_type = "None"

            _muon_ = []
            _electron_ = []


            if options.channel=="electron":
                _muon_ = [ii for ii in signal_muon if ii.pt > 10.]
                _electron_ = [ii for ii in signal_electron if ii.pt > 10.]
            elif options.channel=="muon":                
                _muon_ = [ii for ii in signal_muon if ii.pt > 10.]
                _electron_ = [ii for ii in signal_electron if ii.pt > 10.]



            
            if not (len(_muon_)==1 and len(_electron_)==1):
                ptr_m += nmuon
                ptr_e += nelectron
                ptr_t += ntau
                ptr_vm += nvmuon
                ptr_ve += nvelectron
                ptr_vt += nvtau
                ptr_nb += nbjets
                if pname != 'data': ptr_ng += ngen

                continue

            muon = _muon_[0]
            electron = _electron_[0]
            counter[2] += 1            

            #############################################
            # Tau 

            for it in xrange(ptr_t, ptr_t + ntau):
        
                tchain.LoadTree(it)
                tchain.GetEntry(it)

            
                if (tchain.tau_id and tchain.tau_iso):

                    tau = tool.tauobj(tchain.tau_pt,
                                      tchain.tau_eta,
                                      tchain.tau_phi,
                                      tchain.tau_mass,
                                      tchain.tau_charge,
                                      tchain.dBisolation,
                                      tchain.tau_againstMuTight,
                                      tchain.tau_againstEMedium,
                                      tchain.tau_decaymode,
                                      tchain.tau_ep,
                                      tchain.tau_MT,
                                      tchain.tau_dxy,
                                      tchain.tau_dz,
                                      tchain.tau_dB3D
                                      )


                    if tau.returndR(muon) < 0.5:
                        continue

                    if tau.returndR(electron) < 0.5:
                        continue

                    if tool.diobj(tau, muon).returnmass() > 71.2 and tool.diobj(tau, muon).returnmass() < 111.2:
                        if not (tchain.tau_againstMuTight and
                                ((tchain.tau_decaymode==0 and tchain.tau_ep > 0.2) or (tchain.tau_decaymode!=0))):

                            continue

                    if tool.diobj(tau, electron).returnmass() > 71.2 and tool.diobj(tau, electron).returnmass() < 111.2:
                        if not tchain.tau_againstEMedium:
                            continue
                        
                    signal_tau.append(tau)

                    


            ptr_m += nmuon
            ptr_e += nelectron
            ptr_t += ntau


#            signal_tau = [it for it in signal_tau if it.charge*muon.charge==-1]
            if len(signal_tau)>=1:
                ptr_vm += nvmuon
                ptr_ve += nvelectron
                ptr_vt += nvtau
                ptr_nb += nbjets
                if pname != 'data': ptr_ng += ngen
                continue

            #  VETO
            ######################

            veto_muon = []
            veto_electron = []
            veto_tau = []           
            veto_bjet = []
            gen_particle = []
            
            for im in xrange(ptr_vm, ptr_vm + nvmuon):
        
                vmchain.LoadTree(im)
                vmchain.GetEntry(im)

                vm = tool.easyobj(vmchain.veto_muon_pt,
                             vmchain.veto_muon_eta,
                             vmchain.veto_muon_phi)

                
                if vm.returndR(muon) > 0.4 and \
                       vm.returndR(electron) > 0.4:
                    veto_muon.append(vm)
                

            for ie in xrange(ptr_ve, ptr_ve + nvelectron):
            
                vechain.LoadTree(ie)
                vechain.GetEntry(ie)

                ve = tool.easyobj(vechain.veto_electron_pt,
                             vechain.veto_electron_eta,
                             vechain.veto_electron_phi)
                
                if ve.returndR(muon) > 0.4 and \
                       ve.returndR(electron) > 0.4:
                    veto_electron.append(ve)
                    

            for it in xrange(ptr_vt, ptr_vt + nvtau):
        
                vtchain.LoadTree(it)
                vtchain.GetEntry(it)
                
                vt = tool.easyobj(vtchain.veto_tau_pt,
                             vtchain.veto_tau_eta,
                             vtchain.veto_tau_phi)

                if vt.returndR(muon) > 0.4 and \
                       vt.returndR(electron) > 0.4:
                    
                    veto_tau.append(vt)



            for ib in xrange(ptr_nb, ptr_nb+nbjets):

                bchain.LoadTree(ib)
                bchain.GetEntry(ib)

                bj = tool.easyobj(bchain.bjet_pt,
                             bchain.bjet_eta,
                             bchain.bjet_phi)

#                print 'bjet = ', bj.pt, bj.eta
                if bj.pt > 20 and abs(bj.eta) < 5.0 and  bj.returndR(muon) > 0.4 and bj.returndR(electron) > 0.4:
                    veto_bjet.append(bj)
            

            # generator information
            if pname != 'data':
                for igen in xrange(ptr_ng, ptr_ng+ngen):
                    
                    gchain.LoadTree(igen)
                    gchain.GetEntry(igen)
                    
                    gj = tool.easyobj_gen(gchain.gen_pt,
                                          gchain.gen_eta,
                                          gchain.gen_phi,
                                          gchain.gen_pdgid)
                    gen_particle.append(gj)

            ptr_vm += nvmuon
            ptr_ve += nvelectron
            ptr_vt += nvtau
            ptr_nb += nbjets
            if pname != 'data': ptr_ng += ngen

            if tool.diobj(muon, electron).returnmass() < 20:
                continue

            counter[3] += 1
            
            if not muon.charge*electron.charge==1:
#            if muon.charge*electron.charge==1:
                continue

            counter[4] += 1

            if not (len(veto_muon)==0 and len(veto_electron)==0 and len(veto_tau)==0):
                continue

            counter[5] += 1
            
#            if not ((main.trig_type_M17E8 and muon.pt > 20. and electron.pt > 10. and muon.trigmatch and electron.trigmatch) or \
#                    (main.trig_type_M8E17 and muon.pt > 10. and electron.pt > 20. and muon.trigmatch and electron.trigmatch)
#                    ):
#                
#                continue

            if not ((muon.pt > 20. and electron.pt > 10. and muon.trigmatch and electron.trigmatch) or \
                    (muon.pt > 10. and electron.pt > 20. and muon.trigmatch and electron.trigmatch)
                    ):
                
                continue

            counter[6] += 1
#            if not (len(veto_bjet)) >= 1:
#            if len(veto_bjet) >= 1:
#                continue

            counter[7] += 1


            # PASS ALL THE SELECTIONS !!
            
            weight = 1.
            weight_raw = 1.
            weight_muid = 1.
            weight_eid = 1.
            weight_mutrig = 1.
            weight_etrig = 1.
            
            if pname == 'data':
                pass
            else:
                weight = main.weight*muon.trig*muon.id*electron.trig*electron.id*lum_weight
                weight_raw = lum_weight
                weight_muid = muon.id
                weight_eid = electron.id
                weight_mutrig = muon.trig
                weight_etrig = electron.trig

            if options.channel=="electron":
                var_dict['lepton_pt'][0] = electron.pt
                var_dict['lepton_eta'][0] = electron.eta
                var_dict['lepton_phi'][0] = electron.phi
                var_dict['lepton_mass'][0] = electron.mass
                var_dict['lepton_jetpt'][0] = electron.jetpt
                var_dict['lepton_njet'][0] = electron.njet
                var_dict['lepton_id'][0] = electron.isid 
                var_dict['lepton_iso'][0] = electron.isiso
                var_dict['lepton_reliso'][0] = electron.reliso
                var_dict['lepton_MT'][0] = electron.MT
                var_dict['lepton_charge'][0] = electron.charge
                var_dict['lepton_dpt'][0] = electron.jetpt - electron.pt
                var_dict['lepton_kNN_jetpt'][0] = electron.jetpt
                var_dict['lepton_mva'][0] = electron.new_mva

                threshold = -1.
                if abs(electron.eta) < 1.479:
                    threshold = mva_electron_barrel
                else:
                    threshold = mva_electron_endcap
                    
#                    mva_muon_barrel = 0.0089
#                mva_muon_endcap = 0.0621

                var_dict['lepton_mva_threshold'][0] = threshold
                var_dict['slepton_pt'][0] = muon.pt
                var_dict['slepton_eta'][0] = muon.eta
                var_dict['slepton_phi'][0] = muon.phi
                var_dict['slepton_mass'][0] = muon.mass
                var_dict['slepton_jetpt'][0] = muon.jetpt
                var_dict['slepton_njet'][0] = muon.njet
                var_dict['slepton_id'][0] = muon.isid 
                var_dict['slepton_iso'][0] = muon.isiso
                var_dict['slepton_reliso'][0] = muon.reliso
                var_dict['slepton_MT'][0] = muon.MT
                var_dict['slepton_charge'][0] = muon.charge
                var_dict['slepton_dpt'][0] = muon.jetpt - muon.pt
                var_dict['slepton_kNN_jetpt'][0] = muon.jetpt
                var_dict['slepton_mva'][0] = muon.new_mva
                
                if electron.jetpt == -999:
                    var_dict['lepton_kNN_jetpt'][0] = electron.pt

                if electron.jetpt < electron.pt:
                    var_dict['lepton_kNN_jetpt'][0] = electron.pt
                    
            elif options.channel=="muon":
                var_dict['lepton_pt'][0] = muon.pt
                var_dict['lepton_eta'][0] = muon.eta
                var_dict['lepton_phi'][0] = muon.phi
                var_dict['lepton_mass'][0] = muon.mass
                var_dict['lepton_jetpt'][0] = muon.jetpt
                var_dict['lepton_njet'][0] = muon.njet
                var_dict['lepton_id'][0] = muon.isid 
                var_dict['lepton_iso'][0] = muon.isiso
                var_dict['lepton_reliso'][0] = muon.reliso
                var_dict['lepton_MT'][0] = muon.MT
                var_dict['lepton_charge'][0] = muon.charge
                var_dict['lepton_dpt'][0] = muon.jetpt - muon.pt
                var_dict['lepton_kNN_jetpt'][0] = muon.jetpt
                var_dict['lepton_mva'][0] = muon.new_mva

                threshold = -1.
                if abs(muon.eta) < 1.479:
                    threshold = mva_muon_barrel
                else:
                    threshold = mva_muon_endcap
                    

                var_dict['lepton_mva_threshold'][0] = threshold
                
                var_dict['slepton_pt'][0] = electron.pt
                var_dict['slepton_eta'][0] = electron.eta
                var_dict['slepton_phi'][0] = electron.phi
                var_dict['slepton_mass'][0] = electron.mass
                var_dict['slepton_jetpt'][0] = electron.jetpt
                var_dict['slepton_njet'][0] = electron.njet
                var_dict['slepton_id'][0] = electron.isid 
                var_dict['slepton_iso'][0] = electron.isiso
                var_dict['slepton_reliso'][0] = electron.reliso
                var_dict['slepton_MT'][0] = electron.MT
                var_dict['slepton_charge'][0] = electron.charge
                var_dict['slepton_dpt'][0] = electron.jetpt - electron.pt
                var_dict['slepton_kNN_jetpt'][0] = electron.jetpt
                var_dict['slepton_mva'][0] = electron.new_mva


                if muon.jetpt == -999:
                    var_dict['lepton_kNN_jetpt'][0] = muon.pt

                if muon.jetpt < muon.pt:
                    var_dict['lepton_kNN_jetpt'][0] = muon.pt


            isMC = False
            isMCw = 1.
            
            if pname == 'data':
                pass
            else:
                isMC = True
                isMCw = -1.

            var_dict['evt_weight'][0] = weight
            var_dict['evt_weight_raw'][0] = weight_raw
            
            var_dict['evt_Mem'][0] = tool.diobj(muon, electron).returnmass()
            var_dict['evt_njet'][0] = main.nJets
            var_dict['evt_nbjet'][0] = nbjets
            var_dict['evt_id'][0] = ptype
            var_dict['evt_isMC'][0] = isMC
            var_dict['evt_isMCw'][0] = isMCw
            var_dict['evt_run'][0] = main.run
            var_dict['evt_evt'][0] = main.evt
            var_dict['evt_lum'][0] = main.lumi
            var_dict['evt_met'][0] = main.pfmet
            
            var_dict['evt_weight_muid'][0] = weight_muid
            var_dict['evt_weight_mutrig'][0] = weight_mutrig
            var_dict['evt_weight_eid'][0] = weight_eid
            var_dict['evt_weight_etrig'][0] = weight_etrig

            _lepton_ = None
            _slepton_ = None
            
            if options.channel=="electron":
                _lepton_ = electron
                _slepton_ = muon
            elif options.channel=="muon":
                _lepton_ = muon
                _slepton_ = electron

                
            _lepton_pdgid_ = 0
            _lepton_pdgid_dr_ = 0.5
            _slepton_pdgid_ = 0
            _slepton_pdgid_dr_ = 0.5
            
            if pname != 'data':
                
                for gen in gen_particle:

                    _dR_ = gen.returndR(_lepton_)
                    
                    if _dR_ < _lepton_pdgid_dr_:
                        _lepton_pdgid_dr_ = _dR_
                        _lepton_pdgid_ = gen.pdgid

                    _sdR_ = gen.returndR(_slepton_)
                    
                    if _sdR_ < _slepton_pdgid_dr_:
                        _slepton_pdgid_dr_ = _sdR_
                        _slepton_pdgid_ = gen.pdgid


            var_dict['lepton_pdgid'][0] = _lepton_pdgid_
            var_dict['lepton_pdgid_dr'][0] = _lepton_pdgid_dr_
            var_dict['slepton_pdgid'][0] = _slepton_pdgid_
            var_dict['slepton_pdgid_dr'][0] = _slepton_pdgid_dr_

            t.Fill()

            passed += 1


        print '[INFO] pass, total, eff = ', passed, '/' , total

        for ic in range(len(counter)):
            print '[INFO] cutflow : ', ic, counter[ic]

        ofile.Write()
        ofile.Close()

