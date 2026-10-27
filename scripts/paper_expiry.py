"""Paper-trade the expiry-day short straddle on live Upstox data. Places NO orders.

Replay: if started after the entry time, rebuilds the trade from today's 1-min candles
(same rules as the backtest) so the day still counts as a forward-test sample.
Live: polls LTP, applies per-leg stop / MTM stop / time exit, logs every tick.

    .venv/bin/python scripts/paper_expiry.py --replay          # 9:20 entry from candles
    .venv/bin/python scripts/paper_expiry.py --live            # enter now (or at --entry), poll till exit
"""
import argparse
import csv
import os
import sys
import time as _time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from data.upstox import fetch_today
from options.engine import _charges, lot_size

load_dotenv(config.ROOT / ".env")
API = "https://api.upstox.com/v2"
IDX = {"NIFTY": ("NSE_INDEX|Nifty 50", 50), "SENSEX": ("BSE_INDEX|SENSEX", 100)}
TZ = "Asia/Kolkata"
OUT = config.RESULTS_DIR / "paper"


def get(path, **params):
    r = requests.get(f"{API}/{path}", params=params, timeout=30,
                     headers={"Authorization": f"Bearer {os.environ['UPSTOX_ACCESS_TOKEN']}", "Accept": "application/json"})
    r.raise_for_status()
    return r.json()["data"]


def now():
    return pd.Timestamp.now(tz=TZ)


def atm_row(key, expiry, spot, step):
    atm = int(round(spot / step) * step)
    row = next(r for r in get("option/chain", instrument_key=key, expiry_date=expiry) if r["strike_price"] == atm)
    return atm, {"CE": row["call_options"], "PE": row["put_options"]}


def ltp(keys):
    d = get("market-quote/ltp", instrument_key=",".join(keys))
    return {v["instrument_token"]: v["last_price"] for v in d.values()}


def update(legs, ts, px, a, lot):
    """Apply per-leg SL and MTM stop at one timestamp. Returns True when everything is closed."""
    for L in legs.values():
        p = px.get(L["key"])
        if L["open"] and p is not None and p >= L["entry"] * (1 + a.sl / 100):
            L.update(open=False, exit_px=p * (1 + a.slip / 100), exit_t=ts, why="sl")
    pnl = sum((L["entry_fill"] - (px.get(L["key"], L["entry"]) if L["open"] else L["exit_px"])) * lot for L in legs.values())
    if a.mtm and pnl <= -a.mtm:
        for L in legs.values():
            if L["open"]:
                L.update(open=False, exit_px=px.get(L["key"], L["entry"]) * (1 + a.slip / 100), exit_t=ts, why="mtm")
    return not any(L["open"] for L in legs.values())


def close_rest(legs, ts, px, a, why):
    for L in legs.values():
        if L["open"]:
            L.update(open=False, exit_px=px.get(L["key"], L["entry"]) * (1 + a.slip / 100), exit_t=ts, why=why)


def make_legs(opts, atm, entry_px, a):
    return {o: dict(key=opts[o]["instrument_key"], strike=atm, entry=entry_px[o], entry_fill=entry_px[o] * (1 - a.slip / 100), open=True)
            for o in ("CE", "PE")}


def finish(mode, symbol, day, spot, atm, legs, lot, a):
    gross = cost = credit = 0.0
    for L in legs.values():
        gross += (L["entry_fill"] - L["exit_px"]) * lot
        cost += _charges(L["entry_fill"] * lot, True) + _charges(L["exit_px"] * lot, False)
        credit += L["entry_fill"] * lot
    row = dict(mode=mode, symbol=symbol, day=day, spot=round(spot, 1), atm=atm, lot=lot, credit=round(credit), gross=round(gross),
               cost=round(cost), net=round(gross - cost), exits=",".join(L["why"] for L in legs.values()),
               legs=" ".join(f"S{o}{L['strike']}@{L['entry']:.1f}->{L['exit_px']:.1f}({L['exit_t']:%H:%M})" for o, L in legs.items()))
    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / "trades.csv"
    with open(f, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=row.keys())
        if f.stat().st_size == 0:
            w.writeheader()
        w.writerow(row)
    print(row)
    return row


def mtm_now(legs, px, lot):
    return sum((L["entry_fill"] - (px.get(L["key"], L["entry"]) if L["open"] else L["exit_px"])) * lot for L in legs.values())


