import itertools, copy
from CMGTools.RootTools.fwlite.Config import printComps
from CMGTools.H2TauTau.proto.samples.connect import connect
from CMGTools.H2TauTau.proto.samples.splitFactor import splitFactor
from CMGTools.RootTools.json.jsonPick import jsonPick
from CMGTools.H2TauTau.officialJSONS import jsonMap

from CMGTools.H2TauTau.proto.samples.run2012.data import *
from CMGTools.H2TauTau.proto.samples.run2012.embed import *
from CMGTools.H2TauTau.proto.samples.run2012.ewk import *
#from CMGTools.H2TauTau.proto.samples.run2012.wgamma import *
from CMGTools.H2TauTau.proto.samples.run2012.diboson import *
from CMGTools.H2TauTau.proto.samples.run2012.tH import *
from CMGTools.H2TauTau.proto.samples.run2012.higgs import *
from CMGTools.H2TauTau.proto.samples.run2012.higgs_susy import *
from CMGTools.H2TauTau.proto.samples.run2012.triggers_mumuTau import data_triggers, mc_triggers, embed_triggers
#from CMGTools.H2TauTau.proto.samples.run2012.triggers_tauMu import data_triggers, mc_triggers, embed_triggers

aliases = {
    '/VBF_HToTauTau.*START53.*':'HiggsVBF',
    '/VBFHToTauTau.*START53.*':'HiggsVBF',
    '/GluGluToHToTauTau.*START53.*':'HiggsGGH',
    '/WH_ZH_TTH_HToTauTau.*START53.*':'HiggsVH',
    '/SUSYBB.*START53.*':'HiggsSUSYBB',
    '/SUSYGluGluTo.*START53.*':'HiggsSUSYGluGlu',
    '/DYJets.*START53.*':'DYJets',
    '/DY1JetsToLL_M-50_TuneZ2Star_8TeV-madgraph.*START53.*':'DY1Jets',
    '/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph.*START53.*':'DY2Jets',
    '/DY3JetsToLL_M-50_TuneZ2Star_8TeV-madgraph.*START53.*':'DY3Jets',
    '/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph.*START53.*':'DY4Jets',
    # '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START53_V9-v1.*':'WJets',
    '/WJets.*START53_V7.*':'WJets',
    '/W1Jets.*START53_V7.*':'W1Jets',
    '/W2Jets.*START53_V7.*':'W2Jets',
    '/W3Jets.*START53_V7.*':'W3Jets',
    '/W4Jets.*START53_V7.*':'W4Jets',
    '/W1Jets.*START53_V19.*':'W1Jets_ext',
    '/W2Jets.*START53_V19.*':'W2Jets_ext',
    '/W3Jets.*START53_V19.*':'W3Jets_ext',
    '/TTJets_MassiveBinDECAY_TuneZ2star_8TeV.*START53.*':'TTJets',
    '/TTJets_FullLeptMGDecays_8TeV.*START53.*':'TTJetsFullLept',
    '/TTJets_SemiLeptMGDecays_8TeV.*START53.*':'TTJetsSemiLept',
    '/TTJets_HadronicMGDecays_8TeV.*START53.*':'TTJetsHadronic',
    '/TTWJets_8TeV-madgraph.*START53.*':'TTW',
    '/TTZJets_8TeV-madgraph.*START53.*':'TTZ',
    '/TTH_Inclusive.*START53.*':'HiggsTTH',
    '/TauPlusX/Run2012A-22Jan2013-v1.*':'data_Run2012A',
    '/TauPlusX/Run2012B-22Jan2013-v1.*':'data_Run2012B',
    '/TauPlusX/Run2012C-22Jan2013-v1.*':'data_Run2012C',
    '/TauPlusX/Run2012D-22Jan2013-v1.*':'data_Run2012D',
    '/T_tW-channel.*START53.*':'T_tW',
    '/Tbar_tW-channel.*START53.*':'Tbar_tW',
    '/T_t-channel.*START53.*':'T_tchan',
    '/Tbar_t-channel.*START53.*':'Tbar_tchan',
    '/WWJetsTo2L2Nu.*START53.*':'WWJetsTo2L2Nu',
    '/WZJetsTo2L2Q.*START53.*':'WZJetsTo2L2Q',
    '/WZJetsTo3LNu.*START53.*':'WZJetsTo3LNu',
    '/WW_TuneZ2star.*START53.*':'WW',
    '/WZ_TuneZ2star.*START53.*':'WZ',
    '/ZZ_TuneZ2star.*START53.*':'ZZ',
    '/ZZJetsTo2L2Nu.*START53.*':'ZZJetsTo2L2Nu',
    '/ZZJetsTo2L2Q.*START53.*':'ZZJetsTo2L2Q',
    '/ZZJetsTo4L.*START53.*':'ZZJetsTo4L',
    '/WGToLNuG_TuneZ2star_8TeV-madgraph-tauola.*START53*.':'WgammaInc',
    '/WGstarToLNu2E_TuneZ2star_8TeV-madgraph-tauola.*START53*.':'Wgammaee',
    '/tblv_H126to2tau_q_Yt1-madgraph-pythia6.*START53*.':'tH_Yt1',
#    '/tblv_H126to2tau_q_YtMinus1-madgraph-pythia6.*START53*.':'tH_YtMinus1',
    '/phys_higgs-qtH-blv_1M-mH125Ct-1.*START50*.':'tH_YtMinus1',
    '/phys_higgs-WtH_1M-mH125Ct1.*START50*.':'tHW',
    '/DoubleMu/Run2012A-22Jan2013-v1*' : 'data_Run2012A',
    '/DoubleMuParked/Run2012B-22Jan2013-v1*' : 'data_Run2012B',
    '/DoubleMuParked/Run2012C-22Jan2013-v1*' : 'data_Run2012C',
    '/DoubleMuParked/Run2012D-22Jan2013-v1*' : 'data_Run2012D',
    '/MuEG/Run2012A-22Jan2013-v1*' : 'data_Run2012A',
    '/MuEG/Run2012B-22Jan2013-v1*' : 'data_Run2012B',
    '/MuEG/Run2012C-22Jan2013-v1*' : 'data_Run2012C',
    '/MuEG/Run2012D-22Jan2013-v1*' : 'data_Run2012D'
    }


