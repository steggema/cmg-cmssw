import math, sys, array
import numpy as num
from ROOT import TFile, gDirectory, TH1F, gStyle, gROOT, TTree, TMVA, Double
import math, copy, sys, array
import optparse

process_dict = {'WW':0,
                'WZ':1,
                'ZZ':2,
                'tt0l':3,
                'tt1l':4,
                'tt2l':5,
                'DY':6,
                'DY1':7,
                'DY2':8,
                'DY3':9,
                'DY4':10,
                'Wjet':11,
                'W1jet':12,
                'W2jet':13,
                'W3jet':14,
                'W4jet':15,
                'tH_YtMinus1':16,
                'TTW':17,
                'TTZ':18,
                'TTH':19,
                'redbkg':20,
                'tW':21,
                'tbW':22,
                't_tchan':23,
                'tbar_tchan':24,
                'data':100};

process = ['WW',
           'WZ',
           'ZZ',
           'tt0l',
           'tt1l',
           'tt2l',
           'DY',
           'DY1',
           'DY2',
           'DY3',
           'DY4',
           'Wjet',
           'W1jet',
           'W2jet',
           'W3jet',
           'W4jet',
#           'tH_YtMinus1',
           'TTW',
           'TTZ',
           'TTH',
           'tW',
           'tbW',
           't_tchan',
           'tbar_tchan',
           ]
#           'data']


useTT = False

region = ['signal']

directory = 'root_process'


### For options
parser = optparse.OptionParser()
parser.add_option('--cr', action="store", dest="cr", default='f12')
options, args = parser.parse_args()

print '[INFO] Control region = ', options.cr

gROOT.SetBatch(True)


outputfile = ''
outputfile = 'BDT_training_ss_' + options.cr + '.root'
    
file = TFile(outputfile,'recreate')
t = TTree('Tree','Tree')
        
bdt_muon_pt = num.zeros(1, dtype=num.float32)
bdt_muon_eta = num.zeros(1, dtype=num.float32)
bdt_muon_phi = num.zeros(1, dtype=num.float32)
bdt_muon_mass = num.zeros(1, dtype=num.float32)
bdt_muon_jetpt = num.zeros(1, dtype=num.float32)
bdt_muon_jet_csv = num.zeros(1, dtype=num.float32)
bdt_muon_jet_csv_10 = num.zeros(1, dtype=num.float32)
bdt_muon_id = num.zeros(1, dtype=num.float32)
bdt_muon_iso = num.zeros(1, dtype=num.float32)
bdt_muon_reliso = num.zeros(1, dtype=num.float32)
bdt_muon_MT = num.zeros(1, dtype=num.float32)
bdt_muon_charge = num.zeros(1, dtype=num.float32)
bdt_muon_dpt = num.zeros(1, dtype=num.float32)
bdt_muon_pdg = num.zeros(1, dtype=num.float32)
bdt_muon_dxy = num.zeros(1, dtype=num.float32)
bdt_muon_dz = num.zeros(1, dtype=num.float32)
bdt_muon_dB3D = num.zeros(1, dtype=num.float32)
bdt_muon_mva = num.zeros(1, dtype=num.float32)
bdt_muon_mva_ch_iso = num.zeros(1, dtype=num.float32)
bdt_muon_mva_neu_iso = num.zeros(1, dtype=num.float32)
bdt_muon_mva_jet_dr = num.zeros(1, dtype=num.float32)
bdt_muon_mva_ptratio = num.zeros(1, dtype=num.float32)
bdt_muon_mva_csv = num.zeros(1, dtype=num.float32)


