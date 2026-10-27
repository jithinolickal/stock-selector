"""ORB scalping diagnostic"""
import sys
sys.path.insert(0, ".")

from lib.data_fetcher import UpstoxDataFetcher
from filters.scalping_filters import ScalpingFilter
from lib.indicators import add_all_indicators, add_scalping_indicators

fetcher = UpstoxDataFetcher()
stock_filter = ScalpingFilter()

symbols = ["RELIANCE", "HCLTECH", "SBIN", "ICICIBANK", "INFY", "TCS"]
print("ORB Scalping Diagnostic:\n")

for symbol in symbols:
    print(f"{symbol}:")
    key = fetcher.get_instrument_key(symbol)
    if not key:
        continue

    try:
        daily = fetcher.fetch_historical_daily(key, days=100)
        intraday = fetcher.fetch_intraday_data(key, interval="5min")

        if daily.empty or intraday.empty:
            print(f"  No data ({len(intraday)} candles)\n")
            continue

        daily = add_all_indicators(daily)
        intraday = add_scalping_indicators(intraday)

        # Show ORB calculation
        orb_high, orb_low = stock_filter.calculate_orb(intraday)
        latest = intraday.iloc[-1]
        current_price = latest["close"]

        print(f"  Candles: {len(intraday)}")
        orb_str = f"{orb_low:.2f} - {orb_high:.2f}" if (orb_low and orb_high) else "N/A"
        print(f"  ORB Range: {orb_str}")
        print(f"  Current: {current_price:.2f}")

        if orb_high and orb_low:
            breakout_up = current_price > orb_high * 1.002
            breakout_down = current_price < orb_low * 0.998
            print(f"  Breakout: {'UP' if breakout_up else 'DOWN' if breakout_down else 'NONE'}")

        # Run filters
        passed, results = stock_filter.filter_stock(symbol, daily, intraday)

        print(f"  Stage failed: {results.get('stage', '?')}")
        print(f"  Reason: {results.get('reason', '?')[:80]}")

        if passed:
            print(f"  *** PASSED ALL FILTERS ***")

        print()
    except Exception as e:
        print(f"  Error: {str(e)[:80]}\n")
