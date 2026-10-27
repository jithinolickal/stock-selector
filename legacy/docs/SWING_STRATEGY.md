# Swing Trading Strategy

**Timeframe**: 1-3 day holds
**Best for**: Trending markets with clear directional moves
**Run time**: 9:30-10:00 AM IST daily

## Overview

This strategy identifies high-probability swing trade setups using multi-timeframe analysis (daily, weekly, 15-min intraday) with strict quality filters to reduce false positives.

## When to Use

✅ **Good market conditions**:
- NIFTY50 trending (not down >1%)
- Clear EMA alignment on daily charts
- Stocks showing higher lows pattern
- Weekly timeframe supporting daily trend

❌ **Avoid when**:
- Market choppy or rangebound
- NIFTY50 down significantly (>1%)
- Low volatility periods
- Many stocks failing filters (0 selected = sit out)

## Filters (14 Total)

### Daily Timeframe (11 filters)
1. **Price > 200 EMA**: Ensures long-term uptrend
2. **EMA Alignment**: Close > EMA20 > EMA50 (trending structure)
3. **Bullish Regime**: EMA50 > EMA200 (confirms uptrend)
4. **EMA20 Slope**: Positive over last 5 days (momentum building)
5. **ADX ≥ 23**: Minimum trend strength required
6. **RSI 42-62**: Momentum zone (not overbought/oversold)
7. **ATR ≥ 1.15x avg**: Volatility expansion (movement potential)
8. **Volume > avg**: Institutional participation
9. **Relative Strength > 0**: Outperforming NIFTY50
10. **Higher Lows (min 2)**: Price action confirmation
11. **Volume Expansion** (bonus): Multi-day volume increase

### Weekly Timeframe (1 filter)
12. **Weekly Alignment**: Higher timeframe supports daily trend

### Intraday 15-min (4 filters - 9:30-10:00 AM window)
13. **Price Above VWAP**: Institutional buying
14. **VWAP Hold**: First 2 candles stay above VWAP
15. **No Large Wicks**: Clean candles (< 50% wick)
16. **Volume Confirmation**: 15-min volume ≥ 1.2x average

### Trade Quality Validation
17. **Stop Distance**: 0.5-2.0% (not too tight/wide)
18. **Risk-Reward**: Minimum 1.5R
19. **Distance to Resistance**: ≥2% (room to run)
20. **Distance to Support**: ≤5% (not too far)

## Scoring System (100 points)

Stocks are ranked by weighted score:

| Factor | Weight | What it measures |
|--------|--------|-----------------|
| Trend Strength | 25% | ADX + EMA alignment quality |
| RSI Position | 15% | Optimal 50-55 range |
| Relative Strength | 15% | Outperformance vs NIFTY50 |
| Volume Expansion | 10% | Buying pressure |
| ATR Percentage | 5% | Volatility/opportunity |
| Weekly Alignment | 10% | Higher timeframe support |
| Price Action | 10% | Higher lows + patterns |
| Trade Quality | 10% | Stop quality + R:R |

**Total**: Top 1-3 stocks selected

## Trade Execution

### Entry
- **Primary**: Wait for pullback to EMA9 on 15-min chart
- **Secondary**: Pullback to EMA20 on 15-min chart
- Use limit orders at calculated entry levels

### Stop Loss
- **Method 1**: Below last 15-min swing low
- **Method 2**: ATR-based (whichever is safer)
- **Distance**: 0.5-2.0% from entry

### Target
- **Minimum**: 1.2R risk-reward
- **Method**: Calculate from entry-stop distance
- Trail stop to breakeven after 0.6R profit

### Position Sizing
- Risk 0.5-1% of capital per trade
- Max 2 swing positions simultaneously

## Configuration

Edit `config/swing_config.py` to adjust:

```python
FILTER_THRESHOLDS = {
    "ADX_MIN": 23,        # Trend strength minimum
    "RSI_MIN": 42,        # RSI range
    "RSI_MAX": 62,
    "ATR_MULTIPLIER": 1.15,  # Volatility expansion
    # ... more thresholds
}

SCORING_WEIGHTS = {
    "trend_strength": 25,
    "rsi_position": 15,
    # ... adjust weights
}
```

## Expected Performance

- **Trades per week**: 1-3 (strict filters)
- **Win rate target**: 70-80%
- **Average R:R**: 1.2-1.5R
- **Weekly return target**: 1-2%

**Note**: Some days will return 0 stocks - this is correct behavior preventing bad trades.

## Example Output

```json
{
  "symbol": "RELIANCE",
  "final_score": 87.45,
  "ADX": 32.5,
  "RSI": 58.2,
  "trade_setup": {
    "ltp": 2940.00,
    "entry_ema9": 2928.50,
    "stop_loss": 2918.00,
    "target_ema9": 2951.20
  },
  "market_analysis": {
    "gap_pct": 0.45,
    "support": 2915.00,
    "resistance": 2975.00
  }
}
```

## Tips

1. **Market First**: Check NIFTY50 sentiment before trading
2. **Quality Over Quantity**: 0 stocks selected = sit out, don't force trades
3. **Stick to Levels**: Use calculated entry/stop/target prices
4. **Trail Stops**: Protect profits as trade moves in your favor
5. **Review**: Track performance weekly to optimize thresholds
