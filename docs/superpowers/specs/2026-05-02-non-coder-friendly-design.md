# Non-Coder Friendly Autoresearch Design

## Goal

Make `/autoresearch` fully usable by non-coders: no Python writing, no setup steps, no CLI knowledge required. User provides only a ticker and a goal; Claude handles everything else.

## Architecture

Three changes to the existing plugin:

1. **`backtest_runner.py` moves into plugin root** — embedded, invisible to user, called internally by Claude and agents
2. **`investment-autoresearch` SKILL.md gets three new sections** — setup detection, non-coder onboarding flow, updated agent prompt template
3. **Strategy file structure changes** — from `strategies/{ticker}.py` (monolithic) to `strategies/{ticker}/{StrategyName}.py` (one file per strategy)

No new skills, no new Python scripts beyond moving the runner. All orchestration lives in the updated SKILL.md.

---

## Component 1: backtest_runner.py (Plugin Root)

Move `examples/backtest_runner.py` → `backtest_runner.py` at the plugin root (`~/.claude/plugins/cache/lucemia/investment-autoresearch/backtest_runner.py`).

**Path resolution:** Runner uses `sys.path.insert(0, os.getcwd())` so it finds `strategies/` in the user's project directory. Claude always calls it with `cd {project_dir} &&` prefix, making cwd the user's project.

**Import change:** Updated to load from per-strategy files:
```python
# Old: strategies.{ticker}  → class {StrategyName}
# New: strategies.{ticker}.{StrategyName} → class {StrategyName}
module = importlib.import_module(f"strategies.{ticker.lower()}.{strategy_name}")
strategy_cls = getattr(module, strategy_name)
```

**CLI interface unchanged:** `--ticker`, `--strategy`, `--period` — existing autoresearch-parse skill continues to work without modification.

---

## Component 2: Strategy File Structure

```
strategies/
└── {ticker}/           ← one directory per ticker
    ├── __init__.py     ← empty, makes it a package
    ├── BuyAndHold.py   ← auto-generated at baseline step
    └── {StrategyName}.py  ← promoted from winning agent worktree
```

**Each file contains exactly one class** with the same name as the file:
```python
# strategies/qqq/SmaCross_50_200.py
from backtesting import Strategy
import numpy as np

class SmaCross_50_200(Strategy):
    ...
```

**Agents write in worktree, never touch main repo** during research. After each round, Claude promotes winner(s) by copying `strategies/{ticker}/{Name}.py` from worktree into the main repo.

---

## Component 3: SKILL.md Changes

### 3a. Setup Detection (new — runs before any user questions)

```
1. Check if `strategies/{ticker}/` exists in cwd
   → if not: create after user confirms ticker (step 3b)

2. Check if Python deps installed:
   python3 -c "import backtesting, yfinance"
   → if fails: run `pip install backtesting yfinance` automatically
     (no user prompt needed — deps are a silent implementation detail)

3. Check if `strategies/{ticker}/BuyAndHold.py` exists
   → if not: auto-generate it (see baseline step in 3b)
```

### 3b. Non-Coder Onboarding Flow (replaces current "Setup Requirements")

```
Ask only two questions:

Q1: "What ticker would you like to research? (e.g. QQQ, AAPL, TSLA)"
Q2: "What matters more to you — higher returns, or limiting losses?"

Then auto-handle (no user input needed):
  - Create archive/{ticker}-autoresearch-v{N}/ (auto-increment version)
  - Seed verified_insights.md with baseline section
  - Auto-generate strategies/{ticker}/BuyAndHold.py
  - Run baseline: cd {cwd} && python {plugin_dir}/backtest_runner.py
      --ticker {TICKER} --strategy BuyAndHold --period 5y
  - Record baseline score in verified_insights.md
  - Seed 4–6 hypotheses based on goal answer (see 3c)
  - Launch parallel agents
```

Never mention: scoring command, session folder name, verified_insights.md format, git worktrees, walk-forward validation.

### 3c. Hypothesis Seeding by Goal

**"Higher returns" hypothesis pool:**
- Momentum: buy when 3-month return > 0, exit when negative
- Trend-following: SMA 20/50 crossover
- Breakout: buy on new 52-week highs
- Volatility regime: hold only when VIX < 20
- Dual momentum: relative strength vs. cash

