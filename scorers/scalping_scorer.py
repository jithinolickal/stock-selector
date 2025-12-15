"""Scoring and ranking module for ORB scalping strategy"""

from typing import List, Dict
import pandas as pd

from config.scalping_config import SCORING_WEIGHTS, MAX_STOCKS_TO_SELECT


class ScalpingScorer:
    """Handles scoring and ranking for ORB-based scalping"""

    @staticmethod
    def normalize_to_range(value: float, min_val: float, max_val: float) -> float:
        """Normalize a value to 0-100 range"""
        if max_val == min_val:
            return 50.0

        normalized = ((value - min_val) / (max_val - min_val)) * 100
        return max(0, min(100, normalized))

    def calculate_liquidity_score(self, filter_results: Dict) -> float:
        """Calculate liquidity score (30% weight)"""
        score = 0

        # Volume component (higher is better)
        avg_volume = filter_results.get("avg_volume", 0)
        volume_score = self.normalize_to_range(avg_volume, 2e6, 50e6)
        score += volume_score * 0.6

        # Spread component (lower is better)
        spread_pct = filter_results.get("spread_pct", 0.1)
        spread_score = max(0, 100 - (spread_pct * 1000))
        score += spread_score * 0.4

        return score

    def calculate_orb_breakout_score(self, filter_results: Dict) -> float:
        """Calculate ORB breakout strength score (25% weight)"""
        score = 0

        # ORB breakout distance (further = stronger)
        orb_high = filter_results.get("orb_high", 0)
        orb_low = filter_results.get("orb_low", 0)
        current_price = filter_results.get("current_price", 0)
        orb_direction = filter_results.get("orb_breakout", "")

        if orb_direction and orb_high and orb_low:
            orb_range = orb_high - orb_low
            if orb_direction == "up":
                breakout_dist = current_price - orb_high
                score += self.normalize_to_range(breakout_dist, 0, orb_range * 0.5) * 0.6
            elif orb_direction == "down":
                breakout_dist = orb_low - current_price
                score += self.normalize_to_range(breakout_dist, 0, orb_range * 0.5) * 0.6

        # Volume spike bonus
        volume_spike = filter_results.get("volume_spike", 1.0)
        volume_score = self.normalize_to_range(volume_spike, 1.0, 3.0)
        score += volume_score * 0.4

        return min(100, score)

    def calculate_vwap_score(self, filter_results: Dict) -> float:
        """Calculate VWAP proximity score (20% weight)"""
        vwap_deviation = filter_results.get("vwap_deviation_pct", 0)

        # Closer to VWAP = higher score
        # 0% deviation = 100, 0.8% = 0
        score = max(0, 100 - (vwap_deviation / 0.8) * 100)

        return score

    def calculate_trend_alignment_score(self, filter_results: Dict) -> float:
        """Calculate EMA trend alignment score (15% weight)"""
        score = 0

        # EMA separation (5 vs 9)
        ema_5 = filter_results.get("ema_5", 0)
        ema_9 = filter_results.get("ema_9", 0)

        if ema_5 and ema_9:
            # Stronger separation = stronger trend
            separation_pct = abs((ema_5 - ema_9) / ema_9) * 100
            score = self.normalize_to_range(separation_pct, 0, 1.0)  # 0-1% separation

        return score

    def calculate_volatility_score(self, filter_results: Dict) -> float:
        """Calculate ATR volatility score (10% weight)"""
        atr = filter_results.get("atr", 0)

        # Higher ATR = more movement potential
        # 1.5 to 10 points range
        score = self.normalize_to_range(atr, 1.5, 10.0)

        return score

    def calculate_final_score(self, filter_results: Dict) -> float:
        """
        Calculate weighted final score

        Returns:
            Final score (0-100)
        """
        liquidity = self.calculate_liquidity_score(filter_results)
        orb_breakout = self.calculate_orb_breakout_score(filter_results)
        vwap = self.calculate_vwap_score(filter_results)
        trend_alignment = self.calculate_trend_alignment_score(filter_results)
        volatility = self.calculate_volatility_score(filter_results)

        # Apply weights
        final_score = (
            liquidity * (SCORING_WEIGHTS["liquidity"] / 100) +
            orb_breakout * (SCORING_WEIGHTS["momentum"] / 100) +
            vwap * (SCORING_WEIGHTS["vwap_setup"] / 100) +
            trend_alignment * (SCORING_WEIGHTS["trend_alignment"] / 100) +
            volatility * (SCORING_WEIGHTS["volatility"] / 100)
        )

        return round(final_score, 2)

    def score_and_rank(self, filtered_stocks: List[Dict]) -> List[Dict]:
        """
        Score and rank filtered stocks

        Args:
            filtered_stocks: List of stocks that passed filters

        Returns:
            Sorted list of top stocks with scores
        """
        if not filtered_stocks:
            return []

        # Calculate scores
        for stock in filtered_stocks:
            stock["final_score"] = self.calculate_final_score(stock)

        # Sort by score (descending)
        ranked = sorted(filtered_stocks, key=lambda x: x["final_score"], reverse=True)

        # Return top N
        return ranked[:MAX_STOCKS_TO_SELECT]

    def get_stock_summary(self, stock_data: Dict) -> Dict:
        """Get clean summary for output"""
        return {
            "symbol": stock_data["symbol"],
            "orb_breakout": stock_data.get("orb_breakout", ""),
            "orb_high": round(stock_data.get("orb_high", 0), 2),
            "orb_low": round(stock_data.get("orb_low", 0), 2),
            "current_price": round(stock_data.get("current_price", 0), 2),
            "ema_5": round(stock_data.get("ema_5", 0), 2),
            "ema_9": round(stock_data.get("ema_9", 0), 2),
            "vwap": round(stock_data.get("vwap", 0), 2),
            "vwap_deviation": round(stock_data.get("vwap_deviation_pct", 0), 2),
            "volume_spike": round(stock_data.get("volume_spike", 0), 2),
            "atr": round(stock_data.get("atr", 0), 2),
            "rsi_7": round(stock_data.get("rsi_7", 50), 2),
            "final_score": stock_data.get("final_score", 0),
        }
