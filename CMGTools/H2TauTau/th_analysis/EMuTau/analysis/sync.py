#################################
# 
# 12 Nov 2013
# Y.Takahashi (Yuta.Takahashi@cern.ch)
# 
# This is the analyzer for the isolated Tau region (f12 region)
# python analysis_antiTau.py --mode (antiMu, antiE, antiEMu, signal)
#
#################################

import math, sys, array
import numpy as num
from ROOT import TFile, TH1F, gDirectory, TMVA, TTree, Double
from ROOT import TLorentzVector, Double # for M(l2,tau) calculation
import optparse
import CMGTools.H2TauTau.config as tool
#import config as tool

### For options
parser = optparse.OptionParser()
parser.add_option('--mode', action="store", dest="mode", default='signal')
parser.add_option('--region', action="store", dest="region", default='f12')
parser.add_option('--phys', action="store", dest="phys", default='data')
parser.add_option('--select', action="store_true", dest="select", default=False)
options, args = parser.parse_args()


print '[INFO] Analysis mode = ', options.mode
print '[INFO] Control region = ', options.region
print '[INFO] Physics Proecss = ', options.phys
print '[INFO] Select the event list = ', options.select


e_xml = 'kNN_training/weights/KNN_data_electron_50.xml'
m_xml = 'kNN_training/weights/KNN_data_muon_50.xml'

print '[INFO] electron xml file = ', e_xml
print '[INFO] muon xml file = ', m_xml

muonreader = TMVA.Reader("!Color:Silent=T:Verbose=F")
electronreader = TMVA.Reader("!Color:Silent=T:Verbose=F")        
mvar_map   = {}
evar_map   = {}

# lepton MVA from ttH
#mva_muon_barrel = 0.621
#mva_electron_barrel = 0.477
#
#mva_muon_endcap = 0.739
#mva_electron_endcap = 0.535

# lepton MVA from me

#mva_muon_barrel = 0.0089
#mva_electron_barrel = 0.0649
#
#mva_muon_endcap = 0.0621
#mva_electron_endcap = 0.0891


# after optimization : lepton MVA from me

#mva_muon_barrel = 0.073
#mva_electron_barrel = 0.089
#
#mva_muon_endcap = 0.126
#mva_electron_endcap = 0.113

mva_muon_barrel = 0.001
mva_electron_barrel = 0.073

mva_muon_endcap = 0.054
mva_electron_endcap = 0.097


    
# for var in ['lepton_pt', 'lepton_kNN_jetpt', 'evt_njet']:
for var in ['lepton_pt', 'evt_njet']:
    mvar_map[var] = array.array('f',[0])
    muonreader.AddVariable(var, mvar_map[var])
        
    evar_map[var] = array.array('f',[0])
    electronreader.AddVariable(var, evar_map[var])

muonreader.BookMVA('muon_data', m_xml)
electronreader.BookMVA('electron_data', e_xml)



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



def returnTopWeight(pname, top_pt, atop_pt):

    _weight_top_ = 1.
    _weight_atop_ = 1.

    if pname == 'tt0l':
        _weight_top_  = math.exp(0.156-0.00137*top_pt)
        _weight_atop_ = math.exp(0.156-0.00137*atop_pt)
        
    if pname == 'tt1l':
        _weight_top_  = math.exp(0.159-0.00141*top_pt)
        _weight_atop_ = math.exp(0.159-0.00141*atop_pt)

    if pname == 'tt2l':
        _weight_top_  = math.exp(0.148-0.00129*top_pt)
        _weight_atop_ = math.exp(0.148-0.00129*atop_pt)

    if pname == 'tt0l' or pname == 'tt1l' or pname == 'tt2l':
        if top_pt > 400:
            _weight_top_ = 1.
        if atop_pt > 400:
            _weight_atop_ = 1.

    top_weight = math.sqrt(_weight_top_*_weight_atop_)
    return top_weight



def returnkNN(iregion, weight_electron, weight_muon):

    kNN_weight = 1.
    if iregion=='antiE':
        if weight_electron==1:
            kNN_weight = 0
        else:
            kNN_weight = weight_electron/(1-weight_electron)
    elif iregion=='antiMu':
        if weight_muon==1:
            kNN_weight = 0
        else:
            kNN_weight = weight_muon/(1-weight_muon)
    elif iregion=='antiEMu':
        if weight_electron==1 or weight_muon==1:
            kNN_weight = 0
        else:
            kNN_weight = weight_muon*weight_electron/((1-weight_muon)*(1-weight_electron))
    elif iregion=='signal':
        kNN_weight = 1.

    return kNN_weight



elist = []

#for line in open('f3_signal_data_mauro_only.txt'):
if options.select:
    for line in open('yuta'):
        evt = line.rstrip().split(':')[2]
#        print evt
        elist.append(int(evt))
    print '[INFO] # of selected events = ', len(elist)
        

#process = ['WW','tt1l','tt2l','DY0','DY1','DY3','DY4']
process = [options.phys]

### reading file ...
db = tool.ReadFile(process, 'emt')
filedict = db.returnFile()

#print filedict

### For event list
outfile = [0 for i in range(len(process))]

for ii, pn in enumerate(process):
    outfile[ii] = 'EventList/' + options.region + '_' + options.mode + '_' + pn + '.list'
    print '[INFO] Event list will be written at ', outfile[ii]


    