**"Limiting losses" hypothesis pool:**
- Golden cross: SMA 50/200 (avoids bear markets)
- Volatility exit: exit when 20-day realized vol > threshold
- Trailing stop: exit at -10% from rolling peak
- Price regime: hold only when price > 200-day SMA
- RSI filter: exit when RSI > 75, reenter when RSI < 40

Claude picks 4–6 hypotheses from the matching pool for Round 1. On subsequent sessions, reads `verified_insights.md` rejected approaches and avoids re-testing them.

### 3d. Updated Agent Prompt Template

Each agent receives:

```
Context:
  - Ticker: {TICKER}
  - Goal: {higher returns | limiting losses}
  - Baseline: BuyAndHold = Ann.Return {X}%, MaxDD {Y}%, Calmar {Z}
  - Project dir: {cwd}
  - Plugin dir: {plugin_dir}

Your hypothesis: {ONE specific hypothesis}

Steps:
  1. Write strategies/{ticker}/{StrategyName}.py with ONE class named {StrategyName}
     The class must extend backtesting.Strategy and implement init() and next()
  2. Create strategies/{ticker}/__init__.py if it doesn't exist (empty file)
  3. Run backtest across periods:
     cd {cwd} && python {plugin_dir}/backtest_runner.py \
       --ticker {TICKER} --strategy {StrategyName} --period 5y
     (repeat for 3y, 2y, 1y)
  4. Compute Calmar = Ann.Return / abs(MaxDD) for each period
  5. Write results to archive/{ticker}-autoresearch-v{N}/AGENT_R{round}_{StrategyName}_RESULTS.md

Do NOT write to strategies/ in the main repo — you are in an isolated worktree.
Do NOT create backtest_runner.py — use the one at {plugin_dir}/backtest_runner.py.
```

### 3e. Winner Promotion (after each round)

After all agents complete:
1. Claude builds scoreboard, updates verified_insights.md
2. For strategies that beat baseline on Calmar (any period): copy from worktree to main repo
   ```bash
   cp {worktree}/strategies/{ticker}/{Name}.py {cwd}/strategies/{ticker}/{Name}.py
   ```
3. Strategies that lost remain in worktree only (auto-cleaned up)

---

## User-Visible Surface

What a non-coder sees from start to finish:

```
User: /autoresearch

Claude: What ticker would you like to research?
User: QQQ

Claude: What matters more — higher returns, or limiting losses?
User: Limiting losses

Claude: [silent: creates archive/, generates BuyAndHold.py, runs baseline]
        Running baseline... QQQ buy-and-hold: 15.5% annual return, -34% max drawdown.
        Launching 5 agents to test drawdown-reducing strategies...

[agents run in background]

Claude: Round 1 complete. Here's what we found:
        [scoreboard table]
        Best strategy: SmaCross_50_200 (Calmar 1.45 over 2y, halves drawdown)
        Promoted to strategies/qqq/SmaCross_50_200.py

        Starting Round 2 with new hypotheses...
```

No mention of Python, backtesting.py, git worktrees, verified_insights.md, or scoring commands.

---

## What Doesn't Change

- `autoresearch-parse` skill — unchanged (CLI interface identical)
- `autoresearch-report` skill — unchanged
- `investment-autoresearch-strategy-chart` skill — unchanged
- `examples/` directory — kept for coder users who want to customize
- `verified_insights.md` format — unchanged
- Walk-forward validation logic — unchanged

---

## Files Changed

| File | Change |
|---|---|
| `backtest_runner.py` (plugin root) | Move from `examples/`, update import path for per-strategy files |
| `skills/investment-autoresearch/SKILL.md` | Add sections 3a–3e above |
| `examples/backtest_runner.py` | Update import path to match new structure (kept for coder users) |
| `examples/strategies/qqq/` | Restructure from `qqq.py` → `qqq/{StrategyName}.py` |

---

## Out of Scope

- Web UI or chat interface
- Strategy performance notifications
- Multi-ticker research in one session
- Automatic scheduling of research runs
