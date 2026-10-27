"""Abstract base class for all trading strategies"""

from abc import ABC, abstractmethod
from typing import List, Dict
import pandas as pd


class BaseStrategy(ABC):
    """Abstract base class for all trading strategies"""

    def __init__(self, config_module):
        """
        Initialize strategy with configuration module

        Args:
            config_module: Strategy-specific configuration module
        """
        self.config = config_module

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get strategy name"""
        pass

    @abstractmethod
    def fetch_required_data(self, data_fetcher, symbols: List[str]) -> Dict:
        """
        Fetch data required for this strategy

        Args:
            data_fetcher: UpstoxDataFetcher instance
            symbols: List of stock symbols to fetch

        Returns:
            Dictionary with stock data
        """
        pass

    @abstractmethod
    def analyze_and_select(
        self, all_data: Dict, nifty_index_df: pd.DataFrame, nifty_intraday: pd.DataFrame, test_mode: bool = False
    ) -> tuple:
        """
        Run strategy-specific analysis and return selected stocks

        Args:
            all_data: Dictionary with all stock data
            nifty_index_df: NIFTY50 index daily data
            nifty_intraday: NIFTY50 index intraday data
            test_mode: Whether running in test mode

        Returns:
            Tuple of (selected_stocks, trade_setups, stock_analysis, stats)
        """
        pass
