#include "RecoEgamma/EgammaTools/interface/PhotonEnergyCalibrator.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"
#include "FWCore/Utilities/interface/Exception.h"
#include <CLHEP/Random/RandGaussQ.h>
#include "RecoEgamma/EgammaTools/interface/EGEnergySysIndex.h"

const EnergyScaleCorrection::ScaleCorrection PhotonEnergyCalibrator::defaultScaleCorr_;
const EnergyScaleCorrection::SmearCorrection PhotonEnergyCalibrator::defaultSmearCorr_;

PhotonEnergyCalibrator::PhotonEnergyCalibrator(const std::string& correctionFile):
  correctionRetriever_(correctionFile),
  rng_(nullptr),
  minEt_(1.0)
{

}

void PhotonEnergyCalibrator::initPrivateRng(TRandom *rnd)
{
  rng_ = rnd;
}

std::vector<float> PhotonEnergyCalibrator::
calibrate(reco::Photon &photon,const unsigned int runNumber, 
	  const EcalRecHitCollection *recHits, 
	  edm::StreamID const & id, 
	  const PhotonEnergyCalibrator::EventType eventType) const
{
  return calibrate(photon,runNumber,recHits,gauss(id),eventType);
}

std::vector<float> PhotonEnergyCalibrator::
calibrate(reco::Photon &photon,const unsigned int runNumber, 
	  const EcalRecHitCollection *recHits, 
	  const float smearNrSigma, 
	  const PhotonEnergyCalibrator::EventType eventType) const
{
  const float scEtaAbs = std::abs(photon.superCluster()->eta());
  const float et = photon.getCorrectedEnergy(reco::Photon::P4type::regression2) / cosh(scEtaAbs);

  if (et < minEt_) {
    std::vector<float> retVal(EGEnergySysIndex::kNrSysErrs,
			      photon.getCorrectedEnergy(reco::Photon::P4type::regression2));
    retVal[EGEnergySysIndex::kScaleValue]  = 1.0;
    retVal[EGEnergySysIndex::kSmearValue]  = 0.0;
    retVal[EGEnergySysIndex::kSmearNrSigma]  = smearNrSigma;
    retVal[EGEnergySysIndex::kEcalErrPreCorr] = photon.getCorrectedEnergyError(reco::Photon::P4type::regression2); 
    retVal[EGEnergySysIndex::kEcalErrPostCorr] = photon.getCorrectedEnergyError(reco::Photon::P4type::regression2);
    retVal[EGEnergySysIndex::kEcalTrkPreCorr] = 0.;
    retVal[EGEnergySysIndex::kEcalTrkErrPreCorr] = 0.;
    retVal[EGEnergySysIndex::kEcalTrkPostCorr] = 0.;
    retVal[EGEnergySysIndex::kEcalTrkErrPostCorr] = 0.;
    
    return retVal;
  }

  const DetId seedDetId = photon.superCluster()->seed()->seed();
  EcalRecHitCollection::const_iterator seedRecHit = recHits->find(seedDetId);
  unsigned int gainSeedSC = 12;
  if (seedRecHit != recHits->end()) {
    if(seedRecHit->checkFlag(EcalRecHit::kHasSwitchToGain6)) gainSeedSC = 6;
    if(seedRecHit->checkFlag(EcalRecHit::kHasSwitchToGain1)) gainSeedSC = 1;
  }
  
  const EnergyScaleCorrection::ScaleCorrection* scaleCorr = correctionRetriever_.getScaleCorr(runNumber, et, scEtaAbs, photon.full5x5_r9(), gainSeedSC);  
  const EnergyScaleCorrection::SmearCorrection* smearCorr = correctionRetriever_.getSmearCorr(runNumber, et, scEtaAbs, photon.full5x5_r9(), gainSeedSC);  
  if(scaleCorr==nullptr) scaleCorr=&defaultScaleCorr_;
  if(smearCorr==nullptr) smearCorr=&defaultSmearCorr_;
 

  std::vector<float> uncertainties(EGEnergySysIndex::kNrSysErrs,0.);
  
  uncertainties[EGEnergySysIndex::kScaleValue]  = scaleCorr->scale();
  uncertainties[EGEnergySysIndex::kSmearValue]  = smearCorr->sigma(et); //even though we use scale = 1.0, we still store the value returned for MC
  uncertainties[EGEnergySysIndex::kSmearNrSigma]  = smearNrSigma;
  //MC central values are not scaled (scale = 1.0), data is not smeared (smearNrSigma = 0)
  //smearing still has a second order effect on data as it enters the E/p combination as an 
  //extra uncertainty on the calo energy
  //MC gets all the scale systematics
  if(eventType == EventType::DATA){ 
    setEnergyAndSystVarations(scaleCorr->scale(),0.,et,*scaleCorr,*smearCorr,photon,uncertainties);
  }else if(eventType == EventType::MC){
    setEnergyAndSystVarations(1.0,smearNrSigma,et,*scaleCorr,*smearCorr,photon,uncertainties);
  }
  
  return uncertainties;
  
}

