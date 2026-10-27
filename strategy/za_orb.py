"""Zarattini-Aziz ORB (2023/2024): direction = sign of the 09:15 5-min candle; enter at the
2nd candle open; stop = first-candle extreme ('candle') or 0.1 x daily ATR14 ('atr'); no target
(10R), exit at square-off. 1% risk sizing. Optional opening-RVOL filter (stocks in play)."""
from datetime import time

import numpy as np
import pandas as pd

from strategy.base import Signal, Strategy


class ZAOrb(Strategy):
    name = "za_orb"

    def __init__(self, stop_mode="candle", atr_frac=0.1, min_rvol=0.0, rvol_days=14):
        self.stop_mode, self.atr_frac, self.min_rvol, self.rvol_days = stop_mode, atr_frac, min_rvol, rvol_days
        self.last_entry_time = time(9, 25)
        self.atr = self.avg_or_vol = None

    def on_day_start(self, prior):
        self.atr = self.avg_or_vol = None
        if not len(prior):
            return
        d = prior.groupby(prior.index.date).agg(h=("high", "max"), l=("low", "min"), c=("close", "last"), v=("volume", "sum"))
        tr = pd.concat([d.h - d.l, (d.h - d.c.shift()).abs(), (d.l - d.c.shift()).abs()], axis=1).max(axis=1)
        self.atr = tr.tail(14).mean() if len(tr) >= 14 else None
        first = prior.groupby(prior.index.date).head(1)["volume"]
        self.avg_or_vol = first.tail(self.rvol_days).mean() if len(first) >= 5 else None

    def on_bar(self, bars):
        if len(bars) != 1 or self.atr is None:
            return None
        f = bars.iloc[0]
        if f["close"] == f["open"]:
            return None
        rvol = f["volume"] / self.avg_or_vol if self.avg_or_vol else 0.0
        if self.min_rvol and rvol < self.min_rvol:
            return None
        long = f["close"] > f["open"]
        c = f["close"]
        if self.stop_mode == "candle":
            stop = f["low"] if long else f["high"]
        else:
            stop = c - self.atr_frac * self.atr if long else c + self.atr_frac * self.atr
        if stop == c:
            return None
        risk = abs(c - stop)
        return Signal("BUY" if long else "SELL", stop=stop, target=c + 10 * risk if long else c - 10 * risk, reason="za_orb", priority=rvol)
