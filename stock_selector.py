#!/usr/bin/env python3
"""
NIFTY50 Stock Selector - Main Script
Selects 1-3 high-probability swing trade stocks based on technical filters
"""

import sys
import argparse
from typing import List, Dict
import pandas as pd

from data_fetcher import UpstoxDataFetcher
from indicators import add_all_indicators, add_intraday_indicators
from filters import StockFilter
from scorer import StockScorer
from output import OutputHandler
from market_analysis import MarketAnalyzer


def main():
    """Main execution function"""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="NIFTY50 Stock Selector for swing trading"
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode (skip intraday filters, use daily filters only)",
    )
    args = parser.parse_args()

    try:
        # Initialize components
        if args.test_mode:
            print("⚠️  RUNNING IN TEST MODE - Intraday filters disabled")
            print("This mode is for testing only. Use live mode during market hours.\n")

        print("Initializing stock selector...")
        data_fetcher = UpstoxDataFetcher()
        scorer = StockScorer()

        # Step 1: Fetch NIFTY50 index data for relative strength calculation
        print("\nFetching NIFTY50 index data...")
        nifty_index_df = data_fetcher.fetch_nifty50_index()
        if nifty_index_df.empty:
            print("❌ Failed to fetch NIFTY50 index data. Exiting.")
            sys.exit(1)

        nifty_index_df = add_all_indicators(nifty_index_df)
        print("✓ NIFTY50 index data loaded")

        # Step 1.5: Analyze market sentiment (NIFTY50)
        print("\nAnalyzing market sentiment...")
        nifty_intraday = data_fetcher.fetch_intraday_15min(data_fetcher.get_instrument_key("NIFTY 50") or "NSE_INDEX|Nifty 50") if not args.test_mode else pd.DataFrame()
        market_sentiment = MarketAnalyzer.analyze_nifty_sentiment(nifty_index_df, nifty_intraday)

        print(f"NIFTY50 Sentiment: {market_sentiment['sentiment']} (Gap: {market_sentiment['gap_pct']:+.2f}%)")
        print(f"Recommendation: {market_sentiment['recommendation']}")

        # Warn if market is strongly bearish
        if market_sentiment['day_change_pct'] < -1.0:
            print("⚠️  WARNING: Market is down >1% - Consider reducing position sizes or sitting out")

        # Step 2: Fetch data for all NIFTY50 stocks
        all_stock_data = data_fetcher.fetch_all_nifty50_data()

        if not all_stock_data:
            print("❌ No stock data fetched. Exiting.")
            sys.exit(1)

        # Step 3: Fetch weekly data for all stocks (for higher timeframe validation)
        print("\nFetching weekly candles for trend validation...")
        for symbol in all_stock_data:
            instrument_key = data_fetcher.get_instrument_key(symbol)
            if instrument_key:
                try:
                    weekly_df = data_fetcher.fetch_weekly_candles(instrument_key, weeks=52)
                    if not weekly_df.empty:
                        all_stock_data[symbol]["weekly"] = add_all_indicators(weekly_df)
                    else:
                        all_stock_data[symbol]["weekly"] = pd.DataFrame()
                except Exception:
                    all_stock_data[symbol]["weekly"] = pd.DataFrame()
            else:
                all_stock_data[symbol]["weekly"] = pd.DataFrame()

        print("✓ Weekly data fetched")

        # Step 4: Calculate indicators for all stocks
        print("\nCalculating technical indicators...")
        for symbol in all_stock_data:
            # Add daily indicators
            all_stock_data[symbol]["daily"] = add_all_indicators(
                all_stock_data[symbol]["daily"]
            )

            # Add intraday indicators if intraday data exists
            if not all_stock_data[symbol]["intraday"].empty:
                all_stock_data[symbol]["intraday"] = add_intraday_indicators(
                    all_stock_data[symbol]["intraday"]
                )

        print("✓ Indicators calculated")

        # Step 5: Apply filters
        if args.test_mode:
            print("\nApplying daily filters only (test mode)...")
        else:
            print("\nApplying daily, weekly, and intraday filters...")

        stock_filter = StockFilter(nifty_index_df)

        filtered_stocks: List[Dict] = []
        daily_passed_count = 0
        intraday_passed_count = 0

        for symbol, data in all_stock_data.items():
            if args.test_mode:
                # Test mode: only apply daily filters
                passed, results = stock_filter.apply_daily_filters(symbol, data["daily"])
                if passed:
                    daily_passed_count += 1
                    intraday_passed_count += 1  # Count as passed since skipped
                    # Add mock intraday results for output compatibility
                    results["symbol"] = symbol
                    results["intraday_bias"] = "test_mode"
                    results["volume_confirmed"] = True
                    results["weekly_trend"] = "test_mode"
                    results["weekly_suitable"] = None
                    filtered_stocks.append(results)
            else:
                # Production mode: apply daily, weekly, and intraday filters
                passed, results = stock_filter.filter_stock(
                    symbol, data["daily"], data["intraday"], data.get("weekly")
                )

                if results.get("stage") == "daily" and results.get("passed"):
                    daily_passed_count += 1

                if passed:
                    daily_passed_count += 1
                    intraday_passed_count += 1
                    filtered_stocks.append(results)

        print(f"✓ Filters applied: {len(filtered_stocks)} stocks passed all criteria")

        # Step 5: Score and rank
        print("\nScoring and ranking stocks...")
        ranked_stocks = scorer.score_and_rank(filtered_stocks)

        # Get clean summaries for output
        output_stocks = [scorer.get_stock_summary(stock) for stock in ranked_stocks]

        print(f"✓ Top {len(output_stocks)} stock(s) selected")

        # Step 6: Calculate trade setups and market analysis for selected stocks
        trade_setups = {}
        stock_analysis = {}
        validated_stocks = []

        for stock in ranked_stocks:
            symbol = stock["symbol"]
            if symbol in all_stock_data:
                daily_df = all_stock_data[symbol]["daily"]
                intraday_df = all_stock_data[symbol]["intraday"]

                # Market analysis (gap, prev day, S/R)
                analyzer = MarketAnalyzer()
                gap_info = analyzer.calculate_gap(daily_df, intraday_df)
                prev_day = analyzer.get_previous_day_data(daily_df)

                current_price = intraday_df["close"].iloc[-1] if not intraday_df.empty else daily_df["close"].iloc[-1]
                sr_levels = analyzer.find_support_resistance(daily_df, current_price, lookback=30)

                stock_analysis[symbol] = {
                    "gap": gap_info,
                    "prev_day": prev_day,
                    "sr_levels": sr_levels,
                    "current_price": current_price,
                }

                # Trade setup calculation and quality validation (production mode only)
                if not args.test_mode:
                    from trade_setup import TradeSetupCalculator
                    calculator = TradeSetupCalculator()
                    setup = calculator.calculate_setup(intraday_df, daily_df)

                    if setup:
                        trade_setups[symbol] = setup

                        # Validate trade quality
                        quality_passed, quality_metrics = StockFilter.validate_trade_quality(
                            setup, current_price, stock_analysis[symbol]
                        )

                        if quality_passed:
                            stock["trade_quality"] = quality_metrics
                            validated_stocks.append(stock)
                        else:
                            print(f"  ⚠️  {symbol} rejected: {quality_metrics.get('reason', 'Failed trade quality')}")
                else:
                    # Test mode - skip trade quality validation
                    validated_stocks.append(stock)

        # Update ranked stocks with only validated ones
        if not args.test_mode:
            ranked_stocks = validated_stocks
            print(f"✓ Trade quality validation: {len(ranked_stocks)} stocks passed")
            # Re-score after validation
            output_stocks = [scorer.get_stock_summary(stock) for stock in ranked_stocks]

        # Step 7: Display and save results
        OutputHandler.display_and_save(
            output_stocks,
            len(all_stock_data),
            daily_passed_count,
            intraday_passed_count,
            trade_setups if not args.test_mode else None,
            market_sentiment,
            stock_analysis,
        )

        print("✅ Stock selection completed successfully!\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user. Exiting...")
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
