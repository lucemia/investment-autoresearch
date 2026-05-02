import pandas as pd
from backtesting import Strategy


class MomentumFilter3M(Strategy):
    """
    3-Month Momentum Filter Strategy for QQQ.
    Buy and hold QQQ but exit when the 63-day (~3 month) price return turns negative,
    reenter when it turns positive. Pure price momentum — no SMA needed.
    """

    lookback = 63  # ~3 months of trading days

    def init(self):
        pass

    def next(self):
        # Need at least lookback+1 bars before acting
        if len(self.data.Close) < self.lookback + 2:
            return

        current_price = self.data.Close[-1]
        past_price = self.data.Close[-self.lookback - 1]

        momentum_return = (current_price - past_price) / past_price

        if momentum_return > 0 and not self.position:
            self.buy()
        elif momentum_return < 0 and self.position:
            self.position.close()
