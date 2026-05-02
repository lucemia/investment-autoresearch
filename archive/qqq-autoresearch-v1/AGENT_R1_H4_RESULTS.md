# H4 Results: RSI Mean-Reversion Strategy (QQQ)

## Hypothesis
RSI mean-reversion (buy on oversold RSI < 30, sell on overbought RSI > 70) exploits a different market regime than trend-following and may improve risk-adjusted returns.

## Baseline
| Metric | Value |
|---|---|
| Ann. Return | 15.53% |
| Max. Drawdown | -34.22% |
| Calmar Ratio | 0.45 |

## Results Table

| Period | Ann. Return [%] | Max. Drawdown [%] | Calmar Ratio |
|--------|-----------------|-------------------|--------------|
| 5y     | 0.31            | -29.23            | 0.01         |
| 3y     | 6.53            | -20.01            | 0.33         |
| 2y     | 3.64            | -19.50            | 0.19         |
| 1y     | 11.81           | -2.94             | 4.02         |

## Verdict: MIXED

- **1y: BEAT BASELINE** — Calmar of 4.02 far exceeds the baseline 0.45. MaxDD of only -2.94% is dramatically lower than baseline's -34.22%. However, returns (11.81%) are lower than the baseline (15.53%).
- **3y/2y/5y: WORSE** — Across all longer periods, RSI mean-reversion produces much lower annualized returns (0.31%–6.53%) while only modestly reducing drawdowns. Calmar ratios (0.01–0.33) all fall well short of the 0.45 baseline.

## Key Insight

RSI mean-reversion on QQQ is highly regime-dependent. In the recent 1-year window (2025–2026), the strategy achieved an exceptional Calmar of 4.02 with near-zero drawdown — but this is based on only 2 trades, making it statistically fragile. Over longer multi-year periods, QQQ's strong secular uptrend means RSI rarely reaches oversold territory (<30), resulting in very low market exposure (10–30%), starving the strategy of returns. The strategy fundamentally underperforms BuyAndHold in trending bull markets because it sits in cash while QQQ appreciates. RSI mean-reversion is not a reliable improvement over the baseline across all periods; it may serve as a drawdown hedge in volatile/sideways regimes but sacrifices too much return in uptrending markets.
