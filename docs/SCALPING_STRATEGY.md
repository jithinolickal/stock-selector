# Scalping Strategy (Coming in Phase 2)

**Timeframe**: 5-15 minute holds
**Best for**: High liquidity periods, quick profits
**Run time**: Anytime during market hours (manually)

## Overview

Intraday scalping strategy for NIFTY50 stocks using 3-min candles. Focus on liquidity, momentum bursts, and VWAP mean reversion.

## Status

🚧 **Under Development** - Phase 2 implementation planned

## Planned Features

### Core Filters
- **Liquidity Check**: Volume >20M, bid-ask <₹1
- **VWAP Proximity**: Price within 0.3% of VWAP
- **Momentum**: MACD cross + RSI-3 signals
- **Volume Spike**: 3-min volume >1.5x average
- **EMA Alignment**: Price near 9 EMA for entry
- **ATR Check**: Minimum movement potential

### Scoring Focus
- Liquidity: 30% (most critical for scalping)
- Momentum: 25% (MACD, RSI-3)
- Volatility: 20% (ATR-based)
- Trend: 15% (EMA alignment)
- Setup Quality: 10%

### Trade Parameters
- **Profit Target**: 0.3-0.5%
- **Stop Loss**: 0.3-0.5%
- **Hold Time**: 5-15 minutes
- **Max Trades/Day**: 10-15
- **Risk per Trade**: 0.5-1%

## Configuration (Planned)

```python
# config/scalping_config.py
INTRADAY_INTERVAL = "3min"
FILTER_THRESHOLDS = {
    "VWAP_DEVIATION_MAX": 0.3,  # % from VWAP
    "MIN_VOLUME_SPIKE": 1.5,
    "SPREAD_MAX_PCT": 0.05,     # Max bid-ask spread
}
```

## Implementation Timeline

1. **Phase 2a**: Core scalping filters
2. **Phase 2b**: Scalping-specific indicators
3. **Phase 2c**: Scoring system
4. **Phase 2d**: Testing & optimization

## Notes

- Scalping requires very tight risk management
- Transaction costs can erode profits - factor them in
- Best during high volatility windows (9:15-10:30 AM, 2:30-3:30 PM)
- Stick to NIFTY50 for guaranteed liquidity

---

For now, use the **Swing Strategy** for reliable trades.
