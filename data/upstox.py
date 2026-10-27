"""Upstox V3 historical candles -> parquet.

V3 limits: unit=minutes (1-15) allows 1 month per request, (>15) 1 quarter;
unit=days allows 1 year. Intraday history starts Jan 2022.
"""
import os
import time as _time
from datetime import date, datetime, timedelta
from urllib.parse import quote

import pandas as pd
import requests
from dotenv import load_dotenv

import config

load_dotenv(config.ROOT / ".env")
BASE = "https://api.upstox.com/v3/historical-candle"
COLS = ["timestamp", "open", "high", "low", "close", "volume", "oi"]


def _token() -> str:
    tok = os.getenv("UPSTOX_ACCESS_TOKEN")
    if not tok:
        raise RuntimeError("UPSTOX_ACCESS_TOKEN missing in .env")
    return tok


def _get(url: str, retries: int = 5) -> list:
    for attempt in range(retries):
        try:
            r = requests.get(url, headers={"Authorization": f"Bearer {_token()}", "Accept": "application/json"}, timeout=30)
        except requests.ConnectionError:
            _time.sleep(2 ** attempt)
            continue
        if r.status_code == 429:
            _time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
        return r.json().get("data", {}).get("candles", [])
    raise RuntimeError(f"failed after {retries} retries: {url}")


def _to_df(candles: list) -> pd.DataFrame:
    if not candles:
        return pd.DataFrame(columns=COLS).set_index("timestamp")
    df = pd.DataFrame(candles, columns=COLS)
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_convert("Asia/Kolkata")
    return df.set_index("timestamp").sort_index()


def fetch(instrument_key: str, unit: str, interval: int, start: date, end: date) -> pd.DataFrame:
    """Fetch candles over [start, end], chunking to respect the per-request window."""
    window = timedelta(days=28) if (unit == "minutes" and interval <= 15) else timedelta(days=85) if unit == "minutes" else timedelta(days=360)
    frames = []
    cur = start
    while cur <= end:
        to = min(cur + window, end)
        url = f"{BASE}/{quote(instrument_key, safe='')}/{unit}/{interval}/{to:%Y-%m-%d}/{cur:%Y-%m-%d}"
        frames.append(_to_df(_get(url)))
        cur = to + timedelta(days=1)
    df = pd.concat(frames)
    return df[~df.index.duplicated(keep="last")].sort_index()


def fetch_today(instrument_key: str, interval: int = config.INTERVAL_MINUTES) -> pd.DataFrame:
    url = f"{BASE}/intraday/{quote(instrument_key, safe='')}/minutes/{interval}"
    return _to_df(_get(url))


def parquet_path(symbol: str, unit: str, interval: int):
    return config.DATA_DIR / f"{unit}_{interval}" / f"{symbol}.parquet"


def download(symbol: str, instrument_key: str, unit: str = "minutes", interval: int = config.INTERVAL_MINUTES,
             start: str = config.HISTORY_START, end: date | None = None) -> pd.DataFrame:
    """Incremental download: resumes from the last stored candle."""
    end = end or date.today()
    path = parquet_path(symbol, unit, interval)
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = pd.read_parquet(path) if path.exists() else None
    begin = existing.index.max().date() if existing is not None and len(existing) else datetime.strptime(start, "%Y-%m-%d").date()
    new = fetch(instrument_key, unit, interval, begin, end)
    df = pd.concat([existing, new]) if existing is not None else new
    df = df[~df.index.duplicated(keep="last")].sort_index()
    df.to_parquet(path)
    return df


def load(symbol: str, unit: str = "minutes", interval: int = config.INTERVAL_MINUTES) -> pd.DataFrame:
    return pd.read_parquet(parquet_path(symbol, unit, interval))
