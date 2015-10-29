import PhysicsTools.HeppyCore.framework.config as cfg

from CMGTools.H2TauTau.tauMu_2015_base_cfg import sequence

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import TT_pow, DYJetsToLL_M50, WJetsToLNu, WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, QCD_Mu15, WWTo2L2Nu, ZZp8, WZp8, SingleTop, WJetsToLNu_LO, QCD_Mu5, DYJetsToLL_M50_LO
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import SingleMuon_Run2015D_05Oct, SingleMuon_Run2015B_05Oct, SingleMuon_Run2015D_Promptv4
from CMGTools.H2TauTau.proto.samples.spring15.triggers_tauMu import mc_triggers, mc_triggerfilters
from CMGTools.H2TauTau.proto.samples.spring15.triggers_tauMu import data_triggers, data_triggerfilters
from CMGTools.H2TauTau.proto.samples.spring15.higgs import HiggsGGH125, HiggsVBF125, HiggsTTH125

from CMGTools.H2TauTau.htt_ntuple_base_cff import puFileData, puFileMC, eventSelector

# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production')
production = True
pick_events = False
syncntuple = False

creator = ComponentCreator()

from CMGTools.H2TauTau.proto.samples.spring15.higgs_susy import HiggsSUSYGG160 as ggh160

qcd_flat = creator.makeMCComponent("QCDflat", "/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIISpring15DR74-Asympt25nsRaw_MCRUN2_74_V9-v3/MINIAODSIM", "CMS", ".*root", 2022100000.)

ggh125 = HiggsGGH125


samples = [qcd_flat, TT_pow, DYJetsToLL_M50, WJetsToLNu, WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, ggh125, ggh160]

samples += [WWTo2L2Nu, ZZp8, WZp8]

samples += [QCD_Mu15, HiggsGGH125, HiggsVBF125, HiggsTTH125] + SingleTop


# Additional samples
samples = [WJetsToLNu_LO, DYJetsToLL_M50_LO]

samples += QCD_Mu5

split_factor = 1e5

for sample in samples:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)

data_list = [SingleMuon_Run2015D_05Oct, SingleMuon_Run2015D_Promptv4]#SingleMuon_Run2015B_05Oct, 

for sample in data_list:
    sample.triggers = data_triggers
    sample.triggerobjects = data_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-258750_13TeV_PromptReco_Collisions15_25ns_JSON.txt'
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
selectedComponents = samples + data_list
selectedComponents = data_list
selectedComponents = samples


###################################################
###             CHERRY PICK EVENTS              ###
###################################################

if pick_events:
    eventSelector.toSelect = [308041,191584,240060,73996]
    sequence.insert(0, eventSelector)

if not syncntuple:
    module = [s for s in sequence if s.name == 'H2TauTauSyncTreeProducerTauMu'][0]
    sequence.remove(module)

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    cache = True
    comp = samples[0]
    selectedComponents = [comp]
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    # comp.files = comp.files[]


# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                    )

printComps(config.components, True)

def modCfgForPlot(config):
    config.components = []
