"""Setups S6/S7/S10/S11 from research_notes/.../practitioner_scalping_setups.md, coded verbatim."""
from datetime import time

import numpy as np
import pandas as pd

from strategy.base import Signal, Strategy


def _cap_stop(entry, stop, cap_pct):
    """Return None if stop is further than cap_pct from entry."""
    return None if abs(entry - stop) / entry * 100 > cap_pct else stop


class ORBRetest(Strategy):
    """S6: 15-min OR (0.3-1.5%); after the first close above OR_high, wait for a bar whose low
    touches OR_high (+0.05%) and closes above it within `retest_bars`; stop = OR mid (cap 0.8%), target = 1x OR range."""
    name = "orb_retest"

    def __init__(self, retest_bars=6, stop_cap_pct=0.8, min_range_pct=0.3, max_range_pct=1.5, entry_cutoff=time(11, 0)):
        self.retest_bars, self.stop_cap_pct = retest_bars, stop_cap_pct
        self.min_range_pct, self.max_range_pct, self.entry_cutoff = min_range_pct, max_range_pct, entry_cutoff
        self.last_entry_time = entry_cutoff

    def on_bar(self, bars):
        if len(bars) < 5 or bars.index[-1].time() >= self.entry_cutoff:
            return None
        rng = bars.iloc[:3]
        hi, lo = rng["high"].max(), rng["low"].min()
        o = bars["open"].iloc[0]
        if not (self.min_range_pct <= (hi - lo) / o * 100 <= self.max_range_pct):
            return None
        after = bars.iloc[3:]
        mid, width = lo + 0.5 * (hi - lo), hi - lo
        for side, lvl, touch, ok in (("BUY", hi, lambda b: b["low"] <= hi * 1.0005 and b["close"] > hi, lambda b: b["close"] > hi),
                                     ("SELL", lo, lambda b: b["high"] >= lo * 0.9995 and b["close"] < lo, lambda b: b["close"] < lo)):
            brk = np.argmax(after.apply(ok, axis=1).values) if after.apply(ok, axis=1).any() else None
            if brk is None:
                continue
            window = after.iloc[brk + 1: brk + 1 + self.retest_bars]
            last = bars.iloc[-1]
            if len(window) and last.name in window.index and touch(last):
                stop = _cap_stop(last["close"], mid, self.stop_cap_pct)
                if stop is None:
                    return None
                tgt = lvl + width if side == "BUY" else lvl - width
                return Signal(side, stop=stop, target=tgt, reason="orb_retest")
        return None


class FirstCandle(Strategy):
    """S7: 09:15 bar with body >= 40% of range and range 0.25-1.2%; first close beyond its high/low by 09:45;
    stop = opposite extreme (cap 0.7%); target = 1.5x stop (min 0.4%)."""
    name = "first_candle"

    def __init__(self, rr=1.5, stop_cap_pct=0.7, min_target_pct=0.4, entry_cutoff=time(9, 50)):
        self.rr, self.stop_cap_pct, self.min_target_pct, self.entry_cutoff = rr, stop_cap_pct, min_target_pct, entry_cutoff
        self.last_entry_time = entry_cutoff

    def on_bar(self, bars):
        if len(bars) < 2 or bars.index[-1].time() >= self.entry_cutoff:
            return None
        f, c = bars.iloc[0], bars["close"].iloc[-1]
        rng = f["high"] - f["low"]
        if rng == 0 or abs(f["close"] - f["open"]) / rng < 0.4 or not (0.25 <= rng / f["open"] * 100 <= 1.2):
            return None
        if c > f["high"]:
            stop = _cap_stop(c, f["low"], self.stop_cap_pct)
            return Signal("BUY", stop=stop, target=c + max(self.rr * (c - stop), c * self.min_target_pct / 100), reason="fc_up") if stop else None
        if c < f["low"]:
            stop = _cap_stop(c, f["high"], self.stop_cap_pct)
            return Signal("SELL", stop=stop, target=c - max(self.rr * (stop - c), c * self.min_target_pct / 100), reason="fc_dn") if stop else None
        return None


