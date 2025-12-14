"""Strategy factory for multi-strategy stock selector"""

from typing import List


class StrategyFactory:
    """Factory for creating strategy instances"""

    @staticmethod
    def create_strategy(strategy_name: str):
        """Create strategy instance based on name"""
        if strategy_name == "swing":
            from strategies.swing_strategy import SwingStrategy
            return SwingStrategy()
        elif strategy_name == "scalping":
            from strategies.scalping_strategy import ScalpingStrategy
            return ScalpingStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

    @staticmethod
    def get_available_strategies() -> List[str]:
        """Get list of available strategies"""
        return ["swing", "scalping"]
