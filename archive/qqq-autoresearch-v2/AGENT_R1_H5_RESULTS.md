# H5 Results: SmaCross_30_100 — QQQ

## Hypothesis
SMA 30/100 crossover — intermediate speed between the rejected SMA 10/30 (too fast, whipsaw) and the current best SMA 50/200 (too slow, late reentry). May balance drawdown control with faster reentry after bear markets.

## Results

| Period | Ann. Return (%) | Max Drawdown (%) | Calmar | # Trades |
|--------|----------------|------------------|--------|----------|
| 5y     | 5.24           | -23.92           | 0.219  | 15       |
| 3y     | 14.99          | -14.84           | 1.010  | 9        |
| 2y     | 10.32          | -14.90           | 0.692  | 7        |
| 1y     | 28.81          | -15.00           | 1.921  | 4        |

## Baseline (SmaCross_50_200)
| Period | Ann. Return (%) | Max Drawdown (%) | Calmar |
|--------|----------------|------------------|--------|
| 5y     | 9.57           | -20.71           | 0.46   |
| 2y     | —              | —                | 1.45   |

## Verdict: WORSE

- **5y Calmar: 0.219 vs baseline 0.46** — significantly worse, fails to beat the target
- **2y Calmar: 0.692 vs baseline 1.45** — also worse, fails the ≥ 1.0 maintenance requirement

## Key Insight
The intermediate SMA 30/100 actually performs worse than the slower 50/200 on the 5-year window, taking on more drawdown (-23.92% vs -20.71%) while generating lower annualized returns (5.24% vs 9.57%), suggesting the faster crossover generates more false exits during QQQ's secular uptrend. The 3y window looks decent (Calmar 1.01) but this is period-specific — the 5y window captures the 2022 bear market where faster crossovers whipsaw more severely.
