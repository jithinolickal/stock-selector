"""Expiry-day short-straddle runner (paper / sandbox / live). Read live/README.md first.

    .venv/bin/python -m live.straddle                       # paper, no orders (default)
    .venv/bin/python -m live.straddle --mode sandbox        # HTTP to Upstox sandbox, simulated fills
    .venv/bin/python -m live.straddle --mode live --live-i-understand   # real money

Rules (from the backtest in reports/Options expiry straddle results.md):
  expiry day only -> at ENTRY sell 1 lot ATM CE + 1 lot ATM PE (product I, intraday)
  -> per leg: buy back if LTP >= entry * (1 + SL%)   [25%]
  -> all legs: buy back if combined loss >= MTM_STOP  [₹3,000 per lot]
  -> whatever is open is bought back at EXIT          [15:10, or 10:20 for the 1-hour variant]
Everything else in this file is plumbing and safeguards.
"""
import argparse
import csv
import json
import os
import sys
import time as _time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from live.broker import fill_or_retry, make_broker
from options.engine import _charges

load_dotenv(config.ROOT / ".env")
TZ = "Asia/Kolkata"
API = "https://api.upstox.com/v2"
IDX = {"NIFTY": ("NSE_INDEX|Nifty 50", 50), "SENSEX": ("BSE_INDEX|SENSEX", 100)}
OUT = config.RESULTS_DIR / "live"
STOP_FILE = Path(__file__).with_name("STOP")   # touch live/STOP -> close everything and exit


def now():
    return pd.Timestamp.now(tz=TZ)


def log(msg):
    print(f"{now():%H:%M:%S} {msg}", flush=True)


# ---------------- market data (Analytics token, read-only) ----------------
def get(path, **params):
    r = requests.get(f"{API}/{path}", params=params, timeout=15,
                     headers={"Authorization": f"Bearer {os.environ['UPSTOX_ACCESS_TOKEN']}", "Accept": "application/json"})
    r.raise_for_status()
    return r.json()["data"]


def contracts(key, day):
    """{(strike, 'CE'|'PE'): (instrument_key, lot_size)} for today's expiry."""
    rows = get("option/contract", instrument_key=key, expiry_date=day)
    return {(int(r["strike_price"]), r["instrument_type"]): (r["instrument_key"], int(r["lot_size"])) for r in rows}


def quotes(keys):
    """{instrument_key: {ltp, bid, ask}} from the full-quote endpoint (depth level 1)."""
    d = get("market-quote/quotes", instrument_key=",".join(keys))
    out = {}
    for v in d.values():
        buy, sell = v["depth"]["buy"], v["depth"]["sell"]
        ltp = float(v["last_price"])
        out[v["instrument_token"]] = dict(ltp=ltp, bid=float(buy[0]["price"]) if buy and buy[0]["price"] else ltp,
                                          ask=float(sell[0]["price"]) if sell and sell[0]["price"] else ltp)
    return out


def spot(key):
    d = get("market-quote/ltp", instrument_key=key)
    return float(next(iter(d.values()))["last_price"])


# ---------------- position logic (pure, unit-tested) ----------------
class Straddle:
    def __init__(self, legs: list, qty: int, sl_pct: float, mtm_stop: float):
        self.legs, self.qty, self.sl_pct, self.mtm_stop = legs, qty, sl_pct, mtm_stop  # legs: dict(opt,key,strike,entry,open,exit,why,t)

    def mtm(self, q: dict) -> float:
        return sum((L["entry"] - (q[L["key"]]["ltp"] if L["open"] else L["exit"])) * self.qty for L in self.legs)

    def actions(self, q: dict, ts, t_exit) -> list:
        """Legs that must be closed now and why. Checked in this order: time, mtm, per-leg sl."""
        open_ = [L for L in self.legs if L["open"]]
        if not open_:
            return []
        if ts >= t_exit:
            return [(L, "time") for L in open_]
        if self.mtm_stop and self.mtm(q) <= -self.mtm_stop:
            return [(L, "mtm") for L in open_]
        return [(L, "sl") for L in open_ if q[L["key"]]["ltp"] >= L["entry"] * (1 + self.sl_pct / 100)]

    def done(self):
        return not any(L["open"] for L in self.legs)

    def result(self, symbol, day, mode, spot_px, atm):
        gross = cost = credit = 0.0
        for L in self.legs:
            gross += (L["entry"] - L["exit"]) * self.qty
            cost += _charges(L["entry"] * self.qty, True) + _charges(L["exit"] * self.qty, False)
            credit += L["entry"] * self.qty
        return dict(mode=mode, symbol=symbol, day=day, spot=round(spot_px, 1), atm=atm, qty=self.qty, credit=round(credit), gross=round(gross),
                    cost=round(cost), net=round(gross - cost), exits=",".join(L["why"] or "" for L in self.legs),
                    legs=" ".join(f"S{L['opt']}{L['strike']}@{L['entry']:.2f}->{L['exit']:.2f}({L['t']})" for L in self.legs))


