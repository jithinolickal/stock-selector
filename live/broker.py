"""Broker layer: one interface, three backends.

PaperBroker   - no network for orders; fills instantly at the quoted bid/ask. Default.
SandboxBroker - real HTTP to Upstox sandbox (api-sandbox.upstox.com). Orders are accepted and
                return ids but nothing is executed and there is no order-status endpoint, so fills
                are simulated exactly like paper. Use it to prove the request format/auth works.
UpstoxBroker  - real money. Guarded: needs LIVE_TRADING=yes in .env AND --live-i-understand flag.

Upstox facts this file relies on (verified 27 Oct 2026 from the API docs):
  place  POST https://api-hft.upstox.com/v3/order/place   body: quantity(units), product I/D,
         validity DAY, price, tag, instrument_token, order_type MARKET/LIMIT/SL/SL-M,
         transaction_type BUY/SELL, disclosed_quantity, trigger_price, slice, market_protection
         -> data.order_ids[]
  cancel DELETE https://api-hft.upstox.com/v3/order/cancel?order_id=
  status GET https://api.upstox.com/v2/order/details?order_id=  -> data.status ('complete',
         'rejected', 'cancelled', 'open', ...), average_price, filled_quantity, status_message
  pos    GET https://api.upstox.com/v2/portfolio/short-term-positions
  funds  GET https://api.upstox.com/v2/user/get-funds-and-margin?segment=SEC -> data.equity.available_margin
  margin POST https://api.upstox.com/v2/charges/margin {instruments:[{instrument_key,quantity,
         transaction_type,product}]} -> data.required_margin, final_margin
  sandbox host: https://api-sandbox.upstox.com (same paths; place/modify/cancel only)
  rate limit for order APIs: 10/s, 500/min, 2000/30min. F&O quantity is in UNITS (lot_size * lots).
  The daily trading token (OAuth, expires ~3:30 AM) is required for orders. The 1-year Analytics
  token used for data cannot place orders.
"""
import os
import time as _time
from dataclasses import dataclass, field

import requests


@dataclass
class Fill:
    order_id: str
    key: str
    side: str
    qty: int
    price: float
    status: str = "complete"   # complete | rejected | cancelled | open
    message: str = ""


@dataclass
class PaperBroker:
    """Fills immediately at the price you pass (caller passes bid for SELL, ask for BUY)."""
    name: str = "paper"
    fills: list = field(default_factory=list)

    def place(self, key: str, side: str, qty: int, price: float, tag: str = "") -> Fill:
        f = Fill(f"paper-{len(self.fills) + 1}", key, side, qty, price)
        self.fills.append(f)
        return f

    def status(self, order_id: str) -> Fill:
        return next(f for f in self.fills if f.order_id == order_id)

    def cancel(self, order_id: str) -> None:
        pass

    def positions(self) -> list:
        return []

    def preflight(self, legs: list, lot: int) -> str:
        return "paper: no margin check"


