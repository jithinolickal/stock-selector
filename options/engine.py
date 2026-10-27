"""Minute-level simulator for multi-leg intraday option positions.

A Setup lists legs as (option_type, strike_offset_in_steps, side, lots). The engine
prices legs off the 1-min chain, applies per-leg stop (% of entry premium, short
legs), optional combined MTM stop (₹ per lot), and exits everything at `exit_time`.
"""
from dataclasses import dataclass, field
from datetime import time

import pandas as pd

from options import data

# Charges per leg (Oct 2024 regime): brokerage ₹20/order, STT 0.1% on sell premium,
# NSE txn 0.03503% of premium, SEBI 0.0001%, stamp 0.003% buy, GST 18% on (brok+txn+sebi)
BROKERAGE = 20.0
STT_SELL = 0.001
EXCH = 0.00035
SEBI = 0.000001
STAMP_BUY = 0.00003
GST = 0.18


def lot_size(symbol: str, day: str) -> int:
    if symbol == "NIFTY":
        return 50 if day < "2024-11-20" else 75 if day < "2025-12-30" else 65
    if symbol == "SENSEX":
        return 10 if day < "2024-11-20" else 20
    if symbol == "BANKNIFTY":
        return 25 if day < "2024-11-20" else 30 if day < "2025-12-30" else 35
    return 1


@dataclass
class Leg:
    opt: str          # "CE" / "PE"
    offset: int       # strikes from ATM, in steps (+ above, - below)
    side: str         # "SELL" / "BUY"
    lots: int = 1
    offset_pct: float | None = None  # if set, offset = round(spot * pct / 100 / step), signed like `offset`


@dataclass
class Setup:
    name: str
    legs: list[Leg]
    entry: time = time(9, 20)
    exit: time = time(15, 10)
    leg_sl_pct: float | None = 25.0     # short legs: exit when price >= entry*(1+pct/100)
    close_hedge_with_short: bool = True  # when a short leg stops out, close its paired long too
    mtm_stop_rs: float | None = None    # combined loss per lot-set (₹) that closes everything
    slippage_pct: float = 1.0           # per fill, % of premium, against you
    only_expiry_day: bool = False
    min_dte: int = 0
    max_dte: int = 99
    day_filter: object = None  # callable(symbol, day, t_in) -> bool; False skips the day


def _charges(premium_value: float, sell: bool) -> float:
    c = BROKERAGE + premium_value * (EXCH + SEBI)
    c += premium_value * STT_SELL if sell else premium_value * STAMP_BUY
    return c + (BROKERAGE + premium_value * (EXCH + SEBI)) * GST


