from ROOT import TColor,kViolet, kMagenta, kOrange, kRed, kBlue, kGray, kBlack
from ROOT import TLine, TLegend, TCanvas, TH1F, TLatex, TLorentzVector, Double
from ROOT import TMatrixD, TVectorD
from CMGTools.RootTools.utils.DeltaR import *

import math
import copy, subprocess, shelve

lum = 19700
col_qcd = TColor.GetColor(250,202,255)
col_tt  = TColor.GetColor(155,152,204)
col_ttv  = TColor.GetColor(155,182,204)
col_ewk = TColor.GetColor(222,90,106)
col_zll = TColor.GetColor(100,182,232)
col_red = TColor.GetColor(248,206,104)

filedict_mmt = {'WZ'  :['WZ','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/WZJetsTo3LNu/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 1.058*lum/2017979.,0],
            'ZZ'  :['ZZ','/afs/cern.ch/work/y/ytakahas/th_analysis/CMSSW_5_3_14_patch2/src/CMGTools/H2TauTau/th_analysis/MuMuTau/mmt_20141001/ZZJetsTo4L/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 0.181*lum/4807893.,1],
            'WW'  :['WW','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/WWJetsTo2L2Nu/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 5.824*lum/1933235.,2],
            'tt2l':['tt2l','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/TTJetsFullLept/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 25.144*lum/12011428.,3],
            'tt1l':['tt1l','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/TTJetsSemiLept/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 104.921*lum/24953451.,4],
            'tt0l':['tt0l','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/TTJetsHadronic/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 109.455*lum/31223821.,5],
            'DY' : ['DY','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/DYJets/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 3503.71*lum/30459503., 6],
            'DY1' :['DY1','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/DY1Jets/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 561*lum/24045248., 7 ],
            'DY2' :['DY2','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/DY2Jets/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 181*lum/21852156., 8 ],
            'DY3' :['DY3','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/DY3Jets/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 51.1*lum/11015445.0, 9],
            'DY4' :['DY4','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/DY4Jets/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 23.04*lum/6402827.0, 10],
            'Wjet' :['Wjet','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/WJets/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 36257.2*lum/18393090.0, 11],
            'W1jet' :['W1jet','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/W1Jets/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 6440.4*lum/23141598.0, 12],
            'W2jet' :['W2jet','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/W2Jets/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 2087.2*lum/34044921.0, 13],
            'W3jet' :['W3jet','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/W3Jets/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 619.0*lum/15539503.0, 14],
            'W4jet' :['W4jet','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/W4Jets/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root', 255.2*lum/13331527.9, 15],
            'tW':['tW','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/T_tW/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  11.1*lum/497658.0, 18],
            'tbW':['tbW','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/Tbar_tW/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  11.1*lum/493460.0, 19],
            't_tchan':['t_tchan','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/T_tchan/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  47.0*lum/3758227.0, 20],
            'tbar_tchan':['tbar_tchan','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/Tbar_tchan/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  25*lum/1935072.0, 21],
            'tH_Yt1':['tH_Yt1','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/tH/tH_mmt_20131220/tH_Yt1/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  0.00036776*lum/97986, 22],
            #            'tH_YtMinus1':['tH_YtMinus1','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/tH/tH_mmt_20131227/tH_YtMinus1/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  0.00473*lum/118986, 23],
#            'tH_YtMinus1':['tH_YtMinus1','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/tH/tH_mmt_20131227_old/tH_YtMinus1/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  0.00473*lum/118986, 23],
#            'tH_YtMinus1':['tH_YtMinus1','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/tH/tH_20140608/tH_YtMinus1/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  0.0211*lum/968025, 23],
            'tH_YtMinus1':['tH_YtMinus1','/afs/cern.ch/work/y/ytakahas/th_analysis/CMSSW_5_3_14_patch2/src/CMGTools/H2TauTau/th_analysis/MuMuTau/mmt_20141001/tH_YtMinus1/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  0.0211*lum/968025, 23],
#            'tH_YtMinus1':['tH_YtMinus1','/afs/cern.ch/work/m/manzoni/public/tH_ntuple/newTauID2/signal/tH_YtMinus1/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  0.0211*lum/968025, 23],
            
#            'tH_YtMinus1':['tH_YtMinus1','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/tH/tH_mmt_20131227/tH_YtMinus1/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  0.00473*lum/968025, 23],            
            'TTW':['TTW','/afs/cern.ch/work/y/ytakahas/th_analysis/CMSSW_5_3_14_patch2/src/CMGTools/H2TauTau/th_analysis/MuMuTau/mmt_20141001/TTW/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  0.249*lum/196046, 24],
            'TTZ':['TTZ','/afs/cern.ch/work/y/ytakahas/th_analysis/CMSSW_5_3_14_patch2/src/CMGTools/H2TauTau/th_analysis/MuMuTau/mmt_20141001/TTZ/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  0.208*lum/210160, 25],
            'TTH':['TTH','/afs/cern.ch/work/y/ytakahas/th_analysis/CMSSW_5_3_14_patch2/src/CMGTools/H2TauTau/th_analysis/MuMuTau/mmt_20141001/HiggsTTH125/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  0.1302*lum/871234, 26],
#            'WH':['WH','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140801_WH_notrig/HiggsVH125/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  0.07*lum/27650, 27],
            'WH':['WH','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/HiggsVH125/H2TauTauTreeProducerMMT/H2TauTauTreeProducerMMT_tree.root',  0.07*lum/27650, 27],
            'data':['data','/afs/cern.ch/user/y/ytakahas/work/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/MuMuTau/process/mmt_20140929/H2TauTauTreeProducerMMT_tree.root',1,100]}



filedict_emt = {'WZ'  :['WZ','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/WZJetsTo3LNu/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 1.058*lum/2017979.,0],
            'ZZ'  :['ZZ','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/ZZJetsTo4L/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 0.181*lum/4807893.,1],
            'WW'  :['WW','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/WWJetsTo2L2Nu/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 5.824*lum/1933235.,2],
            'tt2l':['tt2l','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/TTJetsFullLept/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 25.144*lum/12011428.,3],
            'tt1l':['tt1l','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/TTJetsSemiLept/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 104.921*lum/24953451.,4],
            'tt0l':['tt0l','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/TTJetsHadronic/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 109.455*lum/31223821.,5],
            'DY' : ['DY','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/DYJets/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 3503.71*lum/30459503., 6],
            'DY1' :['DY1','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/DY1Jets/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 561*lum/24045248., 7 ],
            'DY2' :['DY2','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/DY2Jets/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 181*lum/21852156., 8 ],
            'DY3' :['DY3','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/DY3Jets/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 51.1*lum/11015445.0, 9],
            'DY4' :['DY4','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/DY4Jets/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 23.04*lum/6402827.0, 10],
            'Wjet' :['Wjet','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/WJets/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 36257.2*lum/18393090.0, 11],
            'W1jet' :['W1jet','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/W1Jets/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 6440.4*lum/23141598.0, 12],
            'W2jet' :['W2jet','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/W2Jets/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 2087.2*lum/34044921.0, 13],
            'W3jet' :['W3jet','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/W3Jets/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 619.0*lum/15539503.0, 14],
            'W4jet' :['W4jet','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/W4Jets/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root', 255.2*lum/13331527.9, 15],
            'tW':['tW','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/WH_analysis/process/WH_em_skim_MC/T_tW/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  11.1*lum/497658.0, 18],
            'tbW':['tbW','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/WH_analysis/process/WH_em_skim_MC/Tbar_tW/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  11.1*lum/493460.0, 19],
            't_tchan':['t_tchan','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/WH_analysis/process/WH_em_skim_MC/T_tchan/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  47.0*lum/3758227.0, 20],
            'tbar_tchan':['tbar_tchan','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/WH_analysis/process/WH_em_skim_MC/Tbar_tchan/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  25*lum/1935072.0, 21],
            'tH_Yt1':['tH_Yt1','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/tH/tH_emt_20131220/tH_Yt1/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  0.00036776*lum/97986, 22],
            #            'tH_YtMinus1':['tH_YtMinus1','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/tH/tH_emt_20131227/tH_YtMinus1/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  0.00473*lum/118986, 23],
#            'tH_YtMinus1':['tH_YtMinus1','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/tH/tH_emt_20131227_old/tH_YtMinus1/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  0.00473*lum/118986, 23],
#            'tH_YtMinus1':['tH_YtMinus1','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/tH/tH_20140608/tH_YtMinus1/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  0.0211*lum/968025, 23],
            'tH_YtMinus1':['tH_YtMinus1','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/tH/tH_20140811/tH_YtMinus1/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  0.0211*lum/968025, 23],
#            'tH_YtMinus1':['tH_YtMinus1','/afs/cern.ch/work/m/manzoni/public/tH_ntuple/newTauID2/signal/tH_YtMinus1/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  0.0211*lum/968025, 23],
            
#            'tH_YtMinus1':['tH_YtMinus1','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/tH/tH_emt_20131227/tH_YtMinus1/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  0.00473*lum/968025, 23],            
            'TTW':['TTW','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/TTW/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  0.249*lum/196046, 24],
            'TTZ':['TTZ','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/TTZ/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  0.208*lum/210160, 25],
            'TTH':['TTH','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/HiggsTTH125/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  0.1302*lum/871234, 26],
#            'WH':['WH','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140801_WH_notrig/HiggsVH125/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  0.07*lum/27650, 27],
            'WH':['WH','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140801_WH/HiggsVH125/H2TauTauTreeProducerEMT2/H2TauTauTreeProducerEMT2_tree.root',  0.07*lum/27650, 27],
            'data':['data','/afs/cern.ch/work/y/ytakahas/htautau_2014/CMSSW_5_3_14/src/CMGTools/H2TauTau/EMuTau/process/emt_20140811/data/H2TauTauTreeProducerEMT2_tree.root',1,100]}


ldict = {'submass_x':'M_{l_{2}#tau} [GeV]',
#         'submass_y':'dN/dM_{l_{2}#tau} [20/GeV]',
         'submass_y':'Events / 20 [GeV/c^{2}]',
         'mupt_x':'p_{T, #mu} [GeV]',
         'mupt_y':'dN/dp_{T, #mu} [1/GeV]',
         'ept_x':'p_{T, e} [GeV]',
         'ept_y':'dN/dp_{T, e} [1/GeV]',
         'taupt_x':'p_{T, #tau} [GeV]',
         'taupt_y':'dN/dp_{T, #tau} [1/GeV]',
         'tauiso_x':'dB isolation [GeV]',
         'tauiso_y':'Entries [1/GeV]',
         'mueta_x':'#eta_{#mu}',
         'mueta_y':'dN/d#eta_{#mu}',
         'eeta_x':'#eta_{e}',
         'eeta_y':'dN/d#eta_{e}',
         'taueta_x':'#eta_{#tau}',
         'taueta_y':'dN/d#eta_{#tau}',
         }



class ReadFile:

    def __init__(self, plist, channel):
        self.file = None

        if channel == 'mmt':
            print '[INFO] file list chosen from mmt channel'
            self.file = filedict_mmt
        elif channel == 'emt':
            print '[INFO] file list chosen from emt channel'
            self.file = filedict_emt
        else:
            print 'Undifined files ! specify mmt or emt'
        self.flist = []
        
        for i, j in sorted(self.file.items()):
            pass
#            print '[INFO] process=', j[0], 'file = ', j[1], 'Xsec = ', j[2]

        for ilist in plist:
            if self.file.has_key(ilist)==False:
                print '[WARNING] no dictionary for process = ', ilist
            else:
                self.flist.append(self.file[ilist])

    def returnFile(self):
        return self.flist

    def returnPid(self, key):
        if filedict.has_key(key)==False:
            print '[WARNING] no dictionary for process', key
            return -999
        else:
            tmp = self.file[key]
            return tmp[3]



### Classes
class mobj:

    def __init__(self, pt, eta, phi, mass, jetpt, njet, charge, trigmatch, trig_weight, id_weight, isid, isiso, reliso, MT, dxy, dz, dB3D, csv, csv_10, mva, mva_ch, mva_neu, mva_jet_dr, mva_ptratio, mva_csv, new_mva, flag=False):
        self.pt = pt
        self.eta = eta
        self.phi = phi
        self.mass = mass
        self.jetpt = jetpt
        self.njet = njet
        self.charge = charge
        self.trigmatch = trigmatch
        self.trig = trig_weight
        self.id = id_weight
        self.isid = isid
        self.isiso = isiso
        self.reliso = reliso
        self.MT = MT
        self.dxy = dxy
        self.dz = dz
        self.dB3D = dB3D
        self.csv = csv
        self.csv_10 = csv_10
        self.mva = mva
        self.mva_ch_iso = mva_ch
        self.mva_neu_iso = mva_neu
        self.mva_jet_dr = mva_jet_dr
        self.mva_ptratio = mva_ptratio
        self.mva_csv = mva_csv
        self.new_mva = new_mva
        self.flag = flag
        tmp = TLorentzVector()
        tmp.SetPtEtaPhiM(pt, eta, phi, mass)
        self.p = tmp.P()
        self.vector = tmp

    def returnVector(self):
        return self.vector
    
    def returndR(self, obj1):
        deta = obj1.eta - self.eta
#        dphi = obj1.phi - self.phi
        dphi = deltaPhi(obj1.phi, self.phi)
        
        dr = deta*deta + dphi*dphi
        return math.sqrt(dr)



class eobj:

    def __init__(self, pt, eta, phi, mass, jetpt, njet, charge, trigmatch, trig_weight, id_weight, isid, isiso, reliso, MT, dxy, dz, dB3D, csv, csv_10, mva, mva_ch, mva_neu, mva_jet_dr, mva_ptratio, mva_csv, mva_score, mva_nhit, new_mva):
        self.pt = pt
        self.eta = eta
        self.phi = phi
        self.mass = mass
        self.jetpt = jetpt
        self.njet = njet
        self.charge = charge
        self.trigmatch = trigmatch
        self.trig = trig_weight
        self.id = id_weight
        self.isid = isid
        self.isiso = isiso
        self.reliso = reliso
        self.MT = MT
        self.dxy = dxy
        self.dz = dz
        self.dB3D = dB3D
        self.csv = csv
        self.csv_10 = csv_10
        self.mva = mva
        self.mva_ch_iso = mva_ch
        self.mva_neu_iso = mva_neu
        self.mva_jet_dr = mva_jet_dr
        self.mva_ptratio = mva_ptratio
        self.mva_csv = mva_csv
        self.mva_score = mva_score
        self.mva_nhit = mva_nhit
        self.new_mva = new_mva
                
        tmp = TLorentzVector()
        tmp.SetPtEtaPhiM(pt, eta, phi, mass)
        self.p = tmp.P()
        self.vector = tmp

    def returnVector(self):
        return self.vector
    
    def returndR(self, obj1):
        deta = obj1.eta - self.eta
#        dphi = obj1.phi - self.phi
        dphi = deltaPhi(obj1.phi, self.phi)        
        dr = deta*deta + dphi*dphi
        return math.sqrt(dr)


class jetobj:

    def __init__(self, pt, eta, phi, mass, mva):
        self.pt = pt
        self.eta = eta
        self.phi = phi
        self.mass = mass
        self.mva = mva

        tmp = TLorentzVector()
        tmp.SetPtEtaPhiM(pt, eta, phi, mass)
        self.p = tmp.P()
        self.vector = tmp

    def returnVector(self):
        return self.vector
        
    def returndR(self, obj1):
        deta = obj1.eta - self.eta
        dphi = deltaPhi(obj1.phi, self.phi)
#        dphi = obj1.phi - self.phi
        
        dr = deta*deta + dphi*dphi
        return math.sqrt(dr)

    def returnmindR(self, obj1):

        rflag = False
        min_dr = 100
        
        for iobj1 in obj1:
            deta = iobj1.eta - self.eta
            dphi = deltaPhi(iobj1.phi, self.phi)
#            dphi = iobj1.phi - self.phi

        
            dr = deta*deta + dphi*dphi
            if math.sqrt(dr) < min_dr:
                min_dr = math.sqrt(dr)
            
#        print 'min_dR = ', min_dr
        return min_dr

class easyobj:

    def __init__(self, pt, eta, phi):
        self.pt = pt
        self.eta = eta
        self.phi = phi

    def returndR(self, obj1):
        deta = obj1.eta - self.eta
        dphi = deltaPhi(obj1.phi, self.phi)
#        dphi = obj1.phi - self.phi
        
        dr = deta*deta + dphi*dphi
        return math.sqrt(dr)


    def returnmindR(self, obj1):

        rflag = False
        min_dr = 100
        
        for iobj1 in obj1:
            deta = iobj1.eta - self.eta
#            dphi = iobj1.phi - self.phi
            dphi = deltaPhi(iobj1.phi, self.phi)
            
            dr = deta*deta + dphi*dphi
            if math.sqrt(dr) < min_dr:
                min_dr = math.sqrt(dr)
            
#        print 'min_dR = ', min_dr
        return min_dr


class easyobj_bjet:

    def __init__(self, pt, eta, phi, mva):
        self.pt = pt
        self.eta = eta
        self.phi = phi
        self.mva = mva

    def returndR(self, obj1):
        deta = obj1.eta - self.eta
        dphi = deltaPhi(obj1.phi, self.phi)
#        dphi = obj1.phi - self.phi
        
        dr = deta*deta + dphi*dphi
        return math.sqrt(dr)


    def returnmindR(self, obj1):

        rflag = False
        min_dr = 100
        
        for iobj1 in obj1:
            deta = iobj1.eta - self.eta
#            dphi = iobj1.phi - self.phi
            dphi = deltaPhi(iobj1.phi, self.phi)
            
            dr = deta*deta + dphi*dphi
            if math.sqrt(dr) < min_dr:
                min_dr = math.sqrt(dr)
            
#        print 'min_dR = ', min_dr
        return min_dr


class easyobj_gen:

    def __init__(self, pt, eta, phi, pdgid):
        self.pt = pt
        self.eta = eta
        self.phi = phi
        self.pdgid = pdgid

    def returndR(self, obj1):
        deta = obj1.eta - self.eta
        dphi = deltaPhi(obj1.phi, self.phi)
#        dphi = obj1.phi - self.phi
        
        dr = deta*deta + dphi*dphi
        return math.sqrt(dr)


    def returnmindR(self, obj1):

        rflag = False
        min_dr = 100
        
        for iobj1 in obj1:
            deta = iobj1.eta - self.eta
#            dphi = iobj1.phi - self.phi
            dphi = deltaPhi(iobj1.phi, self.phi)
            
            dr = deta*deta + dphi*dphi
            if math.sqrt(dr) < min_dr:
                min_dr = math.sqrt(dr)
            
        return min_dr



class tauobj:

    def __init__(self, pt, eta, phi, mass, charge, reliso, againstMuTight, againstEMedium, decaymode, ep, MT, dxy, dz, dB3D):
        self.pt = pt
        self.eta = eta
        self.phi = phi
        self.mass = mass
        self.charge = charge
        self.reliso = reliso
        self.againstMuTight = againstMuTight
        self.againstEMedium = againstEMedium
        self.decaymode = decaymode
        self.ep = ep
        self.MT = MT
        self.dxy = dxy
        self.dz = dz
        self.dB3D = dB3D

        tmp = TLorentzVector()
        tmp.SetPtEtaPhiM(pt, eta, phi, mass)
        self.p = tmp.P()
        self.vector = tmp
        
    def returndR(self, obj1):
        deta = obj1.eta - self.eta
        dphi = deltaPhi(obj1.phi, self.phi)
#        dphi = obj1.phi - self.phi
        
        dr = deta*deta + dphi*dphi
        return math.sqrt(dr)

    def returnVector(self):
        return self.vector

    def returnmindR(self, obj1):

        rflag = False
        min_dr = 100
        
        for iobj1 in obj1:
            deta = iobj1.eta - self.eta
#            dphi = iobj1.phi - self.phi
            dphi = deltaPhi(iobj1.phi, self.phi)

            dr = deta*deta + dphi*dphi
            if math.sqrt(dr) < min_dr:
                min_dr = math.sqrt(dr)
            
#        print 'min_dR = ', min_dr
        return min_dr



class diobj:
    
    def __init__(self, obj1, obj2):
        
        self.lep4 = TLorentzVector()
        self.tau4 = TLorentzVector()
        
        self.lep4.SetPtEtaPhiM(Double(obj1.pt),
                               Double(obj1.eta),
                               Double(obj1.phi),
                               Double(obj1.mass))
        
        self.tau4.SetPtEtaPhiM(Double(obj2.pt),
                               Double(obj2.eta),
                               Double(obj2.phi),
                               Double(obj2.mass))

    
    def returnmass(self):
        return (self.lep4 + self.tau4).M()
        

    def returndR(self, obj1):

        selfeta = (self.lep4 + self.tau4).Eta()
        selfphi = (self.lep4 + self.tau4).Phi()

        deta = obj1.eta - selfeta
#        dphi = obj1.phi - selfphi
        dphi = deltaPhi(obj1.phi, self.phi)
        
        dr = deta*deta + dphi*dphi
        return math.sqrt(dr)


    def returnOpendR(self):

        selfeta = (self.lep4 + self.tau4).Eta()
        selfphi = (self.lep4 + self.tau4).Phi()

        deta = self.lep4.Eta() - self.tau4.Eta()
#        dphi = self.lep4.Phi() - self.tau4.Phi()
        dphi = deltaPhi(self.lep4.Phi(), self.tau4.Phi())
        
        dr = deta*deta + dphi*dphi
        return math.sqrt(dr)


    



def returnDict(mass, process, sys):
    table = 0

    dictname = 'result_' + str(mass) + '/sys_' + process + '_' + sys + '.shelve'
    dict = shelve.open(dictname)
    table = dict['dict']
    dict.close()

    if table==0:
        print 'No dictionary found'

    return table


def returnchannelname(channel):

    _chan_ = ''

    if(channel=='eemm'):
        _chan_ = channel.replace('eemm','$ee, \\mu\\mu$')
    elif(channel=='tautau'):
        _chan_ = channel.replace('tautau','$\\tau\\tau$')
    elif(channel=='emu'):
        _chan_ = channel.replace('emu','e$\\mu$')
    elif(channel=='etau'):
        _chan_ = channel.replace('etau','e$\\tau$')
    elif(channel=='mutau'):
        _chan_ = channel.replace('mutau','$\\mu\\tau$')

    return _chan_

#def NormalizedToBinWidth(h):
##    print h.GetName(), h.GetSumOfWeights()
#    for i in range(1, h.GetNbinsX()+1):
#        h.SetBinContent(i, h.GetBinContent(i) / h.GetBinWidth(i))
#        h.SetBinError(i, h.GetBinError(i) / h.GetBinWidth(i))

def noerr(h):
#    h.SetMarkerSize(0)

    for ibin in range(1,h.GetXaxis().GetNbins()+1):
        h.SetBinError(ibin,0)


def returnTopWeight(pname, top_pt, atop_pt):

    _weight_top_ = 1.
    _weight_atop_ = 1.

    if pname == 'tt0l':
        _weight_top_  = math.exp(0.156-0.00137*top_pt)
        _weight_atop_ = math.exp(0.156-0.00137*atop_pt)
        
    if pname == 'tt1l':
        _weight_top_  = math.exp(0.159-0.00141*top_pt)
        _weight_atop_ = math.exp(0.159-0.00141*atop_pt)

    if pname == 'tt2l':
        _weight_top_  = math.exp(0.148-0.00129*top_pt)
        _weight_atop_ = math.exp(0.148-0.00129*atop_pt)

    if pname == 'tt0l' or pname == 'tt1l' or pname == 'tt2l':
        if top_pt > 400:
            _weight_top_ = 1.
        if atop_pt > 400:
            _weight_atop_ = 1.

    top_weight = math.sqrt(_weight_top_*_weight_atop_)
    return top_weight




def calculateSphericity(particles):
    momentumTensor = TMatrixD(3, 3)
    p2_sum = 0.

    for iparticle in particles:
        px = iparticle.Px()
        py = iparticle.Py()
        pz = iparticle.Pz()

        momentumTensor[0][0] += px * px
        momentumTensor[0][1] += px * py
        momentumTensor[0][2] += px * pz
        momentumTensor[1][0] += py * px
        momentumTensor[1][1] += py * py
        momentumTensor[1][2] += py * pz
        momentumTensor[2][0] += pz * px
        momentumTensor[2][1] += pz * py
        momentumTensor[2][2] += pz * pz
        
        p2_sum += (px * px + py * py + pz * pz)


#    print 'before momentumTensor'
#    momentumTensor.Print()

    if p2_sum != 0.:
        for i in range(3):
            for j in range(3):
                momentumTensor[i][j] = momentumTensor[i][j] / p2_sum

#    print 'after momentumTensor by dividing ', p2_sum
#    momentumTensor.Print()

    ev = TVectorD(3)
    momentumTensor.EigenVectors(ev);

    #some checks & limited precision of TVectorD

    ev0 = abs(ev[0])
    ev1 = abs(ev[1])
    ev2 = abs(ev[2])

    if ev0 < 0.000000000000001:
        ev0 = 0.
    if ev1 < 0.000000000000001:
        ev1 = 0.
    if ev2 < 0.000000000000001:
        ev2 = 0.
    
    if ((ev0 < ev1) or (ev1 < ev2)):
        print 'Calculating eigenvectors failed.'
        return -1
    
    return 3*ev2/2., 3*(ev1+ev2)/2.


def returnlabel(channel):
    
    _chan_ = ''
    
    if(channel=='eemm'):
        _chan_ = channel.replace('eemm','ee, #mu#mu')
    elif(channel=='tautau'):
        _chan_ = channel.replace('tautau','#tau#tau')
    elif(channel=='emu'):
        _chan_ = channel.replace('emu','e#mu')
    elif(channel=='etau'):
        _chan_ = channel.replace('etau','e#tau')
    elif(channel=='mutau'):
        _chan_ = channel.replace('mutau','#mu#tau')

    return _chan_


def returnChannel(decay):
    if decay in [0]:
        return 0
    elif decay in [1,2]:
        return 1
    elif decay in [3,4]:
        return 2
    elif decay in [5,7]:
        return 3
    elif decay in [6,8]:
        return 4
    else:
        print 'Invalid decaymode'
        return -1
    
def ratioFactory(h1,h2):
    _h_ = copy.deepcopy(h1)
#    _h_.Sumw2()
    _h_.Divide(h2)

    return _h_


def legendFactory(x1,y1,x2,y2):

    _leg_ = TLegend(x1,y1,x2,y2)

    return _leg_

def texFactory(x,y,name):

    _tex_ = TLatex(x, y, name)

    return _tex_

def frameFactory(hname, xmax, ymax):

    _frame_ = TH1F(hname, hname, xmax,0,xmax)

    return _frame_

def lineFactory(x_min, y_min, x_max, y_max):

    _line_ = TLine(x_min, y_min, x_max, y_max)
    return _line_

def returnfname(title, base):
    fname = 'figure_' + title + '/' + base + '.gif'
    return fname


def directory(title):
    dname = 'figure_' + title
    cmd = 'mkdir '+dname+' 2>/dev/null'
    subprocess.call(cmd, shell=True)


def DecoHist(name, h, xtitle, ytitle):
#    h.GetXaxis().SetTitle('M_{l_{2}#tau} [GeV]')
#    h.GetYaxis().SetTitle('dN/dM_{l_{2}#tau} [1/GeV]')
    h.GetXaxis().SetTitle(xtitle)
    h.GetYaxis().SetTitle(ytitle)
    h.GetXaxis().SetTitleSize(0.05)
    h.GetYaxis().SetTitleSize(0.05)
        
    h.SetLineColor(hist_dict[name]['lcolor'])
    if name=='data':
        h.SetMarkerStyle(20)
        h.SetFillStyle(0)
        h.SetMarkerSize(1.5)
#        h.SetLineWidth(3)

    h.SetFillColor(hist_dict[name]['color'])
    h.SetLineStyle(hist_dict[name]['lstyle'])

#    print 'lcolor = ', hist_dict[name]['lcolor'], 'col = ', hist_dict[name]['color'], 'lstyle = ', hist_dict[name]['lstyle']
    h.SetLineWidth(2)

#    return h

#def DecoHist(hist, lcolor, mcolor):
#    hist.SetLineWidth(2)
#    hist.SetLineColor(lcolor)
#    hist.SetMarkerColor(mcolor)
##    hist.GetXaxis().SetTitle(xtitle)
#    hist.SetFillColor(2)
#    hist.SetFillStyle(0)
#    hist.SetLineStyle(0)
#    hist.SetLineWidth(2)
#    hist.SetMarkerStyle(20)
#    hist.SetMarkerSize(1.)
#    hist.GetYaxis().SetTitle("Events")
#    hist.GetXaxis().SetNdivisions(505)
#    hist.GetXaxis().SetLabelFont(42)
#    hist.GetXaxis().SetLabelSize(0.05)
#    hist.GetXaxis().SetTitleSize(0.055)
#    hist.GetXaxis().SetTitleOffset(1.2)
#    hist.GetXaxis().SetTitleFont(42)
#    hist.GetYaxis().SetLabelFont(42)
#    hist.GetYaxis().SetLabelOffset(0.01)
#    hist.GetYaxis().SetLabelSize(0.05)
#    hist.GetYaxis().SetTitleSize(0.055)
#    hist.GetYaxis().SetTitleOffset(1.4)
#    hist.GetYaxis().SetTitleFont(42)

def CanvasSetting(canvas):
    canvas.SetHighLightColor(2)
    canvas.Range(0,0,1,1)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetBorderSize(10)
    canvas.SetTickx(1)
    canvas.SetTicky(1)
    canvas.SetLeftMargin(0.15)
    canvas.SetRightMargin(0.05)
    canvas.SetTopMargin(0.08)
    canvas.SetBottomMargin(0.13)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameLineStyle(0)
    canvas.SetFrameLineWidth(2)
    canvas.SetFrameBorderMode(0)
    canvas.SetFrameBorderSize(10)
    
def PadSetting(pad):
    pad.SetFillColor(0)
    pad.SetBorderMode(0)
    pad.SetBorderSize(10)
    pad.SetTickx(1)
    pad.SetTicky(1)
    pad.SetFrameFillStyle(0)
    pad.SetFrameLineStyle(0)
    pad.SetFrameLineWidth(2)
    pad.SetFrameBorderMode(0)
    pad.SetFrameBorderSize(10)
    pad.SetFrameFillStyle(0)
    pad.SetFrameLineStyle(0)
    pad.SetFrameLineWidth(2)
    pad.SetFrameBorderMode(0)
    pad.SetFrameBorderSize(10)


def DecoRatioHist(hist, xtitle):
#    hist.SetMinimum(0.9)
#    hist.SetMaximum(1.1)
    hist.SetFillColor(2)
    hist.SetFillStyle(0)
    hist.SetLineStyle(0)
    hist.SetLineColor(1)
    hist.SetMarkerColor(1)
    hist.SetLineWidth(2)
    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(1.)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetXaxis().SetNdivisions(505)
    hist.GetXaxis().SetLabelFont(42)
    hist.GetXaxis().SetLabelSize(0.12)
    hist.GetXaxis().SetTitleSize(0.14)
    hist.GetXaxis().SetTitleOffset(1.23)
    hist.GetXaxis().SetTitleFont(42)
    hist.GetYaxis().SetNdivisions(503)
    hist.GetYaxis().SetLabelFont(42)
    hist.GetYaxis().SetLabelOffset(0.01)
    hist.GetYaxis().SetLabelSize(0.13)
    hist.GetYaxis().SetTitleSize(0.07)
    hist.GetYaxis().SetTitleOffset(1.6)
    hist.GetYaxis().SetTitleFont(42)


def LegendSettings(leg):
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.04)
    leg.SetTextFont(42)



hist_dict ={
    'QCD' : {'hid':0, 'color': kMagenta-10, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':0},
    'ZTT' : {'hid':1,'color': kOrange-2, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':3},
    'ZL' : {'hid':2,'color': kRed+2, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':1},
    'ZJ' : {'hid':3,'color': kRed+2, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':1},
    'VV' : {'hid':4,'color': kRed+2, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':1},
    'WZ_ZZ' : {'hid':4,'color': kRed+2, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':1},
    'DY' : {'hid':4,'color': kOrange-2, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':1},
    'WZ' : {'hid':4,'color': col_zll, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':1},
    'ZZ' : {'hid':4,'color': col_zll, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':1},
    'W' : {'hid':5,'color': kRed+2, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':1},
    'Wjet' : {'hid':5,'color': kRed+2, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':1},
    'tt' : {'hid':6,'color': col_tt, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':2},
    'TT' : {'hid':6,'color': col_tt, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':2},
    'TTW' : {'hid':6,'color': col_ttv, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':2},
    'TTZ' : {'hid':6,'color': col_ttv, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':2},
    'Reducible' : {'hid':6,'color': kOrange-2, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':2},
    'tt0l' : {'hid':6,'color': col_tt, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':2},
    'tt1l' : {'hid':6,'color': col_tt, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':2},
    'tt2l' : {'hid':6,'color': col_tt, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':2},
    'tH_Yt1' : {'hid':6,'color': kBlue, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':1001},
    'tH_YtMinus1' : {'hid':6,'color': kRed, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':1001},
    'TTH' : {'hid':6,'color': kMagenta, 'fill':1, 'lstyle':1, 'lcolor':1, 'layer':1001},
    'VH' : {'hid':7, 'color':kBlue, 'fill':-1, 'lstyle':2, 'lcolor':kBlue, 'layer':1001},
    'ggH' : {'hid':8,'color': kBlue, 'fill':-1, 'lstyle':2, 'lcolor':kBlue, 'layer':1001},
    'qqH' : {'hid':9,'color': kBlue, 'fill':-1, 'lstyle':2, 'lcolor':kBlue, 'layer':1001},
    'data' : {'hid':10, 'color':kBlack, 'fill':0, 'lstyle':1, 'lcolor':1, 'layer':2999}
    }
