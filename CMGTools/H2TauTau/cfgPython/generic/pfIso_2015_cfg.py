import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

from PhysicsTools.Heppy.analyzers.objects.LeptonAnalyzer import LeptonAnalyzer
from CMGTools.H2TauTau.proto.analyzers.MuonIsolationCalculator import MuonIsolationCalculator
from CMGTools.H2TauTau.proto.analyzers.MuonTreeProducer import MuonTreeProducer

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

# common configuration and sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import genAna, vertexAna


# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production')
production = False

muonIsoCalc = cfg.Analyzer(
    MuonIsolationCalculator,
    name='MuonIsolationCalculator'
)

muonTreeProducer = cfg.Analyzer(
    MuonTreeProducer,
    name='MuonTreeProducer'
)

creator = ComponentCreator()
ggh160 = creator.makeMCComponent("TTJets", "/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-AsymptNoPU_MCRUN2_74_V9A-v2/MINIAODSIM", "CMS", ".*root", 1.0)
dy = creator.makeMCComponent("DY", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-AsymptNoPURawReco_MCRUN2_74_V9A-v4/MINIAODSIM", "CMS", ".*root", 1.0)
qcd120 = creator.makeMCComponent("QCD120", "/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-AsymptNoPUReco_MCRUN2_74_V9A-v1/MINIAODSIM", "CMS", ".*root", 1.0)
qcd20 = creator.makeMCComponent("QCD20", "/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-AsymptNoPUReco_MCRUN2_74_V9A-v2/MINIAODSIM", "CMS", ".*root", 1.0)

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
selectedComponents = [dy, qcd120, qcd20] #DYJetsToLL_M50] # [ggh125]
for comp in selectedComponents:
    comp.splitFactor = 10000

sequence = cfg.Sequence([
    genAna,
    vertexAna,
    muonIsoCalc,
    muonTreeProducer
])

if not production:
    cache = True
    comp = selectedComponents[0]
    selectedComponents = [comp]
    comp.splitFactor = 10000
    comp.fineSplitFactor = 1
    # comp.files = comp.files[:1]


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