# ---------------- runner ----------------
def save_state(path, pos, meta):
    path.write_text(json.dumps(dict(meta=meta, legs=pos.legs), default=str, indent=1))


def close_leg(broker, pos, L, why, q, tag):
    qd = dict(q[L["key"]], refresh=lambda: quotes([L["key"]])[L["key"]])
    f = fill_or_retry(broker, L["key"], "BUY", pos.qty, qd, tag)
    L.update(open=False, exit=f.price, why=why, t=now().strftime("%H:%M:%S"))
    log(f"CLOSED {L['opt']}{L['strike']} @ {f.price:.2f} ({why}) order {f.order_id}")


def main(a):
    key, step = IDX[a.symbol]
    day = str(now().date())
    t_in, t_out = pd.Timestamp(f"{day} {a.entry}", tz=TZ), pd.Timestamp(f"{day} {a.exit}", tz=TZ)
    OUT.mkdir(parents=True, exist_ok=True)
    state_f = OUT / f"state_{a.symbol}_{day}.json"
    tag = f"straddle-{day}"
    broker = make_broker(a.mode, a.live_i_understand)
    log(f"mode={broker.name} symbol={a.symbol} entry={a.entry} exit={a.exit} sl={a.sl}% mtm={a.mtm} lots={a.lots}")

    # --- guards ---
    if STOP_FILE.exists():
        sys.exit(f"{STOP_FILE} exists: remove it to run")
    if now() >= t_out:
        sys.exit("past exit time, nothing to do")
    try:
        cons = contracts(key, day)
    except requests.HTTPError as e:
        sys.exit(f"contract lookup failed (token? holiday?): {e}")
    if not cons:
        sys.exit(f"{day} is not a {a.symbol} expiry day; exiting")
    if a.lots > 1 and not a.allow_multi_lot:
        sys.exit("lots > 1 needs --allow-multi-lot (sizing beyond 1 lot is not validated)")

    # --- resume if the script restarted mid-trade ---
    if state_f.exists():
        st = json.loads(state_f.read_text())
        pos = Straddle(st["legs"], st["meta"]["qty"], a.sl, a.mtm)
        spot_px, atm = st["meta"]["spot"], st["meta"]["atm"]
        log(f"RESUMED from {state_f}: {[(L['opt'], L['open']) for L in pos.legs]}")
    else:
        while now() < t_in:
            if STOP_FILE.exists():
                sys.exit("STOP file found before entry; exiting without trading")
            _time.sleep(min(5, max(0.2, (t_in - now()).total_seconds())))
        spot_px = spot(key)
        atm = int(round(spot_px / step) * step)
        (ce_key, lot), (pe_key, _) = cons[(atm, "CE")], cons[(atm, "PE")]
        qty = lot * a.lots
        legs = [dict(opt="CE", key=ce_key, strike=atm, side="SELL"), dict(opt="PE", key=pe_key, strike=atm, side="SELL")]
        log(broker.preflight(legs, qty))
        q = quotes([ce_key, pe_key])
        log(f"spot {spot_px:.1f} atm {atm} CE bid/ask {q[ce_key]['bid']}/{q[ce_key]['ask']} PE {q[pe_key]['bid']}/{q[pe_key]['ask']} qty {qty}")
        if max(q[k]["ask"] - q[k]["bid"] for k in (ce_key, pe_key)) > a.max_spread:
            sys.exit(f"spread wider than {a.max_spread}: not entering")
        pos = Straddle([], qty, a.sl, a.mtm)
        for L in legs:
            try:
                qd = dict(q[L["key"]], refresh=lambda k=L["key"]: quotes([k])[k])
                f = fill_or_retry(broker, L["key"], "SELL", qty, qd, tag)
                pos.legs.append(dict(L, entry=f.price, open=True, exit=None, why=None, t=None))
                log(f"SOLD {L['opt']}{atm} @ {f.price:.2f} order {f.order_id}")
            except Exception as e:  # noqa: BLE001
                log(f"ENTRY FAILED for {L['opt']}: {e}")
                for O in pos.legs:   # never sit on a single naked leg that was not the plan
                    close_leg(broker, pos, O, "entry_abort", quotes([O["key"]]), tag)
                sys.exit(1)
        save_state(state_f, pos, dict(qty=qty, spot=spot_px, atm=atm, day=day))

    # --- monitor loop ---
    keys = [L["key"] for L in pos.legs]
    errors = 0
    with open(OUT / f"ticks_{a.symbol}_{day}.csv", "a", newline="") as fh:
        w = csv.writer(fh)
        while not pos.done():
            _time.sleep(a.poll)
            ts = now()
            try:
                q = quotes(keys)
                errors = 0
            except Exception as e:  # noqa: BLE001
                errors += 1
                log(f"quote error {errors}: {e}")
                if errors >= 20:   # ~1 min blind in live: get flat rather than run unprotected
                    log("too many quote errors: closing everything")
                    for L in pos.legs:
                        if L["open"]:
                            close_leg(broker, pos, L, "error", quotes([L["key"]]), tag)
                    break
                continue
            m = pos.mtm(q)
            w.writerow([ts.strftime("%H:%M:%S")] + [q[k]["ltp"] for k in keys] + [round(m)])
            fh.flush()
            if ts.second < a.poll:
                log(" ".join(f"{L['opt']} {q[L['key']]['ltp']}" for L in pos.legs) + f" MTM {m:+.0f}")
            todo = pos.actions(q, ts, t_out)
            if STOP_FILE.exists():
                todo = [(L, "stop_file") for L in pos.legs if L["open"]]
            for L, why in todo:
                close_leg(broker, pos, L, why, q, tag)
                save_state(state_f, pos, dict(qty=pos.qty, spot=spot_px, atm=atm, day=day))

    # --- wrap up ---
    row = pos.result(a.symbol, day, broker.name, spot_px, atm)
    f = OUT / "trades.csv"
    new = not f.exists() or f.stat().st_size == 0
    with open(f, "a", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=row.keys())
        if new:
            wr.writeheader()
        wr.writerow(row)
    state_f.rename(state_f.with_suffix(".done.json"))
    log(f"DONE net ₹{row['net']} ({row['exits']}) -> {f}")
    if broker.name == "live":
        left = [p for p in broker.positions() if p["instrument_token"] in keys and int(p["quantity"]) != 0]
        if left:
            log(f"!!! OPEN POSITION REMAINS, close manually in the app: {left}")
            sys.exit(2)
        log("reconciled: no open position in our instruments")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--mode", choices=["paper", "sandbox", "live"], default="paper")
    p.add_argument("--live-i-understand", action="store_true", help="required with --mode live")
    p.add_argument("--symbol", default="NIFTY", choices=list(IDX))
    p.add_argument("--entry", default="09:20")
    p.add_argument("--exit", default="15:10")
    p.add_argument("--sl", type=float, default=25.0, help="per-leg stop, %% of entry premium")
    p.add_argument("--mtm", type=float, default=3000.0, help="combined loss stop in rupees per lot-set, 0 = off")
    p.add_argument("--lots", type=int, default=1)
    p.add_argument("--allow-multi-lot", action="store_true")
    p.add_argument("--max-spread", type=float, default=2.0, help="skip entry if bid/ask spread (points) exceeds this")
    p.add_argument("--poll", type=int, default=3, help="seconds between quote polls")
    main(p.parse_args())
