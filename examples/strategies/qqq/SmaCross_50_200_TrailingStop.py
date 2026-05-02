import numpy as np
import pandas as pd
from backtesting import Strategy
from backtesting.lib import crossover


class SmaCross_50_200_TrailingStop(Strategy):
    fast = 50
    slow = 200
    trail_pct = 0.08  # 8% trailing stop from highest price since entry

    def init(self):
        close = self.data.Close
        self.fast_ma = self.I(lambda x: np.convolve(x, np.ones(self.fast) / self.fast, mode='same'), close)
        self.slow_ma = self.I(lambda x: np.convolve(x, np.ones(self.slow) / self.slow, mode='same'), close)
        self.highest_since_entry = None

    def next(self):
        price_high = self.data.High[-1]
        price_close = self.data.Close[-1]

        if self.position:
            # Update highest price since entry
            if self.highest_since_entry is None or price_high > self.highest_since_entry:
                self.highest_since_entry = price_high

            # Check trailing stop: exit if close drops more than trail_pct from peak
            trail_stop_price = self.highest_since_entry * (1 - self.trail_pct)
            if price_close <= trail_stop_price:
                self.position.close()
                self.highest_since_entry = None
                return

            # Check SMA death cross exit
            if crossover(self.slow_ma, self.fast_ma):
                self.position.close()
                self.highest_since_entry = None
        else:
            # Enter on golden cross
            if crossover(self.fast_ma, self.slow_ma):
                self.buy()
                self.highest_since_entry = price_high