bdt_smuon_pt = num.zeros(1, dtype=num.float32)
bdt_smuon_eta = num.zeros(1, dtype=num.float32)
bdt_smuon_phi = num.zeros(1, dtype=num.float32)
bdt_smuon_mass = num.zeros(1, dtype=num.float32)
bdt_smuon_jetpt = num.zeros(1, dtype=num.float32)
bdt_smuon_jet_csv = num.zeros(1, dtype=num.float32)
bdt_smuon_jet_csv_10 = num.zeros(1, dtype=num.float32)
bdt_smuon_id = num.zeros(1, dtype=num.float32)
bdt_smuon_iso = num.zeros(1, dtype=num.float32)
bdt_smuon_reliso = num.zeros(1, dtype=num.float32)
bdt_smuon_MT = num.zeros(1, dtype=num.float32)
bdt_smuon_charge = num.zeros(1, dtype=num.float32)
bdt_smuon_dpt = num.zeros(1, dtype=num.float32)
bdt_smuon_pdg = num.zeros(1, dtype=num.float32)
bdt_smuon_dxy = num.zeros(1, dtype=num.float32)
bdt_smuon_dz = num.zeros(1, dtype=num.float32)
bdt_smuon_dB3D = num.zeros(1, dtype=num.float32)
bdt_smuon_mva = num.zeros(1, dtype=num.float32)
bdt_smuon_mva_ch_iso = num.zeros(1, dtype=num.float32)
bdt_smuon_mva_neu_iso = num.zeros(1, dtype=num.float32)
bdt_smuon_mva_jet_dr = num.zeros(1, dtype=num.float32)
bdt_smuon_mva_ptratio = num.zeros(1, dtype=num.float32)
bdt_smuon_mva_csv = num.zeros(1, dtype=num.float32)



    
bdt_tau_pt = num.zeros(1, dtype=num.float32)
bdt_tau_eta = num.zeros(1, dtype=num.float32)
bdt_tau_phi = num.zeros(1, dtype=num.float32)
bdt_tau_mass = num.zeros(1, dtype=num.float32)
bdt_tau_charge = num.zeros(1, dtype=num.float32)
bdt_tau_MT = num.zeros(1, dtype=num.float32)
bdt_tau_isolation = num.zeros(1, dtype=num.float32)
bdt_tau_decaymode = num.zeros(1, dtype=num.float32)
bdt_tau_pdg = num.zeros(1, dtype=num.float32)
bdt_tau_jet_csv = num.zeros(1, dtype=num.float32)
bdt_tau_dxy = num.zeros(1, dtype=num.float32)
bdt_tau_dz = num.zeros(1, dtype=num.float32)
bdt_tau_dB3D = num.zeros(1, dtype=num.float32)


