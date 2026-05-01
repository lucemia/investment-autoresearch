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
