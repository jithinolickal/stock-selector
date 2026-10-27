#!/usr/bin/env python3
"""
NIFTY50 Stock Selector - Multi-Strategy Platform
Supports multiple trading strategies: swing (1-3 days), scalping (intraday), etc.
"""

import sys
import argparse
import pandas as pd

from strategies import StrategyFactory
from lib.data_fetcher import UpstoxDataFetcher
from lib.indicators import add_all_indicators
from lib.output_swing import OutputHandler
from lib.output_scalping import ScalpingOutputHandler
from lib.market_analysis import MarketAnalyzer


def main():
    """Main execution function"""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Multi-strategy NIFTY50 stock selector"
    )
    parser.add_argument(
        "--strategy",
        choices=StrategyFactory.get_available_strategies(),
        default="swing",
        help="Trading strategy to use (default: swing)"
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode (skip intraday filters, use daily filters only)",
    )
    args = parser.parse_args()

    try:
        # Initialize strategy
        if args.test_mode:
            print("⚠️  RUNNING IN TEST MODE - Intraday filters disabled")
            print("This mode is for testing only. Use live mode during market hours.\n")

        print(f"Initializing {args.strategy} strategy...")
        strategy = StrategyFactory.create_strategy(args.strategy)

        # Initialize data fetcher
        data_fetcher = UpstoxDataFetcher()

        # Step 1: Fetch NIFTY50 index data
        print("\nFetching NIFTY50 index data...")
        nifty_index_df = data_fetcher.fetch_nifty50_index()
        if nifty_index_df.empty:
            print("❌ Failed to fetch NIFTY50 index data. Exiting.")
            sys.exit(1)

        nifty_index_df = add_all_indicators(nifty_index_df)
        print("✓ NIFTY50 index data loaded")

        # Step 1.5: Analyze market sentiment
        print("\nAnalyzing market sentiment...")
        nifty_intraday = data_fetcher.fetch_intraday_15min(
            data_fetcher.get_instrument_key("NIFTY 50") or "NSE_INDEX|Nifty 50"
        ) if not args.test_mode else pd.DataFrame()
        market_sentiment = MarketAnalyzer.analyze_nifty_sentiment(nifty_index_df, nifty_intraday)

        print(f"NIFTY50 Sentiment: {market_sentiment['sentiment']} (Gap: {market_sentiment['gap_pct']:+.2f}%)")
        print(f"Recommendation: {market_sentiment['recommendation']}")

        # Warn if market is strongly bearish
        if market_sentiment['day_change_pct'] < -1.0:
            print("⚠️  WARNING: Market is down >1% - Consider reducing position sizes or sitting out")

        # Step 2: Fetch strategy-specific data
        all_stock_data = strategy.fetch_required_data(
            data_fetcher,
            strategy.config.NIFTY50_SYMBOLS
        )

        if not all_stock_data:
            print("❌ No stock data fetched. Exiting.")
            sys.exit(1)

        # Step 3: Run strategy analysis
        selected_stocks, trade_setups, stock_analysis, stats = strategy.analyze_and_select(
            all_stock_data,
            nifty_index_df,
            nifty_intraday,
            test_mode=args.test_mode
        )

        # Step 4: Display and save results
        if strategy.get_strategy_name() == "scalping":
            ScalpingOutputHandler.display_and_save(
                selected_stocks,
                trade_setups if not args.test_mode else None,
                market_sentiment,
                stats,
            )
        else:
            OutputHandler.display_and_save(
                selected_stocks,
                stats["total_stocks"],
                stats["daily_passed"],
                stats["intraday_passed"],
                trade_setups if not args.test_mode else None,
                market_sentiment,
                stock_analysis,
            )

    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
