Huk-A-Buk Simulator and Analysis Tool
=====================================

As an example of what kind of analysis can be done on the data:

```
$ python analyze.py \
> --analyze-func=analyze_ace_queen \
> --filename=data/results-1422910886-1000000.bindata
{
  "2": {
    "1": 2,
    "2": 2,
    "3": 2,
    "4": 2,
    "5": 2
  },
  "3": {
    "1": 2,
    "2": 2,
    "3": 2,
    "4": 2,
    "5": 2
  },
  "4": {
    "2": 2,
    "3": 1,
    "4": 1,
    "5": 1
  },
  "5": {
    "1": 1,
    "2": 2,
    "3": 1,
    "4": 1,
    "5": 1
  }
}
```

This seems to indicate that when the winning bidder holds Ace and Queen (and
makes that the trump), they will win between 1-5 tricks with equal probability.

It is a bit surprising that of 1,000,000 simulated games, only 31 result in
a winning bid that holds only Ace and Queen of trump.

Running this on the other 1,000,000 game sample yields similar findings.

```
$ python analyze.py \
> --analyze-func=analyze_ace_queen \
> --filename=data/results-1422909295-1000000.bindata
{
  "2": {
    "1": 2,
    "2": 2,
    "3": 2,
    "4": 2,
    "5": 2
  },
  "3": {
    "1": 2,
    "2": 2,
    "3": 2,
    "4": 2,
    "5": 2
  },
  "4": {
    "1": 1,
    "2": 2,
    "3": 2,
    "4": 2,
    "5": 2
  },
  "5": {
    "2": 2,
    "3": 1,
    "4": 1,
    "5": 2
  }
}
```