class BBSqueeze(Strategy):
    """S10: BB(20,2) on 5-min; squeeze = bandwidth <= 10th pct of trailing 500 bars for >= 6 bars;
    entry = first close outside bands with volume > 2x 20-bar avg, 10:00-14:00; stop = SMA20 (cap 0.6%); target 2x stop."""
    name = "bb_squeeze"

    def __init__(self, rr=2.0, stop_cap_pct=0.6, min_target_pct=0.4, squeeze_bars=6, start=time(10, 0), entry_cutoff=time(14, 0)):
        self.rr, self.stop_cap_pct, self.min_target_pct, self.squeeze_bars = rr, stop_cap_pct, min_target_pct, squeeze_bars
        self.start, self.entry_cutoff = start, entry_cutoff
        self.last_entry_time = entry_cutoff
        self.prior = None

    def on_day_start(self, prior):
        self.prior = prior.tail(500)

    def on_bar(self, bars):
        t = bars.index[-1].time()
        if self.prior is None or t < self.start or t >= self.entry_cutoff:
            return None
        full = pd.concat([self.prior, bars]).tail(500 + self.squeeze_bars + 1)
        c = full["close"]
        mid, sd = c.rolling(20).mean(), c.rolling(20).std()
        bw = (4 * sd / mid).dropna()
        if len(bw) < 100:
            return None
        thresh = bw.iloc[:-self.squeeze_bars].quantile(0.10)
        if not (bw.iloc[-self.squeeze_bars - 1:-1] <= thresh).all():
            return None
        last, m, s = full.iloc[-1], mid.iloc[-1], sd.iloc[-1]
        if last["volume"] < 2 * full["volume"].iloc[-21:-1].mean():
            return None
        stop = _cap_stop(last["close"], m, self.stop_cap_pct)
        if stop is None:
            return None
        if last["close"] > m + 2 * s:
            return Signal("BUY", stop=stop, target=last["close"] + max(self.rr * (last["close"] - stop), last["close"] * self.min_target_pct / 100), reason="bb_up")
        if last["close"] < m - 2 * s:
            return Signal("SELL", stop=stop, target=last["close"] - max(self.rr * (stop - last["close"]), last["close"] * self.min_target_pct / 100), reason="bb_dn")
        return None


class Ignition(Strategy):
    """S11: only on days with opening RVOL >= min_rvol (first 15 min vs median of prior 20 sessions).
    Ignition bar 09:30-14:00: range >= 2x ATR(20), volume >= 3x 20-bar avg, close in top/bottom 25% of range.
    Entry next bar open; stop = bar midpoint (cap 0.7%); target 1.5x stop (min 0.4%)."""
    name = "ignition"

    def __init__(self, min_rvol=2.0, range_mult=2.0, vol_mult=3.0, rr=1.5, stop_cap_pct=0.7, min_target_pct=0.4,
                 start=time(9, 30), entry_cutoff=time(14, 0)):
        self.min_rvol, self.range_mult, self.vol_mult, self.rr = min_rvol, range_mult, vol_mult, rr
        self.stop_cap_pct, self.min_target_pct, self.start, self.entry_cutoff = stop_cap_pct, min_target_pct, start, entry_cutoff
        self.last_entry_time = entry_cutoff
        self.med_or_vol = None

    def on_day_start(self, prior):
        self.med_or_vol = None
        if len(prior):
            first = prior.groupby(prior.index.date).head(3)
            per_day = first.groupby(first.index.date)["volume"].sum().tail(20)
            self.med_or_vol = per_day.median() if len(per_day) >= 10 else None

    def on_bar(self, bars):
        t = bars.index[-1].time()
        if self.med_or_vol is None or t < self.start or t >= self.entry_cutoff or len(bars) < 22:
            return None
        if bars["volume"].iloc[:3].sum() / self.med_or_vol < self.min_rvol:
            return None
        last, prev = bars.iloc[-1], bars.iloc[-21:-1]
        rng = last["high"] - last["low"]
        if rng < self.range_mult * (prev["high"] - prev["low"]).mean() or last["volume"] < self.vol_mult * prev["volume"].mean():
            return None
        pos = (last["close"] - last["low"]) / rng
        mid = last["low"] + 0.5 * rng
        c = last["close"]
        stop = _cap_stop(c, mid, self.stop_cap_pct)
        if stop is None:
            return None
        if pos >= 0.75:
            return Signal("BUY", stop=stop, target=c + max(self.rr * (c - stop), c * self.min_target_pct / 100), reason="ignite_up")
        if pos <= 0.25:
            return Signal("SELL", stop=stop, target=c - max(self.rr * (stop - c), c * self.min_target_pct / 100), reason="ignite_dn")
        return None
