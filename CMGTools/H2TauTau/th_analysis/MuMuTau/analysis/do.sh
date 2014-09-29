## for sample generation

#for a in data WW WZ ZZ tt1l tt2l W1Jet W2Jet W3Jet W4Jet DY1 DY2 DY3 DY4 #tH_YtMinus1
for a in WZ
  do
  python sync.py --mode antiE --region f3 --phys $a &
  python sync.py --mode antiMu --region f3 --phys $a &
  python sync.py --mode antiEMu --region f3 --phys $a &
  python sync.py --mode signal --region f3 --phys $a &

  python sync.py --mode antiE --region f12 --phys $a &
  python sync.py --mode antiMu --region f12 --phys $a &
  python sync.py --mode antiEMu --region f12 --phys $a &
  python sync.py --mode signal --region f12 --phys $a &

done

