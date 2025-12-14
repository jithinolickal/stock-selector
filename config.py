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
    "ADX_MIN": 23,                    # Minimum ADX for trend strength (slightly relaxed for real markets)
    "RSI_MIN": 42,                    # Minimum RSI (balanced - not too tight)
    "RSI_MAX": 62,                    # Maximum RSI (balanced - not too tight)
    "ATR_MULTIPLIER": 1.15,           # ATR must be >= 1.15x its 20-day average (slight expansion)
    "VOLUME_MULTIPLIER": 1.0,         # Current volume > 1x of 20-day average
    "EMA_SLOPE_DAYS": 5,              # Days to check EMA20 slope

    # Price action filters
    "MIN_HIGHER_LOWS": 2,             # Minimum consecutive higher lows required (relaxed to 2)
    "CONSOLIDATION_RANGE": 0.03,      # Max 3% range for consolidation detection
    "CONSOLIDATION_DAYS": 5,          # Minimum days in consolidation
    "VOLUME_EXPANSION_DAYS": 3,       # Check last N days for volume expansion

    # Support/Resistance filters
    "MIN_DISTANCE_TO_RESISTANCE": 2.0,  # Minimum 2% distance to resistance
    "MAX_DISTANCE_TO_SUPPORT": 5.0,     # Maximum 5% distance to support

    # Trade quality filters
    "MIN_STOP_DISTANCE": 0.5,         # Minimum 0.5% stop distance
    "MAX_STOP_DISTANCE": 2.0,         # Maximum 2.0% stop distance
    "MIN_RISK_REWARD": 1.5,           # Minimum 1.5R risk-reward ratio

    # Intraday confirmation filters (15-min)
    "INTRADAY_VOLUME_MULTIPLIER": 1.2,  # 15-min volume >= 1.2x 20-period avg
    "UPPER_WICK_THRESHOLD": 0.5,        # Upper wick must be < 50% of candle range
    "VWAP_CANDLES_TO_CHECK": 2,         # First N candles to check for VWAP hold
}

# Scoring weights (must sum to 100)
SCORING_WEIGHTS = {
    "trend_strength": 25,           # ADX + EMA alignment
    "rsi_position": 15,             # RSI proximity to ideal 50-55
    "relative_strength": 15,        # Outperformance vs NIFTY50
    "volume_expansion": 10,         # Volume above average
    "atr_percentage": 5,            # Volatility measure
    "weekly_alignment": 10,         # Weekly timeframe confirmation
    "price_action": 10,             # Higher lows pattern
    "trade_quality": 10,            # Stop quality + R:R ratio
}

# Output configuration
MAX_STOCKS_TO_SELECT = 3      # Return top 1-3 stocks
RESULTS_DIR = "results"        # Directory for daily JSON outputs

# Data fetching configuration
HISTORICAL_DAYS = 400          # Number of calendar days to fetch (~250-280 trading days for EMA200)
INTRADAY_START_TIME = "09:15"  # Market open time
INTRADAY_END_TIME = "10:00"    # Cutoff for intraday confirmation

# Upstox API configuration
UPSTOX_INSTRUMENTS_URL = "https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz"
