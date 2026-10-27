"""Feature scan: per symbol-day features vs forward intraday returns (bps).
Tells us where, if anywhere, a conditional mean move exceeds friction."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from data import upstox

FRICTION_BPS = 15  # ~8 bps charges + ~2x1-5 bps slippage on 1L notional


def day_table(sym, df):
    g = df.groupby(df.index.date)
    rows = []
    for day, b in g:
        if len(b) < 70 or b.index[0].time() != pd.Timestamp("09:15").time():
            continue
        tt = b.index.time
        px = lambda t: b.loc[tt <= t, "close"].iloc[-1]
        o = b["open"].iloc[0]
        rows.append(dict(symbol=sym, day=day, open=o, close=b["close"].iloc[-1],
                         r_15=(px(pd.Timestamp("09:30").time()) - o) / o, r_30=(px(pd.Timestamp("09:45").time()) - o) / o,
                         p_1445=px(pd.Timestamp("14:45").time()), p_1015=px(pd.Timestamp("10:15").time()), p_1315=px(pd.Timestamp("13:15").time()),
                         vol_15=b["volume"].iloc[:3].sum(), rng_15=(b["high"].iloc[:3].max() - b["low"].iloc[:3].min()) / o))
    t = pd.DataFrame(rows).set_index("day")
    t["prev_close"] = t["close"].shift(1)
    t["gap"] = t["open"] / t["prev_close"] - 1
    t["prev_ret"] = t["prev_close"].pct_change()
    t["rvol_15"] = t["vol_15"] / t["vol_15"].rolling(14).mean().shift(1)
    # forward returns (bps)
    t["fwd_0930_1515"] = (t["close"] / (t["open"] * (1 + t["r_15"])) - 1) * 1e4
    t["fwd_0930_1015"] = (t["p_1015"] / (t["open"] * (1 + t["r_15"])) - 1) * 1e4
    t["fwd_1445_1515"] = (t["close"] / t["p_1445"] - 1) * 1e4
    t["fwd_1315_1515"] = (t["close"] / t["p_1315"] - 1) * 1e4
    t["fwd_0920_1515"] = (t["close"] / t["open"] - 1) * 1e4  # approx: from open
    return t.reset_index()


def main():
    nifty = upstox.load("NIFTY50")
    n = day_table("NIFTY50", nifty)[["day", "r_15", "r_30", "gap"]].rename(columns={"r_15": "n_r15", "r_30": "n_r30", "gap": "n_gap"})
    frames = []
    for s in config.NIFTY50:
        try:
            frames.append(day_table(s, upstox.load(s)))
        except FileNotFoundError:
            pass
    t = pd.concat(frames).merge(n, on="day").dropna()
    t["oos"] = pd.to_datetime(t["day"]) >= "2025-01-01"
    t.to_parquet(config.RESULTS_DIR / "scan.parquet")
    print(f"{len(t)} symbol-days, {t.symbol.nunique()} symbols\n")

    def cond(name, mask, fwd, sign, feat):
        """mean signed forward return (bps) when mask holds; sign=+1 follow, -1 fade"""
        out = []
        for oos in (False, True):
            m = t[mask & (t.oos == oos)]
            if len(m) < 30:
                out.append(f"n={len(m):<5} --"); continue
            r = sign * np.sign(m[feat]) * m[fwd]
            out.append(f"n={len(m):<5} mean={r.mean():>6.1f}bps  hit={(r > 0).mean() * 100:>4.0f}%")
        print(f"{name:<52} IS {out[0]}  | OOS {out[1]}")

    big = lambda col, q: t[col].abs() > t[col].abs().quantile(q)
    sgn = lambda col: np.sign(t[col])
    print("--- Follow (sign * fwd > 0 means continuation pays) ---")
    for fwd in ["fwd_0930_1015", "fwd_0930_1515"]:
        cond(f"follow r_15 (|r15| top 30%) -> {fwd}", big("r_15", 0.7), fwd, 1, "r_15")
        cond(f"follow r_15 & rvol>1.5 -> {fwd}", big("r_15", 0.7) & (t.rvol_15 > 1.5), fwd, 1, "r_15")
        cond(f"follow gap (|gap| top 30%) -> {fwd}", big("gap", 0.7), fwd, 1, "gap")
        cond(f"follow gap>1% -> {fwd}", t.gap.abs() > 0.01, fwd, 1, "gap")
        cond(f"follow r_15 when nifty r15 agrees -> {fwd}", big("r_15", 0.7) & (sgn("r_15") == sgn("n_r15")), fwd, 1, "r_15")
        cond(f"follow prev_ret (top 30%) -> {fwd}", big("prev_ret", 0.7), fwd, 1, "prev_ret")
    print("--- Last-hour momentum ---")
    for fwd in ["fwd_1445_1515", "fwd_1315_1515"]:
        cond(f"follow r_30 -> {fwd}", big("r_30", 0.7), fwd, 1, "r_30")
    # day-so-far sign
    dsf = np.sign(t.p_1445 / t.open - 1)
    for oos in (False, True):
        m = t[t.oos == oos]; r = dsf[m.index] * m.fwd_1445_1515
        print(f"follow day-so-far sign -> fwd_1445_1515 {'OOS' if oos else 'IS'}: n={len(m)} mean={r.mean():.1f}bps hit={(r>0).mean()*100:.0f}%")
    print("--- Fade ---")
    for fwd in ["fwd_0930_1015", "fwd_0930_1515"]:
        cond(f"fade r_15 (|r15| top 30%) -> {fwd}", big("r_15", 0.7), fwd, -1, "r_15")
        cond(f"fade gap>1% -> {fwd}", t.gap.abs() > 0.01, fwd, -1, "gap")
        cond(f"fade r_15 when nifty r15 disagrees -> {fwd}", big("r_15", 0.7) & (sgn("r_15") != sgn("n_r15")), fwd, -1, "r_15")
    print(f"\nfriction to beat ~{FRICTION_BPS} bps per round trip")
    print("\nunconditional |fwd| (bps):", {c: round(t[c].abs().mean(), 1) for c in ["fwd_0930_1015", "fwd_0930_1515", "fwd_1445_1515"]})


if __name__ == "__main__":
    main()
