# Scalping Strategy

**Timeframe**: 5-15 minute holds
**Best for**: High liquidity periods, quick profits
**Run time**: Anytime during market hours (manually)

## Overview

Intraday scalping strategy for NIFTY50 stocks using 3-min candles. Focus on liquidity, momentum bursts, VWAP mean reversion, and MACD crossovers.

## Usage

```bash
python stock_selector.py --strategy scalping
```

**Note**: Only works during market hours (9:15 AM - 3:30 PM IST) when intraday data is available.

## Filters (4 Core Filter Groups)

### 1. Liquidity Filters (Critical)
- **Minimum Volume**: ≥2M shares daily average
- **Bid-Ask Spread**: ≤0.1% (tight execution required)

### 2. Technical Filters
- **RSI-3**: Oversold (<20) or Overbought (>80) for reversals
- **EMA Alignment**: 9 EMA vs 20 EMA (trend direction)
- **Volume Spike**: Current 3-min volume ≥1.5x average
- **ATR**: Minimum 3 points movement potential

### 3. VWAP Filters
- **VWAP Deviation**: Price within 0.3% of VWAP
- **Setup Type**: Above/below VWAP for mean reversion

### 4. Momentum Filters
- **MACD Cross**: Bullish/bearish crossover signals
- **MACD Histogram**: Strength of momentum shift

## Scoring System (100 points)

| Factor | Weight | What it measures |
|--------|--------|-----------------|
| Liquidity | 30% | Volume + tight spreads (most critical) |
| Momentum | 25% | RSI-3 extremes + MACD crosses |
| VWAP Setup | 20% | Proximity to VWAP for entries |
| Trend Alignment | 15% | EMA 9 vs 20 separation |
| Volatility | 10% | ATR + volume spike strength |

**Total**: Top 10 stocks selected

## Trade Execution

### Entry
- **Immediate**: Enter at current price (scalping is fast)
- **Setup Types**:
  - RSI <20 + MACD bullish cross = BUY
  - RSI >80 + MACD bearish cross = SELL
  - VWAP bounce/rejection setups

### Stop Loss
- **0.35%** from entry price (tight stops)
- No room for error in scalping

### Target
- **0.4%** profit target
- **Risk-Reward**: 1:1.15 minimum
- Exit at target or reverse signal

### Position Sizing
- Risk 0.5-1% of capital per trade
- Max 3 scalp positions simultaneously
- Max 10-15 trades per day

## Configuration

Edit `config/scalping_config.py` to adjust:

```python
FILTER_THRESHOLDS = {
    "MIN_AVG_VOLUME": 2000000,      # Liquidity
    "MAX_SPREAD_PERCENT": 0.1,      # Tight spreads
    "RSI_OVERSOLD": 20,             # Buy zone
    "RSI_OVERBOUGHT": 80,           # Sell zone
    "VWAP_DEVIATION_MAX": 0.3,      # Mean reversion range
    "MIN_VOLUME_SPIKE": 1.5,        # Momentum confirmation
}

SCORING_WEIGHTS = {
    "liquidity": 30,
    "momentum": 25,
    "vwap_setup": 20,
    "trend_alignment": 15,
    "volatility": 10,
}

PROFIT_TARGET_PCT = 0.4   # Adjust targets
STOP_LOSS_PCT = 0.35      # Adjust stops
```

## Expected Performance

- **Trades per day**: 5-10 (when running manually)
- **Win rate target**: 60-70% (lower than swing due to tight stops)
- **Average R:R**: 1:1 to 1:1.5
- **Transaction costs**: Factor in brokerage + STT

## Best Time Windows

✅ **High activity periods**:
- 9:15-10:30 AM (opening volatility)
- 2:30-3:30 PM (closing hour)

❌ **Avoid**:
- 11:00 AM-1:30 PM (low volatility lunch period)
- Last 15 minutes (too erratic)

## Example Output

```json
{
  "symbol": "RELIANCE",
  "final_score": 78.5,
  "rsi_3": 18.2,
  "rsi_signal": "oversold_buy",
  "vwap_deviation": 0.15,
  "volume_spike": 2.3,
  "macd_cross": "bullish",
  "trade_setup": {
    "ltp": 2940.00,
    "entry": 2940.00,
    "stop_loss": 2929.71,
    "target": 2951.76,
    "vwap": 2938.50
  }
}
```

## Tips

1. **Market Hours Only**: Only run during 9:15 AM-3:30 PM IST
2. **Quick Execution**: Scalping requires immediate action
3. **Stick to Stops**: No exceptions - tight stops protect capital
4. **Transaction Costs**: Calculate if 0.4% target covers costs
5. **Max Trades**: Don't overtrade - quality over quantity
6. **NIFTY50 Only**: Guaranteed liquidity for instant fills
