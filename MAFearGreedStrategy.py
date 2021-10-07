import backtrader as bt
import pandas
import pandas_market_calendars as market_calendar
from datetime import datetime

class MAFearGreedStrategy(bt.Strategy):

    def __init__(self):
        self.fear_greed = self.datas[0].fear_greed
        self.close = self.datas[0].close
        self.date = self.datas[0].datetime.date
        self.sma = bt.indicators.MovingAverageSimple(period=200)

        nyse = market_calendar.get_calendar('NYSE')
        df = nyse.schedule(start_date='2000-01-01', end_date='2021-12-31')
        df = df.groupby(df.index.strftime('%Y-%m')).tail(1)
        df['date'] = pandas.to_datetime(df['market_open']).dt.date
        self.last_days_of_month = [date.isoformat() for date in df['date'].tolist()]

    def next(self):
        date = self.date(0).isoformat()
        if date in self.last_days_of_month:
            if not self.position:
                size = int(self.broker.getcash() / self.close[0])

                if self.close[0] > self.sma[-1] or get_min(self.fear_greed) < 10:
                    self.buy(size=size)
            else:
                if self.close[0] < self.sma[-1] or get_max(self.fear_greed) > 90:
                    self.sell(size=self.position.size)


def get_max(signal):
    extreme = 0
    for i in range(20):
        extreme = max(signal[-i], extreme)

    return extreme

def get_min(signal):
    extreme = 100
    for i in range(20):
        extreme = min(signal[-i], extreme)

    return extreme

