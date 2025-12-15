"""Configuration for scalping strategy (intraday - minutes)"""

from config.base_config import *

# Strategy metadata
STRATEGY_NAME = "scalping"
STRATEGY_DESCRIPTION = "Intraday scalping (5-15 min holds) based on ORB + 5-min candles"
TIMEFRAME = "intraday (5-15 minutes)"

# Data fetching configuration
HISTORICAL_DAYS = 100          # Need less historical data for scalping
INTRADAY_INTERVAL = "5min"     # 5-min candles (9 candles by 10 AM)
INTRADAY_LOOKBACK_CANDLES = 50  # Last 50 x 5-min candles (~4 hours)

# Filter thresholds
FILTER_THRESHOLDS = {
    # Liquidity filters (critical for scalping)
    "MIN_AVG_VOLUME": 2000000,         # Minimum 2M shares daily volume
    "MAX_SPREAD_PERCENT": 0.15,        # Max 0.15% bid-ask spread

    # Opening Range Breakout (ORB) settings
    "ORB_START_TIME": "09:15",         # ORB period start
    "ORB_END_TIME": "09:30",           # ORB period end (first 15 mins)
    "ORB_BREAKOUT_MIN_PCT": 0.2,       # Must break ORB by 0.2%

    # Fast EMA filters (work with 9+ candles)
    "EMA_FAST": 5,                     # Fast EMA for trend
    "EMA_SLOW": 9,                     # Slow EMA for confirmation

    # RSI (relaxed - not primary filter)
    "RSI_PERIOD": 7,                   # 7-period RSI (more stable than 3)
    "RSI_NEUTRAL_MIN": 40,             # Accept neutral range
    "RSI_NEUTRAL_MAX": 60,             # Not just extremes

    # VWAP filters (relaxed)
    "VWAP_DEVIATION_MAX": 0.8,         # Max 0.8% from VWAP

    # Volume filters (shorter average for responsiveness)
    "MIN_VOLUME_SPIKE": 1.0,           # 1.0x volume (at or above average)
    "VOLUME_AVG_PERIOD": 10,           # Use last 10 candles (not 20)

    # ATR (relaxed)
    "MIN_ATR_POINTS": 1.5,             # Minimum movement potential
}

# Scoring weights (must sum to 100)
SCORING_WEIGHTS = {
    "liquidity": 30,           # Critical for scalping - tight spreads, high volume
    "momentum": 25,            # MACD + RSI strength
    "vwap_setup": 20,          # Proximity to VWAP for entries
    "trend_alignment": 15,     # EMA 9 vs 20 alignment
    "volatility": 10,          # ATR-based movement potential
}

# Trade parameters
PROFIT_TARGET_PCT = 0.4        # 0.4% profit target
STOP_LOSS_PCT = 0.35           # 0.35% stop loss
MIN_RISK_REWARD = 1.0          # Minimum 1:1 R:R (relaxed for scalping)

# Output configuration
MAX_STOCKS_TO_SELECT = 10      # Can handle more opportunities for scalping
