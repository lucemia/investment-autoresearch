# H7 Results: Price > 200-day SMA Regime Filter

## Hypothesis
Hold QQQ when Close > SMA(200), go to cash otherwise. No fast SMA needed — this is a simpler regime filter than a crossover. It fires faster on exit (as soon as price dips below the 200-day SMA, not waiting for a slow crossover) and re-enters sooner (as soon as price reclaims the 200-day). Hypothesis: fewer whipsaws than 50/200 cross AND faster exit/entry.

## Results

| Period | Ann. Return (%) | Max DD (%) | Calmar | # Trades |
|--------|----------------|------------|--------|----------|
| 5y     | 13.62          | -13.38     | 1.019  | 8        |
| 3y     | 12.11          | -13.28     | 0.913  | 4        |
| 2y     | 5.83           | -11.81     | 0.494  | 4        |
| 1y     | 7.95           | -5.40      | 1.471  | 2        |

Baseline (SmaCross_50_200): 5y Calmar 0.46, 2y Calmar 1.45

## Verdict vs Baseline: BEAT (5y) / MIXED (2y)

- **5y Calmar: 1.019 vs baseline 0.46** — decisively beats the baseline (>2x improvement)
- **2y Calmar: 0.494 vs baseline 1.45** — falls below the 1.0 floor requirement

## Key Insight

The Price > 200 SMA regime filter dramatically reduces max drawdown (-13.4% vs -20.7% for baseline) and more than doubles the 5y Calmar ratio, validating the hypothesis that direct price-vs-SMA comparison exits faster than a slow crossover. However, the 2y window captures a difficult chop period where the strategy was repeatedly stopped out near the 200-day, producing a Calmar of only 0.49 — suggesting the strategy underperforms when QQQ oscillates around its 200-day SMA rather than trending clearly above or below it.
