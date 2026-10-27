"""Run every strategy/parameter combo over the universe; rank by out-of-sample results.
In-sample = before SPLIT, out-of-sample = from SPLIT."""
import itertools
import multiprocessing as mp
import sys
from datetime import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from backtest import engine, report
from data import upstox
from strategy.fade import Fade
from strategy.gap import GapGo
from strategy.orb import ORB
from strategy.patterns import RSI2, EmaCross, GapFill, IntradayMomentum, PrevDayBreak, VwapBands
from strategy.practitioner import BBSqueeze, FirstCandle, Ignition, ORBRetest
from strategy.scalp import Scalp
from strategy.za_orb import ZAOrb
from strategy.vwap import VwapPullback

SPLIT = "2025-01-01"


def grid_patterns():
    g = []
    for entry, mm, agree in itertools.product([time(14, 45), time(14, 30)], [0.3, 0.6], [True, False]):
        g.append(("imom", dict(entry=entry, min_move_pct=mm, agree_with_day=agree)))
    for mg, ff in itertools.product([0.7, 1.2], [0.5, 1.0]):
        g.append(("gapfill", dict(min_gap_pct=mg, fill_frac=ff)))
    for rr, nr7 in itertools.product([1.0, 1.5, 2.0], [False, True]):
        g.append(("pdhl", dict(rr=rr, nr7=nr7)))
    for k, ks in itertools.product([1.5, 2.0, 2.5], [1.0, 2.0]):
        g.append(("vwapband", dict(k=k, k_stop=ks)))
    for tp, sl in [(0.4, 0.4), (0.6, 0.4), (0.5, 0.5)]:
        g.append(("rsi2", dict(target_pct=tp, stop_pct=sl)))
    for rr, sb in itertools.product([1.0, 1.5, 2.0], [3, 5]):
        g.append(("ema", dict(rr=rr, swing_bars=sb)))
    return g


def grid_practitioner():
    g = [("orb_retest", {}), ("orb_retest", dict(retest_bars=3)), ("first_candle", {}), ("first_candle", dict(rr=1.0)),
         ("bb_squeeze", {}), ("bb_squeeze", dict(rr=1.5)), ("ignition", {}), ("ignition", dict(min_rvol=1.5, vol_mult=2.0)),
         ("ignition", dict(min_rvol=0.0, vol_mult=3.0))]
    return g


def grid_za():
    g = []
    for mode, rvol in itertools.product(["candle", "atr"], [0.0, 1.5, 2.0]):
        g.append(("za_orb", dict(stop_mode=mode, min_rvol=rvol)))
    g.append(("za_orb", dict(stop_mode="atr", atr_frac=0.2)))
    g.append(("za_orb", dict(stop_mode="atr", atr_frac=0.05)))
    return g


def grid():
    g = []
    for rr, rng, rvol, stall in itertools.product([1.0, 1.5, 2.0], [15, 30], [0.0, 1.5], [None, 60]):
        g.append(("orb", dict(rr=rr, range_minutes=rng, min_rvol=rvol, stall_minutes=stall, stall_min_r=0.3, min_range_pct=0.2)))
    for rr in [1.0, 1.5]:
        g.append(("orb", dict(rr=rr, breakout_vol_mult=1.5, min_range_pct=0.2)))
    for gap, rr in itertools.product([0.75, 1.5], [1.0, 1.5, 2.0]):
        g.append(("gap", dict(min_gap_pct=gap, rr=rr)))
    for rr, sm in itertools.product([1.0, 1.5], [1.0, 2.0]):
        g.append(("vwap", dict(rr=rr, stop_mult=sm)))
    for mv, dist in itertools.product([1.0, 1.5], [0.3, 0.5]):
        g.append(("fade", dict(move_pct=mv, min_dist_pct=dist)))
    for tp, sl in [(0.15, 0.15), (0.2, 0.15), (0.3, 0.3), (0.5, 0.5), (0.3, 0.5)]:
        g.append(("scalp", dict(target_pct=tp, stop_pct=sl)))
        g.append(("scalp+", dict(target_pct=tp, stop_pct=sl)))  # optimistic: target wins ambiguous bars
    return g


CLASSES = {"orb": ORB, "gap": GapGo, "vwap": VwapPullback, "fade": Fade, "scalp": Scalp, "scalp+": Scalp,
           "imom": IntradayMomentum, "gapfill": GapFill, "pdhl": PrevDayBreak, "vwapband": VwapBands, "rsi2": RSI2, "ema": EmaCross,
           "orb_retest": ORBRetest, "first_candle": FirstCandle, "bb_squeeze": BBSqueeze, "ignition": Ignition, "za_orb": ZAOrb}
DATA = {}


def _one(args):
    name, params, symbol = args
    return engine.run({symbol: DATA[symbol]}, CLASSES[name](**params), ambiguous="target" if name.endswith("+") else "stop")


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--set", choices=["base", "patterns", "practitioner", "za"], default="base")
    p.add_argument("--slip", type=float, default=config.SLIPPAGE_BPS)
    p.add_argument("--risk", type=float, default=config.RISK_PER_TRADE_PCT)
    p.add_argument("--out", default="research")
    a = p.parse_args()
    config.SLIPPAGE_BPS, config.RISK_PER_TRADE_PCT = a.slip, a.risk
    combos = {"base": grid, "patterns": grid_patterns, "practitioner": grid_practitioner, "za": grid_za}[a.set]()
    for s in config.NIFTY50:
        try:
            DATA[s] = upstox.load(s)
        except FileNotFoundError:
            pass
    print(f"{len(DATA)} symbols loaded")
    rows = []
    ctx = mp.get_context("fork")
    with ctx.Pool() as pool:
        for i, (name, params) in enumerate(combos, 1):
            parts = pool.map(_one, [(name, params, s) for s in DATA])
            trades = pd.concat([p for p in parts if not p.empty]) if any(not p.empty for p in parts) else pd.DataFrame()
            if not trades.empty:
                trades = engine.select(trades)
            split = pd.Timestamp(SPLIT, tz="Asia/Kolkata")
            ins = report.metrics(trades[trades.entry_time < split]) if not trades.empty else {"trades": 0}
            oos = report.metrics(trades[trades.entry_time >= split]) if not trades.empty else {"trades": 0}
            row = {"strategy": name, "params": str({k: v for k, v in params.items() if v not in (None, 0.0)})}
            row.update({f"is_{k}": v for k, v in ins.items()})
            row.update({f"oos_{k}": v for k, v in oos.items()})
            rows.append(row)
            print(f"[{i}/{len(combos)}] {name} {row['params']}  IS pf={ins.get('pf')} wr={ins.get('win_rate')} n={ins['trades']} | OOS pf={oos.get('pf')} wr={oos.get('win_rate')} n={oos['trades']} %/mo={oos.get('pct_per_month')}", flush=True)
    df = pd.DataFrame(rows)
    config.RESULTS_DIR.mkdir(exist_ok=True)
    df.to_csv(config.RESULTS_DIR / f"{a.out}.csv", index=False)
    cols = ["strategy", "params", "is_trades", "is_win_rate", "is_pf", "is_pct_per_month", "oos_trades", "oos_win_rate", "oos_pf", "oos_pct_per_month", "oos_net_per_share", "oos_max_dd_pct"]
    print("\nTop by out-of-sample profit factor (>=50 OOS trades):")
    print(df[df.oos_trades >= 50].sort_values("oos_pf", ascending=False)[cols].head(15).to_string(index=False))


if __name__ == "__main__":
    main()
