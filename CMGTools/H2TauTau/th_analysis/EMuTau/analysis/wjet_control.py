#################################
# 
# 12 Nov 2013
# Y.Takahashi (Yuta.Takahashi@cern.ch)
# 
# This is the analyzer to obtain control samples for the kNN training
# python analysis_antiTau.py --mode (antiMu, antiE, antiEMu, signal)
#
#################################

import math, sys, array
import numpy as num
from ROOT import TFile, TH1F, gDirectory, TMVA, TTree, Double
from ROOT import TLorentzVector, Double # for M(l2,tau) calculation
import optparse
import config as tool

### For options
parser = optparse.OptionParser()
parser.add_option('--channel', action="store", dest="channel", default='muon') # muon means jet->muon fake sample
parser.add_option('--phys', action="store", dest="phys", default='data') # muon means jet->muon fake sample
options, args = parser.parse_args()

print 
print '[INFO] Analysis channel = ', options.channel


process = [options.phys]

db = tool.ReadFile(process)
filedict = db.returnFile()

mva_muon_barrel = 0.0089
mva_electron_barrel = 0.0649

mva_muon_endcap = 0.0621
mva_electron_endcap = 0.0891


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

        lepton_pt = num.zeros(1, dtype=float)
        lepton_eta = num.zeros(1, dtype=float)
        lepton_phi = num.zeros(1, dtype=float)
        lepton_mass = num.zeros(1, dtype=float)
        lepton_jetpt = num.zeros(1, dtype=float)
        lepton_kNN_jetpt = num.zeros(1, dtype=float)
        lepton_njet = num.zeros(1, dtype=int)
        lepton_id = num.zeros(1, dtype=int)
        lepton_iso = num.zeros(1, dtype=int)
        lepton_reliso = num.zeros(1, dtype=float)
        lepton_MT = num.zeros(1, dtype=float)
        lepton_charge = num.zeros(1, dtype=int)
        lepton_dpt = num.zeros(1, dtype=float)
        lepton_mva = num.zeros(1, dtype=float)
        lepton_mva_threshold = num.zeros(1, dtype=float)
    
        slepton_pt = num.zeros(1, dtype=float)
        slepton_eta = num.zeros(1, dtype=float)
        slepton_phi = num.zeros(1, dtype=float)
        slepton_mass = num.zeros(1, dtype=float)
        slepton_jetpt = num.zeros(1, dtype=float)
        slepton_kNN_jetpt = num.zeros(1, dtype=float)
        slepton_njet = num.zeros(1, dtype=int)
        slepton_id = num.zeros(1, dtype=int)
        slepton_iso = num.zeros(1, dtype=int)
        slepton_reliso = num.zeros(1, dtype=float)
        slepton_MT = num.zeros(1, dtype=float)
        slepton_charge = num.zeros(1, dtype=int)
        slepton_dpt = num.zeros(1, dtype=float)
        slepton_mva = num.zeros(1, dtype=float)
        
        evt_weight = num.zeros(1, dtype=float)
        evt_weight_raw = num.zeros(1, dtype=float)
        evt_weight_muid = num.zeros(1, dtype=float)
        evt_weight_mutrig = num.zeros(1, dtype=float)
        evt_weight_eid = num.zeros(1, dtype=float)
        evt_weight_etrig = num.zeros(1, dtype=float)

        evt_Mem = num.zeros(1, dtype=float)
        evt_run = num.zeros(1, dtype=int)
        evt_evt = num.zeros(1, dtype=int)
        evt_lum = num.zeros(1, dtype=int)
        evt_njet = num.zeros(1, dtype=int)
        evt_isMC = num.zeros(1, dtype=int)
        evt_isMCw = num.zeros(1, dtype=float)
        evt_id = num.zeros(1, dtype=int)
        evt_met = num.zeros(1, dtype=float)
        
        t.Branch('lepton_pt',lepton_pt,'lepton_pt/D')
        t.Branch('lepton_eta',lepton_eta,'lepton_eta/D')
        t.Branch('lepton_phi',lepton_phi,'lepton_phi/D')
        t.Branch('lepton_mass', lepton_mass, 'lepton_mass/D')
        t.Branch('lepton_jetpt',lepton_jetpt, 'lepton_jetpt/D')
        t.Branch('lepton_kNN_jetpt',lepton_kNN_jetpt, 'lepton_kNN_jetpt/D')
        t.Branch('lepton_njet',lepton_njet, 'lepton_njet/I')
        t.Branch('lepton_id', lepton_id, 'lepton_id/I')
        t.Branch('lepton_iso', lepton_iso, 'lepton_iso/I')
        t.Branch('lepton_reliso', lepton_reliso, 'lepton_reliso/D')
        t.Branch('lepton_MT', lepton_MT, 'lepton_MT/D')
        t.Branch('lepton_charge', lepton_charge, 'lepton_charge/I')
        t.Branch('lepton_dpt', lepton_dpt, 'lepton_dpt/D')
        t.Branch('lepton_mva', lepton_mva, 'lepton_mva/D')
        t.Branch('lepton_mva_threshold', lepton_mva_threshold, 'lepton_mva_threshold/D')

        t.Branch('slepton_pt',slepton_pt,'slepton_pt/D')
        t.Branch('slepton_eta',slepton_eta,'slepton_eta/D')
        t.Branch('slepton_phi',slepton_phi,'slepton_phi/D')
        t.Branch('slepton_mass', slepton_mass, 'slepton_mass/D')
        t.Branch('slepton_jetpt',slepton_jetpt, 'slepton_jetpt/D')
        t.Branch('slepton_kNN_jetpt',slepton_kNN_jetpt, 'slepton_kNN_jetpt/D')
        t.Branch('slepton_njet',slepton_njet, 'slepton_njet/I')
        t.Branch('slepton_id', slepton_id, 'slepton_id/I')
        t.Branch('slepton_iso', slepton_iso, 'slepton_iso/I')
        t.Branch('slepton_reliso', slepton_reliso, 'slepton_reliso/D')
        t.Branch('slepton_MT', slepton_MT, 'slepton_MT/D')
        t.Branch('slepton_charge', slepton_charge, 'slepton_charge/I')
        t.Branch('slepton_dpt', slepton_dpt, 'slepton_dpt/D')
        t.Branch('slepton_mva', slepton_mva, 'slepton_mva/D')
        
        t.Branch('evt_Mem', evt_Mem, 'evt_Mem/D')
        t.Branch('evt_weight', evt_weight, 'evt_weight/D')
        t.Branch('evt_weight_raw', evt_weight_raw, 'evt_weight_raw/D')
        t.Branch('evt_weight_muid', evt_weight_muid, 'evt_weight_muid/D')
        t.Branch('evt_weight_eid', evt_weight_eid, 'evt_weight_eid/D')
        t.Branch('evt_weight_mutrig', evt_weight_mutrig, 'evt_weight_mutrig/D')
        t.Branch('evt_weight_etrig', evt_weight_etrig, 'evt_weight_etrig/D')
        
        t.Branch('evt_njet', evt_njet, 'evt_njet/I')
        t.Branch('evt_isMC', evt_isMC, 'evt_isMC/I')
        t.Branch('evt_isMCw', evt_isMCw, 'evt_isMCw/D')
        t.Branch('evt_id', evt_id, 'evt_id/I')
        t.Branch('evt_run', evt_run, 'evt_run/I')
        t.Branch('evt_evt', evt_evt, 'evt_evt/I')
        t.Branch('evt_lum', evt_lum, 'evt_lum/I')
        t.Branch('evt_met', evt_met, 'evt_met/D')
        
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

        ptr_m = 0        
        ptr_e = 0
        ptr_t = 0
        
        ptr_vm = 0      
        ptr_ve = 0
        ptr_vt = 0

        ptr_nb = 0
        
        Total = main.GetEntries()
        Passed = 0

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

            # for real Leptons
            signal_muon = []
            signal_electron = []
            signal_tau = []
            
            for im in xrange(ptr_m, ptr_m + nmuon):
                mchain.LoadTree(im)
                mchain.GetEntry(im)
                

                mva_mvar_map['bdt_muon_dxy'][0] = mchain.muon_dxy
                mva_mvar_map['bdt_muon_dz'][0] = mchain.muon_dz
                mva_mvar_map['bdt_muon_mva_ch_iso'][0] = mchain.muon_mva_ch_iso
                mva_mvar_map['bdt_muon_mva_neu_iso'][0] = mchain.muon_mva_neu_iso
                mva_mvar_map['bdt_muon_mva_jet_dr'][0] = mchain.muon_mva_jet_dr
                mva_mvar_map['bdt_muon_mva_ptratio'][0] = mchain.muon_mva_ptratio
                mva_mvar_map['bdt_muon_mva_csv'][0] = mchain.muon_mva_csv
                
                mva_iso_muon = mva_muonreader.EvaluateMVA('mva_muon_data')

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
                                     mchain.muon_dxy,
                                     mchain.muon_dz,
                                     mchain.muon_dB3D,
                                     mchain.muon_jetcsv,
                                     mchain.muon_jetcsv_10,
                                     mchain.muon_mva,
                                     mchain.muon_mva_ch_iso,
                                     mchain.muon_mva_neu_iso,
                                     mchain.muon_mva_jet_dr,
                                     mchain.muon_mva_ptratio,
                                     mchain.muon_mva_csv,
                                     mva_iso_muon
                                    )

