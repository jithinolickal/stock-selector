#!/usr/bin/env python3
"""Test with ATR = 1.2x instead of 1.5x"""

import pandas as pd
from data_fetcher import UpstoxDataFetcher
from indicators import add_all_indicators
from filters import StockFilter
from config import FILTER_THRESHOLDS

# Temporarily override ATR threshold
FILTER_THRESHOLDS["ATR_MULTIPLIER"] = 1.2

fetcher = UpstoxDataFetcher()
print("Testing with ATR_MULTIPLIER = 1.2x (instead of 1.5x)\n")

nifty_df = fetcher.fetch_nifty50_index(days=400)
nifty_df = add_all_indicators(nifty_df)

test_stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "TITAN", "BAJFINANCE", "BHARTIARTL", "M&M", "LT"]

stock_filter = StockFilter(nifty_df)
passed_stocks = []

for symbol in test_stocks:
    instrument_key = fetcher.get_instrument_key(symbol)
    df = fetcher.fetch_historical_daily(instrument_key, 400)
    df = add_all_indicators(df)
    
    passed, results = stock_filter.apply_daily_filters(symbol, df)
    
    if passed:
        print(f"✅ {symbol} PASSED all filters")
        passed_stocks.append(symbol)
    else:
        print(f"❌ {symbol} - {results.get('reason')}")

print(f"\n{'='*60}")
print(f"RESULT: {len(passed_stocks)}/{len(test_stocks)} stocks passed with ATR = 1.2x")
print(f"{'='*60}")

if len(passed_stocks) > 0:
    print(f"\n✅ This would give you tradeable setups!")
    print(f"Passed stocks: {', '.join(passed_stocks)}")
else:
    print("\n⚠️  Still no stocks - market very weak or other filters too strict")
