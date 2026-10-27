# Intraday strategy test results

Date: 25 Oct 2026. Data: Upstox 5-min candles, 49 Nifty 50 stocks + Nifty index, 3 Jan 2022 to 23 Oct 2026 (~1,180 trading days, ~89k bars per stock). In-sample = 2022–2024, out-of-sample = 2025–2026.

## Verdict

**No rule-based intraday strategy on Nifty 50 stocks at 5-min resolution is profitable after Indian costs in 2022–2026.** 100 configurations across 17 strategy families were tested. Zero had a profit factor ≥ 1.0, in either sample. The best (ORB with relative-volume filter) reached 0.73 out of sample.

The reason is not the strategy choice. It is that the direction of intraday moves in large caps is unpredictable from price/volume features (every conditional edge measured sits at 0–7 bps with 47–53% hit rates), while round-trip friction is 10–18 bps. Stocks move plenty (average absolute 9:30→15:15 move is 89 bps); the sign just cannot be called.

## What was tested

Engine (`backtest/engine.py`): entry at next bar open, stop beats target when both touched in a bar (pessimistic; optimistic variant also run), gap-through fills at open, time-stop at 15:15, 5 bps slippage per side, Upstox MIS tariff (`backtest/costs.py`: ₹20/order, STT 0.025% sell, exchange 0.00307%, SEBI, stamp 0.003% buy, 18% GST), 1% of capital risked per trade, max 2 trades/day across the universe, ₹1 lakh capital.

| Family | Source | Configs | Best OOS PF | Best OOS win rate | Best OOS %/month |
|---|---|---|---|---|---|
| Opening range breakout (ORB) + RVOL / volume / stall filters | classic | 26 | 0.73 | 42% | −2.6 |
| Zarattini-Aziz ORB (first-candle direction, tight stop, hold to close) | SSRN 2023/2024 | 8 | 0.72 | 37% | −6.1 |
| Gap-and-go continuation | practitioner | 6 | 0.70 | 45% | −1.2 |
| Gap fill (fade) | practitioner | 4 | 0.62 | 38% | −5.6 |
| VWAP pullback in trend | practitioner | 4 | 0.55 | 38% | −12.0 |
| First 5-min candle break | QuantInsti/EPAT | 2 | 0.54 | 38% | −9.5 |
| Previous-day high/low break (+NR7 filter) | practitioner | 6 | 0.53 | 34% | −13.1 |
| ORB with retest entry | practitioner | 2 | 0.52 | 42% | −12.4 |
| 9/20 EMA cross | practitioner | 6 | 0.51 | 35% | −12.9 |
| RSI(2) with VWAP filter | Connors | 3 | 0.49 | 26% | −13.2 |
| Fixed % scalp (0.15–0.5%), pessimistic & optimistic fills | user's style | 10 | 0.47 | 42% | −14.9 |
| First-15-min spike fade to VWAP | practitioner | 4 | 0.47 | 26% | −13.9 |
| VWAP ±kσ band mean reversion | practitioner | 6 | 0.43 | 40% | −14.2 |
| Bollinger squeeze breakout | practitioner | 2 | 0.43 | 33% | −11.9 |
| Volume ignition bar (+RVOL stock selection) | practitioner | 3 | 0.38 | 33% | −6.9 |
| Last-30-min intraday momentum (Gao et al.) per stock | JFE 2018 | 8 | 0.31 | 30% | −6.5 |

Full tables: `results/research*.csv`, logs in `results/research*.log`.

## Diagnostics on the best strategy (ORB, 30-min range, RVOL ≥ 1.5, 1.5R)

| Scenario | Trades | Gross | Costs | Net |
|---|---|---|---|---|
| Realistic: 5 bps slippage, charges | 1,449 | −58k | 111k | −169k |
| 1 bps slippage, 2% risk (≈₹1.7L notional) | 1,449 | +76k | 155k | −79k |
| Zero slippage, 2% risk | 1,449 | +126k | 156k | −29k |
| Zero slippage, zero charges | 1,449 | +65k | 0 | +65k |
| Random direction, same stops/targets, zero friction | 1,449 | +13k | 0 | +13k |

