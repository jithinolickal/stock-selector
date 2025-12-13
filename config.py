"""Configuration file for NIFTY50 stock selector"""

# NIFTY50 constituent symbols (official NSE list - updated Dec 2025)
NIFTY50_SYMBOLS = [
    "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK",
    "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BEL", "BHARTIARTL",
    "CIPLA", "COALINDIA", "DRREDDY", "EICHERMOT", "GRASIM",
    "HCLTECH", "HDFCBANK", "HDFCLIFE", "HINDALCO", "HINDUNILVR",
    "ICICIBANK", "INDIGO", "INFY", "ITC", "JIOFIN",
    "JSWSTEEL", "KOTAKBANK", "LT", "M&M", "MARUTI",
    "MAXHEALTH", "NESTLEIND", "NTPC", "ONGC", "POWERGRID",
    "RELIANCE", "SBILIFE", "SBIN", "SHRIRAMFIN", "SUNPHARMA",
    "TATASTEEL", "TATACONSUM", "TCS", "TECHM", "TITAN",
    "TMPV", "TRENT", "ULTRACEMCO", "WIPRO"
]

# NIFTY50 Index instrument key for relative strength calculation
NIFTY50_INDEX_KEY = "NSE_INDEX|Nifty 50"

# Filter thresholds (from updated plan)
FILTER_THRESHOLDS = {
    # Daily timeframe filters
    "ADX_MIN": 25,                    # Minimum ADX for trend strength
    "RSI_MIN": 40,                    # Minimum RSI
    "RSI_MAX": 65,                    # Maximum RSI
    "ATR_MULTIPLIER": 1.5,            # ATR must be >= 1.5x its 20-day average
    "VOLUME_MULTIPLIER": 1.0,         # Current volume > 1x of 20-day average
    "EMA_SLOPE_DAYS": 5,              # Days to check EMA20 slope

    # Intraday confirmation filters (15-min)
    "INTRADAY_VOLUME_MULTIPLIER": 1.2,  # 15-min volume >= 1.2x 20-period avg
    "UPPER_WICK_THRESHOLD": 0.5,        # Upper wick must be < 50% of candle range
    "VWAP_CANDLES_TO_CHECK": 2,         # First N candles to check for VWAP hold
}

# Scoring weights (must sum to 100)
SCORING_WEIGHTS = {
    "trend_strength": 35,      # ADX + EMA alignment
    "rsi_position": 25,        # RSI proximity to ideal 50-60
    "relative_strength": 15,   # Outperformance vs NIFTY50
    "volume_expansion": 15,    # Volume above average
    "atr_percentage": 10,      # Volatility measure
}

# Output configuration
MAX_STOCKS_TO_SELECT = 3      # Return top 1-3 stocks
RESULTS_DIR = "results"        # Directory for daily JSON outputs

# Data fetching configuration
HISTORICAL_DAYS = 200          # Number of daily candles to fetch
INTRADAY_START_TIME = "09:15"  # Market open time
INTRADAY_END_TIME = "10:00"    # Cutoff for intraday confirmation

# Upstox API configuration
UPSTOX_INSTRUMENTS_URL = "https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz"
