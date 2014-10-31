import os
import ROOT
from CMGTools.RootTools.utils.DeltaR import deltaR,deltaPhi

#if "/smearer_cc.so" not in ROOT.gSystem.GetLibraries(): 
#    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/smearer.cc+" % os.environ['CMSSW_BASE']);
#if "/mcCorrections_cc.so" not in ROOT.gSystem.GetLibraries(): 
#    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/mcCorrections.cc+" % os.environ['CMSSW_BASE']);


ROOT.TMVA.Tools.Instance()
ntuple = ROOT.TFile("BDT_training_ss_f12.root")
tree = ntuple.Get("Tree")

fout = ROOT.TFile("test.root","RECREATE")
factory = ROOT.TMVA.Factory("TMVAClassification", fout,
                            ":".join(["!V",
                                      "!Silent",
                                      "Color",
                                      "DrawProgressBar",
                                      "Transformations=I;D;P;G,D",
                                      "AnalysisType=Classification"]
                                     ))

factory.SetWeightExpression('bdt_evt_weight')
factory.AddVariable("bdt_muon_dxy", "F")
factory.AddVariable("bdt_muon_dz", "F")
factory.AddVariable("bdt_muon_mva_ch_iso", "F")
factory.AddVariable("bdt_muon_mva_neu_iso", "F")
factory.AddVariable("bdt_muon_mva_jet_dr", "F")
factory.AddVariable("bdt_muon_mva_ptratio", "F")
factory.AddVariable("bdt_muon_mva_csv", "F")

factory.AddSignalTree(tree)
factory.AddBackgroundTree(tree)

# cuts defining the signal and background sample
sigCut = ROOT.TCut("bdt_evt_processid==16 && (abs(bdt_muon_pdg)==13 || abs(bdt_muon_pdg)==15)")
bgCut = ROOT.TCut("bdt_evt_processid>=4 && bdt_evt_processid<=5 && !(abs(bdt_muon_pdg)==13 || abs(bdt_muon_pdg)==15)")
#sigCut = ROOT.TCut("bdt_evt_processid==16 && (abs(bdt_muon_pdg)==13 || abs(bdt_muon_pdg)==15)")
#bgCut = ROOT.TCut("bdt_evt_processid==16 && !(abs(bdt_muon_pdg)==13 || abs(bdt_muon_pdg)==15)")

factory.PrepareTrainingAndTestTree(sigCut, bgCut, 
                                   ":".join(["nTrain_Signal=0",
                                             "nTrain_Background=0",
                                             "SplitMode=Random",
                                             "NormMode=NumEvents",
                                             "!V"
                                             ]))



method = factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT",
                            ":".join(["!H",
                                      "!V",
                                      "NTrees=850",
                                      "nEventsMin=150",
                                      "MaxDepth=3",
                                      "BoostType=AdaBoost",
                                      "AdaBoostBeta=0.5",
                                      "SeparationType=GiniIndex",
                                      "nCuts=20",
                                      "PruneMethod=NoPruning",
                                      ]))

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

os.system('mv weights/TMVAClassification_BDT.weights.xml weights/TMVAClassification_BDT_muon.weights.xml')
os.system('mv weights/TMVAClassification_BDT.class.C weights/TMVAClassification_BDT_muon.class.C')


###################


feout = ROOT.TFile("etest.root","RECREATE")
efactory = ROOT.TMVA.Factory("TMVAClassification", feout,
                             ":".join(["!V",
                                       "!Silent",
                                       "Color",
                                       "DrawProgressBar",
                                       "Transformations=I;D;P;G,D",
                                       "AnalysisType=Classification"]
                                      ))

efactory.SetWeightExpression('bdt_evt_weight')
efactory.AddVariable("bdt_electron_mva_score", "F")
#efactory.AddVariable("bdt_electron_mva_numberOfHits", "F")
efactory.AddVariable("bdt_electron_mva_ch_iso", "F")
efactory.AddVariable("bdt_electron_mva_neu_iso", "F")
efactory.AddVariable("bdt_electron_mva_jet_dr", "F")
efactory.AddVariable("bdt_electron_mva_ptratio", "F")
efactory.AddVariable("bdt_electron_mva_csv", "F")

efactory.AddSignalTree(tree)
efactory.AddBackgroundTree(tree)

# cuts defining the signal and background sample
esigCut = ROOT.TCut("bdt_evt_processid==16 && (abs(bdt_electron_pdg)==11 || abs(bdt_electron_pdg)==15)")
ebgCut = ROOT.TCut("bdt_evt_processid>=4 && bdt_evt_processid<=5 && !(abs(bdt_electron_pdg)==11 || abs(bdt_electron_pdg)==15)")

efactory.PrepareTrainingAndTestTree(esigCut, ebgCut, 
                                   ":".join(["nTrain_Signal=0",
                                             "nTrain_Background=0",
                                             "SplitMode=Random",
                                             "NormMode=NumEvents",
                                             "!V"
                                             ]))



emethod = efactory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT",
                              ":".join(["!H",
                                        "!V",
                                        "NTrees=850",
                                        "nEventsMin=150",
                                        "MaxDepth=3",
                                        "BoostType=AdaBoost",
                                        "AdaBoostBeta=0.5",
                                        "SeparationType=GiniIndex",
                                        "nCuts=20",
                                        "PruneMethod=NoPruning",
                                        ]))

efactory.TrainAllMethods()
efactory.TestAllMethods()
efactory.EvaluateAllMethods()


os.system('mv weights/TMVAClassification_BDT.weights.xml weights/TMVAClassification_BDT_electron.weights.xml')
os.system('mv weights/TMVAClassification_BDT.class.C weights/TMVAClassification_BDT_electron.class.C')
