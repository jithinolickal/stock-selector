"""Short, rule-based intraday setups from the literature / practitioner lore.
Each is ~20 lines so it can be read and judged in one go."""
from datetime import time

import numpy as np
import pandas as pd

from strategy.base import Signal, Strategy
from strategy.vwap import vwap


def _at(bars: pd.DataFrame, t: time) -> bool:
    return bars.index[-1].time() == t


class IntradayMomentum(Strategy):
    """Gao-Han-Li-Zhou: first-30-min return predicts last-30-min return.
    At `entry` go with the sign of the first `signal_minutes` return (optionally
    requiring the day-so-far return to agree); hold to square-off."""
    name = "imom"

    def __init__(self, entry=time(14, 45), signal_minutes=30, min_move_pct=0.3, agree_with_day=True, stop_pct=1.0):
        self.entry, self.signal_bars, self.min_move_pct = entry, signal_minutes // 5, min_move_pct
        self.agree_with_day, self.stop_pct = agree_with_day, stop_pct
        self.last_entry_time = time(entry.hour, entry.minute + 1)

    def on_bar(self, bars):
        if not _at(bars, self.entry) or len(bars) <= self.signal_bars:
            return None
        o = bars["open"].iloc[0]
        r_first = (bars["close"].iloc[self.signal_bars - 1] - o) / o * 100
        r_day = (bars["close"].iloc[-1] - o) / o * 100
        if abs(r_first) < self.min_move_pct or (self.agree_with_day and np.sign(r_first) != np.sign(r_day)):
            return None
        side = "BUY" if r_first > 0 else "SELL"
        return Signal(side, stop_pct=self.stop_pct, target_pct=10.0, reason=f"imom{r_first:+.1f}")


class GapFill(Strategy):
    """Fade an opening gap of min..max % back toward the previous close.
    Enter after the first bar; target = prev close + (1-fill_frac)*gap; stop beyond first-bar extreme."""
    name = "gapfill"

    def __init__(self, min_gap_pct=0.7, max_gap_pct=3.0, fill_frac=0.5, stop_buffer_pct=0.2):
        self.min_gap_pct, self.max_gap_pct, self.fill_frac, self.stop_buffer_pct = min_gap_pct, max_gap_pct, fill_frac, stop_buffer_pct
        self.last_entry_time = time(9, 30)
        self.prev_close = None

    def on_day_start(self, prior):
        self.prev_close = prior["close"].iloc[-1] if len(prior) else None

    def on_bar(self, bars):
        if self.prev_close is None or len(bars) != 1:
            return None
        first = bars.iloc[0]
        gap = (first["open"] - self.prev_close) / self.prev_close * 100
        if not (self.min_gap_pct <= abs(gap) <= self.max_gap_pct):
            return None
        target = first["close"] - self.fill_frac * (first["close"] - self.prev_close)
        if gap > 0:
            return Signal("SELL", stop=first["high"] * (1 + self.stop_buffer_pct / 100), target=target, reason=f"gapfill{gap:+.1f}")
        return Signal("BUY", stop=first["low"] * (1 - self.stop_buffer_pct / 100), target=target, reason=f"gapfill{gap:+.1f}")


class PrevDayBreak(Strategy):
    """Close above previous-day high (below low) after `start`; stop = lowest low of last `swing_bars`;
    target = rr * risk. nr7=True only trades when yesterday was the narrowest of the last 7 days."""
    name = "pdhl"

    def __init__(self, rr=1.5, swing_bars=3, start=time(9, 30), entry_cutoff=time(13, 0), nr7=False, stall_minutes=None, stall_min_r=0.0):
        self.rr, self.swing_bars, self.start, self.entry_cutoff, self.nr7 = rr, swing_bars, start, entry_cutoff, nr7
        self.stall_minutes, self.stall_min_r = stall_minutes, stall_min_r
        self.last_entry_time = entry_cutoff
        self.pdh = self.pdl = None

    def on_day_start(self, prior):
        self.pdh = self.pdl = None
        if not len(prior):
            return
        days = prior.groupby(prior.index.date).agg(high=("high", "max"), low=("low", "min"))
        if self.nr7 and (len(days) < 7 or (days.high - days.low).iloc[-1] != (days.high - days.low).tail(7).min()):
            return
        self.pdh, self.pdl = days.high.iloc[-1], days.low.iloc[-1]

    def on_bar(self, bars):
        t = bars.index[-1].time()
        if self.pdh is None or t < self.start or t >= self.entry_cutoff or len(bars) < self.swing_bars + 1:
            return None
        c, prev_c = bars["close"].iloc[-1], bars["close"].iloc[-2]
        if c > self.pdh >= prev_c:
            stop = bars["low"].iloc[-self.swing_bars:].min()
            return Signal("BUY", stop=stop, target=c + self.rr * (c - stop), reason="pdh")
        if c < self.pdl <= prev_c:
            stop = bars["high"].iloc[-self.swing_bars:].max()
            return Signal("SELL", stop=stop, target=c - self.rr * (stop - c), reason="pdl")
        return None


