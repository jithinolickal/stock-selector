# live/ — expiry-day short straddle, paper → sandbox → live

This folder is the only code that can ever place an order. Everything else in the repo is
research. Read this whole file before running anything with `--mode live`.

## 1. What it trades and why (decision log)

| Rule | Value | Why (see `reports/Options expiry straddle results.md`) |
|---|---|---|
| Instrument | Nifty 50 weekly options, **expiry day only** (currently Tuesday) | Only setup that is positive after costs in 2021–26 data. Non-expiry days lose (DTE 1 PF 0.85, DTE 2+ 0.6–0.9). |
| Entry | **09:20:00**, sell 1 lot ATM CE + 1 lot ATM PE | 9:20 beats 9:30–11:00 entries by 3x (PF 1.73 vs 1.1–1.4). ATM = spot rounded to nearest 50. |
| Per-leg stop | buy back a leg when its LTP ≥ **1.25 × entry** | Stop 15–40% all work (PF 1.5–1.7); no stop → PF 0.99 with −₹31k worst day. 25% is the middle of the plateau. |
| Combined stop | close all when loss ≥ **₹3,000 per lot** | Improves PF 1.73 → 1.80, caps whipsaw days. |
| Exit | **15:10**, buy back whatever is open | Exit 15:00–15:20 makes no difference; 15:10 stays clear of broker auto-square-off. `--exit 10:20` is the 1-hour variant (PF 1.71, ~half the P&L, 1h exposure). |
| Product | `I` (intraday/MIS) | Lower margin; the position never carries overnight by design. |
| Size | 1 lot (currently 65 units), hard-capped | Live slippage is unmeasured. `--lots 2` requires `--allow-multi-lot`. |
| Orders | LIMIT, sell at bid −0.5% / buy at ask +0.5%, retry ×3 widening to 2% | Fills immediately like a market order but can't fill at a stupid price if the book is thin. Backtest assumed 1% slippage per fill, so this is inside the model. |
| Stops | executed by this script, not exchange SL-M orders | Keeps behaviour identical to the backtest (LTP-based, both legs independent). Cost: if the script dies the position is unprotected → see safeguards. |
| Expected | ~65% win rate, +₹2k avg win, −₹2.3k avg loss, ≈ +₹2.5k/month/lot, worst day ≈ −₹6.6k, max DD ≈ −₹14k | 258 expiry days. Forward test must confirm before sizing up. |

Not traded on purpose: Sensex (marginal, 2026 negative in most variants; the 12:00 Sensex
variant is a candidate, not proven), BankNifty (loses), any non-expiry day, any option buying.

## 2. Files

```
live/broker.py      PaperBroker / SandboxBroker / UpstoxBroker + fill_or_retry()
live/straddle.py    the runner: guards → entry → monitor loop → exit → reconcile
live/STOP           (create this file to make a running instance close everything and exit)
scripts/login.py    daily OAuth login → UPSTOX_TRADE_TOKEN in .env
tests/test_live.py  stop/MTM/time logic, paper fills, live-mode refusal
results/live/       trades.csv (one row per day), ticks_*.csv (every poll), state_*.json (resume)
```

## 2a. Expiry calendar (from Upstox contract list, Oct 2026)

| Index | Expiry | Lot | Status |
|---|---|---|---|
| Nifty 50 | every Tuesday | 65 | proven; run every week |
| Sensex | every Thursday | 20 | marginal; paper only, `--symbol SENSEX --entry 12:00 --sl 40` |
| BankNifty / FinNifty / MidcpNifty | monthly, last Tuesday | 30 / 60 / 120 | not traded (BankNifty loses) |
| Bankex | monthly, last Thursday | 30 | not tested |

≈ 8–10 weekly expiries a month (4–5 Nifty + 4–5 Sensex). A holiday moves the expiry to the previous trading day (e.g. Mon 9 Nov, Mon 23 Nov 2026); the runner's contract-list check handles that only if it is started that day.

## 3. Tokens (two different ones)

