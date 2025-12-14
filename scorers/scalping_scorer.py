"""Scoring and ranking module for scalping strategy"""

from typing import List, Dict
import pandas as pd

from config.scalping_config import SCORING_WEIGHTS, MAX_STOCKS_TO_SELECT


class ScalpingScorer:
    """Handles scoring and ranking of filtered stocks for scalping"""

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

    def calculate_liquidity_score(self, filter_results: Dict) -> float:
        """
        Calculate liquidity score (30% weight - most critical)

        Args:
            filter_results: Dictionary with filter results

        Returns:
            Liquidity score (0-100)
        """
        score = 0

        # Volume component (higher is better)
        avg_volume = filter_results.get("avg_volume", 0)
        # Normalize 2M to 50M shares range
        volume_score = self.normalize_to_range(avg_volume, 2e6, 50e6)
        score += volume_score * 0.6

        # Spread component (lower is better)
        spread_pct = filter_results.get("spread_pct", 0.1)
        # Invert: 0.01% spread = 100 score, 0.1% = 0 score
        spread_score = max(0, 100 - (spread_pct * 1000))
        score += spread_score * 0.4

        return score

    def calculate_momentum_score(self, filter_results: Dict) -> float:
        """
        Calculate momentum score (25% weight)

        Args:
            filter_results: Dictionary with filter results

        Returns:
            Momentum score (0-100)
        """
        score = 0

        # RSI strength (extreme values are better for scalping)
        rsi_3 = filter_results.get("rsi_3", 50)
        if rsi_3 < 20:
            # Oversold - score based on how oversold (lower = better)
            score += self.normalize_to_range(20 - rsi_3, 0, 20) * 0.4
        elif rsi_3 > 80:
            # Overbought - score based on how overbought (higher = better)
            score += self.normalize_to_range(rsi_3 - 80, 0, 20) * 0.4
        else:
            score += 0  # Neutral RSI gets 0

        # MACD cross bonus
        macd_cross = filter_results.get("macd_cross", False)
        if macd_cross == "bullish" or macd_cross == "bearish":
            score += 40  # Strong bonus for fresh crossover
        else:
            score += 20  # Partial credit if MACD exists

        # MACD histogram strength
        macd_hist = filter_results.get("macd_hist", 0)
        hist_score = min(40, abs(macd_hist) * 100)  # Cap at 40
        score += hist_score * 0.4

        return min(100, score)

    def calculate_vwap_setup_score(self, filter_results: Dict) -> float:
        """
        Calculate VWAP setup quality score (20% weight)

        Args:
            filter_results: Dictionary with filter results

        Returns:
            VWAP score (0-100)
        """
        # Closer to VWAP = better score
        vwap_deviation = filter_results.get("vwap_deviation_pct", 0.3)

        # Invert: 0% deviation = 100, 0.3% = 0
        score = max(0, 100 - (vwap_deviation / 0.3) * 100)

        return score

    def calculate_trend_alignment_score(self, filter_results: Dict) -> float:
        """
        Calculate trend alignment score (15% weight)

        Args:
            filter_results: Dictionary with filter results

        Returns:
            Trend alignment score (0-100)
        """
        ema_9 = filter_results.get("ema_9", 0)
        ema_20 = filter_results.get("ema_20", 0)
        trend = filter_results.get("trend", "neutral")

        if trend == "neutral" or ema_9 == 0 or ema_20 == 0:
            return 50

        # Calculate EMA separation (wider = stronger trend)
        ema_diff_pct = abs((ema_9 - ema_20) / ema_20) * 100

        # Normalize 0% to 2% separation
        score = self.normalize_to_range(ema_diff_pct, 0, 2)

        return score

    def calculate_volatility_score(self, filter_results: Dict) -> float:
        """
        Calculate volatility score (10% weight)

        Args:
            filter_results: Dictionary with filter results

        Returns:
            Volatility score (0-100)
        """
        atr = filter_results.get("atr", 3)
        volume_spike = filter_results.get("volume_spike", 1.5)

        # ATR component (higher = more opportunity)
        atr_score = self.normalize_to_range(atr, 3, 15) * 0.5

        # Volume spike component (higher = more momentum)
        spike_score = self.normalize_to_range(volume_spike, 1.5, 3.0) * 0.5

        return atr_score + spike_score

    def calculate_total_score(self, filter_results: Dict) -> float:
        """
        Calculate weighted total score for a stock

        Args:
            filter_results: Dictionary with filter results

        Returns:
            Total weighted score (0-100)
        """
        liquidity_score = self.calculate_liquidity_score(filter_results)
        momentum_score = self.calculate_momentum_score(filter_results)
        vwap_score = self.calculate_vwap_setup_score(filter_results)
        trend_score = self.calculate_trend_alignment_score(filter_results)
        volatility_score = self.calculate_volatility_score(filter_results)

        # Apply weights
        total_score = (
            (liquidity_score * SCORING_WEIGHTS["liquidity"] / 100)
            + (momentum_score * SCORING_WEIGHTS["momentum"] / 100)
            + (vwap_score * SCORING_WEIGHTS["vwap_setup"] / 100)
            + (trend_score * SCORING_WEIGHTS["trend_alignment"] / 100)
            + (volatility_score * SCORING_WEIGHTS["volatility"] / 100)
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

            # Entry reason based on signals
            rsi_signal = stock.get("rsi_signal", "")
            vwap_position = stock.get("vwap_position", "")
            macd_cross = stock.get("macd_cross", False)

            reasons = []
            if rsi_signal:
                reasons.append(rsi_signal)
            if vwap_position:
                reasons.append(f"VWAP {vwap_position}")
            if macd_cross:
                reasons.append(f"MACD {macd_cross}")

            stock["entry_reason"] = " + ".join(reasons) if reasons else "momentum scalp"

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
            "trend": stock_data.get("trend", "unknown"),
            "rsi_3": round(stock_data.get("rsi_3", 0), 2),
            "rsi_signal": stock_data.get("rsi_signal", ""),
            "vwap_deviation": round(stock_data.get("vwap_deviation_pct", 0), 2),
            "volume_spike": round(stock_data.get("volume_spike", 0), 2),
            "atr": round(stock_data.get("atr", 0), 2),
            "macd_cross": stock_data.get("macd_cross", False),
            "final_score": stock_data.get("final_score", 0),
            "entry_reason": stock_data.get("entry_reason", ""),
        }
