"""Single place for universe, capital and risk settings."""
from datetime import time
from pathlib import Path

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data" / "parquet"
RESULTS_DIR = ROOT / "results"

# NIFTY 50 constituents (NSE list, Dec 2025)
NIFTY50 = [
    "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK",
    "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BEL", "BHARTIARTL",
    "CIPLA", "COALINDIA", "DRREDDY", "EICHERMOT", "GRASIM",
    "HCLTECH", "HDFCBANK", "HDFCLIFE", "HINDALCO", "HINDUNILVR",
    "ICICIBANK", "INDIGO", "INFY", "ITC", "JIOFIN",
    "JSWSTEEL", "KOTAKBANK", "LT", "M&M", "MARUTI",
    "MAXHEALTH", "NESTLEIND", "NTPC", "ONGC", "POWERGRID",
    "RELIANCE", "SBILIFE", "SBIN", "SHRIRAMFIN", "SUNPHARMA",
    "TATASTEEL", "TATACONSUM", "TCS", "TECHM", "TITAN",
    "TMPV", "TRENT", "ULTRACEMCO", "WIPRO",
]
NIFTY_INDEX_KEY = "NSE_INDEX|Nifty 50"

# Candle interval used for intraday backtests
INTERVAL_MINUTES = 5
HISTORY_START = "2022-01-01"

# Account / risk
CAPITAL = 100_000           # INR
LEVERAGE = 5                # MIS intraday equity
RISK_PER_TRADE_PCT = 1.0    # % of capital risked between entry and stop
MAX_OPEN_POSITIONS = 2
MAX_TRADES_PER_DAY = 2
SLIPPAGE_BPS = 5            # per side, applied to fill price

MARKET_OPEN = time(9, 15)
SQUARE_OFF = time(15, 15)   # exit everything at/after this bar (Upstox forces 15:25)
