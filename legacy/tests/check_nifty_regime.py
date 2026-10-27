#!/usr/bin/env python3
"""Check if NIFTY50 index itself is in bullish regime"""

from data_fetcher import UpstoxDataFetcher
from indicators import add_all_indicators
import pandas as pd

fetcher = UpstoxDataFetcher()
nifty_df = fetcher.fetch_nifty50_index(days=400)
nifty_df = add_all_indicators(nifty_df)

latest = nifty_df.iloc[-1]

print("="*60)
print("NIFTY50 INDEX - Market Regime Check")
print("="*60)
print(f"\nLatest Close: {latest['close']:.2f}")
print(f"EMA 20:  {latest['ema_20']:.2f}")
print(f"EMA 50:  {latest['ema_50']:.2f}")
print(f"EMA 200: {latest['ema_200']:.2f}")
print(f"\nADX: {latest['adx']:.2f}")
print(f"RSI: {latest['rsi']:.2f}")

print(f"\n{'='*60}")
print("MARKET REGIME:")
print(f"{'='*60}")

if latest['close'] > latest['ema_200']:
    print("✅ Price > 200 EMA: LONG-TERM BULL TREND")
else:
    print("❌ Price < 200 EMA: LONG-TERM BEAR TREND")

if latest['ema_50'] > latest['ema_200']:
    print("✅ 50 EMA > 200 EMA: BULLISH REGIME (Golden Cross)")
else:
    print("❌ 50 EMA < 200 EMA: BEARISH REGIME (Death Cross)")

if latest['close'] > latest['ema_20'] > latest['ema_50']:
    print("✅ Close > EMA20 > EMA50: SHORT-TERM UPTREND")
else:
    print("❌ EMA Alignment broken: SHORT-TERM WEAKNESS")

print(f"\n💡 CONCLUSION:")
if latest['ema_50'] < latest['ema_200']:
    print("   NIFTY50 is in BEARISH/CORRECTIVE phase (50 EMA < 200 EMA)")
    print("   → Most stocks will fail the '50 EMA > 200 EMA' regime filter")
    print("   → This filter might be TOO STRICT for Indian swing trading")
    print("\n   OPTIONS:")
    print("   1. Remove the 50 EMA > 200 EMA filter (trade individual stocks in uptrends)")
    print("   2. Wait for market to recover to bullish regime")
    print("   3. Switch to short-selling setups (reverse filters)")
else:
    print("   NIFTY50 is in BULLISH regime - Individual stocks have other issues")
