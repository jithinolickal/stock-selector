"""Option scalping families on 1-min Nifty data.

Selling: short ATM straddle for fixed 30/60-min windows through the day; afternoon-only 0DTE.
Buying: index signal -> buy ATM option, % target / % stop / time stop (ORB, momentum burst,
EMA pullback, long straddle). Each config x DTE bucket (0 = expiry day, 1-6 = other days).
"""
import multiprocessing as mp
import sys
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from options import data
from options.engine import Leg, Setup, _charges, lot_size, run, summary

TZ = "Asia/Kolkata"
STR = [Leg("CE", 0, "SELL"), Leg("PE", 0, "SELL")]
START, END = "2021-06-01", "2026-08-31"
DTE = {"0": (0, 0), "1-6": (1, 6)}


def plus(t: time, minutes: int) -> time:
    return (datetime.combine(datetime.today(), t) + timedelta(minutes=minutes)).time()


def sell_setups():
    S = []
    for h, m in ((9, 20), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0)):
        for hold in (30, 60):
            for k, (lo, hi) in DTE.items():
                S.append(Setup(f"sell_win_{h:02d}{m:02d}_{hold}m_dte{k}", STR, entry=time(h, m), exit=plus(time(h, m), hold), leg_sl_pct=25, min_dte=lo, max_dte=hi))
    for h in (12, 13, 14):
        for sl in (25, 40):
            S.append(Setup(f"sell_pm_{h:02d}00_sl{sl}_dte0", STR, entry=time(h, 0), leg_sl_pct=sl, min_dte=0, max_dte=0))
    return S


# ---------------- buying scalps ----------------
@dataclass
class P:
    name: str
    sig: str
    sl: float
    tg: float
    hold: int           # minutes, 999 = till 15:10
    max_trades: int = 1
    dte: str = "0"
    thr: float = 0.0025
    overlap: bool = False
    slip: float = 0.01
    side: str = "BUY"   # SELL: sell the option (ORB credit scalp), stop on rise, target on fall
    rng: int = 15       # opening-range minutes for orb signals


def sig_orb(d, p):
    hi, lo = d.high.iloc[:p.rng].max(), d.low.iloc[:p.rng].min()
    c = d.close
    up, dn = ("CE", "PE") if p.side == "BUY" else ("PE", "CE")  # selling: sell the far-side option
    for i in range(p.rng, len(c) - 60):
        if c.iloc[i] > hi:
            return [(i, up)]
        if c.iloc[i] < lo:
            return [(i, dn)]
    return []


def sig_burst(d, p):
    r = d.close.pct_change(5)
    out = []
    for i in range(15, 315):
        if r.iloc[i] > p.thr:
            out.append((i, "CE"))
        elif r.iloc[i] < -p.thr:
            out.append((i, "PE"))
    return out


def sig_pullback(d, p):
    c = d.close
    e = c.ewm(span=20, adjust=False).mean()
    above = (c > e).to_numpy()
    o = c.iloc[0]
    out = []
    for i in range(30, 315):
        if above[i] and not above[i - 1] and c.iloc[i] > o:
            out.append((i, "CE"))
        elif not above[i] and above[i - 1] and c.iloc[i] < o:
            out.append((i, "PE"))
    return out


def sig_lstraddle(d, p):
    return [(4, "CE"), (4, "PE")]  # 9:19 signal -> 9:20 fill


SIG = dict(orb=sig_orb, burst=sig_burst, pullback=sig_pullback, lstr=sig_lstraddle)


def buy_day(symbol, day, p):
    expiry = data.nearest_expiry(symbol, day)
    if expiry is None:
        return []
    dte = (pd.Timestamp(expiry) - pd.Timestamp(day)).days
    lo, hi = DTE[p.dte]
    if not (lo <= dte <= hi):
        return []
    ix = data.index(symbol)
    d = ix[ix.trading_day == day]
    grid = pd.date_range(f"{day} 09:15", f"{day} 15:10", freq="1min", tz=TZ)
    d = d[~d.index.duplicated(keep="last")].reindex(grid).ffill()
    if d.close.isna().iloc[0] or len(d) < 300:
        return []
    dc = data.day_chain(symbol, expiry, day)
    if dc.empty:
        return []
    lot = lot_size(symbol, day)
    cache = {}
    trades, last_exit, n = [], -1, 0
    for pos, opt in SIG[p.sig](d, p):
        if n >= p.max_trades or (not p.overlap and pos <= last_exit):
            continue
        f = pos + 1
        if f >= len(grid) - 2:
            break
        strike = data.atm(symbol, float(d.close.iloc[pos]))
        s = cache.setdefault((strike, opt), data.leg_series(dc, strike, opt, grid))
        if s is None or pd.isna(s.iloc[f]):
            continue
        e0 = float(s.iloc[f])
        sgn = 1 if p.side == "BUY" else -1
        entry = e0 * (1 + sgn * p.slip)
        end = min(f + p.hold, len(grid) - 1)
        why, j, exit_px = "time", end, None
        for j in range(f + 1, end + 1):
            px = s.iloc[j]
            if pd.isna(px):
                continue
            if sgn * (px - e0) <= -e0 * p.sl / 100:
                why, exit_px = "sl", px * (1 - sgn * p.slip)
                break
            if sgn * (px - e0) >= e0 * p.tg / 100:
                why, exit_px = "tg", px * (1 - sgn * p.slip)
                break
        if exit_px is None:
            last = s.iloc[f:end + 1].dropna()
            exit_px = float(last.iloc[-1]) * (1 - sgn * p.slip)
        gross = sgn * (exit_px - entry) * lot
        cost = _charges(entry * lot, sgn < 0) + _charges(exit_px * lot, sgn > 0)
        trades.append(dict(day=day, dte=dte, t=grid[f].strftime("%H:%M"), opt=opt, strike=strike, entry=round(e0, 2), exit=round(exit_px, 2),
                           why=why, gross=round(gross), cost=round(cost), net=round(gross - cost)))
        last_exit, n = j, n + 1
    return trades


