"""Download/refresh candles for the universe. Needs UPSTOX_ACCESS_TOKEN in .env."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from data import instruments, upstox

p = argparse.ArgumentParser()
p.add_argument("--symbols", nargs="*", default=config.NIFTY50)
p.add_argument("--interval", type=int, default=config.INTERVAL_MINUTES)
p.add_argument("--daily", action="store_true", help="also fetch daily candles")
a = p.parse_args()

keys = instruments.load()
for i, s in enumerate(a.symbols, 1):
    if s not in keys:
        print(f"[{i}] {s}: no instrument key, skipped")
        continue
    df = upstox.download(s, keys[s], "minutes", a.interval)
    msg = f"[{i}/{len(a.symbols)}] {s}: {len(df)} bars, {df.index.min().date()} -> {df.index.max().date()}"
    if a.daily:
        d = upstox.download(s, keys[s], "days", 1, start="2015-01-01")
        msg += f" | daily {len(d)}"
    print(msg)
