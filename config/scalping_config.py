"""Configuration for scalping strategy (intraday - minutes)"""

from config.base_config import *

# Strategy metadata
STRATEGY_NAME = "scalping"
STRATEGY_DESCRIPTION = "Intraday scalping (5-15 min holds) based on 3-min candles"
TIMEFRAME = "intraday (5-15 minutes)"

# Data fetching configuration
HISTORICAL_DAYS = 100          # Need less historical data for scalping
INTRADAY_INTERVAL = "3min"     # 3-min candles for scalping
INTRADAY_LOOKBACK_CANDLES = 100  # Last 100 x 3-min candles (~5 hours)

# Filter thresholds
FILTER_THRESHOLDS = {
    # Liquidity filters (critical for scalping)
    "MIN_AVG_VOLUME": 2000000,         # Minimum 2M shares daily volume
    "MAX_SPREAD_PERCENT": 0.1,         # Max 0.1% bid-ask spread

    # Technical filters
    "RSI_PERIOD": 3,                   # Fast RSI for scalping
    "RSI_OVERSOLD": 20,                # RSI oversold level
    "RSI_OVERBOUGHT": 80,              # RSI overbought level
    "EMA_FAST": 9,                     # Fast EMA for entries
    "EMA_SLOW": 20,                    # Slow EMA for trend

    # VWAP filters
    "VWAP_DEVIATION_MAX": 0.3,         # Max 0.3% from VWAP for mean reversion

    # Momentum filters
    "MIN_VOLUME_SPIKE": 1.5,           # 1.5x volume spike required
    "MIN_ATR_POINTS": 3,               # Minimum movement potential (points)

    # MACD settings
    "MACD_FAST": 12,
    "MACD_SLOW": 26,
    "MACD_SIGNAL": 9,
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