class UpstoxBroker:
    """Real orders. Every call raises on HTTP error so the runner can decide what to do."""
    name = "live"
    HOST, ORDER_HOST = "https://api.upstox.com", "https://api-hft.upstox.com"

    def __init__(self, token: str):
        self.h = {"Authorization": f"Bearer {token}", "Accept": "application/json", "Content-Type": "application/json"}

    def _req(self, method, url, **kw):
        r = requests.request(method, url, headers=self.h, timeout=15, **kw)
        if r.status_code >= 400:
            raise RuntimeError(f"{method} {url} -> {r.status_code} {r.text[:300]}")
        return r.json().get("data", {})

    def place(self, key: str, side: str, qty: int, price: float, tag: str = "") -> Fill:
        body = dict(quantity=qty, product="I", validity="DAY", price=round(price, 2), tag=tag[:40], instrument_token=key,
                    order_type="LIMIT", transaction_type=side, disclosed_quantity=0, trigger_price=0, is_amo=False, slice=False)
        d = self._req("POST", f"{self.ORDER_HOST}/v3/order/place", json=body)
        return Fill(d["order_ids"][0], key, side, qty, price, status="open")

    def status(self, order_id: str) -> Fill:
        d = self._req("GET", f"{self.HOST}/v2/order/details", params={"order_id": order_id})
        return Fill(order_id, d.get("instrument_token", ""), d.get("transaction_type", ""), d.get("filled_quantity", 0),
                    float(d.get("average_price") or 0), d.get("status", "open"), d.get("status_message") or "")

    def cancel(self, order_id: str) -> None:
        self._req("DELETE", f"{self.ORDER_HOST}/v3/order/cancel", params={"order_id": order_id})

    def positions(self) -> list:
        return self._req("GET", f"{self.HOST}/v2/portfolio/short-term-positions")

    def funds(self) -> float:
        return float(self._req("GET", f"{self.HOST}/v2/user/get-funds-and-margin", params={"segment": "SEC"})["equity"]["available_margin"])

    def margin(self, legs: list, qty: int) -> float:
        ins = [dict(instrument_key=L["key"], quantity=qty, transaction_type=L["side"], product="I") for L in legs]
        return float(self._req("POST", f"{self.HOST}/v2/charges/margin", json={"instruments": ins})["final_margin"])

    def preflight(self, legs: list, lot: int) -> str:
        """Refuse to trade unless available funds cover the margin with a 20% buffer."""
        need, have = self.margin(legs, lot), self.funds()
        if have < need * 1.2:
            raise RuntimeError(f"insufficient margin: need {need:.0f} x1.2, have {have:.0f}")
        return f"margin ok: need {need:.0f}, available {have:.0f}"


class SandboxBroker(UpstoxBroker):
    """Same requests against the sandbox host. No status endpoint, so fills are simulated."""
    name = "sandbox"
    HOST = ORDER_HOST = "https://api-sandbox.upstox.com"

    def __init__(self, token: str):
        super().__init__(token)
        self._fills = {}

    def place(self, key, side, qty, price, tag=""):
        f = super().place(key, side, qty, price, tag)
        f.status = "complete"
        self._fills[f.order_id] = f
        return f

    def status(self, order_id):
        return self._fills[order_id]

    def positions(self):
        return []

    def preflight(self, legs, lot):
        return "sandbox: margin/funds endpoints not available, skipped"


def make_broker(mode: str, live_ack: bool = False):
    if mode == "paper":
        return PaperBroker()
    if mode == "sandbox":
        tok = os.getenv("UPSTOX_SANDBOX_TOKEN")
        if not tok:
            raise RuntimeError("UPSTOX_SANDBOX_TOKEN missing in .env (create a sandbox app at account.upstox.com/developer/apps)")
        return SandboxBroker(tok)
    if mode == "live":
        if os.getenv("LIVE_TRADING") != "yes" or not live_ack:
            raise RuntimeError("live mode needs LIVE_TRADING=yes in .env AND the --live-i-understand flag")
        tok = os.getenv("UPSTOX_TRADE_TOKEN")
        if not tok:
            raise RuntimeError("UPSTOX_TRADE_TOKEN missing: run scripts/login.py this morning")
        return UpstoxBroker(tok)
    raise ValueError(mode)


def fill_or_retry(broker, key: str, side: str, qty: int, quote: dict, tag: str, tries: int = 3, wait: float = 3.0) -> Fill:
    """Aggressive LIMIT: sell slightly below bid / buy slightly above ask so it fills now but
    cannot fill at a silly price. Re-quote and retry if not complete; last try is 2% through.
    Returns the final Fill (status 'complete') or raises."""
    for i in range(tries):
        bid, ask = quote["bid"], quote["ask"]
        pad = (0.005, 0.01, 0.02)[min(i, 2)]
        price = bid * (1 - pad) if side == "SELL" else ask * (1 + pad)
        f = broker.place(key, side, qty, price, tag)
        for _ in range(int(wait / 0.5)):
            s = broker.status(f.order_id)
            if s.status == "complete":
                return s
            if s.status in ("rejected", "cancelled"):
                raise RuntimeError(f"order {f.order_id} {s.status}: {s.message}")
            _time.sleep(0.5)
        try:
            broker.cancel(f.order_id)
        except Exception as e:  # noqa: BLE001 - may already be filled
            s = broker.status(f.order_id)
            if s.status == "complete":
                return s
            raise RuntimeError(f"cancel failed and order not complete: {e}")
        quote = quote["refresh"]()
    raise RuntimeError(f"{side} {key} not filled after {tries} tries")
