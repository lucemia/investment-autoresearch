# investment-autoresearch

A Claude Code plugin for trading strategy research via parallel agent experimentation.

Inspired by [Ryan Li's Paradigm Hackathon methodology](https://x.com/ryanli_me) — 1,039 variants tested across 8-20 parallel agents with periodic resets.

## What it does

Runs a structured search loop over trading strategy variants:

1. Establish a baseline score
2. Seed hypotheses into `verified_insights.md`
3. Launch 5-10 parallel agents, each testing ONE hypothesis in an isolated git worktree
4. Collect results, update insights, decide: explore more or reset
5. When stuck, spawn a fresh agent that reads only `verified_insights.md` — no existing code

The reset step is the key move. Existing code anchors thinking. Fresh agents find architectures that incremental optimization cannot reach.

## Skills

| Skill | Description |
|---|---|
| `autoresearch` | Core parallel loop — baseline → agents → insights → repeat |
| `autoresearch-parse` | Parse `verified_insights.md` + agent results into structured JSON |
| `autoresearch-report` | Generate a markdown report from `autoresearch_result.json` |
| `strategy-chart` | Generate matplotlib strategy charts; optional upload to Slack, Discord, or save locally |

## Prerequisites

- [Claude Code](https://claude.ai/code)
- A backtesting framework with a CLI command (Backtesting.py works natively)
- Optional: a Slack or Discord bot token for chart uploads

## Installation

```bash
claude plugin install gh:lucemia/investment-autoresearch
```

## Quick start

1. Complete [SETUP.md](SETUP.md) — one-time configuration
2. In Claude Code, invoke: `/autoresearch`
3. Follow the prompts to name your session, set your scoring command, and launch agents

## Folder convention

All research output goes under `archive/{ticker}-autoresearch-v{N}/`:

```
archive/
└── soxl-autoresearch-v1/
    ├── verified_insights.md    ← cumulative state
    ├── AGENT_R1_RESULTS.md     ← per-round results
    ├── AGENT_R2_RESULTS.md
    └── autoresearch_result.json
```

## License

MIT
