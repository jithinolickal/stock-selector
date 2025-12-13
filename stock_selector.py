#!/usr/bin/env python3
"""
NIFTY50 Stock Selector - Main Script
Selects 1-3 high-probability swing trade stocks based on technical filters
"""

import sys
import argparse
from typing import List, Dict

from data_fetcher import UpstoxDataFetcher
from indicators import add_all_indicators, add_intraday_indicators
from filters import StockFilter
from scorer import StockScorer
from output import OutputHandler


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

        # Step 2: Fetch data for all NIFTY50 stocks
        all_stock_data = data_fetcher.fetch_all_nifty50_data()

        if not all_stock_data:
            print("❌ No stock data fetched. Exiting.")
            sys.exit(1)

        # Step 3: Calculate indicators for all stocks
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

        # Step 4: Apply filters
        if args.test_mode:
            print("\nApplying daily filters only (test mode)...")
        else:
            print("\nApplying daily and intraday filters...")

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
                    filtered_stocks.append(results)
            else:
                # Production mode: apply both daily and intraday filters
                passed, results = stock_filter.filter_stock(
                    symbol, data["daily"], data["intraday"]
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

        # Step 6: Display and save results
        OutputHandler.display_and_save(
            output_stocks,
            len(all_stock_data),
            daily_passed_count,
            intraday_passed_count,
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
