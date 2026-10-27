from datetime import date

import pandas as pd
import pytest

import config
from backtest import costs, engine
from strategy.base import Signal, Strategy
from strategy.orb import ORB


def bars(rows, day="2024-01-02"):
    idx = pd.date_range(f"{day} 09:15", periods=len(rows), freq="5min", tz="Asia/Kolkata")
    return pd.DataFrame(rows, columns=["open", "high", "low", "close", "volume", "oi"], index=idx)


class Always(Strategy):
    def __init__(self, side, stop, target):
        self.sig = Signal(side, stop, target)

    def on_bar(self, b):
        return self.sig if len(b) == 1 else None


def test_costs_round_trip_is_about_83_on_1_lakh():
    assert 80 < costs.round_trip(100_000, 100_000) < 86


def test_long_hits_target():
    b = bars([[100, 101, 99, 100, 1, 0], [100, 101, 99, 100, 1, 0], [100, 106, 99, 105, 1, 0]])
    t = engine.run_day("X", b, Always("BUY", stop=98, target=104))
    assert t.exit_reason == "target" and t.gross > 0 and t.net < t.gross


def test_long_stop_beats_target_in_same_bar():
    b = bars([[100, 101, 99, 100, 1, 0], [100, 101, 99, 100, 1, 0], [100, 110, 90, 100, 1, 0]])
    t = engine.run_day("X", b, Always("BUY", stop=98, target=104))
    assert t.exit_reason == "stop" and t.net < 0


def test_short_gap_through_stop_fills_at_open():
    b = bars([[100, 101, 99, 100, 1, 0], [100, 101, 99, 100, 1, 0], [105, 106, 104, 105, 1, 0]])
    t = engine.run_day("X", b, Always("SELL", stop=102, target=95))
    assert t.exit_reason == "stop" and t.exit > 102


def test_time_stop_at_square_off():
    idx = pd.date_range("2024-01-02 09:15", "2024-01-02 15:25", freq="5min", tz="Asia/Kolkata")
    b = pd.DataFrame([[100, 100.5, 99.5, 100, 1, 0]] * len(idx), columns=["open", "high", "low", "close", "volume", "oi"], index=idx)
    t = engine.run_day("X", b, Always("BUY", stop=90, target=110))
    assert t.exit_reason == "time" and t.exit_time.time() == config.SQUARE_OFF


def test_orb_long_signal_after_range():
    b = bars([[100, 100.5, 99.5, 100, 1, 0]] * 3 + [[100, 101.2, 100, 101, 1, 0]])
    s = ORB(range_minutes=15, rr=2).on_bar(b)
    assert s and s.side == "BUY" and s.stop == 99.5 and s.target == pytest.approx(101 + 2 * 1.5)


def test_orb_no_signal_inside_range():
    b = bars([[100, 101, 99, 100, 1, 0]] * 5)
    assert ORB().on_bar(b) is None


def test_run_caps_trades_per_day():
    b = bars([[100, 101, 99, 100, 1, 0], [100, 101, 99, 100, 1, 0], [100, 106, 99, 105, 1, 0]])
    data = {f"S{i}": b for i in range(5)}
    trades = engine.run(data, Always("BUY", stop=98, target=104))
    assert len(trades) == config.MAX_TRADES_PER_DAY


def test_stall_exit():
    idx = pd.date_range("2024-01-02 09:15", "2024-01-02 15:25", freq="5min", tz="Asia/Kolkata")
    b = pd.DataFrame([[100, 100.5, 99.5, 100, 1, 0]] * len(idx), columns=["open", "high", "low", "close", "volume", "oi"], index=idx)
    s = Always("BUY", stop=90, target=110)
    s.stall_minutes, s.stall_min_r = 60, 0.2
    t = engine.run_day("X", b, s)
    assert t.exit_reason == "stall" and (t.exit_time - t.entry_time).total_seconds() == 3600


def test_orb_rvol_filter_blocks_quiet_open():
    o = ORB(min_rvol=2.0)
    prior = bars([[100, 100.5, 99.5, 100, 1000, 0]] * 75, day="2024-01-01")
    o.on_day_start(prior)
    assert o.avg_or_volume is None  # only 1 prior day, need >= 5
    o.avg_or_volume = 3000  # pretend 14-day avg of first-15-min volume
    today = bars([[100, 100.5, 99.5, 100, 1000, 0]] * 3 + [[100, 101.2, 100, 101, 1000, 0]])
    assert o.on_bar(today) is None  # 3000/3000 = 1.0 < 2.0
    o.avg_or_volume = 1000
    assert o.on_bar(today).side == "BUY"


def test_ambiguous_bar_optimistic_fills_target():
    b = bars([[100, 101, 99, 100, 1, 0], [100, 101, 99, 100, 1, 0], [100, 110, 90, 100, 1, 0]])
    t = engine.run_day("X", b, Always("BUY", stop=98, target=104), ambiguous="target")
    assert t.exit_reason == "target"


def test_pct_stop_target_relative_to_fill():
    b = bars([[100, 101, 99, 100, 1, 0], [102, 102.5, 101.5, 102, 1, 0], [102, 110, 101.9, 105, 1, 0]])
    s = Always("BUY", 0, 0)
    s.sig = Signal("BUY", stop_pct=1.0, target_pct=2.0)
    t = engine.run_day("X", b, s)
    assert t.stop == pytest.approx(t.entry * 0.99, rel=1e-3) and t.target == pytest.approx(t.entry * 1.02, rel=1e-3)
