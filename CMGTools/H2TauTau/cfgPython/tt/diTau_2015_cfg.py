import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

# Tau-tau analyzers
from CMGTools.H2TauTau.proto.analyzers.TauTauAnalyzer             import TauTauAnalyzer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerTauTau import H2TauTauTreeProducerTauTau
from CMGTools.H2TauTau.proto.analyzers.TauDecayModeWeighter       import TauDecayModeWeighter
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter             import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.SVfitProducer              import SVfitProducer

# common configuration and sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import commonSequence, genAna, dyJetsFakeAna, puFileData, puFileMC, eventSelector

# Get all heppy options; set via '-o production' or '-o production=True'

# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production')
# production = True
production = False

# local switches
syncntuple   = True
computeSVfit = False
# pick_events  = False
pick_events  = True

dyJetsFakeAna.channel = 'tt'

### Define tau-tau specific modules

tauTauAna = cfg.Analyzer(
  class_object = TauTauAnalyzer              ,
  name         = 'TauTauAnalyzer'            ,
  pt1          = 45                          ,
  eta1         = 2.1                         ,
  iso1         = 1.                          ,
  looseiso1    = 999999910.                         ,
  pt2          = 45                          ,
  eta2         = 2.1                         ,
  iso2         = 1.                          ,
  looseiso2    = 999999910.                         ,
#   isolation    = 'byIsolationMVA3newDMwLTraw',
  isolation    = 'byCombinedIsolationDeltaBetaCorrRaw3Hits', # RIC: 9 March 2015
  m_min        = 10                          ,
  m_max        = 99999                       ,
  dR_min       = 0.5                         ,
#   triggerMap   = pathsAndFilters             ,
  jetPt        = 30.                         ,
  jetEta       = 4.7                         ,
  relaxJetId   = False                       ,
  verbose      = False                       ,
  sameFlavour  = True                        ,  
  from_single_objects = True                 ,
  )

tauDecayModeWeighter = cfg.Analyzer(
  TauDecayModeWeighter   ,
  'TauDecayModeWeighter' ,
  legs = ['leg1', 'leg2'],
  )

tau1Weighter = cfg.Analyzer(
  LeptonWeighter                    ,
  name        ='LeptonWeighter_tau1',
  effWeight   = None                ,
  effWeightMC = None                ,
  lepton      = 'leg1'              ,
  verbose     = False               ,
  disable     = True                ,
  )

tau2Weighter = cfg.Analyzer(
  LeptonWeighter                    ,
  name        ='LeptonWeighter_tau2',
  effWeight   = None                ,
  effWeightMC = None                ,
  lepton      = 'leg2'              ,
  verbose     = False               ,
  disable     = True                ,
  )

treeProducer = cfg.Analyzer(
  H2TauTauTreeProducerTauTau         ,
  name = 'H2TauTauTreeProducerTauTau'
  )

syncTreeProducer = cfg.Analyzer(
  H2TauTauTreeProducerTauTau                     ,
  name         = 'H2TauTauSyncTreeProducerTauTau',
  varStyle     = 'sync'                          ,
  #skimFunction = 'event.isSignal' #don't cut out any events from the sync tuple
  )

svfitProducer = cfg.Analyzer(
  SVfitProducer,
  name        = 'SVfitProducer',
  # integration = 'VEGAS'        ,
  integration = 'MarkovChain'  ,
  # verbose     = True           ,
  # order       = '21'           , # muon first, tau second
  l1type      = 'tau'          ,
  l2type      = 'tau'
  )

###################################################
### CONNECT SAMPLES TO THEIR ALIASES AND FILES  ###
###################################################
# from CMGTools.H2TauTau.proto.samples.phys14.connector import httConnector
# my_connect = httConnector('htt_6mar15_manzoni_nom', 'htautau_group',
#                           '.*root', 'tt', production=production)
# my_connect.connect()
# MC_list = my_connect.MC_list

