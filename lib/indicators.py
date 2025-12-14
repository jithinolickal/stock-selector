"""Technical indicators calculation module"""

import pandas as pd
import numpy as np
import pandas_ta as ta


def calculate_ema(df: pd.DataFrame, period: int, column: str = "close") -> pd.Series:
    """
    Calculate Exponential Moving Average

    Args:
        df: DataFrame with OHLCV data
        period: EMA period
        column: Column to calculate EMA on

    Returns:
        Series with EMA values
    """
    return ta.ema(df[column], length=period)


def calculate_rsi(df: pd.DataFrame, period: int = 14, column: str = "close") -> pd.Series:
    """
    Calculate Relative Strength Index

    Args:
        df: DataFrame with OHLCV data
        period: RSI period (default 14)
        column: Column to calculate RSI on

    Returns:
        Series with RSI values
    """
    return ta.rsi(df[column], length=period)


def calculate_adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate Average Directional Index

    Args:
        df: DataFrame with OHLCV data (must have high, low, close)
        period: ADX period (default 14)

    Returns:
        Series with ADX values
    """
    adx_df = ta.adx(df["high"], df["low"], df["close"], length=period)
    return adx_df[f"ADX_{period}"]


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate Average True Range

    Args:
        df: DataFrame with OHLCV data (must have high, low, close)
        period: ATR period (default 14)

    Returns:
        Series with ATR values
    """
    return ta.atr(df["high"], df["low"], df["close"], length=period)


def calculate_vwap(df: pd.DataFrame) -> pd.Series:
    """
    Calculate Volume Weighted Average Price

    Args:
        df: DataFrame with OHLCV data

    Returns:
        Series with VWAP values
    """
    return ta.vwap(df["high"], df["low"], df["close"], df["volume"])


def calculate_ema_slope(ema_series: pd.Series, days: int = 5) -> float:
    """
    Calculate EMA slope over specified days

    Args:
        ema_series: Series with EMA values
        days: Number of days to check slope

    Returns:
        Slope value (positive indicates upward trend)
    """
    if len(ema_series) < days:
        return 0.0

    recent_ema = ema_series.iloc[-days:]
    x = np.arange(len(recent_ema))
    slope = np.polyfit(x, recent_ema.values, 1)[0]
    return slope


def calculate_volume_ratio(df: pd.DataFrame, period: int = 20) -> float:
    """
    Calculate current volume to average volume ratio

    Args:
        df: DataFrame with volume data
        period: Period for average volume calculation

    Returns:
        Volume ratio (current / average)
    """
    if len(df) < period + 1:
        return 0.0

    avg_volume = df["volume"].iloc[-period - 1 : -1].mean()
    current_volume = df["volume"].iloc[-1]

    if avg_volume == 0:
        return 0.0

    return current_volume / avg_volume


def calculate_atr_ratio(atr_series: pd.Series, period: int = 20) -> float:
    """
    Calculate current ATR to its average ratio

    Args:
        atr_series: Series with ATR values
        period: Period for average ATR calculation

    Returns:
        ATR ratio (current / average)
    """
    if len(atr_series) < period + 1:
        return 0.0

    avg_atr = atr_series.iloc[-period - 1 : -1].mean()
    current_atr = atr_series.iloc[-1]

    if avg_atr == 0:
        return 0.0

    return current_atr / avg_atr


def calculate_relative_strength(
    stock_df: pd.DataFrame, index_df: pd.DataFrame, period: int = 20
) -> float:
    """
    Calculate relative strength of stock vs index

    Args:
        stock_df: Stock DataFrame with close prices
        index_df: Index DataFrame with close prices
        period: Period for RS calculation

    Returns:
        Relative strength value (positive means outperforming)
    """
    if len(stock_df) < period or len(index_df) < period:
        return 0.0

    # Calculate percentage returns over period
    stock_return = (
        (stock_df["close"].iloc[-1] - stock_df["close"].iloc[-period])
        / stock_df["close"].iloc[-period]
    ) * 100

    index_return = (
        (index_df["close"].iloc[-1] - index_df["close"].iloc[-period])
        / index_df["close"].iloc[-period]
    ) * 100

    # Relative strength = stock return - index return
    return stock_return - index_return


def check_higher_lows(df: pd.DataFrame, lookback: int = 5) -> int:
    """
    Count consecutive higher lows in recent price action

    Args:
        df: DataFrame with OHLCV data
        lookback: Number of periods to check

    Returns:
        Count of consecutive higher lows
    """
    if len(df) < lookback:
        return 0

    recent_lows = df["low"].tail(lookback).values
    higher_lows = 0

    for i in range(1, len(recent_lows)):
        if recent_lows[i] > recent_lows[i - 1]:
            higher_lows += 1
        else:
            break

    return higher_lows


