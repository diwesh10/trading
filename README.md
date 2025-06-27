# Algo-Trading System with ML & Automation

This project is a Python-based mini algo-trading prototype that fetches stock data, implements a trading strategy, backtests it, and logs the results to Google Sheets. It also includes a simple machine learning model to predict stock price movements.

## Features

- **Data Ingestion**: Fetches daily stock data from Alpha Vantage.
- **Trading Strategy**: Implements a trading strategy based on RSI and Moving Average Crossover.
- **Backtesting**: Backtests the strategy on the last 6 months of historical data.
- **Google Sheets Integration**: Logs trade signals, P&L, and performance summaries to Google Sheets.
- **ML Model**: A simple Decision Tree model to predict next-day price movements.
- **Automation**: A single script to run the entire pipeline.

## Project Structure
```
algo_trading/
├── main.py
├── data/
│   └── data_fetcher.py
├── strategy/
│   ├── indicators.py
│   └── backtester.py
├── gsheets/
│   └── sheets_client.py
├── ml/
│   └── model.py
├── utils/
│   └── logger.py
├── config.py
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Prerequisites

- Python 3.7+
- An Alpha Vantage API key (get one for free [here](https://www.alphavantage.co/support/#api-key))
- A Google Cloud Platform project with the Google Sheets API enabled and service account credentials (see [gspread docs](https://gspread.readthedocs.io/en/latest/oauth2.html) for instructions).

### 2. Installation

Clone the repository and install the required packages:

```bash
git clone <repository-url>
cd <repository-directory>
pip install -r requirements.txt
```

### 3. Configuration

1.  **API Key**: Open `config.py` and replace `"YOUR_API_KEY"` with your actual Alpha Vantage API key.
2.  **Tickers**: You can change the list of stock tickers in `config.py`.
3.  **Google Sheets (Optional)**:
    *   Follow the `gspread` documentation to set up OAuth2 and get your credentials JSON file.
    *   Update `GSHEETS_CREDENTIALS_PATH` in `config.py` with the path to your credentials file.
    *   Create a new Google Sheet and share it with the `client_email` found in your credentials JSON file.
    *   Update `GSHEETS_SPREADSHEET_NAME` in `config.py` with the name of your spreadsheet.

### 4. Running the Application

To run the entire trading algorithm, execute the `main.py` script:

```bash
python main.py
```

The script will:
- Fetch the latest stock data for the configured tickers.
- Run the backtesting simulation for the past 6 months.
- Train the ML model and output its accuracy.
- Log the trade log and a summary of the performance to your Google Sheet (if configured).

## Bonus: Telegram Integration

The bonus task of integrating Telegram alerts is not implemented in this version. To add this feature, you would need to:
1.  Create a Telegram bot and get its API token.
2.  Use the `python-telegram-bot` library.
3.  Add a function to send messages (e.g., in `utils`) and call it from `main.py` to send alerts for new trades or errors.
