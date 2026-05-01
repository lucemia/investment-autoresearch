# Pre-Release Enhancements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring the investment-autoresearch plugin to a releasable state: clean repo structure, correct README, working examples, and a unit test suite covering plugin metadata, the backtest runner, and JSON schema.

**Architecture:** Split into 5 independent tasks — cleanup, examples, tests, README, SETUP. Each produces working, verifiable output. Tests use `pytest` with no external dependencies except `backtesting` + `yfinance` (already installed). Skills are markdown-only so "tests" focus on schema/metadata correctness and the Python runner template.

**Tech Stack:** Python 3.9+, pytest, backtesting.py, yfinance, json/pathlib (stdlib)

---

## Issues Found in Review

| Area | Problem |
|---|---|
| Repo root | `backtest_runner.py` + `strategies/` from test run sitting in root — not part of plugin |
| README skill table | Shows `strategy-chart` but installed name is `investment-autoresearch-strategy-chart` |
| README | No end-to-end workflow showing all 4 skills in sequence |
| README | Missing link between skills (parse → report → chart flow not shown) |
| SETUP.md | Slack channel ID placeholder `YOUR_CHANNEL_ID` is in SKILL.md, not SETUP.md |
| Tests | Zero tests exist — no metadata validation, no runner smoke test |
| `.gitignore` | Missing — `archive/`, `strategies/`, `__pycache__`, `.pytest_cache` not ignored |
| Examples | No canonical example for new users to copy-paste and run |

---

## File Map

```
investment-autoresearch/
├── .gitignore                          MODIFY (create)
├── README.md                           MODIFY
├── SETUP.md                            MODIFY
├── backtest_runner.py                  DELETE (move to examples/)
├── strategies/                         DELETE (move to examples/)
├── examples/
│   ├── backtest_runner.py              CREATE (canonical template)
│   └── strategies/
│       ├── __init__.py                 CREATE
│       └── qqq.py                      CREATE (sample strategies)
├── tests/
│   ├── __init__.py                     CREATE
│   ├── conftest.py                     CREATE (shared fixtures)
│   ├── test_plugin_metadata.py         CREATE (SKILL.md + plugin.json validation)
│   ├── test_backtest_runner.py         CREATE (smoke test runner + strategies)
│   └── test_json_schema.py             CREATE (autoresearch_result.json schema)
└── docs/superpowers/plans/
    └── 2026-05-02-pre-release-enhancements.md  (this file)
```

---

## Task 1: Repo Cleanup + .gitignore

**Files:**
- Create: `.gitignore`
- Delete: `backtest_runner.py` (root)
- Delete: `strategies/` (root — will be recreated under `examples/`)

- [ ] **Step 1: Create .gitignore**

```
# Research output — user-generated, not part of plugin
archive/

# Example runtime artifacts
strategies/
__pycache__/
.pytest_cache/
*.pyc
*.pyo
.DS_Store
/tmp/chart.png
```

Write this to `.gitignore` at repo root.