#                    muon = tool.obj(mchain.muon_pt,
#                                    mchain.muon_eta,
#                                    mchain.muon_phi,
#                                    mchain.muon_mass,
#                                    mchain.muon_jetpt,
#                                    mchain.muon_njet,
#                                    mchain.muon_charge,
#                                    mchain.muon_trigmatch,
#                                    mchain.muon_trig_weight,
#                                    mchain.muon_id_weight,
#                                    mchain.muon_id,
#                                    mchain.muon_iso,
#                                    mchain.muon_reliso,
#                                    mchain.muon_MT)
                        
                    signal_muon.append(muon)


            for ie in xrange(ptr_e, ptr_e + nelectron):
                echain.LoadTree(ie)
                echain.GetEntry(ie)
                
                mva_evar_map['bdt_electron_mva_score'][0] = echain.electron_mva_score
                mva_evar_map['bdt_electron_mva_ch_iso'][0] = echain.electron_mva_ch_iso
                mva_evar_map['bdt_electron_mva_neu_iso'][0] = echain.electron_mva_neu_iso
                mva_evar_map['bdt_electron_mva_jet_dr'][0] = echain.electron_mva_jet_dr
                mva_evar_map['bdt_electron_mva_ptratio'][0] = echain.electron_mva_ptratio
                mva_evar_map['bdt_electron_mva_csv'][0] = echain.electron_mva_csv
                
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
                                         echain.electron_dxy,
                                         echain.electron_dz,
                                         echain.electron_dB3D,
                                         echain.electron_jetcsv,
                                         echain.electron_jetcsv_10,
                                         echain.electron_mva,
                                         echain.electron_mva_ch_iso,
                                         echain.electron_mva_neu_iso,
                                         echain.electron_mva_jet_dr,
                                         echain.electron_mva_ptratio,
                                         echain.electron_mva_csv,
                                         echain.electron_mva_score,
                                         echain.electron_mva_numberOfHits,
                                         mva_iso_electron
                                         )

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

