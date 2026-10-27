# Stock Selector: AI-assisted intraday equity on Upstox

Status: backtesting done, verdict negative (25 Oct 2026). See `reports/Intraday strategy test results.md`. Full research: `reports/AI intraday trading India feasibility.md`, notes in `research_notes/`.

## Goal

Automated intraday equity trading on NSE via Upstox API, starting with ₹1 lakh, targeting small consistent daily gains. Original target ₹1,000/day (1%/day).

## Decisions so far

- **Equity intraday only.** No F&O: option selling needs ₹1.5–2.5L margin/lot, option buying is a lottery at this size. Swing rejected by preference.
- **Target reset.** 1%/day has no verified track record anywhere (Medallion ~0.2%/day gross). Research-backed realistic range for a good retail system: 2–5%/month, 15–30% drawdowns. Treat ₹1k/day as aspirational, not the success criterion.
- **AI role.** ML is a filter, not an alpha source. Use it for regime detection (trend vs chop), trade filtering (meta-labeling), volatility-based sizing on top of a rule-based strategy. Do not train a model to predict direction from OHLCV.
- **Scalping out.** Costs ~₹83 round-trip at ₹1L notional + spread; HFT prop desks own that space.

## Cost reality (Upstox, 2026)

- ₹20/order brokerage, STT 0.025% sell side, exchange 0.00307%, SEBI ₹10/cr, stamp 0.003% buy, 18% GST.
- Round-trip ≈ ₹83 on ₹1L notional, ≈ ₹225 on ₹5L (5x MIS). Add ~5 bps/side slippage.
- 3 round-trips/day at 5x ≈ ₹2,174/day friction. Fewer, bigger-conviction trades only.

## Pipeline

1. **Backtest (offline).** Upstox V3 historical candles (1-min to 300-min, from Jan 2022, free with live token) → pandas/vectorbt simulator with full cost model + slippage. Must cover shock days: 4 Jun 2024, 5 Aug 2024, 7 Apr 2025.
2. **Validate.** Walk-forward / purged CV, deflated Sharpe, random-skip control for any ML filter, locked holdout scored once.
3. **Paper trade (forward).** Same engine, `SimBroker` fed live Upstox WebSocket ticks instead of parquet. Fills at LTP + slippage, position book, MTM, 5x MIS, 15:15 time-stop, virtual capital ₹1L. Minimum 60 trading days. Expect live to be 15–30% worse.
4. **Live.** Swap `SimBroker` → `UpstoxBroker`. Same strategy code. Start at minimum size, 20% drawdown kill switch.

## Tooling

| Need | Tool |
|---|---|
| Execution + paper trading | Own `Broker` interface: `SimBroker` (backtest + paper) / `UpstoxBroker` (live). OpenAlgo deferred; only if dashboard/multi-broker needed |
| Historical data | Upstox V3 candles API (free) |
| Backtest engine | vectorbt / pandas (marketcalls NSE fork) |
| Order payload test only | Upstox sandbox (order place/modify/cancel only; no positions, no data, no fills) |
| Broker SDK | upstox-python-sdk |

## Upstox API gotchas

- Two tokens: **Analytics token** (My Apps → Analytics) is read-only, valid 1 year, covers historical + market data + WebSocket. Use it for download/backtest/paper. **Trading token** (OAuth, `scripts/login.py`) expires daily ~3:30 AM; only needed for live orders.
- Static IP mandatory for order endpoints (primary + secondary, change once/week). One API app per user.
- Rate limits: 10 orders/sec, 500/min, 2000/30-min. ≤10 OPS needs no SEBI algo registration (generic algo ID auto-tagged).
- No bracket/cover orders in V3. Market orders go through MPP by default since 1 Apr 2026.
- MIS auto square-off 3:25 PM (3:10 PM for some stocks), ₹59–88 charge if broker squares off.
- Sandbox token valid 30 days, separate app.

## Strategy candidates (to backtest)

- Opening range breakout (ORB) on liquid large caps / Nifty 50 constituents, with regime filter.
- VWAP mean reversion / VWAP trend on Nifty 50 names.
- Gap-and-go momentum on top gainers at open.
- Each: 1–3 trades/day max, fixed % risk per trade, hard stop, time stop before 3:15.

## Compliance and tax

- Self-coded algo ≤10 orders/sec: no exchange registration. Static IP + 2FA required.
- Intraday equity profit = speculative business income, slab rate, ITR-3, losses only vs speculative gains (4-yr carry-forward). Advance tax applies.
- Keep a trade log (5-year audit trail expectation).

## Old repo (reviewed 25 Oct 2026)

Cloned `jithinolickal/stock-selector`. It is a stock screener (swing + scalping picks), not a trading system: no orders, no risk mgmt, no cost model, no backtester. Depends on abandoned `pandas-ta`. Decision: rewrite from scratch, keep Nifty 50 list + Upstox V3 endpoint knowledge, move old code to `legacy/`.

## Target layout

```
data/      upstox.py (auth, candles → parquet), instruments.py
strategy/  base.py (on_bar → signal), orb.py
backtest/  costs.py, engine.py, report.py
broker/    sim.py (backtest + paper), upstox.py (live)
config.py, scripts/download.py, scripts/backtest.py
```

Same `Strategy.on_bar()` runs in backtest, paper and live.

## Testing levels

