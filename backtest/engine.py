"""Bar-by-bar simulator. One symbol-day at a time; at most one trade per symbol-day.

Fills: entry at next bar open, stop/target at their price (stop wins if both
touched in a bar, gap-through fills at open), time-stop at the close of the
first bar >= SQUARE_OFF. Slippage is applied against you on every fill.
"""
from dataclasses import dataclass, asdict
from datetime import date

import pandas as pd

import config
from backtest import costs
from strategy.base import Strategy


@dataclass
class Trade:
    symbol: str
    day: date
    side: str
    entry_time: pd.Timestamp
    exit_time: pd.Timestamp
    qty: int
    entry: float
    exit: float
    stop: float
    target: float
    exit_reason: str
    gross: float
    cost: float
    net: float
    r: float
    reason: str
    priority: float = 0.0


def _slip(price: float, side_buy: bool) -> float:
    s = config.SLIPPAGE_BPS / 10_000
    return price * (1 + s) if side_buy else price * (1 - s)


def _qty(entry: float, stop: float) -> int:
    risk_rs = config.CAPITAL * config.RISK_PER_TRADE_PCT / 100
    by_risk = int(risk_rs / abs(entry - stop)) if entry != stop else 0
    by_margin = int(config.CAPITAL * config.LEVERAGE / config.MAX_OPEN_POSITIONS / entry)
    return max(0, min(by_risk, by_margin))


def run_day(symbol: str, day_bars: pd.DataFrame, strategy: Strategy, ambiguous: str = "stop") -> Trade | None:
    """ambiguous: which fill to assume when a bar touches both stop and target ('stop' = pessimistic)."""
    n = len(day_bars)
    for i in range(n - 1):
        if strategy.last_entry_time and day_bars.index[i].time() >= strategy.last_entry_time:
            return None
        sig = strategy.on_bar(day_bars.iloc[: i + 1])
        if sig is None:
            continue
        long = sig.side == "BUY"
        entry_bar = day_bars.iloc[i + 1]
        entry = _slip(entry_bar["open"], long)
        if sig.stop_pct is not None:
            sig.stop = entry * (1 - sig.stop_pct / 100) if long else entry * (1 + sig.stop_pct / 100)
            sig.target = entry * (1 + sig.target_pct / 100) if long else entry * (1 - sig.target_pct / 100)
        qty = _qty(entry, sig.stop)
        if qty == 0:
            return None
        for j in range(i + 1, n):
            bar = day_bars.iloc[j]
            t = bar.name.time()
            held = (bar.name - entry_bar.name).total_seconds() / 60
            unreal_r = ((bar["close"] - entry) if long else (entry - bar["close"])) / abs(entry - sig.stop)
            hit_stop = bar["low"] <= sig.stop if long else bar["high"] >= sig.stop
            hit_target = bar["high"] >= sig.target if long else bar["low"] <= sig.target
            if t >= config.SQUARE_OFF:
                px, why = bar["close"], "time"
            elif strategy.stall_minutes and held >= strategy.stall_minutes and unreal_r < strategy.stall_min_r:
                px, why = bar["close"], "stall"
            elif hit_stop and (not hit_target or ambiguous == "stop"):
                px = (min if long else max)(bar["open"], sig.stop)
                why = "stop"
            elif hit_target:
                px, why = sig.target, "target"
            elif j == n - 1:
                px, why = bar["close"], "eod"
            else:
                continue
            exit_px = _slip(px, not long)
            gross = (exit_px - entry) * qty if long else (entry - exit_px) * qty
            buy_val, sell_val = (entry * qty, exit_px * qty) if long else (exit_px * qty, entry * qty)
            cost = costs.round_trip(buy_val, sell_val)
            risk_rs = abs(entry - sig.stop) * qty
            return Trade(symbol, bar.name.date(), sig.side, entry_bar.name, bar.name, qty, round(entry, 2), round(exit_px, 2),
                         sig.stop, round(sig.target, 2), why, round(gross, 2), cost, round(gross - cost, 2),
                         round((gross - cost) / risk_rs, 2) if risk_rs else 0.0, sig.reason, sig.priority)
    return None


def run(data: dict[str, pd.DataFrame], strategy: Strategy, start: str | None = None, end: str | None = None,
        ambiguous: str = "stop") -> pd.DataFrame:
    trades = []
    for symbol, df in data.items():
        if start:
            df = df[df.index >= pd.Timestamp(start, tz="Asia/Kolkata")]
        if end:
            df = df[df.index < pd.Timestamp(end, tz="Asia/Kolkata") + pd.Timedelta(days=1)]
        lookback = pd.Timedelta(days=30)
        for day, day_bars in df.groupby(df.index.date):
            day_start = day_bars.index[0]
            strategy.on_day_start(df[(df.index >= day_start - lookback) & (df.index < day_start)])
            t = run_day(symbol, day_bars, strategy, ambiguous)
            if t:
                trades.append(asdict(t))
    if not trades:
        return pd.DataFrame()
    out = pd.DataFrame(trades)
    out = select(out)
    return out.reset_index(drop=True)


def select(trades: pd.DataFrame) -> pd.DataFrame:
    """Cap trades per day: highest priority first, then earliest entry (as a live scanner would pick)."""
    if trades.empty:
        return trades
    out = trades.sort_values(["day", "priority", "entry_time"], ascending=[True, False, True])
    return out.groupby("day", group_keys=False).head(config.MAX_TRADES_PER_DAY).sort_values("entry_time").reset_index(drop=True)
