"""Spike-fade scalp on 1-min data, modelled on the discretionary style:
"when a volatile stock runs up sharply, short near the end of the run, cover on a small pullback"
(mirror: buy the end of a sharp drop).

Run       : price moved >= run_pct over the last run_min minutes
Exhaustion: current bar closes in the lower half of its range (or red) AND the run's peak-bar
            volume >= vol_mult x 20-bar average volume   (climax + stall)
Entry     : next bar open, against the run
Exit      : target tgt_pct / stop stop_pct on bar high-low (stop wins if both in one bar),
            time stop hold_min, square-off 15:15
Costs     : Upstox intraday tariff + slip_bps per fill. Reported gross and net, per trade and per month
            at a fixed notional (NOTIONAL rupees per trade, e.g. 1000 x HDFCLIFE).
"""
import multiprocessing as mp
import sys
from dataclasses import dataclass
from datetime import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from backtest.costs import round_trip

NOTIONAL = 600_000
D1 = config.DATA_DIR / "minutes_1"


@dataclass
class P:
    run_min: int = 10
    run_pct: float = 0.75
    vol_mult: float = 2.0
    tgt_pct: float = 0.2
    stop_pct: float = 0.4
    hold_min: int = 20
    start: time = time(9, 30)
    end: time = time(14, 30)
    slip_bps: float = 2.0
    need_stall: bool = True
    max_per_day: int = 3
    tgt_first: bool = False   # optimistic: when a bar touches both target and stop, count the target

    @property
    def name(self):
        return f"r{self.run_min}m{self.run_pct}_v{self.vol_mult}_t{self.tgt_pct}_s{self.stop_pct}_h{self.hold_min}_{self.start:%H%M}-{self.end:%H%M}{'' if self.need_stall else '_nostall'}{'_opt' if self.tgt_first else ''}"


def day_trades(sym, d, p):
    o, h, l, c, v = (d[k].to_numpy() for k in ("open", "high", "low", "close", "volume"))
    n = len(d)
    if n < 60:
        return []
    times = d.index.time
    vavg = pd.Series(v).rolling(20).mean().to_numpy()
    out, i, done = [], p.run_min + 20, 0
    cost_pct = round_trip(NOTIONAL, NOTIONAL) / NOTIONAL * 100 + 2 * p.slip_bps / 100
    while i < n - 2 and done < p.max_per_day:
        t = times[i]
        if t < p.start or t > p.end:
            i += 1
            continue
        run_up = (c[i] / c[i - p.run_min] - 1) * 100
        side = 0
        if run_up >= p.run_pct:
            side = -1
        elif run_up <= -p.run_pct:
            side = 1
        if side:
            rng = h[i] - l[i]
            stall = (c[i] <= l[i] + 0.5 * rng) if side == -1 else (c[i] >= h[i] - 0.5 * rng)
            climax = v[i - p.run_min:i + 1].max() >= p.vol_mult * vavg[i] if vavg[i] > 0 else False
            if (stall or not p.need_stall) and climax:
                e = o[i + 1]
                tgt = e * (1 - p.tgt_pct / 100) if side == -1 else e * (1 + p.tgt_pct / 100)
                stp = e * (1 + p.stop_pct / 100) if side == -1 else e * (1 - p.stop_pct / 100)
                why, x = "time", None
                last = min(i + 1 + p.hold_min, n - 1)
                for j in range(i + 1, last + 1):
                    if times[j] >= time(15, 15):
                        why, x = "eod", c[j]
                        break
                    hit_stop = h[j] >= stp if side == -1 else l[j] <= stp
                    hit_tgt = l[j] <= tgt if side == -1 else h[j] >= tgt
                    if hit_stop and hit_tgt:
                        why, x = ("tgt", tgt) if p.tgt_first else ("stop", stp)
                        break
                    if hit_stop:
                        why, x = "stop", stp
                        break
                    if hit_tgt:
                        why, x = "tgt", tgt
                        break
                if x is None:
                    x, j = c[last], last
                g = side * (x / e - 1) * 100
                out.append(dict(symbol=sym, day=str(d.index[i].date()), t=str(t)[:5], side="S" if side == -1 else "B", run=round(run_up, 2),
                                gross_pct=round(g, 3), net_pct=round(g - cost_pct, 3), why=why, mins=j - i))
                done += 1
                i = j + 1
                continue
        i += 1
    return out


def _sym(a):
    sym, ps = a
    df = pd.read_parquet(D1 / f"{sym}.parquet")
    df = df[(df.index.time >= time(9, 15)) & (df.index.time <= time(15, 29))]
    rows = []
    for p in ps:
        for _, d in df.groupby(df.index.date):
            for r in day_trades(sym, d, p):
                r["setup"] = p.name
                rows.append(r)
    return pd.DataFrame(rows)


