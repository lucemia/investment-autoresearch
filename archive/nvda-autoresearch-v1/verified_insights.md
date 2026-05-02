# Verified Insights — NVDA (v1)

## Baseline
- Current best: **TrailingStop20** = Ann. 44.75%, MaxDD -28.74%, Calmar **1.557** (5y)
- Previous baseline: BuyAndHold = Ann. 68.97%, MaxDD -66.33%, Calmar 1.04
- Scoring: `cd /Users/davidchen/repo/investment-autoresearch/examples && python3 backtest_runner.py --ticker NVDA --strategy {StrategyName} --period {period}`
- Goal: Beat Calmar > 1.557 on 5y AND hold MaxDD < -40%

## Round 1 Scoreboard

| Strategy | 5y Calmar | 3y Calmar | 2y Calmar | 1y Calmar | 5y Ann.Ret | 5y MaxDD |
|----------|-----------|-----------|-----------|-----------|------------|---------|
| **TrailingStop20** | **1.557** | **1.832** | 0.219 | 1.475 | 44.75% | **-28.74%** |
| SmaCross_50_200 | 1.795 | 0.406 | 0.623 | N/A | 50.996% | -28.41% |
| PriceAbove200Sma | 1.297 | 0.818 | 0.611 | 0.365 | 43.16% | -33.27% |
| BuyAndHold (baseline) | 1.04 | — | — | — | 68.97% | -66.33% |
| RsiOverboughtExit | 0.865 | 2.055 | 0.767 | 4.006 | 55.02% | -63.63% |

## Confirmed principles

1. **Trend filters cut NVDA's MaxDD from -66% to -28-33%** — all SMA-based approaches halved or better the max drawdown by sidestepping the 2022 bear market
2. **The 2022 bear is the key event** — every strategy's 5y edge comes almost entirely from avoiding that single -66% drawdown; 3y/2y windows (post-2022) show most strategies struggling
3. **RSI exit fires too late on secular drawdowns** — NVDA's RSI was already declining before triggering; RSI > 80 is useful in bull markets but misses crash entries
4. **Re-entry timing is the hard problem** — TrailingStop20's 2y weakness (Calmar 0.22) and H1's 1y failure (0 trades) both stem from slow/missed re-entry into NVDA's violent V-shaped recoveries
5. **52-week high re-entry is too conservative for NVDA** — kept TrailingStop20 sidelined during the 2024-2025 AI rally; needs a faster re-entry trigger
6. **SMA 50/200 crossover on NVDA: only 2 trades in 5y** — very slow signal; misses 3y/1y windows entirely but does avoid the 2022 crash cleanly

## Rejected approaches

1. **RSI overbought exit (standalone)** — fails the 5y primary benchmark (Calmar 0.87, MaxDD -63.6%); fires too late during secular bear markets. May work as a secondary filter combined with trend.

## Open hypotheses for Round 2

- H5: TrailingStop20 with faster re-entry — replace 52-week high trigger with Price > 200-day SMA reentry; keeps the -20% stop, enters sooner on recovery
- H6: SMA 50/200 + trailing stop -15% — golden cross as regime filter, tight stop for faster exit than crossover alone (adapted from QQQ H6 win)
- H7: Price > 200 SMA + RSI combo — enter when price > 200 SMA AND RSI < 60 (avoid chasing overbought entries); exit when price < 200 SMA OR RSI > 80
- H8: Trailing stop -15% — tighter than H3's -20%; test if capturing more of the downside exit is worth the extra whipsaws on NVDA