- [ ] **Step 2: Move runner and strategies to examples/**

```bash
mkdir -p examples/strategies
cp backtest_runner.py examples/backtest_runner.py
cp strategies/__init__.py examples/strategies/__init__.py
cp strategies/qqq.py examples/strategies/qqq.py
rm backtest_runner.py
rm -rf strategies/
```

- [ ] **Step 3: Verify root is clean**

```bash
ls investment-autoresearch/
```

Expected: `LICENSE  README.md  SETUP.md  .gitignore  examples/  skills/  docs/  tests/` — no `backtest_runner.py`, no `strategies/`.

- [ ] **Step 4: Commit**

```bash
git add .gitignore examples/ && git rm backtest_runner.py && git rm -r strategies/
git commit -m "chore: move example runner/strategies to examples/, add .gitignore"
```

---

## Task 2: Polish examples/backtest_runner.py

**Files:**
- Modify: `examples/backtest_runner.py`
- Modify: `examples/strategies/qqq.py`

The runner from the test run has a yfinance compatibility workaround that could break. Harden it.

- [ ] **Step 1: Rewrite examples/backtest_runner.py with error handling and usage docs**

```python
#!/usr/bin/env python3
"""
Backtest runner for investment-autoresearch plugin.

Usage:
    python examples/backtest_runner.py --ticker QQQ --strategy BuyAndHold --period 5y

Output format (Backtesting.py native — compatible with autoresearch-parse skill):
    Return (Ann.) [%]    15.53
    Max. Drawdown [%]    -34.22
"""
import argparse
import importlib
import sys

import yfinance as yf
from backtesting import Backtest


def load_strategy(ticker: str, strategy_name: str):
    module_name = f"strategies.{ticker.lower()}"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"ERROR: No strategy module found at {module_name}.py", file=sys.stderr)
        sys.exit(1)
    try:
        return getattr(module, strategy_name)
    except AttributeError:
        print(f"ERROR: Strategy '{strategy_name}' not found in {module_name}", file=sys.stderr)
        sys.exit(1)


def fetch_data(ticker: str, period: str):
    data = yf.download(ticker, period=period, auto_adjust=True, progress=False)
    if data.empty:
        print(f"ERROR: No data returned for {ticker} over {period}", file=sys.stderr)
        sys.exit(1)
    if hasattr(data.columns, "droplevel") and isinstance(data.columns[0], tuple):
        data.columns = data.columns.droplevel(1)
    return data


def main():
    parser = argparse.ArgumentParser(description="Run a backtest and print Backtesting.py stats")
    parser.add_argument("--ticker", required=True, help="Ticker symbol (e.g. QQQ)")
    parser.add_argument("--strategy", required=True, help="Strategy class name (e.g. BuyAndHold)")
    parser.add_argument("--period", default="5y", choices=["1y", "2y", "3y", "5y", "10y"],
                        help="Lookback period (default: 5y)")
    args = parser.parse_args()

    strategy_cls = load_strategy(args.ticker, args.strategy)
    data = fetch_data(args.ticker, args.period)

    bt = Backtest(data, strategy_cls, cash=10_000, commission=0.002, finalize_trades=True)
    stats = bt.run()
    print(stats)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Smoke-test the runner manually**

```bash
cd examples && python backtest_runner.py --ticker QQQ --strategy BuyAndHold --period 1y
```

Expected: stats printed including `Return (Ann.) [%]` and `Max. Drawdown [%]` — no errors.

- [ ] **Step 3: Commit**

```bash
git add examples/
git commit -m "feat: harden example backtest runner with error handling and usage docs"
```

---

## Task 3: Unit Tests

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`
- Create: `tests/test_plugin_metadata.py`
- Create: `tests/test_backtest_runner.py`
- Create: `tests/test_json_schema.py`

### Step 1: Create tests/__init__.py and conftest.py

- [ ] **Create tests/__init__.py** (empty file)

- [ ] **Create tests/conftest.py**

```python
import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent


@pytest.fixture
def repo_root():
    return REPO_ROOT


@pytest.fixture
def skills_dir():
    return REPO_ROOT / "skills"


@pytest.fixture
def sample_result_json():
    """Minimal valid autoresearch_result.json for schema tests."""
    return {
        "ticker": "QQQ",
        "research_summary": {
            "rounds_completed": 1,
            "agents_run": 4,
            "strategies_tested": 4,
        },
        "current_best": {
            "strategy_name": "SmaCross_50_200",
            "parameters": {},
            "cagr": 9.57,
            "max_drawdown": -20.71,
            "sharpe": None,
            "robustness_score": None,
            "walk_forward": {
                "5y": {"cagr": 9.57, "ra": 0.46},
                "3y": {"cagr": 14.21, "ra": 0.82},
                "2y": {"cagr": 19.60, "ra": 1.45},
                "1y": {"cagr": None, "ra": None},
            },
            "min_ra_across_periods": 0.46,
        },
        "leaderboard": [
            {
                "rank": 1,
                "strategy_name": "SmaCross_50_200",
                "cagr": 9.57,
                "max_drawdown": -20.71,
                "calmar": 0.46,
                "trades": 4,
            }
        ],
        "verified_insights": ["Slow SMA crossovers halve max drawdown vs buy-and-hold"],
        "rejected_approaches": [
            {"approach": "SMA 10/30", "reason": "Commission drag, whipsaws in trending asset"}
        ],
        "open_hypotheses": ["SMA 30/100 intermediate speed"],
        "recommendation": {
            "graduate": "SmaCross_50_200",
            "confidence": "medium",
        },
    }
```

### Step 2: Write plugin metadata tests

- [ ] **Create tests/test_plugin_metadata.py**

```python
"""Validate all SKILL.md files and plugin.json have required fields."""
import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
PLUGIN_JSON = REPO_ROOT / ".claude-plugin" / "plugin.json"

SKILL_DIRS = list(SKILLS_DIR.iterdir()) if SKILLS_DIR.exists() else []


def test_plugin_json_is_valid():
    assert PLUGIN_JSON.exists(), "plugin.json not found"
    data = json.loads(PLUGIN_JSON.read_text())
    assert "name" in data, "plugin.json missing 'name'"
    assert "version" in data, "plugin.json missing 'version'"
    assert "description" in data, "plugin.json missing 'description'"


def test_plugin_json_version_semver():
    data = json.loads(PLUGIN_JSON.read_text())
    version = data["version"]
    assert re.match(r"^\d+\.\d+\.\d+$", version), f"version '{version}' is not semver"


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=[d.name for d in SKILL_DIRS])
def test_skill_md_exists(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    assert skill_md.exists(), f"Missing SKILL.md in {skill_dir.name}"


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=[d.name for d in SKILL_DIRS])
def test_skill_md_has_frontmatter(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text()
    assert content.startswith("---"), f"{skill_dir.name}/SKILL.md missing frontmatter (---)"
    end = content.index("---", 3)
    frontmatter = content[3:end]
    assert "name:" in frontmatter, f"{skill_dir.name}/SKILL.md frontmatter missing 'name:'"
    assert "description:" in frontmatter, f"{skill_dir.name}/SKILL.md frontmatter missing 'description:'"


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=[d.name for d in SKILL_DIRS])
def test_skill_md_name_matches_dir(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text()
    end = content.index("---", 3)
    frontmatter = content[3:end]
    name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
    assert name_match, f"{skill_dir.name}/SKILL.md frontmatter 'name:' not parseable"
    name = name_match.group(1).strip()
    assert name == skill_dir.name, (
        f"{skill_dir.name}/SKILL.md name='{name}' does not match directory name '{skill_dir.name}'"
    )
```

- [ ] **Run metadata tests**

```bash
cd /path/to/investment-autoresearch && python -m pytest tests/test_plugin_metadata.py -v
```

Expected: All PASS. If `name` mismatches dir, fix frontmatter in the affected SKILL.md.

### Step 3: Write backtest runner tests

- [ ] **Create tests/test_backtest_runner.py**

```python
"""Smoke tests for the example backtest runner."""
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
RUNNER = EXAMPLES_DIR / "backtest_runner.py"


def run_runner(*args):
    """Run the example backtest runner and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(RUNNER), *args],
        cwd=str(EXAMPLES_DIR),
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.returncode, result.stdout, result.stderr


def test_runner_exists():
    assert RUNNER.exists(), "examples/backtest_runner.py not found"


def test_buy_and_hold_prints_required_fields():
    code, stdout, stderr = run_runner("--ticker", "QQQ", "--strategy", "BuyAndHold", "--period", "1y")
    assert code == 0, f"Runner exited {code}. stderr: {stderr}"
    assert "Return (Ann.) [%]" in stdout, "Missing 'Return (Ann.) [%]' in output"
    assert "Max. Drawdown [%]" in stdout, "Missing 'Max. Drawdown [%]' in output"


def test_unknown_strategy_exits_nonzero():
    code, stdout, stderr = run_runner("--ticker", "QQQ", "--strategy", "NonExistent", "--period", "1y")
    assert code != 0, "Expected non-zero exit for unknown strategy"
    assert "ERROR" in stderr, "Expected ERROR message in stderr"


def test_unknown_ticker_module_exits_nonzero():
    code, stdout, stderr = run_runner("--ticker", "FAKEXYZ", "--strategy", "BuyAndHold", "--period", "1y")
    assert code != 0, "Expected non-zero exit for unknown ticker module"


@pytest.mark.parametrize("period", ["1y", "2y", "3y", "5y"])
def test_all_periods_work(period):
    code, stdout, stderr = run_runner("--ticker", "QQQ", "--strategy", "BuyAndHold", "--period", period)
    assert code == 0, f"Runner failed for period={period}. stderr: {stderr}"
    assert "Return (Ann.) [%]" in stdout
```

- [ ] **Run runner tests**

```bash
python -m pytest tests/test_backtest_runner.py -v
```

Expected: All PASS (requires network for yfinance; ~30s).

### Step 4: Write JSON schema tests

- [ ] **Create tests/test_json_schema.py**

```python
"""Validate autoresearch_result.json conforms to the schema defined in autoresearch-parse SKILL.md."""
import json
import tempfile
from pathlib import Path

import pytest


REQUIRED_TOP_LEVEL = ["ticker", "research_summary", "current_best", "leaderboard",
                       "verified_insights", "rejected_approaches", "open_hypotheses", "recommendation"]
REQUIRED_RESEARCH_SUMMARY = ["rounds_completed", "agents_run"]
REQUIRED_CURRENT_BEST = ["strategy_name", "parameters", "cagr", "max_drawdown",
                          "walk_forward", "min_ra_across_periods"]
VALID_WALK_FORWARD_PERIODS = {"5y", "3y", "2y", "1y"}


def validate_result_json(data: dict) -> list[str]:
    """Return list of validation errors. Empty list = valid."""
    errors = []
    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"Missing top-level key: '{key}'")

    rs = data.get("research_summary", {})
    for key in REQUIRED_RESEARCH_SUMMARY:
        if key not in rs:
            errors.append(f"Missing research_summary.{key}")

    cb = data.get("current_best", {})
    for key in REQUIRED_CURRENT_BEST:
        if key not in cb:
            errors.append(f"Missing current_best.{key}")

    wf = cb.get("walk_forward", {})
    for period in VALID_WALK_FORWARD_PERIODS:
        if period not in wf:
            errors.append(f"Missing current_best.walk_forward.{period}")
        else:
            entry = wf[period]
            if "cagr" not in entry:
                errors.append(f"Missing current_best.walk_forward.{period}.cagr")
            if "ra" not in entry:
                errors.append(f"Missing current_best.walk_forward.{period}.ra")

    for i, item in enumerate(data.get("rejected_approaches", [])):
        if "approach" not in item:
            errors.append(f"rejected_approaches[{i}] missing 'approach'")
        if "reason" not in item:
            errors.append(f"rejected_approaches[{i}] missing 'reason'")

    rec = data.get("recommendation", {})
    if "graduate" not in rec:
        errors.append("Missing recommendation.graduate")

    return errors


def test_sample_result_is_valid(sample_result_json):
    errors = validate_result_json(sample_result_json)
    assert errors == [], f"Sample JSON has schema errors:\n" + "\n".join(errors)


def test_missing_ticker_is_invalid(sample_result_json):
    del sample_result_json["ticker"]
    errors = validate_result_json(sample_result_json)
    assert any("ticker" in e for e in errors)


def test_missing_walk_forward_period_is_invalid(sample_result_json):
    del sample_result_json["current_best"]["walk_forward"]["3y"]
    errors = validate_result_json(sample_result_json)
    assert any("3y" in e for e in errors)


def test_missing_rejected_reason_is_invalid(sample_result_json):
    sample_result_json["rejected_approaches"] = [{"approach": "SMA 10/30"}]
    errors = validate_result_json(sample_result_json)
    assert any("reason" in e for e in errors)


def test_real_result_json_if_exists(repo_root):
    """If an archive result exists, validate it against schema."""
    archive = repo_root / "archive"
    if not archive.exists():
        pytest.skip("No archive directory")
    result_files = list(archive.glob("*/autoresearch_result.json"))
    if not result_files:
        pytest.skip("No autoresearch_result.json found in archive/")
    for path in result_files:
        data = json.loads(path.read_text())
        errors = validate_result_json(data)
        assert errors == [], f"{path} has schema errors:\n" + "\n".join(errors)
