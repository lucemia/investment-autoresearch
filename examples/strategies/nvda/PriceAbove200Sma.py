import pandas as pd
from backtesting import Strategy
from backtesting.lib import crossover


class PriceAbove200Sma(Strategy):
    def init(self):
        close = pd.Series(self.data.Close)
        self.sma200 = self.I(lambda x: pd.Series(x).rolling(200).mean(), self.data.Close)

    def next(self):
        if self.data.Close[-1] > self.sma200[-1]:
            if not self.position:
                self.buy()
        else:
            if self.position:
                self.position.close()
