# H3 Results — TrailingStop20 (NVDA)

## Hypothesis
Pure trailing stop at -20% from the rolling peak. NVDA has violent corrections within its uptrend. A -20% trailing stop exits when a correction gets serious, then re-enters when price makes a new 52-week high. Wider than the -8% used for QQQ to accommodate NVDA's normal volatility.

## Baseline (BuyAndHold, 5y)
- Ann. Return: 68.97%
- Max Drawdown: -66.33%
- Calmar: 1.04

## Results

| Period | Ann. Return (%) | Max DD (%) | Calmar | # Trades |
|--------|----------------|------------|--------|----------|
| 5y     | 44.75          | -28.74     | 1.557  | 5        |
| 3y     | 52.64          | -28.73     | 1.832  | 4        |
| 2y     | 6.27           | -28.57     | 0.219  | 4        |
| 1y     | 34.56          | -23.42     | 1.475  | 2        |

## Verdict vs Baseline

**BEAT** (5y primary period)

- MaxDD: -28.74% vs -66.33% baseline — reduced by more than half, well below the -40% target
- Calmar: 1.557 vs 1.04 baseline — exceeds the target of >1.04
- Both goals are met on the 5y period

## Key Insight

The -20% trailing stop dramatically cuts NVDA's catastrophic drawdown (from -66% to -29%) while still delivering a Calmar ratio of 1.56, beating the buy-and-hold baseline on a risk-adjusted basis. The 2y window underperforms (Calmar 0.22) because the strategy missed much of the 2024-2025 AI rally while sitting out after stop-outs, highlighting that the re-entry trigger (new 52-week high) can keep the strategy sidelined during sharp but ultimately recovery-prone pullbacks.
