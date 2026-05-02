# H2 Results: SmaCross 10/30 — Faster SMA Crossover

## Hypothesis

SMA 10/30 crossover (faster signals) may provide better drawdown control with more frequent trading compared to the Buy & Hold baseline.

## Backtest Results

| Period | Ann. Return (%) | Max. Drawdown (%) | Calmar |
|--------|----------------|-------------------|--------|
| 5y     | -5.06          | -34.48            | -0.15  |
| 3y     | +0.66          | -19.26            | +0.03  |
| 2y     | -1.39          | -19.22            | -0.07  |
| 1y     | +9.26          | -11.07            | +0.84  |

## Baseline (Buy & Hold)

| Ann. Return (%) | Max. Drawdown (%) | Calmar |
|----------------|-------------------|--------|
| 15.53          | -34.22            | 0.45   |

## Verdict: WORSE

SmaCross 10/30 fails to beat the baseline across all multi-year periods. Only the 1-year lookback shows a positive Calmar (0.84 vs. 0.45 baseline), but this is a single short window and ann. return of 9.26% falls far below the baseline's 15.53%.

## Key Insight

The faster 10/30 crossover generates many trades (~10–48 depending on period) but is badly hurt by **commission drag** — cumulative commissions range from $424 (1y) to $1,568 (5y) on a $10,000 portfolio. The strategy's ~43–48% win rate combined with high trading frequency produces negative expectancy in trending markets. While the 3y and 2y MaxDD (~-19%) is genuinely lower than the baseline's -34%, the dramatically reduced returns make the risk-adjusted performance worse. Faster SMA signals do reduce absolute drawdown in shorter windows, but they consistently underperform QQQ's strong secular uptrend by sitting in cash during upswings and triggering whipsaws that erode capital.
