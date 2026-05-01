# Non-Coder Friendly Autoresearch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `/autoresearch` usable by non-coders — Claude asks only ticker + goal, writes all strategy code itself, and auto-handles backtesting setup invisibly.

**Architecture:** Three coordinated changes: (1) split `examples/strategies/qqq.py` into one-file-per-strategy under `examples/strategies/qqq/`; (2) update both runners (`examples/backtest_runner.py` and a new plugin-root `backtest_runner.py`) to load from the new per-file structure; (3) rewrite `skills/investment-autoresearch/SKILL.md` to add setup detection, a 2-question onboarding flow, goal-based hypothesis seeding, and a strategy-writing agent prompt.

**Tech Stack:** Python 3.9+, backtesting.py, yfinance, pytest, markdown (SKILL.md)

---

## File Map

```
examples/
  strategies/
    qqq.py                        DELETE (split into per-file)
    qqq/
      __init__.py                 CREATE (empty)
      BuyAndHold.py               CREATE
      SmaCross.py                 CREATE
      SmaCross_10_30.py           CREATE
      SmaCross_50_200.py          CREATE
      RsiStrategy.py              CREATE
  backtest_runner.py              MODIFY (update import: strategies.{ticker} → strategies.{ticker}.{name})

backtest_runner.py                CREATE (plugin-root version, uses os.getcwd() for path resolution)

skills/investment-autoresearch/
  SKILL.md                        MODIFY (add setup detection, onboarding, hypothesis seeding, agent prompt)

tests/
  test_backtest_runner.py         MODIFY (add per-file structure tests, plugin-root runner test)
```

---

## Task 1: Split examples/strategies/qqq.py into per-file structure

**Files:**
- Delete: `examples/strategies/qqq.py`
- Create: `examples/strategies/qqq/__init__.py`
- Create: `examples/strategies/qqq/BuyAndHold.py`
- Create: `examples/strategies/qqq/SmaCross.py`
- Create: `examples/strategies/qqq/SmaCross_10_30.py`
- Create: `examples/strategies/qqq/SmaCross_50_200.py`
- Create: `examples/strategies/qqq/RsiStrategy.py`
- Modify: `tests/test_backtest_runner.py`

- [ ] **Step 1: Write failing tests for per-file structure**

Add to `tests/test_backtest_runner.py` after the existing `test_runner_exists` test:

```python
def test_strategy_files_exist():
    """Each strategy must have its own file under examples/strategies/qqq/"""
    qqq_dir = REPO_ROOT / "examples" / "strategies" / "qqq"
    assert (qqq_dir / "__init__.py").exists(), "Missing examples/strategies/qqq/__init__.py"
    for name in ["BuyAndHold", "SmaCross", "SmaCross_10_30", "SmaCross_50_200", "RsiStrategy"]:
        path = qqq_dir / f"{name}.py"
        assert path.exists(), f"Missing: examples/strategies/qqq/{name}.py"


def test_strategy_file_class_name_matches_filename():
    """Each strategy file must contain a class with the same name as the file."""
    import re
    qqq_dir = REPO_ROOT / "examples" / "strategies" / "qqq"
    for name in ["BuyAndHold", "SmaCross", "SmaCross_10_30", "SmaCross_50_200", "RsiStrategy"]:
        content = (qqq_dir / f"{name}.py").read_text()
        assert f"class {name}(" in content, f"examples/strategies/qqq/{name}.py must define class {name}"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/davidchen/repo/investment-autoresearch
python -m pytest tests/test_backtest_runner.py::test_strategy_files_exist tests/test_backtest_runner.py::test_strategy_file_class_name_matches_filename -v
```

Expected: FAIL — `examples/strategies/qqq/` directory does not exist yet.

- [ ] **Step 3: Create examples/strategies/qqq/__init__.py**

Create empty file at `examples/strategies/qqq/__init__.py`.

- [ ] **Step 4: Create examples/strategies/qqq/BuyAndHold.py**

```python
from backtesting import Strategy


class BuyAndHold(Strategy):
    def init(self):
        pass

    def next(self):
        if not self.position:
            self.buy()
```

- [ ] **Step 5: Create examples/strategies/qqq/SmaCross.py**

