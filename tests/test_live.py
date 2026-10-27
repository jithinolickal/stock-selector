import os

import pandas as pd
import pytest

from live.broker import PaperBroker, fill_or_retry, make_broker
from live.straddle import Straddle

TZ = "Asia/Kolkata"


def legs(ce=100.0, pe=80.0):
    return [dict(opt="CE", key="CE1", strike=22000, entry=ce, open=True, exit=None, why=None, t=None),
            dict(opt="PE", key="PE1", strike=22000, entry=pe, open=True, exit=None, why=None, t=None)]


def q(ce, pe):
    return {"CE1": dict(ltp=ce, bid=ce, ask=ce), "PE1": dict(ltp=pe, bid=pe, ask=pe)}


T0, TX = pd.Timestamp("2026-10-27 10:00", tz=TZ), pd.Timestamp("2026-10-27 15:10", tz=TZ)


def test_no_action_when_quiet():
    p = Straddle(legs(), 65, 25, 3000)
    assert p.actions(q(90, 85), T0, TX) == []
    assert p.mtm(q(90, 85)) == (10 - 5) * 65


def test_leg_stop_triggers_only_that_leg():
    p = Straddle(legs(), 65, 25, 3000)
    acts = p.actions(q(125, 70), T0, TX)
    assert [(L["opt"], why) for L, why in acts] == [("CE", "sl")]


def test_mtm_stop_closes_all():
    p = Straddle(legs(), 65, 25, 3000)
    acts = p.actions(q(120, 110), T0, TX)   # loss (20+30)*65 = 3250
    assert sorted(why for _, why in acts) == ["mtm", "mtm"]


def test_time_exit_closes_all():
    p = Straddle(legs(), 65, 25, 3000)
    assert [why for _, why in p.actions(q(50, 50), TX, TX)] == ["time", "time"]


def test_result_pnl_and_costs():
    p = Straddle(legs(), 65, 25, 3000)
    p.legs[0].update(open=False, exit=50.0, why="time", t="15:10")
    p.legs[1].update(open=False, exit=40.0, why="time", t="15:10")
    r = p.result("NIFTY", "2026-10-27", "paper", 22010, 22000)
    assert r["gross"] == (50 + 40) * 65
    assert 0 < r["cost"] < 300
    assert r["net"] == r["gross"] - r["cost"]


def test_paper_fill_or_retry_fills_below_bid():
    b = PaperBroker()
    f = fill_or_retry(b, "CE1", "SELL", 65, dict(bid=100, ask=101, refresh=lambda: None), "t")
    assert f.status == "complete" and f.price == pytest.approx(99.5)


def test_live_mode_refuses_without_ack(monkeypatch):
    monkeypatch.setenv("LIVE_TRADING", "no")
    with pytest.raises(RuntimeError):
        make_broker("live", live_ack=True)
    monkeypatch.setenv("LIVE_TRADING", "yes")
    with pytest.raises(RuntimeError):
        make_broker("live", live_ack=False)
    assert make_broker("paper").name == "paper"
