import yfinance as yf
import pandas as pd

def fetch_daily_data(symbol):
    """
    Fetches daily stock data using yfinance.

    Args:
        symbol (str): The stock symbol to fetch data for (e.g., 'RELIANCE.NS').

    Returns:
        pandas.DataFrame: A DataFrame containing the daily stock data, or None if an error occurs.
    Note:
        Uses yfinance, which supports US and Indian stocks (NSE: '.NS', BSE: '.BO').
    """
    try:
        data = yf.download(symbol, period="5y", interval="1d", auto_adjust=True)
        if data.empty:
            print(f"No data found for {symbol}.")
            return None
        data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        data.columns = ['open', 'high', 'low', 'close', 'volume']
        data.index = pd.to_datetime(data.index)
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

if __name__ == '__main__':
    from config import TICKERS
    for ticker in TICKERS:
        stock_data = fetch_daily_data(ticker)
        if stock_data is not None:
            print(f"Successfully fetched data for {ticker}")
            print(stock_data.head())
            print("-" * 30)
