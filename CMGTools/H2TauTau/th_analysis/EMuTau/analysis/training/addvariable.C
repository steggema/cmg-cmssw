#include <iostream>
#include <string>
#include "TFile.h"
#include "TTree.h"
#include "TMath.h"

void addvariable(TString filename, TString output){
  
  std::cout << "input file = " <<  filename << std::endl;
  std::cout << "output file = " <<  output << std::endl;

  TFile *lFile = new TFile(filename);
  TTree *lTree = (TTree*) lFile->FindObjectAny("Tree");

  Double_t muon_dxy = 0;
  Double_t muon_dz = 0;
  Double_t muon_ch_iso = 0;
  Double_t muon_neu_iso = 0;
  Double_t muon_jet_dr = 0;
  Double_t muon_ptratio = 0;
  Double_t muon_csv = 0;

  Double_t electron_score = 0;
  Double_t electron_ch_iso = 0;
  Double_t electron_neu_iso = 0;
  Double_t electron_jet_dr = 0;
  Double_t electron_ptratio = 0;
  Double_t electron_csv = 0;

  lTree->SetBranchAddress("muon_dxy", &muon_dxy);
  lTree->SetBranchAddress("muon_dz", &muon_dz);
  lTree->SetBranchAddress("muon_mva_ch_iso", &muon_ch_iso);
  lTree->SetBranchAddress("muon_mva_neu_iso", &muon_neu_iso);
  lTree->SetBranchAddress("muon_mva_jet_dr", &muon_jet_dr);
  lTree->SetBranchAddress("muon_mva_ptratio", &muon_ptratio);
  lTree->SetBranchAddress("muon_mva_csv", &muon_csv);

  lTree->SetBranchAddress("electron_mva_score", &electron_score);
  lTree->SetBranchAddress("electron_mva_ch_iso", &electron_ch_iso);
  lTree->SetBranchAddress("electron_mva_neu_iso", &electron_neu_iso);
  lTree->SetBranchAddress("electron_mva_jet_dr", &electron_jet_dr);
  lTree->SetBranchAddress("electron_mva_ptratio", &electron_ptratio);
  lTree->SetBranchAddress("electron_mva_csv", &electron_csv);


  TMVA::Reader *reader = new TMVA::Reader("!Color"); 
  Float_t var1, var2, var3, var4, var5, var6, var7;

  reader->AddVariable("bdt_muon_dxy", &var1);
  reader->AddVariable("bdt_muon_dz", &var2);
  reader->AddVariable("bdt_muon_mva_ch_iso", &var3);
  reader->AddVariable("bdt_muon_mva_neu_iso", &var4);
  reader->AddVariable("bdt_muon_mva_jet_dr", &var5);
  reader->AddVariable("bdt_muon_mva_ptratio", &var6);
  reader->AddVariable("bdt_muon_mva_csv", &var7); 
  reader->BookMVA( "MVA_classifier", "weights/TMVAClassification_BDT_muon.weights.xml");


  TMVA::Reader *ereader = new TMVA::Reader("!Color"); 
  Float_t evar1, evar2, evar3, evar4, evar5, evar6;

  ereader->AddVariable("bdt_electron_mva_score", &evar1);
  ereader->AddVariable("bdt_electron_mva_ch_iso", &evar2);
  ereader->AddVariable("bdt_electron_mva_neu_iso", &evar3);
  ereader->AddVariable("bdt_electron_mva_jet_dr", &evar4);
  ereader->AddVariable("bdt_electron_mva_ptratio", &evar5);
  ereader->AddVariable("bdt_electron_mva_csv", &evar6); 
  ereader->BookMVA( "eMVA_classifier", "weights/TMVAClassification_BDT_electron.weights.xml");


  TFile *lOFile = new TFile(output,"RECREATE");
  TTree *lOTree = lTree->CloneTree(0);
   
  Float_t yuta_muon_mva;
  Float_t yuta_electron_mva;
  lOTree->Branch("yuta_muon_mva", &yuta_muon_mva, "yuta_muon_mva/F");
  lOTree->Branch("yuta_electron_mva", &yuta_electron_mva, "yuta_electron_mva/F");


  for (Long64_t i0=0; i0<lTree->GetEntries(); i0++) {
    lTree->GetEntry(i0);

    var1 = muon_dxy;
    var2 = muon_dz;
    var3 = muon_ch_iso;
    var4 = muon_neu_iso;
    var5 = muon_jet_dr;
    var6 = muon_ptratio;
    var7 = muon_csv;

    yuta_muon_mva =  reader->EvaluateMVA("MVA_classifier");

    evar1 = electron_score;
    evar2 = electron_ch_iso;
    evar3 = electron_neu_iso;
    evar4 = electron_jet_dr;
    evar5 = electron_ptratio;
    evar6 = electron_csv;

    yuta_electron_mva =  ereader->EvaluateMVA("eMVA_classifier");

    std::cout << var1 << " " << var2 << " " << var3 << " " << var4 << " " << var5 << " " << var6 << " " << var7 << " " << yuta_muon_mva << std::endl;
    std::cout << evar1 << " " << evar2 << " " << evar3 << " " << evar4 << " " << evar5 << " " << evar6 << " " << yuta_electron_mva << std::endl;
    lOTree->Fill();    
  }

  lOTree->Write();
  lOFile->Close();

  delete lFile;

  lFile = 0; lTree = 0; lOTree = 0;

}