bdt_evt_weight = num.zeros(1, dtype=num.float32)
bdt_evt_Mmm = num.zeros(1, dtype=num.float32)
bdt_evt_Msmt = num.zeros(1, dtype=num.float32)
bdt_evt_Mmt = num.zeros(1, dtype=num.float32)
bdt_evt_dphi_metmu = num.zeros(1, dtype=num.float32)
bdt_evt_dphi_mete = num.zeros(1, dtype=num.float32)
bdt_evt_dphi_mettau = num.zeros(1, dtype=num.float32)
bdt_evt_met = num.zeros(1, dtype=num.float32)
bdt_evt_LT = num.zeros(1, dtype=num.float32)
bdt_evt_L2T = num.zeros(1, dtype=num.float32)    
bdt_evt_sumjetpt = num.zeros(1, dtype=num.float32)
bdt_evt_HT = num.zeros(1, dtype=num.float32)
bdt_evt_H = num.zeros(1, dtype=num.float32)
bdt_evt_centrality = num.zeros(1, dtype=num.float32)
bdt_evt_maxMT = num.zeros(1, dtype=num.float32)
bdt_evt_deltaeta = num.zeros(1, dtype=num.float32)
bdt_evt_deltaeta_notau = num.zeros(1, dtype=num.float32)
bdt_evt_njet = num.zeros(1, dtype=num.float32)
bdt_evt_njet_or = num.zeros(1, dtype=num.float32)
bdt_evt_max_jet_eta = num.zeros(1, dtype=num.float32)
bdt_evt_njet_or30 = num.zeros(1, dtype=num.float32)
bdt_evt_max_jet_eta30 = num.zeros(1, dtype=num.float32)
bdt_evt_nbjet = num.zeros(1, dtype=num.float32)
bdt_evt_nbjet10 = num.zeros(1, dtype=num.float32)
bdt_evt_nvetobjet = num.zeros(1, dtype=num.float32)
bdt_evt_isMC = num.zeros(1, dtype=num.float32)
bdt_evt_id = num.zeros(1, dtype=num.float32)
bdt_evt_run = num.zeros(1, dtype=num.float32)
bdt_evt_evt = num.zeros(1, dtype=num.float32)
bdt_evt_lum = num.zeros(1, dtype=num.float32)
bdt_evt_ncmb = num.zeros(1, dtype=num.float32)
bdt_evt_missing_et = num.zeros(1, dtype=num.float32)
bdt_evt_missing_phi = num.zeros(1, dtype=num.float32)
bdt_evt_leading_btag = num.zeros(1, dtype=num.float32)
bdt_evt_sleading_btag = num.zeros(1, dtype=num.float32)
bdt_evt_leading_nbtag = num.zeros(1, dtype=num.float32)
bdt_evt_sleading_nbtag = num.zeros(1, dtype=num.float32)
bdt_evt_leading_btag_pt = num.zeros(1, dtype=num.float32)
bdt_evt_sleading_btag_pt = num.zeros(1, dtype=num.float32)
bdt_evt_isSignal = num.zeros(1, dtype=num.float32)
bdt_evt_processid = num.zeros(1, dtype=num.float32)
bdt_evt_processid_rindex = num.zeros(1, dtype=num.float32)
bdt_evt_sphericity = num.zeros(1, dtype=num.float32)
bdt_evt_aplanarity = num.zeros(1, dtype=num.float32)
bdt_evt_dr_smujet = num.zeros(1, dtype=num.float32)
bdt_evt_dr_mujet = num.zeros(1, dtype=num.float32)
bdt_evt_dr_taujet = num.zeros(1, dtype=num.float32)
bdt_evt_dr_smujet_csv = num.zeros(1, dtype=num.float32)
bdt_evt_dr_mujet_csv = num.zeros(1, dtype=num.float32)
bdt_evt_dr_taujet_csv = num.zeros(1, dtype=num.float32)


t.Branch('bdt_muon_pt',bdt_muon_pt,'bdt_muon_pt/F')
t.Branch('bdt_muon_eta',bdt_muon_eta,'bdt_muon_eta/F')
t.Branch('bdt_muon_phi',bdt_muon_phi,'bdt_muon_phi/F')
t.Branch('bdt_muon_mass', bdt_muon_mass, 'bdt_muon_mass/F')
t.Branch('bdt_muon_jetpt',bdt_muon_jetpt, 'bdt_muon_jetpt/F')
t.Branch('bdt_muon_jet_csv',bdt_muon_jet_csv, 'bdt_muon_jet_csv/F')
t.Branch('bdt_muon_jet_csv_10',bdt_muon_jet_csv_10, 'bdt_muon_jet_csv_10/F')
t.Branch('bdt_muon_id', bdt_muon_id, 'bdt_muon_id/F')
t.Branch('bdt_muon_iso', bdt_muon_iso, 'bdt_muon_iso/F')
t.Branch('bdt_muon_reliso', bdt_muon_reliso, 'bdt_muon_reliso/F')
t.Branch('bdt_muon_MT', bdt_muon_MT, 'bdt_muon_MT/F')
t.Branch('bdt_muon_charge', bdt_muon_charge, 'bdt_muon_charge/F')
t.Branch('bdt_muon_dpt', bdt_muon_dpt, 'bdt_muon_dpt/F')
t.Branch('bdt_muon_pdg', bdt_muon_pdg, 'bdt_muon_pdg/F')
t.Branch('bdt_muon_dxy', bdt_muon_dxy, 'bdt_muon_dxy/F')
t.Branch('bdt_muon_dz', bdt_muon_dz, 'bdt_muon_dz/F')
t.Branch('bdt_muon_dB3D', bdt_muon_dB3D, 'bdt_muon_dB3D/F')
t.Branch('bdt_muon_mva', bdt_muon_mva, 'bdt_muon_mva/F')
t.Branch('bdt_muon_mva_ch_iso', bdt_muon_mva_ch_iso, 'bdt_muon_mva_ch_iso/F')
t.Branch('bdt_muon_mva_neu_iso', bdt_muon_mva_neu_iso, 'bdt_muon_mva_neu_iso/F')
t.Branch('bdt_muon_mva_jet_dr', bdt_muon_mva_jet_dr, 'bdt_muon_mva_jet_dr/F')
t.Branch('bdt_muon_mva_ptratio', bdt_muon_mva_ptratio, 'bdt_muon_mva_ptratio/F')
t.Branch('bdt_muon_mva_csv', bdt_muon_mva_csv, 'bdt_muon_mva_csv/F')


