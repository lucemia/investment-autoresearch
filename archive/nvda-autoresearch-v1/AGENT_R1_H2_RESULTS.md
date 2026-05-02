# H2 Results: Price > 200-Day SMA Regime Filter — NVDA

## Hypothesis
Hold NVDA when Close > SMA(200); go to cash otherwise. This is a faster exit/entry mechanism compared to the 50/200 golden-cross crossover (H1), reacting as soon as price dips below its 200-day average rather than waiting for a slower MA cross. On QQQ this regime filter beat the crossover on 5y returns; the question is whether it works on NVDA's more violent price swings.

## Results

| Period | Ann. Return % | Max DD %  | Calmar | # Trades |
|--------|--------------|-----------|--------|----------|
| 5y     | 43.16        | -33.27    | 1.297  | 9        |
| 3y     | 27.17        | -33.20    | 0.818  | 5        |
| 2y     | 10.59        | -17.34    | 0.611  | 3        |
| 1y     |  4.23        | -11.58    | 0.365  | 2        |

Baseline (BuyAndHold, 5y): Ann. 68.97%, MaxDD -66.33%, Calmar 1.04

## Verdict vs Baseline: MIXED

- **MaxDD goal MET on 5y**: -33.27% is well below the -40% target (vs. -66.33% for buy-and-hold). This is the primary goal.
- **Calmar goal MET on 5y**: 1.297 > 1.04 baseline. H2 beats the baseline on the risk-adjusted metric over the full 5-year window.
- **Shorter periods underperform**: 3y, 2y, and 1y Calmar ratios all fall below the 1.04 baseline, suggesting the strategy's edge comes primarily from avoiding the large 2022 bear market drawdown rather than consistent alpha generation.
- **Return sacrifice**: Ann. return drops from 68.97% to 43.16% on 5y — the strategy gives up roughly 26 pp of annual return to cut the drawdown in half.

## Key Insight
The Price > 200-SMA filter successfully cuts NVDA's catastrophic 2022 drawdown in half (−33% vs −66%), achieving both the MaxDD and Calmar goals on the 5-year horizon — but the strategy's edge is concentrated in that single bear-market avoidance event, and it consistently underperforms buy-and-hold on the recovery periods (3y, 2y, 1y) where NVDA's momentum dominates. This makes H2 a viable defensive overlay but one that requires conviction on multi-year holding periods.
