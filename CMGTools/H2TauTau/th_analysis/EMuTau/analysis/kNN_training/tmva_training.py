import ROOT
import optparse, os

### For options
parser = optparse.OptionParser()
parser.add_option('--channel', action="store", dest="channel", default='electron')
parser.add_option('--process', action="store", dest="process", default='data')
options, args = parser.parse_args()

print 'channel = ', options.channel
print 'process = ', options.process


TMVA_tools = ROOT.TMVA.Tools.Instance()

lname = options.channel
process = options.process
fname = ''

if process == 'data':
    fname = 'Wjet_' + lname + '_training.root'
else:
    fname = 'Wjet_' + lname + '_training_' + process + '.root'

nNeighbours = 50

dir="/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/analysis/root_aux_nobjet/"

file_data = ROOT.TFile(dir + fname)
tree_data = file_data.Get('kNNTrainingTree')

#training_vars = ['lepton_pt', 'lepton_eta', 'lepton_kNN_jetpt', 'evt_njet']
training_vars = ['lepton_pt', 'lepton_kNN_jetpt', 'evt_njet']

#((abs(mchain.muon_eta) < 1.479 and mva_iso_muon > mva_muon_barrel) or \
 #(abs(mchain.muon_eta) > 1.479 and mva_iso_muon > mva_muon_endcap)))):

#mva_muon_barrel = 0.0089
#mva_electron_barrel = 0.0649

#mva_muon_endcap = 0.0621
#mva_electron_endcap = 0.0891


#signal_selection = basic_selection + '(lepton_iso && lepton_id)'
#background_selection = basic_selection + '(!lepton_iso || !lepton_id)'


signal_selection = '(lepton_id > 0.5 && lepton_mva > lepton_mva_threshold)'
background_selection = '!' + signal_selection #(!lepton_iso || !lepton_id)'

num_pass = tree_data.GetEntries(signal_selection)
num_fail = tree_data.GetEntries(background_selection)

outFile = ROOT.TFile('TMVA.root', 'recreate')

factory    = ROOT.TMVA.Factory(
    "TMVAClassification", 
    outFile, 
    "!V:!Silent:Color:DrawProgressBar:Transformations=I" ) 

for var in training_vars:
    factory.AddVariable(var, 'F') 

if process=='data':
    factory.SetWeightExpression('evt_weight*evt_isMCw')
else:
    factory.SetWeightExpression('evt_weight')

factory.SetInputTrees(tree_data, ROOT.TCut(signal_selection), ROOT.TCut(background_selection))
factory.PrepareTrainingAndTestTree( ROOT.TCut(''), ROOT.TCut(''),
                                    "nTrain_Signal={num_pass}:nTrain_Background={num_fail}:SplitMode=Random:NormMode=None:!V" )

factory.BookMethod( 
    ROOT.TMVA.Types.kKNN, "KNN50", 
    "H:nkNN=50:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T")


factory.TrainAllMethods()

os.system('cp ' + dir + fname +' data/Wjet_' + lname + '_training_' + process + '_knn.root')

import NtupleTMVAEvaluate
n = NtupleTMVAEvaluate.NtupleTMVAEvaluate('data/Wjet_' + lname + '_training_' + process + '_knn.root')

n.addMVAMethod('KNN50', 'kNN50Output', 'weights/TMVAClassification_KNN50.weights.xml')
n.setVariables(training_vars)
n.process()


os.system('mv weights/TMVAClassification_KNN50.weights.xml weights/KNN_' + process + '_' + lname + '_50.xml')

