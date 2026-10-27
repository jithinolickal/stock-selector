#!/usr/bin/env python3
"""Diagnose which filters are causing 100% rejection"""

import pandas as pd
from data_fetcher import UpstoxDataFetcher
from indicators import add_all_indicators, calculate_ema_slope, calculate_volume_ratio, calculate_atr_ratio, calculate_relative_strength
from config import FILTER_THRESHOLDS

fetcher = UpstoxDataFetcher()

print("Fetching data...")
nifty_df = fetcher.fetch_nifty50_index(days=400)
nifty_df = add_all_indicators(nifty_df)

test_stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "TITAN", "BAJFINANCE", "BHARTIARTL", "M&M", "LT"]

filter_failures = {
    "Price > 200 EMA": 0,
    "Close > EMA20 > EMA50": 0,
    "50 EMA > 200 EMA (Regime)": 0,
    "EMA20 slope positive": 0,
    "ADX > 25": 0,
    "RSI 40-65": 0,
    "ATR >= 1.5x avg": 0,
    "Volume > 20-day avg": 0,
    "RS vs NIFTY50 > 0": 0,
}

print(f"\nAnalyzing {len(test_stocks)} stocks (latest data)...\n")

for symbol in test_stocks:
    instrument_key = fetcher.get_instrument_key(symbol)
    df = fetcher.fetch_historical_daily(instrument_key, 400)
    df = add_all_indicators(df)
    
    latest = df.iloc[-1]
    
    # Check each filter
    if pd.isna(latest["ema_200"]) or latest["close"] <= latest["ema_200"]:
        filter_failures["Price > 200 EMA"] += 1
    
    if (pd.isna(latest["ema_20"]) or pd.isna(latest["ema_50"]) or 
        latest["close"] <= latest["ema_20"] or latest["ema_20"] <= latest["ema_50"]):
        filter_failures["Close > EMA20 > EMA50"] += 1
    
    if pd.isna(latest["ema_200"]) or latest["ema_50"] <= latest["ema_200"]:
        filter_failures["50 EMA > 200 EMA (Regime)"] += 1
    
    ema20_slope = calculate_ema_slope(df["ema_20"], FILTER_THRESHOLDS["EMA_SLOPE_DAYS"])
    if ema20_slope <= 0:
        filter_failures["EMA20 slope positive"] += 1
    
    if pd.isna(latest["adx"]) or latest["adx"] < FILTER_THRESHOLDS["ADX_MIN"]:
        filter_failures["ADX > 25"] += 1
    
    if (pd.isna(latest["rsi"]) or latest["rsi"] < FILTER_THRESHOLDS["RSI_MIN"] or 
        latest["rsi"] > FILTER_THRESHOLDS["RSI_MAX"]):
        filter_failures["RSI 40-65"] += 1
    
    atr_ratio = calculate_atr_ratio(df["atr"], period=20)
    if atr_ratio < FILTER_THRESHOLDS["ATR_MULTIPLIER"]:
        filter_failures["ATR >= 1.5x avg"] += 1
    
    volume_ratio = calculate_volume_ratio(df, period=20)
    if volume_ratio < FILTER_THRESHOLDS["VOLUME_MULTIPLIER"]:
        filter_failures["Volume > 20-day avg"] += 1
    
    rs = calculate_relative_strength(df, nifty_df, period=20)
    if rs <= 0:
        filter_failures["RS vs NIFTY50 > 0"] += 1

print("="*70)
print("FILTER REJECTION ANALYSIS (% of stocks failing each filter)")
print("="*70)

for filter_name, failure_count in sorted(filter_failures.items(), key=lambda x: x[1], reverse=True):
    pct = (failure_count / len(test_stocks)) * 100
    bar = "█" * int(pct / 5)
    print(f"{filter_name:30} {failure_count:2}/{len(test_stocks)} ({pct:5.1f}%) {bar}")

print("\n💡 DIAGNOSIS:")
most_restrictive = max(filter_failures.items(), key=lambda x: x[1])
print(f"Most restrictive filter: '{most_restrictive[0]}' - blocking {most_restrictive[1]}/{len(test_stocks)} stocks")

if filter_failures["50 EMA > 200 EMA (Regime)"] > len(test_stocks) * 0.7:
    print("\n⚠️  MARKET REGIME ISSUE:")
    print("   70%+ stocks have 50 EMA < 200 EMA (Death Cross)")
    print("   This means market is in BEARISH/CORRECTIVE phase")
    print("   → Consider: Relax this filter OR wait for market recovery")
    
if filter_failures["ATR >= 1.5x avg"] > len(test_stocks) * 0.7:
    print("\n⚠️  VOLATILITY ISSUE:")
    print("   ATR threshold (1.5x) might be too high for current market")
    print("   → Consider: Reduce to 1.2x or 1.3x")

if filter_failures["Volume > 20-day avg"] > len(test_stocks) * 0.7:
    print("\n⚠️  VOLUME ISSUE:")
    print("   Latest day's volume is below average (low participation)")
    print("   → This is a GOOD filter - avoid trading on low volume days")
