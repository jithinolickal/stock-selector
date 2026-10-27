"""Symbol -> Upstox instrument_key mapping for NSE equities."""
import gzip
import json
from pathlib import Path

import requests

URL = "https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz"
CACHE = Path(__file__).parent / "instruments.json"


def load(refresh: bool = False) -> dict[str, str]:
    if CACHE.exists() and not refresh:
        return json.loads(CACHE.read_text())
    raw = requests.get(URL, timeout=60)
    raw.raise_for_status()
    rows = json.loads(gzip.decompress(raw.content))
    mapping = {
        r["trading_symbol"]: r["instrument_key"]
        for r in rows
        if r.get("segment") == "NSE_EQ" and r.get("instrument_type") == "EQ"
    }
    CACHE.write_text(json.dumps(mapping, indent=0, sort_keys=True))
    return mapping