if __name__ == '__main__':

    outputfile = 'root_process/' + options.region + '_' + options.mode + '_' + options.phys + '.root'
    file = TFile(outputfile,'recreate')
    t = TTree('Tree','Tree')
        
    muon_pt = num.zeros(1, dtype=float)
    muon_eta = num.zeros(1, dtype=float)
    muon_phi = num.zeros(1, dtype=float)
    muon_mass = num.zeros(1, dtype=float)
    muon_jetpt = num.zeros(1, dtype=float)
    muon_jet_csv = num.zeros(1, dtype=float)
    muon_jet_csv_10 = num.zeros(1, dtype=float)
    muon_dxy = num.zeros(1, dtype=float)
    muon_dz = num.zeros(1, dtype=float)
    muon_dB3D = num.zeros(1, dtype=float)
    muon_id = num.zeros(1, dtype=int)
    muon_iso = num.zeros(1, dtype=int)
    muon_reliso = num.zeros(1, dtype=float)
    muon_MT = num.zeros(1, dtype=float)
    muon_charge = num.zeros(1, dtype=int)
    muon_dpt = num.zeros(1, dtype=float)
    muon_kNN_jetpt = num.zeros(1, dtype=float)
    muon_kNN = num.zeros(1, dtype=float)
    muon_pdg = num.zeros(1, dtype=int)
    muon_ptratio = num.zeros(1, dtype=float)
    muon_mva = num.zeros(1, dtype=float)
    muon_mva_ch_iso = num.zeros(1, dtype=float)
    muon_mva_neu_iso = num.zeros(1, dtype=float)
    muon_mva_jet_dr = num.zeros(1, dtype=float)
    muon_mva_ptratio = num.zeros(1, dtype=float)
    muon_mva_csv = num.zeros(1, dtype=float)
    muon_new_mva = num.zeros(1, dtype=float)
    
    
    electron_pt = num.zeros(1, dtype=float)
    electron_eta = num.zeros(1, dtype=float)
    electron_phi = num.zeros(1, dtype=float)
    electron_mass = num.zeros(1, dtype=float)
    electron_jetpt = num.zeros(1, dtype=float)
    electron_jet_csv = num.zeros(1, dtype=float)
    electron_jet_csv_10 = num.zeros(1, dtype=float)
    electron_id = num.zeros(1, dtype=int)
    electron_iso = num.zeros(1, dtype=int)
    electron_reliso = num.zeros(1, dtype=float)
    electron_MT = num.zeros(1, dtype=float)
    electron_charge = num.zeros(1, dtype=int)
    electron_dpt = num.zeros(1, dtype=float)
    electron_kNN_jetpt = num.zeros(1, dtype=float)
    electron_kNN = num.zeros(1, dtype=float)
    electron_pdg = num.zeros(1, dtype=int)
    electron_dxy = num.zeros(1, dtype=float)
    electron_dz = num.zeros(1, dtype=float)
    electron_dB3D = num.zeros(1, dtype=float)
    electron_ptratio = num.zeros(1, dtype=float)

    electron_mva = num.zeros(1, dtype=float)
    electron_mva_ch_iso = num.zeros(1, dtype=float)
    electron_mva_neu_iso = num.zeros(1, dtype=float)
    electron_mva_jet_dr = num.zeros(1, dtype=float)
    electron_mva_ptratio = num.zeros(1, dtype=float)
    electron_mva_csv = num.zeros(1, dtype=float)
    electron_mva_score = num.zeros(1, dtype=float)
    electron_mva_numberOfHits = num.zeros(1, dtype=float)
    electron_new_mva = num.zeros(1, dtype=float)


        
    tau_pt = num.zeros(1, dtype=float)
    tau_eta = num.zeros(1, dtype=float)
    tau_phi = num.zeros(1, dtype=float)
    tau_jet_csv = num.zeros(1, dtype=float)
    tau_mass = num.zeros(1, dtype=float)
    tau_charge = num.zeros(1, dtype=int)
    tau_MT = num.zeros(1, dtype=float)
    tau_decaymode = num.zeros(1, dtype=float)
    tau_isolation = num.zeros(1, dtype=float)
    tau_pdg = num.zeros(1, dtype=int)
    tau_dxy = num.zeros(1, dtype=float)
    tau_dz = num.zeros(1, dtype=float)
    tau_dB3D = num.zeros(1, dtype=float)
    tau_ptratio = num.zeros(1, dtype=float)
    
    evt_weight = num.zeros(1, dtype=float)
    evt_top_weight = num.zeros(1, dtype=float)
    evt_Mem = num.zeros(1, dtype=float)
    evt_Met = num.zeros(1, dtype=float)
    evt_Mmt = num.zeros(1, dtype=float)
    evt_dphi_metmu = num.zeros(1, dtype=float)
    evt_dphi_mete = num.zeros(1, dtype=float)
    evt_dphi_mettau = num.zeros(1, dtype=float)
    evt_met = num.zeros(1, dtype=float)
    evt_LT = num.zeros(1, dtype=float)
    evt_L2T = num.zeros(1, dtype=float)
    evt_sumjetpt = num.zeros(1, dtype=float)
    evt_HT = num.zeros(1, dtype=float)
    evt_H = num.zeros(1, dtype=float)
    evt_centrality = num.zeros(1, dtype=float)
    evt_njet = num.zeros(1, dtype=int)
    evt_njet_or = num.zeros(1, dtype=int)
    evt_max_jet_eta = num.zeros(1, dtype=float)
    evt_njet_or30 = num.zeros(1, dtype=int)
    evt_max_jet_eta30 = num.zeros(1, dtype=float)
    evt_maxMT = num.zeros(1, dtype=float)
    evt_deltaeta_notau = num.zeros(1, dtype=float)
    evt_deltaeta = num.zeros(1, dtype=float)
    evt_nbjet = num.zeros(1, dtype=int)
    evt_nbjet10 = num.zeros(1, dtype=int)
    evt_nvetobjet = num.zeros(1, dtype=int)
    evt_isMC = num.zeros(1, dtype=int)
    evt_id = num.zeros(1, dtype=int)
    evt_run = num.zeros(1, dtype=int)
    evt_evt = num.zeros(1, dtype=int)
    evt_lum = num.zeros(1, dtype=int)
    evt_ncmb = num.zeros(1, dtype=int)
    evt_missing_et = num.zeros(1, dtype=float)
    evt_missing_phi = num.zeros(1, dtype=float)
    evt_leading_btag = num.zeros(1, dtype=float)
    evt_sleading_btag = num.zeros(1, dtype=float)
    evt_leading_nbtag = num.zeros(1, dtype=float)
    evt_sleading_nbtag = num.zeros(1, dtype=float)
    evt_leading_btag_pt = num.zeros(1, dtype=float)
    evt_sleading_btag_pt = num.zeros(1, dtype=float)
    evt_aplanarity = num.zeros(1, dtype=float)
    evt_sphericity = num.zeros(1, dtype=float)
    evt_dr_mujet = num.zeros(1, dtype=float)
    evt_dr_ejet = num.zeros(1, dtype=float)
    evt_dr_taujet = num.zeros(1, dtype=float)
    evt_dr_mujet_csv = num.zeros(1, dtype=float)
    evt_dr_ejet_csv = num.zeros(1, dtype=float)
    evt_dr_taujet_csv = num.zeros(1, dtype=float)
    evt_kNN_weight = num.zeros(1, dtype=float)
    
    
    t.Branch('muon_pt',muon_pt,'muon_pt/D')
    t.Branch('muon_eta',muon_eta,'muon_eta/D')
    t.Branch('muon_phi',muon_phi,'muon_phi/D')
    t.Branch('muon_mass', muon_mass, 'muon_mass/D')
    t.Branch('muon_jetpt',muon_jetpt, 'muon_jetpt/D')
    t.Branch('muon_dxy',muon_dxy, 'muon_dxy/D')
    t.Branch('muon_dz',muon_dz, 'muon_dz/D')
    t.Branch('muon_dB3D',muon_dB3D, 'muon_dB3D/D')
    t.Branch('muon_jet_csv',muon_jet_csv, 'muon_jet_csv/D')
    t.Branch('muon_jet_csv_10',muon_jet_csv_10, 'muon_jet_csv_10/D')
    t.Branch('muon_kNN_jetpt',muon_kNN_jetpt, 'muon_kNN_jetpt/D')
    t.Branch('muon_kNN',muon_kNN, 'muon_kNN/D')
    t.Branch('muon_id', muon_id, 'muon_id/I')
    t.Branch('muon_iso', muon_iso, 'muon_iso/I')
    t.Branch('muon_reliso', muon_reliso, 'muon_reliso/D')
    t.Branch('muon_MT', muon_MT, 'muon_MT/D')
    t.Branch('muon_charge', muon_charge, 'muon_charge/I')
    t.Branch('muon_dpt', muon_dpt, 'muon_dpt/D')
    t.Branch('muon_pdg',muon_pdg,'muon_pdg/I')
    t.Branch('muon_ptratio', muon_ptratio, 'muon_ptratio/D')

    t.Branch('muon_mva', muon_mva, 'muon_mva/D')
    t.Branch('muon_mva_ch_iso', muon_mva_ch_iso, 'muon_mva_ch_iso/D')
    t.Branch('muon_mva_neu_iso', muon_mva_neu_iso, 'muon_mva_neu_iso/D')
    t.Branch('muon_mva_jet_dr', muon_mva_jet_dr, 'muon_mva_jet_dr/D')
    t.Branch('muon_mva_ptratio', muon_mva_ptratio, 'muon_mva_ptratio/D')
    t.Branch('muon_mva_csv', muon_mva_csv, 'muon_mva_csv/D')
    t.Branch('muon_new_mva', muon_new_mva, 'muon_new_mva/D')

    t.Branch('electron_pt',electron_pt,'electron_pt/D')
    t.Branch('electron_eta',electron_eta,'electron_eta/D')
    t.Branch('electron_phi',electron_phi,'electron_phi/D')
    t.Branch('electron_mass', electron_mass, 'electron_mass/D')
    t.Branch('electron_jetpt',electron_jetpt, 'electron_jetpt/D')
    t.Branch('electron_jet_csv',electron_jet_csv, 'electron_jet_csv/D')
    t.Branch('electron_jet_csv_10',electron_jet_csv_10, 'electron_jet_csv_10/D')
    t.Branch('electron_kNN_jetpt',electron_kNN_jetpt, 'electron_kNN_jetpt/D')
    t.Branch('electron_kNN',electron_kNN, 'electron_kNN/D')
    t.Branch('electron_id', electron_id, 'electron_id/I')
    t.Branch('electron_iso', electron_iso, 'electron_iso/I')
    t.Branch('electron_reliso', electron_reliso, 'electron_reliso/D')
    t.Branch('electron_MT', electron_MT, 'electron_MT/D')
    t.Branch('electron_charge', electron_charge, 'electron_charge/I')
    t.Branch('electron_dpt', electron_dpt, 'electron_dpt/D')
    t.Branch('electron_pdg',electron_pdg,'electron_pdg/I')
    t.Branch('electron_dxy',electron_dxy, 'electron_dxy/D')
    t.Branch('electron_dz',electron_dz, 'electron_dz/D')
    t.Branch('electron_dB3D',electron_dB3D, 'electron_dB3D/D')
    t.Branch('electron_ptratio', electron_ptratio, 'electron_ptratio/D')

    t.Branch('electron_mva', electron_mva, 'electron_mva/D')
    t.Branch('electron_mva_ch_iso', electron_mva_ch_iso, 'electron_mva_ch_iso/D')
    t.Branch('electron_mva_neu_iso', electron_mva_neu_iso, 'electron_mva_neu_iso/D')
    t.Branch('electron_mva_jet_dr', electron_mva_jet_dr, 'electron_mva_jet_dr/D')
    t.Branch('electron_mva_ptratio', electron_mva_ptratio, 'electron_mva_ptratio/D')
    t.Branch('electron_mva_csv', electron_mva_csv, 'electron_mva_csv/D')
    t.Branch('electron_mva_score', electron_mva_score, 'electron_mva_score/D')
    t.Branch('electron_mva_numberOfHits', electron_mva_numberOfHits, 'electron_mva_numberOfHits/D')
    t.Branch('electron_new_mva', electron_new_mva, 'electron_new_mva/D')
    
    t.Branch('tau_pt',tau_pt,'tau_pt/D')
    t.Branch('tau_eta',tau_eta,'tau_eta/D')
    t.Branch('tau_phi',tau_phi,'tau_phi/D')
    t.Branch('tau_jet_csv',tau_jet_csv,'tau_jet_csv/D')
    t.Branch('tau_mass', tau_mass, 'tau_mass/D')
    t.Branch('tau_charge', tau_charge, 'tau_charge/I')
    t.Branch('tau_MT', tau_MT, 'tau_MT/D')
    t.Branch('tau_decaymode', tau_decaymode, 'tau_decaymode/D')
    t.Branch('tau_isolation', tau_isolation, 'tau_isolation/D')
    t.Branch('tau_pdg',tau_pdg,'tau_pdg/I')
    t.Branch('tau_dxy',tau_dxy, 'tau_dxy/D')
    t.Branch('tau_dz',tau_dz, 'tau_dz/D')
    t.Branch('tau_dB3D',tau_dB3D, 'tau_dB3D/D')
    t.Branch('tau_ptratio', tau_ptratio, 'tau_ptratio/D')
    
    t.Branch('evt_weight', evt_weight, 'evt_weight/D')
    t.Branch('evt_top_weight', evt_top_weight, 'evt_top_weight/D')
    t.Branch('evt_Mem', evt_Mem, 'evt_Mem/D')
    t.Branch('evt_dphi_metmu', evt_dphi_metmu, 'evt_dphi_metmu/D')
    t.Branch('evt_dphi_mete', evt_dphi_mete, 'evt_dphi_mete/D')
    t.Branch('evt_dphi_mettau', evt_dphi_mettau, 'evt_dphi_mettau/D')

    t.Branch('evt_Met', evt_Met, 'evt_Met/D')
    t.Branch('evt_Mmt', evt_Mmt, 'evt_Mmt/D')
    t.Branch('evt_LT', evt_LT, 'evt_LT/D')
    t.Branch('evt_L2T', evt_L2T, 'evt_L2T/D')
    t.Branch('evt_sumjetpt', evt_sumjetpt, 'evt_sumjetpt/D')
    t.Branch('evt_HT', evt_HT, 'evt_HT/D')
    t.Branch('evt_H', evt_H, 'evt_H/D')
    t.Branch('evt_centrality', evt_centrality, 'evt_centrality/D')    
    t.Branch('evt_njet', evt_njet, 'evt_njet/I')
    t.Branch('evt_njet_or', evt_njet_or, 'evt_njet_or/I')
    t.Branch('evt_njet_or30', evt_njet_or30, 'evt_njet_or30/I')
    t.Branch('evt_max_jet_eta', evt_max_jet_eta, 'evt_max_jet_eta/D')
    t.Branch('evt_max_jet_eta30', evt_max_jet_eta30, 'evt_max_jet_eta30/D')
    t.Branch('evt_nbjet', evt_nbjet, 'evt_nbjet/I')
    t.Branch('evt_nbjet10', evt_nbjet10, 'evt_nbjet10/I')
    t.Branch('evt_nvetobjet', evt_nvetobjet, 'evt_nvetobjet/I')
    t.Branch('evt_isMC', evt_isMC, 'evt_isMC/I')
    t.Branch('evt_id', evt_id, 'evt_id/I')
    t.Branch('evt_run', evt_run, 'evt_run/I')
    t.Branch('evt_evt', evt_evt, 'evt_evt/I')
    t.Branch('evt_lum', evt_lum, 'evt_lum/I')
    t.Branch('evt_ncmb', evt_ncmb, 'evt_ncmb/I')
    t.Branch('evt_missing_et', evt_missing_et, 'evt_missing_et/D')
    t.Branch('evt_missing_phi', evt_missing_phi, 'evt_missing_phi/D')
    t.Branch('evt_leading_btag', evt_leading_btag, 'evt_leading_btag/D')
    t.Branch('evt_sleading_btag', evt_sleading_btag, 'evt_sleading_btag/D')
    t.Branch('evt_leading_nbtag', evt_leading_nbtag, 'evt_leading_nbtag/D')
    t.Branch('evt_sleading_nbtag', evt_sleading_nbtag, 'evt_sleading_nbtag/D')
    t.Branch('evt_leading_btag_pt', evt_leading_btag_pt, 'evt_leading_btag_pt/D')
    t.Branch('evt_sleading_btag_pt', evt_sleading_btag_pt, 'evt_sleading_btag_pt/D')
    t.Branch('evt_maxMT', evt_maxMT, 'evt_maxMT/D')
    t.Branch('evt_deltaeta', evt_deltaeta, 'evt_deltaeta/D')
    t.Branch('evt_deltaeta_notau', evt_deltaeta_notau, 'evt_deltaeta_notau/D')
    t.Branch('evt_aplanarity', evt_aplanarity, 'evt_aplanarity/D')
    t.Branch('evt_sphericity', evt_sphericity, 'evt_sphericity/D')
    t.Branch('evt_dr_mujet', evt_dr_mujet, 'evt_dr_mujet/D')
    t.Branch('evt_dr_ejet', evt_dr_ejet, 'evt_dr_ejet/D')
    t.Branch('evt_dr_taujet', evt_dr_taujet, 'evt_dr_taujet/D')

    t.Branch('evt_dr_mujet_csv', evt_dr_mujet_csv, 'evt_dr_mujet_csv/D')
    t.Branch('evt_dr_ejet_csv', evt_dr_ejet_csv, 'evt_dr_ejet_csv/D')
    t.Branch('evt_dr_taujet_csv', evt_dr_taujet_csv, 'evt_dr_taujet_csv/D')
    t.Branch('evt_kNN_weight', evt_kNN_weight, 'evt_kNN_weight/D')
    
    counter_name = ['Initial',
                    '>=1 (e + mu)',
                    '>=1 tau',
                    '==1 bjet',
                    'emu SS',
                    'trigger',
                    'ltau OS',
                    'emu mass > 20',
                    'ltau mass > 20',
                    'no veto object'
                    ]

   
    for index, ifile in enumerate(filedict):

        pname = ifile[0]
        filename = ifile[1]
        lum_weight = ifile[2]
        ptype = ifile[3]

        fw = open(outfile[index], 'w')
        fw_acc = open(outfile[index]+'.acc', 'w')
        
        counter = [0 for ii in range(20)]

        print '[INFO] ', index, filename, 'is processing'

        myfile = TFile(filename)

        main = gDirectory.Get('H2TauTauTreeProducerEMT2')
        mchain = gDirectory.Get('H2TauTauTreeProducerEMT2_muon')
        echain = gDirectory.Get('H2TauTauTreeProducerEMT2_electron')
        tchain = gDirectory.Get('H2TauTauTreeProducerEMT2_tau')
        vmchain = gDirectory.Get('H2TauTauTreeProducerEMT2_vetomuon')
        vechain = gDirectory.Get('H2TauTauTreeProducerEMT2_vetoelectron')
        vtchain = gDirectory.Get('H2TauTauTreeProducerEMT2_vetotau')
        bchain = gDirectory.Get('H2TauTauTreeProducerEMT2_bjet')
        jchain = gDirectory.Get('H2TauTauTreeProducerEMT2_jet')
        gchain = gDirectory.Get('H2TauTauTreeProducerEMT2_gen')
        
        ptr_m = 0        
        ptr_e = 0
        ptr_t = 0
        
        ptr_vm = 0      
        ptr_ve = 0
        ptr_vt = 0

        ptr_nb = 0
        ptr_nj = 0
        ptr_ng = 0

        Total = main.GetEntries()
        Passed = 0

        top_inclusive = 1.
        
        if pname == 'tt0l' or pname=='tt1l' or pname=='tt2l':
            total_entry = 0
            
            for jentry in xrange(main.GetEntries()):

                ientry = main.LoadTree(jentry)
                nb = main.GetEntry(jentry)

                total_entry += returnTopWeight(pname, main.top_pt, main.atop_pt)

            print main.GetEntries(), total_entry, 'weight = ', main.GetEntries()/total_entry
            top_inclusive = main.GetEntries()/total_entry
            
