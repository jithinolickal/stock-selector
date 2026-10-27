"""Non-expiry-day ideas: afternoon theta, quiet-open filter, quiet-previous-day filter, 1-DTE variants."""
import multiprocessing as mp
import sys
from datetime import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from options import data
from options.engine import Leg, Setup, run, summary

STR = [Leg("CE", 0, "SELL"), Leg("PE", 0, "SELL")]


class quiet_open:
    def __init__(self, max_pct):
        self.max_pct = max_pct

    def __call__(self, symbol, day, t_in):
        ix = data.index(symbol)
        b = ix[(ix.index >= pd.Timestamp(f"{day} 09:15", tz="Asia/Kolkata")) & (ix.index < t_in)]
        return len(b) > 0 and (b.high.max() - b.low.min()) / b.open.iloc[0] * 100 <= self.max_pct


class quiet_prev_day:
    def __init__(self, ratio):
        self.ratio = ratio

    def __call__(self, symbol, day, t_in):
        ix = data.index(symbol)
        d = ix[ix.index < pd.Timestamp(f"{day} 09:15", tz="Asia/Kolkata")]
        daily = d.groupby(d.index.date).agg(h=("high", "max"), l=("low", "min"), c=("close", "last"))
        if len(daily) < 21:
            return False
        rng = (daily.h - daily.l) / daily.c
        return rng.iloc[-1] <= self.ratio * rng.iloc[-21:-1].median()


def setups():
    S = []
    for h in (12, 13, 14):
        S.append(Setup(f"pm_straddle_{h}00_sl25_dte1-6", STR, entry=time(h, 0), leg_sl_pct=25, min_dte=1, max_dte=6))
        S.append(Setup(f"pm_straddle_{h}00_sl25_dte1", STR, entry=time(h, 0), leg_sl_pct=25, min_dte=1, max_dte=1))
    S.append(Setup("straddle_0920_sl25_dte1", STR, entry=time(9, 20), leg_sl_pct=25, min_dte=1, max_dte=1))
    S.append(Setup("straddle_0920_sl15_dte1", STR, entry=time(9, 20), leg_sl_pct=15, min_dte=1, max_dte=1))
    for mx in (0.3, 0.5):
        S.append(Setup(f"straddle_0930_sl25_quietopen{mx}_dte1-6", STR, entry=time(9, 30), leg_sl_pct=25, min_dte=1, max_dte=6, day_filter=quiet_open(mx)))
        S.append(Setup(f"straddle_0930_sl25_quietopen{mx}_dte0", STR, entry=time(9, 30), leg_sl_pct=25, only_expiry_day=True, day_filter=quiet_open(mx)))
    for r in (0.7, 1.0):
        S.append(Setup(f"straddle_0920_sl25_quietprev{r}_dte1-6", STR, entry=time(9, 20), leg_sl_pct=25, min_dte=1, max_dte=6, day_filter=quiet_prev_day(r)))
    S.append(Setup("strangle_0920_1pct_sl30_dte1", [Leg("CE", 1, "SELL", offset_pct=1.0), Leg("PE", -1, "SELL", offset_pct=1.0)], entry=time(9, 20), leg_sl_pct=30, min_dte=1, max_dte=1))
    return S


def _one(a):
    sym, s = a
    t = run(sym, s, "2021-06-01", "2026-08-31")
    t["setup"], t["symbol"] = s.name, sym
    return t


if __name__ == "__main__":
    syms = sys.argv[1:] or ["NIFTY", "SENSEX"]
    with mp.get_context("fork").Pool() as pool:
        parts = pool.map(_one, [(sym, s) for sym in syms for s in setups()])
    all_t = pd.concat([x for x in parts if not x.empty])
    all_t.to_csv(config.RESULTS_DIR / "options_nonexpiry_trades.csv", index=False)
    rows = []
    for (sym, name), t in all_t.groupby(["symbol", "setup"], sort=False):
        m = summary(t)
        m.update(symbol=sym, setup=name)
        m.update({f"y{y}": v for y, v in t.groupby(pd.to_datetime(t.day).dt.year).net.sum().round().items()})
        rows.append(m)
    df = pd.DataFrame(rows)
    cols = ["symbol", "setup", "days", "win_rate", "pf", "net_per_month", "max_dd", "worst_day", "cost_share"] + sorted(c for c in df.columns if c.startswith("y"))
    pd.set_option("display.width", 250)
    print(df[cols].to_string(index=False))
