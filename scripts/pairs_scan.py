"""Intraday pairs trading on Nifty 50 5-min data.

Pairs chosen by daily-return correlation on the in-sample years (2022-24). Signal: z-score of
log(price_a/price_b) vs a rolling mean/std over `lookback` bars (continuous across days).
Enter when |z| >= z_in (long the cheap leg, short the rich leg, equal rupee value), exit when
|z| <= z_out or at 15:15. One position per pair at a time. Costs: both legs, intraday tariff.
"""
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from backtest.costs import round_trip

NOTIONAL = 50_000  # per leg
SLIP = 0.0005       # 5 bps per fill


def load_all():
    px = {}
    for f in sorted((config.DATA_DIR / "minutes_5").glob("*.parquet")):
        df = pd.read_parquet(f)
        px[f.stem] = df.close
    df = pd.DataFrame(px).sort_index()
    return df[(df.index.time >= pd.Timestamp("09:15").time()) & (df.index.time <= pd.Timestamp("15:25").time())]


def pick_pairs(close, start, end, n=15):
    d = close[(close.index >= start) & (close.index < end)].resample("1D").last().dropna(how="all")
    r = np.log(d).diff().dropna()
    c = r.corr()
    pairs = sorted(((c.loc[a, b], a, b) for a, b in combinations(c.columns, 2)), reverse=True)
    return [(a, b, round(rho, 2)) for rho, a, b in pairs[:n]]


def backtest_pair(close, a, b, lookback, z_in, z_out, start, end):
    s = np.log(close[a] / close[b])
    z = (s - s.rolling(lookback).mean()) / s.rolling(lookback).std()
    z = z[(z.index >= start) & (z.index < end)]
    trades, pos = [], None
    for ts, zv in z.items():
        if np.isnan(zv):
            continue
        t = ts.time()
        if pos is None:
            if t >= pd.Timestamp("15:00").time() or t < pd.Timestamp("09:30").time():
                continue
            if abs(zv) >= z_in:
                side = -1 if zv > 0 else 1  # +1: long a short b
                pos = dict(t=ts, side=side, pa=close[a][ts], pb=close[b][ts])
        else:
            if abs(zv) <= z_out or t >= pd.Timestamp("15:15").time() or ts.date() != pos["t"].date():
                pa, pb = close[a][ts], close[b][ts]
                ra = pos["side"] * (pa / pos["pa"] - 1)
                rb = -pos["side"] * (pb / pos["pb"] - 1)
                gross = (ra + rb) * NOTIONAL - 4 * SLIP * NOTIONAL
                cost = 2 * round_trip(NOTIONAL, NOTIONAL)
                trades.append(dict(day=str(ts.date()), pair=f"{a}/{b}", gross=round(gross), cost=round(cost), net=round(gross - cost), mins=(ts - pos["t"]).seconds // 60))
                pos = None
    return pd.DataFrame(trades)


def report(t, label):
    if t.empty:
        print(label, "no trades")
        return
    w = t[t.net > 0]
    pf = w.net.sum() / abs(t[t.net <= 0].net.sum()) if (t.net <= 0).any() else float("inf")
    months = pd.to_datetime(t.day).dt.to_period("M").nunique()
    print(f"{label:28s} trades {len(t):5d}  WR {len(w) / len(t) * 100:4.0f}%  PF {pf:4.2f}  gross/trade {t.gross.mean():6.0f}  net/trade {t.net.mean():6.0f}  net/month {t.net.sum() / max(1, months):7.0f}  avg hold {t.mins.mean():3.0f}m")


if __name__ == "__main__":
    close = load_all()
    pairs = pick_pairs(close, "2022-01-01", "2025-01-01")
    print("pairs:", pairs)
    for lookback, z_in, z_out in ((60, 2.0, 0.5), (120, 2.0, 0.5), (60, 2.5, 0.0), (240, 2.0, 0.5)):
        for label, (s, e) in (("IS 2022-24", ("2022-01-01", "2025-01-01")), ("OOS 2025-26", ("2025-01-01", "2027-01-01"))):
            t = pd.concat([backtest_pair(close, a, b, lookback, z_in, z_out, s, e) for a, b, _ in pairs])
            report(t, f"lb{lookback} z{z_in}/{z_out} {label}")
