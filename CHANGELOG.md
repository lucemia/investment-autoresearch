# Changelog

## [1.0.0] — 2026-05-02

Initial release.

### Skills
- `investment-autoresearch:autoresearch` — core parallel loop (two-question onboarding, baseline, agents, insights, reset)
- `investment-autoresearch:parse` — walk-forward backtests across 1y/2y/3y/5y, produces `autoresearch_result.json`
- `investment-autoresearch:report` — structured markdown report from `autoresearch_result.json`
- `investment-autoresearch:strategy-chart` — 3-panel matplotlib chart with optional Slack/Discord upload

### Examples
- QQQ demo archive: two sessions, 8 strategies, Calmar 0.45 → 1.02
- `examples/strategies/qqq/` — 9 strategies (BuyAndHold, SmaCross variants, PriceAbove200Sma, MomentumFilter3M, etc.)
- `backtest_runner.py` — single-command backtest runner used by agents internally
