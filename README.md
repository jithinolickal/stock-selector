# NIFTY50 Stock Selector

Python script for selecting 1-3 high-probability NIFTY50 stocks for swing trading (1-3 day holds) based on rule-based technical filters.

## Features

- **9 Daily Filters**: EMA trends, ADX, RSI, ATR, volume, relative strength vs NIFTY50
- **4 Intraday Confirmations**: VWAP, candle patterns, volume (9:30-10:00 AM window)
- **Weighted Scoring System**: Ranks stocks by trend strength, momentum, and relative performance
- **Automated Data Fetching**: Uses Upstox API V3 for historical and intraday data
- **Daily JSON Output**: Saves results to `results/YYYY-MM-DD.json`

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

[Progress indicators...]

📊 FILTERING SUMMARY
------------------------------------------------------------
Total NIFTY50 stocks analyzed:    50
Passed daily filters:             12
Passed intraday confirmation:     3
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
      "entry_reason": "trend + momentum continuation"
    }
  ]
}
```

## Trading Rules (Manual Execution)

The script provides stock suggestions only. Execute trades manually with these rules:

- **Entry**: Wait for pullback to 9 or 20 EMA on 15-min chart
- **Stop Loss**:
  - Below last 15-min swing low, OR
  - 0.6-0.8× 15-min ATR
- **Target**: 1R to 1.3R (risk-reward ratio)
- **Risk per trade**: ≤ 0.5% of capital
- **Max trades/day**: 1-2

## Expected Behavior

- **Some days return 0 stocks** - this is correct behavior
- Average trades/week: 2-4
- Expected win rate: 65-75%
- Weekly return target: 1-2%

## Project Structure

```
stock-selector/
├── stock_selector.py     # Main entry point
├── config.py            # Configuration & constants
├── data_fetcher.py      # Upstox API data fetching
├── indicators.py        # Technical indicators calculation
├── filters.py           # Daily & intraday filters
├── scorer.py            # Scoring & ranking system
├── output.py            # Console & JSON output
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Your credentials (gitignored)
├── results/             # Daily JSON outputs
│   └── YYYY-MM-DD.json
└── tests/               # Test & debugging scripts
    ├── README.md        # Test scripts documentation
    ├── diagnose_filters.py
    ├── backtest_month.py
    └── ... (see tests/README.md)
```

## Filter Details

### Daily Filters (9 conditions)
1. Price > 200 EMA
2. Close > EMA20 > EMA50
3. 50 EMA > 200 EMA (bullish regime)
4. EMA20 slope positive (last 5 days)
5. ADX(14) > 25
6. RSI(14) between 40-65
7. ATR(14) ≥ 1.0× its 20-day average (adjusted for Indian markets)
8. Volume > 20-day average
9. Relative Strength vs NIFTY50 > 0

### Intraday Confirmations (9:30-10:00 AM)
1. Price above VWAP
2. First two 15-min candles hold above VWAP
3. No large upper wick (>50% of range)
4. 15-min volume ≥ 1.2× 20-period average

## Scoring Weights

- Trend strength (ADX + EMA): 35%
- RSI position: 25%
- Relative Strength vs NIFTY50: 15%
- Volume expansion: 15%
- ATR percentage: 10%

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
