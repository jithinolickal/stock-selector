"""Swing trading strategy (1-3 day holds)"""

import sys
import pandas as pd
from typing import List, Dict

from strategies.base_strategy import BaseStrategy
from config import swing_config
from filters.swing_filters import StockFilter
from scorers.swing_scorer import StockScorer
from lib.indicators import add_all_indicators, add_intraday_indicators
from lib.market_analysis import MarketAnalyzer
from lib.trade_setup import TradeSetupCalculator


class SwingStrategy(BaseStrategy):
    """1-3 day swing trading strategy based on multi-timeframe analysis"""

    def __init__(self):
        super().__init__(swing_config)
        self.scorer = StockScorer()

    def get_strategy_name(self) -> str:
        return self.config.STRATEGY_NAME

    def fetch_required_data(self, data_fetcher, symbols: List[str]) -> Dict:
        """
        Fetch daily + weekly + 15-min intraday data for swing trading

        Args:
            data_fetcher: UpstoxDataFetcher instance
            symbols: List of symbols (not used, fetches all NIFTY50)

        Returns:
            Dictionary with stock data
        """
        # Fetch all NIFTY50 data (daily + intraday)
        all_stock_data = data_fetcher.fetch_all_nifty50_data()

        if not all_stock_data:
            return {}

        # Fetch weekly data for all stocks
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

        # Add indicators to all datasets
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

        return all_stock_data

    def analyze_and_select(
        self, all_data: Dict, nifty_index_df: pd.DataFrame, nifty_intraday: pd.DataFrame, test_mode: bool = False
    ) -> tuple:
        """
        Run swing trading analysis and return selected stocks

        Args:
            all_data: Dictionary with all stock data
            nifty_index_df: NIFTY50 index daily data
            nifty_intraday: NIFTY50 index intraday data
            test_mode: Whether running in test mode

        Returns:
            Tuple of (selected_stocks, trade_setups, stock_analysis, stats)
        """
        # Apply filters
        if test_mode:
            print("\nApplying daily filters only (test mode)...")
        else:
            print("\nApplying daily, weekly, and intraday filters...")

        stock_filter = StockFilter(nifty_index_df)

        filtered_stocks: List[Dict] = []
        daily_passed_count = 0
        intraday_passed_count = 0

        for symbol, data in all_data.items():
            if test_mode:
                # Test mode: only apply daily filters
                passed, results = stock_filter.apply_daily_filters(symbol, data["daily"])
                if passed:
                    daily_passed_count += 1
                    intraday_passed_count += 1
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

        # Score and rank
        print("\nScoring and ranking stocks...")
        ranked_stocks = self.scorer.score_and_rank(filtered_stocks)
        output_stocks = [self.scorer.get_stock_summary(stock) for stock in ranked_stocks]

        print(f"✓ Top {len(output_stocks)} stock(s) selected")

        # Calculate trade setups and market analysis
        trade_setups = {}
        stock_analysis = {}
        validated_stocks = []

        for stock in ranked_stocks:
            symbol = stock["symbol"]
            if symbol in all_data:
                daily_df = all_data[symbol]["daily"]
                intraday_df = all_data[symbol]["intraday"]

                # Market analysis
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
                if not test_mode:
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
                    validated_stocks.append(stock)

        # Update ranked stocks with only validated ones
        if not test_mode:
            ranked_stocks = validated_stocks
            print(f"✓ Trade quality validation: {len(ranked_stocks)} stocks passed")
            output_stocks = [self.scorer.get_stock_summary(stock) for stock in ranked_stocks]

        # Return stats
        stats = {
            "total_stocks": len(all_data),
            "daily_passed": daily_passed_count,
            "intraday_passed": intraday_passed_count,
            "final_selected": len(output_stocks),
        }

        return (output_stocks, trade_setups, stock_analysis, stats)
