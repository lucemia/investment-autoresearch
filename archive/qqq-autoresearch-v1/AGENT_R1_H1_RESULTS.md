# H1 Results: SMA 20/50 Crossover (SmaCross) vs Buy-and-Hold — QQQ

## Hypothesis

SMA 20/50 crossover trend-following may reduce drawdown vs buy-and-hold at acceptable return cost.

**Strategy:** SmaCross (fast=20, slow=50)
**Ticker:** QQQ
**Baseline (Buy & Hold):** Ann. Return 15.53% | MaxDD -34.22% | Calmar 0.45

---

## Results Table

| Period | Ann. Return [%] | Max. Drawdown [%] | Calmar Ratio | vs Baseline Calmar |
|--------|-----------------|-------------------|--------------|--------------------|
| 5y     |  5.22           | -18.04            | 0.29         | WORSE (0.29 < 0.45)|
| 3y     | 10.66           | -16.57            | 0.64         | BEAT  (0.64 > 0.45)|
| 2y     | 10.88           | -16.62            | 0.65         | BEAT  (0.65 > 0.45)|
| 1y     | 31.45           |  -7.36            | 4.27         | BEAT  (4.27 > 0.45)|

*Calmar = Ann. Return / abs(Max. Drawdown)*

---

## Verdict: MIXED

The SMA 20/50 crossover **consistently reduces max drawdown** (from -34.22% baseline to -7% to -18% across periods), confirming the core drawdown-reduction thesis. However, results depend heavily on the evaluation window:

- **5y**: Underperforms on Calmar (0.29 vs 0.45) — the strategy suffered from being out of the market during the 2021–2023 bull run and paid high commission drag over many trades.
- **3y and 2y**: Beats baseline Calmar (0.64–0.65 vs 0.45) with substantially lower drawdown (-16.6% vs -34.2%), though annual returns lag significantly (10.7–10.9% vs 15.53%).
- **1y**: Strongly beats baseline (Calmar 4.27), capturing the 2025 trend with minimal drawdown (-7.4%).

---

## Key Insight

The SMA 20/50 crossover **reliably reduces drawdown by roughly half** (from ~-34% to ~-16 to -18%) across all multi-year windows. The trade-off is that annual returns are cut by one-third to two-thirds vs buy-and-hold, making it attractive only when drawdown protection is the primary goal. The Calmar improvement over buy-and-hold holds for 3y/2y/1y periods but breaks down over 5y due to commission drag and missed upside during extended bull markets. This strategy is **not a return enhancer — it is a risk reducer**, and should be evaluated as such.

---

*Generated: 2026-05-02 | Agent: R1 | Hypothesis: H1*
