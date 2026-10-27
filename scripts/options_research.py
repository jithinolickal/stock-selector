"""Grid of intraday option-selling setups on the HF 1-min data, per-year breakdown."""
import argparse
import multiprocessing as mp
import sys
from datetime import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from options.engine import Leg, Setup, run, summary

T = lambda h, m: time(h, m)


def setups():
    S = []
    for sl in (25, 40):
        S.append(Setup(f"straddle_0920_sl{sl}", [Leg("CE", 0, "SELL"), Leg("PE", 0, "SELL")], entry=T(9, 20), leg_sl_pct=sl))
    S.append(Setup("straddle_0920_sl25_expiryday", [Leg("CE", 0, "SELL"), Leg("PE", 0, "SELL")], entry=T(9, 20), leg_sl_pct=25, only_expiry_day=True))
    S.append(Setup("straddle_0920_sl25_dte1plus", [Leg("CE", 0, "SELL"), Leg("PE", 0, "SELL")], entry=T(9, 20), leg_sl_pct=25, min_dte=1))
    for pct in (0.5, 1.0):
        S.append(Setup(f"strangle_0930_{pct}pct_sl40", [Leg("CE", 1, "SELL", offset_pct=pct), Leg("PE", -1, "SELL", offset_pct=pct)], entry=T(9, 30), leg_sl_pct=40))
    for short, wing in ((0.5, 1.0), (0.5, 1.5), (1.0, 2.0)):
        legs = [Leg("CE", 1, "SELL", offset_pct=short), Leg("CE", 1, "BUY", offset_pct=wing), Leg("PE", -1, "SELL", offset_pct=short), Leg("PE", -1, "BUY", offset_pct=wing)]
        S.append(Setup(f"condor_0930_s{short}_w{wing}_sl40", legs, entry=T(9, 30), leg_sl_pct=40))
        S.append(Setup(f"condor_0930_s{short}_w{wing}_nosl", legs, entry=T(9, 30), leg_sl_pct=None))
    S.append(Setup("ironfly_0920_w1.0_sl30", [Leg("CE", 0, "SELL"), Leg("CE", 1, "BUY", offset_pct=1.0), Leg("PE", 0, "SELL"), Leg("PE", -1, "BUY", offset_pct=1.0)], entry=T(9, 20), leg_sl_pct=30))
    S.append(Setup("ironfly_0920_w1.0_nosl", [Leg("CE", 0, "SELL"), Leg("CE", 1, "BUY", offset_pct=1.0), Leg("PE", 0, "SELL"), Leg("PE", -1, "BUY", offset_pct=1.0)], entry=T(9, 20), leg_sl_pct=None))
    return S


def _one(args):
    symbol, s, start, end = args
    t = run(symbol, s, start, end)
    t["setup"] = s.name
    t["symbol"] = symbol
    return t


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--symbols", nargs="*", default=["SENSEX", "NIFTY"])
    p.add_argument("--start", default="2021-06-01")
    p.add_argument("--end", default="2026-08-31")
    a = p.parse_args()
    jobs = [(sym, s, a.start, a.end) for sym in a.symbols for s in setups()]
    with mp.get_context("fork").Pool() as pool:
        parts = pool.map(_one, jobs)
    all_t = pd.concat([x for x in parts if not x.empty])
    config.RESULTS_DIR.mkdir(exist_ok=True)
    all_t.to_csv(config.RESULTS_DIR / "options_trades.csv", index=False)
    rows = []
    for (sym, name), t in all_t.groupby(["symbol", "setup"]):
        m = summary(t)
        m.update(symbol=sym, setup=name)
        yrs = t.groupby(pd.to_datetime(t.day).dt.year).net.sum().round()
        m.update({f"y{y}": v for y, v in yrs.items()})
        rows.append(m)
    df = pd.DataFrame(rows)
    cols = ["symbol", "setup", "days", "win_rate", "pf", "avg_win", "avg_loss", "net_per_month", "gross_per_month", "max_dd", "worst_day", "cost_share"] + sorted(c for c in df.columns if c.startswith("y"))
    df = df[cols].sort_values(["symbol", "pf"], ascending=[True, False])
    df.to_csv(config.RESULTS_DIR / "options_research.csv", index=False)
    pd.set_option("display.width", 250)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
