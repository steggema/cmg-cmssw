import ROOT
import optparse, os
import array

### For options
parser = optparse.OptionParser()
parser.add_option('--channel', action="store", dest="channel", default='none')
options, args = parser.parse_args()

ROOT.gROOT.SetBatch(True)

print 'channel = ', options.channel

lname = options.channel
fname = 'f3_antiEMu.root'

if options.channel == 'electron':
    fname = 'f12_antiMu.root'
elif options.channel == 'muon':
    fname = 'f12_antiE.root'
elif options.channel == 'signal':
    fname = 'f3_signal.root'
dir="/afs/cern.ch/user/s/steggema/work/Yuta/CMSSW_5_3_19/src/CMGTools/H2TauTau/th_analysis/EMuTau/analysis/root_process/"

file_data = ROOT.TFile(dir + fname)
tree_data = file_data.Get('Tree')


fcontrol = "/afs/cern.ch/user/s/steggema/work/Yuta/CMSSW_5_3_19/src/CMGTools/H2TauTau/th_analysis/EMuTau/analysis/root_process/f12_antiEMu.root"

file_control = ROOT.TFile(fcontrol)
tree_control = file_control.Get('Tree')

# baseline_selection = 'evt_nbjet==1&&(!evt_isMC || evt_id==0 || evt_id==1 || evt_id==18 || evt_id==19)'
baseline_selection = ''

signal_selection = ''

signal_selection += ''

num_pass = tree_data.GetEntries(signal_selection)

var_dict = {
    'tau_pt':{'nbins':30, 'xmin':0., 'xmax':200., 'title':'tau p_{T} (GeV)'},
    'tau_MT':{'nbins':30, 'xmin':0., 'xmax':300., 'title':'M_{T} tau'},
    'evt_maxMT':{'nbins':30, 'xmin':0., 'xmax':300., 'title':'max(M_{T})'},
    'evt_max_jet_eta':{'nbins':30, 'xmin':-5., 'xmax':5., 'title':'max(jet #eta)'},
    'muon_pt':{'nbins':30, 'xmin':0., 'xmax':100., 'title':'muon p_{T} (GeV)'},
    'muon_eta':{'nbins':30, 'xmin':-2.5, 'xmax':2.5, 'title':'muon #eta'},
    'muon_reliso':{'nbins':30, 'xmin':0., 'xmax':10., 'title':'muon relative isolation'},
    'muon_MT':{'nbins':30, 'xmin':0., 'xmax':300., 'title':'M_{T} muon'},
    'muon_kNN_jetpt':{'nbins':30, 'xmin':0., 'xmax':100., 'title':'muon jet p_{T}'},
    'evt_Mem':{'nbins':30, 'xmin':0., 'xmax':400., 'title':'m(e, #mu) (GeV)'},
    'electron_pt':{'nbins':30, 'xmin':0., 'xmax':100., 'title':'electron p_{T} (GeV)'},
    'electron_eta':{'nbins':30, 'xmin':-2.5, 'xmax':2.5, 'title':'electron #eta'},
    'electron_reliso':{'nbins':30, 'xmin':0., 'xmax':10., 'title':'electron relative isolation'},
    'electron_MT':{'nbins':30, 'xmin':0., 'xmax':300., 'title':'M_{T} electron (GeV)'},
    'evt_njet':{'nbins':15, 'xmin':-0.5, 'xmax':14.5, 'title':'n_{jets}'},
    'evt_nbjet':{'nbins':15, 'xmin':-0.5, 'xmax':14.5, 'title':'n_{b jets}'},
    'muon_new_mva':{'nbins':30, 'xmin':-0.5, 'xmax':0.5, 'title':'muon MVA'},
    'electron_new_mva':{'nbins':30, 'xmin':-0.5, 'xmax':0.5, 'title':'electron MVA'},
    'evt_missing_et':{'nbins':30, 'xmin':0., 'xmax':200, 'title':'E_{T}^{miss} (GeV)'},
    'muon_pdg':{'nbins':31, 'xmin':-15.5, 'xmax':15.5, 'title':'muon PDG'},
    'electron_pdg':{'nbins':31, 'xmin':-15.5, 'xmax':15.5, 'title':'electron PDG'},
}

from config import filedict, hist_dict, col_red


samples = [s for s in filedict]
samples.sort()

