## for sample generation
for a in DY DY1 DY2 DY3 DY4 Wjet W1jet W2jet W3jet W4jet WW WZ ZZ tt0l tt1l tt2l TTW TTH TTZ tW tbW t_tchan tbar_tchan WH data #tH_YtMinus1
#for a in data
  do
#  python sync.py --mode antiE --region f3 --phys $a &
#  python sync.py --mode antiMu --region f3 --phys $a &
#  python sync.py --mode antiEMu --region f3 --phys $a &
#  python sync.py --mode signal --region f3 --phys $a &
#
#  python sync.py --mode antiE --region f12 --phys $a &
#  python sync.py --mode antiMu --region f12 --phys $a &
#  python sync.py --mode antiEMu --region f12 --phys $a &
  python sync.py --mode signal --region f12 --phys $a &

done

