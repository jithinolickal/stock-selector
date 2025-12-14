# NIFTY50 Stock Selector

Multi-strategy stock selector for NIFTY50 swing trading and intraday scalping based on technical analysis.

## Quick Start

```bash
# Install dependencies
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up Upstox API token
cp .env.example .env
# Edit .env and add your UPSTOX_ACCESS_TOKEN

# Run swing trading strategy (default)
python stock_selector.py

# Run in test mode (outside market hours)
python stock_selector.py --test-mode
```

## Available Strategies

### Swing Trading (1-3 days)
```bash
python stock_selector.py --strategy swing
```
- **Best for**: Trending markets, directional moves
- **Hold time**: 1-3 days
- **Run time**: 9:30-10:00 AM IST
- **Details**: See [docs/SWING_STRATEGY.md](docs/SWING_STRATEGY.md)

### Scalping (Coming Soon - Phase 2)
```bash
python stock_selector.py --strategy scalping
```
- **Best for**: High liquidity periods, quick profits
- **Hold time**: 5-15 minutes
- **Run time**: Anytime during market hours
- **Details**: See [docs/SCALPING_STRATEGY.md](docs/SCALPING_STRATEGY.md)

## Output

Results are saved to `results/YYYY-MM-DD.json` with:
- Market sentiment (NIFTY50 analysis)
- Selected stocks with scores
- Trade setups (entry, stop loss, targets)
- Market analysis (gaps, support/resistance)

## Project Structure

```
stock-selector/
├── stock_selector.py        # Main entry point
├── strategies/              # Strategy implementations
│   ├── swing_strategy.py   # Swing trading (1-3 days)
│   └── scalping_strategy.py  # Scalping (Phase 2)
├── config/                  # Strategy configurations
│   ├── base_config.py      # Common settings
│   ├── swing_config.py     # Swing parameters
│   └── scalping_config.py  # Scalping parameters
├── filters/                 # Strategy-specific filters
├── scorers/                 # Strategy-specific scoring
├── lib/                     # Shared utilities
│   ├── data_fetcher.py     # Upstox API integration
│   ├── indicators.py       # Technical indicators
│   ├── market_analysis.py  # Gap/S/R analysis
│   ├── trade_setup.py      # Entry/stop/target calculation
│   └── output.py           # Console & JSON output
├── docs/                    # Strategy documentation
├── tests/                   # Testing & diagnostic tools
└── results/                 # Daily JSON outputs
```

## Configuration

Edit files in `config/` to adjust:
- Filter thresholds (RSI, ADX, ATR, etc.)
- Scoring weights
- Timeframes and data requirements

## Getting Upstox API Access

1. Sign up at [Upstox Developer Console](https://api.upstox.com/developer-console)
2. Create an app and get API credentials
3. Generate access token
4. Add to `.env` file

## Support

- **Issues**: [GitHub Issues](https://github.com/jithinolickal/stock-selector/issues)
- **Documentation**: See `docs/` folder for detailed strategy guides

## Disclaimer

This tool is for educational purposes only. Not financial advice. Trading involves risk.
