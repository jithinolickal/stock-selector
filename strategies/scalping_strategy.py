"""Scalping strategy (intraday - minutes)"""

import sys
import pandas as pd
from typing import List, Dict

from strategies.base_strategy import BaseStrategy
from config import scalping_config
from filters.scalping_filters import ScalpingFilter
from scorers.scalping_scorer import ScalpingScorer
from lib.indicators import add_all_indicators, add_scalping_indicators


class ScalpingStrategy(BaseStrategy):
    """Intraday scalping strategy based on 3-min candles"""

    def __init__(self):
        super().__init__(scalping_config)
        self.scorer = ScalpingScorer()

    def get_strategy_name(self) -> str:
        return self.config.STRATEGY_NAME

    def fetch_required_data(self, data_fetcher, symbols: List[str]) -> Dict:
        """
        Fetch 3-min intraday + daily context data for scalping

        Args:
            data_fetcher: UpstoxDataFetcher instance
            symbols: List of symbols (NIFTY50)

        Returns:
            Dictionary with stock data
        """
        all_stock_data = {}

        print(f"\nFetching 3-min intraday data for {len(symbols)} stocks...")

        for i, symbol in enumerate(symbols, 1):
            print(f"[{i}/{len(symbols)}] {symbol}...", end=" ")

            instrument_key = data_fetcher.get_instrument_key(symbol)
            if not instrument_key:
                print("❌ (instrument not found)")
                continue

            try:
                # Fetch daily data (for liquidity check and context)
                daily_df = data_fetcher.fetch_historical_daily(
                    instrument_key,
                    days=self.config.HISTORICAL_DAYS
                )

                # Fetch 3-min intraday data
                intraday_df = data_fetcher.fetch_intraday_data(
                    instrument_key,
                    interval=self.config.INTRADAY_INTERVAL
                )

                if daily_df.empty:
                    print("❌ (no daily data)")
                    continue

                if intraday_df.empty:
                    print("❌ (no intraday data)")
                    continue

                all_stock_data[symbol] = {
                    "daily": daily_df,
                    "intraday": intraday_df,
                }

                print("✓")

            except Exception as e:
                print(f"❌ ({str(e)[:30]})")
                continue

        print(f"\nSuccessfully fetched: {len(all_stock_data)}/{len(symbols)} stocks")

        # Add indicators
        print("\nCalculating scalping indicators...")
        for symbol in all_stock_data:
            # Add basic indicators to daily (for context)
            all_stock_data[symbol]["daily"] = add_all_indicators(
                all_stock_data[symbol]["daily"]
            )

            # Add scalping-specific indicators to 3-min data
            all_stock_data[symbol]["intraday"] = add_scalping_indicators(
                all_stock_data[symbol]["intraday"]
            )

        print("✓ Indicators calculated")

        return all_stock_data

    def analyze_and_select(
        self, all_data: Dict, nifty_index_df: pd.DataFrame, nifty_intraday: pd.DataFrame, test_mode: bool = False
    ) -> tuple:
        """
        Run scalping analysis and return selected stocks

        Args:
            all_data: Dictionary with all stock data
            nifty_index_df: NIFTY50 index daily data
            nifty_intraday: NIFTY50 index intraday data
            test_mode: Whether running in test mode

        Returns:
            Tuple of (selected_stocks, trade_setups, stock_analysis, stats)
        """
        print("\nApplying scalping filters (liquidity, VWAP, momentum)...")

        stock_filter = ScalpingFilter()
        filtered_stocks: List[Dict] = []
        liquidity_passed = 0
        total_passed = 0

        for symbol, data in all_data.items():
            passed, results = stock_filter.filter_stock(
                symbol, data["daily"], data["intraday"]
            )

            # Track liquidity passes (first critical filter)
            if results.get("stage") != "liquidity":
                liquidity_passed += 1

            if passed:
                total_passed += 1
                filtered_stocks.append(results)

        print(f"✓ Filters applied: {len(filtered_stocks)} stocks passed all criteria")
        print(f"  (Liquidity: {liquidity_passed}, Final: {total_passed})")

        # Score and rank
        print("\nScoring and ranking stocks...")
        ranked_stocks = self.scorer.score_and_rank(filtered_stocks)
        output_stocks = [self.scorer.get_stock_summary(stock) for stock in ranked_stocks]

        print(f"✓ Top {len(output_stocks)} scalping opportunity/opportunities selected")

        # Calculate trade setups for scalping
        trade_setups = {}
        stock_analysis = {}

        for stock in ranked_stocks:
            symbol = stock["symbol"]
            if symbol in all_data:
                intraday_df = all_data[symbol]["intraday"]
                latest = intraday_df.iloc[-1]

                # Simple scalping setup
                ltp = latest["close"]
                vwap = latest.get("vwap", ltp)
                atr = latest.get("atr", ltp * 0.005)  # Fallback 0.5%

                # Entry near current price (scalping is immediate)
                stop_loss = ltp * (1 - self.config.STOP_LOSS_PCT / 100)
                target = ltp * (1 + self.config.PROFIT_TARGET_PCT / 100)

                trade_setups[symbol] = {
                    "ltp": round(ltp, 2),
                    "entry": round(ltp, 2),  # Immediate entry for scalping
                    "stop_loss": round(stop_loss, 2),
                    "target": round(target, 2),
                    "risk": round(ltp - stop_loss, 2),
                    "reward": round(target - ltp, 2),
                    "vwap": round(vwap, 2),
                }

                stock_analysis[symbol] = {
                    "current_price": ltp,
                    "vwap": vwap,
                    "atr": atr,
                }

        # Return stats
        stats = {
            "total_stocks": len(all_data),
            "daily_passed": liquidity_passed,
            "intraday_passed": total_passed,
            "final_selected": len(output_stocks),
        }

        return (output_stocks, trade_setups, stock_analysis, stats)
