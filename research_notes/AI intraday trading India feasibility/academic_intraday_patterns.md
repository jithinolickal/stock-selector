# Academic / Backtested Intraday Return Patterns Implementable on 5-min OHLCV (India first, then US/China/Europe)

Scope note: all NSE times below are IST, cash session 09:15–15:30 (75 five-minute bars). "First half-hour" on NSE = bars 09:15–09:45; "last half-hour" = 15:00–15:30; "second-to-last half-hour" = 14:30–15:00. US-paper times are translated to NSE in the Inferences subsections; the translation is my mapping, not something any paper tested.

Source-access note: ResearchGate, SSRN, ScienceDirect, Sage, Alpha Architect and Quantpedia all returned 403/captcha during this research, so several claims rely on (a) full-text PDFs I downloaded directly (Gao et al. 2018 working paper, Zarattini & Aziz 2023, Heston-Korajczyk-Sadka 2010, Baltussen et al. 2021, MPRA Nifty-futures paper, IIMA Agarwalla-Pandey 2012) and (b) search-snippet abstracts for the rest. Where only a snippet was available I say so.

---

## Q1. Market intraday momentum (Gao, Han, Li, Zhou 2018 JFE): exact rule, results, Indian replication, index vs single stock

### Takeaway
Robust, peer-reviewed, out-of-sample and cost-adjusted at the index-ETF level in the US (Sharpe ~1.08 gross, ~0.7–1.0 net on SPY; effect concentrated on high-volatility / high-volume days). The only Indian replication found (Motwani, Burrin, Sharma 2024, ResearchGate preprint, full text inaccessible) reports "strong intraday momentum towards the last half hour" on NIFTY 50 and 44 liquid stocks but says Indian features "necessitate tailored approaches"; no numbers were retrievable. The original paper does NOT test single stocks; HKS (Q2) show single-stock half-hour effects are a different, cost-negative phenomenon.

