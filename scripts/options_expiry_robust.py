"""Robustness of the expiry-day straddle: stops, entry/exit times, slippage, hedged variants."""
import multiprocessing as mp
import sys
from datetime import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from options.engine import Leg, Setup, run, summary

STR = [Leg("CE", 0, "SELL"), Leg("PE", 0, "SELL")]


def fly(w):
    return [Leg("CE", 0, "SELL"), Leg("CE", 1, "BUY", offset_pct=w), Leg("PE", 0, "SELL"), Leg("PE", -1, "BUY", offset_pct=w)]


def setups():
    S = []
    for sl in (15, 20, 25, 30, 40, None):
        S.append(Setup(f"straddle_0920_sl{sl}", STR, entry=time(9, 20), leg_sl_pct=sl, only_expiry_day=True))
    for h, m in ((9, 30), (9, 45), (10, 0), (10, 30), (11, 0)):
        S.append(Setup(f"straddle_{h:02d}{m:02d}_sl25", STR, entry=time(h, m), leg_sl_pct=25, only_expiry_day=True))
    S.append(Setup("straddle_0920_sl25_exit1500", STR, entry=time(9, 20), exit=time(15, 0), leg_sl_pct=25, only_expiry_day=True))
    S.append(Setup("straddle_0920_sl25_exit1520", STR, entry=time(9, 20), exit=time(15, 20), leg_sl_pct=25, only_expiry_day=True))
    S.append(Setup("straddle_0920_sl25_slip2pct", STR, entry=time(9, 20), leg_sl_pct=25, slippage_pct=2.0, only_expiry_day=True))
    S.append(Setup("straddle_0920_sl25_slip3pct", STR, entry=time(9, 20), leg_sl_pct=25, slippage_pct=3.0, only_expiry_day=True))
    S.append(Setup("straddle_0920_sl25_mtm3000", STR, entry=time(9, 20), leg_sl_pct=25, mtm_stop_rs=3000, only_expiry_day=True))
    for w in (1.0, 1.5, 2.0):
        S.append(Setup(f"ironfly_0920_w{w}_sl25", fly(w), entry=time(9, 20), leg_sl_pct=25, close_hedge_with_short=True, only_expiry_day=True))
        S.append(Setup(f"ironfly_0920_w{w}_sl25_keephedge", fly(w), entry=time(9, 20), leg_sl_pct=25, close_hedge_with_short=False, only_expiry_day=True))
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
    all_t.to_csv(config.RESULTS_DIR / "options_expiry_trades.csv", index=False)
    rows = []
    for (sym, name), t in all_t.groupby(["symbol", "setup"], sort=False):
        m = summary(t)
        m.update(symbol=sym, setup=name)
        m.update({f"y{y}": v for y, v in t.groupby(pd.to_datetime(t.day).dt.year).net.sum().round().items()})
        rows.append(m)
    df = pd.DataFrame(rows)
    cols = ["symbol", "setup", "days", "win_rate", "pf", "net_per_month", "gross_per_month", "max_dd", "worst_day", "cost_share"] + sorted(c for c in df.columns if c.startswith("y"))
    pd.set_option("display.width", 250)
    print(df[cols].to_string(index=False))
    base = all_t[(all_t.setup == "straddle_0920_sl25") & (all_t.symbol == "NIFTY")].sort_values("net")
    print("\nNIFTY straddle_0920_sl25 expiry-day: 8 worst days")
    print(base.head(8)[["day", "spot", "credit", "gross", "cost", "net", "exits", "legs"]].to_string(index=False))
    print("\nexit mix:", base.exits.value_counts().to_dict())
    print("by weekday:", base.groupby(pd.to_datetime(base.day).dt.day_name()).net.agg(["count", "sum", "mean"]).round().to_dict())
