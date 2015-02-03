Huk-A-Buk Simulator and Analysis Tool
=====================================

As an example of what kind of analysis can be done on the data:

```
$ python analyze.py \
> --analyze-func=analyze_ace_queen \
> --filename=data/results-1422910886-1000000.bindata
Bid: 2, Total Tricks: 4323
Pr(Win 0 tricks) = 0
Pr(Win 1 tricks) = 0.0414064
Pr(Win 2 tricks) = 0.272496
Pr(Win 3 tricks) = 0.284062
Pr(Win 4 tricks) = 0.20148
Pr(Win 5 tricks) = 0.200555
============================================================
Bid: 3, Total Tricks: 1319
Pr(Win 0 tricks) = 0
Pr(Win 1 tricks) = 0.0432146
Pr(Win 2 tricks) = 0.293404
Pr(Win 3 tricks) = 0.268385
Pr(Win 4 tricks) = 0.185747
Pr(Win 5 tricks) = 0.209249
============================================================
Bid: 4, Total Tricks: 25
Pr(Win 0 tricks) = 0
Pr(Win 1 tricks) = 0
Pr(Win 2 tricks) = 0.2
Pr(Win 3 tricks) = 0.24
Pr(Win 4 tricks) = 0.44
Pr(Win 5 tricks) = 0.12
============================================================
Bid: 5, Total Tricks: 18
Pr(Win 0 tricks) = 0
Pr(Win 1 tricks) = 0.0555556
Pr(Win 2 tricks) = 0.611111
Pr(Win 3 tricks) = 0.222222
Pr(Win 4 tricks) = 0.0555556
Pr(Win 5 tricks) = 0.0555556
============================================================
```

This seems to indicate that when the winning bidder holds Ace and Queen (and
makes that the trump), they will win 2 or 3 tricks most the time, 4 or 5
slightly less (around 1/5) and 1 trick around 1/20 of the time. We also
see they must never win 0 tricks (since the ACE).

Running this on the other 1,000,000 game sample yields similar findings.

```
$ python analyze.py \
> --analyze-func=analyze_ace_queen \
> --filename=data/results-1422909295-1000000.bindata
Bid: 2, Total Tricks: 4210
Pr(Win 0 tricks) = 0
Pr(Win 1 tricks) = 0.0401425
Pr(Win 2 tricks) = 0.271496
Pr(Win 3 tricks) = 0.281948
Pr(Win 4 tricks) = 0.207838
Pr(Win 5 tricks) = 0.198575
============================================================
Bid: 3, Total Tricks: 1288
Pr(Win 0 tricks) = 0
Pr(Win 1 tricks) = 0.0349379
Pr(Win 2 tricks) = 0.272516
Pr(Win 3 tricks) = 0.281056
Pr(Win 4 tricks) = 0.198758
Pr(Win 5 tricks) = 0.212733
============================================================
Bid: 4, Total Tricks: 33
Pr(Win 0 tricks) = 0
Pr(Win 1 tricks) = 0.0606061
Pr(Win 2 tricks) = 0.212121
Pr(Win 3 tricks) = 0.30303
Pr(Win 4 tricks) = 0.212121
Pr(Win 5 tricks) = 0.212121
============================================================
Bid: 5, Total Tricks: 22
Pr(Win 0 tricks) = 0
Pr(Win 1 tricks) = 0
Pr(Win 2 tricks) = 0.272727
Pr(Win 3 tricks) = 0.0909091
Pr(Win 4 tricks) = 0.363636
Pr(Win 5 tricks) = 0.272727
============================================================
```

## Focused Simulations

To simulate with a particular outcome in mind:

```
$ python long_simulation.py \
> --num-games 1000000 \
> --simulator-class=ace_queen
```

After doing this with a 1,000,000 game sample, we see the following
outputs:

```
$ python analyze.py \
> --analyze-func=analyze_ace_queen \
> --filename=data/results-1422928535-1000000-AceQueenSimulator.bindata
Bid: 2, Total Tricks: 871617
Pr(Win 0 tricks) = 0
Pr(Win 1 tricks) = 0.0398581
Pr(Win 2 tricks) = 0.270303
Pr(Win 3 tricks) = 0.288041
Pr(Win 4 tricks) = 0.202058
Pr(Win 5 tricks) = 0.19974
============================================================
Bid: 3, Total Tricks: 124744
Pr(Win 0 tricks) = 0
Pr(Win 1 tricks) = 0.0399618
Pr(Win 2 tricks) = 0.269496
Pr(Win 3 tricks) = 0.285777
Pr(Win 4 tricks) = 0.20413
Pr(Win 5 tricks) = 0.200635
============================================================
Bid: 4, Total Tricks: 2330
Pr(Win 0 tricks) = 0
Pr(Win 1 tricks) = 0.0424893
Pr(Win 2 tricks) = 0.25794
Pr(Win 3 tricks) = 0.298283
Pr(Win 4 tricks) = 0.20515
Pr(Win 5 tricks) = 0.196137
============================================================
Bid: 5, Total Tricks: 1309
Pr(Win 0 tricks) = 0
Pr(Win 1 tricks) = 0.0519481
Pr(Win 2 tricks) = 0.25974
Pr(Win 3 tricks) = 0.26356
Pr(Win 4 tricks) = 0.207028
Pr(Win 5 tricks) = 0.217723
============================================================
```
