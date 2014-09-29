import ROOT
TMVA_tools = ROOT.TMVA.Tools.Instance()


file_data = ROOT.TFile('data/Wjet_muon_training_data.root')
tree_data = file_data.Get('kNNTrainingTree')
# file_wz = ROOT.TFile('data/Wjet_muon_training_WZ.root')
# file_zz = ROOT.TFile('data/Wjet_muon_training_WZ.root')

training_vars = ['lepton_pt', 'lepton_jetpt', 'lepton_reliso'] #, 'lepton_njet']

nNeighbours = 100


basic_selection = 'lepton_jetpt>0. &&' # '(lepton_njet>0. && lepton_jetpt>0.) &&'

# signal_selection = basic_selection + '(lepton_iso && lepton_id)'

# background_selection = basic_selection + '(!lepton_iso || !lepton_id)'

signal_selection = basic_selection + '(lepton_iso && lepton_id)'

background_selection = basic_selection + '(!lepton_iso && lepton_id)'


num_pass = tree_data.GetEntries(signal_selection)
num_fail = tree_data.GetEntries(background_selection)

outFile = ROOT.TFile('TMVA.root', 'RECREATE')

factory    = ROOT.TMVA.Factory(
    "TMVAClassification", 
    outFile, 
    "!V:!Silent:Color:DrawProgressBar:Transformations=I" ) 

for var in training_vars:
    factory.AddVariable(var, 'F') # add float variable

factory.SetWeightExpression('lepton_weight')

factory.SetInputTrees(tree_data, ROOT.TCut(signal_selection), ROOT.TCut(background_selection))

factory.PrepareTrainingAndTestTree( ROOT.TCut(''), ROOT.TCut(''),
                                    "nTrain_Signal={num_pass}:nTrain_Background={num_fail}:SplitMode=Random:NormMode=None:!V" )

factory.BookMethod( 
    ROOT.TMVA.Types.kKNN, "KNN", 
    "H:nkNN={nNeighbours}:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T".format(nNeighbours=nNeighbours))

factory.BookMethod( 
    ROOT.TMVA.Types.kKNN, "KNN50", 
    "H:nkNN=50:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T")

factory.BookMethod( 
    ROOT.TMVA.Types.kKNN, "KNN25", 
    "H:nkNN=25:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T")

factory.TrainAllMethods()

import os
os.system('cp data/Wjet_muon_training_data.root data/Wjet_muon_training_data_knn.root')

import NtupleTMVAEvaluate
n = NtupleTMVAEvaluate.NtupleTMVAEvaluate('data/Wjet_muon_training_data_knn.root')
n.addMVAMethod('KNN', 'kNNOutput', 'weights/TMVAClassification_KNN.weights.xml')
n.addMVAMethod('KNN50', 'kNN50Output', 'weights/TMVAClassification_KNN50.weights.xml')
n.addMVAMethod('KNN25', 'kNN25Output', 'weights/TMVAClassification_KNN25.weights.xml')
n.setVariables(training_vars)
n.process()
