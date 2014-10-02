import math, sys, array, optparse
import numpy as num
from ROOT import TFile, TH1F, gDirectory, TMVA, TTree, Double, TLorentzVector, Double
import config as tool

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

mva_muon_barrel = 0.001
mva_electron_barrel = 0.073

mva_muon_endcap = 0.054
mva_electron_endcap = 0.097

for var in ['lepton_pt', 'lepton_kNN_jetpt', 'evt_njet']:
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

if options.select:
    for line in open('yuta'):
        evt = line.rstrip().split(':')[2]
        elist.append(int(evt))
    print '[INFO] # of selected events = ', len(elist)
        

process = [options.phys]

db = tool.ReadFile(process)
filedict = db.returnFile()

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
    muon_pdg = num.zeros(1, dtype=int)
    muon_ptratio = num.zeros(1, dtype=float)
    muon_mva = num.zeros(1, dtype=float)
    muon_mva_ch_iso = num.zeros(1, dtype=float)
    muon_mva_neu_iso = num.zeros(1, dtype=float)
    muon_mva_jet_dr = num.zeros(1, dtype=float)
    muon_mva_ptratio = num.zeros(1, dtype=float)
    muon_mva_csv = num.zeros(1, dtype=float)
    muon_new_mva = num.zeros(1, dtype=float)
    

    smuon_pt = num.zeros(1, dtype=float)
    smuon_eta = num.zeros(1, dtype=float)
    smuon_phi = num.zeros(1, dtype=float)
    smuon_mass = num.zeros(1, dtype=float)
    smuon_jetpt = num.zeros(1, dtype=float)
    smuon_jet_csv = num.zeros(1, dtype=float)
    smuon_jet_csv_10 = num.zeros(1, dtype=float)
    smuon_dxy = num.zeros(1, dtype=float)
    smuon_dz = num.zeros(1, dtype=float)
    smuon_dB3D = num.zeros(1, dtype=float)
    smuon_id = num.zeros(1, dtype=int)
    smuon_iso = num.zeros(1, dtype=int)
    smuon_reliso = num.zeros(1, dtype=float)
    smuon_MT = num.zeros(1, dtype=float)
    smuon_charge = num.zeros(1, dtype=int)
    smuon_dpt = num.zeros(1, dtype=float)
    smuon_kNN_jetpt = num.zeros(1, dtype=float)
    smuon_pdg = num.zeros(1, dtype=int)
    smuon_ptratio = num.zeros(1, dtype=float)
    smuon_mva = num.zeros(1, dtype=float)
    smuon_mva_ch_iso = num.zeros(1, dtype=float)
    smuon_mva_neu_iso = num.zeros(1, dtype=float)
    smuon_mva_jet_dr = num.zeros(1, dtype=float)
    smuon_mva_ptratio = num.zeros(1, dtype=float)
    smuon_mva_csv = num.zeros(1, dtype=float)
    smuon_new_mva = num.zeros(1, dtype=float)
    

        
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
    evt_Mmm = num.zeros(1, dtype=float)
    evt_Msmt = num.zeros(1, dtype=float)
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
    evt_dr_smujet = num.zeros(1, dtype=float)
    evt_dr_taujet = num.zeros(1, dtype=float)
    evt_dr_mujet_csv = num.zeros(1, dtype=float)
    evt_dr_smujet_csv = num.zeros(1, dtype=float)
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

    t.Branch('smuon_pt',smuon_pt,'smuon_pt/D')
    t.Branch('smuon_eta',smuon_eta,'smuon_eta/D')
    t.Branch('smuon_phi',smuon_phi,'smuon_phi/D')
    t.Branch('smuon_mass', smuon_mass, 'smuon_mass/D')
    t.Branch('smuon_jetpt',smuon_jetpt, 'smuon_jetpt/D')
    t.Branch('smuon_dxy',smuon_dxy, 'smuon_dxy/D')
    t.Branch('smuon_dz',smuon_dz, 'smuon_dz/D')
    t.Branch('smuon_dB3D',smuon_dB3D, 'smuon_dB3D/D')
    t.Branch('smuon_jet_csv',smuon_jet_csv, 'smuon_jet_csv/D')
    t.Branch('smuon_jet_csv_10',smuon_jet_csv_10, 'smuon_jet_csv_10/D')
    t.Branch('smuon_kNN_jetpt',smuon_kNN_jetpt, 'smuon_kNN_jetpt/D')
    t.Branch('smuon_id', smuon_id, 'smuon_id/I')
    t.Branch('smuon_iso', smuon_iso, 'smuon_iso/I')
    t.Branch('smuon_reliso', smuon_reliso, 'smuon_reliso/D')
    t.Branch('smuon_MT', smuon_MT, 'smuon_MT/D')
    t.Branch('smuon_charge', smuon_charge, 'smuon_charge/I')
    t.Branch('smuon_dpt', smuon_dpt, 'smuon_dpt/D')
    t.Branch('smuon_pdg',smuon_pdg,'smuon_pdg/I')
    t.Branch('smuon_ptratio', smuon_ptratio, 'smuon_ptratio/D')
    t.Branch('smuon_mva', smuon_mva, 'smuon_mva/D')
    t.Branch('smuon_mva_ch_iso', smuon_mva_ch_iso, 'smuon_mva_ch_iso/D')
    t.Branch('smuon_mva_neu_iso', smuon_mva_neu_iso, 'smuon_mva_neu_iso/D')
    t.Branch('smuon_mva_jet_dr', smuon_mva_jet_dr, 'smuon_mva_jet_dr/D')
    t.Branch('smuon_mva_ptratio', smuon_mva_ptratio, 'smuon_mva_ptratio/D')
    t.Branch('smuon_mva_csv', smuon_mva_csv, 'smuon_mva_csv/D')
    t.Branch('smuon_new_mva', smuon_new_mva, 'smuon_new_mva/D')
    
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
    t.Branch('evt_Mmm', evt_Mmm, 'evt_Mmm/D')
    t.Branch('evt_dphi_metmu', evt_dphi_metmu, 'evt_dphi_metmu/D')
    t.Branch('evt_dphi_mete', evt_dphi_mete, 'evt_dphi_mete/D')
    t.Branch('evt_dphi_mettau', evt_dphi_mettau, 'evt_dphi_mettau/D')

    t.Branch('evt_Msmt', evt_Msmt, 'evt_Msmt/D')
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
    t.Branch('evt_dr_smujet', evt_dr_smujet, 'evt_dr_smujet/D')
    t.Branch('evt_dr_taujet', evt_dr_taujet, 'evt_dr_taujet/D')

    t.Branch('evt_dr_mujet_csv', evt_dr_mujet_csv, 'evt_dr_mujet_csv/D')
    t.Branch('evt_dr_smujet_csv', evt_dr_smujet_csv, 'evt_dr_smujet_csv/D')
    t.Branch('evt_dr_taujet_csv', evt_dr_taujet_csv, 'evt_dr_taujet_csv/D')
    t.Branch('evt_kNN_weight', evt_kNN_weight, 'evt_kNN_weight/D')
    
    counter_name = ['Initial',
                    'selected',
                    '>=2 mu',
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

        main = gDirectory.Get('H2TauTauTreeProducerMMT')
        mchain = gDirectory.Get('H2TauTauTreeProducerMMT_muon')
        echain = gDirectory.Get('H2TauTauTreeProducerMMT_electron')
        tchain = gDirectory.Get('H2TauTauTreeProducerMMT_tau')
        vmchain = gDirectory.Get('H2TauTauTreeProducerMMT_vetomuon')
        vechain = gDirectory.Get('H2TauTauTreeProducerMMT_vetoelectron')
        vtchain = gDirectory.Get('H2TauTauTreeProducerMMT_vetotau')
        bchain = gDirectory.Get('H2TauTauTreeProducerMMT_bjet')
        jchain = gDirectory.Get('H2TauTauTreeProducerMMT_jet')
        gchain = gDirectory.Get('H2TauTauTreeProducerMMT_gen')
        
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

            counter[1] += 1
            
            # for real Leptons
            signal_muon = []
            signal_electron = []
            signal_tau = []
            
            for im in xrange(ptr_m, ptr_m + nmuon):
                mchain.LoadTree(im)
                mchain.GetEntry(im)
                
#                mva_mvar_map['bdt_muon_dxy'][0] = mchain.muon_mva_dxy
#                mva_mvar_map['bdt_muon_dz'][0] = mchain.muon_mva_dz
                mva_mvar_map['bdt_muon_dxy'][0] = mchain.muon_dxy
                mva_mvar_map['bdt_muon_dz'][0] = mchain.muon_dz
                mva_mvar_map['bdt_muon_mva_ch_iso'][0] = mchain.muon_mva_ch_iso
                mva_mvar_map['bdt_muon_mva_neu_iso'][0] = mchain.muon_mva_neu_iso
                mva_mvar_map['bdt_muon_mva_jet_dr'][0] = mchain.muon_mva_jet_dr
                mva_mvar_map['bdt_muon_mva_ptratio'][0] = mchain.muon_mva_ptratio
                mva_mvar_map['bdt_muon_mva_csv'][0] = mchain.muon_mva_csv
                
                mva_iso_muon = mva_muonreader.EvaluateMVA('mva_muon_data')

                _muon_iso_ = False

                if abs(mchain.muon_eta) < 1.479:
                    _muon_iso_ = (mchain.muon_reliso < 0.2)
                else:
                    _muon_iso_ = (mchain.muon_reliso < 0.15)


                if (options.mode=='signal' and mchain.muon_id and _muon_iso_) or \
                        (options.mode=='antiMu' and not (mchain.muon_id and _muon_iso_)) or \
                        (options.mode=='antiE' and mchain.muon_id and _muon_iso_) or \
                        (options.mode=='antiEMu' and not (mchain.muon_id and _muon_iso_)):
                
#                if (options.mode=='signal' and mchain.muon_id and mchain.muon_iso) or \
#                        (options.mode=='antiMu' and not (mchain.muon_id and mchain.muon_iso)) or \
#                        (options.mode=='antiE' and mchain.muon_id and mchain.muon_iso) or \
#                        (options.mode=='antiEMu' and not (mchain.muon_id and mchain.muon_iso)):


#                if (options.mode=='signal' and mchain.muon_id and ((abs(mchain.muon_eta) < 1.479 and mva_iso_muon > mva_muon_barrel) or (abs(mchain.muon_eta) > 1.479 and mva_iso_muon > mva_muon_endcap))) or \
#                       (options.mode=='antiMu' and not(mchain.muon_id and ((abs(mchain.muon_eta) < 1.479 and mva_iso_muon > mva_muon_barrel) or (abs(mchain.muon_eta) > 1.479 and mva_iso_muon > mva_muon_endcap)))) or \
#                       (options.mode=='antiE' and mchain.muon_id and ((abs(mchain.muon_eta) < 1.479 and mva_iso_muon > mva_muon_barrel) or (abs(mchain.muon_eta) > 1.479 and mva_iso_muon > mva_muon_endcap))) or \
#                       (options.mode=='antiEMu' and not(mchain.muon_id and ((abs(mchain.muon_eta) < 1.479 and mva_iso_muon > mva_muon_barrel) or (abs(mchain.muon_eta) > 1.479 and mva_iso_muon > mva_muon_endcap)))):



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

            
#                if (options.mode=='signal' and echain.electron_id and ((abs(echain.electron_eta) < 1.479 and mva_iso_electron > mva_electron_barrel) or (abs(echain.electron_eta) > 1.479 and mva_iso_electron > mva_electron_endcap))) or \
#                       (options.mode=='antiMu' and echain.electron_id and ((abs(echain.electron_eta) < 1.479 and mva_iso_electron > mva_electron_barrel) or (abs(echain.electron_eta) > 1.479 and mva_iso_electron > mva_electron_endcap))) or \
#                       (options.mode=='antiE' and not(echain.electron_id and ((abs(echain.electron_eta) < 1.479 and mva_iso_electron > mva_electron_barrel) or (abs(echain.electron_eta) > 1.479 and mva_iso_electron > mva_electron_endcap)))) or \
#                       (options.mode=='antiEMu' and not(echain.electron_id and ((abs(echain.electron_eta) < 1.479 and mva_iso_electron > mva_electron_barrel) or (abs(echain.electron_eta) > 1.479 and mva_iso_electron > mva_electron_endcap)))):


                if (options.mode=='signal' and echain.electron_id and echain.electron_iso) or \
                        (options.mode=='antiMu' and echain.electron_id and echain.electron_iso) or \
                        (options.mode=='antiE' and not (echain.electron_id and echain.electron_iso)) or \
                        (options.mode=='antiEMu' and not (echain.electron_id and echain.electron_iso)):


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


                    
#            if not (len(signal_muon)>=2 and len(signal_electron)==0):
#            if not (len(signal_muon)==2):
            if not (len(signal_muon)>=2):
                    
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

            counter[2] += 1
            
            electron = signal_electron
            muon = signal_muon
            

            #############################################
            # Tau 

            for it in xrange(ptr_t, ptr_t + ntau):
        
                tchain.LoadTree(it)
                tchain.GetEntry(it)
                
                _tauid_ = tchain.tau_againstMuTight
#                print 'tauID :', _tauid_
                if ((options.region=='f12' and tchain.tau_id and _tauid_ > 0.5 and tchain.tau_iso) or \
                    (options.region=='f3' and tchain.tau_id and _tauid_ > 0.5 and tchain.tau_iso==False)):

#                if ((options.region=='f12' and tchain.tau_id) or \
#                    (options.region=='f3' and tchain.tau_id)):



#                if ((options.region=='f12' and _tauid_ and tchain.dBisolation < 2.) or \
#                    (options.region=='f3' and _tauid_ and tchain.dBisolation > 2.)):

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

                        
                    signal_tau.append(tau)

            
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
            counter[3] += 1

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
                
               

            for ie in xrange(ptr_ve, ptr_ve + nvelectron):
            
                vechain.LoadTree(ie)
                vechain.GetEntry(ie)

                ve = tool.easyobj(vechain.veto_electron_pt,
                                  vechain.veto_electron_eta,
                                  vechain.veto_electron_phi)
                
                veto_electron.append(ve)

                    

            for it in xrange(ptr_vt, ptr_vt + nvtau):
        
                vtchain.LoadTree(it)
                vtchain.GetEntry(it)
                
                vt = tool.easyobj(vtchain.veto_tau_pt,
                                  vtchain.veto_tau_eta,
                                  vtchain.veto_tau_phi)

                veto_tau.append(vt)



            for ib in xrange(ptr_nb, ptr_nb+nbjets):

                bchain.LoadTree(ib)
                bchain.GetEntry(ib)

                bj = tool.easyobj_bjet(bchain.bjet_pt,
                                       bchain.bjet_eta,
                                       bchain.bjet_phi,
                                       bchain.bjet_mva)

                if bj.pt > 20 and abs(bj.eta) < 2.4 and  bj.returnmindR(muon) > 0.4 and bj.returnmindR(tau) > 0.4:
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

                
                if not (jj.pt > 20. and abs(jj.eta) < 2.4 and jj.returnmindR(muon) > 0.4 and jj.returnmindR(tau) > 0.4):
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

                if not (jj.pt > 20. and abs(jj.eta) < 2.4 and jj.returnmindR(muon) > 0.4 and jj.returnmindR(tau) > 0.4):
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

               
#            if not len(veto_bjet) >= 1:
            if not len(veto_bjet) >= 1:
                continue


            counter[4] += 1

            stau = []

            selectedLeptons = []
            counter_pass = 0
            
            flag_SS = False
            flag_trigger = False
            flag_ltau_OS = False
            flag_mass = False
            flag_ltau_mass = False
            flag_veto = False



            ################################## selected muons ! 
            nplus = []
            nminus = []
            
            for ii in muon:
                if ii.charge==1:
                    nplus.append(ii)
                else:
                    nminus.append(ii)


#            import pdb; pdb.set_trace()
            if not (len(nplus)==2 or len(nminus)==2):
                continue


            muon1 = None
            muon2 = None
            
            if len(nplus)==2 and len(nminus)!=2:
                muon1 = nplus[0]
                muon2 = nplus[1]
            elif len(nplus)!=2 and len(nminus)==2:
                muon1 = nminus[0]
                muon2 = nminus[1]
            elif len(nplus)==2 and len(nminus)==2:

                if (nplus[0].pt + nplus[1].pt) > (nminus[0].pt + nminus[1].pt):
                    muon1 = nplus[0]
                    muon2 = nplus[1]
                else:
                    muon1 = nminus[0]
                    muon2 = nminus[1]


            if not muon1.charge*muon2.charge==1:
                continue

            flag_SS = True

            _muon1_ = None
            _muon2_ = None
            
            if muon1.pt > muon2.pt:
                _muon1_ = muon1
                _muon2_ = muon2

            if muon1.pt < muon2.pt:
                _muon1_ = muon2
                _muon2_ = muon1


            flag_iso = False
            
            if abs(_muon1_.eta) < 1.479:
                flag_iso = (_muon1_.reliso < 0.15)
            else:
                flag_iso = (_muon1_.reliso < 0.1)
                    
                    
            if flag_iso == False:
                continue
            

            if not ((muon1.pt > 20. and muon2.pt > 10. and muon1.trigmatch and muon2.trigmatch) or \
                    (muon1.pt > 10. and muon2.pt > 20. and muon1.trigmatch and muon2.trigmatch)
                    ):
                continue

            flag_trigger = True
                    
            if tool.diobj(muon1, muon2).returnmass() < 20:
                continue

            flag_mass = True

            for itau in tau:
                        
                if not itau.charge*muon1.charge==-1:
                    continue

                flag_ltau_OS = True

                if itau.returndR(muon1) < 0.5 or itau.returndR(muon2) < 0.5:
                    continue
                        
                if tool.diobj(itau, muon1).returnmass() > 71.2 and tool.diobj(itau, muon1).returnmass() < 111.2:
                    if not (itau.againstMuTight and
                            ((itau.decaymode==0 and itau.ep > 0.2) or (itau.decaymode!=0))):
                        
                        continue

                if tool.diobj(itau, muon2).returnmass() > 71.2 and tool.diobj(itau, muon2).returnmass() < 111.2:
                    if not (itau.againstMuTight and
                            ((itau.decaymode==0 and itau.ep > 0.2) or (itau.decaymode!=0))):
                        
                        continue

                # calculate M(l2,tau) => soft-lepton + tau
                Mass = -1
                if muon1.pt < muon2.pt:
                    Mass = tool.diobj(muon1, itau).returnmass()
                elif muon1.pt > muon2.pt:
                    Mass = tool.diobj(muon2, itau).returnmass()
                

                if Mass < 20.:
                    continue

                flag_ltau_mass = True

                # veto
                
                
                vmuon = []
                velectron = []
                vtau = []
                        
                for iv in veto_muon:            
                    if iv.returndR(muon1) > 0.4 and \
                           iv.returndR(muon2) > 0.4 and \
                           iv.returndR(itau) > 0.4:
                        vmuon.append(iv)
                        
                for iv in veto_electron:            
                    if iv.returndR(muon1) > 0.4 and \
                           iv.returndR(muon2) > 0.4 and \
                           iv.returndR(itau) > 0.4:
                        velectron.append(iv)
                        
                                
                for iv in veto_tau:            
                    if iv.returndR(muon1) > 0.4 and \
                           iv.returndR(muon2) > 0.4 and \
                           iv.returndR(itau) > 0.4:
                        vtau.append(iv)

                if not (len(vmuon)==0 and len(velectron)==0 and len(vtau)==0):
                    continue

                flag_veto = True
                        

                selectedLeptons.append((muon1, muon2, itau))
                                
                counter_pass += 1



            if not (len(selectedLeptons) >= 1):
                continue

            check_sumpt = 0

            for cid, icomp in enumerate(selectedLeptons):
                _sumpt_ = icomp[0].pt + icomp[1].pt + icomp[2].pt
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

            
            if flag_SS:
                counter[5] += 1
            if flag_trigger:
                counter[6] += 1
            if flag_ltau_OS:
                counter[7] += 1
            if flag_mass:
                counter[8] += 1
            if flag_ltau_mass:
                counter[9] += 1
            if flag_veto:
                counter[10] += 1


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

            for imuon, ismuon, itau in selectedLeptons:
                        
                weight = 1.
                isMC = False
                        
                if pname == 'data':
                    pass
                else:
                    weight = main.weight*imuon.trig*imuon.id*ismuon.trig*ismuon.id*lum_weight
                    isMC = True



                    
                kNN_muonjetpt = imuon.jetpt
                kNN_smuonjetpt = ismuon.jetpt
                        
                if kNN_muonjetpt == -999:
                    kNN_muonjetpt = imuon.pt
                            
                if kNN_smuonjetpt == -999:
                    kNN_smuonjetpt = ismuon.pt

                if kNN_muonjetpt < imuon.pt:
                    kNN_muonjetpt = imuon.pt

                if kNN_smuonjetpt < ismuon.pt:
                    kNN_smuonjetpt = ismuon.pt


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




                smuon_pt [0] = ismuon.pt
                smuon_eta [0] = ismuon.eta
                smuon_phi [0] = ismuon.phi
                smuon_mass [0] = ismuon.mass
                smuon_jetpt [0] = ismuon.jetpt
                smuon_id [0] = ismuon.isid
                smuon_iso [0] = ismuon.isiso
                smuon_reliso [0] = ismuon.reliso
                smuon_MT [0] = ismuon.MT
                smuon_charge [0] = ismuon.charge
                smuon_dpt [0] = ismuon.jetpt - ismuon.pt
                smuon_kNN_jetpt [0] = kNN_smuonjetpt
                smuon_dxy [0] = ismuon.dxy
                smuon_dz [0] = ismuon.dz
                smuon_dB3D [0] = ismuon.dB3D


                smuon_ipdg = 0
                smuon_min_dr = 100

                if pname != 'data':

                    for gen in gen_particle:
                        if ismuon.returndR(gen) < 0.5:
                            smuon_min_dr = ismuon.returndR(gen)
                            smuon_ipdg = gen.pdgid

                smuon_pdg[0] = smuon_ipdg

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
                
                    
                
                evt_Mmm [0] = tool.diobj(imuon, ismuon).returnmass()
                evt_Msmt [0] = tool.diobj(ismuon, itau).returnmass()
                evt_Mmt [0] = tool.diobj(imuon, itau).returnmass()
                evt_LT [0] = imuon.pt + ismuon.pt + itau.pt
                
                Mass = -1
                if imuon.pt < ismuon.pt:
                    Mass = tool.diobj(imuon, itau).returnmass()
                elif imuon.pt > ismuon.pt:
                    Mass = tool.diobj(ismuon, itau).returnmass()
                            
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
                    if not (jj.returndR(imuon) < 0.4 or jj.returndR(ismuon) < 0.4 or jj.returndR(itau) < 0.4):
                        dr = jj.returndR(imuon)
                        if dr < min_dr_mu:
                            min_dr_mu = dr
                            min_dr_mu_csv = jj.mva

                min_dr_e = 1000
                min_dr_e_csv = -1

                for jj in veto_jet:
                    if not (jj.returndR(imuon) < 0.4 or jj.returndR(ismuon) < 0.4 or jj.returndR(itau) < 0.4):
                        dr = jj.returndR(ismuon)
                        if dr < min_dr_e:
                            min_dr_e = dr
                            min_dr_e_csv = jj.mva
                            
                min_dr_tau = 1000
                min_dr_tau_csv = -1
                
                for jj in veto_jet:
                    if not (jj.returndR(imuon) < 0.4 or jj.returndR(ismuon) < 0.4 or jj.returndR(itau) < 0.4):
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
                    if jj.returndR(ismuon) < 0.5:
                        dr = jj.returndR(ismuon)
                        if dr < csv_min_dr_e:
                            csv_min_dr_e = dr
                            csv_min_dr_e_csv = jj.mva
                            eratio = ismuon.pt/jj.pt
                            
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

                smuon_jet_csv [0] = csv_min_dr_e_csv
                muon_jet_csv [0] = csv_min_dr_mu_csv
                tau_jet_csv [0] = csv_min_dr_tau_csv
                smuon_jet_csv_10 [0] = ismuon.csv_10
                muon_jet_csv_10 [0] = imuon.csv_10
                muon_ptratio[0] = mratio
                tau_ptratio[0] = tratio
                muon_mva[0] = imuon.mva
                
                muon_mva_ch_iso[0] = imuon.mva_ch_iso
                muon_mva_neu_iso[0] = imuon.mva_neu_iso
                muon_mva_jet_dr[0] = imuon.mva_jet_dr
                muon_mva_ptratio[0] = imuon.mva_ptratio
                muon_mva_csv[0] = imuon.mva_csv
                muon_new_mva[0] = imuon.new_mva
                
                evt_dr_mujet[0] = min_dr_mu
                evt_dr_smujet[0] = min_dr_e
                evt_dr_taujet[0] = min_dr_tau
                evt_dr_mujet_csv[0] = min_dr_mu_csv
                evt_dr_smujet_csv[0] = min_dr_e_csv
                evt_dr_taujet_csv[0] = min_dr_tau_csv

                
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
                evt_dphi_mete[0]   = ismuon.phi - main.pfmetphi
                evt_dphi_mettau[0] = itau.phi - main.pfmetphi

                maxMT = imuon.MT

                if imuon.MT < ismuon.MT:
                    maxMT = ismuon.MT

                deltaeta = Double(Double(imuon.eta + ismuon.eta + itau.eta)/3. - max_jet_eta_sign)
                deltaeta_notau = Double(Double(imuon.eta + ismuon.eta)/3. - max_jet_eta_sign)

                
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
                    mvar_map['lepton_kNN_jetpt'][0] = kNN_muonjetpt
                    mvar_map['evt_njet'][0] = main.nJets + 1
                    
                    weight_muon = muonreader.EvaluateMVA('muon_data')
                    
                if options.mode=='antiE' or options.mode=='antiEMu':

                    evar_map['lepton_pt'][0] = ismuon.pt
                    evar_map['lepton_kNN_jetpt'][0] = kNN_electronjetpt
                    evar_map['evt_njet'][0] = main.nJets + 1
                    
                    weight_electron = electronreader.EvaluateMVA('electron_data')

               
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
        for ic in range(11):
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




    