#        for jentry in xrange(1000):
        for jentry in xrange(main.GetEntries()):

            ientry = main.LoadTree(jentry)
            nb = main.GetEntry(jentry)

            evt_flag = False

            if options.select:
                for ievent in elist:
                    if main.evt == ievent:
                        print 'event = ', main.evt, ' has been choosen'
                        evt_flag = True

            
            counter[0] += 1
            
            if jentry%20000==0:
                print '[INFO]', jentry, '/', main.GetEntries() #nmuon, nelectron, ntau, nvmuon, nvelectron, nvtau



            nmuon      = int(main.nmuon)
            nelectron  = int(main.nelectron)
            ntau       = int(main.ntau)
            
            nvmuon     = int(main.nvmuon)
            nvelectron = int(main.nvelectron)
            nvtau      = int(main.nvtau)

            nbjets     = int(main.nBJets)
            njets      = int(main.nJets)

            if pname != 'data':
                ngen       = int(main.nGen)

            if options.select:
                if evt_flag == False:

                    ptr_m += nmuon
                    ptr_e += nelectron
                    ptr_t += ntau
                    ptr_vm += nvmuon
                    ptr_ve += nvelectron
                    ptr_vt += nvtau
                    ptr_nb += nbjets
                    ptr_nj += njets
                    if pname != 'data': ptr_ng += ngen
                    
                    continue

