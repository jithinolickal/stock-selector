"""Base configuration shared across all strategies"""

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

# Upstox API configuration
UPSTOX_INSTRUMENTS_URL = "https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz"

# Output configuration
RESULTS_DIR = "results"
