from dataclasses import dataclass
from typing import Literal

import pandas as pd


@dataclass
class Signal:
    side: Literal["BUY", "SELL"]
    stop: float = 0.0
    target: float = 0.0
    reason: str = ""
    # alternative: set stop/target as % of the actual fill price
    stop_pct: float | None = None
    target_pct: float | None = None
    priority: float = 0.0  # when more signals than MAX_TRADES_PER_DAY, engine keeps the highest


class Strategy:
    """on_day_start gets prior days' bars (for averages); on_bar gets today's bars
    so far (oldest first) and returns a Signal or None. Entry fills at next bar open.
    If stall_minutes is set, the engine exits a trade that hasn't reached
    stall_min_r of its risk after that many minutes."""

    name = "base"
    stall_minutes: int | None = None
    stall_min_r: float = 0.0
    last_entry_time = None  # engine stops asking for signals after this time

    def on_day_start(self, prior: pd.DataFrame) -> None:
        pass

    def on_bar(self, bars: pd.DataFrame) -> Signal | None:
        raise NotImplementedError