| Token | Env var | Life | Used for |
|---|---|---|---|
| Analytics (read-only) | `UPSTOX_ACCESS_TOKEN` | 1 year | option chain, contracts, quotes, LTP. Cannot place orders. |
| Trading (OAuth) | `UPSTOX_TRADE_TOKEN` | expires ~03:30 next day | orders, positions, funds, margin. **Must be refreshed every trading morning** with `scripts/login.py`. |
| Sandbox | `UPSTOX_SANDBOX_TOKEN` | 30 days | `--mode sandbox` only. Generate in account.upstox.com/developer/apps → Sandbox → New Sandbox App → Generate. |

`LIVE_TRADING=yes` in `.env` is additionally required for `--mode live`.

## 4. Modes

```
.venv/bin/python -m live.straddle                              # paper (default): no orders at all
.venv/bin/python -m live.straddle --mode sandbox               # real HTTP to api-sandbox.upstox.com
.venv/bin/python -m live.straddle --mode live --live-i-understand
```

- **paper**: quotes are real, fills are simulated at bid/ask. This is the forward test. Run it every expiry until you have 8–12 rows in `results/live/trades.csv` and they resemble the backtest (win rate ≥ 55%, avg net ≥ 0).
- **sandbox**: proves auth, request format and order ids with Upstox's sandbox. Sandbox has no order-status, positions or funds endpoints, so fills are simulated like paper. Orders never execute.
- **live**: real money. Refuses to start unless `LIVE_TRADING=yes` and the flag are both present.

Useful flags: `--exit 10:20` (1-hour variant), `--sl 25`, `--mtm 3000` (0 = off), `--poll 3`,
`--max-spread 2.0` (skip entry if bid/ask gap in points is wider), `--symbol SENSEX --entry 12:00 --sl 40`.

## 5. What the runner does, step by step

1. Load `.env`, build the broker for the mode (live refuses without both acks).
2. **Guards**: `live/STOP` exists → exit. Past exit time → exit. Ask Upstox for today's option contracts; none → today is not an expiry day → exit 0 (so a scheduler can fire every weekday). Lots > 1 without `--allow-multi-lot` → exit.
3. **Resume**: if `results/live/state_<symbol>_<day>.json` exists, the script crashed or was restarted mid-trade; it reloads the legs and goes straight to monitoring. In live mode cross-check the Positions tab in the app once.
4. Sleep until the entry time (checks STOP file while waiting).
5. Spot → ATM strike → instrument keys + lot size from the contract list (not hardcoded; lot sizes changed twice in the sample).
6. **Preflight** (live): margin API for the two sells vs available funds; needs funds ≥ 1.2 × margin or it exits.
7. Spread check, then sell CE, then PE with `fill_or_retry`. If the second leg fails, the first is bought back immediately (`entry_abort`) — never a lone naked leg by accident.
8. State file written. Monitor loop every `--poll` seconds: quotes → MTM → ticks CSV → checks in this order: exit time, MTM stop, per-leg stop, STOP file. Each close is a `fill_or_retry` BUY, state file updated after each.
9. 20 consecutive quote failures (~1 min blind) → close everything (`error`) rather than run unprotected.
10. Wrap-up: row appended to `results/live/trades.csv` (net includes Upstox charges at the Oct-2024 regime), state file renamed `.done.json`. Live mode then reads Positions; if any quantity remains in our instruments it prints `!!! OPEN POSITION REMAINS` and exits with code 2 — close it in the app.

## 6. Safeguards, in one list

- Paper is the default; live needs env var + flag; sandbox token can't trade.
- Expiry-day check from the exchange contract list, not a calendar.
- Hard cap 1 lot. Margin/funds preflight with 20% buffer.
- Spread guard at entry. LIMIT orders only, max 2% through the touch.
- Per-leg stop, combined MTM stop, time exit, STOP-file kill switch, quote-failure flat-out.
- Resume from state file after a crash; reconcile with broker positions at the end.
- Every poll logged; every fill logged with order id.
- Rate use: ~2 quote calls per poll + ≤ 12 order calls/day; limits are 50/s data, 10/s orders.

