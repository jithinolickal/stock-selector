"""Gap-and-go: stock gaps >= min_gap_pct vs previous close; trade continuation
when price breaks the first bar's high (gap up) / low (gap down)."""
from datetime import time

import pandas as pd

from strategy.base import Signal, Strategy


class GapGo(Strategy):
    name = "gap"

    def __init__(self, min_gap_pct=1.0, rr=1.5, entry_cutoff=time(10, 30), stall_minutes=None, stall_min_r=0.0):
        self.min_gap_pct, self.rr, self.entry_cutoff = min_gap_pct, rr, entry_cutoff
        self.stall_minutes, self.stall_min_r = stall_minutes, stall_min_r
        self.last_entry_time = entry_cutoff
        self.prev_close = None

    def on_day_start(self, prior: pd.DataFrame) -> None:
        self.prev_close = prior["close"].iloc[-1] if len(prior) else None

    def on_bar(self, bars: pd.DataFrame) -> Signal | None:
        if self.prev_close is None or len(bars) < 2:
            return None
        first, last = bars.iloc[0], bars.iloc[-1]
        if last.name.time() >= self.entry_cutoff:
            return None
        gap = (first["open"] - self.prev_close) / self.prev_close * 100
        if gap >= self.min_gap_pct and last["close"] > first["high"]:
            risk = last["close"] - first["low"]
            return Signal("BUY", stop=first["low"], target=last["close"] + self.rr * risk, reason=f"gap+{gap:.1f}")
        if gap <= -self.min_gap_pct and last["close"] < first["low"]:
            risk = first["high"] - last["close"]
            return Signal("SELL", stop=first["high"], target=last["close"] - self.rr * risk, reason=f"gap{gap:.1f}")
        return None