#            counter[1] += 1
            
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

#                print 'yuta_muon', mva_iso_muon
                
#                if (options.mode=='signal' and mchain.muon_id and mchain.muon_iso) or \
#                        (options.mode=='antiMu' and not (mchain.muon_id and mchain.muon_iso)) or \
#                        (options.mode=='antiE' and mchain.muon_id and mchain.muon_iso) or \
#                        (options.mode=='antiEMu' and not (mchain.muon_id and mchain.muon_iso)):


                if (options.mode=='signal' and mchain.muon_id and ((abs(mchain.muon_eta) < 1.479 and mva_iso_muon > mva_muon_barrel) or (abs(mchain.muon_eta) > 1.479 and mva_iso_muon > mva_muon_endcap))) or \
                       (options.mode=='antiMu' and not(mchain.muon_id and ((abs(mchain.muon_eta) < 1.479 and mva_iso_muon > mva_muon_barrel) or (abs(mchain.muon_eta) > 1.479 and mva_iso_muon > mva_muon_endcap)))) or \
                       (options.mode=='antiE' and mchain.muon_id and ((abs(mchain.muon_eta) < 1.479 and mva_iso_muon > mva_muon_barrel) or (abs(mchain.muon_eta) > 1.479 and mva_iso_muon > mva_muon_endcap))) or \
                       (options.mode=='antiEMu' and not(mchain.muon_id and ((abs(mchain.muon_eta) < 1.479 and mva_iso_muon > mva_muon_barrel) or (abs(mchain.muon_eta) > 1.479 and mva_iso_muon > mva_muon_endcap)))):



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

            
                if (options.mode=='signal' and echain.electron_id and ((abs(echain.electron_eta) < 1.479 and mva_iso_electron > mva_electron_barrel) or (abs(echain.electron_eta) > 1.479 and mva_iso_electron > mva_electron_endcap))) or \
                       (options.mode=='antiMu' and echain.electron_id and ((abs(echain.electron_eta) < 1.479 and mva_iso_electron > mva_electron_barrel) or (abs(echain.electron_eta) > 1.479 and mva_iso_electron > mva_electron_endcap))) or \
                       (options.mode=='antiE' and not(echain.electron_id and ((abs(echain.electron_eta) < 1.479 and mva_iso_electron > mva_electron_barrel) or (abs(echain.electron_eta) > 1.479 and mva_iso_electron > mva_electron_endcap)))) or \
                       (options.mode=='antiEMu' and not(echain.electron_id and ((abs(echain.electron_eta) < 1.479 and mva_iso_electron > mva_electron_barrel) or (abs(echain.electron_eta) > 1.479 and mva_iso_electron > mva_electron_endcap)))):




#                if (options.mode=='signal' and echain.electron_id and ((abs(echain.electron_eta) < 1.479 and echain.electron_mva > mva_electron_barrel) or (abs(echain.electron_eta) > 1.479 and echain.electron_mva > mva_electron_endcap))) or \
#                       (options.mode=='antiMu' and echain.electron_id and ((abs(echain.electron_eta) < 1.479 and echain.electron_mva > mva_electron_barrel) or (abs(echain.electron_eta) > 1.479 and echain.electron_mva > mva_electron_endcap))) or \
#                       (options.mode=='antiE' and not(echain.electron_id and ((abs(echain.electron_eta) < 1.479 and echain.electron_mva > mva_electron_barrel) or (abs(echain.electron_eta) > 1.479 and echain.electron_mva > mva_electron_endcap)))) or \
#                       (options.mode=='antiEMu' and not(echain.electron_id and ((abs(echain.electron_eta) < 1.479 and echain.electron_mva > mva_electron_barrel) or (abs(echain.electron_eta) > 1.479 and echain.electron_mva > mva_electron_endcap)))):


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
                    
                    signal_electron.append(electron)


            # e and mu should be 1

#            counter[1] += 1
            
            if not (len(signal_muon)>=1 and len(signal_electron)>=1):
#                if options.select:
#                    print len(signal_muon), len(signal_electron)
                    
                ptr_m += nmuon
                ptr_e += nelectron
                ptr_t += ntau
                ptr_vm += nvmuon
                ptr_ve += nvelectron
                ptr_vt += nvtau
                ptr_nb += nbjets
                if pname != 'data': ptr_ng += ngen
                ptr_nj += njets
                continue

            counter[1] += 1
            
#            lepton_type = "None"

#            _muon_ = []
#            _electron_ = []


#            if signal_muon[0].pt > signal_electron[0].pt:
#                _muon_ = [ii for ii in signal_muon if ii.pt > 20.]
#                _electron_ = [ii for ii in signal_electron if ii.pt > 10.]
#                lepton_type = "muon"
#            elif signal_muon[0].pt < signal_electron[0].pt:
#                _muon_ = [ii for ii in signal_muon if ii.pt > 10.]
#                _electron_ = [ii for ii in signal_electron if ii.pt > 20.]
#                lepton_type = "electron"