### Cited Findings
- Definition: first half-hour return r1 = price at 10:00 ET / previous day's close − 1 (i.e., it INCLUDES the overnight gap); then 12 further 30-min returns to 16:00 ET, 13 per day. r13 = last half-hour (15:30–16:00) return — [Gao, Han, Li, Zhou working paper PDF, Sec. 2](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf)
- Regression r13 on r1 (SPY): scaled slope 6.94, in-sample R² 1.6%; r12 (second-to-last half-hour) also predicts r13 with R² 1.1%; r1 + r12 jointly R² 2.6%; of the 12 intraday half-hours only r1 and r12 predict r13 across all 11 ETFs tested (r1 significant at 1% for all 11) — [same PDF](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf)
- Published version: JFE 2018, SPY 1993–2013; predictability stronger on volatile days, high-volume days, recession days, macro-news days; also holds for ten other heavily traded ETFs — [SSRN abstract page](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2440866); [JFE listing](https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301351)
- Timing rule (exact): at start of last half-hour go long if r1 > 0, short if r1 ≤ 0, close at market close. Variant η(r1,r12): long only if r1>0 AND r12>0, short only if both ≤0, else flat — [working paper PDF, eq. 4–5](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf)
- Gross results (working paper sample, SPY): η(r1) 6.67%/yr, std 6.19%, Sharpe 1.08, skew +0.90, success rate 54.37% vs Always-Long-last-half-hour −1.11%/yr (Sharpe −0.18) and Random Timing −0.68%/yr. η(r1,r12): 4.39%/yr but success rate 77.05% (fewer days traded); excluding non-trading days 8.85%/yr, Sharpe 1.39. η(r12) alone: 1.77%/yr, Sharpe 0.29 — [working paper PDF, Table 4](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf)
- Volatility conditioning (OOS, terciles of first-half-hour realized vol): η(r1) return 0.54%/yr (t=0.43) low-vol, 4.75% (t=2.27) mid, 14.73% (t=3.80) high; Sharpe 0.18 → 0.97 → 1.63. Volume terciles (first-half-hour volume, detrended by year): 1.67% (t=0.98) → 6.46% (t=3.03) → 11.87% (t=3.23); Sharpe 0.42 → 1.29 → 1.38 — [working paper PDF, Table 5](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf)
- Transaction costs: measured by entering at 15:30 ask (long) / bid (short) from TAQ, exiting at the 16:00 closing print (no spread); commissions ignored. Post-decimalization (Jul 2001+): η(r1) falls from ~6.9% to 4.46%/yr (−2.47 pp), std unchanged 6.10%; post-2005 (spread ~1.2 bp): 7.96% gross → 6.52% net; η(r1,r12) 5.50% → 4.74% net — [working paper PDF, Sec. 5.2, Table 10](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf)
- Independent check (CXO Advisory, Aug 2012–May 2014, 441 days): correlation r1–r13 = 0.12, R² 0.014; effect driven by extreme first-half-hour moves; author judges the last-half-hour moves "too small for most investors to exploit once trading frictions are considered"; flags data-snooping from testing many segment combinations — [CXO Advisory](https://www.cxoadvisory.com/?p=25481)
- Index vs stock: the paper explicitly studies "time-series momentum of the market" and contrasts with cross-sectional stock momentum; evidence limited to indices/ETFs — [working paper PDF, fn 2 and fn 10](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf); [Harbourfront commentary](https://harbourfrontquant.substack.com/p/does-intraday-momentum-exist-in-stock)
- Indian replication: "Hedging Demand and Intraday Momentum within the Indian Stock Market" — Adarsh Motwani (EADA), Sam Burrin (Durham), Aanjaneya Sharma (Oxford), Aug 2024, ResearchGate preprint (not peer-reviewed). Per abstract/snippets: adapts Baltussen et al. framework; regressions + Net Gamma Exposure signals; analyses NIFTY 50 and 44 liquid stock symbols; test window described as "second last half hour" 14:30–15:00; finds "strong intraday momentum towards the last half hour" and that some elements translate to India but "unique market features necessitate tailored approaches" — [ResearchGate listing](https://www.researchgate.net/publication/383567351_Hedging_Demand_and_Intraday_Momentum_within_the_Indian_Stock_Market) (full text blocked by captcha; numbers unverified)
- Second Indian item (weak): Scribd document "Intraday Momentum Trading Strategies in India" — 30-min data on Indian stocks, six-month sample, says first/last half-hour returns depend on prior-day return and same-day first-half-hour return; momentum strategies "outperformed the index", best on high-vol/high-volume days. No author, venue, costs, or statistics — [Scribd](https://www.scribd.com/document/670520471/MomentumTrading)
- Developed-market replication (16 developed markets, India not included): ITSM "economically sizable and statistically significant both in- and out-of-sample in most countries", stronger when liquidity low, volatility high, information discrete; US first-half-hour return also predicts other markets' last half-hour — [Li, Sakkas, Urquhart, J. Financial Markets 2022](https://ideas.repec.org/a/eee/finmar/v57y2022ics138641812100001x.html)
- China: Yang (2022, China Finance Review International) CSI 300 2012–2017 finds a last-hour pattern (6th/7th half-hour predicts next), stronger on high-vol/high-volume/high-order-imbalance days — [Emerald](https://emerald.com/insight/content/doi/10.1108/CFRI-06-2021-0106/full/pdf)
- Global futures version (Baltussen, Da, Lammers, Martens, JFE 2021): >60 futures 1974–2020; "rest-of-day" return (prev close → 30 min before close) predicts last-30-min return better than the first-half-hour return; equity-index-futures 1/N portfolio: η(rROD) 6.86%/yr, std 3.96%, Sharpe 1.73, success 0.55; η(rONFH) 4.21%/yr, Sharpe 1.07, success 0.55; η(rONFH,rROD) 5.47%, Sharpe 1.60, success 0.61; Always-Long 0.44%, Sharpe 0.11. No transaction costs; authors say S&P futures stay positive net at 1-tick cost. Effect reverts over next days. Futures list contains no Indian contract — [Baltussen et al. PDF, Table 6, Sec. 4](https://www3.nd.edu/~zda/intramom.pdf)

### Inferences
- NSE translation of the Gao rule for a 5-min engine: r1 = close of 09:40–09:45 bar / previous day close − 1 (includes gap); r12 = close of 14:55–15:00 bar / close of 14:25–14:30 bar − 1; signal at 15:00; enter at open of the 15:00–15:05 bar; exit at close of 15:25–15:30 bar (or at the 15:30 closing price if the data vendor provides it). Baltussen variant: rROD = close of 14:55–15:00 bar / previous close − 1.
- Indian evidence is a single non-peer-reviewed preprint with no retrievable statistics, so the NSE result must be treated as untested until backtested; note the Indian authors chose 14:30–15:00 rather than 15:00–15:30, which may reflect NSE's closing-price mechanism (close = VWAP of last 30 min, per IIMA paper in Q4) — a backtest should try both windows.
- Costs: the US net results assume ~1–2 bp spreads; NSE large-cap spreads plus STT/stamp/exchange charges are an order of magnitude larger per round trip, so the 1–2 pp/yr US cost drag is not transferable. Gating on high first-half-hour realized vol / volume (top tercile) is the documented way to raise per-trade edge above costs.
- Single-stock application is not supported by any cited paper; index-level only (Nifty futures / Nifty ETF). For single stocks the relevant literature is Q2 and is cost-negative.

### Gaps
- Motwani/Burrin/Sharma full results (coefficients, Sharpe, costs) not retrievable; no SSRN/journal version found.
- No peer-reviewed Indian replication in FRL, PBFJ, or IIM working-paper series was found via search; may exist but not surfaced.
- Li-Sakkas-Urquhart market list and net-of-cost numbers unavailable (paywalled).
- Indian statutory intraday costs (STT, exchange, stamp duty, brokerage) were not sourced in this research; the implementer must supply them.

---

## Q2. Intraday cross-sectional patterns (Heston, Korajczyk, Sadka 2010 JF): half-hour periodicity, first-30-min winner/loser reversal, Indian evidence

### Takeaway
HKS document (a) a robust same-half-hour-next-day continuation (~3 bp per half-hour, t≈22) and (b) within-day reversal at non-daily lags, but their own cost-adjusted test shows BOTH long-short strategies lose money after spreads in every size group. No Indian replication found; a 2024 replication finds the pattern in UK and Brazil but weak in China.

### Cited Findings
- Sample: all NYSE-listed common stocks (1,715 firms) Jan 2001–Dec 2005, TAQ half-hour returns, 13 intervals/day, overnight excluded — [HKS PDF, Sec. I.A](https://www.bauer.uh.edu/departments/finance/documents/Heston_Korajczyk_Sadka_paper_UH.pdf)
- Portfolio rule: every half-hour, sort stocks into equal-weighted deciles on their return k half-hours ago; "10−1" = long top decile, short bottom decile, held for that half-hour — [HKS PDF, Sec. I.B](https://www.bauer.uh.edu/departments/finance/documents/Heston_Korajczyk_Sadka_paper_UH.pdf)
- Lag 13 (same half-hour yesterday): winners-minus-losers 3.01 bp per half-hour, t=22; daily winners earn 1.66 bp, daily losers lose 1.35 bp per half-hour; spreads stay >1 bp/half-hour out to lag 5 days (t>8.7) and effect lasts ≥40 trading days — [HKS PDF, Table II text](https://www.bauer.uh.edu/departments/finance/documents/Heston_Korajczyk_Sadka_paper_UH.pdf)
- Non-daily lags (within-day reversal): worst non-daily losers over previous day earn 3.16 bp, best winners lose 1.51 bp per half-hour; reversal driven by bid-ask bounce and liquidity imbalances resolving in <60 minutes — [HKS PDF](https://www.bauer.uh.edu/departments/finance/documents/Heston_Korajczyk_Sadka_paper_UH.pdf)
- Daily-frequency continuation strongest in first and last half-hour of the day — [Kellogg abstract](https://www.kellogg.northwestern.edu/academics-research/research/detail/2010/intraday-patterns-in-the-cross-section-of-stock-returns)
- After transaction costs (Table VII, stocks with quoted relative spread ≤10 bp): returns "negative for all size categories at all times of the day, indicating that the periodicity we find does not indicate a pure profit opportunity"; e.g., small stocks: Day-1 nondaily strategy −25.03 bp, Day-1 daily strategy −23.78 bp (four transactions per round trip). Authors frame the use as timing already-planned trades to save roughly the effective spread — [HKS PDF, Sec. III/Table VII](https://www.bauer.uh.edu/departments/finance/documents/Heston_Korajczyk_Sadka_paper_UH.pdf)
- International replication: Chen, Haboub, Khan, Mahmud (Review of Quantitative Finance and Accounting 2024) find HKS periodicity in UK and Brazil, weak evidence in China — [search result summary; Aston repository](https://publications.aston.ac.uk/id/eprint/46518)
- Persistence: Haendler, Heston, Korajczyk, Sadka (SSRN 2025) report patterns persist out of sample; institutional-trading proxies explain most open/mid-day periodicity — [Kellogg listing](https://www.kellogg.northwestern.edu/academics-research/research/detail/2025/the-intra-day-stock-return-periodicity-puzzle/?p=1)
- Related Indian cross-sectional paper (daily horizon, not half-hour): Siddiqui & Misra, Journal of Asset Management 26(5) 2025, "Intraday overreaction and underreaction": a speed-of-price-adjustment factor long intraday-overreaction / short intraday-underreaction stocks earns a premium not explained by market/size/value/momentum/illiquidity; no numbers, universe or period on the public page — [IDEAS/RePEc](https://ideas.repec.org/a/pal/assmgt/v26y2025i5d10.1057_s41260-025-00418-y.html)

### Inferences
- The gross edge (~3 bp per half-hour, ~1.5 bp per leg) is below any plausible NSE round-trip cost for a retail account; this pattern is useful only as an execution-timing overlay (e.g., if you must buy stock X today, buy it in the half-hour where it was weakest yesterday), not as a standalone strategy.
- A "fade the first-30-min winners/losers" single-stock rule has HKS-type support only at the within-day non-daily lags (reversal ~3 bp/half-hour gross), which HKS attribute largely to bid-ask bounce — i.e., not capturable with market orders.
- No Indian half-hour cross-sectional study exists in the sources found; Siddiqui & Misra is the closest but is a daily-rebalanced factor.

### Gaps
- No NSE replication of HKS found. 
- Chen et al. 2024 details (sample, costs) only from snippet.
- Siddiqui & Misra numeric results paywalled.

---

## Q3. Overnight gap behaviour in Indian large caps: fill vs continuation, which sizes revert, published NSE statistics

### Takeaway
No peer-reviewed NSE study of stock-level gap fills was found. The only transparent Indian dataset is a blog backtest of Nifty-index gaps ≥1% (2016–2026, n=85 up / 76 down): same-day fill rate only ~29% (up) / ~17% (down), but the index closed below the open 55% of the time after gap-ups, i.e., partial reversal is common while full fills are not. Widely quoted "70% of gaps fill" claims are unsourced. US futures evidence (2021–2025, MNQ) finds gap-fade signals too small to cover costs.

### Cited Findings
- Nifty 50 index, Jan 2016–Mar 2026, 2,532 sessions, daily OHLC: gap-up defined as open ≥ +1% vs prior close (85 events, 3.4% of sessions); "fill" = session low ≤ prior close. Same-day fill 25/85 = 29.4%; closed below open 55.3%; mean open-to-close −0.25%. By size: 1–1.5% (n=56) fill 30.4%, bearish close 55.4%, mean −0.32%; 1.5–2% (n=13) fill 30.8%, bullish close 53.8%, mean +0.08%; >2% (n=16) fill 25.0%, bearish close 62.5%, mean −0.29%. 2020 had 31 of the 85 events (mean −0.72%); all other years mean +0.02%, 48.1% bullish close. Monday gap-ups (n=24): 58.3% bullish close. Gap-downs ≤ −1% (n=76): closed green 52.6%, fill rate 17.1% — [IntradayLab blog](https://intradaylab.com/blog/nifty-gap-up-history-analysis)
- Forum statistic (unverified): Nifty gaps >0.8% filled same day 44% (up) / 24% (down) — [TradingQnA thread](https://tradingqna.com/t/gap-filling-statistics/151053)
- Education-site figures (~65–75% fill for 0.3–0.6% gaps, 25–40% for >1.2%) are explicitly "illustrative" — [OneTradeJournal](https://onetradejournal.com/strategies/gap-fill-strategy); a "70% of all Nifty gaps fill same session" claim has no source — [ArthaLearn](https://www.arthalearn.com/learn/gap-trading)
- US micro-futures falsification study (MNQ, 947 days of 5-min bars 2021–2025, walk-forward OOS 2023/24/25, friction floor 2.0 pts/trade): 14 OHLCV signal families, none passed; "gap continuation (short)" had gross +16.53 pts, T=1.46 but failed year-stability and sample-size; 11 families had gross 0.07–1.50 pts, below friction — [arXiv 2605.04004](https://arxiv.org/abs/2605.04004)
- US single-stock price-gap anomaly literature exists (Plastun et al., "Price gap anomaly in the US stock market: the whole story") but was not fetched — [ResearchGate listing](https://www.researchgate.net/publication/339811620_Price_gap_anomaly_in_the_US_stock_market_The_whole_story)
- Index-level context: SENSEX cumulative return 1990–2021 is almost entirely overnight; intraday-only returns lost nearly all capital — [Knuteson arXiv 2201.00223](https://arxiv.org/pdf/2201.00223)

### Inferences
- For Nifty ≥1% gaps, a "fade to full fill" target is hit <30% of the time; a "fade to a partial retrace with EOD exit" captured a negative mean open-to-close only in 2020; ex-2020 the expectancy is ~0. Any gap-fade rule for 2022–2026 must therefore be tested with 2020 excluded as a robustness check.
- No stock-level Indian statistics exist; the implementer should compute fill/continuation rates per gap bucket on the 2022–2026 Nifty-50 constituents themselves before trading.
- Candidate rule for backtest (not evidence-backed in India): gap = open(09:15 bar)/prev close − 1; if |gap| ≥ 1% and the first 5-min bar closes back toward prior close, fade toward prior close with stop at the 09:15–09:20 bar extreme, exit at fill or 15:15. This is a hypothesis to test, not a documented edge.

### Gaps
- No published NSE stock-level gap-fill or gap-continuation statistics found.
- Plastun et al. US gap results not extracted.
- IntradayLab gap-down methodology page not retrieved.

---

## Q4. Time-of-day effects on NSE: volatility/volume peaks, trend persistence windows, first-15-minutes, U-shape papers

### Takeaway
Multiple NSE studies confirm a U / reverse-J intraday volatility pattern: highest 09:15–10:00 (and especially the first 15–30 min), lowest 11:00–12:00, rising again 14:00–15:30, with the last half-hour elevated on derivatives-expiry days because NSE's closing price is the last-30-min VWAP. No NSE study tests whether trends "persist" in the last hour or whether the first 15 minutes is net negative for breakout traders.

### Cited Findings
- Nifty futures, 1-min data Jan 2011–Aug 2018 (MPRA 89689): hourly volatility (all-day avg 0.2917%) by slot: 09:15–10:00 0.3496%; 10–11 0.2380%; 11–12 0.2248% (lowest); 12–13 0.2460%; 13–14 0.2850%; 14–15 0.3268%; 15:00–15:30 0.2799%. Friday highest (09:15–10:00 = 0.4244%). Hourly volatility declined steadily 2011→2018 — [MPRA PDF, Table 1](https://mpra.ub.uni-muenchen.de/89689/1/MPRA_paper_89689.pdf)
- NSE stocks, high-frequency, Jan 2001–Dec 2009 (IIMA WP 2012-11-03, Agarwalla & Pandey): "reverse J"-shaped intraday volatility with much higher intraday variation than other markets; more pronounced for large caps; higher volatility in first hour after weekends, first half-hour after holidays, last hour before weekends; cross-listed stocks more volatile in first 45 min; stocks with derivatives show higher volatility in the last half-hour on expiry day only (settlement price = weighted average of last 30 min); day-trader share of volume 28.1% (2002) → 42.2% (2009) — [IIMA PDF](https://www.iima.ac.in/sites/default/files/rnpfiles/19191060542012-11-03.pdf)
- Nifty index 2000–2003 (Sampath & ArunKumar, SSRN): volatility high at open, elevated for first 30 minutes, rises again in last 15 minutes; "crude U shape" — [SSRN 2255391](https://www.ssrn.com/abstract=2255391) (abstract via search snippet)
- Sampath & Gopalaswamy 2020 (Journal of Emerging Market Finance): positive intraday volume–price-move relation; positive returns drive volume more than negative; U-shape in volatility is weaker unless intraday periodicity is adjusted — [Sage](https://journals.sagepub.com/doi/abs/10.1177/0972652720930586) (snippet)
- NIFTY stocks trade-and-quote study (Journal of Asian Economics 2013): most volume and spread measures U-shaped; high volume coincides with wide spreads, unusual for an order-driven market — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1049007813000596) (snippet)
- 2018–2025 NSE 1-/5-min study (ResearchGate, GARCH/LSTM-GARCH): U-shape with open/close peaks and spikes around macro announcements — [ResearchGate listing](https://www.researchgate.net/publication/401078172_Intraday_Timing_and_Market_Volatility_in_Indian_Financial_Markets_An_Econometric_Approach) (snippet only)
- Practitioner note: first 15–30 min described as a volatility burst that "shakes out" traders; Bank Nifty ORB gives "more violent fake-outs"; STT and brokerage "materially reduce small intraday wins" — [OneTradeJournal 15-min ORB](https://onetradejournal.com/strategies/fifteen-minute-orb-strategy) (no statistics)

### Inferences
- The 09:15–09:30 window carries the highest per-minute variance on NSE (hourly-equivalent 0.35% vs 0.22% mid-day), so fixed-rupee stops placed inside the first 15 minutes will be hit disproportionately; ATR-scaled stops (ORB paper style) or deferring entry to 09:30+ are the natural mitigations. No paper quantifies "net negative for breakout traders".
- 14:00–15:30 has the second-highest volatility; combined with Q1 (last-half-hour momentum) this is the window most likely to reward trend-following, but trend "persistence" per se is undocumented on NSE.
- On monthly/weekly derivatives-expiry days, the last 30 minutes is structurally different (settlement VWAP); strategies entering 15:00–15:30 should flag or exclude expiry days.

### Gaps
- No NSE study found on return (as opposed to volatility) autocorrelation by time of day, or on the first 15 minutes' expectancy for breakouts.
- Monash/ScienceDirect liquidity paper full text blocked.
- Post-2018 (especially 2022–2026) time-of-day volatility figures not available from a public paper.

---

## Q5. Opening-range breakout (Zarattini & Aziz 2023; Zarattini, Barbon, Aziz 2024 "stocks in play"): exact rules, results, replications/critiques

### Takeaway
Rules are fully specified and easy to code. Gross results replicate (independent QQQ replication: Sharpe 1.06 vs paper 1.12; trade count 1,775 vs 1,795), but three independent replications find the edge disappears at realistic spread/slippage (break-even ≈ 2.2¢/share on QQQ; net ≈ 0 or negative on NQ/SPX/Dow/DAX/FTSE), is concentrated in 2022, and had no out-of-sample period. The stocks-in-play version (Sharpe 2.81, 1,637% 2016–2023, $0.0035/share commission, no slippage) has only a partial replication (QuantConnect Sharpe 2.4 / 1.97) and no cost-stress test. No Indian evidence exists.

### Cited Findings
Paper 1 — QQQ/TQQQ (Zarattini & Aziz, SSRN 4416622, Apr 2023; rev. Sep 2025):
- Rule: direction = sign of first 5-min candle (09:30–09:35); doji → no trade; enter at open of second 5-min candle; stop = low of first candle (long) / high (short); $R = entry − stop; target 10R or EOD close, whichever first; no partial exits; risk 1% of equity per trade; max 4× intraday leverage; shares = int(min(0.01·A/$R, 4·A/P)); $25,000 start; commission $0.0005/share; "We assumed no slippage in fills"; 1 Jan 2016–17 Feb 2023 — [Zarattini & Aziz PDF, Table 1](https://static1.squarespace.com/static/5983d931579fb366729580d8/t/643ed6765176b45506e41a01/1681839734183/SSRN-id4416622.pdf)
- Results QQQ: 1,795 trades (51% long), win rate 24%, avg +0.13R/trade, $25k → $192,806 (~675%), annualized alpha 33% net of commissions, Sharpe 1.12, beta ~0; max daily loss ≈ −1R; leverage cap binding on most trades; unconstrained-leverage version ≈ 2× the growth. TQQQ: 1,484% total, alpha 47%, Sharpe 1.18 — [same PDF](https://static1.squarespace.com/static/5983d931579fb366729580d8/t/643ed6765176b45506e41a01/1681839734183/SSRN-id4416622.pdf)
- Parameter search: stop = 5% of 14-day ATR with EOD exit (no target) → 9,350% on TQQQ, alpha 93%; authors themselves call this "unrealistic" because the stop is ~$0.08 on a $25 stock with zero slippage assumed — [same PDF, Sec. "sensitivity"](https://static1.squarespace.com/static/5983d931579fb366729580d8/t/643ed6765176b45506e41a01/1681839734183/SSRN-id4416622.pdf)
- Replication A (GitHub, QQQ 5-min 2016–Feb 2023): 1,775 trades, Sharpe 1.06, max DD 22% (paper 22%), net PnL $138,639 = $0.070/share gross of slippage; at $0.02/share entry slippage PnL falls to $4,860; break-even ≈ 2.2¢/share (QQQ spread ≈ 1¢); 2022 = 38% of PnL; NQ-confirmation filter raises per-trade t to 2.05 but 76% of its PnL is 2022; bootstrap Sharpe CI [0.05, 1.41] overlaps buy-and-hold [−0.03, 1.47]; ES futures Mar–Sep 2026 run found no edge — [giovannibrusco/zarattini-2023-orb-qqq](https://github.com/giovannibrusco/zarattini-2023-orb-qqq)
- Replication B (five index CFDs, Jan 2015–Jun 2026, ~2,900 sessions each, same rule, round-trip cost NQ 2.5 / SPX 0.8 / Dow 4.0 / DAX 2.5 / FTSE 1.5 points charged as spread+slippage): gross avg R/trade NQ +0.131 (t 2.9), SPX +0.119 (t 2.4), DAX +0.116 (t 2.4), Dow +0.048, FTSE +0.050; NET: NQ +0.002 (t 0.0), SPX −0.081, Dow −0.081, DAX −0.038, FTSE −0.079 — "no market is distinguishable from zero and four of five are negative"; hit rate 23.2% (paper ~24%); 2015–2017 negative in every market; OOS 2021–2026 at best +0.06R on NQ — [MQL5 blog replication](https://www.mql5.com/en/blogs/post/776235)
- Replication C (SSRN, Subhani): event-free-Friday variant reports +0.44R/trade OOS on QQQ but authors say results "depend on judgements about the search rather than on the data" and only a forward test resolves it — [SSRN 7589980](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7589980)
- Critique summary: no slippage, no OOS period, parameter search creates overfitting, results depend on leverage constraints — [DanFin review](https://danfin.net/opening-range-breakout-research)

Paper 2 — US stocks in play (Zarattini, Barbon, Aziz 2024, SSRN; "A Profitable Day Trading Strategy for the U.S. Equity Market"):
- Rule: universe ~7,000 US stocks 2016–2023 incl. delisted; filters: open > $5, 14-day avg volume ≥ 1M shares, 14-day ATR > $0.50; relative volume = today's first-5-min volume / avg first-5-min volume over prior 14 days, require ≥ 100% (i.e., ≥1.0), trade top 20 by RVOL; opening range = first 5-min bar; bullish bar → buy-stop at bar high; bearish → sell-stop at bar low; doji → nothing; stop = 10% of 14-day ATR from entry; exit EOD if not stopped (no target); risk up to 1% of equity per position, 4× leverage cap; commission $0.0035/share; no slippage — [DanFin review](https://danfin.net/opening-range-breakout-research); [QuantConnect replication post](https://www.quantconnect.com/research/18444/opening-range-breakout-for-stocks-in-play/)
- Results: filtered portfolio 1,637% total, 41.6% annualized, Sharpe 2.81, hit ratio 48.4%, max DD 12%, worst day −1.61%, alpha 36%; unfiltered base ORB on all stocks: 29% total, Sharpe 0.48, hit 41.4%, max DD 13% — [DanFin review](https://danfin.net/opening-range-breakout-research); [search summary](https://www.alexandria.unisg.ch/entities/publication/ab50f49b-4d5c-4aa8-aaa1-af7a4c131008)
- QuantConnect replication (1,000 most liquid > $5, ATR > $0.50, top-20 RVOL, stop-market at bar high/low, ATR-multiple stop, exit at close, 1% risk per asset sleeve): Sharpe 2.396, beta −0.042 (SPY 0.836) for 2016; separate run Sharpe 1.968; 17/25 parameter combos beat benchmark; ATR threshold $0–$2 all beat buy-and-hold (Sharpe 1.5–2.7); forum users report ~17% win rate and ~10% COVID drawdown — [QuantConnect](https://www.quantconnect.com/research/18444/opening-range-breakout-for-stocks-in-play/)
- Structural note: this is the paper where 5-min range was chosen because it "was the best-performing duration of all the intervals tested" (15/30/60 also tested) — [QuantConnect](https://www.quantconnect.com/research/18444/opening-range-breakout-for-stocks-in-play/)

### Inferences
- NSE translation (Paper 1 style, Nifty futures or liquid F&O stock): OR = 09:15–09:20 bar; direction = sign(close−open) of that bar, skip if |close−open| < x% of range (doji); enter at 09:20 open; stop at OR extreme; target 10R or exit at 15:25 bar close; size so stop-out = 1% equity. Paper 2 style for Nifty-50 stocks: RVOL = vol(09:15–09:20) / mean(vol(09:15–09:20) over prior 14 days); take top-N RVOL ≥ 1; stop-entry at OR high/low; stop = 0.10 × ATR(14, daily); EOD exit.
- Given the replications, expected gross edge ≈ +0.1R/trade with ~24% hit rate and 10R target; NSE round-trip cost on a 5-min-range stop (which on Nifty is often only ~0.1–0.2% wide) will likely consume ≥ 0.1R, so the index version is expected to be net-zero on NSE as it is on NQ/SPX/DAX. The stocks-in-play version has a much higher hit rate (48%) and a volatility filter, which is the variant worth testing on NSE — but it has no cost-stress replication anywhere.
- 2022 (a high-vol year) dominates the US PnL; a 2022–2026 NSE backtest will include a comparable regime only partially, so year-by-year reporting is essential.

### Gaps
- No Indian ORB study with statistics found (only broker education pages).
- Stocks-in-play paper full text not accessed; stop multiplier and sizing confirmed only via secondary sources.
- No published cost-stress or out-of-sample test of the stocks-in-play variant.

---

## Q6. VWAP-based strategies with published evidence

### Takeaway
No peer-reviewed study testing a VWAP-reversion or VWAP-trend rule as a return signal was found, in India or elsewhere. The academic VWAP literature is about execution benchmarking and optimal execution, not alpha. Commonly quoted statistics (e.g., "63% reversion from 2-σ bands", "57% win rate, JPM 2021") are unsourced.

### Cited Findings
- Academic VWAP work is execution-cost measurement (Berkowitz, Logue, Noser 1988 JF) and optimal VWAP execution (e.g., UTS QFR paper; arXiv RL papers), not signal profitability — [UTS QFR-rp201](https://www.uts.edu.au/globalassets/sites/default/files/qfr-archive-02/QFR-rp201.pdf); [arXiv 2212.14670](https://arxiv.org/pdf/2212.14670)
- A TradingView-published backtest claims VWAP crossover shows zero Bonferroni-significant results while VWAP mean-reversion (esp. short side) has the widest positive distribution; unreviewed — [TradingView EdgeTools](https://www.tradingview.com/chart/ES1!/tVJcD92K-Everyone-Uses-VWAP-Wrong/)
- One trading-education site itself notes "there is no reliable published win rate for this 2-standard-deviation fade" — [search summary citing therighttrader.com](https://therighttrader.com/learn/trading-strategies/vwap-mean-reversion)
- HKS note that institutions' VWAP-like trading is a driver of the open/mid-day cross-sectional periodicity (Q2) — [Kellogg 2025 listing](https://www.kellogg.northwestern.edu/academics-research/research/detail/2025/the-intra-day-stock-return-periodicity-puzzle/?p=1)
- Concretum (Zarattini's firm) has a VWAP day-trading write-up; not fetched, non-peer-reviewed — [Concretum VWAP post](https://concretumgroup.com/volume-weighted-average-price-vwap-the-holy-grail-for-day-trading-systems/)

### Inferences
- Any VWAP rule the engineer codes is a hypothesis without literature support; if tested, the natural candidates are (a) reversion: fade price when |close − cumVWAP| > k × intraday σ, exit at VWAP touch or EOD; (b) trend: enter on first 5-min close above VWAP after 10:00 with VWAP rising. Both must be reported gross and net with the NSE cost stack.

### Gaps
- No peer-reviewed VWAP-signal study found; Quantpedia and Alpha Architect inaccessible, so a Quantpedia VWAP strategy page may exist unseen.

---

## Q7. Previous-day high/low breakout, NR7 / inside-day breakout, Bollinger squeeze: rigorous evidence (esp. India)

### Takeaway
No rigorous evidence for any of these at the intraday single-stock level, in India or elsewhere. The only academic test of Bollinger-type volatility breakouts (Fang, Jacobsen, Qin 2014, 14 indices) finds the edge vanished after 2001 and the squeeze variant was negative post-2001. Indian NR7 material is screeners and a Medium backtest with near-50/50 win rate and no costs.

### Cited Findings
- Fang, Jacobsen & Qin, "Popularity versus Profitability: Evidence from Bollinger Bands" (2014 draft): 20-day middle band, ±2σ; buy on close above upper band, sell on close below lower; squeeze variant trades only when bandwidth at a 6-month minimum; 14 international indices from 1885–1971 start to Mar 2014; avg daily buy–sell spread 0.29% full sample (market 0.03%), 0.45% pre-1983, 0.30% 1983–2001 (not for US indices), 0.00% post-2001 (only 2 indices significant); squeeze post-2001 −0.07%; net results assume 1% one-way switching cost and S&P 500 net worked "before the mid-1980s and poorly since" — [CXO Advisory summary](https://www.cxoadvisory.com/big-ideas/when-bollinger-bands-snapped/)
- NR7 India: Medium backtest of NR7+inside-bar on F&O stocks since 2015: next-day buy trades 631 positive vs 724 negative, net P&L positive; no significance test, costs or OOS — [Medium (Amit Ghosh)](https://amit-ghosh.medium.com/backtesting-narrow-range-inside-bar-strategy-using-python-16551f8db7bd)
- NR7 screeners/courses for NSE provide signals only, with disclaimers to backtest yourself — [PKScreener](https://github.com/pkjmesra/PKScreener); [Unofficed NR7 course](https://unofficed.com/courses/narrow-range-strategy/lessons/intraday-strategy-nr7/)
- Previous-day high/low breakout: only indicator scripts and blogs; no academic backtest found — [LuxAlgo PDH/PDL](https://www.luxalgo.com/library/indicator/dn6ogsKO-previous-day-high-and-low-breakout-strategy/)
- Generic 15-min breakout script result (not Nifty-specific): win rate ~35%, R:R ~1.8, 132 trades, average P&L near breakeven — [TradingView KedArc](https://ru.tradingview.com/script/tSoUhlM9-Universal-Breakout-Strategy-KedArc-Quant/)

### Inferences
- These three families should be treated as untested hypotheses on NSE. The Fang-Jacobsen-Qin result (edge decayed as the indicator became popular) is a warning that squeeze/band breakouts are likely crowded.
- If coded, PDH/PDL breakout is the cleanest (no parameters): long on first 5-min close > prior-day high after 09:30 (to avoid Q4's opening variance), stop at prior-day high − 0.5×ATR(5-min, 14), exit 15:15; mirror for PDL.

### Gaps
- No Indian or international peer-reviewed intraday evidence for NR7, inside-day or PDH/PDL rules found.

---

## Q8. Volatility-targeted / regime-conditioned versions: does restricting to high-VIX or high-relative-volume days improve net results?

### Takeaway
Yes for market intraday momentum: Gao et al. show the OOS return of the first-half-hour timing rule rises from 0.54%/yr (low first-half-hour vol tercile) to 14.73%/yr (high tercile) and from 1.67% to 11.87% across volume terciles. For ORB, the relative-volume ("stocks in play") filter is the whole edge (Sharpe 0.48 → 2.81) and QQQ-ORB PnL is concentrated in the high-vol year 2022. No study conditions on India VIX specifically; the US conditioning uses realized first-half-hour volatility and volume, not the VIX.

### Cited Findings
- Gao et al. volatility/volume tercile OOS results (see Q1): η(r1) 0.54%/4.75%/14.73% per yr, t 0.43/2.27/3.80, Sharpe 0.18/0.97/1.63 by first-half-hour realized-vol tercile; 1.67%/6.46%/11.87%, Sharpe 0.42/1.29/1.38 by detrended first-half-hour volume tercile; in-sample R² 0.6% (low vol) → 3.3% (high vol); 1.1% → 3.1% by volume — [Gao et al. PDF, Tables 3 and 5](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf)
- Macro-news days: annualized return of the timing strategy reaches 20.04% on FOMC-minutes days — [Gao et al. PDF, Sec. 5](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf)
- QuantRocket's implementation adds a VIX < 20 "off switch" (practitioner choice, not from the paper) — [QuantRocket notebook](https://www.quantrocket.com/codeload/first-last/first_last/Introduction.ipynb.html)
- Li-Sakkas-Urquhart: ITSM stronger when liquidity low, volatility high, information discrete (16 developed markets) — [JFM 2022](https://ideas.repec.org/a/eee/finmar/v57y2022ics138641812100001x.html)
- Yang 2022 (CSI 300): last-hour momentum stronger on high-vol, high-volume, high-order-imbalance days — [Emerald](https://emerald.com/insight/content/doi/10.1108/CFRI-06-2021-0106/full/pdf)
- Baltussen et al.: intraday momentum strongest when option market makers are net short gamma (negative NGE); the Indian preprint uses the same NGE conditioning — [Baltussen PDF](https://www3.nd.edu/~zda/intramom.pdf); [Motwani et al. listing](https://www.researchgate.net/publication/383567351_Hedging_Demand_and_Intraday_Momentum_within_the_Indian_Stock_Market)
- ORB: base ORB on all US stocks Sharpe 0.48 vs top-20 relative-volume Sharpe 2.81 — [DanFin](https://danfin.net/opening-range-breakout-research); QQQ-ORB: 2022 = 38% of unfiltered PnL and 76% of NQ-filtered PnL — [GitHub replication](https://github.com/giovannibrusco/zarattini-2023-orb-qqq)
- Scribd Indian momentum note: strategies "worked best on high-volatility, high-volume days" — [Scribd](https://www.scribd.com/document/670520471/MomentumTrading) (weak source)

### Inferences
- The most evidence-backed regime filter implementable from 5-min OHLCV is "top tercile of first-half-hour realized volatility (sum of squared 5-min returns 09:15–09:45) and/or first-half-hour volume relative to its trailing distribution." India VIX is a reasonable proxy but is untested in the literature; realized first-30-min vol is what the papers used.
- Because costs are fixed per trade while edge scales with volatility, the net benefit of the filter on NSE should exceed what the US gross numbers show.

### Gaps
- No study found that conditions Indian intraday strategies on India VIX.
- NGE conditioning requires options open-interest data, outside the 5-min OHLCV constraint.

---

## Q9. Candidate strategy list for verbatim implementation on NSE 5-min bars (2022–2026)

### Takeaway
Eight candidates ranked by evidence quality. Only #1–#2 have peer-reviewed, cost-adjusted support (index level, US); #3–#4 have working-paper support with cost-negative replications; #5–#8 are hypotheses with no rigorous support anywhere and none in India. Every rule below should be reported gross and net with the full NSE cost stack and by calendar year.

### Cited Findings
- Rule parameters below are taken from the papers cited in Q1–Q8: Gao et al. (timing at start of last half-hour, long if r1>0 else short, close at close; r1 includes overnight) — [PDF](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf); Baltussen et al. (sign of return from prior close to 30 min before close) — [PDF](https://www3.nd.edu/~zda/intramom.pdf); Zarattini & Aziz (first 5-min candle, enter 2nd candle open, stop at candle extreme, 10R/EOD, 1% risk) — [PDF](https://static1.squarespace.com/static/5983d931579fb366729580d8/t/643ed6765176b45506e41a01/1681839734183/SSRN-id4416622.pdf); Zarattini-Barbon-Aziz (RVOL top-20, stop-entry at 5-min high/low, stop 10% of ATR14, EOD) — [DanFin](https://danfin.net/opening-range-breakout-research), [QuantConnect](https://www.quantconnect.com/research/18444/opening-range-breakout-for-stocks-in-play/); HKS (decile sort on same-half-hour return yesterday) — [PDF](https://www.bauer.uh.edu/departments/finance/documents/Heston_Korajczyk_Sadka_paper_UH.pdf); gap statistics — [IntradayLab](https://intradaylab.com/blog/nifty-gap-up-history-analysis); time-of-day — [MPRA](https://mpra.ub.uni-muenchen.de/89689/1/MPRA_paper_89689.pdf).

### Inferences (the coded rules; NSE time mapping is mine)

**S1. Nifty last-half-hour momentum, first-half-hour signal (Gao et al. 2018).** Instrument: Nifty 50 futures (current month) or Nifty ETF. r1 = close(09:40–09:45 bar) / prev-day close − 1. At 15:00: if r1 > 0 buy at open of 15:00 bar; if r1 ≤ 0 sell. Exit at close of 15:25 bar (or official 15:30 close). No stop (paper uses none; a stop at 2×σ(5-min) is a permissible add-on but untested). Optional filter (strongest evidence): trade only if first-half-hour realized vol (sqrt of sum of squared 5-min log returns 09:15–09:45) is in the top tercile of the trailing 250-day distribution. Evidence: US Sharpe 1.08 gross / ~0.7–1.0 net, success 54%, high-vol tercile 14.7%/yr. India: Motwani et al. preprint reports momentum into last half-hour, numbers unavailable. Failure modes: tiny per-trade edge (R² ~2%) swamped by NSE costs; effect reverts next day; expiry-day last-30-min settlement VWAP mechanics; flat/low-vol years near zero.

**S2. Nifty last-half-hour momentum, rest-of-day signal (Baltussen et al. 2021).** Same as S1 but signal = sign(close(14:55–15:00 bar) / prev-day close − 1). Variant S2b: trade only when sign(r1) == sign(rROD) (equity-futures Sharpe 1.60, success 0.61 gross in US/EU/Asia futures). Evidence: 1/N equity-index-futures Sharpe 1.73 gross, no costs modelled; no Indian contract in the sample. Also test the Indian preprint's window: signal at 14:30, hold 14:30–15:00. Failure modes: as S1; stronger reliance on short-gamma regimes (not observable from OHLCV).

**S3. 5-minute ORB on Nifty futures (Zarattini & Aziz 2023).** OR bar = 09:15–09:20. If close > open: buy at 09:20 open, stop = OR low. If close < open: sell at 09:20 open, stop = OR high. If |close − open| < 10% of OR range treat as doji → no trade (paper says "open ≈ close", threshold unspecified). R = |entry − stop|. Exit at first of: 10R target, stop, or close of 15:25 bar. Size = floor(min(0.01·Equity/R, L·Equity/Price)) with L = broker intraday leverage. Evidence: US gross +0.13R/trade, 24% win, Sharpe 1.12; net ≈ 0 in all five index replications; 2015–2017 negative everywhere; no OOS. Expected NSE net: ≤ 0 unless costs are far below US CFD costs. Failure modes: stop width often < round-trip cost; PnL concentrated in a few 10R days; slippage on stop fills.

**S4. 5-minute ORB on Nifty-50 "stocks in play" (Zarattini, Barbon, Aziz 2024).** Universe: Nifty 50 constituents (paper used ~7,000 stocks; apply same filters: price > threshold, 14-day avg volume floor, ATR14 floor). RVOL = volume(09:15–09:20) / mean(volume(09:15–09:20) over prior 14 sessions). Keep RVOL ≥ 1.0, rank desc, take top N (paper 20; with 50 names use top 5–10). For each: if OR bar bullish, buy-stop at OR high; bearish, sell-stop at OR low; doji → none; stop = entry ∓ 0.10 × ATR(14, daily); no target; exit at 15:25 bar close or stop. Risk 1% of the sleeve per trade; cap leverage. Evidence: US Sharpe 2.81, hit 48.4%, max DD 12%, $0.0035/share commission, no slippage, no OOS; QuantConnect replication Sharpe ~2.0–2.4. No Indian test. Failure modes: tiny ATR-fraction stops get hit by opening noise (Q4 shows 09:15–09:30 is the highest-variance window on NSE); universe of 50 names limits the RVOL selection effect that drove the US result; fills at stop-entry in the first minutes.

**S5. Nifty opening-gap fade (hypothesis; Indian index stats only).** gap = open(09:15 bar) / prev close − 1. If gap ≥ +1%: at 09:20 open sell with stop at max(high(09:15 bar), entry + 0.5%); target = prev close (full fill) OR exit at 15:25 close; mirror for gap ≤ −1%. Evidence: Nifty 2016–2026 n=85 gap-ups: closed below open 55.3%, mean open-to-close −0.25% but ≈ 0 ex-2020; full fill only 29%; gap-downs closed green 52.6%, fill 17%. Failure modes: edge is 2020-specific; >2% gaps on news continue (62.5% bearish close for gap-ups >2% means fading gap-ups >2% was the best bucket, fading gap-downs is weaker); sample is tiny (5–6 events/yr ex-2020).

**S6. Same-half-hour-yesterday continuation, cross-sectional (HKS 2010).** Every 30 min from 09:45, rank Nifty-50 stocks on their return in the same half-hour slot the previous day; long top decile (5 names), short bottom decile (5 names), hold for that half-hour. Evidence: 3.01 bp/half-hour gross (t=22) in US, strongest in first/last half-hour, persists ≥40 days; NEGATIVE after spreads in every size group in the paper itself. India: none. Include only as a cost-floor benchmark / execution-timing overlay; expected net negative.

**S7. Previous-day high/low breakout (no rigorous evidence).** After 09:30, long on first 5-min close > prior-day high; stop = prior-day high − 0.5 × ATR(14 bars of 5-min); exit 15:15 or stop; mirror for prior-day low. No paper supports this; Fang-Jacobsen-Qin shows analogous band breakouts on indices stopped working after 2001.

**S8. VWAP reversion / trend (no rigorous evidence).** cumVWAP from 09:15. Reversion: after 10:00, if close < VWAP − 2σ(5-min returns, trailing 30 bars)×price, buy; exit at VWAP touch or 15:15; stop 1σ beyond entry. Trend: after 10:00, long on first close above a rising VWAP; exit on close below VWAP or 15:15. No published evidence; include only if the implementer wants a null-hypothesis baseline.

Cost reporting requirement for every strategy: report gross, net at NSE statutory+brokerage cost, and the break-even cost (bp per round trip) at which net = 0, following the GitHub ORB replication's method (break-even slippage sweep).

### Gaps
- No Indian paper supplies cost-adjusted numbers for any of S1–S8; S1/S2 are the only ones with any Indian evidence at all (Motwani et al., unverified).
- Doji threshold in Zarattini & Aziz is not numerically defined in the paper.
- Stocks-in-play stop multiplier (10% of ATR14) and sizing come from secondary sources, not the paper PDF.
- No evidence exists on NSE first-15-minute breakout expectancy, last-hour trend persistence, NR7/inside-day, Bollinger squeeze, PDH/PDL, or VWAP strategies.
