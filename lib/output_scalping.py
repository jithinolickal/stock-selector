"""Output handler for scalping strategy"""

import json
from datetime import datetime
from typing import List, Dict


class ScalpingOutputHandler:
    """Handles console output and JSON saving for scalping strategy"""

    @staticmethod
    def print_header():
        """Print scalping header"""
        print("\n" + "=" * 60)
        print("NIFTY50 STOCK SELECTOR - Scalping (ORB)")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60 + "\n")

    @staticmethod
    def print_summary(
        total_stocks: int,
        filtered_liquidity: int,
        filtered_final: int,
    ):
        """Print scalping filtering summary"""
        print("\n📊 FILTERING SUMMARY")
        print("-" * 60)
        print(f"Total NIFTY50 stocks analyzed:    {total_stocks}")
        print(f"Passed liquidity filters:         {filtered_liquidity}")
        print(f"Passed all ORB filters:           {filtered_final}")
        print(f"Final selection:                  {filtered_final}")
        print("-" * 60)

    @staticmethod
    def print_stock_details(stocks: List[Dict], trade_setups: Dict = None):
        """Print scalping stock details"""
        if not stocks:
            print("\n⚠️  NO SCALPING OPPORTUNITIES TODAY")
            print("No stocks passed ORB filters.")
            print("This is normal - ORB breakouts don't occur every day.\n")
            return

        print(f"\n✅ TOP {len(stocks)} SCALPING OPPORTUNITY/OPPORTUNITIES")
        print("=" * 60)

        for i, stock in enumerate(stocks, 1):
            symbol = stock['symbol']
            print(f"\n#{i} {symbol} - Score: {stock['final_score']:.2f}/100")
            print("-" * 60)

            # ORB details
            print(f"  ORB Breakout:       {stock['orb_breakout'].upper()}")
            print(f"  ORB Range:          ₹{stock['orb_low']:.2f} - ₹{stock['orb_high']:.2f}")
            print(f"  Current Price:      ₹{stock['current_price']:.2f}")

            # Technical indicators
            print(f"\n  📊 TECHNICAL:")
            print(f"    EMA 5:            ₹{stock['ema_5']:.2f}")
            print(f"    EMA 9:            ₹{stock['ema_9']:.2f}")
            print(f"    VWAP:             ₹{stock['vwap']:.2f} (deviation: {stock['vwap_deviation']:.2f}%)")
            print(f"    RSI-7:            {stock['rsi_7']:.1f}")
            print(f"    ATR:              {stock['atr']:.2f}")
            print(f"    Volume Spike:     {stock['volume_spike']:.2f}x")

            # Trade setup
            if trade_setups and symbol in trade_setups:
                setup = trade_setups[symbol]
                print(f"\n  💰 TRADE SETUP:")
                print(f"    Entry:            ₹{setup['entry']:.2f} (immediate)")
                print(f"    Stop Loss:        ₹{setup['stop_loss']:.2f}")
                print(f"    Target:           ₹{setup['target']:.2f}")
                print(f"    Risk:             ₹{setup['risk']:.2f}")
                print(f"    Reward:           ₹{setup['reward']:.2f}")
                rr_ratio = setup['reward'] / setup['risk'] if setup['risk'] > 0 else 0
                print(f"    R:R Ratio:        1:{rr_ratio:.2f}")

        print("\n" + "=" * 60)

    @staticmethod
    def save_to_json(
        stocks: List[Dict],
        trade_setups: Dict = None,
        market_sentiment: Dict = None,
    ) -> str:
        """Save scalping results to JSON"""
        output = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().isoformat(),
            "strategy": "scalping",
            "total_selected": len(stocks),
            "market_sentiment": market_sentiment or {},
            "stocks": []
        }

        for stock in stocks:
            stock_data = {
                "symbol": stock["symbol"],
                "score": stock["final_score"],
                "orb_breakout": stock.get("orb_breakout", ""),
                "orb_high": stock.get("orb_high", 0),
                "orb_low": stock.get("orb_low", 0),
                "current_price": stock.get("current_price", 0),
                "ema_5": stock.get("ema_5", 0),
                "ema_9": stock.get("ema_9", 0),
                "vwap": stock.get("vwap", 0),
                "vwap_deviation": stock.get("vwap_deviation", 0),
                "volume_spike": stock.get("volume_spike", 0),
                "atr": stock.get("atr", 0),
                "rsi_7": stock.get("rsi_7", 0),
            }

            # Add trade setup
            if trade_setups and stock["symbol"] in trade_setups:
                stock_data["trade_setup"] = trade_setups[stock["symbol"]]

            output["stocks"].append(stock_data)

        # Save to file
        filename = f"results/{datetime.now().strftime('%Y-%m-%d')}_scalping.json"
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)

        return filename

    @staticmethod
    def display_and_save(
        stocks: List[Dict],
        trade_setups: Dict = None,
        market_sentiment: Dict = None,
        stats: Dict = None,
    ):
        """Display and save scalping results"""
        # Print header
        ScalpingOutputHandler.print_header()

        # Print market sentiment
        if market_sentiment:
            print("📊 MARKET SENTIMENT (NIFTY50):")
            print(f"  Gap: {market_sentiment.get('gap_pct', 0):+.2f}% ({market_sentiment.get('gap_type', 'Unknown')})")
            print(f"  Today: {market_sentiment.get('sentiment', 'Unknown')}")
            print(f"  {market_sentiment.get('recommendation', '')}\n")

        # Print summary
        if stats:
            ScalpingOutputHandler.print_summary(
                stats.get('total_stocks', 0),
                stats.get('daily_passed', 0),
                stats.get('final_selected', 0)
            )

        # Print stock details
        ScalpingOutputHandler.print_stock_details(stocks, trade_setups)

        # Save to JSON
        filename = ScalpingOutputHandler.save_to_json(stocks, trade_setups, market_sentiment)
        print(f"\n💾 Results saved to: {filename}\n")