#            if not (len(_muon_)==1 and len(_electron_)==1):
#                ptr_m += nmuon
#                ptr_e += nelectron
#                ptr_t += ntau
#                ptr_vm += nvmuon
#                ptr_ve += nvelectron
#                ptr_vt += nvtau
#                ptr_nb += nbjets
#                continue

            
            electron = signal_electron
            muon = signal_muon
            

            #############################################
            # Tau 

            for it in xrange(ptr_t, ptr_t + ntau):
        
                tchain.LoadTree(it)
                tchain.GetEntry(it)

            
#                if ((options.region=='f12' and tchain.tau_id and tchain.tau_iso) or \
#                    (options.region=='f3' and tchain.tau_id and tchain.tau_iso==False)):

#                if ((options.region=='f12' and tchain.tau_id) or \
#                    (options.region=='f3' and tchain.tau_id)):


                if ((options.region=='f12' and tchain.tau_id and tchain.dBisolation < 2.) or \
                    (options.region=='f3' and tchain.tau_id and tchain.dBisolation > 2.)):

#                if ((options.region=='f12' and tchain.tau_id and tchain.tau_mvaisolation > 0.785) or \
#                    (options.region=='f3' and tchain.tau_id and tchain.dBisolation < 0.785)):

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




#                    if tau.charge*muon.charge==1:
#                        continue
#                    
#                    if tau.returnmindR(muon) < 0.5:
#                        continue
#
#                    if tau.returnmindR(electron) < 0.5:
#                        continue
#
#                    if tool.diobj(tau, muon).returnmass() > 71.2 and tool.diobj(tau, muon).returnmass() < 111.2:
#                        if not (tchain.tau_againstMuTight and
#                                ((tchain.tau_decaymode==0 and tchain.tau_ep > 0.2) or (tchain.tau_decaymode!=0))):
#
#                            continue
#
#                    if tool.diobj(tau, electron).returnmass() > 71.2 and tool.diobj(tau, electron).returnmass() < 111.2:
#                        if not tchain.tau_againstEMedium:
#                            continue
#                        
#                    # calculate M(l2,tau) => soft-lepton + tau
#                    Mass = -1
#                    if lepton_type=="electron":
#                        Mass = tool.diobj(muon, tau).returnmass()
#                    elif lepton_type=="muon":
#                        Mass = tool.diobj(electron, tau).returnmass()
#                
#
#                    if Mass < 20.:
#                        continue

                        
                    signal_tau.append(tau)

                    

#            print 'muon = ', len(signal_muon), 'electron = ', len(signal_electron), 'tau = ', len(signal_tau)
            
            ptr_m += nmuon
            ptr_e += nelectron
            ptr_t += ntau


#            signal_tau = [it for it in signal_tau if it.charge*muon.charge==-1]
            if not len(signal_tau)>=1:
                ptr_vm += nvmuon
                ptr_ve += nvelectron
                ptr_vt += nvtau
                ptr_nb += nbjets
                if pname != 'data': ptr_ng += ngen
                ptr_nj += njets
#                print 'tau requirement = ', main.evt
                continue

            tau = signal_tau
            counter[2] += 1

            #  VETO
            ######################

            veto_muon = []
            veto_electron = []
            veto_tau = []           
            veto_bjet = []
            cont_jet = []
            veto_jet = []
            veto_jet30 = []
            gen_particle = []
            
            for im in xrange(ptr_vm, ptr_vm + nvmuon):
        
                vmchain.LoadTree(im)
                vmchain.GetEntry(im)

                vm = tool.easyobj(vmchain.veto_muon_pt,
                                  vmchain.veto_muon_eta,
                                  vmchain.veto_muon_phi)

                veto_muon.append(vm)
                
#                if vm.returnmindR(muon) > 0.4 and \
#                       vm.returnmindR(electron) > 0.4 and \
#                       vm.returnmindR(tau) > 0.4:
 
                

            for ie in xrange(ptr_ve, ptr_ve + nvelectron):
            
                vechain.LoadTree(ie)
                vechain.GetEntry(ie)

                ve = tool.easyobj(vechain.veto_electron_pt,
                                  vechain.veto_electron_eta,
                                  vechain.veto_electron_phi)
                
                veto_electron.append(ve)
#                if ve.returnmindR(muon) > 0.4 and \
#                       ve.returnmindR(electron) > 0.4 and \
#                       ve.returnmindR(tau) > 0.4:

                    

            for it in xrange(ptr_vt, ptr_vt + nvtau):
        
                vtchain.LoadTree(it)
                vtchain.GetEntry(it)
                
                vt = tool.easyobj(vtchain.veto_tau_pt,
                                  vtchain.veto_tau_eta,
                                  vtchain.veto_tau_phi)

                veto_tau.append(vt)
#                if vt.returnmindR(muon) > 0.4 and \
#                       vt.returnmindR(electron) > 0.4 and \
#                       vt.returnmindR(tau) > 0.4:
                    




            for ib in xrange(ptr_nb, ptr_nb+nbjets):

                bchain.LoadTree(ib)
                bchain.GetEntry(ib)

                bj = tool.easyobj_bjet(bchain.bjet_pt,
                                       bchain.bjet_eta,
                                       bchain.bjet_phi,
                                       bchain.bjet_mva)

                if bj.pt > 20 and abs(bj.eta) < 2.4 and  bj.returnmindR(muon) > 0.4 and bj.returnmindR(electron) > 0.4 and bj.returnmindR(tau) > 0.4:
#                if bj.pt > 20 and abs(bj.eta) < 2.4 and bj.mva > 0.898:
#                if bj.pt > 20 and abs(bj.eta) < 2.4:
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

                    
            for ij in xrange(ptr_nj, ptr_nj+njets):

                jchain.LoadTree(ij)
                jchain.GetEntry(ij)

                jj = tool.jetobj(jchain.jet_pt,
                                 jchain.jet_eta,
                                 jchain.jet_phi,
                                 jchain.jet_mass,
                                 jchain.jet_btagMVA)

                if jj.pt > 20. and abs(jj.eta) < 4.7:
                    veto_jet.append(jj)

                if jj.pt > 30. and abs(jj.eta) < 4.7:
                    veto_jet30.append(jj)

            leading_nbtag_csv = -1
            leading_nbtag_id = -1
            nbtag_pt = -1

            # leading non b-tag jet
            for ij in xrange(ptr_nj, ptr_nj+njets):

                jchain.LoadTree(ij)
                jchain.GetEntry(ij)

                jj = tool.jetobj(jchain.jet_pt,
                                 jchain.jet_eta,
                                 jchain.jet_phi,
                                 jchain.jet_mass,
                                 jchain.jet_btagMVA)

                
                if not (jj.pt > 20. and abs(jj.eta) < 2.4 and jj.returnmindR(muon) > 0.4 and jj.returnmindR(electron) > 0.4 and jj.returnmindR(tau) > 0.4):
                    continue

                or_bjet = False
                for bj in veto_bjet:
                    if bj.returndR(jj) < 0.4:
                        or_bjet = True

                if or_bjet==False:
                    if nbtag_pt < jj.pt:
                        nbtag_pt = jj.pt
                        leading_nbtag_csv = jchain.jet_btagMVA
                        leading_nbtag_id = ij

            sleading_nbtag_csv = -1
            snbtag_pt = -1

            for ij in xrange(ptr_nj, ptr_nj+njets):

                jchain.LoadTree(ij)
                jchain.GetEntry(ij)

                jj = tool.jetobj(jchain.jet_pt,
                                 jchain.jet_eta,
                                 jchain.jet_phi,
                                 jchain.jet_mass,
                                 jchain.jet_btagMVA)

                if not (jj.pt > 20. and abs(jj.eta) < 2.4 and jj.returnmindR(muon) > 0.4 and jj.returnmindR(electron) > 0.4 and jj.returnmindR(tau) > 0.4):
