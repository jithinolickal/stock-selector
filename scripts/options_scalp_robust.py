"""Robustness of the two scalp survivors: Nifty 0DTE 9:20 straddle held ~1h, Sensex 0DTE noon straddle."""
import multiprocessing as mp
import sys
from datetime import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from options.engine import Leg, Setup, run, summary
from scripts.options_scalp import plus

STR = [Leg("CE", 0, "SELL"), Leg("PE", 0, "SELL")]


def setups():
    S = []
    for hold in (45, 60, 90, 120):
        for sl in (20, 25, 30):
            S.append(("NIFTY", Setup(f"N_0920_{hold}m_sl{sl}", STR, entry=time(9, 20), exit=plus(time(9, 20), hold), leg_sl_pct=sl, slippage_pct=0.5, min_dte=0, max_dte=0)))
    S.append(("NIFTY", Setup("N_0920_60m_sl25_slip1", STR, entry=time(9, 20), exit=time(10, 20), leg_sl_pct=25, slippage_pct=1.0, min_dte=0, max_dte=0)))
    S.append(("NIFTY", Setup("N_0920_60m_sl25_slip2", STR, entry=time(9, 20), exit=time(10, 20), leg_sl_pct=25, slippage_pct=2.0, min_dte=0, max_dte=0)))
    for h, m in ((11, 30), (12, 0), (12, 30), (13, 0)):
        for sl in (30, 40, 50):
            S.append(("SENSEX", Setup(f"S_{h:02d}{m:02d}_sl{sl}", STR, entry=time(h, m), leg_sl_pct=sl, slippage_pct=1.0, min_dte=0, max_dte=0)))
    S.append(("SENSEX", Setup("S_1200_sl40_mtm3000", STR, entry=time(12, 0), leg_sl_pct=40, mtm_stop_rs=3000, slippage_pct=1.0, min_dte=0, max_dte=0)))
    S.append(("SENSEX", Setup("S_1200_sl40_slip2", STR, entry=time(12, 0), leg_sl_pct=40, slippage_pct=2.0, min_dte=0, max_dte=0)))
    S.append(("NIFTY", Setup("N_1200_sl40", STR, entry=time(12, 0), leg_sl_pct=40, slippage_pct=0.5, min_dte=0, max_dte=0)))
    return S


def _one(a):
    sym, s = a
    t = run(sym, s, "2021-06-01", "2026-08-31")
    t["setup"], t["symbol"] = s.name, sym
    return t


if __name__ == "__main__":
    with mp.get_context("fork").Pool() as pool:
        parts = pool.map(_one, setups())
    all_t = pd.concat([x for x in parts if not x.empty])
    all_t.to_csv(config.RESULTS_DIR / "options_scalp_robust.csv", index=False)
    rows = []
    for (sym, name), t in all_t.groupby(["symbol", "setup"], sort=False):
        m = summary(t)
        m.update(setup=name)
        m.update({f"y{y}": v for y, v in t.groupby(pd.to_datetime(t.day).dt.year).net.sum().round().items()})
        rows.append(m)
    df = pd.DataFrame(rows)
    pd.set_option("display.width", 250)
    print(df[["setup", "days", "win_rate", "pf", "net_per_month", "max_dd", "worst_day"] + sorted(c for c in df.columns if c.startswith("y"))].to_string(index=False))
    # Nifty: first-hour + noon re-entry combined
    a = all_t[all_t.setup == "N_0920_60m_sl25"].set_index("day").net
    b = all_t[all_t.setup == "N_1200_sl40"].set_index("day").net
    c = (a.add(b, fill_value=0)).reset_index().rename(columns={0: "net"})
    c["gross"] = c["cost"] = 0
    print("\nNIFTY 9:20-60m + 12:00 combined:", summary(c))
