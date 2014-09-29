import CMGTools.RootTools.fwlite.Config as cfg


tH_Yt1 = cfg.MCComponent(
    name = 'tH_Yt1',
    files = [],
    xSection = 0.01796, #PG from twiki: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2012#MC_samples_and_cross_sections
    nGenEvents = 0,
    triggers = [],
    effCorrFactor = 1 )


tH_YtMinus1 = cfg.MCComponent(
    name = 'tH_YtMinus1',
    files = [],
    xSection = 0.231, #PG from twiki: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2012#MC_samples_and_cross_sections
    nGenEvents = 0,
    triggers = [],
    effCorrFactor = 1 )



mc_tH = [
#    tH_Yt1,
    tH_YtMinus1
    ]
