import pandas as pd
import numpy as np
import sys
sys.path.append(r'd:\ai new\growth_intern')
from strategy.indicators import add_rsi, add_sma
from gsheets.sheets_client import write_to_gsheet
import yfinance as yf

def backtest_strategy(data, initial_capital=100000.0):
    """
    Backtests the trading strategy.

    Args:
        data (pd.DataFrame): DataFrame with stock data and indicators.
        initial_capital (float): The initial capital for trading.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: The log of trades.
            - dict: A dictionary with performance metrics.
    """
    # Add indicators
    data = add_rsi(data)
    data = add_sma(data, 20)
    data = add_sma(data, 50)
    
    # Drop rows with NaN values after indicator calculation
    data.dropna(inplace=True)

    # Trading signals
    data['signal'] = 0
    # Buy signal: RSI < 30 and 20-DMA crosses above 50-DMA
    data.loc[(data['rsi'] < 30) & (data['sma_20'] > data['sma_50']), 'signal'] = 1
    # Sell signal: 20-DMA crosses below 50-DMA
    data.loc[(data['sma_20'] < data['sma_50']), 'signal'] = -1

    # Generate positions
    data['position'] = data['signal'].replace(0, pd.NA).ffill()
    data['position'] = data['position'].shift(1) # Shift to avoid lookahead bias

    # Calculate returns
    data['returns'] = data['close'].pct_change()
    data['strategy_returns'] = data['returns'] * data['position']

    # Generate trade log
    trades = []
    position = 0  # 0 = no position, 1 = in position
    for i, row in data.iterrows():
        if row['signal'] == 1 and position == 0:  # Buy
            trades.append({'date': i, 'type': 'BUY', 'price': row['open']})
            position = 1
        elif row['signal'] == -1 and position == 1:  # Sell
            trades.append({'date': i, 'type': 'SELL', 'price': row['open']})
            position = 0
    trade_log = pd.DataFrame(trades)

    if trade_log.empty:
        return pd.DataFrame(), {'pnl': 0, 'win_ratio': 0, 'total_trades': 0}

    # Calculate P&L
    if len(trade_log) % 2 != 0:
        trade_log = trade_log[:-1]

    buys = trade_log[trade_log['type'] == 'BUY']
    sells = trade_log[trade_log['type'] == 'SELL']

    if len(buys) == 0 or len(sells) == 0:
        return trade_log, {'pnl': 0, 'win_ratio': 0, 'total_trades': 0}


    pnl = (sells['price'].values - buys['price'].values[:len(sells)]).sum()
    wins = (sells['price'].values > buys['price'].values[:len(sells)]).sum()
    total_trades = len(buys)
    win_ratio = (wins / total_trades) * 100 if total_trades > 0 else 0
    
    performance = {
        'pnl': pnl,
        'win_ratio': win_ratio,
        'total_trades': total_trades
    }

    print(data[['rsi', 'sma_20', 'sma_50', 'signal']].tail(30))
    print("Number of buy signals:", (data['signal'] == 1).sum())
    print("Number of sell signals:", (data['signal'] == -1).sum())
    print(data.isna().sum())

    print(trade_log)

    return trade_log, performance

if __name__ == '__main__':
    from data.data_fetcher import fetch_daily_data
    from config import TICKERS

    for ticker in TICKERS:
        print(f"Backtesting for {ticker}...")
        stock_data = yf.download(ticker, period="5y", interval="1d", auto_adjust=True)
        
        if not stock_data.empty:
            # Backtest on last 6 months of data
            six_months_ago = pd.to_datetime('today') - pd.DateOffset(months=6)
            stock_data_6m = stock_data[stock_data.index >= six_months_ago]

            if not stock_data_6m.empty:
                trade_log, performance = backtest_strategy(stock_data_6m)
                print("Trade Log:")
                print(trade_log)
                print("\nPerformance:")
                print(performance)
                print("-" * 30)
                write_to_gsheet('AlgoTradingLog', ticker, trade_log)
            else:
                print(f"Not enough data for the last 6 months for {ticker}.")
