"""Scalping filters based on Opening Range Breakout (ORB) strategy"""

import pandas as pd
from typing import Tuple, Dict
from datetime import time
from config.scalping_config import FILTER_THRESHOLDS


class ScalpingFilter:
    """ORB-based scalping filters for 5-min candles"""

    def calculate_orb(self, intraday_df: pd.DataFrame) -> Tuple[float, float]:
        """
        Calculate Opening Range (first 15 mins: 9:15-9:30)

        Args:
            intraday_df: 5-min intraday DataFrame

        Returns:
            Tuple of (orb_high, orb_low)
        """
        # Filter candles between 9:15 and 9:30
        orb_start = time(9, 15)
        orb_end = time(9, 30)

        orb_candles = intraday_df[
            (intraday_df.index.time >= orb_start) &
            (intraday_df.index.time < orb_end)
        ]

        if orb_candles.empty:
            return None, None

        orb_high = orb_candles["high"].max()
        orb_low = orb_candles["low"].min()

        return orb_high, orb_low

    def apply_liquidity_filters(
        self, symbol: str, daily_df: pd.DataFrame, intraday_df: pd.DataFrame
    ) -> Tuple[bool, Dict]:
        """
        Check liquidity (volume + spreads)

        Args:
            symbol: Stock symbol
            daily_df: Daily DataFrame
            intraday_df: 5-min intraday DataFrame

        Returns:
            Tuple of (passed: bool, results: dict)
        """
        results = {"symbol": symbol}

        # Daily average volume check
        avg_volume = daily_df["volume"].tail(20).mean()
        if avg_volume < FILTER_THRESHOLDS["MIN_AVG_VOLUME"]:
            return False, {"reason": f"Low volume ({avg_volume/1e6:.1f}M)"}

        results["avg_volume"] = avg_volume

        # Spread check (using latest 5-min candle)
        latest = intraday_df.iloc[-1]
        spread_pct = ((latest["high"] - latest["low"]) / latest["close"]) * 100

        if spread_pct > FILTER_THRESHOLDS["MAX_SPREAD_PERCENT"]:
            return False, {"reason": f"Wide spread ({spread_pct:.2f}%)"}

        results["spread_pct"] = spread_pct
        results["passed"] = True

        return True, results

    def apply_orb_filters(
        self, intraday_df: pd.DataFrame
    ) -> Tuple[bool, Dict]:
        """
        Check for Opening Range Breakout

        Args:
            intraday_df: 5-min intraday DataFrame

        Returns:
            Tuple of (passed: bool, results: dict)
        """
        if intraday_df.empty or len(intraday_df) < 3:
            return False, {"reason": "Insufficient data for ORB"}

        results = {}

        # Calculate ORB range
        orb_high, orb_low = self.calculate_orb(intraday_df)

        if orb_high is None or orb_low is None:
            return False, {"reason": "ORB range not available"}

        results["orb_high"] = orb_high
        results["orb_low"] = orb_low

        # Current price
        latest = intraday_df.iloc[-1]
        current_price = latest["close"]
        results["current_price"] = current_price

        # Check for breakout (must be at least 0.2% beyond ORB)
        breakout_threshold = FILTER_THRESHOLDS["ORB_BREAKOUT_MIN_PCT"] / 100

        breakout_up = current_price > orb_high * (1 + breakout_threshold)
        breakout_down = current_price < orb_low * (1 - breakout_threshold)

        if breakout_up:
            results["orb_breakout"] = "up"
        elif breakout_down:
            results["orb_breakout"] = "down"
        else:
            return False, {"reason": f"No ORB breakout (price: {current_price:.2f}, ORB: {orb_low:.2f}-{orb_high:.2f})"}

        results["passed"] = True
        return True, results

    def apply_ema_filters(
        self, intraday_df: pd.DataFrame, orb_direction: str
    ) -> Tuple[bool, Dict]:
        """
        Check EMA alignment with ORB breakout direction

        Args:
            intraday_df: 5-min intraday DataFrame
            orb_direction: "up" or "down"

        Returns:
            Tuple of (passed: bool, results: dict)
        """
        results = {}
        latest = intraday_df.iloc[-1]

        ema_5 = latest.get("ema_5")
        ema_9 = latest.get("ema_9")

        if pd.isna(ema_5) or pd.isna(ema_9):
            return False, {"reason": "EMA not available"}

        results["ema_5"] = ema_5
        results["ema_9"] = ema_9

        # Bullish breakout: EMA5 should be > EMA9
        if orb_direction == "up" and ema_5 <= ema_9:
            return False, {"reason": f"EMA not aligned for bullish (5:{ema_5:.2f} <= 9:{ema_9:.2f})"}

        # Bearish breakout: EMA5 should be < EMA9
        if orb_direction == "down" and ema_5 >= ema_9:
            return False, {"reason": f"EMA not aligned for bearish (5:{ema_5:.2f} >= 9:{ema_9:.2f})"}

        results["ema_aligned"] = True
        results["passed"] = True
        return True, results

    def apply_volume_filters(
        self, intraday_df: pd.DataFrame
    ) -> Tuple[bool, Dict]:
        """
        Check volume spike (using 10-candle average)

        Args:
            intraday_df: 5-min intraday DataFrame

        Returns:
            Tuple of (passed: bool, results: dict)
        """
        results = {}
        latest = intraday_df.iloc[-1]

        # Volume average from indicator (10-period)
        volume_avg = latest.get("volume_avg_10")
        current_volume = latest["volume"]

        if pd.isna(volume_avg) or volume_avg == 0:
            return False, {"reason": "Volume average not available"}

        volume_ratio = current_volume / volume_avg

        if volume_ratio < FILTER_THRESHOLDS["MIN_VOLUME_SPIKE"]:
            return False, {"reason": f"No volume spike ({volume_ratio:.1f}x < {FILTER_THRESHOLDS['MIN_VOLUME_SPIKE']}x)"}

        results["volume_spike"] = volume_ratio
        results["passed"] = True
        return True, results

    def apply_vwap_atr_filters(
        self, intraday_df: pd.DataFrame
    ) -> Tuple[bool, Dict]:
        """
        Check VWAP proximity and ATR

        Args:
            intraday_df: 5-min intraday DataFrame

        Returns:
            Tuple of (passed: bool, results: dict)
        """
        results = {}
        latest = intraday_df.iloc[-1]

        # VWAP deviation
        vwap = latest.get("vwap")
        close = latest["close"]

        if pd.isna(vwap):
            return False, {"reason": "VWAP not available"}

        vwap_deviation_pct = abs((close - vwap) / vwap) * 100

        if vwap_deviation_pct > FILTER_THRESHOLDS["VWAP_DEVIATION_MAX"]:
            return False, {"reason": f"Too far from VWAP ({vwap_deviation_pct:.2f}%)"}

        results["vwap"] = vwap
        results["vwap_deviation_pct"] = vwap_deviation_pct

        # ATR check
        atr = latest.get("atr")

        if pd.isna(atr):
            return False, {"reason": "ATR not available"}

        if atr < FILTER_THRESHOLDS["MIN_ATR_POINTS"]:
            return False, {"reason": f"Low ATR ({atr:.2f} < {FILTER_THRESHOLDS['MIN_ATR_POINTS']})"}

        results["atr"] = atr

        # RSI (optional - just store, don't filter)
        rsi = latest.get("rsi_7")
        if not pd.isna(rsi):
            results["rsi_7"] = rsi

        results["passed"] = True
        return True, results

    def filter_stock(
        self, symbol: str, daily_df: pd.DataFrame, intraday_df: pd.DataFrame
    ) -> Tuple[bool, Dict]:
        """
        Apply all ORB scalping filters

        Args:
            symbol: Stock symbol
            daily_df: Daily DataFrame
            intraday_df: 5-min intraday DataFrame

        Returns:
            Tuple of (passed: bool, results: dict)
        """
        # Minimum candles check
        if intraday_df.empty or len(intraday_df) < 5:
            return False, {"stage": "data", "reason": "Insufficient intraday data"}

        # Filter 1: Liquidity
        liquidity_passed, liquidity_results = self.apply_liquidity_filters(
            symbol, daily_df, intraday_df
        )
        if not liquidity_passed:
            return False, {"stage": "liquidity", **liquidity_results}

        # Filter 2: ORB Breakout (PRIMARY)
        orb_passed, orb_results = self.apply_orb_filters(intraday_df)
        if not orb_passed:
            return False, {"stage": "orb", **liquidity_results, **orb_results}

        orb_direction = orb_results["orb_breakout"]

        # Filter 3: EMA Alignment
        ema_passed, ema_results = self.apply_ema_filters(intraday_df, orb_direction)
        if not ema_passed:
            return False, {"stage": "ema", **liquidity_results, **orb_results, **ema_results}

        # Filter 4: Volume Spike
        volume_passed, volume_results = self.apply_volume_filters(intraday_df)
        if not volume_passed:
            return False, {"stage": "volume", **liquidity_results, **orb_results, **ema_results, **volume_results}

        # Filter 5: VWAP + ATR
        vwap_atr_passed, vwap_atr_results = self.apply_vwap_atr_filters(intraday_df)
        if not vwap_atr_passed:
            return False, {"stage": "vwap_atr", **liquidity_results, **orb_results, **ema_results, **volume_results, **vwap_atr_results}

        # All filters passed
        combined = {
            "symbol": symbol,
            "passed": True,
            **liquidity_results,
            **orb_results,
            **ema_results,
            **volume_results,
            **vwap_atr_results,
        }

        return True, combined
