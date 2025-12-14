"""Data fetching module for Upstox API"""

import os
import gzip
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import upstox_client
from dotenv import load_dotenv
import pandas as pd

from config.base_config import (
    NIFTY50_SYMBOLS,
    NIFTY50_INDEX_KEY,
    UPSTOX_INSTRUMENTS_URL,
)
from config.swing_config import HISTORICAL_DAYS

# Load environment variables
load_dotenv()


class UpstoxDataFetcher:
    """Handles all data fetching operations from Upstox API"""

    def __init__(self):
        """Initialize Upstox API client with access token"""
        self.access_token = os.getenv("UPSTOX_ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError("UPSTOX_ACCESS_TOKEN not found in environment variables")

        # Configure API client
        self.configuration = upstox_client.Configuration()
        self.configuration.access_token = self.access_token
        self.api_client = upstox_client.ApiClient(self.configuration)

        # Cache for instrument keys
        self.instrument_map: Dict[str, str] = {}

    def fetch_instruments(self) -> Dict[str, str]:
        """
        Fetch and parse NSE instruments to map symbols to instrument keys

        Returns:
            Dict mapping trading symbols to instrument keys
        """
        print("Fetching NSE instruments...")
        response = requests.get(UPSTOX_INSTRUMENTS_URL, timeout=30)
        response.raise_for_status()

        # Decompress gzip content
        decompressed = gzip.decompress(response.content)
        instruments = json.loads(decompressed)

        # Filter for NSE_EQ segment and create symbol -> instrument_key mapping
        for instrument in instruments:
            if (
                instrument.get("segment") == "NSE_EQ"
                and instrument.get("instrument_type") == "EQ"
            ):
                symbol = instrument.get("trading_symbol")
                instrument_key = instrument.get("instrument_key")
                if symbol and instrument_key:
                    self.instrument_map[symbol] = instrument_key

        print(f"Loaded {len(self.instrument_map)} NSE equity instruments")
        return self.instrument_map

    def get_instrument_key(self, symbol: str) -> Optional[str]:
        """
        Get instrument key for a given symbol

        Args:
            symbol: Trading symbol (e.g., 'RELIANCE')

        Returns:
            Instrument key or None if not found
        """
        if not self.instrument_map:
            self.fetch_instruments()
        return self.instrument_map.get(symbol)

    def fetch_historical_daily(self, instrument_key: str, days: int = HISTORICAL_DAYS) -> pd.DataFrame:
        """
        Fetch historical daily candles

        Args:
            instrument_key: Upstox instrument key
            days: Number of days of historical data

        Returns:
            DataFrame with OHLCV data
        """
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        url = f"https://api.upstox.com/v3/historical-candle/{instrument_key}/days/1/{to_date}/{from_date}"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        candles = data.get("data", {}).get("candles", [])

        if not candles:
            return pd.DataFrame()

        # Convert to DataFrame
        df = pd.DataFrame(
            candles,
            columns=["timestamp", "open", "high", "low", "close", "volume", "oi"],
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)
        df.sort_index(inplace=True)

        return df

    def fetch_intraday_15min(self, instrument_key: str) -> pd.DataFrame:
        """
        Fetch today's 15-minute intraday candles

        Args:
            instrument_key: Upstox instrument key

        Returns:
            DataFrame with 15-min OHLCV data
        """
        url = f"https://api.upstox.com/v3/historical-candle/intraday/{instrument_key}/minutes/15"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        candles = data.get("data", {}).get("candles", [])

        if not candles:
            return pd.DataFrame()

        # Convert to DataFrame
        df = pd.DataFrame(
            candles,
            columns=["timestamp", "open", "high", "low", "close", "volume", "oi"],
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)
        df.sort_index(inplace=True)

        return df

    def fetch_nifty50_index(self, days: int = HISTORICAL_DAYS) -> pd.DataFrame:
        """
        Fetch NIFTY50 index historical data for relative strength calculation

        Args:
            days: Number of days of historical data

        Returns:
            DataFrame with NIFTY50 index OHLCV data
        """
        return self.fetch_historical_daily(NIFTY50_INDEX_KEY, days)

    def fetch_weekly_candles(self, instrument_key: str, weeks: int = 52) -> pd.DataFrame:
        """
        Fetch weekly candles for longer-term trend analysis

        Args:
            instrument_key: Upstox instrument key
            weeks: Number of weeks of data (default 52 = 1 year)

        Returns:
            DataFrame with weekly OHLCV data
        """
        # Calculate days needed (weeks * 7 + buffer for weekends)
        days = weeks * 9  # 9 days per week avg to account for weekends/holidays

        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        url = f"https://api.upstox.com/v3/historical-candle/{instrument_key}/weeks/1/{to_date}/{from_date}"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        candles = data.get("data", {}).get("candles", [])

        if not candles:
            return pd.DataFrame()

        # Convert to DataFrame
        df = pd.DataFrame(
            candles,
            columns=["timestamp", "open", "high", "low", "close", "volume", "oi"],
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)
        df.sort_index(inplace=True)

        return df

    def fetch_all_nifty50_data(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Fetch both daily and intraday data for all NIFTY50 stocks

        Returns:
            Dict with structure: {symbol: {"daily": df, "intraday": df}}
        """
        if not self.instrument_map:
            self.fetch_instruments()

        all_data = {}
        failed_symbols = []

        print(f"\nFetching data for {len(NIFTY50_SYMBOLS)} NIFTY50 stocks...")

        for i, symbol in enumerate(NIFTY50_SYMBOLS, 1):
            print(f"[{i}/{len(NIFTY50_SYMBOLS)}] {symbol}...", end=" ")

            instrument_key = self.get_instrument_key(symbol)
            if not instrument_key:
                print(f"⚠️  Instrument key not found")
                failed_symbols.append(symbol)
                continue

            try:
                daily_df = self.fetch_historical_daily(instrument_key)
                intraday_df = self.fetch_intraday_15min(instrument_key)

                if daily_df.empty:
                    print("⚠️  No daily data")
                    failed_symbols.append(symbol)
                    continue

                all_data[symbol] = {"daily": daily_df, "intraday": intraday_df}
                print("✓")

            except Exception as e:
                print(f"❌ Error: {str(e)}")
                failed_symbols.append(symbol)
                continue

        print(f"\nSuccessfully fetched: {len(all_data)}/{len(NIFTY50_SYMBOLS)} stocks")
        if failed_symbols:
            print(f"Failed symbols: {', '.join(failed_symbols)}")

        return all_data
