import ROOT
import optparse

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

file_data = ROOT.TFile('/afs/cern.ch/work/y/ytakahas/VH_analysis/CMGTools/CMSSW_5_3_9/src/CMGTools/H2TauTau/WH_analysis/sync_withloose/root_aux/' + fname)
tree_data = file_data.Get('kNNTrainingTree')

#training_vars = ['lepton_pt', 'lepton_kNN_jetpt', 'lepton_eta', 'evt_njet']
training_vars = ['lepton_pt', 'lepton_kNN_jetpt', 'evt_njet']


basic_selection = '' # '(lepton_njet>0. && lepton_jetpt>0.) &&'
signal_selection = basic_selection + '(lepton_iso && lepton_id)'
background_selection = basic_selection + '(!lepton_iso || !lepton_id)'

num_pass = tree_data.GetEntries(signal_selection)
num_fail = tree_data.GetEntries(background_selection)

outFile = ROOT.TFile('TMVA.root', 'recreate')

factory    = ROOT.TMVA.Factory(
    "TMVAClassification", 
    outFile, 
    "!V:!Silent:Color:DrawProgressBar:Transformations=I" ) 

for var in training_vars:
    # add float variable
    factory.AddVariable(var, 'F') 

if process=='data':
    factory.SetWeightExpression('evt_weight*evt_isMCw')
else:
    factory.SetWeightExpression('evt_weight')

factory.SetInputTrees(tree_data, ROOT.TCut(signal_selection), ROOT.TCut(background_selection))
factory.PrepareTrainingAndTestTree( ROOT.TCut(''), ROOT.TCut(''),
                                    "nTrain_Signal={num_pass}:nTrain_Background={num_fail}:SplitMode=Random:NormMode=None:!V" )

#factory.BookMethod( 
#    ROOT.TMVA.Types.kKNN, "KNN", 
#    "H:nkNN={nNeighbours}:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T".format(nNeighbours=nNeighbours))

factory.BookMethod( 
    ROOT.TMVA.Types.kKNN, "KNN50", 
    "H:nkNN=50:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T")

#factory.BookMethod( 
#    ROOT.TMVA.Types.kKNN, "KNN25", 
#    "H:nkNN=25:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T")

factory.TrainAllMethods()

import os
os.system('cp /afs/cern.ch/work/y/ytakahas/VH_analysis/CMGTools/CMSSW_5_3_9/src/CMGTools/H2TauTau/WH_analysis/sync_withloose/root_aux/' + fname +' data/Wjet_' + lname + '_training_' + process + '_knn.root')

import NtupleTMVAEvaluate
n = NtupleTMVAEvaluate.NtupleTMVAEvaluate('data/Wjet_' + lname + '_training_' + process + '_knn.root')

#n.addMVAMethod('KNN', 'kNNOutput', 'weights/TMVAClassification_KNN.weights.xml')
n.addMVAMethod('KNN50', 'kNN50Output', 'weights/TMVAClassification_KNN50.weights.xml')
#n.addMVAMethod('KNN25', 'kNN25Output', 'weights/TMVAClassification_KNN25.weights.xml')
n.setVariables(training_vars)
n.process()


#os.system('mv weights/TMVAClassification_KNN.weights.xml weights/KNN_' + process + '_' + lname + '_100.xml')
os.system('mv weights/TMVAClassification_KNN50.weights.xml weights/KNN_' + process + '_' + lname + '_50.xml')
#os.system('mv weights/TMVAClassification_KNN25.weights.xml weights/KNN_' + process + '_' + lname + '_25.xml')
