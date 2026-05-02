# Verified Insights — QQQ

## Baseline
- Current best: SmaCross_50_200 = Ann. 9.57%, MaxDD -20.71%, Calmar 0.46 (5y); 2y Calmar 1.45
- Previous baseline: BuyAndHold = Return (Ann.) 15.53%, MaxDD -34.22%, Calmar 0.45
- Scoring command: `python3 backtest_runner.py --ticker QQQ --strategy {StrategyName} --period {period}`
- Goal: Beat Calmar > 0.46 across all periods, ideally with Ann. Return > 12%

## Round 1 Scoreboard

| Strategy | 5y Calmar | 3y Calmar | 2y Calmar | 1y Calmar | 5y Ann.Ret | 5y MaxDD |
|----------|-----------|-----------|-----------|-----------|------------|---------|
| BuyAndHold | 0.45 | — | — | — | 15.53% | -34.22% |
| **SmaCross_50_200** | **0.46** | **0.82** | **1.45** | 3.34* | 9.57% | -20.71% |
| SmaCross_20_50 | 0.29 | 0.64 | 0.65 | 4.27 | 5.22% | -18.04% |
| RsiStrategy | 0.01 | 0.33 | 0.19 | 4.02 | 0.31% | -29.23% |
| SmaCross_10_30 | -0.15 | 0.03 | -0.07 | 0.84 | -5.06% | -34.48% |

*1y result for 50/200: 0 trades triggered (sat in cash entire year) — 3.34 Calmar is misleading

## Confirmed principles
1. **Slow SMA crossovers (50/200) halve max drawdown** vs buy-and-hold (~-20% vs -34%), confirming bear market avoidance value
2. **Commission drag kills faster strategies on QQQ** — SMA 10/30 generated $424–$1,568 in fees on $10k, destroying returns in a trending asset
3. **QQQ is a strong secular uptrend — mean-reversion is structurally mismatched** — RSI <30 triggers rarely; strategy sits mostly in cash missing appreciation
4. **Slower signals = better drawdown but worse recovery** — SMA 50/200 lags on 5y return (9.57% vs 15.53%) because it's slow to reenter after bear markets
5. **1y Calmar metrics are unreliable** — small trade counts (0–2 trades) make short-window Calmars statistically noise

## Rejected approaches
1. **SMA 10/30** — whipsaws in QQQ trend, commission drag nets negative Calmar on 5y. Too fast for a momentum-driven index.
2. **RSI mean-reversion (buy<30, sell>70)** — wrong regime for QQQ. Misses secular uptrend by sitting in cash. Calmar 0.01 over 5y.

## Open hypotheses for Round 2
- H5: SMA 30/100 — intermediate speed, may balance 50/200 drawdown control with faster reentry
- H6: SMA 50/200 + trailing stop at -8% — keep golden cross for exits, add stop-loss for faster bear exit
- H7: SMA 50/200 but hold QQQ when above 200-day SMA, switch to cash only when price < 200 SMA (simpler, fewer trades than crossover)
- H8: Momentum filter — buy and hold but exit when QQQ 3-month return < 0, reenter when positive (pure momentum, no SMA)
