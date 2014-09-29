#pybatch.py -o mmt_20140826 mumutau_2014_cfg.py -b 'bsub -q 8nh -J mmt_20140826 < batchScript.sh'
#pybatch.py -o mmt_20140827 mumutau_2014_cfg.py -b 'bsub -q 8nh -J mmt_20140827 < batchScript.sh'
#pybatch.py -o mmt_20140929 mumutau_2014_cfg.py -b 'bsub -q 8nh -J mmt_20140929 < batchScript.sh'
pybatch.py -o mmt_20140929_data mumutau_2014_data.py -b 'bsub -q 8nh -J mmt_20140929_data < batchScript.sh'
