from collections import namedtuple

import ROOT

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import VariableCfg
from CMGTools.H2TauTau.proto.plotter.ROCPlotter import histsToRoc, makeROCPlot

# f_root = ROOT.TFile('BatchTest/TTJets/MuonTreeProducer/tree.root')
# tree = f_root.Get('tree')

tree_s = ROOT.TChain('tree')
# tree_s.AddFile('BatchDY/DY/MuonTreeProducer/tree.root')
tree_s.AddFile('BatchTest/TTJets/MuonTreeProducer/tree.root')

tree_b = ROOT.TChain('tree')
# tree_b.AddFile('BatchTest/TTJets/MuonTreeProducer/tree.root')
tree_b.AddFile('BatchRest/QCD120/MuonTreeProducer/tree.root')
tree_b.AddFile('BatchRest/QCD20/MuonTreeProducer/tree.root')

VarSet = namedtuple('VariableSet', ['name', 'vars', 'cut_s', 'cut_b'])

vars = [
    VariableCfg(name='pf_iso03', drawname='pf_iso03_pt/muon_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 100.}, unit='', xtitle='PF iso 0.3 from packed'),
    VariableCfg(name='pf_iso03obj', drawname='(pf03sumChargedHadronPt + pf03sumNeutralHadronEt + pf03sumPhotonEt)/muon_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 100.}, unit='', xtitle='PF iso 0.3'),
    VariableCfg(name='pf_iso03obj_all', drawname='(pf03sumChargedParticlePt + pf03sumNeutralHadronEt + pf03sumPhotonEt)/muon_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 100.}, unit='', xtitle='PF iso 0.3 all charged'),
    # VariableCfg(name='pf_iso03objnonh_all', drawname='(pf03sumChargedParticlePt + pf03sumPhotonEt)/muon_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 100.}, unit='', xtitle='PF no NH iso 0.3 all charged'),
    VariableCfg(name='det_iso03', drawname='(det03emEt + det03hadEt + det03sumPt)/muon_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 100.}, unit='', xtitle='Det iso 0.3'),
    VariableCfg(name='det_iso05', drawname='(det05emEt + det05hadEt + det05sumPt)/muon_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 100.}, unit='', xtitle='Det iso 0.5'),
    VariableCfg(name='pf_iso04obj', drawname='(pf04sumChargedHadronPt + pf04sumNeutralHadronEt + pf04sumPhotonEt)/muon_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 100.}, unit='', xtitle='PF iso 0.4'),
    VariableCfg(name='pf_iso05obj', drawname='pf_iso05_pt/muon_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 100.}, unit='', xtitle='PF iso 0.5 from packed'),
]

vars2 = [
    VariableCfg(name='det03sumPt', drawname='det03sumPt/muon_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 100.}, unit='', xtitle='Det track only 0.3'),
    VariableCfg(name='pf03sumChargedParticlePt', drawname='pf03sumChargedParticlePt/muon_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 100.}, unit='', xtitle='PF all charged 0.3'),
    VariableCfg(name='det03emEt', drawname='det03emEt/muon_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 100.}, unit='', xtitle='Det EM only 0.3'),
    VariableCfg(name='pf03sumPhotonEt', drawname='pf03sumPhotonEt/muon_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 100.}, unit='', xtitle='PF photon 0.3'),
    VariableCfg(name='det03hadEt', drawname='det03hadEt/muon_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 100.}, unit='', xtitle='Det had only 0.3'),
    VariableCfg(name='pf03sumNeutralHadronEt', drawname='pf03sumNeutralHadronEt/muon_pt', binning={'nbinsx': 10000, 
        'xmin': 0., 'xmax': 100.}, unit='', xtitle='PF neutral hadron 0.3'),
    VariableCfg(name='pf03sumChargedHadronPt', drawname='pf03sumChargedHadronPt/muon_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 100.}, unit='', xtitle='PF charged hadron 0.3'),
]

var_sets = [
    VarSet('iso03', vars, 'abs(gen_pdgId) < 20 && muon_pt > 15', 'abs(gen_pdgId) > 20 && muon_pt > 15'),
    # VarSet('subdets', vars2, 'abs(gen_pdgId) < 20', 'abs(gen_pdgId) > 20'),
]

rocs = []

for var_set in var_sets:
    cut_s = var_set.cut_s
    cut_b = var_set.cut_b

    print 'Cuts'
    print cut_s
    print cut_b

    for var in var_set.vars:
        h_s_name = var_set.name + var.name + 's'
        h_b_name = var_set.name + var.name + 'b'

        h_signal = ROOT.TH1F(h_s_name, '', var.binning['nbinsx'], var.binning['xmin'], var.binning['xmax'])
        h_bg = ROOT.TH1F(h_b_name, '', var.binning['nbinsx'], var.binning['xmin'], var.binning['xmax'])

        tree_s.Project(h_s_name, var.drawname, cut_s)
        tree_b.Project(h_b_name, var.drawname, cut_b)

        roc = histsToRoc(h_signal, h_bg)
        roc.title = var.xtitle
        roc.name = var.name

        rocs.append(roc)

    allrocs = makeROCPlot(rocs, var_set.name, xmin=0.8, ymin=0.002, ymax=0.2, logy=False)
