"""Daily (non-expiry) option ideas, round 2:
  A. overnight short straddle/strangle: sell 15:20, buy back 9:20 next day (no stop possible overnight)
  B. 9:20 full-day straddle on DTE 1-6 filtered by India VIX level / VIX change
  C. 9:20 full-day straddle on DTE 1-6 filtered by premium richness: straddle credit vs recent realized intraday range
"""
import multiprocessing as mp
import sys
from datetime import time
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
VIX = pd.read_parquet(config.ROOT / "data" / "external" / "india_vix_daily.parquet").close
VIX.index = VIX.index.strftime("%Y-%m-%d")


# ---------- A. overnight ----------
def overnight_day(symbol, day, nxt, otm_pct, slip=0.01):
    expiry = data.nearest_expiry(symbol, day)
    if expiry is None:
        return None
    if expiry == day:  # today's contract dies at 15:30 -> use next weekly
        e = [x for x in data.expiries(symbol) if x > day]
        if not e:
            return None
        expiry = e[0]
    if expiry < nxt:
        return None
    dte = (pd.Timestamp(expiry) - pd.Timestamp(day)).days
    t_in = pd.Timestamp(f"{day} 15:20", tz=TZ)
    t_out = pd.Timestamp(f"{nxt} 09:20", tz=TZ)
    spot = data.spot_at(symbol, t_in)
    if spot is None:
        return None
    step = data.STEP[symbol]
    atm = data.atm(symbol, spot)
    off = int(round(spot * otm_pct / 100 / step)) * step
    dc0, dc1 = data.day_chain(symbol, expiry, day), data.day_chain(symbol, expiry, nxt)
    if dc0.empty or dc1.empty:
        return None
    lot = lot_size(symbol, day)
    gross = cost = 0.0
    legs = []
    for opt, strike in (("CE", atm + off), ("PE", atm - off)):
        s0 = data.leg_series(dc0, strike, opt, pd.DatetimeIndex([t_in]))
        s1 = data.leg_series(dc1, strike, opt, pd.DatetimeIndex([t_out]))
        if s0 is None or s1 is None or pd.isna(s0.iloc[0]) or pd.isna(s1.iloc[0]):
            return None
        e, x = float(s0.iloc[0]) * (1 - slip), float(s1.iloc[0]) * (1 + slip)
        gross += (e - x) * lot
        cost += _charges(e * lot, True) + _charges(x * lot, False)
        legs.append(f"S{opt}{strike}@{e:.1f}->{x:.1f}")
    return dict(day=day, dte=dte, spot=spot, gross=round(gross), cost=round(cost), net=round(gross - cost), legs=" ".join(legs),
                weekday=pd.Timestamp(day).day_name()[:3])


def _overnight(a):
    symbol, otm, days = a
    rows = []
    for d, n in zip(days[:-1], days[1:]):
        r = overnight_day(symbol, d, n, otm)
        if r:
            rows.append(r)
    t = pd.DataFrame(rows)
    t["setup"] = f"overnight_otm{otm}"
    return t


# ---------- B/C. filtered intraday straddles ----------
class VixFilter:
    def __init__(self, lo, hi):
        self.lo, self.hi = lo, hi

    def __call__(self, symbol, day, t_in):
        v = VIX.get(day)
        return v is not None and self.lo <= v < self.hi


class VixJump:  # VIX rose >= pct the previous day
    def __init__(self, pct):
        self.pct = pct

    def __call__(self, symbol, day, t_in):
        i = VIX.index.get_loc(day) if day in VIX.index else None
        if i is None or i < 1:
            return False
        return (VIX.iloc[i - 1] / VIX.iloc[i - 2] - 1) * 100 >= self.pct


class RichPremium:
    """Straddle credit (as % of spot) vs mean |9:20->15:10 move| of the last n days. Trade if ratio >= k."""
    def __init__(self, k, n=10):
        self.k, self.n = k, n
        self.cache = {}

    def _move(self, symbol, day):
        if (symbol, day) not in self.cache:
            ix = data.index(symbol)
            d = ix[ix.trading_day == day]
            a, b = d.between_time("09:20", "09:21").close, d.between_time("15:09", "15:10").close
            self.cache[(symbol, day)] = abs(b.iloc[-1] / a.iloc[0] - 1) * 100 if len(a) and len(b) else np.nan
        return self.cache[(symbol, day)]

    def __call__(self, symbol, day, t_in):
        days = sorted(data.index(symbol).trading_day.unique())
        i = days.index(day)
        if i < self.n:
            return False
        rv = np.nanmean([self._move(symbol, d) for d in days[i - self.n:i]])
        expiry = data.nearest_expiry(symbol, day)
        spot = data.spot_at(symbol, t_in)
        atm = data.atm(symbol, spot)
        dc = data.day_chain(symbol, expiry, day)
        g = pd.DatetimeIndex([t_in])
        c, p = data.leg_series(dc, atm, "CE", g), data.leg_series(dc, atm, "PE", g)
        if c is None or p is None or pd.isna(c.iloc[0]) or pd.isna(p.iloc[0]):
            return False
        credit_pct = (c.iloc[0] + p.iloc[0]) / spot * 100
        return rv > 0 and credit_pct / rv >= self.k


