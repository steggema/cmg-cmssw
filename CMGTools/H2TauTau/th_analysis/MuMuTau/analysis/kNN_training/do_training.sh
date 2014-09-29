#python tmva_training.py --channel electron --process data
#python tmva_training.py --channel electron --process WZ
#python tmva_training.py --channel electron --process ZZ
#python tmva_training.py --channel muon --process data
#python tmva_training.py --channel muon --process WZ
#python tmva_training.py --channel muon --process ZZ

python tmva_training.py --channel muon --process tt1l
python tmva_training.py --channel electron --process tt1l

python tmva_training.py --channel muon --process tt2l
python tmva_training.py --channel electron --process tt2l

python tmva_training.py --channel muon --process WZ
python tmva_training.py --channel electron --process WZ

python tmva_training.py --channel muon --process ZZ
python tmva_training.py --channel electron --process ZZ

python tmva_training.py --channel muon --process data
python tmva_training.py --channel electron --process data