t.Branch('bdt_smuon_pt',bdt_smuon_pt,'bdt_smuon_pt/F')
t.Branch('bdt_smuon_eta',bdt_smuon_eta,'bdt_smuon_eta/F')
t.Branch('bdt_smuon_phi',bdt_smuon_phi,'bdt_smuon_phi/F')
t.Branch('bdt_smuon_mass', bdt_smuon_mass, 'bdt_smuon_mass/F')
t.Branch('bdt_smuon_jetpt',bdt_smuon_jetpt, 'bdt_smuon_jetpt/F')
t.Branch('bdt_smuon_jet_csv',bdt_smuon_jet_csv, 'bdt_smuon_jet_csv/F')
t.Branch('bdt_smuon_jet_csv_10',bdt_smuon_jet_csv_10, 'bdt_smuon_jet_csv_10/F')
t.Branch('bdt_smuon_id', bdt_smuon_id, 'bdt_smuon_id/F')
t.Branch('bdt_smuon_iso', bdt_smuon_iso, 'bdt_smuon_iso/F')
t.Branch('bdt_smuon_reliso', bdt_smuon_reliso, 'bdt_smuon_reliso/F')
t.Branch('bdt_smuon_MT', bdt_smuon_MT, 'bdt_smuon_MT/F')
t.Branch('bdt_smuon_charge', bdt_smuon_charge, 'bdt_smuon_charge/F')
t.Branch('bdt_smuon_dpt', bdt_smuon_dpt, 'bdt_smuon_dpt/F')
t.Branch('bdt_smuon_pdg', bdt_smuon_pdg, 'bdt_smuon_pdg/F')
t.Branch('bdt_smuon_dxy', bdt_smuon_dxy, 'bdt_smuon_dxy/F')
t.Branch('bdt_smuon_dz', bdt_smuon_dz, 'bdt_smuon_dz/F')
t.Branch('bdt_smuon_dB3D', bdt_smuon_dB3D, 'bdt_smuon_dB3D/F')
t.Branch('bdt_smuon_mva', bdt_smuon_mva, 'bdt_smuon_mva/F')
t.Branch('bdt_smuon_mva_ch_iso', bdt_smuon_mva_ch_iso, 'bdt_smuon_mva_ch_iso/F')
t.Branch('bdt_smuon_mva_neu_iso', bdt_smuon_mva_neu_iso, 'bdt_smuon_mva_neu_iso/F')
t.Branch('bdt_smuon_mva_jet_dr', bdt_smuon_mva_jet_dr, 'bdt_smuon_mva_jet_dr/F')
t.Branch('bdt_smuon_mva_ptratio', bdt_smuon_mva_ptratio, 'bdt_smuon_mva_ptratio/F')
t.Branch('bdt_smuon_mva_csv', bdt_smuon_mva_csv, 'bdt_smuon_mva_csv/F')