#                if not (jj.pt > 20. and abs(jj.eta) < 2.4):
                    continue

                if ij==leading_nbtag_id:
                    continue

                or_bjet = False
                for bj in veto_bjet:
                    if bj.returndR(jj) < 0.1:
                        or_bjet = True
                
                if or_bjet==False:
                    if snbtag_pt < jj.pt:
                        snbtag_pt = jj.pt
                        sleading_nbtag_csv = jchain.jet_btagMVA



            ptr_vm += nvmuon
            ptr_ve += nvelectron
            ptr_vt += nvtau
            ptr_nj += njets
            ptr_nb += nbjets
            if pname != 'data': ptr_ng += ngen

               
            if not len(veto_bjet) >= 1:
                continue
#            if not njets >= 4:




            counter[3] += 1

            stau = []

            selectedLeptons = []
            counter_pass = 0

            flag_em_SS = False
            flag_trigger = False
            flag_ltau_OS = False
            flag_em_mass = False
            flag_ltau_mass = False
            flag_veto = False

            for imuon in muon:
                for ielectron in electron:

                    if not imuon.charge*ielectron.charge==1:
#                    if not imuon.charge*ielectron.charge==-1:
                        continue

                    flag_em_SS = True

                        # Trigger matching
                        # Mu8_Ele17 : Trig_type = 1
                        # Mu17_Ele8 : Trig_type = 2

#                    if not ((main.trig_type_M17E8 and imuon.pt > 20. and ielectron.pt > 10. and imuon.trigmatch and ielectron.trigmatch) or \
#                            (main.trig_type_M8E17 and imuon.pt > 10. and ielectron.pt > 20. and imuon.trigmatch and ielectron.trigmatch)
#                            ):
                    if not ((imuon.pt > 20. and ielectron.pt > 10. and imuon.trigmatch and ielectron.trigmatch) or \
                            (imuon.pt > 10. and ielectron.pt > 20. and imuon.trigmatch and ielectron.trigmatch)
                            ):
#                        pass
                        continue
                    flag_trigger = True
#                    print 'trigger match !'
                    
                    if tool.diobj(imuon, ielectron).returnmass() < 20:
                        continue

                    flag_em_mass = True

                    for itau in tau:
                        
                        if not itau.charge*imuon.charge==-1:
                            continue

                        flag_ltau_OS = True

#                        if not (itau.charge*imuon.charge==1 and itau.charge*ielectron.charge==1):
#                            continue
                        if itau.returndR(imuon) < 0.5:
                            continue
                        
                        if itau.returndR(ielectron) < 0.5:
                            continue
                        
                        if tool.diobj(itau, imuon).returnmass() > 71.2 and tool.diobj(itau, imuon).returnmass() < 111.2:
                            if not (itau.againstMuTight and
                                    ((itau.decaymode==0 and itau.ep > 0.2) or (itau.decaymode!=0))):
                                
                                continue

                        if tool.diobj(itau, ielectron).returnmass() > 71.2 and tool.diobj(itau, ielectron).returnmass() < 111.2:
                            if not itau.againstEMedium:
                                continue
                        
                        # calculate M(l2,tau) => soft-lepton + tau
                        Mass = -1
                        if imuon.pt < ielectron.pt:
                            Mass = tool.diobj(imuon, itau).returnmass()
                        elif imuon.pt > ielectron.pt:
                            Mass = tool.diobj(ielectron, itau).returnmass()
                

                        if Mass < 20.:
                            continue

                        flag_ltau_mass = True

                        # veto


                        vmuon = []
                        velectron = []
                        vtau = []
                        
                        for iv in veto_muon:            
                            if iv.returndR(imuon) > 0.4 and \
                                   iv.returndR(ielectron) > 0.4 and \
                                   iv.returndR(itau) > 0.4:
                                vmuon.append(iv)
                                
                        for iv in veto_electron:            
                            if iv.returndR(imuon) > 0.4 and \
                                   iv.returndR(ielectron) > 0.4 and \
                                   iv.returndR(itau) > 0.4:
                                velectron.append(iv)

                                
                        for iv in veto_tau:            
                            if iv.returndR(imuon) > 0.4 and \
                                   iv.returndR(ielectron) > 0.4 and \
                                   iv.returndR(itau) > 0.4:
                                vtau.append(iv)

                        if not (len(vmuon)==0 and len(velectron)==0 and len(vtau)==0):
                            continue

                        flag_veto = True
                        
                        # bjet
#                        count_bjet = 0
#                        for bj in veto_bjet:
#                            if bj.returndR(imuon) > 0.4 and bj.returndR(ielectron) > 0.4 and bj.returndR(itau) > 0.4:
#                                count_bjet += 1
#
#                        if count_bjet >= 1:
#                            continue

                        selectedLeptons.append((imuon, ielectron, itau))
                                
                        counter_pass += 1


            # check veto
#            if not (len(smuon) >= 1 and len(selectron) >= 1 and len(stau) >= 1):

            if not (len(selectedLeptons) >= 1):
                continue

            check_sumpt = 0

            for cid, icomp in enumerate(selectedLeptons):
                _sumpt_ = icomp[0].pt + icomp[1].pt + icomp[2].pt
 #               print cid, _sumpt_
                if _sumpt_ > check_sumpt:
                    check_sumpt = _sumpt_


            _selected_ = []
            for cid, icomp in enumerate(selectedLeptons):
                _sumpt_ = icomp[0].pt + icomp[1].pt + icomp[2].pt
                if _sumpt_ == check_sumpt:
                    _selected_.append(icomp)


            if len(_selected_)!=1:
                print "!!! There are multiple candidates !!!"
                continue

            else:
                _sumpt_ = _selected_[0][0].pt + _selected_[0][1].pt + _selected_[0][2].pt
#                print 'check !', _sumpt_



            selectedLeptons = _selected_

            
            if flag_em_SS:
                counter[4] += 1
            if flag_trigger:
                counter[5] += 1
            if flag_ltau_OS:
                counter[6] += 1
            if flag_em_mass:
                counter[7] += 1
            if flag_ltau_mass:
                counter[8] += 1
            if flag_veto:
                counter[9] += 1


#            counter[9] += 1



            # count # of jets, not overlapping e,mu and tau

            
            counter_njet_or = 0
            counter_njet_or30 = 0
            max_jet_eta = -100
            max_jet_eta30 = -100
            max_jet_eta_sign = -999
            max_jet_eta30_sign = -999
            sumjetpt = 0
            sumjetp = 0
            allparticles = []

            for jj in veto_jet:
                flag_or = False
                for imuon, ielectron, itau in selectedLeptons:
                    if jj.returndR(imuon) < 0.4 or jj.returndR(ielectron) < 0.4 or jj.returndR(itau) < 0.4:
                        flag_or = True

                if flag_or==False:
                    counter_njet_or += 1
                    sumjetpt += jj.pt
                    sumjetp += jj.p
                    allparticles.append(jj.returnVector())

                    if max_jet_eta < abs(jj.eta):
                        max_jet_eta = abs(jj.eta)
                        max_jet_eta_sign = jj.eta                        
                        
            HT = sumjetpt
            H = sumjetp


            for jj in veto_jet:
                
                imu_pt = 0
                ie_pt = 0
                itau_pt = 0
                imu_p = 0
                ie_p = 0
                itau_p = 0
                imu_4v = None
                ie_4v = None
                itau_4v = None

                for imuon, ielectron, itau in selectedLeptons:
                    if jj.returndR(imuon) < 0.4:
                        imu_pt = imuon.pt
                        imu_p = imuon.p
                        imu_4v = imuon.returnVector()
                    elif jj.returndR(ielectron) < 0.4:
                        ie_pt = ielectron.pt
                        ie_p = ielectron.p
                        ie_4v = ielectron.returnVector()
                    elif jj.returndR(itau) < 0.4:
                        itau_pt = itau.pt
                        itau_p = itau.p
                        itau_4v = itau.returnVector()
                                                
                HT += (imu_pt + ie_pt + itau_pt)
                H += imu_p + ie_p + itau_p

                if imu_4v is not None:
                    allparticles.append(imu_4v)
                if ie_4v is not None:
                    allparticles.append(ie_4v)
                if itau_4v is not None:
                    allparticles.append(itau_4v)

