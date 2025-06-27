# Algo-Trading System with ML & Automation

## Overview
This project is a Python-based mini algo-trading prototype that:
- Fetches daily stock data for 3 NIFTY 50 stocks using Yahoo Finance (`yfinance`)
- Implements a sample trading strategy (RSI < 30 + 20/50-DMA crossover)
- Logs trades and analytics to Google Sheets
- Uses a machine learning model to predict next-day movement
- Sends Telegram alerts for trades and errors

## Features
- **Data Ingestion:** Free daily data for Indian stocks (NSE) via yfinance
- **Strategy:** Buy when RSI < 30 and 20-DMA crosses above 50-DMA; sell on reverse cross
- **Backtesting:** Last 6 months, with 5 years of data for indicator accuracy
- **ML Model:** Random Forest using RSI, MACD, EMAs, Bollinger Bands, returns, and volume
- **Google Sheets:** Logs trade signals, P&L, win ratio, and summary in separate tabs
- **Telegram Alerts:** Notifies on trades and errors
- **Modular Code:** Well-documented, easy to extend

## Setup

### 1. Clone the Repo or Unzip
```bash
git clone https://github.com/diwesh10/trading.git
cd trading
```

### 2. Install Requirements
```bash
python -m pip install -r requirements.txt
```

### 3. Configure `.env`
Create a `.env` file in the project root:
```
GSHEETS_CREDENTIALS_PATH=your-credentials.json
GSHEETS_SPREADSHEET_NAME=AlgoTradingLog
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 4. Set Tickers in `config.py`
```python
TICKERS = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]
```

### 5. Google Sheets Setup
- Create a Google Sheet named `AlgoTradingLog`
- Share it with your service account email (from credentials.json) as Editor

### 6. Run the Algo
```bash
python main.py
```

## How the Strategy Works
- **Buy:** RSI < 30 and 20-DMA > 50-DMA
- **Sell:** 20-DMA < 50-DMA
- **Backtest:** Only last 6 months are used for results

## Output
- **Console:** Shows trade log, P&L, win ratio, ML accuracy
- **Google Sheets:** Tabs for Trade Log and Summary P&L
- **Telegram:** Alerts for trades and errors