ORB has a real but tiny directional edge: about ₹36/trade over coin-flip direction, ≈ 4–5 bps of notional. Statutory charges alone (STT + exchange + stamp + GST, ignoring brokerage) are ≈ 4 bps. Even with impossible execution (zero slippage) it only reaches break-even. Zarattini ORB and gap-and-go behave the same way (PF 0.96–0.99 at 1 bps slippage and doubled size).

Per-year ORB net was negative in every year 2022–2026. Half of all ORB trades exit on the time stop having gone nowhere.

## Feature scan (52,989 symbol-days)

Mean signed forward return (bps) when following or fading a feature, vs ~15 bps friction:

| Feature → forward window | IS | OOS |
|---|---|---|
| Follow first-15-min move (top 30%) → 9:30–15:15 | +0.2 | +0.7 |
| … and opening RVOL > 1.5 | +3.6 | +2.7 |
| Follow gap > 1% → 9:30–10:15 | −1.5 | +7.0 |
| Fade gap > 1% → 9:30–15:15 | +1.5 | −2.3 |
| Follow previous-day return (top 30%) → 9:30–15:15 | −4.2 | −5.1 |
| Follow first-30-min → last 30 min | −0.7 | +0.7 |
| Follow day-so-far sign → last 30 min | −1.3 | −0.4 |
| Cross-sectional: fade top-3 vs bottom-3 relative movers (9:30–10:15) → rest of day | −0.5 | −0.7 |
| Cross-sectional: fade biggest gap-ups vs gap-downs → rest of day | +8.3 | +5.1 (two legs, so ~2× friction) |
| Follow yesterday's last-30-min sign today | +1.4 | +1.7 |

Nifty index, Gao intraday momentum (prev close→9:45 predicting 14:45→15:15): +0.3 to +0.9 bps/day, hit 49–53%, including the high-volatility-tercile conditioning the paper relies on. The documented US effect (≈ 4.5–6.5%/yr net on SPY) is absent on Nifty 2022–2026.

## Round 2 (same day): ranking, structural effects, 1-min data, ML

Prompted by "iterate until you get one". Everything below is out-of-sample-checked.

**RVOL ranking (pick the top relative-volume stocks instead of arbitrary ones).** Added `Signal.priority`; engine now keeps the highest-priority signals per day. Zarattini ORB gross edge: +0.12R in 2022–24 → +0.02 to +0.06R in 2025–26. Decaying, not stable. ORB-best gross stays +0.05R in both samples (PF 1.18, ≈ +1.8%/month gross, ≈ 0 after charges).

**Gross-only view (no fees, no slippage), best three:**

| Strategy | Trades | Win | Avg R | Gross %/month | Max DD |
|---|---|---|---|---|---|
| Zarattini ORB, RVOL ≥ 1.5 | 2,305 | 40% | +0.13 | +4.5 | −35% |
| ORB 30-min, RVOL ≥ 1.5, 1.5R | 1,449 | 50% | +0.04 | +1.5 | −17% |
| Gap-and-go 1.5% | 632 | 48% | +0.04 | +1.3 | −15% |

Only Zarattini ORB has a meaningful gross edge, and it fades out of sample. Its +0.13R matches the paper's QQQ figure, consistent with three published replications: gross reproduces, net ≈ 0.

**Structural effects at 5-min (53k symbol-days).** Broker MIS square-off window 15:10→15:20, 15:20→15:30, conditioned on day direction: all 0–3 bps. Trend-day persistence (at day extreme by 11:00 with range > 0.8–1.2%): +3 bps IS, +0.3 bps OOS. Gaps > 3% flip sign between samples (n≈350, noise).

**1-min data (12 liquid stocks + Nifty, 14k symbol-days).** Opening-minute follow/fade, 09:16–09:17 continuation, high-volume first bar fade: 0–2 bps. Square-off minutes 15:19→15:21, 15:24→15:26, 15:26→close, forced-unwind/rebound conditioning: 0–2 bps. Opening-range "liquidity sweep" reversal (pierce ≤ 0.1%, close back inside): stop hit 80% of the time within 60 min, target 12%.

**Machine learning (gradient boosting, 14 features known at 09:30, train 2022–24, test 2025–26).** Accuracy 52%; the 2 most confident picks per day average 12 bps on the full-day target and 4 bps on the 9:30→10:15 target. Shuffled-label control: 5 bps. No conditional pocket. A first run showed 94% accuracy because one feature (price at 09:45) was measured after the 09:30 entry: look-ahead leak, caught and removed. Worth remembering: any intraday ML result above ~55% is a leak until proven otherwise.

