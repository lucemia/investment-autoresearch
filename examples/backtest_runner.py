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

import pandas as pd
import yfinance as yf
from backtesting import Backtest

import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))


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
