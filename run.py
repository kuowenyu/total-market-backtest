import backtrader as bt
from MAFearGreedStrategy import MAFearGreedStrategy
from MAStrategy import MAStrategy
from BuyAndHoldStrategy import BuyAndHoldStrategy

cerebro = bt.Cerebro()
cerebro.broker.setcash(1000000)

class SPYPutCallFearGreedVixData(bt.feeds.GenericCSVData):
    lines = ('put_call', 'fear_greed', 'vix')

    params = (
        ('dtformat', '%Y-%m-%d'),
        ('date', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('adj', 5),
        ('volume', 6),
        ('put_call', 7),
        ('fear_greed', 8),
        ('vix', 9)
    )

class FearGreedData(bt.feeds.GenericCSVData):

    params = (
        ('dtformat', '%Y-%m-%d'),
        ('datetime', 0),
        ('fear_greed', 4),
        ('volume', -1),
        ('openinterest', -1)
    )

spy_combined_csv_file = "spy-put-call-fear-greed-vix.csv"
fear_greed_csv_file = "fear-greed.csv"

spyCombinedFeed = SPYPutCallFearGreedVixData(dataname=spy_combined_csv_file)
fearGreedFeed = FearGreedData(dataname=fear_greed_csv_file)

cerebro.adddata(spyCombinedFeed)
cerebro.adddata(fearGreedFeed)

# cerebro.addstrategy(BuyAndHoldStrategy)
cerebro.addstrategy(MAStrategy)
# cerebro.addstrategy(MAFearGreedStrategy)


cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="mytrade")
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')

###########
# Start simulation
###########
cerebro.broker.set_cash(100000)
start_cash = cerebro.broker.getvalue()
print('Starting Portfolio Value: %.2f' % start_cash)

strats = cerebro.run()

fianl_cash = cerebro.broker.getvalue()
print('Final Portfolio Value: %.2f' % fianl_cash)
print('Final Portfolio Change: %.2f' % (fianl_cash/start_cash*100-100)+"%")

cerebro.run()

strat = strats[0]
for x in strat.analyzers:
    x.print()

cerebro.plot(volume=False)