t.Branch('bdt_tau_pt',bdt_tau_pt,'bdt_tau_pt/F')
t.Branch('bdt_tau_eta',bdt_tau_eta,'bdt_tau_eta/F')
t.Branch('bdt_tau_phi',bdt_tau_phi,'bdt_tau_phi/F')
t.Branch('bdt_tau_mass', bdt_tau_mass, 'bdt_tau_mass/F')
t.Branch('bdt_tau_charge', bdt_tau_charge, 'bdt_tau_charge/F')
t.Branch('bdt_tau_MT', bdt_tau_MT, 'bdt_tau_MT/F')
t.Branch('bdt_tau_decaymode', bdt_tau_decaymode, 'bdt_tau_decaymode/F')
t.Branch('bdt_tau_isolation', bdt_tau_isolation, 'bdt_tau_isolation/F')
t.Branch('bdt_tau_pdg', bdt_tau_pdg, 'bdt_tau_pdg/F')
t.Branch('bdt_tau_jet_csv', bdt_tau_jet_csv, 'bdt_tau_jet_csv/F')
t.Branch('bdt_tau_dxy', bdt_tau_dxy, 'bdt_tau_dxy/F')
t.Branch('bdt_tau_dz', bdt_tau_dz, 'bdt_tau_dz/F')
t.Branch('bdt_tau_dB3D', bdt_tau_dB3D, 'bdt_tau_dB3D/F')

t.Branch('bdt_evt_weight', bdt_evt_weight, 'bdt_evt_weight/F')
t.Branch('bdt_evt_Mmm', bdt_evt_Mmm, 'bdt_evt_Mmm/F')
t.Branch('bdt_evt_Mmt', bdt_evt_Mmt, 'bdt_evt_Mmt/F')
t.Branch('bdt_evt_Msmt', bdt_evt_Msmt, 'bdt_evt_Msmt/F')

t.Branch('bdt_evt_dphi_metmu', bdt_evt_dphi_metmu, 'bdt_evt_dphi_metmu/F')
t.Branch('bdt_evt_dphi_mete', bdt_evt_dphi_mete, 'bdt_evt_dphi_mete/F')
t.Branch('bdt_evt_dphi_mettau', bdt_evt_dphi_mettau, 'bdt_evt_dphi_mettau/F')

