import numpy as np
import pandas as pd
from backtesting import Strategy
from backtesting.lib import crossover


class SmaCross_50_200(Strategy):
    fast = 50
    slow = 200

    def init(self):
        close = self.data.Close
        self.fast_ma = self.I(lambda x: pd.Series(x).rolling(self.fast).mean().values, close)
        self.slow_ma = self.I(lambda x: pd.Series(x).rolling(self.slow).mean().values, close)

    def next(self):
        if crossover(self.fast_ma, self.slow_ma):
            self.buy()
        elif crossover(self.slow_ma, self.fast_ma):
            self.position.close()
