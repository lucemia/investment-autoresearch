# Demo Walkthrough — QQQ Autoresearch (v1 + v2)

A complete end-to-end example of the autoresearch loop applied to QQQ. Two sessions, 8 strategies tested, showing how the loop finds signal and iterates.

---

## What this demo covers

- Setting up the backtest runner and baseline
- Running parallel agents (4 at a time)
- Reading results and updating insights
- How the loop compounds across sessions

---

## Setup

### Prerequisites

```bash
pip install backtesting yfinance
```

Copy the example runner into your project:

```bash
PLUGIN=~/.claude/plugins/cache/lucemia/investment-autoresearch
cp $PLUGIN/examples/backtest_runner.py your-project/
cp -r $PLUGIN/examples/strategies/ your-project/strategies/
```

Verify it works:

```bash
cd your-project
python3 backtest_runner.py --ticker QQQ --strategy BuyAndHold --period 5y
```

Expected output (approximate):

```
Return (Ann.) [%]    15.31
Max. Drawdown [%]    -34.22
```

### Project structure after setup

```
your-project/
├── backtest_runner.py          ← copied from plugin
├── strategies/
│   └── qqq/
│       ├── __init__.py
│       └── BuyAndHold.py       ← starting point
└── archive/                    ← created by autoresearch skill
```

---

## Session v1 — Broad exploration

**Trigger:** `/autoresearch` in Claude Code

**Ticker:** QQQ  
**Goal:** Higher returns (user answered Q2: "higher returns")  
**Session folder:** `archive/qqq-autoresearch-v1/`

### Baseline

```
BuyAndHold — 5y results:
  Return (Ann.): 15.53%
  Max. Drawdown: -34.22%
  Calmar:         0.45
```

### Hypotheses tested (Round 1, v1)

Four strategies ran in parallel — one agent per hypothesis:

| Hypothesis | Strategy | 5y Calmar | 5y Ann.Ret | 5y MaxDD |
|------------|----------|-----------|------------|---------|
| H1: Slow SMA crossover | SmaCross_50_200 | **0.46** | 9.57% | -20.71% |
| H2: Medium SMA crossover | SmaCross_20_50 | 0.29 | 5.22% | -18.04% |
| H3: RSI mean-reversion | RsiStrategy | 0.01 | 0.31% | -29.23% |
| H4: Fast SMA crossover | SmaCross_10_30 | -0.15 | -5.06% | -34.48% |

### Key findings from v1

1. **Drawdown protection works** — SMA 50/200 cuts max drawdown from -34% to -21% by avoiding the 2022 bear market
2. **Commission drag kills faster strategies** — SMA 10/30 went negative; fees on $10k capital wiped out any edge
3. **Mean-reversion is wrong for QQQ** — RSI strategies sit in cash while QQQ trends up; Calmar 0.01
4. **Speed spectrum confirmed** — faster signal = more whipsaws on a trending asset

**New best:** SmaCross_50_200 (Calmar 0.46)  
**Session files:** `archive/qqq-autoresearch-v1/`

---

## Session v2 — Deeper on winners

The loop promoted SmaCross_50_200 as the new baseline and seeded 4 new hypotheses targeting the known weaknesses: slow reentry, large drawdown.

**Session folder:** `archive/qqq-autoresearch-v2/`  
**New target:** Calmar > 0.46 on 5y AND ≥ 1.0 on 2y

### Hypotheses tested (Round 1, v2)

All 4 agents ran in parallel, completing in ~45 seconds each:

| Hypothesis | Strategy | 5y Calmar | 2y Calmar | 5y Ann.Ret | 5y MaxDD | Verdict |
|------------|----------|-----------|-----------|------------|---------|---------|
| H5: Intermediate SMA speed | SmaCross_30_100 | 0.22 | 0.69 | 5.24% | -23.92% | WORSE |
| H6: Golden cross + trailing stop | SmaCross_50_200_TrailingStop | **0.97** | 0.87 | 9.70% | **-9.96%** | BEAT 5y |
| H7: Price > 200 SMA regime | PriceAbove200Sma | **1.02** | 0.49 | **13.62%** | -13.38% | BEAT 5y |
| H8: 3-month momentum | MomentumFilter3M | 0.34 | 0.93 | 7.56% | -22.43% | WORSE |