def buy_configs():
    C = []
    for k in DTE:
        for sl, tg, hold in ((20, 40, 60), (30, 60, 180), (25, 50, 999)):
            C.append(P(f"buy_orb15_sl{sl}_tg{tg}_h{hold}_dte{k}", "orb", sl, tg, hold, 1, k))
        for thr in (0.0025, 0.004):
            for hold in (15, 30):
                C.append(P(f"buy_burst{thr * 100:.2f}_h{hold}_dte{k}", "burst", 20, 30, hold, 3, k, thr=thr))
        for sl, tg, hold in ((20, 30, 30), (25, 50, 60)):
            C.append(P(f"buy_pullback_sl{sl}_tg{tg}_h{hold}_dte{k}", "pullback", sl, tg, hold, 3, k))
        for sl, tg in ((30, 100), (40, 80)):
            C.append(P(f"buy_lstraddle_sl{sl}_tg{tg}_dte{k}", "lstr", sl, tg, 999, 2, k, overlap=True))
        for rng in (15, 60):
            for sl, tg in ((25, 50), (40, 80)):
                C.append(P(f"sell_orb{rng}_far_sl{sl}_tg{tg}_dte{k}", "orb", sl, tg, 999, 1, k, side="SELL", rng=rng))
    return C


def _sell(a):
    sym, s = a
    t = run(sym, s, START, END)
    t["setup"] = s.name
    return t


def _buy(a):
    sym, p, days = a
    rows = [r for d in days for r in buy_day(sym, d, p)]
    t = pd.DataFrame(rows)
    t["setup"] = p.name
    return t


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol", nargs="?", default="NIFTY")
    ap.add_argument("--slip", type=float, default=1.0, help="slippage % per fill")
    ap.add_argument("--only", default="", help="substring filter on setup name")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    sym = a.symbol
    days = sorted({d for d in data.index(sym).trading_day.unique() if START <= d <= END})
    chunks = [days[i::6] for i in range(6)]
    S = [s for s in sell_setups() if a.only in s.name]
    B = [p for p in buy_configs() if a.only in p.name]
    for s in S:
        s.slippage_pct = a.slip
    for p in B:
        p.slip = a.slip / 100
    with mp.get_context("fork").Pool() as pool:
        sells = pool.map(_sell, [(sym, s) for s in S])
        buys = pool.map(_buy, [(sym, p, ch) for p in B for ch in chunks])
    all_t = pd.concat([x for x in sells + buys if not x.empty])
    sym = f"{sym}{a.tag}"
    all_t.to_csv(config.RESULTS_DIR / f"options_scalp_{sym}.csv", index=False)
    rows = []
    for name, t in all_t.groupby("setup", sort=False):
        t = t.sort_values("day")
        m = summary(t)
        m.update(setup=name, per_day=round(len(t) / max(1, t.day.nunique()), 1), t_stat=round(t.net.mean() / t.net.std() * np.sqrt(len(t)), 1) if len(t) > 2 else 0)
        m.update({f"y{y}": v for y, v in t.groupby(pd.to_datetime(t.day).dt.year).net.sum().round().items()})
        if "why" in t:
            m["exits"] = t.why.value_counts(normalize=True).round(2).to_dict()
        rows.append(m)
    df = pd.DataFrame(rows)
    cols = ["setup", "days", "per_day", "win_rate", "pf", "t_stat", "net_per_month", "gross_per_month", "max_dd", "worst_day", "cost_share"] + sorted(c for c in df.columns if c.startswith("y")) + ["exits"]
    pd.set_option("display.width", 300)
    pd.set_option("display.max_colwidth", 60)
    print(df[cols].sort_values("pf", ascending=False).to_string(index=False))
    df.to_csv(config.RESULTS_DIR / f"options_scalp_{sym}_summary.csv", index=False)
