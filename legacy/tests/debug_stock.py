#!/usr/bin/env python3
"""Debug script to analyze why stocks are failing filters"""

import pandas as pd
from data_fetcher import UpstoxDataFetcher
from indicators import add_all_indicators
from filters import StockFilter

# Initialize
fetcher = UpstoxDataFetcher()

# Fetch NIFTY50 index
print("Fetching NIFTY50 index...")
nifty_df = fetcher.fetch_nifty50_index()
nifty_df = add_all_indicators(nifty_df)

# Test with RELIANCE
print("\nFetching RELIANCE data...")
instrument_key = fetcher.get_instrument_key("RELIANCE")
print(f"Instrument key: {instrument_key}")

daily_df = fetcher.fetch_historical_daily(instrument_key, 200)
daily_df = add_all_indicators(daily_df)

print(f"\nData fetched: {len(daily_df)} days")
print("\n=== Latest Values ===")
latest = daily_df.iloc[-1]
print(f"Close: {latest['close']:.2f}")
print(f"EMA20: {latest['ema_20'] if pd.notna(latest['ema_20']) else 'NaN'}")
print(f"EMA50: {latest['ema_50'] if pd.notna(latest['ema_50']) else 'NaN'}")
print(f"EMA200: {latest['ema_200'] if pd.notna(latest['ema_200']) else 'NaN'}")
print(f"RSI: {latest['rsi'] if pd.notna(latest['rsi']) else 'NaN'}")
print(f"ADX: {latest['adx'] if pd.notna(latest['adx']) else 'NaN'}")
print(f"ATR: {latest['atr'] if pd.notna(latest['atr']) else 'NaN'}")

# Check how many valid EMA200 values we have
valid_ema200 = daily_df['ema_200'].notna().sum()
print(f"\nValid EMA200 values: {valid_ema200}/{len(daily_df)}")

# Apply filters
print("\n=== Applying Filters ===")
stock_filter = StockFilter(nifty_df)
passed, results = stock_filter.apply_daily_filters("RELIANCE", daily_df)

print(f"Passed: {passed}")
print(f"Failure reason: {results.get('reason', 'All passed!')}")
