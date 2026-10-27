# Options backtest: expiry-day straddle

Date: 26 Oct 2026. Data: Hugging Face `thetrademarkk/india-index-options-1m` (1-min, Nifty May 2021 → Aug 2026, Sensex Aug 2023 → Aug 2026), validated against NSE bhavcopy (highs/lows match to the tick on normal days; 1-min highs understate extremes on crash opens, so stop fills are slightly optimistic). Engine: `options/engine.py`, 1-min simulation, per-leg stop, charges at the Oct-2024 regime (₹20/order, STT 0.1% sell premium, exchange 0.035%, GST), 1% slippage per fill, lot sizes by date (Nifty 50→75→65, Sensex 10→20).

## Headline

Of 14 setup families × 2 indices, exactly one family is profitable after costs: **sell the ATM straddle at 9:20 on expiry day only, 25% stop per leg, square off 15:10.** Same structure on non-expiry days loses. Iron condors, strangles and iron flies on all days lose heavily (costs are 100%+ of gross).

| Nifty, 1 lot | 2021-06 → 2026-08 | 2025-01 → 2026-08 |
|---|---|---|
| Trades | 258 (1/week) | 72 |
| Win rate | 65.5% | 65% |
| Profit factor | 1.73 | 1.68 |
| Mean per trade | +₹577 (σ ₹2,550, t = 3.6) | |
| Net per month | +₹2,480 | +₹3,370 |
| Avg win / avg loss | +₹2,081 / −₹2,279 | |
| Worst day / max drawdown | −₹6,583 / −₹14,267 | |
| Positive months | 72% of 60 | |
| Worst month / best | −₹5,872 / +₹13,957 | |
| Max consecutive losing weeks | 5 | |
| Years positive | 6 of 6 (17.6k, 18.4k, 9.2k, 46.4k, 34.7k, 22.5k) | |
| Costs as % of gross | 16% | |

Sensex, same setup with 30% stop: 144 trades, 68% win rate, PF 1.57, +₹2,360/month, 2023–2025 positive, 2026 +₹6.4k. Weaker and noisier (t = 2.0).

## Robustness (Nifty, expiry day only)

| Variation | PF | Net/month |
|---|---|---|
| Stop 15 / 20 / 25 / 30 / 40 % | 1.50 / 1.71 / 1.73 / 1.68 / 1.48 | 1.8k–2.5k |
| No stop | 0.99 | ≈ 0 (worst day −₹31k) |
| Entry 9:30 / 9:45 / 10:00 / 10:30 / 11:00 | 1.13 / 1.20 / 1.38 / 1.35 / 1.27 | 0.5k–1.3k |
| Exit 15:00 / 15:20 | 1.74 / 1.73 | same |
| Slippage 2% / 3% per fill | 1.54 / 1.38 | 2.0k / 1.4k |
| + combined MTM stop ₹3,000 | 1.80 | 2.6k |
| Iron fly, wings at 2% (defined risk) | 1.46 | 1.65k, 6/6 years positive |
| Iron fly, wings at 1% | 1.29 | 1.0k |

Reads: the stop is essential, 9:20 entry is essential, exit time doesn't matter, result survives 3x the slippage assumption. The edge persisted after the Sep 2025 expiry-day move from Thursday to Tuesday (Tuesday mean ₹783/trade vs Thursday ₹460).

## What the losing days look like

All eight worst days are "both legs stopped": the index whipsaws through both stops before trending. −₹4k to −₹6.6k per lot each. No single-day blow-up because of the stops; without them the worst day is −₹31k.

4 Jun 2024 and 7 Apr 2025 were not expiry days, so this setup was flat on both. A crash landing on an expiry day has not been observed in this sample. The stop caps it near −₹7k per lot in a normal fast move, but a gap-through-stop on a limit-down open could exceed that. Iron fly with 2% wings caps the true worst case at roughly ₹30k per lot.

## Can it be daily? (tested 26 Oct 2026)

**By days-to-expiry (Nifty 9:20 straddle, 40% stop):** DTE 0 PF 1.48 (73% WR, +₹416/trade); DTE 1 PF 0.85; DTE 2 0.92; DTE 3+ 0.6–0.8. The edge is strictly expiry-day.

**Non-expiry-day ideas, all negative or marginal:** afternoon straddles (12:00/13:00/14:00) on DTE 1–6: PF 0.4–0.8. Quiet-open filter (first-15-min range < 0.3%/0.5%) on DTE 1–6: PF 0.6–0.8. Quiet-previous-day filter: PF 0.8. Best marginal: 12:00 straddle on DTE 1 only (PF 1.21, ₹433/month) and 1%-OTM strangle at 9:20 on DTE 1 (PF 1.25, ₹298/month). Too thin to trade.

