"""Output module for displaying and saving stock selection results"""

import json
import os
from datetime import datetime
from typing import List, Dict

from config.base_config import RESULTS_DIR


class OutputHandler:
    """Handles console output and JSON file saving"""

    @staticmethod
    def print_header():
        """Print script header"""
        print("\n" + "=" * 60)
        print("NIFTY50 STOCK SELECTOR - Swing Trading")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60 + "\n")

    @staticmethod
    def print_summary(
        total_stocks: int,
        filtered_daily: int,
        filtered_intraday: int,
        final_count: int,
    ):
        """
        Print filtering summary

        Args:
            total_stocks: Total stocks analyzed
            filtered_daily: Stocks that passed daily filters
            filtered_intraday: Stocks that passed intraday filters
            final_count: Final selected stocks count
        """
        print("\n📊 FILTERING SUMMARY")
        print("-" * 60)
        print(f"Total NIFTY50 stocks analyzed:    {total_stocks}")
        print(f"Passed daily filters:             {filtered_daily}")
        print(f"Passed intraday confirmation:     {filtered_intraday}")
        print(f"Final selection:                  {final_count}")
        print("-" * 60)

    @staticmethod
    def print_stock_details(stocks: List[Dict], trade_setups: Dict = None, stock_analysis: Dict = None):
        """
        Print detailed stock information to console

        Args:
            stocks: List of selected stocks with scores
            trade_setups: Optional dict of trade setups by symbol
            stock_analysis: Optional dict of market analysis by symbol
        """
        if not stocks:
            print("\n⚠️  NO STOCKS SELECTED TODAY")
            print("All stocks failed to meet the filtering criteria.")
            print("This is normal behavior - not every day has suitable setups.\n")
            return

        print(f"\n✅ TOP {len(stocks)} STOCK(S) SELECTED")
        print("=" * 60)

        for i, stock in enumerate(stocks, 1):
            symbol = stock['symbol']
            print(f"\n#{i} {symbol} - Score: {stock['final_score']}/100")
            print("-" * 60)

            # Check if ORB scalping or swing strategy
            if 'orb_breakout' in stock:
                # Scalping output
                print(f"  ORB Breakout:       {stock['orb_breakout'].upper()}")
                print(f"  ORB Range:          {stock['orb_low']} - {stock['orb_high']}")
                print(f"  Current Price:      {stock['current_price']}")
                print(f"  EMA 5/9:            {stock['ema_5']} / {stock['ema_9']}")
                print(f"  VWAP:               {stock['vwap']} (dev: {stock['vwap_deviation']}%)")
                print(f"  Volume Spike:       {stock['volume_spike']}x")
                print(f"  ATR:                {stock['atr']}")
                print(f"  RSI-7:              {stock['rsi_7']}")
            else:
                # Swing output
                print(f"  Daily Trend:        {'✓' if stock.get('daily_trend') else '✗'}")
                print(f"  Above 200 EMA:      {'✓' if stock.get('above_200ema') else '✗'}")
                print(f"  ADX:                {stock.get('ADX', 0):.2f}")
                print(f"  RSI:                {stock.get('RSI', 0):.2f}")
                print(f"  ATR Ratio:          {stock.get('ATR_ratio', 0):.2f}x")
                print(f"  Relative Strength:  {stock.get('relative_strength', 0):+.2f}%")
                print(f"  Volume Confirmed:   {'✓' if stock.get('volume_confirmed') else '✗'}")
                print(f"  Intraday Bias:      {stock.get('intraday_bias', '')}")
                print(f"  Entry Reason:       {stock.get('entry_reason', '')}")

            # Print market analysis if available
            if stock_analysis and symbol in stock_analysis:
                analysis = stock_analysis[symbol]
                print(f"\n  📈 MARKET CONTEXT:")

                # Gap info
                if "gap" in analysis and analysis["gap"]:
                    gap = analysis["gap"]
                    print(f"    Gap: {gap['gap_pct']:+.2f}% ({gap['gap_type']})")

                # Previous day levels
                if "prev_day" in analysis and analysis["prev_day"]:
                    prev = analysis["prev_day"]
                    print(f"    Prev Day: H:₹{prev['prev_high']:.2f} L:₹{prev['prev_low']:.2f} C:₹{prev['prev_close']:.2f}")

                # Support/Resistance
                if "sr_levels" in analysis and analysis["sr_levels"]:
                    sr = analysis["sr_levels"]
                    if "support" in sr:
                        print(f"    Support: ₹{sr['support']:.2f} ({sr['support_distance_pct']:.1f}% below)")
                    if "resistance" in sr:
                        print(f"    Resistance: ₹{sr['resistance']:.2f} ({sr['resistance_distance_pct']:.1f}% above)")

            # Print trade setup if available
            if trade_setups and symbol in trade_setups:
                from trade_setup import TradeSetupCalculator
                setup_str = TradeSetupCalculator.format_trade_setup(trade_setups[symbol], symbol)
                print(setup_str)

        print("\n" + "=" * 60)

    @staticmethod
    def save_to_json(stocks: List[Dict], trade_setups: Dict = None, market_sentiment: Dict = None, stock_analysis: Dict = None) -> str:
        """
        Save results to JSON file with date in filename

        Args:
            stocks: List of selected stocks
            trade_setups: Optional dict of trade setups by symbol
            market_sentiment: Optional market sentiment analysis
            stock_analysis: Optional dict of stock market analysis

        Returns:
            Path to saved file
        """
        # Create results directory if it doesn't exist
        os.makedirs(RESULTS_DIR, exist_ok=True)

        # Generate filename with current date
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str}.json"
        filepath = os.path.join(RESULTS_DIR, filename)

        # Prepare output data
        output_data = {
            "date": date_str,
            "timestamp": datetime.now().isoformat(),
            "total_selected": len(stocks),
            "market_sentiment": market_sentiment,
            "stocks": stocks,
        }

        # Add trade setups and market analysis for each stock
        if trade_setups or stock_analysis:
            for stock in output_data["stocks"]:
                symbol = stock.get("symbol")
                if symbol:
                    if trade_setups and symbol in trade_setups:
                        stock["trade_setup"] = trade_setups[symbol]
                    if stock_analysis and symbol in stock_analysis:
                        stock["market_analysis"] = stock_analysis[symbol]

        # Save to file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        return filepath

    @staticmethod
    def display_and_save(
        stocks: List[Dict],
        total_stocks: int,
        filtered_daily: int,
        filtered_intraday: int,
        trade_setups: Dict = None,
        market_sentiment: Dict = None,
        stock_analysis: Dict = None,
    ):
        """
        Main output function - display to console and save to JSON

        Args:
            stocks: List of selected stocks
            total_stocks: Total stocks analyzed
            filtered_daily: Stocks that passed daily filters
            filtered_intraday: Stocks that passed intraday filters
            trade_setups: Optional dict of trade setups by symbol
            market_sentiment: Optional market sentiment analysis
            stock_analysis: Optional dict of stock market analysis
        """
        # Print header
        OutputHandler.print_header()

        # Print market sentiment
        if market_sentiment:
            print("📊 MARKET SENTIMENT (NIFTY50):")
            print(f"  Gap: {market_sentiment['gap_pct']:+.2f}% ({market_sentiment['gap_type']})")
            print(f"  Today: {market_sentiment['sentiment']}")
            print(f"  {market_sentiment['recommendation']}\n")

        # Print summary
        OutputHandler.print_summary(
            total_stocks, filtered_daily, filtered_intraday, len(stocks)
        )

        # Print stock details
        OutputHandler.print_stock_details(stocks, trade_setups, stock_analysis)

        # Save to JSON
        try:
            filepath = OutputHandler.save_to_json(stocks, trade_setups, market_sentiment, stock_analysis)
            print(f"\n💾 Results saved to: {filepath}\n")
        except Exception as e:
            print(f"\n⚠️  Failed to save results to JSON: {str(e)}\n")

        # Print trading reminder
        if stocks:
            print("📝 TRADING NOTES:")
            print("- Entry: Wait for pullback to 9 or 20 EMA on 15-min chart")
            print("- Stop Loss: Below last 15-min swing low or 0.6-0.8× 15-min ATR")
            print("- Target: 1R to 1.3R")
            print("- Risk per trade: ≤ 0.5% of capital")
            print("- Max trades/day: 1-2\n")
