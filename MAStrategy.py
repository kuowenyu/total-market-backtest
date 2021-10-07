import backtrader as bt
import pandas
import pandas_market_calendars as market_calendar
from datetime import datetime

class MAStrategy(bt.Strategy):

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

                if self.close[0] > self.sma[-1]:
                    self.buy(size=size)
            else:
                if self.close[0] < self.sma[-1]:
                    self.sell(size=self.position.size)