#                    tau = tool.obj(tchain.tau_pt,
#                                   tchain.tau_eta,
#                                   tchain.tau_phi,
#                                   tchain.tau_mass,
#                                   1,1,
#                                   tchain.tau_charge,1,1,1,1,1,1,1)

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
                continue

            #  VETO
            ######################

            veto_muon = []
            veto_electron = []
            veto_tau = []           
            veto_bjet = []
            
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
                    
            ptr_vm += nvmuon
            ptr_ve += nvelectron
            ptr_vt += nvtau
            ptr_nb += nbjets

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
                lepton_pt    [0] = electron.pt
                lepton_eta   [0] = electron.eta
                lepton_phi   [0] = electron.phi
                lepton_mass  [0] = electron.mass
                lepton_jetpt [0] = electron.jetpt
                lepton_njet  [0] = electron.njet
                lepton_id    [0] = electron.isid 
                lepton_iso   [0] = electron.isiso
                lepton_reliso[0] = electron.reliso
                lepton_MT    [0] = electron.MT
                lepton_charge[0] = electron.charge
                lepton_dpt   [0] = electron.jetpt - electron.pt
                lepton_kNN_jetpt [0] = electron.jetpt
                lepton_mva [0] = electron.new_mva

                threshold = -1.
                if abs(electron.eta) < 1.479:
                    threshold = 0.0649
                else:
                    threshold = 0.0891
                    
