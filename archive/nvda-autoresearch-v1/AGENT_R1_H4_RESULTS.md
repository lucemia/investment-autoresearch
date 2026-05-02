# H4: RSI Overbought Exit Filter — Results

## Hypothesis
RSI overbought exit filter — unlike QQQ where RSI rarely hits extremes, NVDA regularly reaches RSI > 80 before major corrections. Sell when RSI(14) > 80, re-enter when RSI(14) < 50. This is not mean-reversion — it's using RSI as an overextension warning for a momentum stock.

**Baseline (BuyAndHold, 5y):** Ann. 68.97%, MaxDD -66.33%, Calmar 1.04

---

## Results

| Period | Ann. Return | MaxDD    | Calmar | # Trades |
|--------|-------------|----------|--------|----------|
| 5y     | 55.02%      | -63.63%  | 0.865  | 5        |
| 3y     | 75.57%      | -36.77%  | 2.055  | 3        |
| 2y     | 28.08%      | -36.62%  | 0.767  | 2        |
| 1y     | 80.44%      | -20.08%  | 4.006  | 2        |

---

## Verdict vs Baseline: MIXED

- **5y (primary benchmark): WORSE** — MaxDD barely improved (-63.6% vs -66.3%), Calmar dropped from 1.04 to 0.87. The strategy did not sidestep the 2022 drawdown effectively enough.
- **3y/1y: BEAT** — Over shorter recent windows the RSI exit works well; 3y Calmar 2.05 and 1y Calmar 4.01 both clearly beat the baseline, and 3y MaxDD of -36.8% breaks through the -40% target.

---

## Key Insight

The RSI > 80 exit filter is genuinely useful in NVDA's recent bull phase (2023–2026) where it reduces MaxDD to -36.8% with Calmar 2.05 over 3y, but the 5y picture is dominated by the 2022 bear market — NVDA's RSI was already falling hard before hitting 80, so the signal fired too late to prevent that catastrophic drawdown. The strategy works as a "top trimmer" but needs an additional regime or trend filter to handle secular bear moves.