```python
import numpy as np
from backtesting import Strategy
from backtesting.lib import crossover


class SmaCross(Strategy):
    fast = 20
    slow = 50

    def init(self):
        close = self.data.Close
        self.fast_ma = self.I(lambda x: np.convolve(x, np.ones(self.fast) / self.fast, mode='same'), close)
        self.slow_ma = self.I(lambda x: np.convolve(x, np.ones(self.slow) / self.slow, mode='same'), close)

    def next(self):
        if crossover(self.fast_ma, self.slow_ma):
            self.buy()
        elif crossover(self.slow_ma, self.fast_ma):
            self.position.close()
```

- [ ] **Step 6: Create examples/strategies/qqq/SmaCross_10_30.py**

```python
import numpy as np
from backtesting import Strategy
from backtesting.lib import crossover


class SmaCross_10_30(Strategy):
    fast = 10
    slow = 30

    def init(self):
        close = self.data.Close
        self.fast_ma = self.I(lambda x: np.convolve(x, np.ones(self.fast) / self.fast, mode='same'), close)
        self.slow_ma = self.I(lambda x: np.convolve(x, np.ones(self.slow) / self.slow, mode='same'), close)

    def next(self):
        if crossover(self.fast_ma, self.slow_ma):
            self.buy()
        elif crossover(self.slow_ma, self.fast_ma):
            self.position.close()
```

- [ ] **Step 7: Create examples/strategies/qqq/SmaCross_50_200.py**

```python
import numpy as np
from backtesting import Strategy
from backtesting.lib import crossover


class SmaCross_50_200(Strategy):
    fast = 50
    slow = 200

    def init(self):
        close = self.data.Close
        self.fast_ma = self.I(lambda x: np.convolve(x, np.ones(self.fast) / self.fast, mode='same'), close)
        self.slow_ma = self.I(lambda x: np.convolve(x, np.ones(self.slow) / self.slow, mode='same'), close)

    def next(self):
        if crossover(self.fast_ma, self.slow_ma):
            self.buy()
        elif crossover(self.slow_ma, self.fast_ma):
            self.position.close()
```

- [ ] **Step 8: Create examples/strategies/qqq/RsiStrategy.py**

```python
import numpy as np
from backtesting import Strategy


class RsiStrategy(Strategy):
    rsi_period = 14
    overbought = 70
    oversold = 30

    def init(self):
        close = self.data.Close

        def rsi(prices, period):
            delta = np.diff(prices)
            gain = np.where(delta > 0, delta, 0)
            loss = np.where(delta < 0, -delta, 0)
            avg_gain = np.convolve(gain, np.ones(period) / period, mode='full')[:len(prices)]
            avg_loss = np.convolve(loss, np.ones(period) / period, mode='full')[:len(prices)]
            rs = np.where(avg_loss == 0, 100, avg_gain / avg_loss)
            result = 100 - (100 / (1 + rs))
            result[:period] = 50
            return result

        self.rsi = self.I(rsi, close, self.rsi_period)

    def next(self):
        if self.rsi[-1] < self.oversold and not self.position:
            self.buy()
        elif self.rsi[-1] > self.overbought and self.position:
            self.position.close()
```

- [ ] **Step 9: Delete examples/strategies/qqq.py**

```bash
rm /Users/davidchen/repo/investment-autoresearch/examples/strategies/qqq.py
```

- [ ] **Step 10: Run structure tests to verify they pass**

```bash
cd /Users/davidchen/repo/investment-autoresearch
python -m pytest tests/test_backtest_runner.py::test_strategy_files_exist tests/test_backtest_runner.py::test_strategy_file_class_name_matches_filename -v
```

Expected: both PASS.

- [ ] **Step 11: Commit**

```bash
cd /Users/davidchen/repo/investment-autoresearch
git add examples/strategies/qqq/ tests/test_backtest_runner.py
git rm examples/strategies/qqq.py
git commit -m "refactor: split examples/strategies/qqq.py into one-file-per-strategy"
```

---

## Task 2: Update examples/backtest_runner.py import path

**Files:**
- Modify: `examples/backtest_runner.py` (lines 25-35)
- Test: `tests/test_backtest_runner.py`

The runner currently does `importlib.import_module(f"strategies.{ticker.lower()}")` then `getattr(module, strategy_name)`. After Task 1, each strategy lives in its own module `strategies.{ticker}.{strategy_name}` and the class is the module's top-level export.