## 7. What is NOT handled (know these)

- **Script dies and does not restart** → position has no stop. Mitigation: run under launchd `KeepAlive` so it restarts and resumes; keep the Upstox app open on expiry days; Upstox will square off MIS positions itself in the last ~15 min (verify the exact F&O time in the app before going live; a possible Aug-2026 closing-auction change may move it).
- **Gap through the stop** (limit-down open after entry): loss can exceed −₹7k/lot. Iron-fly wings (buy 2% OTM CE/PE first) cap it at ~₹30k and cut margin to ~₹25k; not implemented in the runner yet.
- **Token expired** at 09:20 → contract/quote calls return 401 and the script exits before trading. Run `scripts/login.py` before 09:15.
- **Static IP**: Upstox requires a whitelisted static IP for order endpoints on some plans. Check the developer app settings before the first live run.
- **Holiday on Tuesday**: NSE shifts weekly expiry to the previous trading day. The contract-list check handles it only if you run the script that day; the scheduler below runs every weekday for that reason.
- No alerts beyond stdout/log. Tail the log or add a notifier before going live.

## 8. Daily routine (expiry day)

```
08:45  .venv/bin/python scripts/login.py        # paste redirect URL → UPSTOX_TRADE_TOKEN
09:00  .venv/bin/python -m live.straddle --mode paper   (or live, see above)
15:15  check results/live/trades.csv and the Positions tab (must be empty)
```

Scheduler (macOS launchd, runs every weekday 09:05, exits by itself on non-expiry days):

```xml
<!-- ~/Library/LaunchAgents/com.jithin.straddle.plist -->
<plist version="1.0"><dict>
  <key>Label</key><string>com.jithin.straddle</string>
  <key>ProgramArguments</key><array>
    <string>/Users/jithin/personal/code/stock-selector/.venv/bin/python</string>
    <string>-m</string><string>live.straddle</string><string>--mode</string><string>paper</string>
  </array>
  <key>WorkingDirectory</key><string>/Users/jithin/personal/code/stock-selector</string>
  <key>StartCalendarInterval</key><array>
    <dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>5</integer></dict>
    <dict><key>Weekday</key><integer>2</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>5</integer></dict>
    <dict><key>Weekday</key><integer>3</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>5</integer></dict>
    <dict><key>Weekday</key><integer>4</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>5</integer></dict>
    <dict><key>Weekday</key><integer>5</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>5</integer></dict>
  </array>
  <key>StandardOutPath</key><string>/Users/jithin/personal/code/stock-selector/results/live/launchd.log</string>
  <key>StandardErrorPath</key><string>/Users/jithin/personal/code/stock-selector/results/live/launchd.log</string>
</dict></plist>
```
`launchctl load ~/Library/LaunchAgents/com.jithin.straddle.plist`. The daily login step cannot be
automated without storing your Upstox password/TOTP; do it by hand.

## 9. Go-live checklist

- [ ] 8–12 paper expiries logged; win rate ≥ 55 %, average net ≥ 0, fills within ~1 % of backtest assumptions
- [ ] One sandbox run completed without errors (order ids returned)
- [ ] Upstox app: API key has order permission, static IP set if required, MIS square-off time for F&O confirmed
- [ ] Funds ≥ 1.2 × margin shown by preflight (naked straddle ≈ ₹1.5–2L; add wings if capital is ₹1L)
- [ ] `scripts/login.py` run that morning; `LIVE_TRADING=yes`; command includes `--live-i-understand`
- [ ] You are watching the log for the first 3 live expiries
- [ ] Stop live and go back to paper if 3 consecutive losses exceed −₹7k/lot each, or anything in the log says `!!!`

## 10. Status

- 27 Oct 2026: module written, 7 unit tests, paper smoke run on live quotes. Zero live or sandbox orders placed so far.