**Structural-effects research** (`research_notes/.../structural_intraday_effects.md`). How profitable intraday players actually earn: prop/FPI desks made ₹61k cr in F&O in FY24, 96–97% via algos; HFT profit is spread capture (passive execution) minus inventory loss; a member desk pays ~3–4 bps round trip or earns the spread, retail at ₹1L pays 11–15 bps. The irreducible floor for everyone is STT (2.5 bps sell-side). So a 10 bps gross edge is break-even for us and a living for a desk. The only Indian structural effects with published evidence are multi-day, not intraday: Nifty index-inclusion effective-day pressure (≈ +1.5%, reverting over ~9 days), rebalance-day last-30-min volatility (1.5–3x), block-deal front-running (institutional). MIS square-off selloff/bounce, post-open reversal, intraday earnings drift, block-window footprint: hypotheses only, no Indian data, and our own scans put them at 0–3 bps.

*Unverified regime note:* the researcher reports NSE moved Nifty 50 stocks to a closing auction (15:15–15:35) from 3 Aug 2026 with Upstox MIS square-off at 15:05 for those stocks, revised again from 7 Dec 2026. Our Upstox candles still show a 15:25 last bar through Oct 2026, so this is not confirmed by data. Check Upstox's current MIS square-off time before any live or paper run; the engine's 15:15 time-stop may need to move earlier.

**Cumulative count:** ~100 strategy configs + ~60 feature/structural tests + ML. Nothing beats friction out of sample.

## What the literature said, and whether it matched

- SEBI: 71% of intraday equity traders lose; 80% of those trading >500 times/yr; costs are 57% of loss-makers' losses. Matches: costs are the dominant term in every run here.
- Zarattini-Aziz ORB: gross edge reproduces in three independent replications, net ≈ 0 after costs. Matches exactly: gross +, net −.
- Gao et al. intraday momentum: index-level, strongest in high-vol opens. Not present on Nifty in this period.
- VWAP, EMA cross, NR7, Bollinger squeeze, PDH/PDL, RSI(2), gap fill: no rigorous after-cost evidence anywhere; the two NSE cost-inclusive datapoints found (marketcalls VWAP on Nifty futures, Streak 9/21 EMA on Nifty 50 stocks) were negative. Matches.
- No verified Indian retail algo track record at 15–20%/month exists. SEBI's Asmita Patel case: claimed 300%, actual ₹12.3L profit.

Notes: `research_notes/AI intraday trading India feasibility/` (7 files), earlier report `reports/AI intraday trading India feasibility.md`.

## Why the ₹1/share scalp cannot work

On a ₹700 stock, ₹1 = 14 bps. Statutory charges ≈ 4 bps, brokerage 1–5 bps depending on size, spread + slippage 2–10 bps. Friction is 7–19 bps against a 14 bps target with a comparable stop. At 50% hit rate that is a guaranteed loss; it needs >65–70% hit rate just to break even, and nothing in the data provides a directional edge of that size at any horizon.

## What could still work (honest options)

1. **Reduce friction, accept break-even at best.** Limit-order entries at the level (ORB retest, gap fill) instead of market, larger notional so brokerage → ~1 bp, 1 trade/day. Gets ORB to PF ≈ 1.0. Not an income.
2. **Information that is not in OHLCV.** Earnings/news/event-driven entries, order-book imbalance, options-flow signals. Requires tick/news data we do not have; untested.
3. **Longer holding period.** Overnight and multi-day effects (momentum, post-earnings drift, gap-day reversal next day) are where documented, replicated edges exist. The engine works unchanged on daily bars. Rejected earlier by preference; this is the single largest lever.
4. **ML as a filter.** Nothing to filter: when the base signal is 0–5 bps, a filter cannot create the missing 10 bps.
5. **Paper trade ORB-best at minimum size for 20 days solely to measure real slippage.** Cheap, and tells us whether the 5 bps assumption is too harsh. Does not change the conclusion unless real slippage is ~0.

## Repo

