---
name: investment-autoresearch-parse
description: Use when converting autoresearch markdown results (verified_insights.md and AGENT_R*_RESULTS.md) into structured JSON for reporting or slides generation.
---

# Autoresearch Parse

Extracts structured JSON from autoresearch markdown outputs for a given ticker, then **always runs walk-forward backtests** to populate authoritative numeric values.

## Two-Phase Process

```
Phase 1: Parse markdown → text fields (strategy name, insights, rejections, hypotheses)
Phase 2: Run your backtest command → numeric fields (cagr, max_drawdown, walk_forward RA)
```

**Never trust markdown numbers for `cagr` or `max_drawdown`.** Agents write `Return [%]` (total return) and `Return (Ann.) [%]` (CAGR) interchangeably. Only backtesting gives the authoritative annualized CAGR.

## Input Files

For a given ticker, two file types exist under `archive/{ticker}-autoresearch-v{N}/`:

| File | Contains |
|---|---|
| `verified_insights.md` | Cumulative state: current best, insights, rejections, open hypotheses |
| `AGENT_R{N}_RESULTS.md` | Per-round: hypothesis, results table, key learnings |

## Output JSON Schema

```json
{
  "ticker": "SOXL",
  "research_summary": {
    "rounds_completed": 40,
    "agents_run": 42,
    "strategies_tested": 630
  },
  "current_best": {
    "strategy_name": "R15 W7 + min hold 10 days",
    "parameters": {},
    "cagr": 104.5,
    "max_drawdown": -31.8,
    "sharpe": null,
    "robustness_score": 0.710,
    "walk_forward": {
      "5y": { "cagr": 104.5, "ra": 5.86 },
      "3y": { "cagr": 98.2,  "ra": 5.51 },
      "2y": { "cagr": 110.3, "ra": 6.19 },
      "1y": { "cagr": 88.7,  "ra": 4.98 }
    },
    "min_ra_across_periods": 4.98
  },
  ...
}
```

`cagr` and all `walk_forward` values come from **Phase 2 backtesting**, not markdown parsing.

## Phase 1 — Parse Markdown

### `ticker`
From the `verified_insights.md` header line: `# Verified Insights — {TICKER} ...`

### `research_summary`
- `rounds_completed`: "after N rounds" or count of AGENT_R*_RESULTS.md files
- `strategies_tested`: "N+ strategies evaluated across N rounds"
- `agents_run`: same as `rounds_completed` unless stated otherwise

### `current_best` (text fields only)
Prefer the risk-adjusted / lowest MaxDD champion:
- `strategy_name`: bolded strategy label
- `parameters`: extract from markdown if listed; else `{}`
- Leave `cagr`, `max_drawdown`, `walk_forward` as `null` — Phase 2 will fill them

### `leaderboard`
From `## Current Best` section — ranked strategies with scores. `cagr`/`max_drawdown` here come from markdown (acceptable for leaderboard display, but not used for `current_best` numeric fields).

### `verified_insights`
From `## Confirmed principles` — each item → one string. Strip leading number and bold markers.

### `rejected_approaches`
From `## Rejected Approaches`. Each → `{ "approach": "...", "reason": "..." }`. Fall back to `REJECT` rows in AGENT_R*_RESULTS.md if no explicit section.

### `open_hypotheses`
From `## Remaining hypotheses` or `## Open Hypotheses`.

### `recommendation`
- `graduate`: strategy name from explicit recommendation or "By risk-adjusted" section
- `confidence`: derive from walk-forward consistency after Phase 2 completes

## Phase 2 — Run Walk-Forward Backtests

Run your configured backtest command across four rolling periods to populate authoritative numeric values. Your backtest command must output lines containing `Return (Ann.) [%]` and `Max. Drawdown [%]` — this is the native output format of Backtesting.py; adapt your runner if using a different framework.

### Configure your backtest command

In your project, you need a CLI command that:
1. Accepts a ticker and strategy class name as arguments
2. Runs a backtest for the requested period
3. Prints output containing these two lines:

```
Return (Ann.) [%]     <value>
Max. Drawdown [%]     <value>
```

Example with Backtesting.py (native format, no adaptation needed):
```bash
python backtest_runner.py --ticker SOXL --strategy MyStrategy --period 5y
```

Example minimal runner if you need to build one:
```python
# backtest_runner.py
import argparse
from backtesting import Backtest
# ... import your strategy ...

parser = argparse.ArgumentParser()
parser.add_argument("--ticker")
parser.add_argument("--strategy")
parser.add_argument("--period", default="5y")
args = parser.parse_args()

# load data, run backtest, print stats
bt = Backtest(data, StrategyClass)
stats = bt.run()
print(stats)  # Backtesting.py prints Return (Ann.) [%] and Max. Drawdown [%] natively
```

### Step 1 — Find the strategy Python class name

Replace `<YOUR_STRATEGY_DIR>` with your actual strategy directory path (e.g. `src/strategies/`, `strategies/`, `my_app/trading/`):

```bash
grep -rn "class.*{strategy_name_keywords}" <YOUR_STRATEGY_DIR>/{ticker}/
```

### Step 2 — Run across four periods

```bash
YOUR_BACKTEST_COMMAND --ticker {TICKER} --strategy {ClassName} --period 5y
YOUR_BACKTEST_COMMAND --ticker {TICKER} --strategy {ClassName} --period 3y
YOUR_BACKTEST_COMMAND --ticker {TICKER} --strategy {ClassName} --period 2y
YOUR_BACKTEST_COMMAND --ticker {TICKER} --strategy {ClassName} --period 1y
```

Parse `Return (Ann.) [%]` from each run as `cagr`, and `Max. Drawdown [%]` as `max_drawdown`.
Compute `ra = cagr / abs(max_drawdown)` for each period.
Set `min_ra_across_periods` to the minimum RA across all four periods.

### Step 3 — Verify the JSON was updated

```bash
python3 -c "
import json
with open('archive/{ticker}-autoresearch-v{N}/autoresearch_result.json') as f:
    d = json.load(f)
cb = d['current_best']
print('CAGR:', cb['cagr'])
print('MaxDD:', cb['max_drawdown'])
print('Min RA:', cb['min_ra_across_periods'])
for p, v in cb['walk_forward'].items():
    print(f'  {p}: cagr={v[\"cagr\"]} ra={v[\"ra\"]}')
"
```

All walk_forward values should be non-null.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using markdown `Return [%]` as `cagr` | That is total return, not annualized. Always use Phase 2. |
| Skipping Phase 2 because "numbers are already in the markdown" | Markdown numbers are untrustworthy. Run the backtest. |
| Backtest command doesn't print `Return (Ann.) [%]` | Check your runner outputs Backtesting.py-style stats; total return ≠ annualized CAGR |
| Using total return instead of annualized CAGR | Parse `Return (Ann.) [%]` not `Return [%]` |
| Using score-based "best" instead of risk-adjusted | Prefer lowest MaxDD / highest Calmar as `current_best`. |
| Conflating rounds with agents | They are equal unless file explicitly states resets/reruns. |
