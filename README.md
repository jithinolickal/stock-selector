# NIFTY50 Stock Selector

Python script for selecting 1-3 high-probability NIFTY50 stocks for swing trading (1-3 day holds) based on rule-based technical filters.

## Features

- **14 Daily Filters**: EMA trends, ADX, RSI, ATR, volume, relative strength, higher lows pattern, volume expansion, weekly timeframe validation
- **4 Intraday Confirmations**: VWAP, candle patterns, volume (9:30-10:00 AM window)
- **Trade Quality Validation**: Stop distance, risk-reward ratio, support/resistance proximity checks
- **Multi-Timeframe Analysis**: Daily + Weekly + 15-min intraday data
- **Automated Trade Setups**: LTP, entry levels (EMA9/20), stop loss, targets calculated automatically
- **Market Analysis**: Gap analysis, previous day levels, support/resistance detection, NIFTY50 sentiment
- **Enhanced Scoring System**: 8 factors including weekly alignment, price action patterns, trade quality
- **Automated Data Fetching**: Uses Upstox API V3 for historical, weekly, and intraday data
- **Comprehensive JSON Output**: Saves results with trade setups and market analysis to `results/YYYY-MM-DD.json`

## Requirements

- Python 3.8+
- Upstox trading account with API access
- Upstox API access token

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd stock-selector
```

2. Create and activate virtual environment:
```bash
# Create virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Upstox access token
```

## Configuration

### Get Upstox Access Token

1. Sign up at [Upstox Developer Console](https://api.upstox.com/developer-console)
2. Create an app and get API key & secret
3. Generate access token from "My Apps" section
4. Add token to `.env` file:
```
UPSTOX_ACCESS_TOKEN=your_token_here
```

### Customize Filters (Optional)

Edit `config.py` to adjust:
- Filter thresholds (ADX, RSI ranges, ATR multiplier, etc.)
- Scoring weights
- NIFTY50 symbols list

## Usage

### Production Mode (Live Trading)

Run the script on days you want to trade (ideally between 9:30-10:00 AM IST):

```bash
python stock_selector.py
```

Or make it executable:
```bash
chmod +x stock_selector.py
./stock_selector.py
```

### Test Mode (For Testing Anytime)

Run with `--test-mode` flag to skip intraday filters and test with daily data only:

```bash
python stock_selector.py --test-mode
```

**⚠️ Important:**
- Test mode is ONLY for testing the script outside market hours
- It skips all intraday 15-min confirmations (VWAP, candle patterns, etc.)
- Results will be less accurate since intraday filters are critical for entry timing
- Always use production mode (without flag) during actual trading hours

## Output

### Console Output
```
============================================================
NIFTY50 STOCK SELECTOR - Swing Trading
Date: 2025-12-13 09:45:00
============================================================

📊 MARKET SENTIMENT (NIFTY50):
  Gap: +0.35% (Flat)
  Today: Bullish
  Favorable for trades

[Progress indicators...]

📊 FILTERING SUMMARY
------------------------------------------------------------
Total NIFTY50 stocks analyzed:    49
Passed daily filters:             12
Passed intraday confirmation:     5
Trade quality validation:         3
Final selection:                  3
------------------------------------------------------------

✅ TOP 3 STOCK(S) SELECTED
============================================================

#1 RELIANCE - Score: 87.45/100
------------------------------------------------------------
  Daily Trend:        ✓
  Above 200 EMA:      ✓
  ADX:                32.50
  RSI:                58.20
  ATR Ratio:          1.85x
  Relative Strength:  +3.45%
  Volume Confirmed:   ✓
  Intraday Bias:      bullish
  Entry Reason:       trend + momentum continuation

  📈 MARKET CONTEXT:
    Gap: +0.45% (Flat)
    Prev Day: H:₹2950.00 L:₹2920.00 C:₹2935.50
    Support: ₹2915.00 (1.2% below)
    Resistance: ₹2975.00 (1.8% above)

  💰 TRADE SETUP:
    LTP: ₹2940.00
    Entry (EMA9): ₹2928.50 | Target: ₹2951.20 (1.2R)
    Entry (EMA20): ₹2920.00 | Target: ₹2944.80 (1.2R)
    Stop Loss: ₹2918.00 (0.75% risk)

[Additional stocks...]

