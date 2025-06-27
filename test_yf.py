import yfinance as yf
import pandas as pd
data = yf.download("AAPL", period="1y")
print(data)
data['position'] = data['signal'].replace(0, pd.NA).ffill()