# Daily-runnable systematic strategies on Indian index derivatives — Round 2 (non-expiry-day families)

Scope: families 1–7 from the brief. Evidence tags: **COSTED** = result reported after brokerage/STT/slippage; **GROSS ONLY** = backtest with no costs; **CLAIM** = vendor/forum assertion without verifiable numbers; **LOCAL** = computed in this session from the repo's own `data/parquet/minutes_1/NIFTY50.parquet` (1-min, 2022-01-03 → 2026-10-23, 1,192 sessions) and `data/external/india_vix_daily.parquet`. Research date: 2026-10-27.

Headline: across ~35 searches/fetches I found **zero** independent, cost-adjusted, 2023–2026 backtests showing a non-expiry-day index-option or index-futures intraday system with positive expectancy. The only costed results found (Marketcalls VWAP on Nifty futures, QuantInsti cointegration pairs) are negative or ~zero after costs. Everything positive is GROSS ONLY or CLAIM. The one genuinely new, quantitative input here is the LOCAL gap/VIX conditioning data, which bounds the overnight-selling family.

---

## 1. Overnight short strangle/straddle (sell ~15:20, buy back ~9:20)

### Takeaway
No published cost-adjusted backtest of a 15:20→09:20 Nifty short straddle/strangle exists in the public sources searched. LOCAL data: the overnight window carries 43% of total daily variance (std 0.575% overnight vs 0.661% for 9:20–15:20), so the "theta-for-free" premise is weak; weekend/holiday gaps are ~2.5× as likely to exceed 1% as single-night gaps, and the tail (−4.5% on 2025-04-07) is a multi-week-premium loss.

