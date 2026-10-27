# Intraday Option/Futures Scalping Strategies for Indian Index Derivatives (Nifty/BankNifty/Sensex) — Rule-Sets and Evidence

Scope: things NOT already tested by us (we know 0DTE 9:20 ATM short straddle w/ 25% leg SL works after costs; non-expiry straddles and Nifty-50 stock 1/5-min scalps do not). Focus: short-hold premium-decay scalps, expiry-afternoon selling, option-BUYING scalps (ORB/VWAP/9:15 candle/straddle-breakout), Nifty futures scalps, and pitfalls (costs, STT, slippage, SEBI stats, decay timing).

Labeling convention used below: **[COSTED]** = source states brokerage/taxes/slippage included; **[GROSS ONLY]** = no costs; **[CLAIM]** = marketing/vendor/anecdote with no methodology shown.

Research note: ~30 searches/fetches run (2026-10-27). Several key pages were 403/404 (SSRN 4641356 abstract page, Moneylife cost-table article, PL India expiry guide, Nitter/Xpert0ptions). Findings from those are via secondary coverage and are marked.

---

## Key Question 1: Which option-scalping rule-sets have ANY published cost-adjusted backtest, and what were the results?

### Takeaway
Almost none. For India, I found exactly zero public backtests of option-scalping (sub-60-min hold) rule-sets that state costs and slippage were included. The only India-specific results with numbers are (a) a 1:00 PM Sensex 0DTE short straddle (63% win rate, costs not stated), (b) a 9:20 Nifty straddle Dec-2024 1-min bot test (gross only), (c) a Marketcalls 15-min VWAP Nifty-futures system that was profitable gross and **unprofitable after costs**, and (d) unverified social-media backtests (RSI-50 option buying, a Nifty futures "dual-confirmation" system). The best cost-adjusted evidence is US (SPX) and it says the 0DTE premium-selling edge is "statistically real, economically irrelevant" after costs for static rules.

### Cited Findings

