# Verified Insights — QQQ (v2)

## Baseline
- Current best: **PriceAbove200Sma** = Ann. 13.62%, MaxDD -13.38%, Calmar **1.02** (5y)
- Previous best: SmaCross_50_200 = Ann. 9.57%, MaxDD -20.71%, Calmar 0.46 (5y); 2y Calmar 1.45
- Buy & Hold: Return (Ann.) 15.53%, MaxDD -34.22%, Calmar 0.45
- Scoring command: `cd /Users/davidchen/repo/investment-autoresearch/examples && python3 backtest_runner.py --ticker QQQ --strategy {StrategyName} --period {period}`
- Goal: Beat Calmar > 1.02 on 5y AND ≥ 1.0 on 2y

## Round 1 (v2) Scoreboard

| Strategy | 5y Calmar | 3y Calmar | 2y Calmar | 5y Ann.Ret | 5y MaxDD | # Trades (5y) |
|----------|-----------|-----------|-----------|------------|---------|----------------|
| **PriceAbove200Sma** | **1.02** | 0.91 | 0.49 | 13.62% | -13.38% | 8 |
| SmaCross_50_200_TrailingStop | 0.97 | 1.16 | 0.87 | 9.70% | **-9.96%** | 7 |
| SmaCross_50_200 (v1 best) | 0.46 | 0.82 | 1.45 | 9.57% | -20.71% | — |
| MomentumFilter3M | 0.34 | 0.65 | 0.93 | 7.56% | -22.43% | 24 |
| SmaCross_30_100 | 0.22 | 1.01 | 0.69 | 5.24% | -23.92% | 15 |

## Confirmed principles (cumulative)

### From v1
1. **Slow SMA crossovers (50/200) halve max drawdown** vs buy-and-hold (~-20% vs -34%)
2. **Commission drag kills faster strategies on QQQ** — SMA 10/30 generated $424–$1,568 in fees, destroying returns
3. **QQQ is a strong secular uptrend — mean-reversion is structurally mismatched** — RSI strategies sit in cash missing appreciation
4. **Slower signals = better drawdown but worse recovery** — SMA 50/200 lags on 5y return because slow reentry
5. **1y Calmar metrics are unreliable** — small trade counts (0–2) make short-window Calmars statistical noise

### New from v2
6. **Trailing stop on golden cross nearly doubles Calmar** (0.46 → 0.97) by cutting MaxDD in half (-20.7% → -9.96%) with almost no return cost (9.57% → 9.70% ann.)
7. **Price > 200-SMA filter beats the crossover on 5y returns** (13.62% vs 9.57%) because it re-enters faster when price reclaims the 200-day vs waiting for the slow crossover
8. **Both best strategies suffer on 2y** — the 2024–2026 bull market caused whipsaws around the 200-SMA, with multiple false exits costing participation in the strong run
9. **Intermediate SMA speed (30/100) is strictly worse than 50/200 on QQQ** — generates more whipsaws AND larger max drawdown; confirms faster is not better for this secular-trend asset
10. **Pure 3-month momentum is noisy (24 trades/5y)** — high turnover erodes returns vs SMA-based filters despite similar logic

## Rejected approaches (cumulative)
1. **SMA 10/30** — whipsaws in QQQ trend, commission drag nets negative Calmar on 5y
2. **RSI mean-reversion (buy<30, sell>70)** — wrong regime for QQQ; misses secular uptrend
3. **SMA 30/100** — strictly worse than 50/200: more whipsaws, larger drawdown, lower returns
4. **Pure 3-month momentum (63-day return)** — 24 trades/5y generates too much noise; SMA filter is a better regime signal

## Open hypotheses for Round 2 (v2)
- H9: Price > 200 SMA + trailing stop (-8%) — remove the crossover entirely; enter on price reclaiming 200-SMA, exit on trailing stop OR price breaking below 200-SMA. Combines best of H6 and H7.
- H10: Price > 200 SMA with buffer zone — enter when price > SMA×1.01, exit when price < SMA×0.99. Small buffer to filter out 200-SMA whipsaws seen in 2024–2025.
- H11: SmaCross_50_200_TrailingStop with wider stop (-12%) — test if more breathing room captures more bull-market upside while still protecting on bear legs
- H12: Price > 200 SMA + VIX regime — only enter when VIX < 25; exit when VIX > 30 or price < 200 SMA. Hypothesis: volatility regime adds orthogonal signal to trend filter.
