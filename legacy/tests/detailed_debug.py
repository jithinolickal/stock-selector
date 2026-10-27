#!/usr/bin/env python3
import pandas as pd
from data_fetcher import UpstoxDataFetcher
from indicators import add_all_indicators
from filters import StockFilter

fetcher = UpstoxDataFetcher()
print("Fetching NIFTY50 index...")
nifty_df = fetcher.fetch_nifty50_index(days=400)
nifty_df = add_all_indicators(nifty_df)
print(f"NIFTY50 data: {len(nifty_df)} days\n")

test_stocks = ["RELIANCE", "TCS", "INFY"]

for symbol in test_stocks:
    print(f"\n{'='*60}\nANALYZING: {symbol}\n{'='*60}")
    
    instrument_key = fetcher.get_instrument_key(symbol)
    daily_df = fetcher.fetch_historical_daily(instrument_key, 400)
    daily_df = add_all_indicators(daily_df)
    
    print(f"Data points: {len(daily_df)} trading days")
    
    latest = daily_df.iloc[-1]
    print(f"\n📊 Latest Values:")
    print(f"  Close: {latest['close']:.2f}")
    print(f"  EMA20: {latest['ema_20']:.2f}" if pd.notna(latest['ema_20']) else "  EMA20: NaN")
    print(f"  EMA50: {latest['ema_50']:.2f}" if pd.notna(latest['ema_50']) else "  EMA50: NaN")
    print(f"  EMA200: {latest['ema_200']:.2f}" if pd.notna(latest['ema_200']) else "  EMA200: NaN")
    print(f"  RSI: {latest['rsi']:.2f}" if pd.notna(latest['rsi']) else "  RSI: NaN")
    print(f"  ADX: {latest['adx']:.2f}" if pd.notna(latest['adx']) else "  ADX: NaN")
    
    print(f"\n✅ Filter Checks:")
    if pd.notna(latest['ema_200']):
        print(f"  1. Price ({latest['close']:.2f}) > 200 EMA ({latest['ema_200']:.2f}): {latest['close'] > latest['ema_200']}")
    if pd.notna(latest['ema_20']) and pd.notna(latest['ema_50']):
        print(f"  2. Close > EMA20 > EMA50: {latest['close'] > latest['ema_20'] > latest['ema_50']}")
        print(f"  3. 50 EMA ({latest['ema_50']:.2f}) > 200 EMA ({latest['ema_200']:.2f}): {latest['ema_50'] > latest['ema_200']}" if pd.notna(latest['ema_200']) else "  3. NO EMA200")
    if pd.notna(latest['adx']):
        print(f"  5. ADX ({latest['adx']:.2f}) > 25: {latest['adx'] > 25}")
    if pd.notna(latest['rsi']):
        print(f"  6. RSI ({latest['rsi']:.2f}) in 40-65: {40 <= latest['rsi'] <= 65}")
    
    stock_filter = StockFilter(nifty_df)
    passed, results = stock_filter.apply_daily_filters(symbol, daily_df)
    
    print(f"\n❌ FAILED: {results.get('reason')}" if not passed else f"\n✅ PASSED")