**Other indices on expiry day:** BankNifty (dataset has monthly expiries only): PF 0.9, loses. Sensex: PF 1.35–1.57 overall but only +₹6.4k (30% stop) / −₹2.9k (25% stop) in 2026; since Sep 2025 Sensex is −₹9.1k over 37 trades while Nifty is +₹29.7k over 37. Sensex is marginal, Nifty is the one.

**Expiry-day OTM strangles (Nifty, 9:20, DTE 0)** confirm the family is robust across structures, not one parameter set:

| Strikes | Stop | PF | WR | Net/month | Max DD | Worst day | Years positive |
|---|---|---|---|---|---|---|---|
| ATM straddle | 25% | 1.73 | 65% | ₹2,480 | −₹14.3k | −₹6.6k | 6/6 |
| ±0.3% strangle | 30% | 1.89 | 68% | ₹1,950 | −₹11.5k | −₹6.2k | 6/6 |
| ±0.5% strangle | 30% | 1.96 | 66% | ₹1,390 | −₹9.3k | −₹5.0k | 6/6 |
| ±0.75% strangle | 30% | 2.13 | 61% | ₹930 | −₹5.9k | −₹3.0k | 6/6 |

Further OTM = less income, better drawdown. Sensex strangles: PF 1.15–1.49, 2026 negative in every variant.

**Literature check** (`research_notes/.../daily_option_strategies.md`): Zerodha's 2019–2025 Nifty study with costs found the same ordering (0 DTE consistent, 1 DTE faded after 2024, 2+ DTE duds). No cost-adjusted evidence exists anywhere for daily option strategies, option buying, re-entry, trailing stops or VIX filters.

**Practical frequency:** Nifty Tuesday, 4–5 trades/month. Sensex Thursday optional with a 30% stop. That is the realistic ceiling for this edge.

## Capital

- Naked straddle: ~₹1.5–2L SPAN+exposure per Nifty lot, +2% ELM on expiry day. Not feasible on ₹1L.
- Iron fly, wings 2%: margin ≈ wing width (≈500 pts × 65 = ₹32.5k) − credit (≈₹11k) ≈ ₹22k + ELM. Fits ₹1L at 1 lot with a 4x buffer. Expected +₹1,650/month, worst day ≈ −₹6.6k, max DD ≈ −₹14k (14% of ₹1L).
- Sizing beyond 1 lot is not advised until live slippage is measured.

## Caveats, honestly

1. Selection: ~45 configurations were examined across both indices; one family survived. Year-by-year consistency, both indices agreeing, the known 0DTE theta mechanism, and t = 3.6 make this better than noise, but out-of-sample forward testing is still required.
2. Data: minute snapshots, not ticks. Expect real stop fills 1–3% worse than modelled; the 3%-slippage row (PF 1.38) is the conservative estimate.
3. Regime: lot sizes, STT and expiry weekdays all changed inside the sample and the result held. The possible Aug-2026 closing-auction change (unverified) could move the mandatory square-off earlier; exit time doesn't affect results, so this is operational, not statistical.
4. It is one trade a week. ₹2–3k/month on one lot is the realistic expectation, not daily income.

## Files

```
options/data.py                 HF dataset access, ATM, leg price series
options/engine.py               1-min multi-leg simulator, charges, lot schedule
scripts/download_hf_options.py  dataset download (resumable)
scripts/options_research.py     14-setup grid, per-year table -> results/options_research.csv
scripts/options_expiry_robust.py robustness grid -> results/options_expiry_trades.csv
data/external/nse_bhavcopy/     6 validation days (NSE official)
```

## Scalping round (27 Oct 2026)

Scripts: `scripts/options_scalp.py` (grid), `scripts/options_scalp_robust.py`. Research: `research_notes/.../option_scalping_strategies.md` (no public India option-scalping backtest states costs; option buying has no credible positive evidence; SEBI FY25–26: ~90% of pure option buyers lose).

Tested on Nifty 1-min, 2021–26, expiry day (DTE 0) and other days (DTE 1–6), 0.25–1% slippage: short straddle windows (6 entry times × 30/60 min hold), afternoon 0DTE sells (12:00/13:00/14:00), option-buying scalps (15-min ORB → buy ATM option; 5-min momentum burst; EMA-20 pullback; 9:20 long straddle; 22 configs), ORB far-side option selling (15/60-min range), Sensex selling grid.

**Dead:** every option-buying config (PF 0.5–0.97, 26–40% win rate, −₹0.1k to −₹11k/month). Every window on non-expiry days (PF 0.1–1.0; short holds have no theta to collect and friction dominates). ORB far-side sell: PF 1.3 on Nifty 0DTE but 50% WR, 2023 −₹10k, DD −₹21k; marginal.

**Survivors (both are expiry-day selling, again):**

