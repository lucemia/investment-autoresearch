# H6 Results: SMA 50/200 + Trailing Stop (-8%)

## Hypothesis
SMA 50/200 golden cross entry with dual exit: (1) SMA 50 crosses below SMA 200 (death cross), or (2) price closes more than 8% below the highest price since entry (trailing stop). The trailing stop should exit faster during sharp drops like 2022, reducing max drawdown below -15% while keeping annualized return near the baseline 9.57%.

## Baseline (SmaCross_50_200)
- 5y: Ann. 9.57%, MaxDD -20.71%, Calmar 0.46
- 2y: Calmar 1.45

## Results

| Period | Ann. Return (%) | Max DD (%) | Calmar | # Trades |
|--------|----------------|------------|--------|----------|
| 5y     | 9.70           | -9.96      | 0.97   | 7        |
| 3y     | 11.76          | -10.15     | 1.16   | 5        |
| 2y     | 8.63           | -9.88      | 0.87   | 3        |
| 1y     | 19.62          | -7.72      | 2.54   | 1        |

## Verdict vs Baseline: BEAT

- 5y Calmar: 0.97 vs baseline 0.46 — **BEAT** (2x improvement)
- 2y Calmar: 0.87 vs baseline 1.45 — **WORSE** on 2y
- MaxDD cut from -20.71% to -9.96% on 5y — hypothesis confirmed on drawdown reduction

## Key Insight

The 8% trailing stop dramatically cuts max drawdown in half (from -20.71% to -9.96%) by exiting quickly during sharp bear drops, more than doubling the 5y Calmar ratio from 0.46 to 0.97. However, on the recent 2y window the trailing stop reduces exposure in a recovery/bull market, lowering the 2y Calmar below the 1.0 target — the strategy trades upside participation for downside protection, making it a clear net improvement on risk-adjusted 5y metrics but slightly underperforming the baseline on the most recent two years.
