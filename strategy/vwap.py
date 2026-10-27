"""VWAP pullback in an established intraday trend. After `start`, if the last
`trend_bars` closes were on one side of VWAP and this bar touches VWAP and
closes back on the trend side, enter with the trend. Stop = VWAP -/+ stop_mult
* average 5-min bar range (from prior days)."""
from datetime import time

import pandas as pd

from strategy.base import Signal, Strategy


def vwap(bars: pd.DataFrame) -> pd.Series:
    tp = (bars["high"] + bars["low"] + bars["close"]) / 3
    return (tp * bars["volume"]).cumsum() / bars["volume"].cumsum().replace(0, 1)


class VwapPullback(Strategy):
    name = "vwap"

    def __init__(self, rr=1.5, stop_mult=1.0, trend_bars=6, start=time(10, 0), entry_cutoff=time(14, 0),
                 stall_minutes=None, stall_min_r=0.0):
        self.rr, self.stop_mult, self.trend_bars = rr, stop_mult, trend_bars
        self.start, self.entry_cutoff = start, entry_cutoff
        self.stall_minutes, self.stall_min_r = stall_minutes, stall_min_r
        self.last_entry_time = entry_cutoff
        self.bar_range = None

    def on_day_start(self, prior: pd.DataFrame) -> None:
        tail = prior.tail(75 * 5)
        self.bar_range = (tail["high"] - tail["low"]).mean() if len(tail) else None

    def on_bar(self, bars: pd.DataFrame) -> Signal | None:
        t = bars.index[-1].time()
        if self.bar_range is None or t < self.start or t >= self.entry_cutoff or len(bars) < self.trend_bars + 2:
            return None
        v = vwap(bars)
        last, v_last = bars.iloc[-1], v.iloc[-1]
        prev_close, prev_v = bars["close"].iloc[-self.trend_bars - 1:-1], v.iloc[-self.trend_bars - 1:-1]
        if (prev_close > prev_v).all() and last["low"] <= v_last and last["close"] > v_last:
            stop = v_last - self.stop_mult * self.bar_range
            return Signal("BUY", stop=stop, target=last["close"] + self.rr * (last["close"] - stop), reason="vwap_pb_up")
        if (prev_close < prev_v).all() and last["high"] >= v_last and last["close"] < v_last:
            stop = v_last + self.stop_mult * self.bar_range
            return Signal("SELL", stop=stop, target=last["close"] - self.rr * (stop - last["close"]), reason="vwap_pb_dn")
        return None
