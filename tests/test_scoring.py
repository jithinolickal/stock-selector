#!/usr/bin/env python3
"""Test scoring logic by temporarily relaxing the 50 EMA > 200 EMA filter"""

import pandas as pd
from data_fetcher import UpstoxDataFetcher
from indicators import add_all_indicators
from filters import StockFilter
from scorer import StockScorer

# Initialize
fetcher = UpstoxDataFetcher()
scorer = StockScorer()

print("Fetching NIFTY50 index...")
nifty_df = fetcher.fetch_nifty50_index(days=400)
nifty_df = add_all_indicators(nifty_df)

# Temporarily modify filter to skip regime check
class RelaxedFilter(StockFilter):
    def apply_daily_filters(self, symbol, df):
        if df.empty or len(df) < 200:
            return False, {"reason": "Insufficient data"}

        results = {}
        latest = df.iloc[-1]

        # Filter 1: Price > 200 EMA
        if pd.isna(latest["ema_200"]) or latest["close"] <= latest["ema_200"]:
            return False, {"reason": "Price not above 200 EMA"}
        results["above_200ema"] = True

        # Filter 2: Close > EMA20 > EMA50
        if (
            pd.isna(latest["ema_20"])
            or pd.isna(latest["ema_50"])
            or latest["close"] <= latest["ema_20"]
            or latest["ema_20"] <= latest["ema_50"]
        ):
            return False, {"reason": "EMA alignment failed"}
        results["ema_alignment"] = True

        # SKIP Filter 3: 50 EMA > 200 EMA (regime check)
        print(f"  {symbol}: Skipping regime check (50 EMA > 200 EMA)")
        results["bullish_regime"] = True  # Force pass

        # Filter 4: EMA20 slope positive
        from indicators import calculate_ema_slope
        from config import FILTER_THRESHOLDS
        ema20_slope = calculate_ema_slope(df["ema_20"], FILTER_THRESHOLDS["EMA_SLOPE_DAYS"])
        if ema20_slope <= 0:
            return False, {"reason": "EMA20 slope not positive"}
        results["ema20_slope"] = ema20_slope

        # Filter 5: ADX > 25
        if pd.isna(latest["adx"]) or latest["adx"] < FILTER_THRESHOLDS["ADX_MIN"]:
            return False, {"reason": f"ADX < {FILTER_THRESHOLDS['ADX_MIN']}"}
        results["adx"] = latest["adx"]

        # Filter 6: RSI between 40 and 65
        if (
            pd.isna(latest["rsi"])
            or latest["rsi"] < FILTER_THRESHOLDS["RSI_MIN"]
            or latest["rsi"] > FILTER_THRESHOLDS["RSI_MAX"]
        ):
            return False, {"reason": f"RSI not in range {FILTER_THRESHOLDS['RSI_MIN']}-{FILTER_THRESHOLDS['RSI_MAX']}"}
        results["rsi"] = latest["rsi"]

        # SKIP Filter 7: ATR >= 1.5x (also strict)
        from indicators import calculate_atr_ratio
        atr_ratio = calculate_atr_ratio(df["atr"], period=20)
        print(f"  {symbol}: ATR ratio {atr_ratio:.2f}x (relaxed from 1.5x requirement)")
        results["atr_ratio"] = atr_ratio

        # Filter 8: Volume > 20-day average
        from indicators import calculate_volume_ratio
        volume_ratio = calculate_volume_ratio(df, period=20)
        if volume_ratio < FILTER_THRESHOLDS["VOLUME_MULTIPLIER"]:
            return False, {"reason": "Volume below 20-day average"}
        results["volume_ratio"] = volume_ratio

        # Filter 9: RS vs NIFTY50 > 0
        from indicators import calculate_relative_strength
        rs = calculate_relative_strength(df, self.nifty_index_df, period=20)
        if rs <= 0:
            return False, {"reason": "Not outperforming NIFTY50"}
        results["relative_strength"] = rs

        results["passed"] = True
        results["symbol"] = symbol
        return True, results

# Test with relaxed filter
print("\n" + "="*60)
print("TESTING WITH RELAXED FILTERS (Skip regime + ATR checks)")
print("="*60)

test_stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]
filtered_stocks = []

relaxed_filter = RelaxedFilter(nifty_df)

for symbol in test_stocks:
    print(f"\n{symbol}:")
    instrument_key = fetcher.get_instrument_key(symbol)
    daily_df = fetcher.fetch_historical_daily(instrument_key, 400)
    daily_df = add_all_indicators(daily_df)
    
    passed, results = relaxed_filter.apply_daily_filters(symbol, daily_df)
    
    if passed:
        print(f"  ✅ PASSED all relaxed filters")
        # Add mock intraday fields
        results["intraday_bias"] = "test_mode"
        results["volume_confirmed"] = True
        filtered_stocks.append(results)
    else:
        print(f"  ❌ FAILED: {results.get('reason')}")

print(f"\n{'='*60}")
print(f"FILTERED STOCKS: {len(filtered_stocks)}")
print("="*60)

if filtered_stocks:
    print("\n📊 SCORING & RANKING:")
    ranked = scorer.score_and_rank(filtered_stocks)
    
    for i, stock in enumerate(ranked, 1):
        summary = scorer.get_stock_summary(stock)
        print(f"\n#{i} {summary['symbol']} - Score: {summary['final_score']}/100")
        print(f"  ADX: {summary['ADX']:.2f}")
        print(f"  RSI: {summary['RSI']:.2f}")
        print(f"  ATR Ratio: {summary['ATR_ratio']:.2f}x")
        print(f"  Relative Strength: {summary['relative_strength']:+.2f}%")
        print(f"  Entry Reason: {summary['entry_reason']}")
else:
    print("\nNo stocks passed even with relaxed filters!")
