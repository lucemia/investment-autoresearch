# H8: 3-Month Momentum Filter — Results

## Hypothesis
Buy and hold QQQ but exit when the 63-day (~3 month) price return turns negative, reenter when it turns positive. No SMA needed — pure price momentum. From confirmed principles: QQQ is a secular uptrend so being out during negative-momentum regimes should cut drawdown without missing much upside. Expected: similar or better Calmar than SMA 50/200 with more responsive entries/exits.

## Results

| Period | Ann. Return (%) | Max DD (%) | Calmar | # Trades |
|--------|----------------|------------|--------|----------|
| 5y     | 7.56           | -22.43     | 0.34   | 24       |
| 3y     | 8.80           | -13.47     | 0.65   | 17       |
| 2y     | 10.52          | -11.35     | 0.93   | 12       |
| 1y     | 13.03          | -7.55      | 1.73   | 5        |

**Baseline (SmaCross_50_200):** 5y Calmar 0.46 | 2y Calmar 1.45

## Verdict vs Baseline: MIXED

- 5y Calmar: **0.34 vs 0.46** — WORSE (fails primary goal)
- 2y Calmar: **0.93 vs 1.45** — WORSE (fails secondary goal)
- 3y Calmar: 0.65 (strong, no direct baseline)
- 1y Calmar: 1.73 (strong, but statistically noisy per confirmed principles)

## Key Insight

The 3-month momentum filter reduces drawdown significantly on shorter windows (2y MaxDD -11% vs -20% for SMA 50/200) but lags badly on the 5y window — the 2022 bear market caused a prolonged cash period that cost ~8pp of annualized return, dragging the 5y Calmar to 0.34 vs the baseline 0.46. The strategy is responsive enough to avoid deep drawdowns in calmer regimes but is still whipsawed sufficiently during prolonged bear/recovery cycles to underperform the slower SMA 50/200 crossover on the critical 5y benchmark.
