"""Mean-reversion fade: if the stock has moved >= move_pct from today's open
early in the session, fade it back toward VWAP. Stop beyond the day's extreme."""
from datetime import time

import pandas as pd

from strategy.base import Signal, Strategy
from strategy.vwap import vwap


class Fade(Strategy):
    name = "fade"

    def __init__(self, move_pct=1.0, min_dist_pct=0.3, stop_buffer_pct=0.1, start=time(9, 30), entry_cutoff=time(11, 0),
                 stall_minutes=None, stall_min_r=0.0):
        self.move_pct, self.min_dist_pct, self.stop_buffer_pct = move_pct, min_dist_pct, stop_buffer_pct
        self.start, self.entry_cutoff = start, entry_cutoff
        self.stall_minutes, self.stall_min_r = stall_minutes, stall_min_r
        self.last_entry_time = entry_cutoff

    def on_bar(self, bars: pd.DataFrame) -> Signal | None:
        t = bars.index[-1].time()
        if t < self.start or t >= self.entry_cutoff or len(bars) < 3:
            return None
        o, last, v_last = bars["open"].iloc[0], bars.iloc[-1], vwap(bars).iloc[-1]
        move = (last["close"] - o) / o * 100
        dist = (last["close"] - v_last) / v_last * 100
        if move >= self.move_pct and dist >= self.min_dist_pct:
            return Signal("SELL", stop=bars["high"].max() * (1 + self.stop_buffer_pct / 100), target=v_last, reason="fade_dn")
        if move <= -self.move_pct and dist <= -self.min_dist_pct:
            return Signal("BUY", stop=bars["low"].min() * (1 - self.stop_buffer_pct / 100), target=v_last, reason="fade_up")
        return None
