from ROOT import TFile, TH1F, TTree, TGraph, kBlue, kRed, TCanvas, gROOT, TLegend, gStyle
import os
import numpy
from officialStyle import officialStyle
officialStyle(gStyle)

def LegendSettings(leg):
  leg.SetBorderSize(0)
  leg.SetFillColor(0)
  leg.SetLineColor(0)
  leg.SetFillStyle(0)
  leg.SetTextSize(0.045)
  leg.SetTextFont(42)




rel_thr = 1.
#isBarrel = False
isBarrel = True

gROOT.SetBatch(True)

nbins = 10000

if isBarrel==True:
  rel_thr = 0.15
else:
  rel_thr = 0.1

def rocCurve(hS, hB, caption):
  ''' Create a ROC TGraph from two input histograms.
  '''

  global efficiency
  maxBin = hS.GetNbinsX()

  if hS.Integral() == 0.:
    print 'ROC curve creator, hist', hS.GetName(), 'has zero entries'
    return

  effsS = [hS.Integral(nBin, maxBin+1)/hS.Integral(0, maxBin+1) for nBin in range(0, maxBin + 1) ]
  rejB = [hB.Integral(nBin, maxBin+1)/hB.Integral(0, maxBin+1) for nBin in range(0, maxBin + 1) ]


  if caption.find('reliso')!=-1:
    effsS = [hS.Integral(0, nBin)/hS.Integral(0, maxBin+1) for nBin in range(0, maxBin + 1) ]
    rejB = [hB.Integral(0, nBin)/hB.Integral(0, maxBin+1) for nBin in range(0, maxBin + 1) ]

    FindBin = hS.FindBin(rel_thr)
    efficiency = hS.Integral(0, FindBin)/hS.Integral(0, maxBin+1)
    print 'relIso efficiency @ relIso < ', rel_thr, ' = ', efficiency

  else:
    ibin = -1

    for ii, ieff in enumerate(effsS):
      if ieff < efficiency and ibin==-1:
        ibin = hS.GetBinCenter(ii)

    print caption, 'cut on ', ibin, ' to get ', efficiency

  rocCurve = TGraph(maxBin, numpy.asarray(effsS), numpy.asarray(rejB))
#  rocCurve = TGraph(maxBin, numpy.asarray(rejB), numpy.asarray(effsS))


  return rocCurve



def decorate(h, col, xlabel='', ylabel=''):
  h.SetLineColor(col)
  h.SetMarkerColor(col)
  h.SetLineWidth(3)
  h.SetMinimum(0)
  h.SetMaximum(1)
  h.GetXaxis().SetNdivisions(506)
  h.GetYaxis().SetNdivisions(505)

  if xlabel!='':
    h.GetXaxis().SetTitle(xlabel)
  if ylabel!='':
    h.GetYaxis().SetTitle(ylabel)


if __name__ == '__main__':
  
  file_ = TFile("BDT_training_ss_f12.root")

  h_reliso_S = TH1F("h_reliso_S", "h_reliso_S", nbins,0,10.)
  h_reliso_B = TH1F("h_reliso_B", "h_reliso_B", nbins,0,10.)

  sig_criteria = "(bdt_evt_processid==16 &&  abs(bdt_muon_eta)"
  bkg_criteria = "(bdt_evt_processid>=4 && bdt_evt_processid<=5 && abs(bdt_muon_eta)"


  if isBarrel:
    sig_criteria += " < 1.479 && (abs(bdt_muon_pdg)==13 || abs(bdt_muon_pdg)==15))*bdt_evt_weight"
    bkg_criteria += " < 1.479 && !(abs(bdt_muon_pdg)==13 || abs(bdt_muon_pdg)==15))*bdt_evt_weight"
  else:
    sig_criteria += " > 1.479 && (abs(bdt_muon_pdg)==13 || abs(bdt_muon_pdg)==15))*bdt_evt_weight"
    bkg_criteria += " > 1.479 && !(abs(bdt_muon_pdg)==13 || abs(bdt_muon_pdg)==15))*bdt_evt_weight"


  file_.Tree.Draw("bdt_muon_reliso >> h_reliso_S", sig_criteria)
  file_.Tree.Draw("bdt_muon_reliso >> h_reliso_B", bkg_criteria)
            
  roc_reliso = rocCurve(h_reliso_S, h_reliso_B, 'muon_reliso')
  decorate(roc_reliso, 4, 'Eff Signal', 'Eff Background')
  decorate(h_reliso_S, 2)
  decorate(h_reliso_B, 4)

 # print 'relIso, S, B = ', h_reliso_S.GetEntries(), h_reliso_B.GetEntries()
#  print 'MVA S, B = ', h_giovanni_S.GetEntries(), h_giovanni_B.GetEntries()

  h_giovanni_S = TH1F("h_giovanni_S", "h_giovanni_S", nbins,-1,1)
  h_giovanni_B = TH1F("h_giovanni_B", "h_giovanni_B", nbins,-1,1)
  file_.Tree.Draw("bdt_muon_mva >> h_giovanni_S", sig_criteria)
  file_.Tree.Draw("bdt_muon_mva >> h_giovanni_B", bkg_criteria)
            
  roc_giovanni = rocCurve(h_giovanni_S, h_giovanni_B, 'muon_MVA')
  decorate(roc_giovanni, 2)
  decorate(h_giovanni_S, 2)
  decorate(h_giovanni_B, 4)


  h_yuta_S = TH1F("h_yuta_S", "h_yuta_S", nbins,-1,1)
  h_yuta_B = TH1F("h_yuta_B", "h_yuta_B", nbins,-1,1)
  file_.Tree.Draw("bdt_yuta_muon_mva >> h_yuta_S", sig_criteria)
  file_.Tree.Draw("bdt_yuta_muon_mva >> h_yuta_B", bkg_criteria)
            
  roc_yuta = rocCurve(h_yuta_S, h_yuta_B, 'muon_MVA_yuta')
  decorate(roc_yuta, 8)
  decorate(h_yuta_S, 2)
  decorate(h_yuta_B, 4)