#            print 'check -> ', allparticles
                    
            for jj in veto_jet30:
                flag_or = False
                for imuon, ielectron, itau in selectedLeptons:
                    if jj.returndR(imuon) < 0.4 or jj.returndR(ielectron) < 0.4 or jj.returndR(itau) < 0.4:
                        flag_or = True

                if flag_or==False:
                    counter_njet_or30 += 1
                    if max_jet_eta30 < abs(jj.eta):
                        max_jet_eta30 = abs(jj.eta)
                        max_jet_eta30_sign = jj.eta

#            for imuon in smuon:
#                for ielectron in selectron:
#                    for itau in stau:

            for imuon, ielectron, itau in selectedLeptons:
                        
                weight = 1.
                isMC = False
                        
                if pname == 'data':
                    pass
                else:
                    weight = main.weight*imuon.trig*imuon.id*ielectron.trig*ielectron.id*lum_weight
                    isMC = True



                    
                kNN_muonjetpt = imuon.jetpt
                kNN_electronjetpt = ielectron.jetpt
                        
                if kNN_muonjetpt == -999:
                    kNN_muonjetpt = imuon.pt
                            
                if kNN_electronjetpt == -999:
                    kNN_electronjetpt = ielectron.pt

                if kNN_muonjetpt < imuon.pt:
                    kNN_muonjetpt = imuon.pt

                if kNN_electronjetpt < ielectron.pt:
                    kNN_electronjetpt = ielectron.pt


                muon_pt [0] = imuon.pt
                muon_eta [0] = imuon.eta
                muon_phi [0] = imuon.phi
                muon_mass [0] = imuon.mass
                muon_jetpt [0] = imuon.jetpt
                muon_id [0] = imuon.isid
                muon_iso [0] = imuon.isiso
                muon_reliso [0] = imuon.reliso
                muon_MT [0] = imuon.MT
                muon_charge [0] = imuon.charge
                muon_dpt [0] = imuon.jetpt - imuon.pt
                muon_kNN_jetpt [0] = kNN_muonjetpt
                muon_dxy [0] = imuon.dxy
                muon_dz [0] = imuon.dz
                muon_dB3D [0] = imuon.dB3D


                muon_ipdg = 0
                muon_min_dr = 100

                if pname != 'data':

                    for gen in gen_particle:
                        if imuon.returndR(gen) < 0.5:
                            muon_min_dr = imuon.returndR(gen)
                            muon_ipdg = gen.pdgid

                muon_pdg[0] = muon_ipdg
                
                electron_pt [0] = ielectron.pt
                electron_eta [0] = ielectron.eta
                electron_phi [0] = ielectron.phi
                electron_mass [0] = ielectron.mass
                electron_jetpt [0] = ielectron.jetpt
                electron_id [0] = ielectron.isid
                electron_iso [0] = ielectron.isiso
                electron_reliso [0] = ielectron.reliso
                electron_MT [0] = ielectron.MT
                electron_charge [0] = ielectron.charge
                electron_dpt [0] = ielectron.jetpt - ielectron.pt
                electron_kNN_jetpt [0] = kNN_electronjetpt
                electron_dxy [0] = ielectron.dxy
                electron_dz [0] = ielectron.dz
                electron_dB3D [0] = ielectron.dB3D


                electron_ipdg = 0
                electron_min_dr = 100

                if pname != 'data':
                    for gen in gen_particle:
                        if ielectron.returndR(gen) < 0.5:
                            electron_min_dr = ielectron.returndR(gen)
                            electron_ipdg = gen.pdgid

                electron_pdg[0] = electron_ipdg
                
                   
                tau_pt [0] = itau.pt
                tau_eta [0] = itau.eta
                tau_phi [0] = itau.phi
                tau_mass [0] = itau.mass
                tau_charge [0] = itau.charge
                tau_isolation [0] = itau.reliso
                tau_MT [0] = itau.MT
                tau_decaymode [0] = itau.decaymode
                tau_dxy [0] = itau.dxy
                tau_dz [0] = itau.dz
                tau_dB3D [0] = itau.dB3D


                tau_ipdg = 0
                tau_min_dr = 100

                if pname != 'data':
                    for gen in gen_particle:
                        if itau.returndR(gen) < 0.5:
                            tau_min_dr = itau.returndR(gen)
                            tau_ipdg = gen.pdgid

                tau_pdg[0] = tau_ipdg
                

                if pname == 'tt0l' or pname=='tt1l' or pname=='tt2l':
                    evt_weight [0] = weight*top_inclusive*returnTopWeight(pname, main.top_pt, main.atop_pt)
                    evt_top_weight [0] = top_inclusive*returnTopWeight(pname, main.top_pt, main.atop_pt)
                else:
                    evt_weight [0] = weight
                    evt_top_weight [0] = 1.
                    
#                print weight, top_inclusive*returnTopWeight(pname, main.top_pt, main.atop_pt), evt_weight[0]
                
                    
                
                evt_Mem [0] = tool.diobj(imuon, ielectron).returnmass()
                evt_Met [0] = tool.diobj(ielectron, itau).returnmass()
                evt_Mmt [0] = tool.diobj(imuon, itau).returnmass()
                evt_LT [0] = imuon.pt + ielectron.pt + itau.pt
                
                Mass = -1
                if imuon.pt < ielectron.pt:
                    Mass = tool.diobj(imuon, itau).returnmass()
                elif imuon.pt > ielectron.pt:
                    Mass = tool.diobj(ielectron, itau).returnmass()
                            
                evt_L2T [0] = Mass
                evt_sumjetpt[0] = sumjetpt
                evt_HT[0] = HT
                evt_H[0] = H

                if H!=0:
                    evt_centrality[0] = Double(HT/H)
                else:
                    evt_centrality[0] = Double(-1)
                    
                aplanarity, sphericity = tool.calculateSphericity(allparticles)
                evt_aplanarity[0] = aplanarity
                evt_sphericity[0] = sphericity


                min_dr_mu = 1000
                min_dr_mu_csv = -1
                for jj in veto_jet:
                    if not (jj.returndR(imuon) < 0.4 or jj.returndR(ielectron) < 0.4 or jj.returndR(itau) < 0.4):
                        dr = jj.returndR(imuon)
                        if dr < min_dr_mu:
                            min_dr_mu = dr
                            min_dr_mu_csv = jj.mva

                min_dr_e = 1000
                min_dr_e_csv = -1

                for jj in veto_jet:
                    if not (jj.returndR(imuon) < 0.4 or jj.returndR(ielectron) < 0.4 or jj.returndR(itau) < 0.4):
                        dr = jj.returndR(ielectron)
                        if dr < min_dr_e:
                            min_dr_e = dr
                            min_dr_e_csv = jj.mva
                            
                min_dr_tau = 1000
                min_dr_tau_csv = -1
                
                for jj in veto_jet:
                    if not (jj.returndR(imuon) < 0.4 or jj.returndR(ielectron) < 0.4 or jj.returndR(itau) < 0.4):
                        dr = jj.returndR(itau)
                        if dr < min_dr_tau:
                            min_dr_tau = dr
                            min_dr_tau_csv = jj.mva


                ###############

                csv_min_dr_mu = 1000
                csv_min_dr_mu_csv = -1
                mratio = -1
                for jj in veto_jet:
                    if jj.returndR(imuon) < 0.5:
                        dr = jj.returndR(imuon)
                        if dr < csv_min_dr_mu:
                            csv_min_dr_mu = dr
                            csv_min_dr_mu_csv = jj.mva
                            mratio = imuon.pt/jj.pt

                csv_min_dr_e = 1000
                csv_min_dr_e_csv = -1
                eratio = -1
                
                for jj in veto_jet:
                    if jj.returndR(ielectron) < 0.5:
                        dr = jj.returndR(ielectron)
                        if dr < csv_min_dr_e:
                            csv_min_dr_e = dr
                            csv_min_dr_e_csv = jj.mva
                            eratio = ielectron.pt/jj.pt
                            
                csv_min_dr_tau = 1000
                csv_min_dr_tau_csv = -1
                tratio = -1
                
                for jj in veto_jet:
                    if jj.returndR(itau) < 0.5:
                        dr = jj.returndR(itau)
                        if dr < csv_min_dr_tau:
                            csv_min_dr_tau = dr
                            csv_min_dr_tau_csv = jj.mva
                            tratio = itau.pt/jj.pt

                electron_jet_csv [0] = csv_min_dr_e_csv
                muon_jet_csv [0] = csv_min_dr_mu_csv
                tau_jet_csv [0] = csv_min_dr_tau_csv
                electron_jet_csv_10 [0] = ielectron.csv_10
                muon_jet_csv_10 [0] = imuon.csv_10
                muon_ptratio[0] = mratio
                electron_ptratio[0] = eratio
                tau_ptratio[0] = tratio
                muon_mva[0] = imuon.mva
                
                muon_mva_ch_iso[0] = imuon.mva_ch_iso
                muon_mva_neu_iso[0] = imuon.mva_neu_iso
                muon_mva_jet_dr[0] = imuon.mva_jet_dr
                muon_mva_ptratio[0] = imuon.mva_ptratio
                muon_mva_csv[0] = imuon.mva_csv
                muon_new_mva[0] = imuon.new_mva
                
                electron_mva[0] = ielectron.mva

                electron_mva_ch_iso[0] = ielectron.mva_ch_iso
                electron_mva_neu_iso[0] = ielectron.mva_neu_iso
                electron_mva_jet_dr[0] = ielectron.mva_jet_dr
                electron_mva_ptratio[0] = ielectron.mva_ptratio
                electron_mva_csv[0] = ielectron.mva_csv
                electron_mva_score[0] = ielectron.mva_score
                electron_mva_numberOfHits[0] = ielectron.mva_nhit
                electron_new_mva[0] = ielectron.new_mva

                evt_dr_mujet[0] = min_dr_mu
                evt_dr_ejet[0] = min_dr_e
                evt_dr_taujet[0] = min_dr_tau
                evt_dr_mujet_csv[0] = min_dr_mu_csv
                evt_dr_ejet_csv[0] = min_dr_e_csv
                evt_dr_taujet_csv[0] = min_dr_tau_csv

                # Yuta added 
