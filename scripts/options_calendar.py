"""Expiry-day straddle on each index + combined expiry calendar P&L."""
import multiprocessing as mp
import sys
from datetime import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from options.engine import Leg, Setup, run, summary

STR = [Leg("CE", 0, "SELL"), Leg("PE", 0, "SELL")]


def _one(a):
    sym, sl = a
    t = run(sym, Setup(f"straddle_0920_sl{sl}_dte0", STR, entry=time(9, 20), leg_sl_pct=sl, only_expiry_day=True), "2021-06-01", "2026-08-31")
    t["symbol"], t["sl"] = sym, sl
    return t


if __name__ == "__main__":
    with mp.get_context("fork").Pool() as pool:
        parts = pool.map(_one, [(s, sl) for s in ("NIFTY", "SENSEX", "BANKNIFTY") for sl in (25, 30, 40)])
    t = pd.concat(parts)
    t.to_csv(config.RESULTS_DIR / "options_calendar_trades.csv", index=False)
    for (sym, sl), b in t.groupby(["symbol", "sl"]):
        m = summary(b)
        yrs = b.groupby(pd.to_datetime(b.day).dt.year).net.sum().round().to_dict()
        print(f"{sym:<9} sl{sl}: n={m['days']} wr={m['win_rate']} pf={m['pf']} net/mo={m['net_per_month']} dd={m['max_dd']} worst={m['worst_day']} | {yrs}")
    print()
    b = t[t.sl == 25].copy()
    b["dow"] = pd.to_datetime(b.day).dt.day_name().str[:3]
    print("expiry weekday by symbol & year (trade counts):")
    print(b.groupby([pd.to_datetime(b.day).dt.year, "symbol", "dow"]).size().unstack(fill_value=0).to_string())
    print("\nCombined calendar (all three, sl25), per month:")
    m = b.groupby(pd.to_datetime(b.day).dt.to_period("M")).agg(trades=("net", "size"), net=("net", "sum"))
    print(f"months={len(m)} avg trades/month={m.trades.mean():.1f} avg net/month={m.net.mean():.0f} positive months={(m.net > 0).mean() * 100:.0f}% worst={m.net.min():.0f} best={m.net.max():.0f}")
    cur = b[b.day >= "2025-09-01"]
    mc = cur.groupby(pd.to_datetime(cur.day).dt.to_period("M")).agg(trades=("net", "size"), net=("net", "sum"))
    print(f"current regime (since 2025-09): months={len(mc)} trades/month={mc.trades.mean():.1f} net/month={mc.net.mean():.0f} positive={(mc.net > 0).mean() * 100:.0f}% | by symbol: {cur.groupby('symbol').net.agg(['size', 'sum']).round().to_dict()}")
    daily = b.groupby("day").net.sum()
    eq = daily.cumsum()
    print(f"combined max drawdown={(eq - eq.cummax()).min():.0f}, worst single day (all indices)={daily.min():.0f}")