def run_day(symbol: str, day: str, setup: Setup) -> dict | None:
    expiry = data.nearest_expiry(symbol, day)
    if expiry is None:
        return None
    dte = (pd.Timestamp(expiry) - pd.Timestamp(day)).days
    if setup.only_expiry_day and dte != 0:
        return None
    if not (setup.min_dte <= dte <= setup.max_dte):
        return None
    tz = "Asia/Kolkata"
    t_in = pd.Timestamp(f"{day} {setup.entry}", tz=tz)
    t_out = pd.Timestamp(f"{day} {setup.exit}", tz=tz)
    spot = data.spot_at(symbol, t_in)
    if spot is None or data.index(symbol).loc[:t_in].index[-1].date() != t_in.date():
        return None
    if setup.day_filter is not None and not setup.day_filter(symbol, day, t_in):
        return None
    atm = data.atm(symbol, spot)
    step = data.STEP[symbol]
    dc = data.day_chain(symbol, expiry, day)
    if dc.empty:
        return None
    grid = pd.date_range(t_in, t_out, freq="1min")
    lot = lot_size(symbol, day)
    legs = []
    for lg in setup.legs:
        off = lg.offset if lg.offset_pct is None else int(round(spot * lg.offset_pct / 100 / step)) * (1 if lg.offset >= 0 else -1)
        strike = atm + off * step
        s = data.leg_series(dc, strike, lg.opt, grid)
        if s is None or pd.isna(s.iloc[0]):
            return None  # contract not traded at entry -> skip day
        legs.append(dict(leg=lg, strike=strike, px=s, entry=float(s.iloc[0]), open=True, exit_px=None, exit_t=None, why=None))
    slip = setup.slippage_pct / 100
    for L in legs:
        L["entry_fill"] = L["entry"] * (1 - slip) if L["leg"].side == "SELL" else L["entry"] * (1 + slip)
    # walk minutes
    def leg_pnl_pts(L, px):
        return (L["entry_fill"] - px) if L["leg"].side == "SELL" else (px - L["entry_fill"])
    for ts in grid[1:]:
        # per-leg stop on short legs
        for i, L in enumerate(legs):
            if not L["open"] or L["leg"].side != "SELL" or setup.leg_sl_pct is None:
                continue
            px = L["px"].loc[ts]
            if pd.notna(px) and px >= L["entry"] * (1 + setup.leg_sl_pct / 100):
                L.update(open=False, exit_px=px * (1 + slip), exit_t=ts, why="sl")
                if setup.close_hedge_with_short:
                    for H in legs:
                        if H["open"] and H["leg"].side == "BUY" and H["leg"].opt == L["leg"].opt:
                            hp = H["px"].loc[ts]
                            H.update(open=False, exit_px=(hp if pd.notna(hp) else H["entry"]) * (1 - slip), exit_t=ts, why="sl_hedge")
        if setup.mtm_stop_rs is not None:
            pnl = 0.0
            for L in legs:
                px = L["px"].loc[ts] if L["open"] else L["exit_px"]
                if pd.isna(px):
                    px = L["entry"]
                pnl += leg_pnl_pts(L, px) * lot * L["leg"].lots
            if pnl <= -setup.mtm_stop_rs:
                for L in legs:
                    if L["open"]:
                        px = L["px"].loc[ts]
                        L.update(open=False, exit_px=(px if pd.notna(px) else L["entry"]) * (1 + slip if L["leg"].side == "SELL" else 1 - slip), exit_t=ts, why="mtm")
                break
        if not any(L["open"] for L in legs):
            break
    for L in legs:
        if L["open"]:
            px = L["px"].iloc[-1]
            L.update(open=False, exit_px=(px if pd.notna(px) else L["entry"]) * (1 + slip if L["leg"].side == "SELL" else 1 - slip), exit_t=grid[-1], why="time")
    gross = cost = 0.0
    credit = 0.0
    for L in legs:
        q = lot * L["leg"].lots
        gross += leg_pnl_pts(L, L["exit_px"]) * q
        sell_first = L["leg"].side == "SELL"
        cost += _charges(L["entry_fill"] * q, sell_first) + _charges(L["exit_px"] * q, not sell_first)
        credit += (L["entry_fill"] if sell_first else -L["entry_fill"]) * q
    return dict(day=day, expiry=expiry, dte=dte, spot=spot, atm=atm, lot=lot, credit=round(credit), gross=round(gross), cost=round(cost),
                net=round(gross - cost), exits=",".join(L["why"] for L in legs),
                legs=" ".join(f"{L['leg'].side[0]}{L['leg'].opt}{L['strike']}@{L['entry']:.1f}->{L['exit_px']:.1f}" for L in legs))


def run(symbol: str, setup: Setup, start: str, end: str) -> pd.DataFrame:
    days = sorted({d for d in data.index(symbol).index.strftime("%Y-%m-%d").unique() if start <= d <= end})
    rows = [r for d in days if (r := run_day(symbol, d, setup))]
    return pd.DataFrame(rows)


def summary(t: pd.DataFrame, capital: float | None = None) -> dict:
    if t.empty:
        return {"days": 0}
    wins = t[t.net > 0]
    eq = t.net.cumsum()
    months = max(1, pd.to_datetime(t.day).dt.to_period("M").nunique())
    out = dict(days=len(t), win_rate=round(len(wins) / len(t) * 100, 1), avg_win=round(wins.net.mean()) if len(wins) else 0,
               avg_loss=round(t[t.net <= 0].net.mean()) if len(t) > len(wins) else 0,
               pf=round(wins.net.sum() / abs(t[t.net <= 0].net.sum()), 2) if (t.net <= 0).any() and t[t.net <= 0].net.sum() else float("inf"),
               net=round(t.net.sum()), net_per_month=round(t.net.sum() / months), gross_per_month=round(t.gross.sum() / months), max_dd=round((eq - eq.cummax()).min()),
               worst_day=round(t.net.min()), cost_share=round(t.cost.sum() / max(1, abs(t.gross.sum())) * 100))
    if capital:
        out["pct_per_month"] = round(out["net_per_month"] / capital * 100, 2)
        out["max_dd_pct"] = round(out["max_dd"] / capital * 100, 1)
    return out