#                    mva_muon_barrel = 0.0089
#                mva_muon_endcap = 0.0621


                lepton_mva_threshold [0] = threshold

                slepton_pt    [0] = muon.pt
                slepton_eta   [0] = muon.eta
                slepton_phi   [0] = muon.phi
                slepton_mass  [0] = muon.mass
                slepton_jetpt [0] = muon.jetpt
                slepton_njet  [0] = muon.njet
                slepton_id    [0] = muon.isid 
                slepton_iso   [0] = muon.isiso
                slepton_reliso[0] = muon.reliso
                slepton_MT    [0] = muon.MT
                slepton_charge[0] = muon.charge
                slepton_dpt   [0] = muon.jetpt - muon.pt
                slepton_kNN_jetpt [0] = muon.jetpt
                slepton_mva [0] = muon.new_mva
                
                if electron.jetpt == -999:
                    lepton_kNN_jetpt [0] = electron.pt

                if electron.jetpt < electron.pt:
                    lepton_kNN_jetpt [0] = electron.pt
                    
            elif options.channel=="muon":
                lepton_pt    [0] = muon.pt
                lepton_eta   [0] = muon.eta
                lepton_phi   [0] = muon.phi
                lepton_mass  [0] = muon.mass
                lepton_jetpt [0] = muon.jetpt
                lepton_njet  [0] = muon.njet
                lepton_id    [0] = muon.isid 
                lepton_iso   [0] = muon.isiso
                lepton_reliso[0] = muon.reliso
                lepton_MT    [0] = muon.MT
                lepton_charge[0] = muon.charge
                lepton_dpt   [0] = muon.jetpt - muon.pt
                lepton_kNN_jetpt [0] = muon.jetpt
                lepton_mva [0] = muon.new_mva

                threshold = -1.
                if abs(muon.eta) < 1.479:
                    threshold = 0.0089
                else:
                    threshold = 0.0621
                    

                lepton_mva_threshold [0] = threshold
                
                slepton_pt    [0] = electron.pt
                slepton_eta   [0] = electron.eta
                slepton_phi   [0] = electron.phi
                slepton_mass  [0] = electron.mass
                slepton_jetpt [0] = electron.jetpt
                slepton_njet  [0] = electron.njet
                slepton_id    [0] = electron.isid 
                slepton_iso   [0] = electron.isiso
                slepton_reliso[0] = electron.reliso
                slepton_MT    [0] = electron.MT
                slepton_charge[0] = electron.charge
                slepton_dpt   [0] = electron.jetpt - electron.pt
                slepton_kNN_jetpt [0] = electron.jetpt
                slepton_mva [0] = electron.new_mva


                if muon.jetpt == -999:
                    lepton_kNN_jetpt [0] = muon.pt

                if muon.jetpt < muon.pt:
                    lepton_kNN_jetpt [0] = muon.pt


            isMC = False
            isMCw = 1.
            
            if pname == 'data':
                pass
            else:
                isMC = True
                isMCw = -1.

            evt_weight[0] = weight
            evt_weight_raw[0] = weight_raw
            
            evt_Mem   [0] = tool.diobj(muon, electron).returnmass()
            evt_njet [0] = main.nJets
            evt_id [0] = ptype
            evt_isMC [0] = isMC
            evt_isMCw [0] = isMCw
            evt_run[0] = main.run
            evt_evt[0] = main.evt
            evt_lum[0] = main.lumi
            evt_met[0] = main.pfmet
            
            evt_weight_muid[0] = weight_muid
            evt_weight_mutrig[0] = weight_mutrig
            evt_weight_eid[0] = weight_eid
            evt_weight_etrig[0] = weight_etrig

            t.Fill()

            Passed += 1


        print '[INFO] pass, total, eff = ', Passed, '/' , Total

        for ic in range(len(counter)):
            print '[INFO] cutflow : ', ic, counter[ic]

        ofile.Write()
        ofile.Close()

