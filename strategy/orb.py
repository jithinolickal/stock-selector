"""Opening Range Breakout with 'stock in play' filters.

Range = first `range_minutes`. Long on a close above the range high, short on a
close below the range low, before `entry_cutoff`. Stop = opposite side of the
range, target = rr * risk.

Filters (all optional, 0 disables):
  min_rvol          opening-range volume vs the same window's average over the
                    last `rvol_days` days (stock is 'in play' today)
  breakout_vol_mult breakout bar volume vs mean range-bar volume
  min/max_range_pct range size as % of price
"""
from datetime import time

import pandas as pd

from strategy.base import Signal, Strategy


class ORB(Strategy):
    name = "orb"

    def __init__(self, range_minutes=15, rr=1.5, entry_cutoff=time(11, 0), min_range_pct=0.0, max_range_pct=1.5,
                 min_rvol=0.0, rvol_days=14, breakout_vol_mult=0.0, stall_minutes=None, stall_min_r=0.0, bar_minutes=5):
        self.range_bars = range_minutes // bar_minutes
        self.rr = rr
        self.entry_cutoff = entry_cutoff
        self.min_range_pct, self.max_range_pct = min_range_pct, max_range_pct
        self.min_rvol, self.rvol_days = min_rvol, rvol_days
        self.breakout_vol_mult = breakout_vol_mult
        self.stall_minutes, self.stall_min_r = stall_minutes, stall_min_r
        self.last_entry_time = entry_cutoff
        self.avg_or_volume = None

    def on_day_start(self, prior: pd.DataFrame) -> None:
        self.avg_or_volume = None
        if len(prior):
            first = prior.groupby(prior.index.date).head(self.range_bars)
            per_day = first.groupby(first.index.date)["volume"].sum().tail(self.rvol_days)
            self.avg_or_volume = per_day.mean() if len(per_day) >= 5 else None

    def on_bar(self, bars: pd.DataFrame) -> Signal | None:
        if len(bars) <= self.range_bars:
            return None
        last = bars.iloc[-1]
        if last.name.time() >= self.entry_cutoff:
            return None
        rng = bars.iloc[: self.range_bars]
        hi, lo = rng["high"].max(), rng["low"].min()
        range_pct = (hi - lo) / lo * 100
        if not (self.min_range_pct <= range_pct <= self.max_range_pct):
            return None
        rvol = rng["volume"].sum() / self.avg_or_volume if self.avg_or_volume else 0.0
        if self.min_rvol and rvol < self.min_rvol:
            return None
        if self.breakout_vol_mult and last["volume"] < self.breakout_vol_mult * rng["volume"].mean():
            return None
        if last["close"] > hi:
            risk = last["close"] - lo
            return Signal("BUY", stop=lo, target=last["close"] + self.rr * risk, reason="orb_up", priority=rvol)
        if last["close"] < lo:
            risk = hi - last["close"]
            return Signal("SELL", stop=hi, target=last["close"] - self.rr * risk, reason="orb_down", priority=rvol)
        return None