- [ ] **Step 1: Run existing smoke test to confirm it currently fails**

The existing test `test_buy_and_hold_prints_required_fields` calls the runner with `--strategy BuyAndHold`. After Task 1 deleted `qqq.py`, the old import `strategies.qqq` no longer resolves. Verify:

```bash
cd /Users/davidchen/repo/investment-autoresearch
python -m pytest tests/test_backtest_runner.py::test_unknown_strategy_exits_nonzero -v
```

Note: `test_buy_and_hold_prints_required_fields` is `@pytest.mark.network` — skip for now. The `test_unknown_strategy_exits_nonzero` test exercises the import path and should still exit non-zero (just with a different error). Focus on making BuyAndHold work.

- [ ] **Step 2: Update load_strategy in examples/backtest_runner.py**

Replace the `load_strategy` function (lines 24–35) with:

```python
def load_strategy(ticker: str, strategy_name: str):
    module_name = f"strategies.{ticker.lower()}.{strategy_name}"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"ERROR: No strategy file found at strategies/{ticker.lower()}/{strategy_name}.py", file=sys.stderr)
        sys.exit(1)
    try:
        return getattr(module, strategy_name)
    except AttributeError:
        print(f"ERROR: Class '{strategy_name}' not found in strategies/{ticker.lower()}/{strategy_name}.py", file=sys.stderr)
        sys.exit(1)
```

- [ ] **Step 3: Verify runner works manually**

```bash
cd /Users/davidchen/repo/investment-autoresearch/examples
python backtest_runner.py --ticker QQQ --strategy BuyAndHold --period 1y 2>&1 | grep -E "Return \(Ann\.\)|Max\. Drawdown|ERROR"
```

Expected: `Return (Ann.) [%]` line printed, no ERROR.

- [ ] **Step 4: Run full test suite (excluding network tests)**

```bash
cd /Users/davidchen/repo/investment-autoresearch
python -m pytest tests/test_backtest_runner.py -v -m "not network"
```

Expected: `test_runner_exists`, `test_strategy_files_exist`, `test_strategy_file_class_name_matches_filename`, `test_unknown_strategy_exits_nonzero`, `test_unknown_ticker_module_exits_nonzero` all PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/davidchen/repo/investment-autoresearch
git add examples/backtest_runner.py
git commit -m "fix: update examples runner to load from strategies/{ticker}/{StrategyName}.py"
```

---

## Task 3: Add plugin-root backtest_runner.py

**Files:**
- Create: `backtest_runner.py` (repo root)
- Modify: `tests/test_backtest_runner.py`

This is the embedded runner Claude uses internally. Differs from `examples/backtest_runner.py` in one key way: uses `os.getcwd()` for `sys.path` (not `Path(__file__).parent`), so it finds strategies in the user's project dir regardless of where the runner itself lives.

- [ ] **Step 1: Write failing test**

Add to `tests/test_backtest_runner.py`:

```python
PLUGIN_RUNNER = REPO_ROOT / "backtest_runner.py"


def test_plugin_runner_exists():
    assert PLUGIN_RUNNER.exists(), "backtest_runner.py not found at plugin root"


def test_plugin_runner_uses_cwd_for_path():
    """Plugin runner must use os.getcwd() so Claude can call it from any project dir."""
    content = PLUGIN_RUNNER.read_text()
    assert "os.getcwd()" in content, "Plugin runner must use os.getcwd() for sys.path"


