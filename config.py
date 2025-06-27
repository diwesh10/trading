# config.py

from dotenv import load_dotenv
import os

load_dotenv()

# Stock symbols to trade
TICKERS = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

# Google Sheets configuration
GSHEETS_CREDENTIALS_PATH = os.getenv("GSHEETS_CREDENTIALS_PATH")
GSHEETS_SPREADSHEET_NAME = os.getenv("GSHEETS_SPREADSHEET_NAME")