t.Branch('bdt_evt_LT', bdt_evt_LT, 'bdt_evt_LT/F')
t.Branch('bdt_evt_L2T', bdt_evt_L2T, 'bdt_evt_L2T/F')
t.Branch('bdt_evt_sumjetpt', bdt_evt_sumjetpt, 'bdt_evt_sumjetpt/F')
t.Branch('bdt_evt_HT', bdt_evt_HT, 'bdt_evt_HT/F')
t.Branch('bdt_evt_H', bdt_evt_H, 'bdt_evt_H/F')
t.Branch('bdt_evt_centrality', bdt_evt_centrality, 'bdt_evt_centrality/F')
t.Branch('bdt_evt_maxMT', bdt_evt_maxMT, 'bdt_evt_maxMT/F')
t.Branch('bdt_evt_deltaeta', bdt_evt_deltaeta, 'bdt_evt_deltaeta/F')
t.Branch('bdt_evt_deltaeta_notau', bdt_evt_deltaeta_notau, 'bdt_evt_deltaeta_notau/F')
t.Branch('bdt_evt_njet', bdt_evt_njet, 'bdt_evt_njet/F')
t.Branch('bdt_evt_njet_or', bdt_evt_njet_or, 'bdt_evt_njet_or/F')
t.Branch('bdt_evt_njet_or30', bdt_evt_njet_or30, 'bdt_evt_njet_or30/F')
t.Branch('bdt_evt_max_jet_eta', bdt_evt_max_jet_eta, 'bdt_evt_max_jet_eta/F')
t.Branch('bdt_evt_max_jet_eta30', bdt_evt_max_jet_eta30, 'bdt_evt_max_jet_eta30/F')
t.Branch('bdt_evt_nbjet', bdt_evt_nbjet, 'bdt_evt_nbjet/F')
t.Branch('bdt_evt_nbjet10', bdt_evt_nbjet10, 'bdt_evt_nbjet10/F')
t.Branch('bdt_evt_nvetobjet', bdt_evt_nvetobjet, 'bdt_evt_nvetobjet/F')
t.Branch('bdt_evt_isMC', bdt_evt_isMC, 'bdt_evt_isMC/F')
t.Branch('bdt_evt_id', bdt_evt_id, 'bdt_evt_id/F')
t.Branch('bdt_evt_run', bdt_evt_run, 'bdt_evt_run/F')
t.Branch('bdt_evt_evt', bdt_evt_evt, 'bdt_evt_evt/F')
t.Branch('bdt_evt_lum', bdt_evt_lum, 'bdt_evt_lum/F')
t.Branch('bdt_evt_ncmb', bdt_evt_ncmb, 'bdt_evt_ncmb/F')
t.Branch('bdt_evt_missing_et', bdt_evt_missing_et, 'bdt_evt_missing_et/F')
t.Branch('bdt_evt_missing_phi', bdt_evt_missing_phi, 'bdt_evt_missing_phi/F')
t.Branch('bdt_evt_leading_btag', bdt_evt_leading_btag, 'bdt_evt_leading_btag/F')
t.Branch('bdt_evt_sleading_btag', bdt_evt_sleading_btag, 'bdt_evt_sleading_btag/F')
t.Branch('bdt_evt_leading_nbtag', bdt_evt_leading_nbtag, 'bdt_evt_leading_nbtag/F')
t.Branch('bdt_evt_sleading_nbtag', bdt_evt_sleading_nbtag, 'bdt_evt_sleading_nbtag/F')
t.Branch('bdt_evt_leading_btag_pt', bdt_evt_leading_btag_pt, 'bdt_evt_leading_btag_pt/F')
t.Branch('bdt_evt_sleading_btag_pt', bdt_evt_sleading_btag_pt, 'bdt_evt_sleading_btag_pt/F')
t.Branch('bdt_evt_isSignal', bdt_evt_isSignal, 'bdt_evt_isSignal/F')
t.Branch('bdt_evt_processid', bdt_evt_processid, 'bdt_evt_processid/F')
t.Branch('bdt_evt_processid_rindex', bdt_evt_processid_rindex, 'bdt_evt_processid_rindex/F')
t.Branch('bdt_evt_sphericity', bdt_evt_sphericity, 'bdt_evt_sphericity/F')
t.Branch('bdt_evt_aplanarity', bdt_evt_aplanarity, 'bdt_evt_aplanarity/F')
t.Branch('bdt_evt_dr_mujet', bdt_evt_dr_mujet, 'bdt_evt_dr_mujet/F')
t.Branch('bdt_evt_dr_smujet', bdt_evt_dr_smujet, 'bdt_evt_dr_smujet/F')
t.Branch('bdt_evt_dr_taujet', bdt_evt_dr_taujet, 'bdt_evt_dr_taujet/F')
t.Branch('bdt_evt_dr_mujet_csv', bdt_evt_dr_mujet_csv, 'bdt_evt_dr_mujet_csv/F')
t.Branch('bdt_evt_dr_smujet_csv', bdt_evt_dr_smujet_csv, 'bdt_evt_dr_smujet_csv/F')
t.Branch('bdt_evt_dr_taujet_csv', bdt_evt_dr_taujet_csv, 'bdt_evt_dr_taujet_csv/F')


#run_process = ['WZ', 'ZZ', 'tt1l', 'tt2l', 'tH_YtMinus1']
#run_region = ['signal']

# First, run over the signal region

for rindex, iregion in enumerate(region):

    if iregion is not 'signal':
        continue

    for index, iprocess in enumerate(process):

        if useTT==False and iprocess in ['tt0l', 'tt1l', 'tt2l']:
            continue
        
