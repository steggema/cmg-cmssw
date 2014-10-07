import ROOT
import optparse, os
import array

### For options
parser = optparse.OptionParser()
parser.add_option('--channel', action="store", dest="channel", default='electron')
options, args = parser.parse_args()

ROOT.gROOT.SetBatch(True)

print 'channel = ', options.channel

lname = options.channel
fname = ''

fname = 'f3_antiE.root'
dir="/afs/cern.ch/user/s/steggema/work/Yuta/CMSSW_5_3_19/src/CMGTools/H2TauTau/th_analysis/EMuTau/analysis/root_process/"

file_data = ROOT.TFile(dir + fname)
tree_data = file_data.Get('Tree')


# baseline_selection = 'evt_nbjet==1&&(!evt_isMC || evt_id==0 || evt_id==1 || evt_id==18 || evt_id==19)'
baseline_selection = ''

signal_selection = ''

signal_selection += ''

num_pass = tree_data.GetEntries(signal_selection)

var_dict = {
    'muon_pt':{'nbins':30, 'xmin':0., 'xmax':100., 'title':'muon p_{T} (GeV)'},
    'muon_eta':{'nbins':30, 'xmin':-2.5, 'xmax':2.5, 'title':'muon #eta'},
    'muon_MT':{'nbins':30, 'xmin':0., 'xmax':40., 'title':'M_{T} muon'},
    'muon_kNN_jetpt':{'nbins':30, 'xmin':0., 'xmax':100., 'title':'muon jet p_{T}'},
    'evt_Mem':{'nbins':30, 'xmin':0., 'xmax':400., 'title':'m(e, #mu) (GeV)'},
    'electron_pt':{'nbins':30, 'xmin':0., 'xmax':100., 'title':'electron p_{T} (GeV)'},
    'electron_eta':{'nbins':30, 'xmin':-2.5, 'xmax':2.5, 'title':'electron #eta'},
    'electron_MT':{'nbins':30, 'xmin':0., 'xmax':300., 'title':'M_{T} electron (GeV)'},
    'evt_njet':{'nbins':10, 'xmin':-0.5, 'xmax':9.5, 'title':'n_{jets}'},
    'muon_new_mva':{'nbins':30, 'xmin':-0.5, 'xmax':0.5, 'title':'muon MVA'},
    'electron_new_mva':{'nbins':30, 'xmin':-0.5, 'xmax':0.5, 'title':'electron MVA'},
    'evt_missing_et':{'nbins':30, 'xmin':0., 'xmax':100, 'title':'E_{T}^{miss} (GeV)'},
}

from config import filedict, hist_dict


samples = [s for s in filedict]
samples.sort()

for var in var_dict:
    vd = var_dict[var]
    vd['hist_data'] = ROOT.TH1F(var+'_data', '', vd['nbins'], vd['xmin'], vd['xmax'])
    vd['hist_data'].Sumw2()
    vd['hist_data'].GetXaxis().SetTitle(vd['title'])
    vd['hist_data'].GetYaxis().SetTitle('Events')
    vd['mc_stack'] = ROOT.THStack('sum_mc'+var, '')

    for sample in samples:
        if sample == 'data':
            continue
        vd['hist_'+sample] = ROOT.TH1F(var+sample, '', vd['nbins'], vd['xmin'], vd['xmax'])
        vd['hist_'+sample].Sumw2()
        vd['hist_'+sample].SetLineColor(hist_dict[sample]['color'])
        vd['hist_'+sample].SetFillColor(hist_dict[sample]['color'])
        vd['mc_stack'].Add(vd['hist_'+sample])
        vd['hist_'+sample].GetXaxis().SetTitle(vd['title'])


for evt in tree_data:
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

cv = ROOT.TCanvas()
for var in var_dict:
    legend = ROOT.TLegend(0.75, 0.65, 0.95, 0.95)
    legend.AddEntry(vd['hist_data'], 'Data', 'l')
    legend.AddEntry(vd['hist_ZZ'], 'Diboson', 'f')
    legend.AddEntry(vd['hist_W4jet'], 'W+jets', 'f')
    legend.AddEntry(vd['hist_tt1l'], 'Top', 'f')
    legend.AddEntry(vd['hist_tt2l'], 'Dilepton top', 'f')
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
    # vd['hist_mc'].SetLineColor(2)
    # vd['hist_mc'].Draw('same')
    print 'Integral data', vd['hist_data'].Integral()
    print 'Integral MC', sum(m.Integral() for m in vd['mc_stack'].GetHists())
    legend.Draw()

    cv.Print('f3plots/'+var+'.pdf')