from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
from CMGTools.RootTools.samples.samples_13TeV_74X import TT_pow, DYJetsToLL_M50, WJetsToLNu, WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, QCD_Mu15, WWTo2L2Nu, ZZp8, WZp8, SingleTop
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import SingleMuon_Run2015B_17Jul, SingleMuon_Run2015B
from CMGTools.H2TauTau.proto.samples.spring15.triggers_tauTau import mc_triggers as mc_triggers_tt

creator = ComponentCreator()

ggh160   = creator.makeMCComponent  ("GGH160", 
                                     "/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", 
                                     "CMS", 
                                     ".*root", 
                                     1.0)
run2015B = creator.makeDataComponent("DataRun2015B", 
                                     "/Tau/Run2015B-PromptReco-v1/MINIAOD", 
                                     "CMS", 
                                     ".*root", 
                                     "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/DCSOnly/json_DCSONLY_Run2015B.txt"
                                     )

MC_list = [ggh160]

run2015B.intLumi  = '2.0' # in pb
run2015B.triggers = mc_triggers_tt

split_factor = 1e5

for sample in MC_list:
    sample.triggers = mc_triggers_tt
    sample.splitFactor = splitFactor(sample, split_factor)
    
data_list = [run2015B]

###################################################
###              ASSIGN PU to MC                ###
###################################################
for mc in MC_list:
    mc.puFileData = puFileData
    mc.puFileMC = puFileMC

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
selectedComponents = MC_list #+ data_list
# selectedComponents = mc_dict['HiggsGGH125']
for c in selectedComponents : 
    c.splitFactor *= 10
#     c.fineSplitFactor = 4

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = commonSequence
sequence.insert(sequence.index(genAna), tauTauAna)
sequence.append(tauDecayModeWeighter)
sequence.append(tau1Weighter)
sequence.append(tau2Weighter)
if computeSVfit:
    sequence.append(svfitProducer)
sequence.append(treeProducer)
if syncntuple:
    sequence.append(syncTreeProducer)

###################################################
###             CHERRY PICK EVENTS              ###
###################################################
if pick_events:

    import csv
    fileName = '/afs/cern.ch/work/m/manzoni/diTau2015/CMSSW_7_4_3/src/CMGTools/H2TauTau/cfgPython/2015-sync/Imperial.csv'
