from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
from CMGTools.H2TauTau.proto.plotter.categories_MuMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import getVars, mumu_vars
from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff, getPUWeight


total_weight = 'weight * ' + getPUWeight()

cuts = {}

inc_cut = '&&'.join([cat_Inc])

cuts['OS_mZ_PU'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis > 50.'

cuts['OS_mZ_PU_vetob'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis > 50. && n_bjets == 0'
cuts['OS_mZ_PU_1jet'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis > 50. && n_jets>=1'
cuts['OS_mZ_PU_1bjet'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis > 50. && n_bjets>=1'

int_lumi = 1560.

# -> Command line
analysis_dir = '/afs/cern.ch/user/s/steggema/work/public/mm/MiniAODv2'
tree_prod_name = 'H2TauTauTreeProducerMuMu'

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir, tree_prod_name,  ztt_cut='(l1_gen_match == 4 && l2_gen_match == 4)', zl_cut='(l1_gen_match == 2 && l2_gen_match == 2)', zj_cut='(l1_gen_match != l2_gen_match || (l1_gen_match != 4 && l1_gen_match != 2))')

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = getVars(['l1_pt', 'l2_pt', 'l1_gen_pdgId', 'l2_gen_pdgId', 'l1_reliso05_04', 'l1_reliso05', 'l2_byCombinedIsolationDeltaBetaCorrRaw3Hits'])


variables = getVars(['_norm_', 'tau1_pt', 'tau1_eta', 'tau1_mass', 'tau1_decayMode', 'mvis', 'mt', 'tau1_gen_pdgId', 'l2_mt', 'n_vertices', 'met_phi', 'met_pt'])
# variables = all_vars


for cut_name in cuts:
    cfg_tight = HistogramCfg(name='tight', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight+' * ((tau1_gen_match != 5) - (tau1_gen_match == 5))')
    cfg_loose = HistogramCfg(name='loose', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight+' * ((tau1_gen_match != 5) - (tau1_gen_match == 5))')

    cfg_data_tight = HistogramCfg(name='tight_data', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight+' * ((genmet_pt < 0.) - (tau1_gen_match == 5))')
    cfg_data_loose = HistogramCfg(name='loose_data', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight+' * ((genmet_pt < 0.) - (tau1_gen_match == 5))')


    cfg_tight.cut = cuts[cut_name] + '&& tau1_byCombinedIsolationDeltaBetaCorrRaw3Hits<1.5 && tau1_pt > 0.'
    cfg_loose.cut = cuts[cut_name] +  '&& tau1_pt > 0.'
    cfg_data_tight.cut = cuts[cut_name] + '&& tau1_byCombinedIsolationDeltaBetaCorrRaw3Hits<1.5 && tau1_pt > 0.'
    cfg_data_loose.cut = cuts[cut_name] + '&& tau1_pt > 0.'

    for variable in variables:
        cfg_tight.var = variable
        cfg_loose.var = variable
        cfg_data_tight.var = variable
        cfg_data_loose.var = variable
        
        plot_tight = createHistogram(cfg_tight, verbose=False)
        plot_loose = createHistogram(cfg_loose, verbose=False)
        plot_data_tight = createHistogram(cfg_data_tight, verbose=False, all_stack=True)
        plot_data_loose = createHistogram(cfg_data_loose, verbose=False, all_stack=True)
        for plot in [plot_tight, plot_loose, plot_data_tight, plot_data_loose]:
            plot.Group('VV', ['ZZ', 'WZ', 'WW', 'T_tWch', 'TBar_tWch'])
            # out_dir = 'fakeplots/'+cut_name if plot is plot_tight else 'fakeplots/loose'+cut_name
            # HistDrawer.draw(plot, plot_dir='fakeplots/'+cut_name)

        plotDataOverMCEff(plot_tight.GetStack().totalHist.weighted, 
                          plot_loose.GetStack().totalHist.weighted, 
                          plot_data_tight.GetStack().totalHist.weighted, 
                          plot_data_loose.GetStack().totalHist.weighted,
                          'fakeplots/fakerate_' + variable.name + cut_name + '.pdf')