void PhotonEnergyCalibrator::
setEnergyAndSystVarations(const float scale,const float smearNrSigma,const float et,
			  const EnergyScaleCorrection::ScaleCorrection& scaleCorr,
			  const EnergyScaleCorrection::SmearCorrection& smearCorr,
			  reco::Photon& photon,
			  std::vector<float>& energyData)const
{
 
  const float smear = smearCorr.sigma(et);   
  const float smearRhoUp = smearCorr.sigma(et,1,0);
  const float smearRhoDn = smearCorr.sigma(et,-1,0);
  const float smearPhiUp = smearCorr.sigma(et,0,1);
  const float smearPhiDn = smearCorr.sigma(et,0,-1);
 
  const float corr = scale + smear * smearNrSigma;
  const float corrRhoUp = scale + smearRhoUp * smearNrSigma;
  const float corrRhoDn = scale + smearRhoDn * smearNrSigma;
  const float corrPhiUp = scale + smearPhiUp * smearNrSigma;
  const float corrPhiDn = scale + smearPhiDn * smearNrSigma;
  const float corrUp = corrPhiUp;
  const float corrDn = corrPhiDn;

  const float scaleShiftStatUp = 1+scaleCorr.scaleErrStat();
  const float scaleShiftStatDn = 1-scaleCorr.scaleErrStat();
  const float scaleShiftSystUp = 1+scaleCorr.scaleErrSyst();
  const float scaleShiftSystDn = 1-scaleCorr.scaleErrSyst();
  const float scaleShiftGainUp = 1+scaleCorr.scaleErrGain();
  const float scaleShiftGainDn = 1-scaleCorr.scaleErrGain();
  const float scaleShiftUp = 1+scaleCorr.scaleErr(EnergyScaleCorrection::kErrStatSystGain);
  const float scaleShiftDn = 1-scaleCorr.scaleErr(EnergyScaleCorrection::kErrStatSystGain);

  
  const double oldEcalEnergy = photon.getCorrectedEnergy(reco::Photon::P4type::regression2);
  const double oldEcalEnergyError = photon.getCorrectedEnergyError(reco::Photon::P4type::regression2);
  
  energyData[EGEnergySysIndex::kEcalPreCorr] = oldEcalEnergy;
  energyData[EGEnergySysIndex::kEcalErrPreCorr] = oldEcalEnergyError;

  const double newEcalEnergy      = oldEcalEnergy * corr;
  const double newEcalEnergyError = std::hypot(oldEcalEnergyError * corr, smear * newEcalEnergy);
  photon.setCorrectedEnergy(reco::Photon::P4type::regression2, newEcalEnergy, newEcalEnergyError, true);
  
  energyData[EGEnergySysIndex::kScaleStatUp]   = oldEcalEnergy * scaleShiftStatUp * corr;
  energyData[EGEnergySysIndex::kScaleStatDown] = oldEcalEnergy * scaleShiftStatDn * corr;
  energyData[EGEnergySysIndex::kScaleSystUp]   = oldEcalEnergy * scaleShiftSystUp * corr;
  energyData[EGEnergySysIndex::kScaleSystDown] = oldEcalEnergy * scaleShiftSystDn * corr;
  energyData[EGEnergySysIndex::kScaleGainUp]   = oldEcalEnergy * scaleShiftGainUp * corr;
  energyData[EGEnergySysIndex::kScaleGainDown] = oldEcalEnergy * scaleShiftGainDn * corr;
  energyData[EGEnergySysIndex::kSmearRhoUp]    = oldEcalEnergy * corrRhoUp;
  energyData[EGEnergySysIndex::kSmearRhoDown]  = oldEcalEnergy * corrRhoDn;
  energyData[EGEnergySysIndex::kSmearPhiUp]    = oldEcalEnergy * corrPhiUp;
  energyData[EGEnergySysIndex::kSmearPhiDown]  = oldEcalEnergy * corrPhiDn;
  
  // The total variation
  energyData[EGEnergySysIndex::kScaleUp]   = oldEcalEnergy * scaleShiftUp * corr;
  energyData[EGEnergySysIndex::kScaleDown] = oldEcalEnergy * scaleShiftDn * corr;
  energyData[EGEnergySysIndex::kSmearUp]   = oldEcalEnergy * corrUp;
  energyData[EGEnergySysIndex::kSmearDown] = oldEcalEnergy * corrDn;

  
  energyData[EGEnergySysIndex::kEcalPostCorr] = photon.getCorrectedEnergy(reco::Photon::P4type::regression2);
  energyData[EGEnergySysIndex::kEcalErrPostCorr] = photon.getCorrectedEnergyError(reco::Photon::P4type::regression2);
}  


double PhotonEnergyCalibrator::gauss(edm::StreamID const& id) const
{
  if (rng_) {
    return rng_->Gaus();
  } else {
    edm::Service<edm::RandomNumberGenerator> rng;
    if ( !rng.isAvailable() ) {
      throw cms::Exception("Configuration")
	<< "XXXXXXX requires the RandomNumberGeneratorService\n"
	"which is not present in the configuration file.  You must add the service\n"
	"in the configuration file or remove the modules that require it.";
		}
    CLHEP::RandGaussQ gaussDistribution(rng->getEngine(id), 0.0, 1.0);
    return gaussDistribution.fire();
  }
}

