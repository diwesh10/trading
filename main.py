import pandas as pd
from config import TICKERS, GSHEETS_SPREADSHEET_NAME, GSHEETS_CREDENTIALS_PATH
from data.data_fetcher import fetch_daily_data
from strategy.backtester import backtest_strategy
from gsheets.sheets_client import write_to_gsheet
from ml.model import train_and_predict
from utils.logger import logger
from utils.telegram_alert import send_telegram_alert
import yfinance as yf

print("Tickers being used:", TICKERS)

def run_trading_algo():
    """
    Main function to run the algo-trading process.
    """
    logger.info("Starting the algo-trading process...")

    if GSHEETS_CREDENTIALS_PATH == "path/to/your/credentials.json":
        logger.warning("Google Sheets credentials are not configured in config.py. Skipping GSheets logging.")
        gsheets_enabled = False
    else:
        gsheets_enabled = True

    all_trade_logs = []
    summary_data = []

    for ticker in TICKERS:
        logger.info(f"Processing ticker: {ticker}")

        # 1. Data Ingestion
        stock_data = fetch_daily_data(ticker)
        if stock_data is None or stock_data.empty:
            logger.warning(f"No data fetched for {ticker}. Skipping.")
            send_telegram_alert(f"❗️ *Error*: No data fetched for {ticker}. Skipping.")
            continue

        # 2. Backtesting for the last 6 months
        six_months_ago = pd.to_datetime('today') - pd.DateOffset(months=6)
        stock_data_6m = stock_data[stock_data.index >= six_months_ago].copy()

        if stock_data_6m.empty:
            logger.warning(f"Not enough data for the last 6 months for {ticker}. Skipping backtest.")
            send_telegram_alert(f"❗️ *Error*: Not enough data for the last 6 months for {ticker}. Skipping backtest.")
            continue
            
        trade_log, performance = backtest_strategy(stock_data_6m)
        logger.info(f"Backtesting complete for {ticker}. P&L: {performance['pnl']:.2f}, Win Ratio: {performance['win_ratio']:.2f}%")
        
        if not trade_log.empty:
            trade_log['ticker'] = ticker
            all_trade_logs.append(trade_log)
            # Send Telegram alerts for each trade
            for _, trade in trade_log.iterrows():
                msg = f"*{trade['type']}* signal for *{ticker}* at {trade['date'].strftime('%Y-%m-%d')}, price: {trade['price']:.2f}"
                send_telegram_alert(msg)

        # 3. ML Model
        accuracy = train_and_predict(stock_data.copy())
        if accuracy is not None:
            logger.info(f"ML model accuracy for {ticker}: {accuracy:.2f}")
        else:
            accuracy = "N/A"

        summary_data.append({
            'Ticker': ticker,
            'P&L': performance['pnl'],
            'Win Ratio (%)': performance['win_ratio'],
            'Total Trades': performance['total_trades'],
            'ML Model Accuracy': accuracy
        })

    # 4. Google Sheets Automation
    if gsheets_enabled:
        if all_trade_logs:
            full_trade_log = pd.concat(all_trade_logs, ignore_index=True)
            logger.info("Writing full trade log to Google Sheets...")
            write_to_gsheet(GSHEETS_SPREADSHEET_NAME, 'Trade Log', full_trade_log)
        else:
            logger.info("No trades to log to Google Sheets.")

        summary_df = pd.DataFrame(summary_data)
        if not summary_df.empty:
            logger.info("Writing summary P&L to Google Sheets...")
            write_to_gsheet(GSHEETS_SPREADSHEET_NAME, 'Summary P&L', summary_df)

    logger.info("Algo-trading process finished.")

if __name__ == '__main__':
    run_trading_algo()
