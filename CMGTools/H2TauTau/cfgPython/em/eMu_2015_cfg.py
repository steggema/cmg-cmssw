import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps

from CMGTools.H2TauTau.proto.analyzers.LeptonIsolationCalculator import LeptonIsolationCalculator

# Tau-tau analyzers
from CMGTools.H2TauTau.proto.analyzers.MuEleAnalyzer             import MuEleAnalyzer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerMuEle import H2TauTauTreeProducerMuEle
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter            import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.SVfitProducer              import SVfitProducer

# common configuration and sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import commonSequence, genAna, dyJetsFakeAna, puFileData, puFileMC, eventSelector

from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.H2TauTau.proto.samples.spring15.triggers_muEle  import mc_triggers, mc_triggerfilters, data_triggers, data_triggerfilters

from CMGTools.H2TauTau.proto.samples.spring15.higgs_susy import HiggsSUSYGG160 as ggh160
from CMGTools.H2TauTau.proto.samples.spring15.higgs_susy import HiggsSUSYGG2000 as ggh2000
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import TT_pow, TT_pow_ext, DYJetsToLL_M50, WJetsToLNu, WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, QCD_Mu15, WWTo2L2Nu, ZZp8, WZp8, WWp8, SingleTop, WJetsToLNu_LO, QCD_Mu5, DYJetsToLL_M50_LO, TToLeptons_tch_powheg, TBarToLeptons_tch_powheg, VVTo2L2Nu, ZZTo2L2Q, ZZTo4L, WWTo1L1Nu2Q, WZTo2L2Q, WZTo3L, WZTo1L3Nu, WZTo1L1Nu2Q
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import MuonEG_Run2015D_05Oct, MuonEG_Run2015D_Promptv4, MuonEG_Run2015B_05Oct
from CMGTools.H2TauTau.proto.samples.spring15.higgs import HiggsGGH125, HiggsVBF125, HiggsTTH125


# local switches
syncntuple   = False
computeSVfit = False
production   = True  # production = True run on batch, production = False run locally

muonIsoCalc = cfg.Analyzer(
    LeptonIsolationCalculator,
    name='MuonIsolationCalculator',
    lepton='muon',
    getter=lambda event: [event.leg2]
)

electronIsoCalc = cfg.Analyzer(
    LeptonIsolationCalculator,
    name='ElectronIsolationCalculator',
    lepton='electron',
    getter=lambda event: [event.leg1]
)


dyJetsFakeAna.channel = 'em'

### Define mu-ele specific modules

muEleAna = cfg.Analyzer(
  MuEleAnalyzer                 ,
  'MuEleAnalyzer'               ,
  pt1          = 13.            ,
  eta1         = 2.5            ,
  iso1         = 0.15           ,
  looseiso1    = 9999.            ,
  pt2          = 10.            ,
  eta2         = 2.4            ,
  iso2         = 0.15           ,
  looseiso2    = 9999.            ,
  m_min        = 0.             ,
  m_max        = 99999          ,
  dR_min       = 0.3            ,
  from_single_objects=True,
  verbose      = False          ,
  )

muonWeighter = cfg.Analyzer(
  LeptonWeighter                  ,
  name        ='LeptonWeighter_mu',
  effWeight   = None              ,
  effWeightMC = None              ,
  lepton      = 'leg1'            ,
  verbose     = False             ,
  disable     = True              ,
  idWeight    = None              ,
  isoWeight   = None
  )

eleWeighter = cfg.Analyzer(
  LeptonWeighter                   ,
  name        ='LeptonWeighter_ele',
  effWeight   = None               ,
  effWeightMC = None               ,
  lepton      = 'leg2'             ,
  verbose     = False              ,
  disable     = True               ,
  idWeight    = None               ,
  isoWeight   = None
  )

treeProducer = cfg.Analyzer(
  H2TauTauTreeProducerMuEle         ,
  name = 'H2TauTauTreeProducerMuEle'
  )

syncTreeProducer = cfg.Analyzer(
  H2TauTauTreeProducerMuEle                     ,
  name         = 'H2TauTauSyncTreeProducerMuEle',
  varStyle     = 'sync'                         ,
#  skimFunction = 'event.isSignal'
  )

svfitProducer = cfg.Analyzer(
  SVfitProducer                ,
  name        = 'SVfitProducer',
  # integration = 'VEGAS'        ,
  integration = 'MarkovChain'  ,
  # verbose     = True           ,
  # order       = '21'           , # muon first, tau second
  l1type      = 'muon'         ,
  l2type      = 'ele'
  )


#samples = [ggh160]
#ggh125 = HiggsGGH125


#samples = [ggh160]

samples = [TToLeptons_tch_powheg, TBarToLeptons_tch_powheg, VVTo2L2Nu, ZZTo2L2Q, ZZTo4L, WWTo1L1Nu2Q, WZTo2L2Q, WZTo3L, WZTo1L3Nu, WZTo1L1Nu2Q]

#samples = [TT_pow_ext, WWTo2L2Nu]
#samples = [TT_pow, ggh160]
#samples += [WJetsToLNu_LO, DYJetsToLL_M50_LO]
#samples += [WWp8, ZZp8, WZp8]
#samples += [QCD_Mu15, HiggsGGH125, HiggsVBF125, HiggsTTH125] + SingleTop

split_factor = 1e5

for sample in samples:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)

data_list = [MuonEG_Run2015D_05Oct, MuonEG_Run2015D_Promptv4]

for sample in data_list:
    sample.triggers = data_triggers
    sample.triggerobjects = data_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt'
#    sample.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON_Silver.txt'
#    sample.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt'
    sample.lumi = 40.03


###################################################
###              ASSIGN PU to MC                ###
###################################################
for mc in samples:
    mc.puFileData = puFileData
    mc.puFileMC = puFileMC

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
#selectedComponents = samples
#selectedComponents = samples + data_list
selectedComponents = data_list
#selectedComponents = samples


###################################################
###                  SEQUENCE                   ###
###################################################
sequence = commonSequence
sequence.insert(sequence.index(genAna), muEleAna)
sequence.append(muonWeighter)
sequence.append(eleWeighter)
if computeSVfit:
    sequence.append(svfitProducer)
sequence.append(treeProducer)
if syncntuple:
    sequence.append(syncTreeProducer)

sequence.insert(sequence.index(treeProducer), muonIsoCalc)
sequence.insert(sequence.index(treeProducer), electronIsoCalc)
treeProducer.addIsoInfo = True


###################################################
###             CHERRY PICK EVENTS              ###
###################################################
# eventSelector.toSelect = [133381]
# sequence.insert(0, eventSelector)

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
  cache                = True
#  comp                 = my_connect.mc_dict['HiggsGGH125']
#  comp = MuonEG_Run2015D_05Oct
#  comp = MuonEG_Run2015D_Promptv4
#  comp = ggh2000
  comp = ggh160
  selectedComponents   = [comp]
  comp.splitFactor     = 8
  comp.fineSplitFactor = 1
#  comp.files           = comp.files[:1]

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config( components   = selectedComponents,
                     sequence     = sequence          ,
                     services     = []                ,
                     events_class = Events
                     )

printComps(config.components, True)

def modCfgForPlot(config):
  config.components = []