```
scripts/download.py     refresh candles (Analytics token, 1-yr validity)
scripts/backtest.py     single strategy run with report
scripts/research.py     grids: --set base|patterns|practitioner|za  [--slip N --risk N]
scripts/scan.py         feature scan over symbol-days (5-min)
scripts/scan_1min.py    opening-minute / square-off / liquidity-sweep scan (1-min)
scripts/ml_scan.py      gradient-boosting conditional-edge test (IS/OOS, shuffled control)
strategy/               orb, za_orb, gap, vwap, fade, scalp, patterns (6), practitioner (4); Signal.priority ranks picks
backtest/               costs, engine, report
tests/                  12 unit tests (pytest)
results/                research*.csv/log, scan.parquet, orb_trades.csv
```

## Spike-fade scalp (27 Oct 2026)

Jithin's discretionary style: a volatile, active stock runs up sharply → short near the end of the run → cover on a small pullback (≈ ₹1 on a ₹600 stock, 1000 qty); mirror for sharp drops. Script `scripts/spike_fade.py`, 1-min data, 12 Nifty 50 stocks (AXISBANK, BAJFINANCE, HDFCBANK, HDFCLIFE, ICICIBANK, INFY, KOTAKBANK, LT, RELIANCE, SBIN, TATASTEEL, TCS), Jan 2022 – Oct 2026, notional ₹6L per trade.

Rules: run = move ≥ 0.5–1.5% over the last 5–30 min; exhaustion = bar closes in the lower half of its range + climax volume ≥ 2× 20-bar average; entry next bar open against the run; target 0.15–0.4%, stop 0.3–0.6%, time stop 15–60 min; ≤ 3 trades/stock/day. 25 variants.

| Variant | Trades | Win rate | Gross/trade | Net/trade | Net ₹/month (₹6L) |
|---|---|---|---|---|---|
| run 10 min ≥ 0.75%, target 0.2%, stop 0.4% (base) | 2,164 | 63% | −0.7 bps | −9.0 bps | −₹20k |
| target 0.15%, stop 0.3% | 2,273 | 65% | −0.6 bps | −8.9 bps | −₹21k |
| tiny target 0.15%, wide stop 0.5% | 727 | 72% | −2.1 bps | −10.4 bps | −₹8k |
| fade any run, no stall/volume filter | 4,427 | 65% | +0.5 bps | −7.8 bps | −₹36k |
| **first 45 min only (9:16–10:00)** | 351 | 67% | **+1.4 bps** | −6.9 bps | −₹2.8k |
| midday only (11:00–14:30) | 1,258 | 61% | −2.2 bps | −10.5 bps | −₹14k |
| optimistic fill rule (target wins ties) | 2,164 | 64% | −0.6 bps | −8.9 bps | −₹20k |

By hour (base): 9–11 h gross +1.1 to +1.5 bps, 12–13 h −4 to −7 bps. By symbol: HDFCBANK +5 bps, LT +2.4, TCS +2.2 gross; HDFCLIFE −4.2, ICICIBANK −3.8. By side: shorts −1.2 bps, longs −0.2 bps. By year: 2022 −2.8, 2023–25 +0.7 to +1.1, 2026 −1.8 bps gross.

Reads: the win rate is real (60–72%), which is why the style feels good, but the maths is 65% × +0.2% − 35% × −0.4% ≈ 0. Gross expectancy is zero to +1.5 bps per trade in the best slice (opening 45 min); the round trip costs 4.3 bps plus slippage. Every variant is negative after costs. This is the same picture as every other equity scalp tested: no gross edge large enough to pay the friction.

Research (`research_notes/.../spike_fade_scalping.md`): no cost-adjusted evidence anywhere for a spike-fade/climax short on NSE stocks; practitioner rule-sets (TradeZella/Qullamaggie) are unmeasured claims and themselves say "no fades in the first 30 min" and expect 35–45% win rates at 1.5–5R targets, i.e. the opposite shape of a ₹1 scalp. Academic intraday-reversal effects (Brogaard et al., Baltussen et al.) are gross-only, concentrated in the last 30 min and in buying intraday losers, and the authors judge them unexploitable after costs. SEBI FY23: 71% of intraday cash traders lose, 80% among those doing > 500 trades/year, with costs = 57% of losers' losses. Structural: cash shorts are MIS-only (forced cover by 15:20), F&O stocks have 10% dynamic bands, non-F&O names at upper circuit leave shorts uncoverable, ASM/GSM/T2T names must be excluded daily. Equity STT unchanged by the Apr-2026 budget. Verdict unchanged.
