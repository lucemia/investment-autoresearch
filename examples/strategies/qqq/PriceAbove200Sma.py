import pandas as pd
import numpy as np
from backtesting import Strategy


class PriceAbove200Sma(Strategy):
    period = 200

    def init(self):
        close = self.data.Close
        self.sma200 = self.I(lambda x: pd.Series(x).rolling(self.period).mean().values, close)

    def next(self):
        price = self.data.Close[-1]
        sma = self.sma200[-1]

        if np.isnan(sma):
            return

        if price > sma and not self.position:
            self.buy()
        elif price < sma and self.position:
            self.position.close()
