import argparse
import importlib
import yfinance as yf
from backtesting import Backtest

parser = argparse.ArgumentParser()
parser.add_argument("--ticker", required=True)
parser.add_argument("--strategy", required=True)
parser.add_argument("--period", default="5y")
args = parser.parse_args()

module = importlib.import_module(f"strategies.{args.ticker.lower()}")
strategy_cls = getattr(module, args.strategy)

data = yf.download(args.ticker, period=args.period, auto_adjust=True, progress=False)
data.columns = data.columns.droplevel(1) if hasattr(data.columns, 'droplevel') else data.columns

bt = Backtest(data, strategy_cls, cash=10_000, commission=0.002)
stats = bt.run()
print(stats)
