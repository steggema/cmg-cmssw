for a in DY DY1 DY2 DY3 DY4 W1jet W2jet W3jet W4jet WZ ZZ tt0l tt1l tt2l TTH TTW TTZ WW tH_YtMinus1 data
  do
  nice python sync.py --mode antiE --region f3 --phys $a &
  nice python sync.py --mode antiMu --region f3 --phys $a &
  nice python sync.py --mode antiEMu --region f3 --phys $a &
  nice python sync.py --mode signal --region f3 --phys $a 
  nice python sync.py --mode antiE --region f12 --phys $a &
  nice python sync.py --mode antiMu --region f12 --phys $a &
  nice python sync.py --mode antiEMu --region f12 --phys $a &
  nice python sync.py --mode signal --region f12 --phys $a 
done