| Level | Market hours? | Data | Proves |
|---|---|---|---|
| Unit tests (engine, costs, strategy) | No | Synthetic candles | Code correct |
| Backtest | No | Parquet 2022→now | Edge after costs, historically |
| Replay | No | Historic candles streamed bar-by-bar through the live path | Live code path works |
| Paper | Yes | Live WebSocket, SimBroker | Edge on unseen data |
| Live | Yes | Real orders | Real money |

Downloading candles uses the 1-year Analytics token and can run any day.

## Results so far (25 Oct 2026)

- Rewrite done on `feat/rewrite`; 5-min data for 49 stocks + Nifty, Jan 2022 → Oct 2026, downloaded.
- 100 configs / 17 strategy families backtested with full cost model. **None profitable** (best OOS PF 0.73). ORB has a ~5 bps gross edge; friction is 10–18 bps. Feature scan finds no directional signal > 7 bps anywhere.
- Fixed ₹1/share scalping is structurally negative: target ≈ friction.
- Round 2: RVOL ranking, structural close/open effects (5-min and 1-min), liquidity sweeps, gradient-boosting over 14 features: all 0–12 bps OOS, same as shuffled-label control. Zarattini ORB's gross edge decays OOS.
- Details and options: `reports/Intraday strategy test results.md`.
- Unverified: NSE closing-auction change (Aug 2026) may have moved Upstox MIS square-off to 15:05 for Nifty 50 stocks. Verify before paper/live.
- Spike-fade scalp (27 Oct 2026, Jithin's old style): 60–72% win rate but gross ≈ 0 (best slice +1.4 bps, opening 45 min), net −7 to −10 bps per trade on 12 stocks × 1-min × 2022–26. No costed evidence in literature either. Equity scalping stays closed.

## Options (26 Oct 2026)

- Free 1-min options data (Hugging Face `thetrademarkk/india-index-options-1m`, Nifty 2021→2026, Sensex 2023→2026) downloaded to `data/external/hf_options/`, validated vs NSE bhavcopy.
- 14 setups × 2 indices: only **expiry-day 9:20 ATM straddle, 25% stop/leg** is profitable after costs. Nifty: 258 trades, 65% WR, PF 1.73, +₹2,480/month/lot, 6/6 years positive, max DD −₹14k, t=3.6. Defined-risk iron fly (2% wings): PF 1.46, +₹1,650/month, fits ₹1L margin.
- Everything else (condors, strangles, all-day straddles, iron flies on all days) loses; costs 100%+ of gross.
- Daily? No. Edge is strictly DTE 0 (DTE 1 PF 0.85, DTE 2+ 0.6–0.9). Afternoon/quiet-open/quiet-prev-day filters don't rescue non-expiry days. BankNifty monthly expiry loses. Sensex Thursday marginal (2026 negative). Nifty 0DTE strangles ±0.3–0.75% all PF 1.9–2.1, 6/6 years, smaller DD. Realistic frequency: Nifty Tuesday, 4–5 trades/month.
- Report: `reports/Options expiry straddle results.md`.

- Scalping (27 Oct 2026): 22 option-buying configs, 30-/60-min straddle windows, ORB far-side selling all tested — nothing works on non-expiry days, no buying setup is positive. Two expiry-day scalp variants survive: Nifty 9:20 straddle exit 10:20 (PF 1.71, 67% WR, ₹1.3k/month, 6/6 years, half the full-day P&L in 1 hour) and Sensex 12:00 straddle SL 40% (PF 1.65, 72% WR, ₹1.4k/month, 4/4 years, 144 samples, entry-time sensitive). Paper trader built: `scripts/paper_expiry.py` (replay + live, no orders).

- Daily round 2 (27 Oct 2026): overnight straddle/strangle (all DTE, DTE-1 only), VIX-level and VIX-jump filters, premium-richness filter, equity pairs trading — all negative or gap-exposed (DTE-1 overnight: 78% WR but −₹31k single night). No daily edge exists; calendar is Nifty Tue + optional Sensex Thu.

## Live module (27 Oct 2026)

`live/` holds the only order-capable code: `live/broker.py` (paper / sandbox / live backends, guarded), `live/straddle.py` (runner with guards, resume, kill file, reconcile), `live/README.md` (every rule, why, safeguards, go-live checklist). Daily order token = `UPSTOX_TRADE_TOKEN` via `scripts/login.py`; data token untouched. Paper smoke run on live quotes passed. Zero live/sandbox orders placed. Lot sizes come from the contract API at runtime (Oct 2026: Nifty 65, Sensex 20, BankNifty 30).

Expiry calendar (from Upstox contract list, Oct 2026): Nifty weekly Tuesday; Sensex weekly Thursday; BankNifty, FinNifty, MidcpNifty monthly (last Tuesday); Bankex monthly (last Thursday). Only Nifty and Sensex have weekly expiries. Holiday shifts expiry to the previous trading day (e.g. Mon 9 Nov, Mon 23 Nov 2026).

## Next steps (decision needed)

1. Equity intraday: closed. No edge after costs.
2. Options forward test: run `python -m live.straddle` (paper) every Nifty expiry; 8–12 rows in `results/live/trades.csv`, compare to backtest (WR ≥ 55%, avg net ≥ 0). Optional: Sensex Thursday `--entry 12:00 --sl 40` as a second paper stream.
3. Before live: sandbox run once; confirm static-IP requirement and F&O MIS square-off time in the Upstox app; add iron-fly wings to the runner if capital is ₹1L (naked straddle needs ~₹1.5–2L).
