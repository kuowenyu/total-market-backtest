import backtrader as bt

class BuyAndHoldStrategy(bt.Strategy):

    def __init__(self):
        self.close = self.datas[0].close

    def next(self):
        if not self.position:
            size = int(self.broker.getcash() / self.close[0])
            self.buy(size=size)
