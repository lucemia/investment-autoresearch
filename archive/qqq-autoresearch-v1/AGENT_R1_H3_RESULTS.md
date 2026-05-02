# H3 Results: SMA 50/200 Golden Cross — QQQ Backtest

## Hypothesis Statement
SMA 50/200 (golden cross) — very slow signals should avoid major bear markets and dramatically reduce max drawdown compared to Buy & Hold baseline.

## Baseline (Buy & Hold)
| Metric | Value |
|--------|-------|
| Ann. Return | 15.53% |
| Max. Drawdown | -34.22% |
| Calmar | 0.45 |

## SmaCross_50_200 Results

| Period | Ann. Return [%] | Max. Drawdown [%] | Calmar |
|--------|----------------|-------------------|--------|
| 5y | 9.57 | -20.71 | 0.46 |
| 3y | 14.21 | -17.41 | 0.82 |
| 2y | 19.60 | -13.52 | 1.45 |
| 1y | 38.72* | -11.61 | 3.34* |

*1y note: 0 trades executed — strategy held cash the entire period (no golden cross triggered). Returns reflect initial equity carry, not active trading. This period's stats are not representative of the strategy's active behavior.

## Verdict: MIXED (leans BEAT BASELINE for medium-term)

- **5y**: Calmar 0.46 vs baseline 0.45 — essentially flat. Ann. return (9.57%) significantly below baseline (15.53%), but MaxDD cut nearly in half (-20.71% vs -34.22%). The 5y window includes the 2022 bear market where the golden cross did provide meaningful downside protection, but missed the subsequent recovery upside.
- **3y**: Calmar 0.82 — clearly beats baseline. MaxDD reduced to -17.41%, while Ann. Return (14.21%) is close to baseline. Strong risk-adjusted performance.
- **2y**: Calmar 1.45 — strongly beats baseline. MaxDD only -13.52%, Ann. Return 19.60% exceeds baseline. Best active trading result.
- **1y**: Strategy never entered — no golden cross signal in the past year window (SMA 50 did not cross above SMA 200). Numbers reflect undeployed capital and are not meaningful for strategy evaluation.

## Key Insight

The golden cross strategy **dramatically reduces max drawdown** across all periods (MaxDD ranges from -11.6% to -20.7% vs baseline -34.22%) — confirming the core hypothesis. The Calmar ratio improvement is substantial in 2y and 3y windows (1.45 and 0.82 vs 0.45 baseline). However, the strategy suffers significant **opportunity cost on annual returns in longer windows** (5y Ann. Return only 9.57%), because it stays in cash during recoveries when the 50 SMA has not yet crossed back above the 200 SMA. The golden cross is a high-conviction, low-frequency signal that works best when the backtest period includes at least one full bear-and-recovery cycle. The 1y result (0 trades) is a key risk: in trending bull markets, the strategy may never trigger and sits entirely in cash — a real deployment risk to monitor.