#        if iprocess is 'data':
#            continue



        print iregion, '(', rindex, ')', iprocess, '(', index, ') is processing'
        
        fname = directory + '/' + options.cr + '_' + iregion + '_' + iprocess + '.root'
        print fname
        myfile = TFile(fname)
        main = gDirectory.Get('Tree')

        for jentry in xrange(main.GetEntries()):
#        for jentry in xrange(100):

            ientry = main.LoadTree(jentry)
            nb = main.GetEntry(jentry)
            
            isSignal = False
            if iprocess=='tH_YtMinus1':
                isSignal = True
                
            ## Filling the trees

            bdt_muon_pt [0] = main.muon_pt
            bdt_muon_eta [0] = main.muon_eta
            bdt_muon_phi [0] = main.muon_phi
            bdt_muon_mass [0] = main.muon_mass
            bdt_muon_jetpt [0] = main.muon_jetpt
            bdt_muon_jet_csv [0] = main.muon_jet_csv
            bdt_muon_jet_csv_10 [0] = main.muon_jet_csv_10
            bdt_muon_id [0] = main.muon_id
            bdt_muon_iso [0] = main.muon_iso
            bdt_muon_reliso [0] = main.muon_reliso
            bdt_muon_MT [0] = main.muon_MT
            bdt_muon_charge [0] = main.muon_charge
            bdt_muon_dpt [0] = main.muon_dpt
            bdt_muon_pdg [0] = main.muon_pdg
            bdt_muon_dxy [0] = math.log(abs(main.muon_dxy))
            bdt_muon_dz [0] = math.log(abs(main.muon_dz))
            bdt_muon_dB3D [0] = main.muon_dB3D
            bdt_muon_mva [0] = main.muon_mva
            bdt_muon_mva_ch_iso [0] = main.muon_mva_ch_iso
            bdt_muon_mva_neu_iso [0] = main.muon_mva_neu_iso
            bdt_muon_mva_jet_dr [0] = main.muon_mva_jet_dr
            bdt_muon_mva_ptratio [0] = main.muon_mva_ptratio
            bdt_muon_mva_csv [0] =  main.muon_mva_csv
            
            bdt_smuon_pt [0] = main.smuon_pt
            bdt_smuon_eta [0] = main.smuon_eta
            bdt_smuon_phi [0] = main.smuon_phi
            bdt_smuon_mass [0] = main.smuon_mass
            bdt_smuon_jetpt [0] = main.smuon_jetpt
            bdt_smuon_jet_csv [0] = main.smuon_jet_csv
            bdt_smuon_jet_csv_10 [0] = main.smuon_jet_csv_10
            bdt_smuon_id [0] = main.smuon_id
            bdt_smuon_iso [0] = main.smuon_iso
            bdt_smuon_reliso [0] = main.smuon_reliso
            bdt_smuon_MT [0] = main.smuon_MT
            bdt_smuon_charge [0] = main.smuon_charge
            bdt_smuon_dpt [0] = main.smuon_dpt
            bdt_smuon_pdg [0] = main.smuon_pdg
            bdt_smuon_dxy [0] = math.log(abs(main.smuon_dxy))
            bdt_smuon_dz [0] = math.log(abs(main.smuon_dz))
            bdt_smuon_dB3D [0] = main.smuon_dB3D
            bdt_smuon_mva [0] = main.smuon_mva
            bdt_smuon_mva_ch_iso [0] = main.smuon_mva_ch_iso
            bdt_smuon_mva_neu_iso [0] = main.smuon_mva_neu_iso
            bdt_smuon_mva_jet_dr [0] = main.smuon_mva_jet_dr
            bdt_smuon_mva_ptratio [0] = main.smuon_mva_ptratio
            bdt_smuon_mva_csv [0] =  main.smuon_mva_csv
            


            
            bdt_tau_pt [0] = main.tau_pt
            bdt_tau_eta [0] = main.tau_eta
            bdt_tau_phi [0] = main.tau_phi
            bdt_tau_mass [0] = main.tau_mass
            bdt_tau_charge [0] = main.tau_charge
            bdt_tau_isolation [0] = main.tau_isolation
            bdt_tau_MT [0] = main.tau_MT
            bdt_tau_decaymode [0] = main.tau_decaymode
            bdt_tau_pdg [0] = main.tau_pdg
            bdt_tau_jet_csv [0] = main.tau_jet_csv
            bdt_tau_dxy [0] = main.tau_dxy
            bdt_tau_dz [0] = main.tau_dz
            bdt_tau_dB3D [0] = main.tau_dB3D
            
            bdt_evt_weight [0] = main.evt_weight
            bdt_evt_Mmm [0] = main.evt_Mmm
            bdt_evt_Msmt [0] = main.evt_Msmt
            bdt_evt_Mmt [0] = main.evt_Mmt
            bdt_evt_LT [0] = main.evt_LT
            bdt_evt_L2T [0] = main.evt_L2T
            bdt_evt_sumjetpt[0] = main.evt_sumjetpt
            bdt_evt_HT[0] = main.evt_HT
            bdt_evt_H[0] = main.evt_H
            bdt_evt_centrality[0] = main.evt_centrality
            bdt_evt_maxMT[0] = main.evt_maxMT
            bdt_evt_deltaeta[0] = main.evt_deltaeta
            bdt_evt_deltaeta_notau[0] = main.evt_deltaeta_notau
            
            bdt_evt_njet [0] = main.evt_njet
            bdt_evt_njet_or [0] = main.evt_njet_or
            bdt_evt_njet_or30 [0] = main.evt_njet_or30
            bdt_evt_max_jet_eta [0] = main.evt_max_jet_eta
            bdt_evt_max_jet_eta30 [0] = main.evt_max_jet_eta30
            bdt_evt_nvetobjet [0] = main.evt_nvetobjet
            bdt_evt_nbjet [0] = main.evt_nbjet
            bdt_evt_nbjet10 [0] = main.evt_nbjet10
            bdt_evt_isMC [0] = main.evt_isMC
            bdt_evt_id [0] = main.evt_id
            bdt_evt_run[0] = main.evt_run
            bdt_evt_evt[0] = main.evt_evt
            bdt_evt_lum[0] = main.evt_lum
            bdt_evt_ncmb[0] = main.evt_ncmb
            bdt_evt_missing_et[0] = main.evt_missing_et
            bdt_evt_missing_phi[0] = main.evt_missing_phi
            bdt_evt_dphi_metmu[0]  = main.evt_dphi_metmu
            bdt_evt_dphi_mete[0]   = main.evt_dphi_mete
            bdt_evt_dphi_mettau[0] = main.evt_dphi_mettau
            bdt_evt_leading_btag[0] = main.evt_leading_btag
            bdt_evt_sleading_btag[0] = main.evt_sleading_btag
            bdt_evt_leading_nbtag[0] = main.evt_leading_nbtag
            bdt_evt_sleading_nbtag[0] = main.evt_sleading_nbtag
            bdt_evt_leading_btag_pt[0] = main.evt_leading_btag_pt
            bdt_evt_sleading_btag_pt[0] = main.evt_sleading_btag_pt
            bdt_evt_isSignal[0] = isSignal
            bdt_evt_processid[0] = process_dict[iprocess]
            bdt_evt_processid_rindex[0] = -1.
            bdt_evt_sphericity[0] = main.evt_sphericity
            bdt_evt_aplanarity[0] = main.evt_aplanarity
            bdt_evt_dr_smujet[0] = main.evt_dr_smujet
            bdt_evt_dr_mujet[0] = main.evt_dr_mujet
            bdt_evt_dr_taujet[0] = main.evt_dr_taujet
            bdt_evt_dr_smujet_csv[0] = main.evt_dr_smujet_csv
            bdt_evt_dr_mujet_csv[0] = main.evt_dr_mujet_csv
            bdt_evt_dr_taujet_csv[0] = main.evt_dr_taujet_csv
            
            t.Fill()



file.Write()
file.Close()