def detect_consolidation(df: pd.DataFrame, days: int = 5, max_range_pct: float = 0.03) -> bool:
    """
    Detect if stock is in consolidation (tight range)

    Args:
        df: DataFrame with OHLCV data
        days: Number of days to check
        max_range_pct: Maximum range as percentage (e.g., 0.03 = 3%)

    Returns:
        True if in consolidation
    """
    if len(df) < days:
        return False

    recent = df.tail(days)
    high = recent["high"].max()
    low = recent["low"].min()
    range_pct = (high - low) / low

    return range_pct <= max_range_pct


def check_volume_expansion(df: pd.DataFrame, days: int = 3) -> bool:
    """
    Check if volume is expanding over last N days

    Args:
        df: DataFrame with OHLCV data
        days: Number of days to check

    Returns:
        True if volume is expanding
    """
    if len(df) < days:
        return False

    recent_volume = df["volume"].tail(days).values

    # Check if each day has higher volume than previous
    for i in range(1, len(recent_volume)):
        if recent_volume[i] <= recent_volume[i - 1]:
            return False

    return True


def detect_bullish_engulfing(df: pd.DataFrame) -> bool:
    """
    Detect bullish engulfing pattern in last 2 candles

    Args:
        df: DataFrame with OHLCV data

    Returns:
        True if bullish engulfing detected
    """
    if len(df) < 2:
        return False

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    # Previous candle bearish, current bullish
    prev_bearish = prev["close"] < prev["open"]
    curr_bullish = curr["close"] > curr["open"]

    # Current engulfs previous
    engulfs = curr["open"] <= prev["close"] and curr["close"] >= prev["open"]

    return prev_bearish and curr_bullish and engulfs


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add all technical indicators to DataFrame

    Args:
        df: DataFrame with OHLCV data

    Returns:
        DataFrame with added indicator columns
    """
    df = df.copy()

    # EMAs
    df["ema_20"] = calculate_ema(df, 20)
    df["ema_50"] = calculate_ema(df, 50)
    df["ema_200"] = calculate_ema(df, 200)

    # RSI
    df["rsi"] = calculate_rsi(df, 14)

    # ADX
    df["adx"] = calculate_adx(df, 14)

    # ATR
    df["atr"] = calculate_atr(df, 14)

    return df


def add_intraday_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add intraday-specific indicators (VWAP, volume, EMAs) to 15-min DataFrame

    Args:
        df: DataFrame with 15-min OHLCV data

    Returns:
        DataFrame with added intraday indicators
    """
    df = df.copy()

    # VWAP
    df["vwap"] = calculate_vwap(df)

    # 20-period volume average for intraday
    df["volume_avg_20"] = df["volume"].rolling(window=20).mean()

    # EMAs for entry levels (9 and 20 period on 15-min)
    df["ema_9"] = calculate_ema(df, 9)
    df["ema_20_intraday"] = calculate_ema(df, 20)

    return df


def find_swing_low(df: pd.DataFrame, lookback: int = 10) -> float:
    """
    Find the last swing low from recent candles

    Args:
        df: DataFrame with OHLCV data
        lookback: Number of recent candles to check

    Returns:
        Swing low price
    """
    if len(df) < lookback:
        lookback = len(df)

    recent_lows = df["low"].tail(lookback)
    return recent_lows.min()

def add_scalping_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add scalping-specific indicators to 3-min DataFrame

    Args:
        df: DataFrame with OHLCV data (3-min candles)

    Returns:
        DataFrame with added scalping indicator columns
    """
    df = df.copy()

    # Fast RSI for scalping (3-period)
    df["rsi_3"] = pandas_ta.rsi(df["close"], length=3)

    # EMAs for entries (9 and 20)
    df["ema_9"] = calculate_ema(df, 9)
    df["ema_20"] = calculate_ema(df, 20)

    # VWAP
    df["vwap"] = calculate_vwap(df)

    # MACD for momentum
    macd = pandas_ta.macd(df["close"], fast=12, slow=26, signal=9)
    if macd is not None and not macd.empty:
        df["macd"] = macd["MACD_12_26_9"]
        df["macd_signal"] = macd["MACDs_12_26_9"]
        df["macd_hist"] = macd["MACDh_12_26_9"]

    # ATR for volatility
    df["atr"] = calculate_atr(df, period=14)

    # 20-period volume average
    df["volume_avg_20"] = df["volume"].rolling(window=20).mean()

    return df