#                if flag_or==False:
#                    counter_njet_or += 1
#                    sumjetpt += jj.pt
#                    sumjetp += jj.p
#                    allparticles.append(jj.returnVector())
#
#                    if abs(max_jet_eta) < abs(jj.eta):
#                        max_jet_eta = jj.eta

                
                evt_njet [0] = main.nJets
                evt_njet_or [0] = counter_njet_or
                evt_njet_or30 [0] = counter_njet_or30
                evt_max_jet_eta [0] = max_jet_eta_sign
                evt_max_jet_eta30 [0] = max_jet_eta30_sign
                evt_nvetobjet [0] = len(veto_bjet)
                evt_nbjet [0] = main.nBJets
                evt_nbjet10 [0] = main.nBJets_10
                
                evt_isMC [0] = isMC
                evt_id [0] = ptype
                evt_run[0] = main.run
                evt_evt[0] = main.evt
                evt_lum[0] = main.lumi
                evt_ncmb[0] = len(selectedLeptons)
                evt_missing_et[0] = main.pfmet
                evt_missing_phi[0] = main.pfmetphi

                evt_dphi_metmu[0]  = imuon.phi - main.pfmetphi
                evt_dphi_mete[0]   = ielectron.phi - main.pfmetphi
                evt_dphi_mettau[0] = itau.phi - main.pfmetphi

                maxMT = imuon.MT

                if imuon.MT < ielectron.MT:
                    maxMT = ielectron.MT

                deltaeta = Double(Double(imuon.eta + ielectron.eta + itau.eta)/3. - max_jet_eta_sign)
                deltaeta_notau = Double(Double(imuon.eta + ielectron.eta)/3. - max_jet_eta_sign)

                
                evt_maxMT[0] = maxMT
                evt_deltaeta[0] = deltaeta
                evt_deltaeta_notau[0] = deltaeta_notau
                evt_leading_nbtag[0] =  leading_nbtag_csv
                evt_sleading_nbtag[0] =  sleading_nbtag_csv

                if len(veto_bjet)==0:
                    evt_leading_btag[0] = -1
                    evt_sleading_btag[0] = -1
                    evt_leading_btag_pt[0] = -1
                    evt_sleading_btag_pt[0] = -1
                    
                elif len(veto_bjet)==1:
                    evt_leading_btag[0] = veto_bjet[0].mva
                    evt_sleading_btag[0] = -1
                    evt_leading_btag_pt[0] = veto_bjet[0].pt
                    evt_sleading_btag_pt[0] = -1
                elif len(veto_bjet)>=2:

                    # find maximum btag
                    max_btag = -1
                    max_btag_id = -1
                    max_btag_pt = -1


                    for icount, ibjet in enumerate(veto_bjet):
                        if max_btag < ibjet.mva:
                            max_btag = ibjet.mva
                            max_btag_id = icount
                            max_btag_pt = ibjet.pt
                            
                    smax_btag = -1
                    smax_btag_pt = -1
                    
                    for icount, ibjet in enumerate(veto_bjet):
                        if icount == max_btag_id:
                            continue
                        if smax_btag < ibjet.mva:
                            smax_btag = ibjet.mva
                            smax_btag_pt = ibjet.pt
                            
                    evt_leading_btag[0] = max_btag
                    evt_sleading_btag[0] = smax_btag
                    evt_leading_btag_pt[0] = max_btag_pt
                    evt_sleading_btag_pt[0] = smax_btag_pt

                    
                weight_muon = 0.5
                weight_electron = 0.5
            
                if options.mode=='antiMu' or options.mode=='antiEMu':

                    mvar_map['lepton_pt'][0] = imuon.pt
                    # mvar_map['lepton_kNN_jetpt'][0] = kNN_muonjetpt
                    mvar_map['evt_njet'][0] = main.nJets + 1
                    
                    weight_muon = muonreader.EvaluateMVA('muon_data')
                    muon_kNN[0] = weight_muon
                if options.mode=='antiE' or options.mode=='antiEMu':

                    evar_map['lepton_pt'][0] = ielectron.pt
                    # evar_map['lepton_kNN_jetpt'][0] = kNN_electronjetpt
                    evar_map['evt_njet'][0] = main.nJets + 1
                    
                    weight_electron = electronreader.EvaluateMVA('electron_data')
                    electron_kNN[0] = weight_electron

               
                kNN_weight = returnkNN(options.mode,  weight_electron, weight_muon)
                
#                weight_total = main.evt_weight*kNN_weight*nsf[rindex]
                if options.mode=='antiEMu':
                    kNN_weight *= -1.

                evt_kNN_weight[0] = kNN_weight

                t.Fill()




#            print 'Ne, Nm, Nt = ', len(selectron), len(smuon), len(stau), ' comb = ', counter_pass

            if options.mode=='signal' and options.region=='f12':
                if counter_pass == 1:
                    line = str(int(main.run))+':'+str(int(main.lumi))+':'+str(int(main.evt))+'\n'
#                    print 'List = ', line
                    fw.write(line)
            else:
                if counter_pass >= 1:
                    line = str(int(main.run))+':'+str(int(main.lumi))+':'+str(int(main.evt))+'\n'
#                    print 'List = ', line
                    fw.write(line)
                
        
            Passed += 1

        print '[INFO] pass, total, eff = ', Passed, '/' , Total
        fw.close()
        

#        for ic in range(len(counter)):
        for ic in range(10):
            acc = 1.
            if ic != 0:
                if counter[ic-1]==0:
                    acc = 0
                else:
                    acc = Double(Double(counter[ic])/Double(counter[ic-1]))

#            line = '[INFO]', '%-15s %-15s %-5s %-15s %10s (%.2f)' % (options.mode, pname, ic, counter_name[ic], counter[ic], acc)
            print '[INFO]', '%-15s %-15s %-5s %-15s %10s (%.2f)' % (options.mode, pname, ic, counter_name[ic], counter[ic], acc)
            fw_acc.write(str(acc) + '\n')
        fw_acc.close()

    file.Write()
    file.Close()




    