def replay(symbol, key, step, expiry, day, t_in, t_out, a):
    idx = fetch_today(key, 1)
    spot = float(idx.loc[t_in, "open"])
    atm, opts = atm_row(key, expiry, spot, step)
    c = {o: fetch_today(opts[o]["instrument_key"], 1) for o in opts}
    legs = make_legs(opts, atm, {o: float(c[o].loc[t_in, "open"]) for o in opts}, a)
    lot = lot_size(symbol, day)
    print(f"replay {day} spot {spot:.1f} atm {atm} entry CE {legs['CE']['entry']:.2f} PE {legs['PE']['entry']:.2f} lot {lot}")
    last = {}
    for ts in c["CE"].index[c["CE"].index > t_in]:
        if ts >= t_out:
            break
        last = {legs[o]["key"]: float(c[o].loc[ts, "close"]) for o in opts if ts in c[o].index}
        if update(legs, ts, last, a, lot):
            break
    ts = min(c["CE"].index[-1], t_out)
    if any(L["open"] for L in legs.values()):
        if now() >= t_out:
            close_rest(legs, ts, last, a, "time")
        else:
            print(f"still open at {ts:%H:%M}: MTM {mtm_now(legs, last, lot):+.0f} "
                  + " ".join(f"{o} {L['entry']:.1f}->{last.get(L['key'], float('nan')):.1f} {'open' if L['open'] else L['why']}" for o, L in legs.items()))
            return
    finish("replay", symbol, day, spot, atm, legs, lot, a)


def live(symbol, key, step, expiry, day, t_in, t_out, a):
    while now() < t_in:
        _time.sleep(1)
    ch = get("option/chain", instrument_key=key, expiry_date=expiry)
    spot = ch[0]["underlying_spot_price"]
    atm, opts = atm_row(key, expiry, spot, step)
    legs = make_legs(opts, atm, {o: opts[o]["market_data"]["bid_price"] for o in opts}, a)  # sell at bid
    lot = lot_size(symbol, day)
    OUT.mkdir(parents=True, exist_ok=True)
    tick_f = OUT / f"{symbol}_{day}_ticks.csv"
    print(f"live {now():%H:%M:%S} spot {spot:.1f} atm {atm} sold CE {legs['CE']['entry']:.2f} PE {legs['PE']['entry']:.2f} lot {lot}", flush=True)
    keys = [L["key"] for L in legs.values()]
    with open(tick_f, "a", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["ts", "CE", "PE", "mtm"])
        while True:
            _time.sleep(a.poll)
            ts = now()
            try:
                px = ltp(keys)
            except Exception as e:  # noqa: BLE001
                print("ltp error", e, flush=True)
                continue
            m = mtm_now(legs, px, lot)
            w.writerow([ts.strftime("%H:%M:%S"), px.get(keys[0]), px.get(keys[1]), round(m)])
            fh.flush()
            if ts.second < a.poll:
                print(f"{ts:%H:%M} CE {px.get(keys[0])} PE {px.get(keys[1])} MTM {m:+.0f}", flush=True)
            if update(legs, ts, px, a, lot):
                break
            if ts >= t_out:
                close_rest(legs, ts, px, a, "time")
                break
    finish("live", symbol, day, spot, atm, legs, lot, a)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--symbol", default="NIFTY")
    p.add_argument("--entry", default="09:20")
    p.add_argument("--exit", default="15:10")
    p.add_argument("--sl", type=float, default=25.0)
    p.add_argument("--mtm", type=float, default=3000.0)
    p.add_argument("--slip", type=float, default=1.0)
    p.add_argument("--poll", type=int, default=5)
    p.add_argument("--replay", action="store_true")
    p.add_argument("--live", action="store_true")
    a = p.parse_args()
    key, step = IDX[a.symbol]
    day = str(now().date())
    expiries = sorted({c["expiry"] for c in get("option/contract", instrument_key=key)})
    if day not in expiries:
        sys.exit(f"{day} is not an expiry day; next: {expiries[:2]}")
    t_in, t_out = pd.Timestamp(f"{day} {a.entry}", tz=TZ), pd.Timestamp(f"{day} {a.exit}", tz=TZ)
    if a.replay:
        replay(a.symbol, key, step, day, day, t_in, t_out, a)
    if a.live:
        live(a.symbol, key, step, day, day, t_in, t_out, a)
