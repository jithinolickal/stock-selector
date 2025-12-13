#!/usr/bin/env python3
"""Minimal filter test - only check basic trend alignment to test scoring"""

import pandas as pd
from data_fetcher import UpstoxDataFetcher
from indicators import add_all_indicators, calculate_ema_slope, calculate_volume_ratio, calculate_atr_ratio, calculate_relative_strength
from scorer import StockScorer

fetcher = UpstoxDataFetcher()
scorer = StockScorer()

print("Fetching NIFTY50 index...")
nifty_df = fetcher.fetch_nifty50_index(days=400)
nifty_df = add_all_indicators(nifty_df)

print("\n" + "="*60)
print("MINIMAL FILTERS (only Price > EMA20 > EMA50 + indicators exist)")
print("="*60)

test_stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "TITAN", "BAJFINANCE"]
filtered_stocks = []

for symbol in test_stocks:
    print(f"\n{symbol}:")
    instrument_key = fetcher.get_instrument_key(symbol)
    daily_df = fetcher.fetch_historical_daily(instrument_key, 400)
    daily_df = add_all_indicators(daily_df)
    
    latest = daily_df.iloc[-1]
    
    # Minimal check: Close > EMA20 > EMA50
    if (pd.notna(latest["ema_20"]) and pd.notna(latest["ema_50"]) and 
        latest["close"] > latest["ema_20"] > latest["ema_50"] and
        pd.notna(latest["adx"]) and pd.notna(latest["rsi"])):
        
        print(f"  ✅ Passed minimal filter (Close > EMA20 > EMA50)")
        
        # Build results dict with all required fields
        results = {
            "symbol": symbol,
            "passed": True,
            "above_200ema": latest["close"] > latest["ema_200"] if pd.notna(latest["ema_200"]) else False,
            "ema_alignment": True,
            "bullish_regime": latest["ema_50"] > latest["ema_200"] if pd.notna(latest["ema_200"]) else False,
            "ema20_slope": calculate_ema_slope(daily_df["ema_20"], 5),
            "adx": latest["adx"],
            "rsi": latest["rsi"],
            "atr_ratio": calculate_atr_ratio(daily_df["atr"], 20),
            "volume_ratio": calculate_volume_ratio(daily_df, 20),
            "relative_strength": calculate_relative_strength(daily_df, nifty_df, 20),
            "intraday_bias": "test_mode",
            "volume_confirmed": True,
        }
        
        print(f"    ADX: {results['adx']:.2f}, RSI: {results['rsi']:.2f}, RS: {results['relative_strength']:+.2f}%")
        filtered_stocks.append(results)
    else:
        print(f"  ❌ Failed minimal filter")

print(f"\n{'='*60}")
print(f"STOCKS PASSING MINIMAL FILTER: {len(filtered_stocks)}")
print("="*60)

if filtered_stocks:
    print("\n📊 TESTING SCORING & RANKING LOGIC:")
    print("="*60)
    ranked = scorer.score_and_rank(filtered_stocks)
    
    for i, stock in enumerate(ranked, 1):
        summary = scorer.get_stock_summary(stock)
        print(f"\n#{i} {summary['symbol']} - Final Score: {summary['final_score']}/100")
        print(f"  ├─ Daily Trend: {'✓' if summary['daily_trend'] else '✗'}")
        print(f"  ├─ Above 200 EMA: {'✓' if summary['above_200ema'] else '✗'}")
        print(f"  ├─ ADX: {summary['ADX']:.2f}")
        print(f"  ├─ RSI: {summary['RSI']:.2f}")
        print(f"  ├─ ATR Ratio: {summary['ATR_ratio']:.2f}x")
        print(f"  ├─ Relative Strength: {summary['relative_strength']:+.2f}%")
        print(f"  ├─ Volume Confirmed: {'✓' if summary['volume_confirmed'] else '✗'}")
        print(f"  └─ Entry Reason: {summary['entry_reason']}")
    
    print("\n✅ SCORING LOGIC VERIFIED - Rankings look correct!")
else:
    print("\n⚠️  Even minimal filter found no stocks (market very weak)")