### Cited Findings
- No public backtest of the exact overnight window was found; Stratzy "Short Strangle Overnight" algos on Dhan show blank metrics — [Dhan/Stratzy Bazaar Overnight](https://dhanhq.co/algos/managers/stratzy/bazaar-short-strangle-overnight/6999e494918d3e58dc31f871); [Homecoming Overnight](https://dhanhq.co/algos/managers/stratzy/homecoming-short-strangle-overnight/69988df1b36043d450294e73). **CLAIM (no numbers).**
- Closest costed-adjacent positional result: an OptionsIQ vendor PDF reports shorting ATM+100 CE on expiry eve (Feb 2019–Nov 2023): 247 trades, ~81% wins, CAGR 6.5%, max DD −7.9%; costs not stated, vendor pitch — [OptionsIQ PDF](https://optionsiq.substack.com/api/v1/file/e360eb84-5531-4c31-8c7c-30cfbd9d25ea.pdf) (redirects to signed S3; contents seen only via search snippet). **GROSS ONLY / CLAIM.**
- Zerodha "In The Money" tested selling Nifty straddle/strangle at 45 DTE over 7+ years with a VIX filter; teaser page gives no numbers and flags "gap risk, drawdowns, and the danger of using too much leverage" — [Zerodha Aftermarket Report](https://aftermarketreport.zerodha.com/p/new-week-same-range-bound-session); series at [inthemoneybyzerodha.substack.com](https://inthemoneybyzerodha.substack.com/). **CLAIM (numbers not retrievable).**
- Long-run gap frequency (20+ yrs, Nifty): 82 gap-downs < −1% and 131 gap-ups > +1%; avg open-to-close after gap-down +0.32%, after gap-up −0.04% — [TradingQnA](https://tradingqna.com/t/trading-the-gap-how-does-one-trade-nifty-bank-nifty-during-gap-down-and-gap-up-days/78838). **GROSS ONLY (forum).**
- **LOCAL gap statistics, Nifty 50, 15:20 close → next-day 09:20 close, n=1,181 (Jan 2022–Oct 2026):**
  - mean +0.044%, std 0.575%, mean |move| 0.389%, median |move| 0.274%
  - |move| > 0.5%: 287 (24.3%); > 0.75%: 146 (12.4%); > 1.0%: 83 (7.0%); > 1.5%: 35 (3.0%); > 2.0%: 15 (1.3%); > 3.0%: 3 (0.3%)
  - By year, count of |move|>1% / sessions: 2022 43/245; 2023 2/244; 2024 9/245; 2025 8/247; 2026 (to 23 Oct) 21/200. Yearly std: 0.76%, 0.36%, 0.45%, 0.51%, 0.72%.
  - Single-night (consecutive trading days, n=897): std 0.493%, >1% in 5.0%. Weekend/holiday (n=284): std 0.777%, >1% in 13.4%.
  - Worst: 2025-04-07 −4.47%; 2026-03-09 −2.78%; 2022-02-14 −2.53%; 2022-03-07 −2.27%; 2022-06-13 −2.14%; 2026-03-04 −2.08%; 2024-06-04 −2.02%. Best: 2026-04-08 +3.37%; 2026-02-03 +3.05%; 2024-06-03 +2.54%.
  - Open-vs-prior-close gap (conventional definition, n=1,191): >1% on 72 days (6.0%), >2% on 15 (1.3%), >3% on 4; worst 2025-04-07 −5.04%.
  - Overnight share of daily variance = 43% (overnight std 0.575% vs 9:20→15:20 std 0.661%).
  - Source: repo file `data/parquet/minutes_1/NIFTY50.parquet` (session computation; script not saved).
- Margin: a Dec-2024 forum post states a near-ATM naked 1-lot (75 qty) Nifty short straddle needed ~₹2.36 lakh; converting to an iron fly cut it to ~₹93.7k — [TradingQnA 920 thread](https://tradingqna.com/t/reports-of-the-death-of-920-short-straddle-are-greatly-exaggerated/179061). **CLAIM (user report; lot is now 65).** Zerodha defines NRML margin = SPAN + exposure − spread benefit, with premium credited — [Zerodha Z-Connect](https://zerodha.com/z-connect/?p=2114). A 1LyAlgos vendor page cites ₹3.2 lakh margin for 1 lot Sensex straddle (2026) — [Aliceblue](https://aliceblueonline.com/blog/sensex-0dte-strategy-1lyalgos-complete-guide-for-2026). **CLAIM.**
- SEBI framework affecting overnight carry into expiry: 2% additional ELM on short index options **on their expiry day** (effective 20 Nov 2024; applies to positions open at start of the day and opened that day), computed as 2% × underlying × lot; calendar-spread margin benefit removed on expiry day for the expiring contract (effective 10 Feb 2025); intraday position-limit monitoring from 1 Apr 2025 — [Zerodha Z-Connect](https://zerodha.com/z-connect/?p=391917). So a Mon-15:20 → Tue-09:20 Nifty carry is hit by the extra 2% ELM on Tuesday morning.
- STT from 1 Apr 2026: futures 0.02% → 0.05% (sell side); options premium 0.1% → 0.15%; exercise 0.125% → 0.15% — [5paisa](https://www.5paisa.com/news/stt-hike-on-fo-to-take-effect-from-april-1-amid-rising-options-activity); [Outlook Money](https://www.outlookmoney.com/invest/budget-2026-market-experts-suggest-stt-hike-likely-to-dent-trading-volumes-by-20-30).

### Inferences
- With overnight realised std ≈ 0.58% vs an ATM 1–6 DTE straddle's overnight theta, the structural edge is at best the VRP (implied daily σ ≈ VIX/√252 ≈ 0.72–1.22% vs realised overnight σ 0.33–0.84% by VIX tercile; see §2), minus ~2 round-trips of costs per day and gap tail. The 2022 and 2026 regimes (std ≥0.72%) would likely have wiped out several months of 2023-style gains.
- Weekend carry (Fri→Mon) has 2.7× the >1% gap frequency of a weeknight; "capture weekend theta" is therefore the riskiest variant, not the best.
- Tuesday-morning buyback of a Monday-sold weekly straddle will require the extra 2% ELM at open on expiry day — plan margin at ~1.2× normal.

### Gaps
- No costed overnight backtest found anywhere (AlgoTest/Stockmock/Tradetron public pages, Zerodha, QuantInsti, SSRN). The repo's 1-min option data can answer this directly; recommend running 15:20→09:20 with 0.15% STT on sell premium + slippage.
- Current rupee NRML margin for 1 lot (65) Nifty strangle not found in a dated 2026 source; use broker calculator.

---

## 2. IV-vs-realised-vol filters for DTE 1–6 intraday selling

### Takeaway
No published Indian evidence that a VIX/IV-percentile filter turns non-expiry-day intraday selling positive after costs. Academic work confirms a positive Nifty variance risk premium, and LOCAL data shows implied daily σ exceeds realised intraday σ in every VIX tercile — but the premium is widest in *low* VIX in absolute-ratio terms and the high-VIX bucket is where >1% moves cluster (20% of days), i.e. a VIX filter mostly removes tail days, not the cost drag.

### Cited Findings
- Sankar, Ramachandran & Lukose (2020, IREF): variance risk premium is priced in India despite high retail participation; only past continuous variance forecasts short-term synthetic variance-swap returns — [Manipal repository](https://researcher.manipal.edu/en/publications/dynamics-of-variance-risk-premium-evidence-from-india/). **Academic, not a trading backtest.**
- LinkedIn-posted study (Arsh Hora, Apr 2021–Jul 2025, daily Nifty/India VIX): VRP positive and significant; short-VIX-futures, synthetic short-variance and delta-hedged ATM straddles "profitable in normal regimes, concentrated losses in vol shocks" — [LinkedIn profile](https://in.linkedin.com/in/arshhora). **CLAIM (no paper retrieved, costs unknown).**
- IV percentile as a straddle entry filter (SPY, Feb 2021–Feb 2026): best variant +10.8% total, Sharpe 0.46, MaxDD 8.9% — "profitable but far behind z-score timing" — [IVolatility](https://www.ivolatility.com/news/3131). **Non-Indian; GROSS ONLY.**
- Theta-Edge claims IVR/IVP>50 filter lifted short-iron-condor win rate 48.2% → 56.8%, no period or market stated — [thetaedge.ai](https://thetaedge.ai/blog/iv-rank-vs-iv-percentile-key-differences). **CLAIM.**
- Sensibull: IV percentile "is not a magic number"; mean-reversion trades work when extreme IV is not persistent — [Sensibull blog](https://blog.sensibull.com/2018/11/25/how-high-is-high-the-iv-percentile/).
- AlgoTest's generic straddle backtest guide uses 10:15 entry, 35–50% per-leg SL, and warns drawdowns rise on trending days; no VIX-filter numbers — [AlgoTest](https://algotest.in/blog/how-to-backtest-options-trading-strategies-with-examples.md). **CLAIM.**
- **LOCAL (Nifty, 2022–2026, India VIX close terciles; implied daily σ = VIX/√252):**
  - Intraday 09:20→15:20: low VIX (9.2–12.7) realised std 0.421% vs implied 0.723%, >1% moves 1.0% of days; mid (12.7–15.6) 0.641% vs 0.883%, >1% 12.4%; high (15.6–32) 0.851% vs 1.219%, >1% 20.3%.
  - Overnight 15:20→09:20: low 0.333% vs 0.723%, >1% 0.3%; mid 0.425% vs 0.883%, >1% 3.0%; high 0.837% vs 1.219%, >1% 17.7%.
  - Previous-day range terciles vs overnight move: quiet (avg range 0.54%) → overnight std 0.382%, >1% 2.0%; mid → 0.516%, 5.3%; wild (1.56%) → 0.762%, 13.7%.

### Inferences
- Realised/implied ratio is ~0.58 (low VIX), ~0.73 (mid), ~0.70 (high) intraday, so the *relative* premium is largest in low-VIX regimes — consistent with the user's finding that quiet-day filters didn't rescue DTE 1–6 selling: low VIX also means tiny absolute premium, so fixed per-lot costs (brokerage + 0.15% STT + spread) dominate.
- A VIX filter is primarily a tail-trimmer (removes 17–20% ">1%-move" days); any strategy whose non-expiry losses come from cost drag rather than tails will not be rescued by it.

### Gaps
- No AlgoTest/Stockmock/Tradetron public result for a VIX-conditioned non-expiry straddle was retrievable (their results pages are behind login). No SSRN paper with cost-adjusted Nifty short-vol conditioning found.

---

## 3. Delta-hedged / adjusted short straddles intraday

### Takeaway
No cost-adjusted intraday adjustment backtest found. The only academic test (Univ. of Vaasa MSc, 2025) finds both long and short initial-delta-neutral Nifty straddles have **negative Sharpe**; weekly shorts "steadier" than monthly.

### Cited Findings
- Lalit Kumar (2025, Univ. of Vaasa MSc thesis, "Profitability of Initial Delta Neutral Strategies… Nifty 50"): long and short initial delta-neutral straddles both have negative Sharpe ratios; weekly short straddles steadier than monthly; limited sample flagged — [OSUVA record](https://osuva.uwasa.fi/handle/11111/19466) (full PDF blocked by bot protection; summary via search snippet). **Costs unstated.**
- AlgoTest re-entry logic documented (re-enter new ATM after SL, optionally flipping to long) but no results published — [AlgoTest glossary](https://algotest.in/blog/definition-of-terms-used-in-backtesting-platform.md); adjustment-trigger heuristic "within 50–75 pts of strike, per-leg SL 40–60%" — [AlgoTest guide](https://algotest.in/blog/how-to-backtest-options-trading-strategies-with-examples.md). **CLAIM.**
- AlgoTest warns that ignoring brokerage, taxes and slippage makes simulated P&L look better than live — same source.
- QuantConnect delta-hedge examples found are SPY only, code-only, no stats — e.g. [QuantConnect](https://www.quantconnect.com/terminal/cache/embedded_backtest_c8dc908c35a3a7842239c03c51e0a283.html). **Not applicable.**

### Inferences
- Every adjustment adds a round-trip (brokerage + 0.15% STT on the sold premium + spread). With ATM 1–6 DTE Nifty premiums ~₹150–300 and lot 65, each adjustment costs roughly 0.5–1% of straddle premium; adjustment-heavy systems are structurally worse after costs than the plain straddle the user already found losing.

### Gaps
- No cost-adjusted Indian result for "shift untested leg" or band-rehedging found.

---

## 4. Intraday pairs / stat-arb (NSE large caps; Nifty–BankNifty; Nifty–Sensex)

### Takeaway
The only costed Indian pairs study found (QuantInsti EPAT, 2016–2025, daily, 5 bps/leg/side) returns 0.30% annualised, Sharpe 0.09, MaxDD −34% — effectively zero. Nothing intraday or post-2022 with costs exists for index pairs.

### Cited Findings
- QuantInsti EPAT project: 25 NSE large caps, walk-forward (252-day train / 21-day step), Jan 2016–Jun 2025, 3 pairs (HDFCBANK/KOTAKBANK, HEROMOTOCO/ULTRACEMCO, HCLTECH/ICICIBANK), costs 5 bps per leg per side: annualised return 0.30%, Sharpe 0.089, MaxDD −34.31%, win ratio 63.47%, 271 trades — [QuantInsti blog](https://blog.quantinsti.com/cointegrated-pairs-trading-indian-equity-market-epat-project/). **COSTED — ≈0 net.**
- Marketcalls Nifty/BankNifty pair AFL prototype: brokerage ₹400 per round trip for 2 lots each, 11.61% CAGR since 2008, author calls it "just a sample prototype"; results shown per-leg not pair-level — [Marketcalls](https://www.marketcalls.in/amibroker/pair-trading-amibroker-afl-code.html). **COSTED but pre-2020, prototype, not pair-level.**
- IIMB thesis: pairs attractive only with very low transaction costs; suggests same-sector derivatives — [IIMB repository](https://repository.iimb.ac.in/handle/2074/18231). **Academic, no 2022+ numbers.**
- Nifty futures–spot mispricing (2002–2004): 0.34% avg after-cost arbitrage on 37% of days for NSE members — [Vipul, SAGE](https://journals.sagepub.com/doi/abs/10.1177/0256090920050403). **COSTED but 20 years old, member-level costs.**
- Nifty–Sensex cross-exchange spread: no backtest found. Exchange fee asymmetry: BSE futures 0%, NSE 0.00183%; BSE options 0.005%, NSE 0.0355% — [TradeBrains](https://tradebrains.in/fo-market-is-bse-the-new-preference-for-fo-traders/).

### Inferences
- Nifty vs Sensex futures are ~0.99-correlated with overlapping constituents; any spread is tiny relative to two futures round-trips (now 0.05% STT each sell side) — not viable for retail.

### Gaps
- No 2022–2026 intraday pairs result with costs on NSE large caps or index futures found.

---

## 5. Index futures intraday systems (VWAP, mean reversion, trend)

### Takeaway
The only Indian costed study found (Marketcalls, Nifty futures 2011–2019, 15-min VWAP breakout, 30-pt target/20-pt SL) is profitable gross and **unprofitable after commissions and slippage**; BankNifty variant loses even gross. Nothing costed post-2024 exists.

### Cited Findings
- Marketcalls VWAP intraday (Nifty & BankNifty futures, Jan 2011–Dec 2019, 15-min; buy on break of high of bullish candle that closed above VWAP, target 30/90 pts, SL 20/60, one trade/day, square-off 15:14:59): Nifty profitable before costs, not after "reasonable commissions and slippages"; BankNifty not profitable even before costs; rates not stated — [Marketcalls Part 4](https://www.marketcalls.in/amibroker/vwap-intraday-trading-strategy-do-simple-trading-strategies-really-work-part4.html). **COSTED — negative.**
- Marketcalls BTST (buy close, sell next open, 2011–Jun 2018): 595% with zero costs; costed version at 0.02% not shown — [Marketcalls Part 2](https://www.marketcalls.in/amibroker/buy-at-todays-close-and-sell-at-next-day-open-do-simple-trading-strategies-really-work-part2.html). **GROSS ONLY.**
- QuantInsti transaction-cost article: 10 bps/trade turns a small gross profit to a loss, Sharpe → ~0; Indian explicit costs higher than expected due to STT; futures STT 0.05% from 1 Apr 2026 — [QuantInsti](https://www.quantinsti.com/articles/transaction-costs-automated-trading/).
- A QuantConnect reproduction of a VWAP-crossover study on QQQ: out-of-sample Sharpe decays to ~0.7 and "the edge disappears under realistic retail transaction costs" — [QuantConnect](https://www.quantconnect.com/terminal/cache/embedded_backtest_b115d0894231d55994b1068202f6c0ae.html). **Non-Indian.**
- No QuantInsti EPAT project matching "Nifty futures intraday + Sharpe + costs + 2024" was found; listings include TSMOM futures and gap-trading equity projects — [QuantInsti EPAT projects](https://blog.quantinsti.com/tag/epat-trading-projects/page/2/).

### Inferences
- With 2026 STT on futures at 0.05% of sell value (≈₹7.3 per ₹14.7 lakh contract… i.e. ~₹735 per lot round-trip for Nifty at 22,600 × 65) plus spread/slippage, a 1-trade/day futures system needs >~0.1% average gross edge per trade; no published Indian system clears that.

### Gaps
- No costed post-2024 Nifty/BankNifty futures intraday system found anywhere (Marketcalls, QuantInsti, SSRN, TradingView scripts give no verified net figures).

---

## 6. Rotating expiry days across indices; liquidity in Sensex/Bankex/FinNifty

### Takeaway
As of Oct 2026 there are exactly two weekly 0DTE sessions per week: Nifty (NSE, Tuesday) and Sensex (BSE, Thursday). BankNifty/FinNifty/Midcp/NiftyNext50 are monthly (last Tuesday); Bankex/Sensex50 monthly (last Thursday). So a "rotate across indices" scheme yields at most 2 weekly + ~2 monthly 0DTE days per month, not daily. Sensex 0DTE liquidity is adequate on expiry day (BSE took 55% notional / ~34% premium share in Apr 2026) but no bid-ask or OI data was found; Bankex/FinNifty weeklies no longer exist.

### Cited Findings
- SEBI Oct-2024 circular: one weekly-expiry benchmark per exchange, effective 20 Nov 2024; NSE kept Nifty, BSE kept Sensex; BankNifty, FinNifty, Midcp Select, NiftyNext50, Bankex, Sensex50 weeklies discontinued — [Zerodha Z-Connect](https://zerodha.com/z-connect/?p=391917); [Zerodha support](https://support.zerodha.com/category/trading-and-markets/trading-faqs/f-otrading/articles/weekly-expiries-discontinued-for-certain-index-derivatives).
- SEBI 26 May 2025 circular: each exchange designates Tuesday **or** Thursday for all equity-derivative expiries; NSE → Tuesday, BSE → Thursday, effective 1 Sep 2025 — [Business Today](https://www.businesstoday.in/markets/stocks/story/nse-receives-sebi-nod-for-tuesday-expiry-bse-thursday-480736-2025-06-17); [Moneylife](https://moneylife.in/article/sebi-tightens-equity-derivatives-rules-asks-exchanges-to-pick-tuesday-or-thursday/77245.html); [AlgoTest Oct 2026](https://algotest.in/blog/all-index-expiry-day.md).
- Current expiry table: Nifty weekly Tue; Sensex weekly Thu; BankNifty/FinNifty/Midcp/NiftyNext50 monthly last Tue; Bankex monthly last Thu; Sensex50 monthly; holiday → prior trading day (e.g. Sensex expiry moved to Wed 27 May 2026 for Bakri Id) — [PhonePe/Share.Market](https://www.phonepeinvest.com/buzz/insights/weekly-expiry-days-in-indian-fo-markets/).
- Lot sizes from Jan-2026 series: Nifty 65 (from 75), BankNifty 30 (from 35), FinNifty 60 (from 65), Midcpnifty 120 (from 140), NiftyNext50 25, Sensex 20 (from 10 earlier in 2025) — [Sahi](https://www.sahi.com/blogs/nifty-lot-size-2026-bank-nifty-sensex); Bankex 30 — [AlgoTest Bankex](https://algotest.in/blog/bankex-expiry/); [StockMojo](https://stockmojo.in/fno-lot-size). Nov-2024 revision for reference: Nifty 25→75, BankNifty 15→30, FinNifty 25→65, Midcp 50→120, NiftyNext50 10→25, Sensex 10→20, Bankex 15→30, Sensex50 25→60 — [Zerodha Z-Connect](https://zerodha.com/z-connect/?p=391917). (Sources disagree on BankNifty's intermediate 35 step; verify on NSE.)
- BSE vs NSE F&O share, Apr 2026: BSE 55.4% vs NSE 44.6% on **notional**; NSE ~66% on **premium** turnover — [TradeBrains, 4 May 2026](https://tradebrains.in/fo-market-is-bse-the-new-preference-for-fo-traders/). NSE index-options premium share 66.7% (Jan 2026) → 72.1% (Mar 2026); April dip attributed to 2 of 4 NSE Tuesday expiries lost to holidays; NSE claims "tighter spreads" but no spread data given — [Business Today, 15 May 2026](https://www.businesstoday.in/opinion/story/behind-the-numbers-why-nses-derivatives-dominance-remains-intact-531683-2026-05-15).
- 2023 Geojit snapshot: Sensex options = 99.998% of BSE derivative contracts; 95% of weekly trades on expiry day (then Friday) — [Geojit](https://insights.geojit.com/2023/09/29/sensex-options-tides-rising/). Bankex weekly last traded 18 Nov 2024 — [Bajaj Broking](https://bajajbroking.in/blog/nse-to-end-weekly-expiry-for-bank-nifty-fin-nifty-and-midcap).
- Exchange transaction fees: BSE options 0.005% vs NSE 0.0355% of premium; BSE futures 0% vs NSE 0.00183% — [TradeBrains](https://tradebrains.in/fo-market-is-bse-the-new-preference-for-fo-traders/); option fee ₹325/₹1 mn premium (BSE) vs ₹350 (NSE) — [Swastika](https://www.swastika.co.in/blog/sensex-share-price-outlook-bse-market-share-adto-trends-and-investor-action).
- Aug 2026: options ADTO down 14% (NSE) / 12% (BSE) vs July; Jefferies flags RBI bank-guarantee norms could cut premium turnover up to 10% — [Swastika](https://www.swastika.co.in/blog/sensex-share-price-outlook-bse-market-share-adto-trends-and-investor-action).

### Inferences
- A Tue (Nifty) + Thu (Sensex) 0DTE rotation gives ~8–9 sessions/month; adding monthly expiries (last Tue: BankNifty/FinNifty/Midcp; last Thu: Bankex) adds ~2 more but with only monthly-series liquidity. Mon/Wed/Fri remain structurally non-expiry.
- Sensex expiry-day liquidity is adequate near ATM (BSE carries roughly a third of national premium turnover, almost all of it in Sensex); off-expiry Sensex and all Bankex/FinNifty/Midcp series should be assumed thin.

### Gaps
- No bid-ask spread or OI depth statistics for Sensex/Bankex/FinNifty 0DTE were found; need BSE/NSE bhavcopy or live order-book sampling.
- Business Standard Sept-2025 explainer was 403-blocked; weekday mapping taken from AlgoTest/PhonePe instead.

---

## 7. Anything else credible that runs daily with ≥55% win rate and costed positive expectancy

### Takeaway
Nothing found that is both daily and costed-positive. The only ≥55%-win results with numbers are 0DTE (Sensex 1:00 PM straddle, 63% win, vendor, costs unstated) and gross intraday straddles. "Calendar/diagonal intraday" has no Indian backtests at all.

### Cited Findings
- 1LyAlgos Sensex 0DTE (via Aliceblue, Aug 2026): sell ATM CE+PE at 13:00 Thursday, exit 15:20 or when combined premium −30%; 15-month backtest, 63.32% wins, ₹77,603 net on ₹3.2 lakh margin (~24%); Aug 2026 live ₹6,684 on 4 expiries (~2.1%); costs/slippage and drawdown not stated — [Aliceblue](https://aliceblueonline.com/blog/sensex-0dte-strategy-1lyalgos-complete-guide-for-2026). **CLAIM (vendor).** Consistent with user's own finding that Sensex 12:00 Thu works.
- TradingQnA Dec-2024 Nifty 9:20→15:15 straddle, 1-min data, no SL, **no costs**: 20 days, 60% win, +434 pts; non-expiry 10/16 wins (+269 pts), expiry 2/4 (+165 pts); worst −79 pts; commenters flag one-month sample and missing costs — [TradingQnA](https://tradingqna.com/t/reports-of-the-death-of-920-short-straddle-are-greatly-exaggerated/179061). **GROSS ONLY.**
- Bank Nifty expiry trades 2017–2020: hedged iron condor "ends up in loss after all cost"; a forum poster reports 30–40% capital fluctuations typical for BN expiry straddles — [TradingQnA iron condor](https://tradingqna.com/t/is-iron-condor-a-profitable-option-trading-strategy/81708). **COSTED — negative (hedged variant).**
- Nasdaq-100 1-day ATM straddle study: "results are poor for a consistent short strategy using 1-day options" (slippage 2 pts) — [Nasdaq](https://www.nasdaq.com/articles/1-day-nasdaq-100-money-straddle-performance-analysis). **Non-Indian, COSTED-ish, negative.**
- Dhan/Stratzy "Flux Strangle": overnight Nifty strangle 10:15–14:00 entry, 2% capital SL; metrics blank — [Dhan](https://dhanhq.co/algos/managers/stratzy/flux-strangle/683c57d0ed2623775f750342). **CLAIM.**
- No Indian intraday calendar/diagonal backtest found; SEBI removed calendar-spread margin benefit on the expiring leg on expiry day (10 Feb 2025) — [Zerodha Z-Connect](https://zerodha.com/z-connect/?p=391917) — which raises margin for any calendar that uses the 0DTE leg as the short.

### Inferences
- The consistent pattern across every source (and the user's own tests): edges that survive costs are concentrated in 0DTE gamma/theta hours; everything on DTE ≥1 is at best gross-positive and net-flat/negative. The practical daily "system" is therefore Tue Nifty 0DTE + Thu Sensex 0DTE (+ monthly-expiry Tuesdays/Thursdays), with Mon/Wed/Fri flat — unless the repo's own overnight test (§1) surprises.
- If testing the overnight family anyway, the LOCAL conditioning suggests the only candidate filter with real separation is the *combination* "low VIX tercile AND single-night (not weekend) AND quiet previous-day range" (overnight >1% frequency ≈0.3–2%), accepting that absolute premium in that regime is small.

### Gaps
- No reddit/IndianStreetBets thread with costed numbers surfaced via search.
- Zerodha In The Money 45-DTE/VIX-filter numbers not retrievable (video-only).
- Stockmock/AlgoTest/Tradetron result pages are login-gated; no public cost-adjusted non-expiry results found.
