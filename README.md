# investment-autoresearch

A Claude Code plugin for trading strategy research via parallel agent experimentation.

Inspired by [Ryan Li's Paradigm Hackathon methodology](https://x.com/ryanli_me) — 1,039 variants tested across 8–20 parallel agents with periodic resets.

## What it does

Runs a structured search loop over trading strategy variants:

1. Establish a baseline score
2. Seed hypotheses into `verified_insights.md`
3. Launch 5–10 parallel agents, each testing ONE hypothesis in an isolated git worktree
4. Collect results, update insights, decide: explore more or reset
5. When stuck, spawn a fresh agent that reads only `verified_insights.md` — no existing code

The reset step is the key move. Existing code anchors thinking. Fresh agents find architectures incremental optimization cannot reach.

## Skills

| Skill | Trigger | Description |
|---|---|---|
| `investment-autoresearch` | `/autoresearch` | Core parallel loop — baseline → agents → insights → repeat |
| `investment-autoresearch-parse` | `/autoresearch-parse` | Parse agent results into structured JSON + walk-forward backtests |
| `investment-autoresearch-report` | `/autoresearch-report` | Generate a markdown report from `autoresearch_result.json` |
| `investment-autoresearch-strategy-chart` | `/autoresearch-strategy-chart` | Generate matplotlib strategy chart; upload to Slack, Discord, or save locally |

## Prerequisites

- [Claude Code](https://claude.ai/code)
- git 2.5+ (required for isolated worktrees)
- Python 3.9+ with `backtesting` and `yfinance` installed
- A CLI backtest command that outputs `Return (Ann.) [%]` and `Max. Drawdown [%]`
- Optional: Slack or Discord bot token for chart uploads

## Installation

```bash
claude plugin install gh:lucemia/investment-autoresearch
pip install backtesting yfinance
```

## End-to-End Workflow

### 1. Set up your backtest runner (one-time)

Copy the example runner from the plugin repo into your trading project. The plugin is installed at `~/.claude/plugins/cache/lucemia/investment-autoresearch/`:

```bash
PLUGIN=~/.claude/plugins/cache/lucemia/investment-autoresearch
cp $PLUGIN/examples/backtest_runner.py your-project/
cp -r $PLUGIN/examples/strategies/ your-project/strategies/
```

Add your strategy classes to `strategies/{ticker}.py`. Verify it works:

```bash
cd your-project
python backtest_runner.py --ticker QQQ --strategy BuyAndHold --period 5y
```

You should see output containing `Return (Ann.) [%]` and `Max. Drawdown [%]`.

### 2. Run autoresearch

In Claude Code:

```
/autoresearch
```

Claude will ask for your ticker, scoring command, and session name, then launch parallel agents — each testing one hypothesis in an isolated git worktree.

### 3. Parse results

After one or more rounds:

```
/autoresearch-parse
```

Runs walk-forward backtests across 1y/2y/3y/5y and produces `autoresearch_result.json`.

### 4. Generate report

```
/autoresearch-report
```

Produces a structured markdown report from `autoresearch_result.json`.

### 5. Visualize

```
/autoresearch-strategy-chart
```

Generates a 3-panel matplotlib chart (price + equity curve, drawdown, VIX). Optionally uploads to Slack or Discord.

## Folder convention

All research output goes under `archive/{ticker}-autoresearch-v{N}/`:

```
archive/
└── qqq-autoresearch-v1/
    ├── verified_insights.md        ← cumulative state (baseline, insights, rejections, hypotheses)
    ├── AGENT_R1_RESULTS.md         ← round 1 results (one file per agent or per hypothesis)
    ├── AGENT_R2_RESULTS.md
    └── autoresearch_result.json    ← parsed + walk-forward metrics (from /autoresearch-parse)
```

## Running tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## License

MIT
