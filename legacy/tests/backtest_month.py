#!/usr/bin/env python3
"""Check how many stocks would have passed daily filters over the past month"""

import pandas as pd
from datetime import datetime, timedelta
from data_fetcher import UpstoxDataFetcher
from indicators import add_all_indicators
from filters import StockFilter

fetcher = UpstoxDataFetcher()

print("Fetching NIFTY50 index...")
nifty_df = fetcher.fetch_nifty50_index(days=400)
nifty_df = add_all_indicators(nifty_df)

# Get a few representative stocks
test_stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "TITAN", "BAJFINANCE", "BHARTIARTL"]
print(f"\nFetching data for {len(test_stocks)} test stocks...")

all_data = {}
for symbol in test_stocks:
    instrument_key = fetcher.get_instrument_key(symbol)
    daily_df = fetcher.fetch_historical_daily(instrument_key, 400)
    daily_df = add_all_indicators(daily_df)
    all_data[symbol] = daily_df

# Get last 30 trading days
last_30_days = all_data["RELIANCE"].tail(30).index

print(f"\n{'='*80}")
print(f"BACKTEST: Daily Filter Pass Rate (Last {len(last_30_days)} Trading Days)")
print(f"{'='*80}\n")

stock_filter = StockFilter(nifty_df)

# For each day, check how many stocks pass
daily_results = []

for day_idx, date in enumerate(last_30_days):
    passed_count = 0
    passed_symbols = []
    
    for symbol, df in all_data.items():
        # Get data up to this date
        historical_df = df[df.index <= date]
        
        if len(historical_df) < 250:  # Need enough data
            continue
        
        passed, results = stock_filter.apply_daily_filters(symbol, historical_df)
        
        if passed:
            passed_count += 1
            passed_symbols.append(symbol)
    
    daily_results.append({
        'date': date,
        'count': passed_count,
        'symbols': passed_symbols
    })
    
    print(f"{date.strftime('%Y-%m-%d')}: {passed_count}/{len(test_stocks)} stocks passed | {', '.join(passed_symbols) if passed_symbols else 'None'}")

# Summary
print(f"\n{'='*80}")
print("SUMMARY:")
print(f"{'='*80}")

counts = [r['count'] for r in daily_results]
days_with_stocks = sum(1 for c in counts if c > 0)
avg_stocks = sum(counts) / len(counts)

print(f"Days with at least 1 stock passing: {days_with_stocks}/{len(last_30_days)} ({days_with_stocks/len(last_30_days)*100:.1f}%)")
print(f"Average stocks passing per day: {avg_stocks:.1f}")
print(f"Max stocks in a day: {max(counts)}")
print(f"Days with zero stocks: {len(counts) - days_with_stocks}")

print("\n💡 INTERPRETATION:")
if days_with_stocks < len(last_30_days) * 0.3:
    print("  Market has been in a WEAK/CHOPPY phase - Few quality setups")
    print("  This is NORMAL - The filters are protecting you from low-probability trades")
elif days_with_stocks > len(last_30_days) * 0.6:
    print("  Market has been in a STRONG TRENDING phase - Many opportunities")
else:
    print("  Market has been MODERATE - Some opportunities available")

print("\n✅ Remember: 'Average trades/week: 2-4' from the plan")
print("   Not trading = Avoiding bad setups = Capital preservation!")
