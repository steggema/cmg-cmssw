import ROOT
TMVA_tools = ROOT.TMVA.Tools.Instance()


file_data = ROOT.TFile('data/Wjet_muon_training_data_knn.root')
tree_data = file_data.Get('kNNTrainingTree')

plot_vars = ['lepton_pt', 'lepton_jetpt'] #, 'lepton_njet']

basic_selection = '(lepton_jetpt>0.)*' # '(lepton_njet>0. && lepton_jetpt>0.) &&'
signal_selection = basic_selection + '(lepton_iso && lepton_id)'
background_selection = basic_selection + '(!lepton_iso || !lepton_id)'


c = ROOT.TCanvas()
for var in plot_vars:
    hist = ROOT.TH1F(var, var, 20, 0., 200.)
    tree_data.Project(var, var, background_selection + '*kNNOutput/(1.-kNNOutput)')
    hist.DrawCopy()

    histSignal = ROOT.TH1F(var+'s', var+'s', 20, 0., 200.)
    tree_data.Project(var+'s', var, signal_selection + '')

    histSignal.SetLineColor(2)
    histSignal.SetLineStyle(2)
    histSignal.DrawCopy('same')

    c.Print('plots/'+var+'.pdf')
