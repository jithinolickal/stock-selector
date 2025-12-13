# Test Scripts

Utility scripts for testing and debugging the stock selector.

## Available Scripts

### Debugging & Analysis

**`debug_stock.py`**
- Quick debug of a single stock (RELIANCE)
- Shows latest indicator values and filter checks
- Usage: `python tests/debug_stock.py`

**`detailed_debug.py`**
- Detailed analysis of multiple stocks
- Shows which filters pass/fail for each stock
- Usage: `python tests/detailed_debug.py`

**`diagnose_filters.py`**
- Analyzes which filters are blocking the most stocks
- Shows rejection rate for each of the 9 filters
- Identifies overly restrictive filters
- Usage: `python tests/diagnose_filters.py`

### Scoring & Logic Testing

**`test_scoring_minimal.py`**
- Tests scoring logic with minimal filters
- Verifies ranking algorithm works correctly
- Shows how stocks are scored and ranked
- Usage: `python tests/test_scoring_minimal.py`

**`test_scoring.py`**
- Tests scoring with relaxed regime filter
- Usage: `python tests/test_scoring.py`

### Market Analysis

**`check_nifty_regime.py`**
- Checks if NIFTY50 index is in bullish/bearish regime
- Shows market-wide trend status
- Usage: `python tests/check_nifty_regime.py`

**`backtest_month.py`**
- Backtests how many stocks would pass filters over last 30 days
- Shows daily pass rate and summary statistics
- Useful for understanding if filters are too strict
- Usage: `python tests/backtest_month.py`

### API Testing

**`test_api_limit.py`**
- Tests Upstox API data availability limits
- Checks how many trading days are returned for different date ranges
- Usage: `python tests/test_api_limit.py`

**`test_relaxed_atr.py`**
- Tests with different ATR thresholds (1.2x, 1.3x, etc.)
- Usage: `python tests/test_relaxed_atr.py`

## Running Tests

All tests should be run from the project root with the virtual environment activated:

```bash
# Activate virtual environment
source venv/bin/activate

# Run any test
python tests/diagnose_filters.py
python tests/backtest_month.py
```

## Common Use Cases

### "Why are no stocks passing?"
1. Run `diagnose_filters.py` to see which filter is blocking
2. Run `check_nifty_regime.py` to check overall market condition
3. Run `backtest_month.py` to see historical pass rates

### "Is the scoring logic working?"
1. Run `test_scoring_minimal.py` to verify ranking algorithm
2. Check that higher-scoring stocks have better indicators

### "How much data does Upstox return?"
1. Run `test_api_limit.py` to check trading days vs calendar days

## Note

These scripts require:
- Active virtual environment
- `.env` file with `UPSTOX_ACCESS_TOKEN`
- Internet connection for API calls
