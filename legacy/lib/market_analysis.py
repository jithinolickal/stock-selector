"""Market analysis module for gap analysis, support/resistance, and market sentiment"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class MarketAnalyzer:
    """Analyzes market conditions, gaps, support/resistance levels"""

    @staticmethod
    def calculate_gap(daily_df: pd.DataFrame, intraday_df: pd.DataFrame) -> Dict:
        """
        Calculate gap between today's open and previous close

        Args:
            daily_df: Daily OHLCV DataFrame
            intraday_df: Today's intraday DataFrame

        Returns:
            Dict with gap analysis
        """
        if daily_df.empty or len(daily_df) < 2:
            return {"gap_pct": 0, "gap_type": "unknown", "prev_close": 0}

        prev_close = daily_df["close"].iloc[-2]  # Yesterday's close

        # Get today's open from intraday data if available
        if not intraday_df.empty:
            today_open = intraday_df["open"].iloc[0]
        else:
            # Fallback to latest daily candle's open
            today_open = daily_df["open"].iloc[-1]

        gap_pct = ((today_open - prev_close) / prev_close) * 100

        # Classify gap
        if gap_pct > 2.0:
            gap_type = "Strong Bullish"
        elif gap_pct > 0.5:
            gap_type = "Bullish"
        elif gap_pct > -0.5:
            gap_type = "Flat"
        elif gap_pct > -2.0:
            gap_type = "Bearish"
        else:
            gap_type = "Strong Bearish"

        return {
            "gap_pct": gap_pct,
            "gap_type": gap_type,
            "prev_close": prev_close,
            "today_open": today_open,
        }

    @staticmethod
    def get_previous_day_data(daily_df: pd.DataFrame) -> Dict:
        """
        Get previous day's OHLC data

        Args:
            daily_df: Daily OHLCV DataFrame

        Returns:
            Dict with previous day data
        """
        if daily_df.empty or len(daily_df) < 2:
            return {}

        prev_day = daily_df.iloc[-2]

        return {
            "prev_high": prev_day["high"],
            "prev_low": prev_day["low"],
            "prev_close": prev_day["close"],
            "prev_volume": prev_day["volume"],
        }

    @staticmethod
    def find_support_resistance(
        daily_df: pd.DataFrame, current_price: float, lookback: int = 30
    ) -> Dict:
        """
        Find nearest support and resistance levels from swing highs/lows

        Args:
            daily_df: Daily OHLCV DataFrame
            current_price: Current stock price
            lookback: Number of days to look back for swing points

        Returns:
            Dict with support/resistance levels
        """
        if daily_df.empty or len(daily_df) < lookback:
            return {}

        recent_data = daily_df.tail(lookback)

        # Find swing highs (local maximas)
        highs = recent_data["high"].values
        swing_highs = []
        for i in range(2, len(highs) - 2):
            if highs[i] > highs[i - 1] and highs[i] > highs[i - 2] and \
               highs[i] > highs[i + 1] and highs[i] > highs[i + 2]:
                swing_highs.append(highs[i])

        # Find swing lows (local minimas)
        lows = recent_data["low"].values
        swing_lows = []
        for i in range(2, len(lows) - 2):
            if lows[i] < lows[i - 1] and lows[i] < lows[i - 2] and \
               lows[i] < lows[i + 1] and lows[i] < lows[i + 2]:
                swing_lows.append(lows[i])

        # Find nearest resistance (swing high above current price)
        resistances = [h for h in swing_highs if h > current_price]
        nearest_resistance = min(resistances) if resistances else None

        # Find nearest support (swing low below current price)
        supports = [l for l in swing_lows if l < current_price]
        nearest_support = max(supports) if supports else None

        result = {}

        if nearest_support:
            support_distance = ((current_price - nearest_support) / current_price) * 100
            result["support"] = nearest_support
            result["support_distance_pct"] = support_distance

        if nearest_resistance:
            resistance_distance = ((nearest_resistance - current_price) / current_price) * 100
            result["resistance"] = nearest_resistance
            result["resistance_distance_pct"] = resistance_distance

        return result

    @staticmethod
    def check_price_location(
        current_price: float, prev_high: float, prev_low: float, prev_close: float
    ) -> str:
        """
        Check where current price is relative to previous day's range

        Args:
            current_price: Current price
            prev_high: Previous day's high
            prev_low: Previous day's low
            prev_close: Previous day's close

        Returns:
            Description of price location
        """
        if current_price > prev_high:
            return "Above prev high (breakout)"
        elif current_price < prev_low:
            return "Below prev low (breakdown)"
        elif current_price > prev_close:
            return "Above prev close (bullish)"
        elif current_price < prev_close:
            return "Below prev close (bearish)"
        else:
            return "At prev close (neutral)"

    @staticmethod
    def analyze_nifty_sentiment(nifty_daily_df: pd.DataFrame, nifty_intraday_df: pd.DataFrame) -> Dict:
        """
        Analyze NIFTY50 market sentiment

        Args:
            nifty_daily_df: NIFTY50 daily DataFrame
            nifty_intraday_df: NIFTY50 intraday DataFrame

        Returns:
            Dict with market sentiment analysis
        """
        gap_analysis = MarketAnalyzer.calculate_gap(nifty_daily_df, nifty_intraday_df)

        # Get current NIFTY price
        if not nifty_intraday_df.empty:
            current_nifty = nifty_intraday_df["close"].iloc[-1]
        else:
            current_nifty = nifty_daily_df["close"].iloc[-1]

        prev_close = gap_analysis.get("prev_close", current_nifty)
        day_change_pct = ((current_nifty - prev_close) / prev_close) * 100

        # Determine market sentiment
        if day_change_pct > 1.0:
            sentiment = "Strong Bullish"
            recommendation = "Full confidence - good day for longs"
        elif day_change_pct > 0.3:
            sentiment = "Bullish"
            recommendation = "Favorable for trades"
        elif day_change_pct > -0.3:
            sentiment = "Neutral"
            recommendation = "Be selective"
        elif day_change_pct > -1.0:
            sentiment = "Bearish"
            recommendation = "Reduce position sizes"
        else:
            sentiment = "Strong Bearish"
            recommendation = "Avoid new longs - sit out"

        return {
            "gap_pct": gap_analysis["gap_pct"],
            "gap_type": gap_analysis["gap_type"],
            "day_change_pct": day_change_pct,
            "sentiment": sentiment,
            "recommendation": recommendation,
            "current_price": current_nifty,
        }

    @staticmethod
    def check_weekly_trend(weekly_df: pd.DataFrame) -> Dict:
        """
        Check weekly timeframe trend

        Args:
            weekly_df: Weekly OHLCV DataFrame with indicators

        Returns:
            Dict with weekly trend analysis
        """
        if weekly_df.empty or len(weekly_df) < 50:
            return {"weekly_trend": "Unknown", "reason": "Insufficient data"}

        latest = weekly_df.iloc[-1]

        # Check weekly EMA alignment
        if pd.notna(latest.get("ema_20")) and pd.notna(latest.get("ema_50")):
            ema_aligned = latest["close"] > latest["ema_20"] > latest["ema_50"]
        else:
            ema_aligned = False

        # Check weekly RSI
        weekly_rsi = latest.get("rsi")
        rsi_ok = pd.notna(weekly_rsi) and 40 < weekly_rsi < 70

        if ema_aligned and rsi_ok:
            trend = "Bullish"
            suitable = True
        elif ema_aligned:
            trend = "Bullish (RSI warning)"
            suitable = True
        else:
            trend = "Not Bullish"
            suitable = False

        return {
            "weekly_trend": trend,
            "weekly_rsi": weekly_rsi if pd.notna(weekly_rsi) else 0,
            "ema_aligned": ema_aligned,
            "suitable_for_swing": suitable,
        }
