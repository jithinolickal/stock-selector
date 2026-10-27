"""Proxy for fixed-paise scalping: enter in the opening-range breakout
direction with a fixed % target and stop. 5-min bars are coarse for this
(stop is assumed to hit first when both are touched), so results are a
conservative bound, not a tick-accurate test."""
from datetime import time

import pandas as pd

from strategy.base import Signal, Strategy


class Scalp(Strategy):
    name = "scalp"

    def __init__(self, target_pct=0.15, stop_pct=0.15, range_minutes=15, entry_cutoff=time(11, 0), bar_minutes=5):
        self.target_pct, self.stop_pct = target_pct, stop_pct
        self.range_bars, self.entry_cutoff = range_minutes // bar_minutes, entry_cutoff
        self.last_entry_time = entry_cutoff

    def on_bar(self, bars: pd.DataFrame) -> Signal | None:
        if len(bars) <= self.range_bars or bars.index[-1].time() >= self.entry_cutoff:
            return None
        rng, c = bars.iloc[: self.range_bars], bars["close"].iloc[-1]
        if c > rng["high"].max():
            return Signal("BUY", stop_pct=self.stop_pct, target_pct=self.target_pct, reason="scalp_up")
        if c < rng["low"].min():
            return Signal("SELL", stop_pct=self.stop_pct, target_pct=self.target_pct, reason="scalp_dn")
        return None
