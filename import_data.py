import yfinance as yf

data = yf.download("SPY", start="2000-01-01", end="2021-10-01")
data.to_csv("spy.csv")