#     fileName = '/afs/cern.ch/work/m/manzoni/diTau2015/CMSSW_7_4_3/src/CMGTools/H2TauTau/cfgPython/2015-sync/CERN.csv'
    f = open(fileName, 'rb')
    reader = csv.reader(f)
    evtsToPick = []

    for i, row in enumerate(reader):
        evtsToPick += [int(j) for j in row]

    eventSelector.toSelect = evtsToPick
    eventSelector.toSelect = [711,2212,3557,3175,3186,21560,21644,21830,11081,8904,9998,10324,11352,12423,17678,13927,14457,14704,15057,15140,15640,15742,15225,19114,19295,19399,16618,23035,22797,22822,20138,20140,21305,21340,42254,42332,42460,28204,58365,58462,30283,30375,30401,34989,37340,42012,43067,62824,62955,44628,45138,45183,67223,56548,50587,53958,64684,59679,59819,61385,61691,118920,66907,66929,119753,119974,71638,73561,81374,82694,82945,83012,87314,98232,93584,99140,103136,103271,103300,103732,122528,122682,122694,122721,122777,104239,122006,105875,107155,107225,109270,111031,110649,118392,118481,111419,114287,114647,112037,112190,134573,134863,127088,116496,120238,125700,150677,122131,122319,122427,123840,124003,166133,126489,126706,129067,129900,130128,129158,129227,133888,137410,166767,138603,138627,138836,139311,147296,140047,142780,142922,143874,155429,155463,145245,146511,149370,154240,150011,150091,151053,151302,159004,159016,151726,151926,172385,172634,157553,159444,159509,190527,190551,163901,181953,172303,172358,164322,164509,165283,166159,166194,166323,166484,186820,186840,187059,168045,183024,190133,190284,170123,170333,170539,170676,171231,171378,171516,173699,203320,174218,175793,195441,195718,176246,176586,180229,180248,202381,181357,181362,181521,181707,182200,182219,185463,182565,182696,182743,184259,184360,188409,188752,189283,189461,187352,188775,188896,189089,188067,188095,188142,198590,198711,192339,192382,192443,199547,199675,197483,197562,196160,196785,217318,201438,202842,205221,477886,478411,479061,479098,479250,483987,480619,480653,482031,483189,483271,484526,484553,484824,484901,484932,485803,486081,486215,494725,494759,280190,280377,279005,281469,302455,299471,299484,282049,291446,291641,291688,296039,296166,296246,298583,299874,300109,300416,301311,302685,303498,303734,301509,302221,309965,303120,327726,306654,306875,305743,307531,307746,307979,308072,308421,310174,310808,312802,312915,338013,365140,317627,338772,319529,322721,322729,322772,326508,326602,328557,328598,328746,332159,339832,334121,337314,341890,342309,354015,342921,344066,344101,343306,343416,349643,344996,345208,345229,345396,388054,388073,388356,348370,348477,348537,354235,354302,355540,355641,375636,382615,360518,371053,371214,371238,366107,375503,371455,371549,379554,372284,372305,384161,384172,384203,384376,384401,377448,380006,380045,378709,379028,380797,397446,381846,382131,382207,382265,385833,385989,385262,387701,387735,387804,387849,387994,385427,385574,368029,457942,370514,374123,374216,381077,383959,399040,399104,399206,416726,416864,390070,390326,409689,409738,393360,393392,393396,395517,395677,396542,394396,431363,431495,400615,400733,400805,400825,404766,402104,403048,403897,403473,440896,440926,406663,406893,445113,410698,410731,410826,412633,412663,412251,416282,416333,427578,418260,424942,419944,420335,421836,440055,423132,423941,424290,425341,425365,425475,427312,427378,426463,428284,456085,431071,433388,441158,440572,440595,450609,470538,470546,463618,455247,455287,457154,457270,494011,461115,470090,490324,490519,467270,468003,474784,471200,471258,471405,474196,472530,472578,485528,479325,480004,480934,481159,486775,486776,486982,482183,487174,487339,493091,493271,488771,489578,91625,91637,90953,91989,92519,92531,92812,94840,95051,127959,128195,101457,101596,102244,104924,142063,142325,113842,114825,116684,116799,122976,123178,120914,120967,132615,131180,131298,152627,146247,187866,135926,136198,136738,142505,196366,196485,196498,145597,145725,145812,157820,147671,149374,149499,149511,149717,148281,148317,153302,161179,155109,155201,177820,155675,169982,179903,180089,246932,177202,186167,216746,193105,193156,193772,287122,237520,196995,197052,197073,198412,210287,210459,199247,199915,200799,200822,201656,221352,221459,221892,243886,249863,252570,252658,258353,296909,255681,255756,281583,257204,259468,260640,260864,260433,265625,265821,278268,270406,390,1686,1696,1525,2749,2808,2915,2941,4687,4731,5001,18020,14088,16937,26672,18664,19581,24280,31737,31958,25022,25132,29041,32226,32268,32279,34381,34633,32451,32587,32603,32612,32726,33742,32898,33319,33340,33371,35259,35344,35539,35740,35846,82528,36094,37504,36744,38858,38253,39824,40739,40757,46732,46775,40983,41430,41577,43297,45699,46164,47078,48826,54415,54501,51289,52832,52315,53524,53753,53087,81018,62551,62778,62391,55431,55523,55672,55762,56996,57164,57230,58005,58101,63472,66271,59558,60277,60650,60664,66456,66660,66661,65665,67743,68083,69430,69803,78889,73315,74110,76092,76373,77497,77600,77960,78077,112341,112480,112576,112627,88934,78609,83283,87885,88110,84456,89439,85253,85759,94254,490634,492752,492834,491052,496236,496414,495808,496054,494919,496700,498591,498609,498396,499548,206051,206548,208432,207174,207214,207535,207905,212196,212231,209216,209006,210080,210107,210173,216090,216092,210913,234305,224984,212842,231873,215295,215489,215610,217166,217682,217889,225161,219036,241500,241528,219975,220656,220708,224152,220808,242431,225800,225886,227090,227228,228476,227979,228098,228916,228952,229555,230561,229921,230222,230423,236265,236280,230965,231124,234710,241823,236647,236689,236831,255114,255191,237916,238360,238409,245725,245779,245921,248633,244929,259985,245368,245517,245605,283543,248935,250858,251126,250239,250353,251868,272005,272064,272102,252051,252100,252229,262208,252828,252926,253116,253229,268915,254759,263995,349430,258931,260932,261280,259093,259282,261792,261793,261938,264226,262514,273921,267220,267228,267529,268513,269334,269376,269618,272838,270951,270962,314687,271660,277804,272382,272571,285577,285592,273637,274900,357523,275002,275119,275179,276830,277039,277043,277198,277254,277356,280533,280549,280563,283234,284612,285370,286174,286706,287004,287482,289397,289446,288655,288688,288794,289032,289148,289203,290366,289861,290687,291820,292093,340434,340454,292218,292898,292977,293142,293741,293796,293820,326199,393960,304258,304489,308766,312123,312146,312206,312255,312290,311303,311521,311645,339396,323872,323997,330830,331392,327048,329882,330223,334944,335180,335471,335810,417738,417991,336608,351954,351955,339152,340573,356678,356692,351178,351250,346641,346285,347556,347675,364122,348920,401434,401468,350369,355275,351563,351664,350944,350961,350983,416953,417134,417145,352704,352711,352956,353011,353261,353620,358257,366813,366928,360326,372041,362151,364773,363317,376549,386508,415383,392889,393037,387434,391504,390950,394897,396000,396049,396237,396891,399973,398608,398764,413855,451566,407433,409356,422489,410426,410546,419572,456333,456537,456597,411597,413068,413079,413124,413141,413699,414610,414194,414463,433275,415113,415141,420755,426046,423383,424634,429800,429881,429890,429939,428956,426683,429015,429335,432582,432768,435794,436476,443175,437702,444445,438229,456810,457059,438834,438888,438953,439066,439290,439438,439529,441926,441989,442091,454276,454305,439617,439760,441596,441731,442951,443862,444087,444860,444946,446213,446218,446272,446309,446484,447857,447884,447619,448996,449207,499852,452543,493608,454382,454470,455819,458621,475973,459196,460174,466958,461456,462232,462430,463988,464900,466422,465583,468871,469266,481507,472873,473122,473334,474542,28660,29826,29847,51593,51748,51836,44077,44215,47450,69898,73902,74681,82192,79425,83871,84056,84816,86159,92912,86822,86889,90735,95711,96967,96013,101343,97245,97438,104123,108678,106760,110045,119465,119638,124138,124234,314974,133421,133521,141633,141917,148800,153052,160920,160978,161930,162162,162638,162730,163430,163471,163594,177994,178043,168181,168548,168724,250557,172821,189692,189812,178776,178802,180810,197903,197945,195022,344530,307201,275396,315535,315874,319072,323170,333575,341180,356310,361301,369157,369201,369308,370155,370349,372503,416045]
    sequence.insert(0, eventSelector)

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
  cache                = True
#   comp                 = my_connect.mc_dict['HiggsGGH125']
#   comp                 = DYJetsToLL_M50
#   comp                 = run2015B
  comp                 = ggh160
  selectedComponents   = [comp]
  comp.splitFactor     = 1
  comp.fineSplitFactor = 1
#   comp.files           = comp.files[:1]
#   for comp in selectedComponents:
#     comp.splitFactor     = 1
#     comp.fineSplitFactor = 4
    


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
