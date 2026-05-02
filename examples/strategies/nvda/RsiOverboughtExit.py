import numpy as np
import pandas as pd
from backtesting import Strategy


def compute_rsi(close, period=14):
    series = pd.Series(close)
    delta = series.diff()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)
    avg_gain = gains.ewm(com=period - 1, adjust=False).mean()
    avg_loss = losses.ewm(com=period - 1, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - 100 / (1 + rs)
    rsi = rsi.fillna(50)
    return rsi.values


class RsiOverboughtExit(Strategy):
    rsi_period = 14
    overbought = 80
    oversold = 50

    def init(self):
        close = self.data.Close
        self.rsi = self.I(
            lambda x: compute_rsi(x, self.rsi_period),
            close,
            name="RSI"
        )
        # Track whether we've initialized the starting position
        self._started = False

    def next(self):
        rsi_val = self.rsi[-1]

        # On first bar, start in position if RSI is between 50-80
        if not self._started:
            self._started = True
            if 50 <= rsi_val <= 80:
                self.buy()
            return

        if self.position:
            # Sell when RSI > 80 (overbought exit)
            if rsi_val > self.overbought:
                self.position.close()
        else:
            # Re-enter when RSI < 50
            if rsi_val < self.oversold:
                self.buy()
