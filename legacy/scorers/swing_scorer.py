"""Scoring and ranking module for filtered stocks"""

from typing import List, Dict
import pandas as pd

from config.swing_config import SCORING_WEIGHTS, MAX_STOCKS_TO_SELECT


class StockScorer:
    """Handles scoring and ranking of filtered stocks"""

    @staticmethod
    def normalize_to_range(value: float, min_val: float, max_val: float) -> float:
        """
        Normalize a value to 0-100 range

        Args:
            value: Value to normalize
            min_val: Minimum expected value
            max_val: Maximum expected value

        Returns:
            Normalized value (0-100)
        """
        if max_val == min_val:
            return 50.0

        normalized = ((value - min_val) / (max_val - min_val)) * 100
        return max(0, min(100, normalized))

    def calculate_trend_score(self, filter_results: Dict) -> float:
        """
        Calculate trend strength score (35% weight)
        Based on ADX + EMA alignment

        Args:
            filter_results: Dictionary with filter results

        Returns:
            Trend score (0-100)
        """
        adx = filter_results.get("adx", 25)
        ema_slope = filter_results.get("ema20_slope", 0)

        # ADX component (0-100 scale, with 25 as min and 50+ as strong)
        adx_score = self.normalize_to_range(adx, 25, 50)

        # EMA slope component (higher slope = stronger trend)
        # Normalize slope (assume slope range 0 to 5 is good)
        slope_score = self.normalize_to_range(abs(ema_slope), 0, 5)

        # Combine: 70% ADX, 30% slope
        trend_score = (adx_score * 0.7) + (slope_score * 0.3)
        return trend_score

    def calculate_rsi_score(self, filter_results: Dict) -> float:
        """
        Calculate RSI position score (25% weight)
        Best RSI range is 50-60 for momentum continuation

        Args:
            filter_results: Dictionary with filter results

        Returns:
            RSI score (0-100)
        """
        rsi = filter_results.get("rsi", 50)

        # Ideal RSI is between 50-60
        # Score decreases as RSI moves away from this range
        if 50 <= rsi <= 60:
            # Perfect range - full score
            score = 100
        elif 40 <= rsi < 50:
            # Pullback zone - still good, score 60-100
            score = self.normalize_to_range(rsi, 40, 50) * 0.4 + 60
        elif 60 < rsi <= 65:
            # Momentum zone - acceptable, score 70-100
            score = 100 - self.normalize_to_range(rsi, 60, 65) * 0.3
        else:
            # Outside range (should have been filtered out, but just in case)
            score = 50

        return score

    def calculate_relative_strength_score(self, filter_results: Dict) -> float:
        """
        Calculate relative strength score (15% weight)
        Higher RS vs NIFTY50 is better

        Args:
            filter_results: Dictionary with filter results

        Returns:
            RS score (0-100)
        """
        rs = filter_results.get("relative_strength", 0)

        # Normalize RS (assume range 0 to 10% outperformance is excellent)
        score = self.normalize_to_range(rs, 0, 10)
        return score

    def calculate_volume_score(self, filter_results: Dict) -> float:
        """
        Calculate volume expansion score (15% weight)
        Higher volume expansion indicates stronger conviction

        Args:
            filter_results: Dictionary with filter results

        Returns:
            Volume score (0-100)
        """
        volume_ratio = filter_results.get("volume_ratio", 1.0)

        # Normalize volume ratio (1.0 to 2.5x is good range)
        score = self.normalize_to_range(volume_ratio, 1.0, 2.5)
        return score

    def calculate_atr_score(self, filter_results: Dict) -> float:
        """
        Calculate ATR percentage score (10% weight)
        Higher ATR indicates more volatility/opportunity

        Args:
            filter_results: Dictionary with filter results

        Returns:
            ATR score (0-100)
        """
        atr_ratio = filter_results.get("atr_ratio", 1.5)

        # Normalize ATR ratio (1.5 to 3.0x is good range)
        score = self.normalize_to_range(atr_ratio, 1.5, 3.0)
        return score

    def calculate_weekly_score(self, filter_results: Dict) -> float:
        """
        Calculate weekly timeframe alignment score (10% weight)

        Args:
            filter_results: Dictionary with filter results

        Returns:
            Weekly score (0-100)
        """
        weekly_suitable = filter_results.get("weekly_suitable")

        if weekly_suitable is True:
            return 100
        elif weekly_suitable is False:
            return 0
        else:
            # Unknown - neutral score
            return 50

    def calculate_price_action_score(self, filter_results: Dict) -> float:
        """
        Calculate price action pattern score (10% weight)

        Args:
            filter_results: Dictionary with filter results

        Returns:
            Price action score (0-100)
        """
        score = 0

        # Higher lows count (max 5)
        higher_lows = filter_results.get("higher_lows_count", 0)
        score += self.normalize_to_range(higher_lows, 3, 5) * 0.4

        # Consolidation breakout bonus
        if filter_results.get("breakout_from_consolidation", False):
            score += 30

        # Bullish pattern bonus
        if filter_results.get("bullish_pattern", False):
            score += 30

        # Volume expansion confirmation
        if filter_results.get("volume_expanding", False):
            score += 40

        return min(100, score)

    def calculate_trade_quality_score(self, filter_results: Dict) -> float:
        """
        Calculate trade quality score (10% weight)
        Based on stop quality and R:R ratio

        Args:
            filter_results: Dictionary with filter results

        Returns:
            Trade quality score (0-100)
        """
        quality_metrics = filter_results.get("trade_quality", {})

        if not quality_metrics or not quality_metrics.get("passed"):
            return 50  # Neutral if no trade quality data

        score = 0

        # Stop distance quality (closer to 1% is ideal)
        stop_distance = quality_metrics.get("stop_distance_pct")
        if stop_distance:
            # Ideal is 0.8-1.2%, score decreases as it moves away
            if 0.8 <= stop_distance <= 1.2:
                score += 50
            else:
                # Score based on distance from ideal
                ideal_distance = abs(stop_distance - 1.0)
                score += max(0, 50 - (ideal_distance * 25))

        # Risk-reward ratio (higher is better)
        rr = quality_metrics.get("risk_reward", 1.5)
        # Normalize 1.5R to 3.0R range
        score += self.normalize_to_range(rr, 1.5, 3.0) * 0.5

        return min(100, score)

    def calculate_total_score(self, filter_results: Dict) -> float:
        """
        Calculate weighted total score for a stock

        Args:
            filter_results: Dictionary with filter results

        Returns:
            Total weighted score (0-100)
        """
        trend_score = self.calculate_trend_score(filter_results)
        rsi_score = self.calculate_rsi_score(filter_results)
        rs_score = self.calculate_relative_strength_score(filter_results)
        volume_score = self.calculate_volume_score(filter_results)
        atr_score = self.calculate_atr_score(filter_results)
        weekly_score = self.calculate_weekly_score(filter_results)
        price_action_score = self.calculate_price_action_score(filter_results)
        trade_quality_score = self.calculate_trade_quality_score(filter_results)

        # Apply weights
        total_score = (
            (trend_score * SCORING_WEIGHTS["trend_strength"] / 100)
            + (rsi_score * SCORING_WEIGHTS["rsi_position"] / 100)
            + (rs_score * SCORING_WEIGHTS["relative_strength"] / 100)
            + (volume_score * SCORING_WEIGHTS["volume_expansion"] / 100)
            + (atr_score * SCORING_WEIGHTS["atr_percentage"] / 100)
            + (weekly_score * SCORING_WEIGHTS["weekly_alignment"] / 100)
            + (price_action_score * SCORING_WEIGHTS["price_action"] / 100)
            + (trade_quality_score * SCORING_WEIGHTS["trade_quality"] / 100)
        )

        return round(total_score, 2)

    def score_and_rank(self, filtered_stocks: List[Dict]) -> List[Dict]:
        """
        Score all filtered stocks and rank them

        Args:
            filtered_stocks: List of dictionaries with filter results

        Returns:
            Sorted list of stocks with scores (highest first)
        """
        if not filtered_stocks:
            return []

        # Calculate scores for each stock
        for stock in filtered_stocks:
            stock["final_score"] = self.calculate_total_score(stock)
            stock["entry_reason"] = "trend + momentum continuation"

        # Sort by score (descending)
        ranked_stocks = sorted(
            filtered_stocks, key=lambda x: x["final_score"], reverse=True
        )

        # Return top N stocks
        return ranked_stocks[:MAX_STOCKS_TO_SELECT]

    def get_stock_summary(self, stock_data: Dict) -> Dict:
        """
        Get clean summary dict for output

        Args:
            stock_data: Full stock data with all filter results

        Returns:
            Clean summary dict for output
        """
        return {
            "symbol": stock_data["symbol"],
            "daily_trend": stock_data.get("ema_alignment", False),
            "above_200ema": stock_data.get("above_200ema", False),
            "ADX": round(stock_data.get("adx", 0), 2),
            "RSI": round(stock_data.get("rsi", 0), 2),
            "ATR_ratio": round(stock_data.get("atr_ratio", 0), 2),
            "relative_strength": round(stock_data.get("relative_strength", 0), 2),
            "volume_confirmed": stock_data.get("volume_confirmed", False),
            "intraday_bias": stock_data.get("intraday_bias", "neutral"),
            "final_score": stock_data.get("final_score", 0),
            "entry_reason": stock_data.get("entry_reason", ""),
        }