mc_ewk += mc_dy
mc_ewk += t_mc_ewk
mc_ewk += mc_w
mc_ewk += mc_w_ext

MC_list = copy.copy( mc_diboson ) ## for mumuTau
MC_list.extend( mc_w )
MC_list.extend( mc_dy )
MC_list.extend( t_mc_ewk )
MC_list.extend( mc_ttbarh )
MC_list.extend( mc_ttv )
MC_list.extend( mc_vh )
#MC_list.extend( mc_tH )

allsamples = copy.copy( MC_list )
allsamples.extend( data_list )


#mc_repro = []
#mc_repro += mc_dy
#mc_repro += mc_higgs
#mc_repro += mc_higgs_susy

print 'connect to the db'
#connect(mc_diboson, '%TH_mmt_22jul_newTauID_manzoni%', 'cmgTuple_.*root', aliases, cache=True, verbose=False)
#connect(mc_diboson, '%TH_mmt_26sep_newTauID_manzoni%', 'cmgTuple_.*root', aliases, cache=True, verbose=False)
#connect(mc_diboson, '%MuMuTau_Yuta_Oct19%', 'cmgTuple_.*root', aliases, cache=True, verbose=False)
connect(MC_list, '%MUMUTAU_Sep27_yuta%', 'cmgTuple_.*root', aliases, cache=True, verbose=False)
connect(data_list, '%MuMuTau_Yuta_Oct13%', 'cmgTuple_.*root', aliases, cache=True, verbose=False)

#connect(t_mc_ewk, '%MuTauTau_Yuta_Feb28', 'cmgTuple_.*root', aliases, cache=True, verbose=False)
#connect(mc_dy, '%MuTauTau_Yuta_Feb28', 'cmgTuple_.*root', aliases, cache=True, verbose=False)
#connect(mc_w, '%MuTauTau_Yuta_Feb28', 'cmgTuple_.*root', aliases, cache=True, verbose=False)
#connect(data_list, '%MuTauTau_Yuta_Feb28', 'cmgTuple_.*root', aliases, cache=True, verbose=False)
#connect(mc_tH, '%MuTauTau_Yuta_Feb28', 'cmgTuple_.*root', aliases, cache=True, verbose=False)
connect(mc_tH, '%MUMUTAU_Sep27_yuta%', 'cmgTuple_.*root', aliases, cache=True, verbose=False)


#allsamples.extend( embed_list )
#allsamples.extend( mc_repro )
#MC_list.extend( mc_repro ) 

# Attach number of generated events for stitching
#dy_nevents = [ DYJets.nGenEvents,
#               DY1Jets.nGenEvents,
#               DY2Jets.nGenEvents,
#               DY3Jets.nGenEvents,
#               DY4Jets.nGenEvents
#               ]
#for dy in mc_dy:
#    dy.nevents = dy_nevents

# Attach number of generated events for stitching
#w_nevents = [ WJets.nGenEvents,
#               W1Jets.nGenEvents+W1Jets_ext.nGenEvents,
#               W2Jets.nGenEvents+W2Jets_ext.nGenEvents,
#               W3Jets.nGenEvents+W3Jets_ext.nGenEvents,
#               W4Jets.nGenEvents
#               ]
#for w in mc_w+mc_w_ext:
#    w.nevents = w_nevents

print [(s.name, s.dataset_entries) for s in allsamples if s.dataset_entries]
print [(s.name, s.dataset_entries) for s in allsamples if not s.dataset_entries]

for mc in MC_list:
    mc.triggers = mc_triggers
#    mc.dataset_entries = 10000
    
    # allsamples.append(mc)
for data in data_list:
    if len(data.files):
#        import pdb; pdb.set_trace()
        data.json = jsonPick( data.files[0], jsonMap)
#        data.triggers = data_parked_triggers_2012
        data.triggers = data_triggers
        # allsamples.append(data)
#for embed in embed_list:
#    if len(embed.files):
#        embed.json = jsonPick( embed.files[0], jsonMap)
#        embed.triggers = embed_triggers
        # No trigger requirements for embedded samples

for c in allsamples:
    c.splitFactor = splitFactor(c, 1e4)
