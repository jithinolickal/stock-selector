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

# Filter thresholds (to be implemented in Phase 2)
FILTER_THRESHOLDS = {
    # TODO: Implement scalping-specific thresholds
}

# Scoring weights (to be implemented in Phase 2)
SCORING_WEIGHTS = {
    # TODO: Implement scalping-specific scoring
}

# Output configuration
MAX_STOCKS_TO_SELECT = 5  # Can handle more for scalping