@pytest.mark.network
def test_plugin_runner_works_with_cwd_as_examples():
    """Plugin runner finds strategies/ when cwd is set to examples/ directory."""
    result = subprocess.run(
        [sys.executable, str(PLUGIN_RUNNER),
         "--ticker", "QQQ", "--strategy", "BuyAndHold", "--period", "1y"],
        cwd=str(REPO_ROOT / "examples"),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, f"Plugin runner failed: {result.stderr}"
    assert "Return (Ann.) [%]" in result.stdout
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/davidchen/repo/investment-autoresearch
python -m pytest tests/test_backtest_runner.py::test_plugin_runner_exists tests/test_backtest_runner.py::test_plugin_runner_uses_cwd_for_path -v
```

Expected: FAIL — `backtest_runner.py` does not exist at repo root.

- [ ] **Step 3: Create backtest_runner.py at repo root**

```python
#!/usr/bin/env python3
"""
Embedded backtest runner for investment-autoresearch plugin.

Called internally by Claude and agents. Not intended for direct use.
Claude always calls this with cwd set to the user's project directory:

    cd /user/project && python ~/.claude/plugins/cache/lucemia/investment-autoresearch/backtest_runner.py \
        --ticker QQQ --strategy SmaCross_50_200 --period 5y

Strategies are loaded from strategies/{ticker}/{StrategyName}.py in the user's project.

Output format (Backtesting.py native — compatible with autoresearch-parse skill):
    Return (Ann.) [%]    15.53
    Max. Drawdown [%]    -34.22
"""
import argparse
import importlib
import os
import sys

import pandas as pd
import yfinance as yf
from backtesting import Backtest

# User's project dir is always cwd — Claude calls this as: cd {project_dir} && python {plugin}/backtest_runner.py
sys.path.insert(0, os.getcwd())


def load_strategy(ticker: str, strategy_name: str):
    module_name = f"strategies.{ticker.lower()}.{strategy_name}"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"ERROR: No strategy file found at strategies/{ticker.lower()}/{strategy_name}.py", file=sys.stderr)
        sys.exit(1)
    try:
        return getattr(module, strategy_name)
    except AttributeError:
        print(f"ERROR: Class '{strategy_name}' not found in strategies/{ticker.lower()}/{strategy_name}.py", file=sys.stderr)
        sys.exit(1)


def fetch_data(ticker: str, period: str):
    data = yf.download(ticker, period=period, auto_adjust=True, progress=False)
    if data.empty:
        print(f"ERROR: No data returned for {ticker} over {period}", file=sys.stderr)
        sys.exit(1)
    # yfinance >= 0.2 returns MultiIndex (field, ticker) for single-ticker downloads
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
    return data


def main():
    parser = argparse.ArgumentParser(description="Internal backtest runner for investment-autoresearch plugin")
    parser.add_argument("--ticker", required=True, help="Ticker symbol (e.g. QQQ)")
    parser.add_argument("--strategy", required=True, help="Strategy class name (e.g. SmaCross_50_200)")
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

- [ ] **Step 4: Run non-network tests to verify they pass**

```bash
cd /Users/davidchen/repo/investment-autoresearch
python -m pytest tests/test_backtest_runner.py::test_plugin_runner_exists tests/test_backtest_runner.py::test_plugin_runner_uses_cwd_for_path -v
```

Expected: both PASS.

- [ ] **Step 5: Run full non-network suite to check for regressions**

```bash
cd /Users/davidchen/repo/investment-autoresearch
python -m pytest tests/ -v -m "not network"
```

Expected: all pass, 1 skipped (archive schema test).

- [ ] **Step 6: Commit**

```bash
cd /Users/davidchen/repo/investment-autoresearch
git add backtest_runner.py tests/test_backtest_runner.py
git commit -m "feat: add plugin-root backtest_runner.py using os.getcwd() for agent use"
```

---

## Task 4: Rewrite investment-autoresearch SKILL.md for non-coder flow

**Files:**
- Modify: `skills/investment-autoresearch/SKILL.md`

Replace the existing `## Setup Requirements` section and update `## Phase 1` agent prompt. Add three new sections: Setup Detection, Hypothesis Seeding, Winner Promotion.

**Current section order in SKILL.md:**
1. Frontmatter + header
2. When to Use / When NOT to Use
3. The Loop (digraph)
4. **Setup Requirements** ← replace content
5. **Phase 1: Parallel Exploration** ← update agent prompt
6. Phase 2: Collect and Update
7. Phase 3: Reset
8. Iteration Pattern
9. Common Mistakes

- [ ] **Step 1: Verify metadata test passes before editing**

```bash
cd /Users/davidchen/repo/investment-autoresearch
python -m pytest tests/test_plugin_metadata.py -v
```

Expected: all pass. Record this as baseline — same tests must pass after editing.

- [ ] **Step 2: Replace ## Setup Requirements section**

Find the `## Setup Requirements` section (starts at line 39 of SKILL.md) and replace it entirely with:

```markdown
## Setup Detection

Before asking the user anything, silently check for missing dependencies:

```bash
python3 -c "import backtesting, yfinance" 2>/dev/null || pip install backtesting yfinance
```

Do not mention this to the user. Deps are an implementation detail.

## Onboarding

Ask only two questions — nothing else:

**Q1:** "What ticker would you like to research? (e.g. QQQ, AAPL, TSLA)"

**Q2:** "What matters more to you — higher returns, or limiting losses?"

Then auto-handle everything below without user input:

1. Auto-increment session version:
   ```bash
   ls archive/ 2>/dev/null | grep -c "{ticker}-autoresearch" || echo 0
   ```
   Use next N → session folder = `archive/{ticker}-autoresearch-v{N}/`

2. Create directories:
   ```bash
   mkdir -p archive/{ticker}-autoresearch-v{N}
   mkdir -p strategies/{ticker}
   touch strategies/{ticker}/__init__.py
   ```

3. Write baseline strategy to `strategies/{ticker}/BuyAndHold.py`:
   ```python
   from backtesting import Strategy

   class BuyAndHold(Strategy):
       def init(self):
           pass

       def next(self):
           if not self.position:
               self.buy()
   ```

4. Run baseline:
   ```bash
   cd {cwd} && python ~/.claude/plugins/cache/lucemia/investment-autoresearch/backtest_runner.py \
     --ticker {TICKER} --strategy BuyAndHold --period 5y
   ```

5. Seed `archive/{ticker}-autoresearch-v{N}/verified_insights.md`:
   ```markdown
   # Verified Insights — {TICKER}

   ## Baseline
   - Current best: BuyAndHold = Return (Ann.) {X}%, MaxDD {Y}%, Calmar {Z}
   - Goal: {higher returns | limiting losses}
   - Scoring: cd {cwd} && python ~/.claude/plugins/cache/lucemia/investment-autoresearch/backtest_runner.py --ticker {TICKER} --strategy {StrategyName} --period {period}

   ## Confirmed principles
   (none yet — first session)

   ## Rejected approaches
   (none yet — first session)

   ## Open hypotheses to test
   {seed 4-6 from Hypothesis Seeding section below}
   ```

6. Launch agents (Phase 1 below).

**Never mention to the user:** scoring command, session folder, verified_insights.md, git worktrees, backtest_runner.py, walk-forward validation.

## Hypothesis Seeding by Goal

Pick 4–6 hypotheses from the matching pool. On subsequent sessions, read `verified_insights.md` rejected approaches and exclude those.

**"Higher returns" pool:**
- Momentum: buy when 3-month price return > 0, exit when negative
- Trend-following SMA 20/50: buy on fast-crosses-slow, sell on reverse
- Breakout: buy on new 52-week high close, exit on 10% trailing stop
- Volatility regime: hold only when VIX < 20, else cash
- Dual momentum: hold only when ticker outperforms 3-month T-bill return

**"Limiting losses" pool:**
- Golden cross SMA 50/200: buy when 50 > 200, sell when 200 > 50
- Volatility exit: exit when 20-day realized volatility exceeds 30%, reenter when < 20%
- Trailing stop: exit at -10% from rolling 52-week high, reenter on new high
- Price regime: hold only when price > 200-day SMA, else cash
- RSI filter: exit when RSI(14) > 75, reenter when RSI(14) < 40
```

- [ ] **Step 3: Update ## Phase 1 agent prompt**

Find the agent prompt template in `## Phase 1: Parallel Exploration` and replace the inner `prompt="""..."""` block with:

```
  prompt="""
  Read archive/{ticker}-autoresearch-v{N}/verified_insights.md first.

  Baseline: BuyAndHold = Return (Ann.) {X}%, MaxDD {Y}%, Calmar {Z}
  Goal: {higher returns | limiting losses}

  YOUR HYPOTHESIS: {specific, testable claim}

  STEPS:
  1. Write your strategy to strategies/{ticker}/{StrategyName}.py
     (Replace {StrategyName} with a descriptive CamelCase name, e.g. GoldenCross, MomentumFilter)
     The file must contain exactly one class with the same name as the file.
     The class must extend backtesting.Strategy and implement init() and next().
     Create strategies/{ticker}/__init__.py (empty) if it doesn't exist.

  2. Run backtest across all four periods:
     cd {cwd} && python ~/.claude/plugins/cache/lucemia/investment-autoresearch/backtest_runner.py \
       --ticker {TICKER} --strategy {StrategyName} --period 5y
     cd {cwd} && python ~/.claude/plugins/cache/lucemia/investment-autoresearch/backtest_runner.py \
       --ticker {TICKER} --strategy {StrategyName} --period 3y
     cd {cwd} && python ~/.claude/plugins/cache/lucemia/investment-autoresearch/backtest_runner.py \
       --ticker {TICKER} --strategy {StrategyName} --period 2y
     cd {cwd} && python ~/.claude/plugins/cache/lucemia/investment-autoresearch/backtest_runner.py \
       --ticker {TICKER} --strategy {StrategyName} --period 1y

  3. For each period compute: Calmar = Return (Ann.) [%] / abs(Max. Drawdown [%])

  4. Write results to archive/{ticker}-autoresearch-v{N}/AGENT_R{round}_{StrategyName}_RESULTS.md:
     - Hypothesis statement
     - Results table: period | Ann.Return | MaxDD | Calmar
     - Verdict vs baseline: BEAT / WORSE / MIXED
     - Key insight

  DO NOT touch main repo strategies/ — you are in an isolated worktree.
  DO NOT create backtest_runner.py — use the plugin's runner at the path above.
  """
```

- [ ] **Step 4: Add ## Winner Promotion section after ## Phase 2**

Insert after the `## Phase 2: Collect and Update` section:

```markdown
## Winner Promotion

After updating `verified_insights.md`, promote any strategy that beat the baseline Calmar in at least one period:

```bash
cp {worktree}/strategies/{ticker}/{StrategyName}.py {cwd}/strategies/{ticker}/{StrategyName}.py
```

One file per winning strategy. Losing strategies stay in their worktrees and are auto-cleaned up. The user's `strategies/{ticker}/` folder accumulates only strategies worth keeping.
```

- [ ] **Step 5: Run metadata test to verify frontmatter unchanged**

```bash
cd /Users/davidchen/repo/investment-autoresearch
python -m pytest tests/test_plugin_metadata.py -v
```

Expected: all pass. If `test_skill_md_name_matches_dir` fails, the frontmatter `name:` field was accidentally edited — restore it to `investment-autoresearch`.

- [ ] **Step 6: Commit**

```bash
cd /Users/davidchen/repo/investment-autoresearch
git add skills/investment-autoresearch/SKILL.md
git commit -m "feat: rewrite autoresearch skill for non-coder flow — setup detection, 2-question onboarding, goal-based hypothesis seeding, agent strategy writing"
```

---

## Self-Review

**Spec coverage:**

| Spec requirement | Covered by |
|---|---|
| Setup detection (pip install silently) | Task 4 Step 2 — Setup Detection section |
| Ask only ticker + goal | Task 4 Step 2 — Onboarding section |
| Auto-create session folder, BuyAndHold, baseline | Task 4 Step 2 — Onboarding auto-handle list |
| Hypothesis seeding by goal (2 pools) | Task 4 Step 2 — Hypothesis Seeding by Goal |
| Agents write strategies/{ticker}/{Name}.py in worktree | Task 4 Step 3 — updated agent prompt |
| Per-file strategy structure | Task 1 |
| examples runner import updated | Task 2 |
| Plugin-root runner with os.getcwd() | Task 3 |
| Winner promotion to main repo | Task 4 Step 4 |
| examples/ kept for coder users | examples/ untouched beyond Task 1 restructure |
| autoresearch-parse CLI unchanged | backtest_runner.py CLI args identical — confirmed |

**Placeholder scan:** No TBD/TODO. All `{placeholder}` values in SKILL.md steps are runtime values Claude fills in — not plan gaps. Plugin path `~/.claude/plugins/cache/lucemia/investment-autoresearch/` is hardcoded in SKILL.md — this is the correct install location for `claude plugin install gh:lucemia/investment-autoresearch`.

**Type consistency:** `load_strategy(ticker, strategy_name)` and `fetch_data(ticker, period)` signatures identical in both Task 2 (examples runner) and Task 3 (plugin runner). Module path `strategies.{ticker.lower()}.{strategy_name}` used consistently in both.

**One gap fixed:** Task 4 Step 2 adds `strategies/{ticker}/__init__.py` creation to the onboarding auto-handle list (without it, `importlib.import_module("strategies.qqq.BuyAndHold")` raises `ModuleNotFoundError` even if the file exists).