| Setup | PF | WR | Net/month | Max DD | Worst day | Years + |
|---|---|---|---|---|---|---|
| Nifty 0DTE 9:20 straddle, exit 10:20, SL 25% (0.5% slip) | 1.71 | 67% | ₹1,280 | −₹12.0k | −₹5.0k | 6/6 |
| … hold 45 / 90 / 120 min | 1.61 / 1.63 / 1.63 | | 955 / 1,403 / 1,501 | | | 6/6 each |
| … slippage 1% / 2% | 1.53 / 1.23 | | 1,014 / 481 | | | |
| Sensex 0DTE 12:00 straddle, exit 15:10, SL 40% (1% slip) | 1.65 | 72% | ₹1,426 | −₹8.4k | −₹5.7k | 4/4 |
| … SL 30 / 50 | 1.63 / 1.55 | | 1,455 / 1,184 | | | 4/4 |
| … entry 11:30 (SL 30–50) | 1.70–1.81 | 72% | 1,550–1,780 | −₹13.5k | −₹13.5k | 4/4 |
| … entry 12:30 / 13:00 | 0.98–1.17 / 1.03–1.66 | | ≈0 / mixed | | | 2026 negative |
| … slippage 2% | 1.47 | | 1,088 | | | |

Reads: the Nifty first hour carries about half the full-day straddle's P&L (₹1,280 vs ₹2,480/month) with 1 hour of exposure instead of 6; robust to hold 45–120 min and SL 20–30%. Adding a 12:00 Nifty re-entry (PF 1.33) gives ₹2,073/month but DD −₹21.8k, worse than simply holding the 9:20 straddle all day. Sensex noon entry is the new find: 4/4 years positive, SL-insensitive, but entry-time-sensitive (11:30–12:00 work, 12:30 doesn't) and only 144 samples, so treat as a candidate for forward testing, not proven. Nifty 12:00 entry: PF 1.33, 2026 negative.

**What this means for "scalping":** there is no intraday option-buying or short-hold scalp with an edge in this data. The only thing that looks like a scalp and works is the first 45–120 minutes of the expiry-day straddle.

## Daily strategies, round 2 (27 Oct 2026)

Scripts: `scripts/options_daily.py`, `scripts/pairs_scan.py`. Research: `research_notes/.../daily_strategies_round2.md` (no independent cost-adjusted evidence for any non-expiry-day index option/futures system exists; the only costed public results are zero or negative: QuantInsti pairs Sharpe 0.09, Marketcalls VWAP futures loses after costs, Vaasa 2025 delta-neutral straddles negative Sharpe).

| Idea (Nifty, 1 lot, with costs) | Result | Verdict |
|---|---|---|
| Overnight short straddle 15:20 → 9:20 next day, all DTE | PF 0.59, −₹6k/month | dead |
| … 1% / 2% OTM strangle | PF 0.71 / 0.66 | dead |
| … only the night before expiry (DTE 1), 1% OTM | 78% WR, PF 1.65, +₹830/month, but 2 Feb 2026 gap −₹31k in one night, 2023–24 ≈ 0 | uncapped gap risk, no |
| 9:20 straddle DTE 1–6 by India VIX bucket (<12 / 12–14 / 14–17 / 17–20 / >20) | PF 0.61 / 0.64 / 1.00 / 0.68 / 0.93 | no bucket works |
| … after VIX jump ≥ 5% / 10% | PF 0.77 / 0.92 | no |
| … premium-richness filter (straddle credit ≥ k × recent realized intraday move), k 1.5–3 | PF 0.7–0.8 (DTE 1–6); DTE 1 with k=2: PF 1.29 on 83 trades, 2021–23 negative | no |
| 0DTE straddle split by VIX > 20 / < 20 | PF 1.93 / 1.70 | expiry edge holds in both regimes |
| 30/60-min straddle windows on DTE 1–6 at 0.25% slippage | gross ≈ 0, net −₹1.7k to −₹3k/month | no theta to collect intraday |
| Equity pairs (top-15 correlated Nifty 50 pairs, z-score 5-min, 2022–26) | gross negative before costs, PF 0.1–0.3 | dead |

Overnight gap statistics (repo 1-min Nifty, 2022–Oct 2026): overnight move > 1% on 7% of nights, > 2% on 1.3%, worst −4.5% (7 Apr 2025); overnight carries 43% of daily variance. That is why the overnight carry fails: one bad night per year outweighs the theta.

Note from research: STT on option premium may have risen to 0.15% from 1 Apr 2026 (claim, unverified); the engine uses 0.1%. Effect on the expiry straddle: ≈ ₹7 per leg per trade, immaterial.

**Conclusion.** Nothing runs daily with an edge. The tradeable calendar is: Nifty Tuesday (expiry) 9:20 straddle, optionally Sensex Thursday 12:00 straddle. Two trades a week is the ceiling this data supports.
