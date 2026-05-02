import pandas as pd
from backtesting import Strategy


class TrailingStop20(Strategy):
    """
    Trailing stop strategy for NVDA.
    - Enter on first bar if not in position.
    - Track the highest Close since entry; exit when Close falls more than 20% below that peak.
    - After exit, re-enter when price makes a new 52-week high (Close > max of last 252 bars).
    """

    def init(self):
        close = self.data.Close
        self.high52 = self.I(
            lambda x: pd.Series(x).rolling(252, min_periods=1).max().values,
            close
        )
        self.peak = None

    def next(self):
        price = self.data.Close[-1]

        if self.position:
            # Update trailing peak
            if price > self.peak:
                self.peak = price
            # Exit if price falls more than 20% below peak
            if price < self.peak * 0.80:
                self.position.close()
                self.peak = None
        else:
            # Enter on first bar, or when price makes a new 52-week high
            if len(self.data.Close) <= 1:
                self.buy()
                self.peak = price
            else:
                prev_high52 = self.high52[-2] if len(self.data.Close) > 1 else self.high52[-1]
                if price > prev_high52:
                    self.buy()
                    self.peak = price