def grid():
    G = []
    for run_min, run_pct in ((5, 0.5), (10, 0.75), (15, 1.0), (30, 1.5)):
        for tgt, stop in ((0.15, 0.3), (0.2, 0.4), (0.3, 0.3), (0.4, 0.6)):
            G.append(P(run_min, run_pct, 2.0, tgt, stop, 20))
    G.append(P(10, 0.75, 2.0, 0.2, 0.4, 20, time(9, 16), time(10, 0)))      # opening-run fades only
    G.append(P(10, 0.75, 2.0, 0.2, 0.4, 20, time(11, 0), time(14, 30)))     # midday only
    G.append(P(10, 0.75, 3.0, 0.2, 0.4, 20))                                # stronger climax
    G.append(P(10, 0.75, 1.0, 0.2, 0.4, 20, need_stall=False))              # no filters: fade any run
    G.append(P(10, 0.75, 2.0, 0.2, 0.4, 60))                                # longer hold
    G.append(P(10, 1.0, 2.0, 0.15, 0.5, 15))                                # tiny target, wide stop (high WR?)
    G.append(P(10, 0.75, 2.0, 0.2, 0.4, 20, tgt_first=True))                # optimistic fill rule bound
    G.append(P(10, 0.75, 2.0, 0.2, 0.4, 20, time(9, 16), time(10, 0), tgt_first=True))
    G.append(P(15, 1.0, 2.0, 0.15, 0.3, 20, time(9, 16), time(10, 0)))      # opening only, tiny target
    return G


def table(t):
    rows = []
    for name, g in t.groupby("setup", sort=False):
        w = g[g.net_pct > 0]
        months = pd.to_datetime(g.day).dt.to_period("M").nunique()
        rows.append(dict(setup=name, trades=len(g), per_day=round(len(g) / g.day.nunique(), 1), wr_gross=round((g.gross_pct > 0).mean() * 100),
                         wr_net=round((g.net_pct > 0).mean() * 100), gross_bps=round(g.gross_pct.mean() * 100, 1), net_bps=round(g.net_pct.mean() * 100, 1),
                         pf_net=round(w.net_pct.sum() / abs(g[g.net_pct <= 0].net_pct.sum()), 2) if (g.net_pct <= 0).any() else 99,
                         rs_month_net=round(g.net_pct.sum() / 100 * NOTIONAL / months), rs_month_gross=round(g.gross_pct.sum() / 100 * NOTIONAL / months),
                         exits=g.why.value_counts(normalize=True).round(2).to_dict()))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    syms = sorted(p.stem for p in D1.glob("*.parquet") if p.stem != "NIFTY50")
    print("symbols:", syms)
    ps = grid()
    with mp.get_context("fork").Pool() as pool:
        parts = pool.map(_sym, [(s, ps) for s in syms])
    t = pd.concat([x for x in parts if not x.empty])
    t.to_csv(config.RESULTS_DIR / "spike_fade_trades.csv", index=False)
    pd.set_option("display.width", 300)
    pd.set_option("display.max_colwidth", 50)
    print(f"\nnotional {NOTIONAL}, cost per round trip {round_trip(NOTIONAL, NOTIONAL):.0f} + slippage\n")
    print(table(t).to_string(index=False))
    base = t[t.setup == P().name]
    print("\nbase setup by symbol:")
    print(base.groupby("symbol").agg(n=("net_pct", "size"), wr=("net_pct", lambda s: round((s > 0).mean() * 100)), gross_bps=("gross_pct", lambda s: round(s.mean() * 100, 1)), net_bps=("net_pct", lambda s: round(s.mean() * 100, 1))).to_string())
    print("\nbase setup by side:")
    print(base.groupby("side").agg(n=("net_pct", "size"), wr=("net_pct", lambda s: round((s > 0).mean() * 100)), gross_bps=("gross_pct", lambda s: round(s.mean() * 100, 1))).to_string())
    print("\nbase setup by year:")
    print(base.groupby(pd.to_datetime(base.day).dt.year).agg(n=("net_pct", "size"), gross_bps=("gross_pct", lambda s: round(s.mean() * 100, 1)), net_bps=("net_pct", lambda s: round(s.mean() * 100, 1))).to_string())
    print("\nbase setup by hour:")
    print(base.groupby(base.t.str[:2]).agg(n=("net_pct", "size"), wr=("net_pct", lambda s: round((s > 0).mean() * 100)), gross_bps=("gross_pct", lambda s: round(s.mean() * 100, 1))).to_string())
