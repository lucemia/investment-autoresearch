---
name: autoresearch-report
description: Use when generating a structured markdown report from an autoresearch_result.json file for a given ticker. Triggered when user asks for a report, summary, or writeup of autoresearch results.
---

# Autoresearch Report

Generates a structured markdown report from `archive/{ticker}-autoresearch-v{N}/autoresearch_result.json`.

## Input

Read the JSON file for the requested ticker:
```
archive/{ticker}-autoresearch-v{N}/autoresearch_result.json
```

If no version is specified, use the latest `v{N}` directory. If the JSON doesn't exist, run the `autoresearch-parse` skill first.

## Report Template

Fill each section from the JSON fields below. Omit a row/field only if the value is `null`.

---

```markdown
# {ticker} Autoresearch Report

## Strategy Identity

| Field | Value |
|---|---|
| Ticker | {ticker} |
| Champion Strategy | {current_best.strategy_name} |
| Parameters | {current_best.parameters as key=value pairs} |

## Performance Summary

| Metric | Value |
|---|---|
| CAGR | {current_best.cagr}% |
| Max Drawdown | {current_best.max_drawdown}% |
| Sharpe | {current_best.sharpe ?? —} |
| Trades | {leaderboard[0].trades} |
| Trades / Parameter | {leaderboard[0].trades_per_param ?? —} |

## Risk-Adjusted Validation

Walk-forward RA = CAGR / |MaxDD| across rolling periods:

| Period | CAGR | RA |
|---|---|---|
| 5y | {walk_forward.5y.cagr ?? —} | {walk_forward.5y.ra ?? —} |
| 3y | {walk_forward.3y.cagr ?? —} | {walk_forward.3y.ra ?? —} |
| 2y | {walk_forward.2y.cagr ?? —} | {walk_forward.2y.ra ?? —} |
| 1y | {walk_forward.1y.cagr ?? —} | {walk_forward.1y.ra ?? —} |

**Min RA across periods: {current_best.min_ra_across_periods}**
_(Lower bound on risk-adjusted return; guards against period-specific overfitting)_

## Research Process

- **Rounds completed:** {research_summary.rounds_completed}
- **Agents run:** {research_summary.agents_run}
- **Strategies tested:** {research_summary.strategies_tested ?? unknown}

### Verified Insights

{verified_insights as numbered list}

### Rejected Approaches

| Approach | Why It Failed |
|---|---|
{rejected_approaches as table rows: approach | reason}

## Top Strategies Leaderboard

| Rank | Strategy | CAGR | MaxDD | Calmar | Trades |
|---|---|---|---|---|---|
{leaderboard rows}

## Recommendations

- **Graduate to production:** {recommendation.graduate}
- **Confidence:** {recommendation.confidence}

### Open Hypotheses

{open_hypotheses as numbered list}
```

---

## Field Mapping

| Report Section | JSON Path |
|---|---|
| Ticker | `ticker` |
| Champion name | `current_best.strategy_name` |
| Parameters | `current_best.parameters` |
| CAGR | `current_best.cagr` |
| Max Drawdown | `current_best.max_drawdown` |
| Sharpe | `current_best.sharpe` |
| Walk-forward table | `current_best.walk_forward` |
| Min RA | `current_best.min_ra_across_periods` |
| Rounds | `research_summary.rounds_completed` |
| Agents | `research_summary.agents_run` |
| Strategies tested | `research_summary.strategies_tested` |
| Verified insights | `verified_insights[]` |
| Rejected approaches | `rejected_approaches[].approach` + `.reason` |
| Leaderboard | `leaderboard[]` |
| Graduate recommendation | `recommendation.graduate` |
| Confidence | `recommendation.confidence` |
| Open hypotheses | `open_hypotheses[]` |

## Benchmark Comparison

The JSON does not store buy-and-hold figures. If needed, note the period CAGR of the ticker from yfinance and compute manually. Leave section out if no data available.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Showing `null` in the report | Replace with `—` for missing values |
| Omitting walk-forward table when all values are null | Include table but note "walk-forward not yet run" |
| Using `leaderboard[0]` trade count when leaderboard is empty | Fall back to `current_best` trades field |
| Rendering parameters dict as `{...}` | Format as `key=value, key=value` pairs |
