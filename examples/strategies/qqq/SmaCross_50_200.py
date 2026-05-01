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
