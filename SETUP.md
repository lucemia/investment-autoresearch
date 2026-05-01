# Setup Guide

Complete these steps once before using the plugin skills.

## 1. Install the plugin

```bash
claude plugin install gh:lucemia/investment-autoresearch
```

## 2. Set up chart uploads (optional)

The `strategy-chart` skill generates charts locally at `/tmp/chart.png`. Upload is optional.

**Slack:** Add to your shell profile:
```bash
export SLACK_BOT_TOKEN=xoxb-your-token-here
```
Get a token at https://api.slack.com/apps — add `files:write` and `chat:write` scopes.

Find your channel ID: right-click any Slack channel → **View channel details** → copy the ID (`C0XXXXXXXXX`). Update the channel ID in `skills/strategy-chart/SKILL.md`.

**Discord:** Set `DISCORD_BOT_TOKEN` and use your channel ID from the Discord developer portal.

**Local only:** Skip this step — charts save to `/tmp/chart.png` and can be copied manually.

## 3. Configure your backtest command

The `autoresearch-parse` skill needs a CLI command that:
- Accepts `--ticker` and `--strategy` arguments
- Accepts a `--period` argument (values: `5y`, `3y`, `2y`, `1y`)
- Prints output containing `Return (Ann.) [%]` and `Max. Drawdown [%]`

**If you use Backtesting.py**, its default `print(stats)` output already contains these fields — no adaptation needed.

**Example runner template** (if you need to build one):

```python
# backtest_runner.py
import argparse
from backtesting import Backtest
import yfinance as yf

parser = argparse.ArgumentParser()
parser.add_argument("--ticker", required=True)
parser.add_argument("--strategy", required=True)
parser.add_argument("--period", default="5y")
args = parser.parse_args()

# Import strategy dynamically
import importlib
module = importlib.import_module(f"strategies.{args.ticker.lower()}")
strategy_cls = getattr(module, args.strategy)

# Fetch data
data = yf.download(args.ticker, period=args.period)
data.columns = data.columns.droplevel(1)

# Run backtest
bt = Backtest(data, strategy_cls, cash=10_000, commission=0.002)
stats = bt.run()
print(stats)
```

Once built, record your command in your project notes:
```
YOUR_BACKTEST_COMMAND = python backtest_runner.py
```

When using `/autoresearch-parse`, replace `YOUR_BACKTEST_COMMAND` with this command.
