"""Scalping-specific filters for intraday trading"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple

from config.scalping_config import FILTER_THRESHOLDS


class ScalpingFilter:
    """Handles all filtering logic for scalping strategy"""

    def __init__(self):
        """Initialize scalping filter"""
        pass

    def apply_liquidity_filters(self, symbol: str, daily_df: pd.DataFrame, intraday_df: pd.DataFrame) -> Tuple[bool, Dict]:
        """
        Check liquidity requirements (most critical for scalping)

        Args:
            symbol: Stock symbol
            daily_df: Daily DataFrame for volume check
            intraday_df: Intraday DataFrame for spread check

        Returns:
            Tuple of (passed: bool, results: dict)
        """
        results = {}

        # Check average daily volume
        if len(daily_df) < 20:
            return False, {"reason": "Insufficient daily data"}

        avg_volume = daily_df["volume"].tail(20).mean()
        if avg_volume < FILTER_THRESHOLDS["MIN_AVG_VOLUME"]:
            return False, {"reason": f"Low volume ({avg_volume/1e6:.1f}M < {FILTER_THRESHOLDS['MIN_AVG_VOLUME']/1e6:.1f}M)"}

        results["avg_volume"] = avg_volume

        # Check bid-ask spread (estimate from intraday high-low)
        if not intraday_df.empty:
            latest = intraday_df.iloc[-1]
            spread_pct = ((latest["high"] - latest["low"]) / latest["close"]) * 100

            if spread_pct > FILTER_THRESHOLDS["MAX_SPREAD_PERCENT"]:
                return False, {"reason": f"Wide spread ({spread_pct:.2f}% > {FILTER_THRESHOLDS['MAX_SPREAD_PERCENT']}%)"}

            results["spread_pct"] = spread_pct

        results["passed"] = True
        return True, results

    def apply_technical_filters(self, intraday_df: pd.DataFrame) -> Tuple[bool, Dict]:
        """
        Apply technical filters on 3-min data

        Args:
            intraday_df: 3-min intraday DataFrame with indicators

        Returns:
            Tuple of (passed: bool, results: dict)
        """
        if intraday_df.empty or len(intraday_df) < 30:
            return False, {"reason": "Insufficient intraday data"}

        results = {}
        latest = intraday_df.iloc[-1]

        # RSI-3 check (for reversal entries)
        rsi = latest.get("rsi_3")
        if pd.isna(rsi):
            return False, {"reason": "RSI not available"}

        # Look for oversold (buy signal) or overbought (sell signal)
        if rsi < FILTER_THRESHOLDS["RSI_OVERSOLD"]:
            results["rsi_signal"] = "oversold_buy"
            results["rsi_3"] = rsi
        elif rsi > FILTER_THRESHOLDS["RSI_OVERBOUGHT"]:
            results["rsi_signal"] = "overbought_sell"
            results["rsi_3"] = rsi
        else:
            return False, {"reason": f"RSI neutral ({rsi:.1f})"}

        # EMA alignment check
        ema_9 = latest.get("ema_9")
        ema_20 = latest.get("ema_20")

        if pd.isna(ema_9) or pd.isna(ema_20):
            return False, {"reason": "EMAs not available"}

        results["ema_9"] = ema_9
        results["ema_20"] = ema_20

        # Trend direction
        if ema_9 > ema_20:
            results["trend"] = "bullish"
        else:
            results["trend"] = "bearish"

        # Volume spike check
        volume_avg = intraday_df["volume"].tail(20).mean()
        current_volume = latest["volume"]

        if current_volume < FILTER_THRESHOLDS["MIN_VOLUME_SPIKE"] * volume_avg:
            return False, {"reason": f"No volume spike ({current_volume/volume_avg:.1f}x < {FILTER_THRESHOLDS['MIN_VOLUME_SPIKE']}x)"}

        results["volume_spike"] = current_volume / volume_avg

        # ATR check (minimum movement potential)
        atr = latest.get("atr")
        if pd.isna(atr) or atr < FILTER_THRESHOLDS["MIN_ATR_POINTS"]:
            return False, {"reason": f"Low ATR ({atr:.1f} < {FILTER_THRESHOLDS['MIN_ATR_POINTS']})"}

        results["atr"] = atr

        results["passed"] = True
        return True, results

    def apply_vwap_filters(self, intraday_df: pd.DataFrame) -> Tuple[bool, Dict]:
        """
        Check VWAP proximity for mean reversion setups

        Args:
            intraday_df: 3-min intraday DataFrame

        Returns:
            Tuple of (passed: bool, results: dict)
        """
        if intraday_df.empty:
            return False, {"reason": "No intraday data"}

        results = {}
        latest = intraday_df.iloc[-1]

        vwap = latest.get("vwap")
        close = latest["close"]

        if pd.isna(vwap):
            return False, {"reason": "VWAP not available"}

        # Calculate deviation from VWAP
        vwap_deviation_pct = abs((close - vwap) / vwap) * 100

        if vwap_deviation_pct > FILTER_THRESHOLDS["VWAP_DEVIATION_MAX"]:
            return False, {"reason": f"Too far from VWAP ({vwap_deviation_pct:.2f}% > {FILTER_THRESHOLDS['VWAP_DEVIATION_MAX']}%)"}

        results["vwap"] = vwap
        results["vwap_deviation_pct"] = vwap_deviation_pct

        # Determine setup type
        if close > vwap:
            results["vwap_position"] = "above"  # Look for pullbacks to VWAP
        else:
            results["vwap_position"] = "below"  # Look for bounces from VWAP

        results["passed"] = True
        return True, results

    def apply_momentum_filters(self, intraday_df: pd.DataFrame) -> Tuple[bool, Dict]:
        """
        Check MACD momentum

        Args:
            intraday_df: 3-min intraday DataFrame

        Returns:
            Tuple of (passed: bool, results: dict)
        """
        if intraday_df.empty or len(intraday_df) < 30:
            return False, {"reason": "Insufficient data for MACD"}

        results = {}
        latest = intraday_df.iloc[-1]
        prev = intraday_df.iloc[-2]

        macd = latest.get("macd")
        macd_signal = latest.get("macd_signal")
        macd_hist = latest.get("macd_hist")

        if pd.isna(macd) or pd.isna(macd_signal):
            return False, {"reason": "MACD not available"}

        # Check for MACD crossover (momentum shift)
        prev_macd = prev.get("macd")
        prev_signal = prev.get("macd_signal")

        if pd.isna(prev_macd) or pd.isna(prev_signal):
            results["macd_cross"] = False
        else:
            # Bullish cross
            if prev_macd <= prev_signal and macd > macd_signal:
                results["macd_cross"] = "bullish"
            # Bearish cross
            elif prev_macd >= prev_signal and macd < macd_signal:
                results["macd_cross"] = "bearish"
            else:
                results["macd_cross"] = False

        results["macd"] = macd
        results["macd_signal"] = macd_signal
        results["macd_hist"] = macd_hist

        results["passed"] = True
        return True, results

    def filter_stock(
        self, symbol: str, daily_df: pd.DataFrame, intraday_df: pd.DataFrame
    ) -> Tuple[bool, Dict]:
        """
        Apply all scalping filters to a stock

        Args:
            symbol: Stock symbol
            daily_df: Daily DataFrame
            intraday_df: 3-min intraday DataFrame with indicators

        Returns:
            Tuple of (passed: bool, combined_results: dict)
        """
        # Filter 1: Liquidity (critical - check first)
        liquidity_passed, liquidity_results = self.apply_liquidity_filters(symbol, daily_df, intraday_df)
        if not liquidity_passed:
            return False, {"stage": "liquidity", **liquidity_results}

        # Filter 2: Technical indicators
        technical_passed, technical_results = self.apply_technical_filters(intraday_df)
        if not technical_passed:
            return False, {"stage": "technical", **liquidity_results, **technical_results}

        # Filter 3: VWAP proximity
        vwap_passed, vwap_results = self.apply_vwap_filters(intraday_df)
        if not vwap_passed:
            return False, {"stage": "vwap", **liquidity_results, **technical_results, **vwap_results}

        # Filter 4: Momentum (MACD)
        momentum_passed, momentum_results = self.apply_momentum_filters(intraday_df)
        if not momentum_passed:
            return False, {"stage": "momentum", **liquidity_results, **technical_results, **vwap_results, **momentum_results}

        # All filters passed
        combined = {
            "symbol": symbol,
            "passed": True,
            **liquidity_results,
            **technical_results,
            **vwap_results,
            **momentum_results,
        }

        return True, combined