class VwapBands(Strategy):
    """Mean reversion to VWAP: close beyond vwap -/+ k*sigma (sigma = running std of typical price - vwap)
    and the bar closes back in the direction of VWAP. Target VWAP, stop k_stop*sigma beyond entry."""
    name = "vwapband"

    def __init__(self, k=2.0, k_stop=1.0, start=time(10, 0), entry_cutoff=time(14, 30), stall_minutes=None, stall_min_r=0.0):
        self.k, self.k_stop, self.start, self.entry_cutoff = k, k_stop, start, entry_cutoff
        self.stall_minutes, self.stall_min_r = stall_minutes, stall_min_r
        self.last_entry_time = entry_cutoff

    def on_bar(self, bars):
        t = bars.index[-1].time()
        if t < self.start or t >= self.entry_cutoff or len(bars) < 6:
            return None
        v = vwap(bars)
        sigma = ((bars["high"] + bars["low"] + bars["close"]) / 3 - v).std()
        if not sigma or np.isnan(sigma):
            return None
        last, v_last = bars.iloc[-1], v.iloc[-1]
        if last["close"] < v_last - self.k * sigma and last["close"] > last["open"]:
            return Signal("BUY", stop=last["close"] - self.k_stop * sigma, target=v_last, reason="vwap-band")
        if last["close"] > v_last + self.k * sigma and last["close"] < last["open"]:
            return Signal("SELL", stop=last["close"] + self.k_stop * sigma, target=v_last, reason="vwap+band")
        return None


class RSI2(Strategy):
    """Connors-style: RSI(2) on 5-min < low with price above VWAP -> BUY (mirror for SELL).
    Fixed % stop/target, short hold."""
    name = "rsi2"

    def __init__(self, low=10, high=90, target_pct=0.5, stop_pct=0.5, start=time(9, 45), entry_cutoff=time(14, 30), stall_minutes=30, stall_min_r=0.0):
        self.low, self.high, self.target_pct, self.stop_pct = low, high, target_pct, stop_pct
        self.start, self.entry_cutoff = start, entry_cutoff
        self.stall_minutes, self.stall_min_r = stall_minutes, stall_min_r
        self.last_entry_time = entry_cutoff

    def on_bar(self, bars):
        t = bars.index[-1].time()
        if t < self.start or t >= self.entry_cutoff or len(bars) < 5:
            return None
        d = bars["close"].diff().iloc[-2:]
        up, dn = d.clip(lower=0).mean(), (-d.clip(upper=0)).mean()
        rsi = 100 if dn == 0 else 100 - 100 / (1 + up / dn)
        c, v = bars["close"].iloc[-1], vwap(bars).iloc[-1]
        if rsi < self.low and c > v:
            return Signal("BUY", stop_pct=self.stop_pct, target_pct=self.target_pct, reason=f"rsi2={rsi:.0f}")
        if rsi > self.high and c < v:
            return Signal("SELL", stop_pct=self.stop_pct, target_pct=self.target_pct, reason=f"rsi2={rsi:.0f}")
        return None


class EmaCross(Strategy):
    """9/20 EMA cross on 5-min after `start`; stop = swing low/high of last `swing_bars`; target rr."""
    name = "ema"

    def __init__(self, fast=9, slow=20, rr=1.5, swing_bars=5, start=time(9, 45), entry_cutoff=time(14, 0), stall_minutes=None, stall_min_r=0.0):
        self.fast, self.slow, self.rr, self.swing_bars = fast, slow, rr, swing_bars
        self.start, self.entry_cutoff = start, entry_cutoff
        self.stall_minutes, self.stall_min_r = stall_minutes, stall_min_r
        self.last_entry_time = entry_cutoff

    def on_bar(self, bars):
        t = bars.index[-1].time()
        if t < self.start or t >= self.entry_cutoff or len(bars) < self.slow + 2:
            return None
        f = bars["close"].ewm(span=self.fast, adjust=False).mean()
        s = bars["close"].ewm(span=self.slow, adjust=False).mean()
        c = bars["close"].iloc[-1]
        if f.iloc[-2] <= s.iloc[-2] and f.iloc[-1] > s.iloc[-1]:
            stop = bars["low"].iloc[-self.swing_bars:].min()
            return Signal("BUY", stop=stop, target=c + self.rr * (c - stop), reason="ema_x_up") if stop < c else None
        if f.iloc[-2] >= s.iloc[-2] and f.iloc[-1] < s.iloc[-1]:
            stop = bars["high"].iloc[-self.swing_bars:].max()
            return Signal("SELL", stop=stop, target=c - self.rr * (stop - c), reason="ema_x_dn") if stop > c else None
        return None
