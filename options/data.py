"""Access to the HF 1-min index-options dataset (data/external/hf_options)."""
from functools import lru_cache
from pathlib import Path

import pandas as pd

import config

ROOT = config.ROOT / "data" / "external" / "hf_options"
STEP = {"NIFTY": 50, "SENSEX": 100, "BANKNIFTY": 100}


@lru_cache(maxsize=4)
def index(symbol: str) -> pd.DataFrame:
    df = pd.read_parquet(ROOT / "index" / f"{symbol}.parquet")
    return df.set_index("timestamp").sort_index()


def expiries(symbol: str) -> list[str]:
    return sorted(p.stem for p in (ROOT / "options" / symbol).glob("*.parquet"))


def nearest_expiry(symbol: str, day: str) -> str | None:
    e = [x for x in expiries(symbol) if x >= day]
    return e[0] if e else None


@lru_cache(maxsize=8)
def chain(symbol: str, expiry: str) -> pd.DataFrame:
    df = pd.read_parquet(ROOT / "options" / symbol / f"{expiry}.parquet")
    return df.set_index("timestamp").sort_index()


def day_chain(symbol: str, expiry: str, day: str) -> pd.DataFrame:
    c = chain(symbol, expiry)
    return c[c.trading_day == day]


def leg_series(dc: pd.DataFrame, strike: int, opt: str, grid: pd.DatetimeIndex) -> pd.Series | None:
    """1-min close series for one contract on the day's minute grid, forward-filled."""
    s = dc[(dc.strike == strike) & (dc.option_type == opt)]["close"]
    if s.empty:
        return None
    s = s[~s.index.duplicated(keep="last")]
    return s.reindex(grid.union(s.index)).ffill().reindex(grid)


def spot_at(symbol: str, ts: pd.Timestamp) -> float | None:
    ix = index(symbol)
    s = ix.loc[:ts, "close"]
    return float(s.iloc[-1]) if len(s) else None


def atm(symbol: str, spot: float) -> int:
    step = STEP[symbol]
    return int(round(spot / step) * step)