def setups():
    S = []
    for lo, hi in ((0, 12), (12, 14), (14, 17), (17, 20), (20, 99)):
        S.append(Setup(f"dte1-6_vix{lo}-{hi}", STR, entry=time(9, 20), leg_sl_pct=25, min_dte=1, max_dte=6, day_filter=VixFilter(lo, hi)))
    S.append(Setup("dte1-6_vixjump5", STR, entry=time(9, 20), leg_sl_pct=25, min_dte=1, max_dte=6, day_filter=VixJump(5)))
    S.append(Setup("dte1-6_vixjump10", STR, entry=time(9, 20), leg_sl_pct=25, min_dte=1, max_dte=6, day_filter=VixJump(10)))
    for k in (1.5, 2.0, 2.5, 3.0):
        S.append(Setup(f"dte1-6_rich{k}", STR, entry=time(9, 20), leg_sl_pct=25, min_dte=1, max_dte=6, day_filter=RichPremium(k)))
        S.append(Setup(f"dte1_rich{k}", STR, entry=time(9, 20), leg_sl_pct=25, min_dte=1, max_dte=1, day_filter=RichPremium(k)))
    S.append(Setup("dte0_vix20+", STR, entry=time(9, 20), leg_sl_pct=25, min_dte=0, max_dte=0, day_filter=VixFilter(20, 99)))
    S.append(Setup("dte0_vix<20", STR, entry=time(9, 20), leg_sl_pct=25, min_dte=0, max_dte=0, day_filter=VixFilter(0, 20)))
    return S


def _sell(a):
    sym, s = a
    t = run(sym, s, START, END)
    t["setup"] = s.name
    return t


def table(all_t, by=None):
    rows = []
    for name, t in all_t.groupby("setup", sort=False):
        m = summary(t)
        m.update(setup=name, t_stat=round(t.net.mean() / t.net.std() * np.sqrt(len(t)), 1) if len(t) > 2 else 0)
        m.update({f"y{y}": v for y, v in t.groupby(pd.to_datetime(t.day).dt.year).net.sum().round().items()})
        rows.append(m)
    df = pd.DataFrame(rows)
    cols = ["setup", "days", "win_rate", "pf", "t_stat", "net_per_month", "gross_per_month", "max_dd", "worst_day"] + sorted(c for c in df.columns if c.startswith("y"))
    return df[cols].to_string(index=False)


if __name__ == "__main__":
    sym = sys.argv[1] if len(sys.argv) > 1 else "NIFTY"
    days = sorted({d for d in data.index(sym).trading_day.unique() if START <= d <= END})
    pd.set_option("display.width", 300)
    with mp.get_context("fork").Pool() as pool:
        on = pool.map(_overnight, [(sym, otm, days) for otm in (0.0, 1.0, 2.0)])
        fl = pool.map(_sell, [(sym, s) for s in setups()])
    on_t = pd.concat([x for x in on if not x.empty])
    on_t.to_csv(config.RESULTS_DIR / f"options_overnight_{sym}.csv", index=False)
    print("== A. overnight 15:20 -> 9:20, all DTE ==")
    print(table(on_t))
    for name, t in on_t.groupby("setup"):
        print(f"\n{name} by DTE at entry:")
        print(t.groupby("dte").net.agg(["count", "mean", "sum"]).round().T.to_string())
        print(f"{name} by weekday:", t.groupby("weekday").net.agg(["count", "mean"]).round().to_dict())
    fl_t = pd.concat([x for x in fl if not x.empty])
    fl_t.to_csv(config.RESULTS_DIR / f"options_daily_filters_{sym}.csv", index=False)
    print("\n== B/C. 9:20 straddle with VIX / premium-richness filters ==")
    print(table(fl_t))