```

- [ ] **Run all tests**

```bash
python -m pytest tests/ -v
```

Expected: All PASS. Full output shows metadata, runner, and schema tests green.

- [ ] **Commit tests**

```bash
git add tests/
git commit -m "test: add plugin metadata, runner smoke, and JSON schema tests"
```

---

## Task 4: Fix and Expand README.md

**Files:**
- Modify: `README.md`

Issues to fix:
1. Skill table shows `strategy-chart` — should be `investment-autoresearch-strategy-chart`
2. No end-to-end workflow showing all 4 skills in sequence
3. No mention of the `examples/` directory

- [ ] **Step 1: Rewrite README.md**

```markdown
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

Copy `examples/backtest_runner.py` and `examples/strategies/` into your project. Add your strategy classes to `strategies/{ticker}.py`.

```bash
cp -r examples/backtest_runner.py examples/strategies your-project/
python backtest_runner.py --ticker QQQ --strategy BuyAndHold --period 5y
```

### 2. Run autoresearch

In Claude Code:

```
/autoresearch
```

Claude will:
- Ask for your ticker, scoring command, and session name
- Create `archive/{ticker}-autoresearch-v1/verified_insights.md`
- Launch parallel agents, each testing one hypothesis
- Collect results and update the insights file

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
    ├── AGENT_R1_RESULTS.md         ← per-round agent results
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
```

- [ ] **Step 2: Verify README renders correctly**

Open README.md and confirm:
- Skill table has 4 rows with correct installed names (investment-autoresearch-*)
- Workflow section has 5 numbered steps
- No broken links

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: rewrite README with correct skill names, end-to-end workflow, and test instructions"
```