for var in var_dict:
    vd = var_dict[var]
    vd['hist_data'] = ROOT.TH1F(var+'_data', '', vd['nbins'], vd['xmin'], vd['xmax'])
    vd['hist_data'].Sumw2()
    vd['hist_data'].GetXaxis().SetTitle(vd['title'])
    vd['hist_data'].GetYaxis().SetTitle('Events')
    vd['mc_stack'] = ROOT.THStack('sum_mc'+var, '')

    vd['hist_control'] = ROOT.TH1F(var+'_control', '', vd['nbins'], vd['xmin'], vd['xmax'])
    vd['hist_control'].Sumw2()
    vd['hist_control'].GetXaxis().SetTitle(vd['title'])
    vd['hist_control'].GetYaxis().SetTitle('Events')
    vd['hist_control'].SetLineColor(ROOT.kMagenta-10)
    vd['hist_control'].SetFillColor(ROOT.kMagenta-10)

    for sample in samples:
        if sample == 'data':
            continue
        vd['hist_'+sample] = ROOT.TH1F(var+sample, '', vd['nbins'], vd['xmin'], vd['xmax'])
        vd['hist_'+sample].Sumw2()
        vd['hist_'+sample].SetLineColor(hist_dict[sample]['color'])
        vd['hist_'+sample].SetFillColor(hist_dict[sample]['color'])
        vd['mc_stack'].Add(vd['hist_'+sample])
        vd['hist_'+sample].GetXaxis().SetTitle(vd['title'])
    vd['mc_stack'].Add(vd['hist_control'])


for evt in tree_data:
    # if not evt.evt_nbjet==2:
    #     continue
    if not evt.evt_isMC:    
        for var in var_dict:
            vd = var_dict[var]
            vd['hist_data'].Fill(getattr(evt, var), evt.evt_weight)
    else:
        for var in var_dict:
            vd = var_dict[var]
            for sample in samples:
                if sample == 'data':
                    continue
                if filedict[sample][3] == evt.evt_id:
                    vd['hist_'+sample].Fill(getattr(evt, var), evt.evt_weight)

for evt in tree_control:
    # if not evt.evt_nbjet==2:
    #     continue
    if options.channel == 'muon':
        mva = evt.muon_kNN
    elif options.channel == 'electron':
        mva = evt.electron_kNN
    else:
        mva = 0.
    for var in var_dict:
        vd = var_dict[var]
        if not evt.evt_isMC:
            vd['hist_control'].Fill(getattr(evt, var), mva/(1.-mva))
        else:
            # Subtract MC background; subtract in same phase space
            vd['hist_control'].Fill(getattr(evt, var), -mva/(1.-mva)*evt.evt_weight)


cv = ROOT.TCanvas()
for var in var_dict:
    legend = ROOT.TLegend(0.75, 0.65, 0.95, 0.95)
    legend.AddEntry(vd['hist_data'], 'Data', 'l')
    legend.AddEntry(vd['hist_ZZ'], 'Diboson', 'f')
    legend.AddEntry(vd['hist_W4jet'], 'W+jets', 'f')
    legend.AddEntry(vd['hist_tt1l'], 'Top', 'f')
    # legend.AddEntry(vd['hist_tt2l'], 'Dilepton top', 'f')
    legend.AddEntry(vd['hist_control'], 'Reducible', 'f')
    legend.AddEntry(vd['hist_TTW'], 'Top+V', 'f')
    legend.AddEntry(vd['hist_DY4'], 'DY', 'f')

    
    vd = var_dict[var]
    vd['hist_data'].SetMinimum(0.)
    vd['hist_data'].SetLineColor(1)
    vd['hist_data'].SetLineWidth(3)
    vd['hist_data'].Draw('E')
    vd['hist_data'].SetMinimum(0.)
    vd['mc_stack'].Draw('same hist')
    vd['hist_data'].Draw('same e')
    vd['sum_mc'] = vd['mc_stack'].GetStack().Last().Clone()

    # vd['hist_control'].SetLineColor(col_red)
    # # vd['hist_control'].SetLineStyle(2)
    # vd['hist_control'].SetLineWidth(3)
    # vd['hist_control'].SetFillColor(col_red)
    # vd['hist_control'].Draw('same hist')

    # vd['hist_mc'].SetLineColor(2)
    # vd['hist_mc'].Draw('same')
    print 'Integral data', vd['hist_data'].Integral()
    print 'Integral MC', sum(m.Integral() for m in vd['mc_stack'].GetHists())
    legend.Draw()
    print 'Integral red', vd['hist_control'].Integral()

    cv.Print('f3plots/'+var+'.pdf')

    vd['hist_data'].Divide(vd['sum_mc'])
    vd['hist_data'].GetYaxis().SetTitle('Data/MC')
    vd['hist_data'].Draw('e')
    vd['hist_data'].GetYaxis().SetRangeUser(0., 2.)
    vd['hist_data'].Fit('pol1')
    line = ROOT.TLine()
    line.SetLineColor(ROOT.kGray)
    line.DrawLine(vd['hist_data'].GetXaxis().GetXmin(), 1., vd['hist_data'].GetXaxis().GetXmax(), 1.)
    
    cv.Print('f3plots/'+var+'_ratio.pdf')