#  can_leptonMVA_muon = TCanvas("can_leptonMVA_muon")
#  h_giovanni_S.DrawNormalized()
#  h_giovanni_B.DrawNormalized("same")
#
#  can_leptoniso_muon = TCanvas("can_leptoniso_muon")
#  h_reliso_S.DrawNormalized()
#  h_reliso_B.DrawNormalized("same")

  can_roc_muon = TCanvas("can_roc_muon")

  title = 'muon'
  if isBarrel:
    title += ' (Barrel)'
  else:
    title += ' (Endcap)'
    
  roc_reliso.SetTitle(title)
  roc_reliso.Draw("al")
  roc_giovanni.Draw("lsame")
  roc_yuta.Draw("lsame")

  leg = TLegend(0.2,0.65,0.4,0.85)
  LegendSettings(leg)

  leg.AddEntry(roc_reliso, 'relIso', 'l')
  leg.AddEntry(roc_giovanni, 'ttH lepton MVA', 'l')
  leg.AddEntry(roc_yuta, 'tH lepton MVA', 'l')
  leg.Draw()



  print 'relIso : S = ', h_reliso_S.GetEntries(), 'B = ', h_reliso_B.GetEntries()
  print 'MVA : S = ', h_giovanni_S.GetEntries(), 'B = ', h_giovanni_B.GetEntries()
  print 'MVA_yuta : S = ', h_yuta_S.GetEntries(), 'B = ', h_yuta_B.GetEntries()




  #########################################################################

  ce = TCanvas("roc_electron")

  esig_criteria = sig_criteria.replace('13','11').replace('muon','electron')
  ebkg_criteria = bkg_criteria.replace('13','11').replace('muon','electron')

  print esig_criteria
  print ebkg_criteria
  
  e_reliso_S = TH1F("e_reliso_S", "e_reliso_S", nbins,0,10)
  e_reliso_B = TH1F("e_reliso_B", "e_reliso_B", nbins,0,10)
  file_.Tree.Draw("bdt_electron_reliso >> e_reliso_S", esig_criteria)
  file_.Tree.Draw("bdt_electron_reliso >> e_reliso_B", ebkg_criteria)
            
  eroc_reliso = rocCurve(e_reliso_S, e_reliso_B, 'electron_reliso')
  decorate(eroc_reliso, 4, 'Eff Signal', 'Eff Background')
  decorate(e_reliso_S, 2)
  decorate(e_reliso_B, 4)


  e_giovanni_S = TH1F("e_giovanni_S", "e_giovanni_S", nbins,-1,1)
  e_giovanni_B = TH1F("e_giovanni_B", "e_giovanni_B", nbins,-1,1)
  file_.Tree.Draw("bdt_electron_mva >> e_giovanni_S", esig_criteria)
  file_.Tree.Draw("bdt_electron_mva >> e_giovanni_B", ebkg_criteria)
            
  eroc_giovanni = rocCurve(e_giovanni_S, e_giovanni_B, 'electron_MVA')
  decorate(eroc_giovanni, 2)
  decorate(e_giovanni_S, 2)
  decorate(e_giovanni_B, 4)

  e_yuta_S = TH1F("e_yuta_S", "e_yuta_S", nbins,-1,1)
  e_yuta_B = TH1F("e_yuta_B", "e_yuta_B", nbins,-1,1)
  file_.Tree.Draw("bdt_yuta_electron_mva >> e_yuta_S", esig_criteria)
  file_.Tree.Draw("bdt_yuta_electron_mva >> e_yuta_B", ebkg_criteria)
            
  eroc_yuta = rocCurve(e_yuta_S, e_yuta_B, 'electron_MVA_yuta')
  decorate(eroc_yuta, 8, 'signal efficiency', 'background efficiency')
  decorate(e_yuta_S, 2)
  decorate(e_yuta_B, 4)

  
#  ecan_leptonMVA_electron = TCanvas("ecan_leptonMVA_electron")
#  e_giovanni_S.DrawNormalized()
#  e_giovanni_B.DrawNormalized("same")
#
#  ecan_leptoniso_electron = TCanvas("ecan_leptoniso_electron")
#  e_reliso_S.DrawNormalized()
#  e_reliso_B.DrawNormalized("same")

  ecan_roc_electron = TCanvas("ecan_roc_electron")
  eroc_reliso.SetTitle(title.replace('muon','electron'))
  eroc_reliso.Draw("al")
  eroc_giovanni.Draw("lsame")
  eroc_yuta.Draw("lsame")

  eleg = TLegend(0.2,0.65,0.4,0.85)
  LegendSettings(eleg)

  eleg.AddEntry(eroc_reliso, 'relIso', 'l')
  eleg.AddEntry(eroc_giovanni, 'ttH lepton MVA', 'l')
  eleg.AddEntry(eroc_yuta, 'tH lepton MVA', 'l')
  eleg.Draw()


  print 'relIso : S = ', e_reliso_S.GetEntries(), 'B = ', e_reliso_B.GetEntries()
  print 'MVA : S = ', e_giovanni_S.GetEntries(), 'B = ', e_giovanni_B.GetEntries()
  print 'MVA_yuta : S = ', e_yuta_S.GetEntries(), 'B = ', e_yuta_B.GetEntries()
