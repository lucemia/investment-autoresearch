# H1 Results: SMA 50/200 Golden Cross — NVDA

## Hypothesis
Buy when SMA(50) crosses above SMA(200) (golden cross); sell when SMA(50) crosses below SMA(200) (death cross). This approach avoided the 2022 bear market on QQQ by exiting before the deep drawdown. Test whether it similarly limits NVDA's -66% max drawdown.

## Baseline (BuyAndHold, 5y)
- Ann. Return: 68.97% | MaxDD: -66.33% | Calmar: 1.04 | Goal: MaxDD < -40% AND Calmar > 1.04

## Results

| Period | Ann. Return | MaxDD    | Calmar | # Trades |
|--------|-------------|----------|--------|----------|
| 5y     | 50.996%     | -28.41%  | 1.795  | 2        |
| 3y     | 8.207%      | -20.21%  | 0.406  | 1        |
| 2y     | 12.586%     | -20.21%  | 0.623  | 1        |
| 1y     | 0.0%        | -0.0%    | N/A    | 0        |

## Verdict vs Baseline: MIXED

- **5y period: BEAT** — MaxDD crushed from -66.33% to -28.41% (well under the -40% target), and Calmar improved from 1.04 to 1.795. Both goals met.
- **3y / 2y periods: WORSE** — Strategy was mostly out of the market (1 trade, low exposure ~28-42%), capturing only the tail end of the NVDA AI rally. Calmar well below 1.04.
- **1y period: N/A** — No crossover signal fired; strategy sat in cash the entire year, missing a +5.6% buy-and-hold return.

## Key Insight
The SMA 50/200 crossover successfully avoided NVDA's catastrophic 2022 bear market on the 5-year window, cutting MaxDD by more than half and exceeding the Calmar target. However, the strategy's long lag (SMA200 requires ~200 days of warmup and is slow to re-trigger) caused it to miss most of the 2023-2025 AI bull run in shorter windows, resulting in poor risk-adjusted returns outside the 5y frame.