---

## Task 5: Enhance SETUP.md

**Files:**
- Modify: `SETUP.md`

Issues: Slack channel ID setup is scattered (partly in SETUP.md, partly in SKILL.md). Make SETUP.md the single source of truth for all one-time configuration.

- [ ] **Step 1: Rewrite SETUP.md**

```markdown
# Setup Guide

Complete these steps once before using the plugin skills.

## 1. Install the plugin

```bash
claude plugin install gh:lucemia/investment-autoresearch
```

## 2. Install Python dependencies

```bash
pip install backtesting yfinance
```

## 3. Set up your backtest runner

Copy the example runner into your trading project:

```bash
cp examples/backtest_runner.py your-project/
cp -r examples/strategies/ your-project/strategies/
```

Add your strategy classes to `your-project/strategies/{ticker}.py`. Each class must extend `backtesting.Strategy`. The runner discovers classes by module name, so `--ticker QQQ --strategy MyStrategy` loads `strategies.qqq.MyStrategy`.

Verify it works:

```bash
cd your-project
python backtest_runner.py --ticker QQQ --strategy BuyAndHold --period 5y
```

You should see output containing:
```
Return (Ann.) [%]    15.5
Max. Drawdown [%]    -34.2
```

## 4. Configure chart uploads (optional)

### Slack

**Get a bot token:**
1. Go to https://api.slack.com/apps → Create New App
2. Add OAuth scopes: `files:write`, `chat:write`
3. Install to workspace and copy the `xoxb-` bot token

**Get your channel ID:**
Right-click any Slack channel → **View channel details** → copy the ID (starts with `C`).

**Set in your shell profile** (`~/.zshrc` or `~/.bashrc`):

```bash
export SLACK_BOT_TOKEN=xoxb-your-token-here
```

**Update the channel ID** in `skills/investment-autoresearch-strategy-chart/SKILL.md`:
Find `YOUR_CHANNEL_ID` and replace with your actual channel ID (e.g. `C0XXXXXXXXX`).

### Discord

Set `DISCORD_BOT_TOKEN` in your shell profile and use your Discord channel ID when the skill prompts.

### Local only

Skip steps above. Charts save to `/tmp/chart.png` automatically.

## 5. Verify everything works

Run the test suite from the plugin repo:

```bash
python -m pytest tests/ -v
```

All tests should pass. The runner tests require network access for yfinance data.
```

- [ ] **Step 2: Commit**

```bash
git add SETUP.md
git commit -m "docs: consolidate all setup steps into SETUP.md, add verification step"
```

---

## Self-Review

**Spec coverage check:**

| Requirement | Covered by |
|---|---|
| Update README | Task 4 |
| Add unit tests | Task 3 (metadata, runner, schema) |
| All functions ready to use | Task 2 (hardened runner), Task 1 (clean repo) |
| Install guidance | Task 4 (README), Task 5 (SETUP.md) |
| Clean repo artifacts from test run | Task 1 |
| .gitignore | Task 1 |

**Placeholder scan:** No TBD/TODO in any code blocks. All test assertions are concrete. All commands are exact.

**Type consistency:** `validate_result_json` defined in conftest is imported in `test_json_schema.py` via `sample_result_json` fixture — consistent across Tasks 3 step 1, 3 step 4. `REPO_ROOT` fixture defined in conftest, used in `test_plugin_metadata.py` and `test_json_schema.py` consistently.

**One gap found and fixed:** `test_plugin_metadata.py` uses `SKILLS_DIR` directly (not via fixture) — this is fine since it's a module-level constant, not session state.
