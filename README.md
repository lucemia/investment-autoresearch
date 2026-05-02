# investment-autoresearch

A Claude Code plugin for trading strategy research via parallel agent experimentation.

Inspired by [Ryan Li's Paradigm Hackathon methodology](https://x.com/ryanli_me) — 1,039 variants tested across 8–20 parallel agents with periodic resets.

## What it does

Runs a structured search loop over trading strategy variants:

1. Ask two questions (ticker + goal), then auto-handle everything else
2. Establish a buy-and-hold baseline
3. Seed hypotheses into `verified_insights.md`
4. Launch 4–10 parallel agents, each testing ONE hypothesis in an isolated git worktree
5. Collect results, update insights, decide: explore more or reset
6. When stuck, spawn a fresh agent that reads only `verified_insights.md` — no existing code

The reset step is the key move. Existing code anchors thinking. Fresh agents find architectures incremental optimization cannot reach.

**In practice:** QQQ went from Calmar 0.45 (buy-and-hold) to **Calmar 1.02** in two sessions, 8 total backtests. See [docs/demo-walkthrough.md](docs/demo-walkthrough.md).

## Skills

| Skill | Trigger | Description |
|---|---|---|
| `investment-autoresearch` | `/autoresearch` | Core parallel loop — two questions, then baseline → agents → insights → repeat |
| `investment-autoresearch-parse` | `/autoresearch-parse` | Parse agent results into structured JSON + walk-forward backtests |
| `investment-autoresearch-report` | `/autoresearch-report` | Generate a markdown report from `autoresearch_result.json` |
| `investment-autoresearch-strategy-chart` | `/autoresearch-strategy-chart` | Generate matplotlib strategy chart; upload to Slack, Discord, or save locally |

## Prerequisites

- [Claude Code](https://claude.ai/code)
- git 2.5+ (required for isolated worktrees)
- Python 3.9+ with `backtesting` and `yfinance` installed
- Optional: Slack or Discord bot token for chart uploads

## Installation

**Option A — Claude Code marketplace (when available):**
```bash
claude plugin install gh:lucemia/investment-autoresearch
pip install backtesting yfinance
```

**Option B — Manual install (git clone):**
```bash
git clone https://github.com/lucemia/investment-autoresearch ~/.claude/plugins/cache/lucemia/investment-autoresearch
pip install backtesting yfinance
# Copy skills into Claude Code:
for skill in ~/.claude/plugins/cache/lucemia/investment-autoresearch/skills/*/; do
  cp -r "$skill" ~/.claude/skills/"$(basename "$skill")"
done
```

## Usage

### 1. Run autoresearch

```
/autoresearch
```

Claude asks two questions — ticker and goal — then handles everything automatically: baseline run, hypothesis seeding, parallel agents, result collection, winner promotion.

### 3. Parse results

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

All research output goes under `archive/{ticker}-autoresearch-v{N}/`. Each session auto-increments N.

```
archive/
└── qqq-autoresearch-v2/
    ├── verified_insights.md           ← cumulative state: baseline, confirmed, rejected, next hypotheses
    ├── AGENT_R1_H5_RESULTS.md         ← one file per agent/hypothesis
    ├── AGENT_R1_H6_RESULTS.md
    ├── AGENT_R1_H7_RESULTS.md
    ├── AGENT_R1_H8_RESULTS.md
    └── autoresearch_result.json       ← parsed + walk-forward metrics (from /autoresearch-parse)
```

`verified_insights.md` is the state machine of the loop — it carries every confirmed principle and rejection forward across sessions. New sessions seed from the previous session's file.

## Running tests

```bash
pip install pytest
python3 -m pytest tests/ -v
```

## Demo

See [docs/demo-walkthrough.md](docs/demo-walkthrough.md) for a full QQQ example: two sessions, 8 strategies, buy-and-hold Calmar 0.45 → **1.02**.

## License

MIT