💾 Results saved to: results/2025-12-13.json
```

### JSON Output
Results are saved to `results/YYYY-MM-DD.json`:
```json
{
  "date": "2025-12-13",
  "timestamp": "2025-12-13T09:45:00",
  "total_selected": 3,
  "market_sentiment": {
    "gap_pct": 0.35,
    "gap_type": "Flat",
    "day_change_pct": 0.28,
    "today_trend": "Bullish",
    "recommendation": "Favorable for trades"
  },
  "stocks": [
    {
      "symbol": "RELIANCE",
      "daily_trend": true,
      "above_200ema": true,
      "ADX": 32.50,
      "RSI": 58.20,
      "ATR_ratio": 1.85,
      "relative_strength": 3.45,
      "volume_confirmed": true,
      "intraday_bias": "bullish",
      "final_score": 87.45,
      "entry_reason": "trend + momentum continuation",
      "trade_setup": {
        "ltp": 2940.00,
        "ema9": 2928.50,
        "ema20_intraday": 2920.00,
        "stop_loss": 2918.00,
        "target_ema9": 2951.20,
        "target_ema20": 2944.80,
        "risk_ema9": 10.50,
        "risk_ema20": 2.00
      },
      "market_analysis": {
        "gap": {
          "gap_pct": 0.45,
          "gap_type": "Flat"
        },
        "prev_day": {
          "high": 2950.00,
          "low": 2920.00,
          "close": 2935.50
        },
        "sr_levels": {
          "support": 2915.00,
          "resistance": 2975.00,
          "support_distance_pct": 1.2,
          "resistance_distance_pct": 1.8
        }
      }
    }
  ]
}
```

## Trading Rules (Manual Execution)

The script provides stock suggestions with automated trade setups. Execute trades manually using the provided levels:

- **Entry**: Use EMA9 or EMA20 entry levels shown in trade setup (wait for pullback)
- **Stop Loss**: Use calculated stop loss (typically 0.5-2.0% below entry)
- **Target**: Use calculated targets (minimum 1.2R risk-reward)
- **Risk per trade**: ≤ 0.5-1% of capital
- **Max trades/day**: 1-2
- **Quality Check**: Only trade if:
  - Market sentiment is favorable (NIFTY50 not down >1%)
  - Stock has ≥2% room to resistance
  - Stop loss is 0.5-2.0% away (not too tight/wide)

## Expected Behavior

- **Some days return 0 stocks** - this is correct behavior (prevents trading in weak market conditions)
- Average trades/week: 1-3 (strict filters ensure high quality)
- Expected win rate: 70-80% (improved with quality filters)
- Weekly return target: 1-2%
- Market conditions required:
  - Strong trending stocks (ADX ≥23, EMA alignment)
  - Weekly timeframe support
  - Multiple confirmation factors

## Project Structure

```
stock-selector/
├── stock_selector.py     # Main entry point
├── config.py            # Configuration & constants
├── data_fetcher.py      # Upstox API data fetching (daily, weekly, intraday)
├── indicators.py        # Technical indicators + price action patterns
├── filters.py           # Daily, weekly & intraday filters + trade quality validation
├── scorer.py            # Enhanced scoring system (8 factors)
├── trade_setup.py       # Automated trade setup calculator
├── market_analysis.py   # Gap, S/R, sentiment analysis
├── output.py            # Console & JSON output with full details
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Your credentials (gitignored)
├── results/             # Daily JSON outputs with trade setups
│   └── YYYY-MM-DD.json
└── tests/               # Test & debugging scripts
    ├── README.md        # Test scripts documentation
    ├── diagnose_filters.py
    ├── diagnose_new_filters.py
    ├── backtest_month.py
    └── ... (see tests/README.md)
```

## Filter Details

### Daily Filters (14 conditions)
1. Price > 200 EMA
2. Close > EMA20 > EMA50
3. 50 EMA > 200 EMA (bullish regime)
4. EMA20 slope positive (last 5 days)
5. ADX(14) ≥ 23 (trend strength)
6. RSI(14) between 42-62 (momentum zone)
7. ATR(14) ≥ 1.15× its 20-day average (volatility expansion)
8. Volume > 20-day average
9. Relative Strength vs NIFTY50 > 0
10. Minimum 2 consecutive higher lows (price action)
11. Volume expansion pattern (bonus - optional)
12. Consolidation breakout detection (bonus - optional)
13. Bullish candlestick patterns (bonus - optional)
14. Weekly timeframe alignment (required for swing trades)

### Intraday Confirmations (9:30-10:00 AM)
1. Price above VWAP
2. First two 15-min candles hold above VWAP
3. No large upper wick (>50% of range)
4. 15-min volume ≥ 1.2× 20-period average

### Trade Quality Validation
1. Stop loss distance: 0.5-2.0% from entry (not too tight/wide)
2. Risk-reward ratio: Minimum 1.5R
3. Distance to resistance: Minimum 2% (room to move)
4. Distance to support: Maximum 5% (not too far)

## Scoring Weights (Enhanced - 8 Factors)

- Trend strength (ADX + EMA): 25%
- RSI position: 15%
- Relative Strength vs NIFTY50: 15%
- Volume expansion: 10%
- ATR percentage: 5%
- Weekly alignment: 10%
- Price action patterns: 10%
- Trade quality: 10%

## Troubleshooting

### "UPSTOX_ACCESS_TOKEN not found"
- Ensure `.env` file exists with `UPSTOX_ACCESS_TOKEN=your_token`
- Check token is valid and not expired

### "Failed to fetch data"
- Check internet connection
- Verify Upstox API is accessible
- Check API rate limits haven't been exceeded
- Ensure market is open (for intraday data)

### "No stocks selected today"
- This is normal - not every day has suitable setups
- Check if market conditions are choppy/bearish
- Run `python tests/diagnose_filters.py` to see which filters are blocking stocks
- Run `python tests/backtest_month.py` to check historical pass rates

## License

MIT License

## Disclaimer

This tool is for educational and informational purposes only. It does not constitute financial advice. Trading stocks involves risk, and you should do your own research before making trading decisions.