**India — premium selling, short windows / afternoon**
- **Sensex 0DTE 1:00 PM short straddle (1lyAlgos via Aliceblue)**: Thursday expiry, sell ATM CE+PE at 1:00 PM, exit 3:20 PM or earlier if combined premium falls 30%; no explicit stop-loss stated ("losses have no upper limit"); 1 lot, ₹3.2L margin. 15-month backtest: **63.32% win rate, net ₹77,603 (~24% on margin)**; max DD, trade count, costs and slippage **not stated**. Aug-2026 live: 4 Thursdays, +₹6,684 total (+2.09%). — [Aliceblue/1lyAlgos](https://aliceblueonline.com/blog/sensex-0dte-strategy-1lyalgos-complete-guide-for-2026) **[CLAIM / costs not stated — promotional]**
- **Nifty 9:20 short straddle, Dec 2024, 1-min Python bot, no SL, exit 15:15 (TradingQnA user iankurseth)**: 20 trading days, 12 wins / 8 losses, +434 pts total (~+21.7 pts/day); largest win +168 (expiry 19-Dec, straddle 170→1.85), largest loss −79. Expiry-day entries (4) = +165 pts net, dominated by one day. **No brokerage/STT/slippage** included; bar-close fills. — [TradingQnA](https://tradingqna.com/t/reports-of-the-death-of-920-short-straddle-are-greatly-exaggerated/179061) **[GROSS ONLY]**
- Same thread reply (Bhupen_A): a "premium-100 Rs strategy with a 25% stop loss works, very well" — stopped only due to margin; no numbers. — [TradingQnA](https://tradingqna.com/t/reports-of-the-death-of-920-short-straddle-are-greatly-exaggerated/179061) **[CLAIM]**
- **Bank Nifty 1 PM straddle (Streak template)**: sell straddle at 1 PM daily, per-leg SL, exit 3 PM; poster says SL/target "chosen arbitrarily"; **no results posted**. — [TradingQnA](https://tradingqna.com/t/bank-nifty-straddle-backtest-in-streak/136147)
- **Bank Nifty 2:30–3:15 PM window**: a trader states he is "90 percent sure there will be at least 50 points of movement in any direction between 2.30 pm and 3.15 pm" (he was deploying a *long* straddle ~2 PM); anecdotal, no backtest. — [TradingQnA](https://tradingqna.com/t/intraday-bank-nifty-short-straddle-short-strangle/38046) **[CLAIM]**
- Expiry-day Bank Nifty thread: fills rarely occur at quoted open price, "premium decays within minutes," so slippage must be modelled; STT near expiry flagged as a drag. — [TradingQnA via search summary](https://tradingqna.com/t/intraday-bank-nifty-short-straddle-short-strangle/38046)
- Re-entry (sell straddle → SL → re-enter after 15–30 min) backtesting: a TradingQnA user requested it; another said StockMock lacks re-entry; AlgoTest (competitor) claims both platforms support re-entry. I found **no published results** for a repeated 15–60-min straddle-selling loop. — [TradingQnA](https://tradingqna.com/t/sensibull-fno-backtesting/92466); [AlgoTest vs StockMock](https://algotest.in/blog/algotest-vs-stockmock.md)
- AlgoTest general guidance for straddles: per-leg SL 35–50% or combined SL ~1.5× premium; "results may look strong during sideways markets, but drawdowns increase during trending days." Re-entry "creates additional exposure and trading costs." — [AlgoTest](https://algotest.in/blog/how-to-backtest-options-trading-strategies-with-examples.md); [AlgoTest short straddle](https://algotest.in/blog/short-straddle-strategy.md)

**India — option buying (momentum/ORB/RSI)**
- **"RSI-50 ATM buying" (viral creator backtest, unnamed)**: buy ATM CE when RSI>50, ATM PE when RSI<50; fixed premium SL/target (e.g., entry ₹100, SL ₹75, target ₹150); 5 years, **829 trades, 52.96% win rate, ~₹4L total PnL**; 641 EOD exits vs 188 trailing-SL exits; drawdown and costs **not stated**. — [Multibagg roundup](https://www.multibagg.ai/market-pulse/articles/nifty-algo-backtest-results-2026-cmrg191cpjai5np0jleu5s47x) **[GROSS ONLY / unverified]**
- **Nifty futures "dual-confirmation" (unnamed poster)**: Jan 2025–Jan 2026, ₹4L capital, max 2 contracts, **159 trades, 55.35% win, profit factor 1.906, max DD ₹98,727**; rules and costs not disclosed. — [Multibagg roundup](https://www.multibagg.ai/market-pulse/articles/nifty-algo-backtest-results-2026-cmrg191cpjai5np0jleu5s47x) **[GROSS ONLY / unverified]**
- **Tradetron "RKT" weekly-options intraday algo**: Apr 2025–Apr 2026, 1-min data "open trade price" fills; no PnL/win-rate disclosed; commenters question fill assumptions. — [Multibagg roundup](https://www.multibagg.ai/market-pulse/articles/nifty-algo-backtest-results-2026-cmrg191cpjai5np0jleu5s47x) **[CLAIM]**
- **AlgoTest ORB/option-buying**: no published AlgoTest ORB result found; an AlgoTest blog (different setup, from 2021) reportedly showed **60% win rate, ~₹11k max DD before costs, and "profit curve drops significantly once brokerage, slippage and charges are added."** — [search summary citing AlgoTest blog](https://algotest.in/blog/how-to-backtest-options-trading-strategies-with-examples.md) (exact post not retrieved)
- **AlgoTest scalping guide** gives rule templates only (1-min VWAP + 9/21 EMA cross; 5-min VWAP pullback with 20 EMA) with **no backtest numbers**; only warning: "A strategy that looks profitable before costs may produce a loss after them." — [AlgoTest scalping](https://algotest.in/blog/scalping-strategy.md)
- Vendor Telegram (Xpert0ptions) claims Nifty/Sensex 0DTE systems backtested Jun 2019–Jun 2026 **with 1% slippage (Nifty) / 2% (Sensex)** — no PF/DD visible; page 403'd on fetch; unverified. — [Nitter mirror](https://nitter.kareem.one/Xpert0ptions) **[CLAIM]**

**India — futures**
- **Marketcalls 15-min VWAP strategy (Nifty & BankNifty futures, Jan 2011–Dec 2019)**: buy when bullish 15-min candle touches and closes above day-VWAP, enter on break of its high (mirror for short); target 30 pts Nifty / 90 BN; SL 20 / 60; one trade/day; no signals after 14:44; square-off 15:14; prior-day VWAP as bias. **Result: Nifty profitable gross but NOT after commissions+slippage; Bank Nifty unprofitable even gross.** Reader running it live 2 months: "rarely gives target of 35 points," reversals near 20 pts. — [Marketcalls](https://www.marketcalls.in/?p=51686) **[COSTED → negative]**

**US (SPX) — cost-adjusted evidence**
- **Vilkov, "0DTE Trading Rules" (Frankfurt School; SSRN 4641356; SPX, Sep 2016–Jan 11 2024)**: static daily rules (straddles, strangles, condors, butterflies, spreads, risk reversals held to expiry). Variance risk premium exists but is ~**0.001% of index from 10 a.m. to close**; "transaction costs absorb it"; straddles show no consistent profitability held to expiry; realized **skewness**, not variance, explains daily P&L; Sharpe ≈ 0; risk reversals ~+0.01% of index mean (trivial). Conditional (skew/vol/macro-adaptive) rules may have an edge but need skew forecasting. — [Breaking Nasdaq summary](https://breakingnasdaq.beehiiv.com/p/the-0dte-illusion); [Hull Tactical commentary](https://hulltactical.com/2026/07/08/0dte-options-tiny-edge-huge-distribution/); SSRN page 403'd. Data at osf.io/7q86u per paper. **[COSTED → ~zero edge]**
- **Option Alpha ORB on SPX 0DTE credit spreads** (bullish break of 15/30/60-min range → short put spread with short strike at/below range low; bearish mirror; range ≥0.2% of open; no entry after 12:00 ET; hold to close; $15 wings best): 60-min: **win 89.4%, PF 1.44, avg $39/trade, max DD −$3,453**; 30-min: 82.6%, PF 1.19, DD −$8,306; 15-min: 78.1%, PF 1.17, DD −$7,602. Period, trade count, commissions **not stated**. — [Option Alpha](https://optionalpha.com/blog/opening-range-breakout-0dte-options-trading-strategy-explained) **[GROSS ONLY — and note it's premium SELLING on breakout, not buying]**
- **Option Alpha 0DTE user data (230k trades)**: only **49.64% of 0DTE traders profitable**; iron condors 70.19% win, iron butterflies 66.76% win (78% of positions); profitable traders entered ~**10:15 ET and exited ~12:00 ET (~2h hold)**; example rules: TP +15%, SL −25%, time-exit 12:00; Thursday consistently negative; commissions not mentioned. — [Option Alpha](https://optionalpha.com/blog/0dte-options-strategy-performance) **[GROSS ONLY]**
- Retail trade-journal sample (US, 2020–22): average return per trade **option purchases −3.95%, 0DTE trades −4.6%, non-0DTE ~0%, naked sales +20% (with tail risk)**; a conference paper attributes **~60% of daily retail 0DTE losses to transaction costs**. — [LambdaFin](https://www.lambdafin.com/articles/option-trading-success-rate/) (secondary; underlying paper unnamed)

### Inferences
- The only "costed" results that exist for anything scalping-like in India (Marketcalls VWAP futures) went from profitable to losing once costs were added — consistent with our own stock-scalp findings.
- The 1 PM Sensex straddle result (63% WR, ~24% on margin in 15 months, no SL) is the most promising untested India rule-set, but with no SL and no cost disclosure the expected net after Sensex slippage (vendor itself assumes 2%) is unclear; must be re-run with 25–30% leg SL and costs.
- The Option Alpha ORB finding transfers as a *hypothesis* only: breakout → sell the OTHER side (credit spread) rather than buy the breakout option. Their 60-min range beat 15-min on every metric.

### Gaps
- No public India backtest found for: repeated 15–60-min straddle-selling loops; "last hour" (14:30–15:10) 0DTE selling; straddle-breakout (buy both, exit loser); 9:15-candle option buying; VWAP/EMA scalps on option premium — all absent or results-free.
- SSRN abstract and Moneylife cost article blocked (403); numbers above are via secondary coverage.

---

## Key Question 2: For 0DTE Nifty, what is the intraday premium-decay profile, and does afternoon selling have an edge?

### Takeaway
No measured Nifty dataset of "fraction of ATM straddle premium decayed by 10:30/12:00/14:00" was found anywhere public. Claims conflict: broker/vendor pages put the steepest decay in the afternoon (12:00–15:30, "70–80%"), while a forum view says most decay is done by noon. US sources (SpotGamma) say most 0DTE SPX time-value decay occurs 11:00–15:00 ET. Treat all as unmeasured; this is a gap we should fill with our own minute data.

### Cited Findings
- Sahi (broker blog) Nifty Tuesday-expiry figures (unsourced): ATM ₹80–100 at open → ₹10–15 by 2:30 PM; 10:30–13:30 window "ATM loses 30–40% of remaining value"; afternoon "₹20–40+/hour"; after ~2 PM "an ATM at ₹15 can fall to ₹2 in 20 minutes sideways"; also claims Nifty can move 100–200 pts in 30 min late-session; internally inconsistent on whether to sell in the last 30 minutes. — [Sahi](https://www.sahi.com/blogs/nifty-expiry-day-strategies-scalping-guide) **[CLAIM]**
- Sahi separate article: square off short-theta positions before 12 PM "when IV compresses fastest" (assertion). — [Sahi](https://www.sahi.com/blogs/5-rules-every-trader-must-follow-on-nifty-options-expiry-day) **[CLAIM]**
- Stockmojo (vendor): expiry-day ATM straddle "can lose 50–80% in a single session"; typical pattern "slight premium inflation in the mornings, modest decay mid-day, accelerated decay in the last two hours"; no data. — [Stockmojo](https://stockmojo.in/learn/option-premium-decay/); [Stockmojo BN live](https://stockmojo.in/premium-decay/banknifty) **[CLAIM]**
- PL India guide (Bank Nifty): options lose "70–80% value between 12 PM and 3:30 PM"; no method; page 404 on fetch. — [PL India via search](https://www.plindia.com/?p=21074) **[CLAIM]**
- TradingQnA user: "most of the decay happens till 12 noon then the decay rate decreases" — contradicts vendor pages. — [TradingQnA](https://tradingqna.com/t/related-to-option-theta-or-time-decay/134556) **[CLAIM]**
- Expiry-day theta values differ materially between Upstox and Sensibull — any decay backtest must fix a time-stamp/model convention. — [Upstox community](https://community.upstox.com/t/discrepancy-in-theta-values-between-upstox-and-sensibull-on-expiry-day/8326)
- US SPX: "most of that decay happens between 11 AM and 3 PM" ET; 0DTE hedging flows peak in final two hours; 2:00–3:30 PM ET is the "pin or pop" window; avoid first 15–30 and last 15 min — all qualitative, no data shown. — [SpotGamma](https://spotgamma.com/?p=19841) **[CLAIM]**
- US SPX: Vilkov finds the 10 a.m.–close variance risk premium is ~0.001% of index and costs absorb it; i.e., no clear afternoon seller's edge in static rules. — [Breaking Nasdaq](https://breakingnasdaq.beehiiv.com/p/the-0dte-illusion)
- Hizmeri et al., "0DTE Asset Pricing": intraday VRP driven mainly by **upside** risk and negatively predicts intraday returns; many 0DTEs violate stochastic-dominance bounds and exploiting that was "highly profitable up to 2022 but dissipated after daily 0DTE availability." — [Liverpool seminar](https://liverpool.ac.uk/institute-for-financial-and-actuarial-mathematics/past-seminars/rodrigo-hizmeri); [Tinbergen](https://tinbergen.nl/event/2025/11/06/13089/0dte-asset-pricing)
- Only India result with an afternoon entry and numbers: Sensex 1 PM straddle, 63.32% win (see Q1). — [Aliceblue](https://aliceblueonline.com/blog/sensex-0dte-strategy-1lyalgos-complete-guide-for-2026) **[costs not stated]**
- Dec-2024 Nifty 9:20 straddle table shows the expiry-day straddle at 9:20 was 221 (5-Dec), 81 (12-Dec), 170 (19-Dec), 125 (26-Dec) pts and closed at 232 / 100 / 1.85 / 99 respectively — i.e., 2 of 4 expiry days the ATM straddle *rose* from 9:20 to 15:15. — [TradingQnA](https://tradingqna.com/t/reports-of-the-death-of-920-short-straddle-are-greatly-exaggerated/179061)

### Inferences
- The "afternoon decay" edge is asserted by vendors with incentives, contradicted by a forum trader, and the only rigorous study (US) says static selling at any hour is ~zero after costs. The Sensex 1 PM result is the only India datapoint and is unverified.
- The Dec-2024 table shows the 0DTE straddle can finish *above* its 9:20 level on half of expiries; afternoon entries would be subject to the same late moves (SpotGamma's "pop" window), so an SL is essential, which vendor 1 PM setups omit.

### Gaps
- No public Nifty minute-level measurement of % premium decayed by 10:30/12:00/14:00 on expiry. Must be computed from our own data.
- No India backtest comparing entry-time buckets (9:20 vs 11:00 vs 13:00 vs 14:30) for short straddles with costs.

---

## Key Question 3: Do option-buying momentum scalps show positive expectancy anywhere credible?

### Takeaway
No. Every credible dataset found shows negative expectancy for retail option buying (SEBI: ~90% of "only option buyers" lose; US journals: −3.95%/trade; buying $1 calls into close ~15% win). The only "positive" buying backtests are unverified creator claims (RSI-50: 53% win, costs unstated). Option Alpha's ORB "edge" is achieved by SELLING spreads on the breakout, not buying.

### Cited Findings
- **SEBI FY25–FY26 study (Aug 2026)**: "only option buyers" = ~93% of individual F&O traders, **~90% loss-makers, avg loss ~₹1.3L**; "majorly option sellers" = ~2% of traders, ~44% loss-makers, avg loss among losers ~₹51.7L; traders active >100 days: 42% of traders, 87% of losses, avg loss ₹2.76L; profitable quarters 15.4%; median winning-quarter profit ₹4,366 vs median losing-quarter loss ₹10,525; FY22–26 only 0.5% profitable every year. **No intraday-vs-positional or holding-time breakdown published.** — [TradingQnA summary of SEBI](https://tradingqna.com/t/win-rate-capital-experience-what-sebi-found-about-f-o-traders/197266)
- Earlier SEBI (FY24): 91.1% of individual F&O traders lost; 91.5% of options traders lost; transaction costs ≈ 28% of loss-makers' net losses (per Sahi citing SEBI). — [Moneylife](https://moneylife.in/article/91-percentage-of-retail-traders-lost-money-in-derivatives-losses-in-fo-surged-41-percentage-to-rs105-lakh-crore-in-fy25-sebi-study/77613.html); [Sahi](https://www.sahi.com/blogs/nifty-expiry-day-strategies-scalping-guide)
- US retail journals: option purchases **−3.95%/trade**, 0DTE **−4.6%/trade**; ~60% of daily retail 0DTE losses attributed to transaction costs. — [LambdaFin](https://www.lambdafin.com/articles/option-trading-success-rate/)
- Buying ~$1 SPX calls daily into the close: **~15% win rate**, inconsistent returns. — [Vol Vibes "Liftin' 0-DTEs"](https://volvibes.substack.com/p/liftin-0-dtes)
- Option Alpha: win rates for long calls/puts **not even reported**; profitable 0DTE users are overwhelmingly condor/butterfly sellers. — [Option Alpha](https://optionalpha.com/blog/0dte-options-strategy-performance)
- RSI-50 ATM buying: 829 trades, 52.96% win, ~₹4L over 5 years, costs not stated, source unnamed. — [Multibagg](https://www.multibagg.ai/market-pulse/articles/nifty-algo-backtest-results-2026-cmrg191cpjai5np0jleu5s47x) **[GROSS ONLY / unverified]**
- **Expiry ORB option-buying rule-set (Sahi, no backtest)**: 9:15–10:00 ORB; buy ATM CE on break above ORB high with volume spike + above VWAP (mirror for PE); **SL 30% of premium; target 20–30 pts premium; time-stop 30 min**; max 2–3 trades/day; flat by 2 PM. Also "Max-pain convergence" buying 12:00–14:00 with 30% SL. No stats. — [Sahi](https://www.sahi.com/blogs/nifty-expiry-day-strategies-scalping-guide) **[CLAIM]**
- 15-min ORB (OneTradeJournal, Bank Nifty futures illustration): range 9:15–9:30 incl. wicks; confirm with a 5-min close outside; SL = opposite range edge; target discretionary; worked R:R 1.4; "no fixed win rate is established." — [OneTradeJournal](https://onetradejournal.com/strategies/fifteen-minute-orb-strategy)
- Breakout → buy ATM call with 25-pt target / 10-pt stop appears only as a template, no results. — [Tability template](https://tability.io/templates/strategies/tags/breakout-trading) **[CLAIM]**
- Straddle-breakout (buy both, exit loser): no backtest found; AlgoTest notes two-leg trades double all charges. — [AlgoTest rolling straddles](https://algotest.in/blog/how-to-backtest-rolling-straddles-with-indicators.md)
- Long straddle timing: forum thread asks for best deployment time, no data. — [TradingQnA](https://tradingqna.com/t/what-would-be-the-best-time-to-deploy-the-long-straddle-for-nifty-50/194686)
- Blueshift/QuantInsti has minute-level F&O option data but has **not released it** because it "has not yet found a methodology accurate enough to rely on the backtest results." — [Quantra community](https://quantra.quantinsti.com/community/t/intraday-option-data/22752)
- Nubra open-source NSE backtester notes intraday option bars "stop publishing the day before expiry" for NIFTY 5-min in some data sets — data-quality trap for 0DTE tests. — [PyPI nubra-backtest-engine](https://pypi.org/project/nubra-backtest-engine/)

### Inferences
- Any option-buying scalp we test should be benchmarked against the SPX ORB *credit-spread* variant (sell the far side on breakout, hold to close), which is the only ORB with published positive stats — and even that is gross.
- With ~53% win rate at 1:1.5 R:R (RSI-50 claim) the gross edge is thin; India round-trip option costs (~₹165 per 200-unit trade, see Q5) plus 2–3 pt spread on ₹100 premium (~3%) likely erase it.

### Gaps
- No credible costed India option-buying scalp backtest exists publicly. Zerodha Z-Connect has no option-buying win-rate study (only an anecdotal "60-day challenge" winner).
- SEBI publishes no holding-time breakdown.

---

## Key Question 4: US 0DTE academic findings that transfer

### Takeaway
Two academic lines: (1) Vilkov (Frankfurt) — static 0DTE selling rules have a tiny VRP wiped out by costs; P&L is driven by realized skew; only conditional rules might work. (2) Hizmeri et al. — intraday VRP is mostly upside-risk compensation and negatively predicts intraday returns; mispricing-based profits vanished once daily expiries arrived (2022). Transfer to India: daily index expiries existed (Nifty/BN/FinNifty/Sensex/Bankex staggered) in 2023–24 and were then cut back to one weekly expiry per exchange — so the "edge dissipates with more 0DTE availability" result is directly relevant.

### Cited Findings
- Vilkov "0DTE Trading Rules": SPX 09/2016–01/2024; straddles/strangles/spreads/risk reversals held to expiry; VRP "statistically present but economically negligible" (~0.001% of index, 10 a.m.–close); costs eliminate it; Sharpe ~0; realized skewness explains most P&L; "static strategies fail across the board." — [Breaking Nasdaq](https://breakingnasdaq.beehiiv.com/p/the-0dte-illusion); [Hull Tactical](https://hulltactical.com/2026/07/08/0dte-options-tiny-edge-huge-distribution/)
- Hizmeri et al. "0DTE Asset Pricing": most intraday equity premium comes from market returns in [−5%, 0]; VRP driven by upside risk, negatively predicts intraday returns; stochastic-dominance violations were "highly profitable up to 2022" then dissipated after daily 0DTE listings. — [Liverpool](https://liverpool.ac.uk/institute-for-financial-and-actuarial-mathematics/past-seminars/rodrigo-hizmeri); [Tinbergen](https://tinbergen.nl/event/2025/11/06/13089/0dte-asset-pricing)
- OptionMetrics: ex-ante 0DTE VRP positive on mean and median but "not directly tradeable." — [OptionMetrics](https://optionmetrics.com/?p=3155)
- A 2025 SPX 0DTE study: implied jump-risk premium ≈ 2× the diffusion-vol premium (via search summary; paper not retrieved). — [search summary](https://optionmetrics.com/?p=3155)
- Numerix: backtests using daily/30-min snapshots "fail to capture intraday swings"; most 0DTE backtests ignore bid-ask, slippage, liquidity. — [Numerix white paper](https://www.numerix.com/sites/default/files/file/2026-01/Numerix_White_Paper_0DTE_Trading_Strategies.pdf)
- Vol Vibes: 1-DTE (overnight) vs 0-DTE (RTH open) straddle legs — relative outperformance 2018–20, "largely in line after mid-2022" when overnight/intraday vol balanced; details paywalled. — [Vol Vibes](https://volvibes.substack.com/p/daily-intraday-spx-straddle-performance)
- tastylive: no intraday/one-hour straddle study; management rule is 25% of max profit for straddles, 50% for strangles (45-DTE context). — [tastylive](https://tastylive.com/shows/market-measures/episodes/managing-short-straddles-how-early-is-too-early-04-10-2018)
- Option Alpha 0DTE: profitable traders' modal pattern = enter ~10:15 ET, exit ~12:00 ET (2-hour hold), neutral structures. — [Option Alpha](https://optionalpha.com/blog/0dte-options-strategy-performance)

### Inferences
- Transferable test: a *conditional* 0DTE straddle (e.g., only sell when realized intraday vol/skew signal is favourable) rather than fixed-time; and a 2-hour mid-morning (10:15–12:15 IST analogue) hold window with 15% TP / 25% SL.
- Our existing 9:20 Nifty straddle success vs. Vilkov's null result may reflect the India-specific higher IV/RV gap or simply a favourable sample; worth re-checking across the 2023 daily-expiry regime vs post-Nov-2024 regime.

### Gaps
- Could not retrieve the SSRN PDF for per-strategy tables (win rate / PF) — SSRN returned 403.

---

## Key Question 5 (pitfalls): costs, STT, slippage, data traps

### Takeaway
India round-trip charges make tick/10-point futures scalps need ~87% win rate to break even (Marketcalls math); STT on futures was raised 0.02%→0.05% from 1 Apr 2026, pushing Nifty futures breakeven from ~6 to ~13 pts per lot; ITM long index options held to expiry pay STT on intrinsic value (0.125–0.15%, sources conflict); 0DTE backtests are routinely wrong on fills and on expiry-day data gaps.

### Cited Findings
- **Nifty futures round trip (50 units, pre-April-2026)**: brokerage ₹40 + statutory ₹365.89 = **₹405.89**, breakeven ~7.3 pts; 2–3 pt spread in fast markets + 1–2 pt slippage → ~12–13 pts all-in; on a 10-pt target, expectancy at 50% win = −₹383/trade; breakeven win rate ≈ 87%. **Nifty options (200 units)**: ₹40 + ₹124.67 = **₹164.67**, breakeven ~0.62 pts premium. — [Marketcalls](https://www.marketcalls.in/learnings/why-scalping-just-10-points-in-nifty-futures-options-isnt-as-easy-as-it-sounds.html)
- **Post-1-Apr-2026 STT hike**: futures sell-side STT 0.02%→0.05%; Nifty futures (lot 65) charges ~₹392→~₹837 per lot, breakeven ~6→~13 pts; Bank Nifty ~10.4→~26 pts. — [Moneylife via search](https://mas360.moneylife.in/article/derivatives-trading-gets-costlier-from-1-april-2026/4874.html) (page 403'd; numbers from search summary); [Finnovate](https://www.finnovate.in/learn/blog/budget-2026-stt-hike-fno-trades-explained)
- A second source estimates only ₹65–75 (17–20 ticks) per Nifty futures round trip — conflicts with Marketcalls; depends on STT treatment/broker plan. — [OneTradeJournal](https://onetradejournal.com/learn/scalping-vs-intraday-trading)
- **STT on exercise**: ITM index options auto-exercised at expiry; STT on intrinsic value — Zerodha pages state **0.15%** on one FAQ and **0.125%** on another (conflict); seller pays no further STT; since Sep-2019 STT is on intrinsic (not notional), so the old "STT trap" is much smaller but still exceeds sell-side STT on premium. — [Zerodha FAQ](https://support.zerodha.com/category/trading-and-markets/trading-faqs/f-otrading/articles/options-on-expiry-day); [Zerodha Z-Connect](https://zerodha.com/z-connect/?p=125); [Zerodha bulletin 2017](https://zerodha.com/marketintel/bulletin/53041/square-off-your-itm-in-the-money-options-and-avoid-paying-excess-stt)
- Structural breaks for multi-year tests: Nifty lot 25→75→65; weekly expiries retained only on Nifty (NSE) and Sensex (BSE); Nifty expiry moved Thursday→Tuesday; STT on option sells raised twice. — [search summary / Marketcalls](https://www.marketcalls.in/?p=61524)
- Slippage: most platforms default slippage to zero; on expiry days SL fills "may be significantly worse than anticipated." — [Marketcalls slippage](https://www.marketcalls.in/system-trading/understanding-slippage-and-its-impact-on-trading-strategy-performance.html); [OneTradeJournal](https://onetradejournal.com/platforms/backtest-vs-live-results)
- Sahi quotes 5–10 pt slippage on market exits on expiry (unsourced). — [Sahi](https://www.sahi.com/blogs/nifty-expiry-day-strategies-scalping-guide) **[CLAIM]**
- Data trap: some NSE intraday option feeds stop publishing bars the day before expiry (Nifty 5-min confirmed). — [Nubra](https://pypi.org/project/nubra-backtest-engine/)
- Zerodha's own published straddle/strangle study is 45-DTE (not intraday), with VIX filter; flags gap risk and leverage. — [search summary](https://tradingqna.com/t/intraday-bank-nifty-short-straddle-short-strangle/38046) (Zerodha study not fetched)

### Inferences
- With post-April-2026 costs, a Nifty futures scalp needs ≥13 pts gross per round trip just to break even before slippage; 1-min/3-min VWAP-bounce scalps targeting 10–20 pts are structurally dead. Only option *premium* scalps (breakeven ~0.6–1 pt premium) have room.
- For 0DTE buying scalps that end ITM, always sell on exchange rather than let exercise; for sellers it's irrelevant.

### Gaps
- Exact current (post-April-2026) option charge stack per lot not retrieved (Moneylife 403).
- No SEBI breakdown of losses by holding time.

---

## Consolidated list of concrete, untested rule-sets to put in our backtester (all currently unproven after costs)

| # | Rule-set | Entry | Strike | Exit/Target | Stop | Time exit | Source status |
|---|---|---|---|---|---|---|---|
| 1 | Sensex/Nifty 0DTE 1 PM short straddle | 13:00 on expiry | ATM CE+PE | buy back at −30% combined premium | none in source (add 25–30% leg SL) | 15:20 | 63% WR, ₹77.6k/15mo on ₹3.2L, costs unstated — [Aliceblue](https://aliceblueonline.com/blog/sensex-0dte-strategy-1lyalgos-complete-guide-for-2026) |
| 2 | Mid-morning 2h neutral (OA profitable-user pattern) | ~10:15 | ATM straddle or iron fly | +15% of credit | −25% | 12:00–12:15 | US pattern only — [Option Alpha](https://optionalpha.com/blog/0dte-options-strategy-performance) |
| 3 | ORB → sell far-side credit spread | break of 60-min (or 15/30) range, range ≥0.2% of open, before 12:00 | short strike at/beyond opposite range edge, wide wing | hold to close | none | 15:20 | SPX 89% WR PF 1.44 gross — [Option Alpha](https://optionalpha.com/blog/opening-range-breakout-0dte-options-trading-strategy-explained) |
| 4 | Expiry ORB option buy | 9:15–10:00 ORB break + volume spike + VWAP side | ATM | +20–30 pts premium | −30% premium | 30 min | no data — [Sahi](https://www.sahi.com/blogs/nifty-expiry-day-strategies-scalping-guide) |
| 5 | RSI-50 ATM buy | RSI>50 buy CE / <50 buy PE | ATM | +50% premium | −25% premium | EOD | 53% WR, 829 trades, gross — [Multibagg](https://www.multibagg.ai/market-pulse/articles/nifty-algo-backtest-results-2026-cmrg191cpjai5np0jleu5s47x) |
| 6 | 11:00–13:00 OTM call credit spread (range day) | 11:00 | sell CE 150–200 pts OTM, buy +50 | 50% of max profit | spread width | 13:30 | no data — [Sahi](https://www.sahi.com/blogs/nifty-expiry-day-strategies-scalping-guide) |
| 7 | 15-min VWAP futures | 15-min candle touches & closes above VWAP, enter on break of high | futures | +30 pts | −20 pts | 15:14, 1 trade/day | **negative after costs** 2011–19 — [Marketcalls](https://www.marketcalls.in/?p=51686) |
| 8 | 1 PM BN straddle, per-leg SL, exit 3 PM | 13:00 daily | ATM | – | per-leg SL (arbitrary) | 15:00 | no results — [TradingQnA](https://tradingqna.com/t/bank-nifty-straddle-backtest-in-streak/136147) |
| 9 | 2:30–3:15 BN long straddle (volatility pop) | 14:00–14:30 | ATM | – | – | 15:15 | anecdote only — [TradingQnA](https://tradingqna.com/t/intraday-bank-nifty-short-straddle-short-strangle/38046) |

Priority for our own costed test (by evidence strength): #1 (with SL added) > #3 > #2 > #6 > #4/#5. Also compute Nifty 0DTE ATM-straddle decay-by-hour curve from our minute data (Q2 gap), bucketed expiry vs non-expiry and pre/post Nov-2024 weekly-expiry rationalisation.
