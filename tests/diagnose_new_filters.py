"""Quick diagnostic to check which new filters are blocking stocks"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_fetcher import UpstoxDataFetcher
from indicators import add_all_indicators
from filters import StockFilter
from config import NIFTY50_SYMBOLS

# Initialize
data_fetcher = UpstoxDataFetcher()

# Fetch NIFTY50 index
nifty_index_df = data_fetcher.fetch_nifty50_index()
if nifty_index_df.empty:
    print("Failed to fetch NIFTY50 index")
    sys.exit(1)

nifty_index_df = add_all_indicators(nifty_index_df)

# Fetch data for first 10 stocks
print("Fetching sample stocks...")
stock_filter = StockFilter(nifty_index_df)

filter_reasons = {}

for i, symbol in enumerate(NIFTY50_SYMBOLS[:15]):
    print(f"[{i+1}/15] {symbol}...")

    instrument_key = data_fetcher.get_instrument_key(symbol)
    if not instrument_key:
        continue

    daily_df = data_fetcher.fetch_historical_daily(instrument_key)
    if daily_df.empty:
        continue

    daily_df = add_all_indicators(daily_df)

    # Apply daily filters
    passed, results = stock_filter.apply_daily_filters(symbol, daily_df)

    if not passed:
        reason = results.get("reason", "Unknown")
        if reason not in filter_reasons:
            filter_reasons[reason] = 0
        filter_reasons[reason] += 1
        print(f"  ❌ {reason}")
    else:
        print(f"  ✓ PASSED all filters!")

print("\n" + "="*60)
print("FILTER BLOCKING SUMMARY:")
print("="*60)
for reason, count in sorted(filter_reasons.items(), key=lambda x: x[1], reverse=True):
    print(f"{count:2d} stocks blocked by: {reason}")