### Key findings from v2

1. **H6 cuts max drawdown from -20.7% → -9.96%** with negligible return cost — the -8% trailing stop fires before the slow 50/200 crossover during sharp sell-offs
2. **H7 more than doubles the ann. return** (9.57% → 13.62%) because price reclaims the 200-day SMA faster than the 50-day crosses it
3. **Both H6 and H7 struggle on 2y** — 2024–2026 was a whipsaw environment near the 200-SMA, causing repeated false exits
4. **Intermediate SMA (30/100) still worse** — confirms faster signals are structurally bad for QQQ regardless of speed
5. **Pure momentum is noisy** — 24 trades/5y vs 7 for the best strategy; high turnover erodes edge

**New best:** PriceAbove200Sma (5y Calmar 1.02, 5y Return 13.62%, MaxDD -13.38%)

### Cumulative progress

```
Session    Best Strategy              5y Calmar   5y MaxDD
v1         SmaCross_50_200            0.46        -20.71%
v2         PriceAbove200Sma           1.02        -13.38%
           (SmaCross_50_200_TS also)  0.97        -9.96%
```

In two sessions, 5y Calmar went from 0.45 (buy-and-hold) → 0.46 → **1.02**. Max drawdown went from -34% → -21% → **-13%**.

---

## How to read the archive

```
archive/
└── qqq-autoresearch-v2/
    ├── verified_insights.md         ← cumulative state: baseline, insights, rejections, next hypotheses
    ├── AGENT_R1_H5_RESULTS.md       ← H5 result (SmaCross_30_100)
    ├── AGENT_R1_H6_RESULTS.md       ← H6 result (SmaCross_50_200_TrailingStop)
    ├── AGENT_R1_H7_RESULTS.md       ← H7 result (PriceAbove200Sma)
    └── AGENT_R1_H8_RESULTS.md       ← H8 result (MomentumFilter3M)
```

`verified_insights.md` is the state machine — it carries forward every confirmed principle and rejected approach, and lists the next hypotheses. Read it to understand why each strategy was tried.

---

## Next steps (Round 2, v2)

Four hypotheses ready to test in the next `/autoresearch` call:

| Hypothesis | Key idea |
|------------|----------|
| H9: Price > 200 SMA + trailing stop | Merge H6 and H7 — faster entry, fast exit |
| H10: Price > 200 SMA with buffer | ±1% buffer to suppress 2024–2025 whipsaws |
| H11: Trailing stop widened to -12% | More bull market participation |
| H12: Price > 200 SMA + VIX regime | Add orthogonal volatility signal |

---

## Strategy reference

All strategies are in `examples/strategies/qqq/`. Each file contains one class matching the filename:

| File | Description |
|------|-------------|
| `BuyAndHold.py` | Buy on day 1, hold forever |
| `SmaCross_50_200.py` | Golden cross — buy when SMA50 > SMA200 |
| `SmaCross_30_100.py` | Intermediate crossover (v2 reject) |
| `SmaCross_10_30.py` | Fast crossover (v1 reject) |
| `SmaCross_20_50.py` | Medium crossover (v1 reject) |
| `RsiStrategy.py` | RSI mean-reversion (v1 reject) |
| `SmaCross_50_200_TrailingStop.py` | Golden cross + -8% trailing stop |
| `PriceAbove200Sma.py` | Hold when price > 200-day SMA |
| `MomentumFilter3M.py` | Hold when 63-day return > 0 |

Run any strategy manually:

```bash
cd examples
python3 backtest_runner.py --ticker QQQ --strategy PriceAbove200Sma --period 5y
python3 backtest_runner.py --ticker QQQ --strategy PriceAbove200Sma --period 2y
```

---

## Lessons for other tickers

From this QQQ run:

- **Start with BuyAndHold as baseline** — know what you're trying to beat before launching agents
- **Walk-forward validation matters** — strategies that look good on 5y often fall apart on 2y (different market regime)
- **One hypothesis per agent** — agents with multiple hypotheses dilute focus and produce harder-to-interpret results
- **Record rejections explicitly** — H5 (SMA 30/100) taught us that intermediate speed is still wrong, ruling out a whole class of future hypotheses
- **Two sessions is often enough to 2× Calmar** — this run went 0.45 → 1.02 in 8 total backtests
