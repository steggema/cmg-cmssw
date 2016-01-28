import copy

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
from CMGTools.H2TauTau.proto.plotter.categories_MuMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import getVars, mumu_vars
from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists
from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff, getPUWeight


total_weight = 'weight * ' + getPUWeight()
total_weight = 'weight'

print 'Total weight', total_weight

int_lumi = 2240.

cuts = {}

inc_cut = '&&'.join([cat_Inc])


# cuts['OS_mZ_PU_lowmtmet'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis > 50. && mt<5. && met_pt < 1.'

# cuts['OS_mZ_PU_vetolowmtmt'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis > 50. && !(mt<5. && met_pt < 1.)'

cuts['OS_PU'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1'
# cuts['OS_mZ_PU_MT5'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis > 50. && mt<5.'
# cuts['OS_mZ_PU'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis > 50.'
# cuts['OS_mZ_PU_vetob'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis > 50. && n_bjets == 0'
# cuts['OS_mZ_PU_1jet'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis > 50. && n_jets>=1'
# cuts['OS_mZ_PU_1bjet'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis > 50. && n_bjets>=1'

# cuts['OS_VetomZ_PU_1bjet'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && (mvis < 80. || mvis > 100.) && mvis > 50. && n_bjets>=1'

# cuts['OS_lowmZ_PU_1bjet'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis < 50. && n_bjets>=1'

# cuts['SS_mZ_PU'] = inc_cut + '&& l1_charge == l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis > 50.'
# cuts['OS_mZ_PU_tauDM'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis > 50. && tau1_decayModeFinding'


qcd_from_same_sign = False

# -> Command line
analysis_dir = '/afs/cern.ch/user/s/steggema/work/public/mm/190116'
tree_prod_name = 'H2TauTauTreeProducerMuMu'

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir, tree_prod_name,  ztt_cut='(l1_gen_match == 4 && l2_gen_match == 4)', zl_cut='(l1_gen_match == 2 && l2_gen_match == 2)', zj_cut='(l1_gen_match != l2_gen_match || (l1_gen_match != 4 && l1_gen_match != 2))')

if qcd_from_same_sign:
    samples_qcdfromss = [s for s in samples if s.name != 'QCD']
    samples_ss = copy.deepcopy(samples_qcdfromss)

    scale = 1.06

    for sample in samples_ss:
        sample.scale = scale
        if sample.name != 'Data':
            # Subtract background from data
            sample.scale = -scale

    qcd = HistogramCfg(name='QCD', var=None, cfgs=samples_ss, cut=inc_cut, lumi=int_lumi)

    samples_qcdfromss.append(qcd)

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = mumu_vars
# variables = getVars(['mt'])
# variables = [
#     VariableCfg(name='mvis', binning={'nbinsx':35, 'xmin':0, 'xmax':350}, unit='GeV', xtitle='m_{vis}')
# ]

for cut_name in cuts:
    if  qcd_from_same_sign and not 'SS' in cut_name :
        cfg_example = HistogramCfg(name='example', var=None, cfgs=samples_qcdfromss, cut=inc_cut, lumi=int_lumi, weight=total_weight)
    else:
        cfg_example = HistogramCfg(name='example', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight)
        

    cfg_example.cut = cuts[cut_name]
    if qcd_from_same_sign and 'OS' in cut_name:
        qcd.cut = cuts[cut_name].replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

    for variable in variables:
        cfg_example.var = variable
        if qcd_from_same_sign:
            qcd.var = variable # Can put into function but we will not want it by default if we take normalisations from e.g. high MT
        
        plot = createHistogram(cfg_example, verbose=True)
        plot.Group('VV', ['ZZ', 'WZ', 'WW', 'T_tWch', 'TBar_tWch'])
        plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TToLeptons_sch', 'TToLeptons_tch'])
        # plot.Group('ZLL', ['ZL', 'ZJ'], style=plot.Hist('ZL').style)
        HistDrawer.draw(plot, plot_dir='plots/'+cut_name)

        # plot.WriteDataCard(filename='datacard_mm.root', dir='mm_' + cut_name)
