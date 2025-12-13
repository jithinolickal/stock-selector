"""Stock filtering module with daily and intraday filters"""

import pandas as pd
from typing import Dict, Tuple
from datetime import time

from config import FILTER_THRESHOLDS, INTRADAY_START_TIME, INTRADAY_END_TIME
from indicators import (
    calculate_ema_slope,
    calculate_volume_ratio,
    calculate_atr_ratio,
    calculate_relative_strength,
)


class StockFilter:
    """Handles all filtering logic for stock selection"""

    def __init__(self, nifty_index_df: pd.DataFrame):
        """
        Initialize filter with NIFTY50 index data

        Args:
            nifty_index_df: DataFrame with NIFTY50 index daily data
        """
        self.nifty_index_df = nifty_index_df

    def apply_daily_filters(
        self, symbol: str, df: pd.DataFrame
    ) -> Tuple[bool, Dict[str, any]]:
        """
        Apply all 9 daily timeframe filters

        Args:
            symbol: Stock symbol
            df: DataFrame with daily OHLCV and indicators

        Returns:
            Tuple of (passed: bool, filter_results: dict)
        """
        if df.empty or len(df) < 200:
            return False, {"reason": "Insufficient data"}

        results = {}
        latest = df.iloc[-1]

        # Filter 1: Price > 200 EMA
        if pd.isna(latest["ema_200"]) or latest["close"] <= latest["ema_200"]:
            return False, {"reason": "Price not above 200 EMA"}
        results["above_200ema"] = True

        # Filter 2: Close > EMA20 > EMA50
        if (
            pd.isna(latest["ema_20"])
            or pd.isna(latest["ema_50"])
            or latest["close"] <= latest["ema_20"]
            or latest["ema_20"] <= latest["ema_50"]
        ):
            return False, {"reason": "EMA alignment failed (Close > EMA20 > EMA50)"}
        results["ema_alignment"] = True

        # Filter 3: 50 EMA > 200 EMA (bullish regime)
        if pd.isna(latest["ema_200"]) or latest["ema_50"] <= latest["ema_200"]:
            return False, {"reason": "Not in bullish regime (50 EMA <= 200 EMA)"}
        results["bullish_regime"] = True

        # Filter 4: EMA20 slope positive (last 5 days)
        ema20_slope = calculate_ema_slope(df["ema_20"], FILTER_THRESHOLDS["EMA_SLOPE_DAYS"])
        if ema20_slope <= 0:
            return False, {"reason": "EMA20 slope not positive"}
        results["ema20_slope"] = ema20_slope

        # Filter 5: ADX > 25
        if pd.isna(latest["adx"]) or latest["adx"] < FILTER_THRESHOLDS["ADX_MIN"]:
            return False, {"reason": f"ADX < {FILTER_THRESHOLDS['ADX_MIN']}"}
        results["adx"] = latest["adx"]

        # Filter 6: RSI between 40 and 65
        if (
            pd.isna(latest["rsi"])
            or latest["rsi"] < FILTER_THRESHOLDS["RSI_MIN"]
            or latest["rsi"] > FILTER_THRESHOLDS["RSI_MAX"]
        ):
            return False, {
                "reason": f"RSI not in range {FILTER_THRESHOLDS['RSI_MIN']}-{FILTER_THRESHOLDS['RSI_MAX']}"
            }
        results["rsi"] = latest["rsi"]

        # Filter 7: ATR >= 1.5x its 20-day average
        atr_ratio = calculate_atr_ratio(df["atr"], period=20)
        if atr_ratio < FILTER_THRESHOLDS["ATR_MULTIPLIER"]:
            return False, {"reason": f"ATR ratio < {FILTER_THRESHOLDS['ATR_MULTIPLIER']}x"}
        results["atr_ratio"] = atr_ratio

        # Filter 8: Current volume > 20-day average
        volume_ratio = calculate_volume_ratio(df, period=20)
        if volume_ratio < FILTER_THRESHOLDS["VOLUME_MULTIPLIER"]:
            return False, {"reason": "Volume below 20-day average"}
        results["volume_ratio"] = volume_ratio

        # Filter 9: Relative Strength vs NIFTY50 > 0
        rs = calculate_relative_strength(df, self.nifty_index_df, period=20)
        if rs <= 0:
            return False, {"reason": "Not outperforming NIFTY50"}
        results["relative_strength"] = rs

        # All filters passed
        results["passed"] = True
        return True, results

    def apply_intraday_filters(self, df: pd.DataFrame) -> Tuple[bool, Dict[str, any]]:
        """
        Apply intraday confirmation filters (9:30-10:00 AM window)

        Args:
            df: DataFrame with 15-min intraday OHLCV and indicators

        Returns:
            Tuple of (passed: bool, filter_results: dict)
        """
        if df.empty:
            return False, {"reason": "No intraday data available"}

        results = {}

        # Filter intraday data to 9:30-10:00 window
        # Convert time strings to time objects for comparison
        start_time = time(9, 30)
        end_time = time(10, 0)

        # Filter candles in the window
        mask = (df.index.time >= start_time) & (df.index.time <= end_time)
        window_df = df[mask]

        if len(window_df) < FILTER_THRESHOLDS["VWAP_CANDLES_TO_CHECK"]:
            return False, {"reason": "Insufficient intraday candles in 9:30-10:00 window"}

        # Get first N candles for checks
        first_candles = window_df.head(FILTER_THRESHOLDS["VWAP_CANDLES_TO_CHECK"])

        # Filter 6: Price above VWAP
        latest_price = window_df["close"].iloc[-1]
        latest_vwap = window_df["vwap"].iloc[-1]

        if pd.isna(latest_vwap) or latest_price <= latest_vwap:
            return False, {"reason": "Price not above VWAP"}
        results["above_vwap"] = True

        # Filter 7: First two 15-min candles hold above VWAP
        for i, (idx, candle) in enumerate(first_candles.iterrows()):
            if pd.isna(candle["vwap"]) or candle["low"] < candle["vwap"]:
                return False, {"reason": f"Candle {i+1} dropped below VWAP"}
        results["vwap_hold"] = True

        # Filter 8: No large upper wick (>50% of candle range)
        for i, (idx, candle) in enumerate(first_candles.iterrows()):
            candle_range = candle["high"] - candle["low"]
            if candle_range == 0:
                continue

            upper_wick = candle["high"] - max(candle["open"], candle["close"])
            wick_ratio = upper_wick / candle_range

            if wick_ratio > FILTER_THRESHOLDS["UPPER_WICK_THRESHOLD"]:
                return False, {"reason": f"Candle {i+1} has large upper wick ({wick_ratio:.1%})"}
        results["no_large_wicks"] = True

        # Filter 9: 15-min volume >= 1.2x 20-period average
        # Check latest candle's volume
        latest_volume = window_df["volume"].iloc[-1]
        avg_volume = window_df["volume_avg_20"].iloc[-1]

        if pd.isna(avg_volume) or avg_volume == 0:
            # If no volume average, skip this check
            results["volume_confirmed"] = True
        elif latest_volume < FILTER_THRESHOLDS["INTRADAY_VOLUME_MULTIPLIER"] * avg_volume:
            return False, {
                "reason": f"15-min volume < {FILTER_THRESHOLDS['INTRADAY_VOLUME_MULTIPLIER']}x average"
            }
        else:
            results["volume_confirmed"] = True

        # All intraday filters passed
        results["passed"] = True
        results["intraday_bias"] = "bullish"
        return True, results

    def filter_stock(
        self, symbol: str, daily_df: pd.DataFrame, intraday_df: pd.DataFrame
    ) -> Tuple[bool, Dict[str, any]]:
        """
        Apply both daily and intraday filters to a stock

        Args:
            symbol: Stock symbol
            daily_df: DataFrame with daily data and indicators
            intraday_df: DataFrame with 15-min intraday data and indicators

        Returns:
            Tuple of (passed: bool, combined_results: dict)
        """
        # Apply daily filters first
        daily_passed, daily_results = self.apply_daily_filters(symbol, daily_df)

        if not daily_passed:
            return False, {"stage": "daily", **daily_results}

        # Apply intraday filters
        intraday_passed, intraday_results = self.apply_intraday_filters(intraday_df)

        if not intraday_passed:
            return False, {"stage": "intraday", **daily_results, **intraday_results}

        # Both passed - combine results
        combined = {
            "symbol": symbol,
            "passed": True,
            **daily_results,
            **intraday_results,
        }

        return True, combined
