import numpy as np
from backtesting import Strategy


class RsiStrategy(Strategy):
    rsi_period = 14
    overbought = 70
    oversold = 30

    def init(self):
        close = self.data.Close

        def rsi(prices, period):
            delta = np.diff(prices)
            gain = np.where(delta > 0, delta, 0)
            loss = np.where(delta < 0, -delta, 0)
            avg_gain = np.convolve(gain, np.ones(period) / period, mode='full')[:len(prices)]
            avg_loss = np.convolve(loss, np.ones(period) / period, mode='full')[:len(prices)]
            rs = np.where(avg_loss == 0, 100, avg_gain / avg_loss)
            result = 100 - (100 / (1 + rs))
            result[:period] = 50
            return result

        self.rsi = self.I(rsi, close, self.rsi_period)

    def next(self):
        if self.rsi[-1] < self.oversold and not self.position:
            self.buy()
        elif self.rsi[-1] > self.overbought and self.position:
            self.position.close()
