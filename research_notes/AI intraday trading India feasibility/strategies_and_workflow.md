# Intraday Strategy Archetypes for NSE Retail Algo Traders (~₹1 lakh), Realistic Performance, and Where ML Adds Value

Research date: 2026-10-25. Scope: Indian NSE/BSE intraday, post-Nov-2024 SEBI F&O framework. "Backtested" and "live" results are labelled explicitly throughout. Almost every performance figure found is a self-published, unaudited backtest; no independently audited long-run retail track record was found.

---

## KQ1. Strategy families and sourced results (ORB, VWAP, momentum/gap, 9:20 straddle, condors/spreads, pairs, scalping) incl. crash-day behaviour

### Takeaway
Published Indian backtests exist mainly for time-based short straddles and ORB on Nifty/BankNifty; they show positive gross expectancy but win rates of 43–70%, average loss often 2–3x average win for straddles, and backtested max drawdowns of 6% (hedged/large-margin option selling) to 45–50% (naked spot ORB, option buying). VWAP, gap-momentum and intraday pairs have essentially no credible NSE backtests with net-of-cost results, and the pairs/stat-arb results that do exist go negative after Indian costs.

### Cited Findings

**Macro base rate (live, regulator data)**
- SEBI (Sep 2024): ~93% of >1 crore individual equity F&O traders lost money FY22–FY24; aggregate losses >₹1.8 lakh crore; average loss ~₹2 lakh; >75% of loss-makers kept trading — [Business Standard](https://www.business-standard.com/markets/news/over-93-retail-traders-lost-money-in-f-o-in-three-years-says-sebi-124092300853_1.html); [SEBI PR via AIBI (PDF)](https://aibi.org.in/Sebipr/Updated_SEBI_Study_Reveals_93_percentage_of_Individual_Traders_Incurred_Losses_in_Equity_F&O_between_FY22_and_FY24.pdf)
- Top 3.5% of loss-makers (~4 lakh traders) lost an average ₹28 lakh each incl. transaction costs — [Outlook Business](https://www.outlookbusiness.com/markets/sebi-moves-to-protect-investors-as-93-of-fo-traders-face-losses)
- Only ~7% of individual F&O traders were profitable over FY22–FY24; an even smaller share made >₹1 lakh after costs; FY25 (SEBI, Jul 2025): 91% lost, net losses ₹1,05,603 crore, up 41% from ₹74,812 crore in FY24 — [imrawal.com summary of SEBI studies](https://imrawal.com/Website/articles/sebi-fo-study-why-retail-traders-lose.html)
- SEBI intraday equity cash study (Jul 2024, FY23): 71% of individual intraday traders lost money; 80% among those doing >500 trades/yr; 76% among under-30s; loss-makers spent an additional 57% of their losses on trading costs vs. 19% of profits for profit-makers; sample = top-10 brokers' clients (~86% of individual clients) — [SEBI report (PDF)](https://www.sebi.gov.in/sebi_data/attachdocs/jul-2024/1721818140715.pdf); [Business Standard](https://www.business-standard.com/amp/markets/news/7-in-10-intraday-traders-in-equity-cash-suffered-losses-in-fy23-sebi-study-124072400975_1.html); [Moneylife](https://moneylife.in/article/7-out-of-10-individual-intraday-traders-in-equity-cash-segment-make-losses-sebi-study/74733.html)
- Nithin Kamath (Jan 2022): <1% of active traders beat a bank FD over a 3-year window — [OfficeChai](https://officechai.com/stories/less-than-1-of-stock-traders-make-more-returns-than-an-fd-over-a-3-year-period-zerodha-ceo/); Value Research argued even this overstates success — [Value Research](https://www.valueresearchonline.com/stories/50287/more-active-less-money/)
- Academic (Agarwal, Ghosh, Prabhala, Zhao, CFR WP 25-09, 2025): India has ~80% of global option contracts; retail dominates index options, trades short-term/0DTE directional bets and "make[s] significant losses"; lot-size increases and margins were offset by migration to small-ticket, riskier options — [IDEAS/RePEc abstract](https://ideas.repec.org/p/zbw/cfrwps/327125.html); [full PDF](https://www.ualberta.ca/en/finance-department/media-library/documents/vikas-agarwal.pdf). Search snippet of the paper reports retail option *selling* earned ~₹3 billion cumulative in normal times but lost ~₹11 billion during COVID, wiping out all gains — snippet only, not verified against full text (PDF text extraction failed locally).

**A. Opening Range Breakout (ORB) — backtested**
- BankNifty spot ORB 2015–2023 (self-published): 352% total return, max DD 48%, win rate 43%, R:R 1.54; author shows results before and after slippage/charges and flags the DD as "very high" — [saimohanreddy.com](https://saimohanreddy.com/orb-backtest-on-banknifty/) (page blocked direct fetch; figures from search snippet)
- BankNifty 2PM range-break 2010–2018 (TradingQnA): >17,000 points, 48% win rate, "transaction cost & slippages were not considered" — [TradingQnA](https://tradingqna.com/t/orb-opening-range-breakout-2pm-banknifty-intraday-strategy/39756)
- Zerodha "In The Money" Nifty weekly-option ORB, Jan 2022–Feb 2026, 9:15–11:15 range, ₹200-premium strikes, 20% SL per leg, post-costs with 0.2% slippage: **option buying** win rate ~48%, max DD ~45%, equity curve bumpy from Jan 2024 and not recovered from a mid-2024 drawdown; 2025 "rough". **Option selling** (₹3.5L margin/lot) all years positive, max DD ~6%, win rate only marginally better than buying, larger DDs in 2025; author says selling "may not be trade-ready as-is" — [In The Money by Zerodha](https://inthemoneybyzerodha.substack.com/p/how-to-trade-opening-range-breakout)
- US academic ORB (Zarattini & Aziz 2023, QQQ 5-min ORB): 24% hit rate, +0.13R/trade, 33%/yr at 4x leverage; charges commission but no spread/slippage, no OOS period — [MQL5 critical replication](https://www.mql5.com/en/blogs/post/776235); independent re-run on 5 index CFDs 2015–2026: gross reproduced on NQ, **net of costs no market distinguishable from zero, 4 of 5 negative** — same source. QuantConnect recreation of the 2024 "stocks in play" paper: Sharpe 2.4 but only for 2016 — [QuantConnect](https://www.quantconnect.com/research/18444/opening-range-breakout-for-stocks-in-play/)
- "15 price action patterns on Nifty/BankNifty, only 6 survived" (blog, methodology unverified) — [DataDrivenInvestor](https://datadriveninvestor.com/articles/i-backtested-15-price-action-patterns-on-nifty-banknifty-only-6-survived)

**B. 9:20 short straddle / strangle (the "0.5%/day" family) — backtested**
- BankNifty 9:20 straddle on AlgoTest, ~5 yrs: win rate 69%, max DD ~₹17,000 on ~₹0.9 lakh average capital; period not fully specified (Medium, 403 on direct fetch; figures from snippet) — [Medium](https://medium.com/@amit179.iitk2/optimized-920-straddle-strategy-to-get-more-than-80-return-annually-e977453dca80)
- Nifty weekly 2019–2024 straddle guide (QuintalMind, no data/method published): 9:20 entry 25% SL win rate ~65–70%, **average loss 2–3x average win**; 50% SL ~72–78%; hold-to-expiry no SL ~55–60%; 2020 COVID "destroyed many short straddle systems, with drawdowns of 30–50% of capital"; a gap/trending expiry can wipe 3–6 months of profit; live results "typically 15–30% worse than backtests"; Nifty straddle margin ₹1.5–2.5 lakh/lot; suggests ₹5–10 lakh minimum per lot — [QuintalMind](https://www.quintalmind.com/blog/time-based-straddle-strategy-nifty-options)
- Weekly BankNifty short straddle 9:45 w/ 25% SL (StockMock, calendar 2022): profit ₹29,746, max DD ₹−23,063 (i.e., DD ≈ 78% of the year's profit) — [SlideShare/StockMock](https://www.slideshare.net/slideshow/945-short-straddle-with-sl-25stockmockpdf/256122277)
- Streak user self-report: BankNifty straddle Apr 2020–Mar 2021, 30% SL, "62% profit after brokerage"; another poster warns of big single-day loss without SL; Streak backtests were limited to ~1 month of expired contracts in 2021 — [TradingQnA](https://tradingqna.com/t/options-streak-algorithmic-for-intraday-uncovered-short-straddle-trading/112663)
- AlgoTest documents the 920 straddle template (25% SL) and notes Nifty expiry moved Thursday → Tuesday from Sep 2025 (affects any expiry-day split) — [AlgoTest docs](https://docs.algotest.in/Time-Based-Algo-Trading/how-to-backtest/backtest-920-Straddle/)
- US analogue (consistent 1-day ATM NDX straddle seller) lost in both 2023 and 2024 — [Nasdaq](https://www.nasdaq.com/articles/ndx-1-day-atm-straddle-mid-year-performance-update)

**C. Crash days (live market data; no India-specific seller P&L found)**
- 4 Jun 2024 (election count): Nifty −1,379 pts (−5.93%) to 21,884.50; intraday >8% drawdown; India VIX +23.65% to 25.89 — [Multibagg](https://www.multibagg.ai/market-pulse/articles/nifty-june-four-crash-2024-cmvmpfycn000s2vpia6oq4kq8); [ICICI Direct](https://www.icicidirect.com/futures-and-options/news/nifty-june-futures-trade-at-premium/1518821). Zerodha's pre-event note warned against naked selling and illiquid strikes — [Zerodha](https://zerodha.com/z-connect/subtext/trading-options-on-election-results-day)
- 5 Aug 2024 (yen carry unwind): Nifty −2.7% to ~24,048; India VIX +42%, biggest jump in 9 years, to 20.4 — [Business Standard](https://www.business-standard.com/markets/stock-market-news/fear-gripped-equity-investors-lose-rs-15-trillion-sensex-nifty-fall-2-7-124080501212_1.html); [HDFC Sky](https://hdfcsky.com/blogs/market-wtf-by-sky/the-vix-spike-nobody-saw-coming)
- 7 Apr 2025 (tariff "Black Monday"): Nifty closed ~−3.98% at ~21,993 (one blog says −5.07%, inconsistent); intraday −1,160 pts; India VIX +55–60% to ~21.8–21.9; Nifty Metal −8%, IT −7%, smallcap −10% — [Business Standard](https://www.business-standard.com/markets/news/black-monday-on-dalal-street-why-nifty-sensex-crashed-today-125040700187_1.html); [HSBC AM flash (PDF)](https://www.assetmanagement.hsbc.co.in/assets/documents/mutual-funds/en/ab3c035e-446f-4ee5-a159-d34870674405/monday-market-flash-april-7-2025.pdf)
- COVID 2020: only quantification found is the (unverified) "30–50% of capital" straddle drawdown claim above and the Agarwal paper snippet (₹11 bn retail seller loss).

**D. VWAP mean reversion / VWAP trend — backtested (non-NSE only)**
- No NSE backtest with numbers found. Indian pages (MarketNetra, BottomStreet) give rules of thumb only (short at VWAP after gap-up, square off before 15:15) — [MarketNetra](https://marketnetra.in/blog/vwap-trading-strategy-indian-stocks-intraday-nse); [BottomStreet](https://bottomstreet.com/learn/what-is-vwap-trading-india/)
- US-data VWAP backtest: mean reversion "works in the short run but not the long run" — [QuantifiedStrategies](https://www.quantifiedstrategies.com/vwap-trading-strategy/); multi-asset VWAP suite average profit factor 1.3, Sharpe 0.09 (marketing page) — [TradeSearcher](https://tradesearcher.ai/strategies/2815-vwap-suite-trend-mean-reversion-with-adaptive-filters)

**E. Intraday momentum / gap on large caps — backtested**
- No credible NSE intraday gap-momentum backtest found. Indian momentum evidence is daily/monthly: Nifty 200 Momentum 30 18-yr ~14% CAGR vs ~10.4% Nifty 50 but −70% DD in 2008 — [BacktestIndia](https://backtestindia.com/blog/momentum-investing-india-backtest); 10-yr large-cap top-pick momentum ~2.2% CAGR vs Nifty 11.3% ("mostly noise") — [Thuztra](https://thuztra.com/research/momentum-investing-india-honest-backtest)
- Survivorship bias in Indian index backtests materially inflates results (Nifty Smallcap 250 study) — [arXiv](https://arxiv.org/pdf/2603.19380)

**F. Intraday pairs / stat-arb — backtested**
- 5-min NSE pairs (Jul–Sep 2026): none of 3 pairs cointegrated at 5%; SBIN/BANKBARODA +1.3% gross → **−3.7% after realistic NSE costs** — [GitHub avadhi3103](https://github.com/avadhi3103/Intraday-Pairs-Trading)
- 5 NSE IT stocks OU pairs 2019–2026 daily: +13.0%, Sharpe 0.88 after costs; most profit in 2019–21, edge faded — [GitHub AtharvaMistry](https://github.com/AtharvaMistry/ou-pairs-trading-nse)
- EPAT 25 large-caps 2016–2025: Sharpe 0.089, max DD −34.31% — [QuantInsti](https://blog.quantinsti.com/cointegrated-pairs-trading-indian-equity-market-epat-project/)
- PCA-residual stat-arb NSE 2015–2024: +32.9% zero-cost → −32.9% under full Indian costs; "no statistically supported tradable edge" — [GitHub kartikya2207](https://github.com/kartikya2207/quant-stat-arb); OpenAlgo course: in-sample net Sharpe 1.01 vs OOS 0.34 — [OpenAlgo](https://openalgo.in/stats-arb/the-brutal-reality-check)

**G. Microstructure scalping — why retail can't compete (live)**
- SEBI interim order 3 Jul 2025: Jane Street allegedly manipulated BankNifty expiry via constituent/futures buying-then-selling while holding larger options positions; 21 instances; ₹4,843.57 crore impounded; media estimate ~₹36,500 crore net profit (options gains ₹43–44k crore); Jane Street ~25% of BankNifty options volume in the period (commentary) — [Business Standard](https://www.business-standard.com/amp/markets/news/sebi-bars-jane-street-orders-rs-4844-cr-disgorgement-market-manipulation-125070400081_1.html); [Share.Market](https://www.share.market/buzz/futures-and-options/sebi-vs-jane-street-36500-crore-profit-a-massive-ban-what-you-need-to-know/)
- Nithin Kamath (Apr 2026): 60–70% of F&O turnover comes from 1–2% of traders — [Business Today](https://www.businesstoday.in/amp/markets/stocks/story/zerodhas-nithin-kamath-says-60-70-of-fo-volumes-come-from-just-1-2-traders-526999-2026-04-23)
- Measured Nifty/BankNifty ATM spreads: ~₹12–16 per lot (2021 blog) — [Medium niuhi](https://medium.com/@niuhi/algo-trading-execution-analysis-2d970d6c4aad); recent Nifty ATM quote 148/150 (₹2 spread ≈1.3%/side) and a 2026 market order filled ₹30 worse than ask (₹9,750 on 5 lots) — [Navia](https://navia.co.in/blog/slippage-in-trading/)

### Inferences
- The best-documented Indian intraday families (time-based straddles, ORB) are positive-expectancy in backtests but regime-dependent: straddles bleed in trending/gap regimes (2020, mid-2024–2025), ORB/option-buying bleeds in choppy regimes (2024–25). Neither is robust across all regimes without a regime filter.
- Every family that was tested with full Indian costs *and* an honest OOS split (pairs, stat-arb, replicated ORB) saw the edge shrink to ~zero or negative. Headline ORB/straddle backtests lacking slippage or OOS should be discounted 15–30% (per QuintalMind) or more.
- Short-straddle drawdowns as a share of annual profit are large (2022 StockMock: DD ≈ 78% of yearly P&L), meaning a few bad months can erase a year even when win rate is ~65–70%.
- Scalping/market-making is structurally dominated by colocated prop firms (Jane Street scale, 1–2% of traders = 60–70% of turnover); retail with ₹20/order brokerage and ₹2 spreads on a ₹150 premium cannot compete on microstructure edge.

### Gaps
- No published Indian backtest of a 9:20 Nifty straddle with year-by-year 2020–2025 drawdowns was found (AlgoTest/Quantman data require running it yourself).
- No India-specific quantification of option-seller P&L on 4 Jun 2024, 5 Aug 2024 or 7 Apr 2025.
- No credible NSE backtests for VWAP mean reversion/trend, intraday gap-momentum on large caps, or iron condors/credit spreads intraday (iron-butterfly margin reduction "40–60%" is the only condor-adjacent figure, from QuintalMind).
- Agarwal et al. full-text statistics (seller P&L, COVID loss) not verified due to PDF extraction failure.

---

## KQ2. Index options with ₹1 lakh after SEBI 2024–25 changes: what can actually be traded

### Takeaway
After the Nov 2024 framework (₹15–20 lakh minimum contract value, one weekly expiry per exchange, 2% extra ELM on expiry-day shorts, no calendar-spread benefit on expiry day), a naked Nifty/BankNifty option sale needs roughly ₹1–2.5 lakh margin per lot, so ₹1 lakh cannot realistically run naked or even most defined-risk selling at 1 lot with any buffer; option *buying* (₹5–15k per lot) is the only index-options path, and Sensex weekly (lot 20) is the only alternative weekly to Nifty.

### Cited Findings
- SEBI framework (Zerodha summary): minimum contract value ₹15–20 lakh for new contracts from 21 Nov 2024; lot revisions Nifty 25→75, BankNifty 15→30, FinNifty 25→65, Midcap Select 50→120, Sensex 10→20, Bankex 15→30; weekly expiry only on one benchmark per exchange from 20 Nov 2024 (NSE kept Nifty; BSE kept Sensex; BankNifty/FinNifty/Midcap/Bankex/Sensex 50 weeklies discontinued); 2% extra ELM on short options on expiry day (example: Nifty 26,200 × 75 × 2% = ₹39,300/lot); upfront premium collection from buyers; no calendar-spread margin benefit on expiry day from 10 Feb 2025; intraday position-limit monitoring from 1 Apr 2025 — [Zerodha Z-Connect](https://zerodha.com/z-connect/business-updates/sebis-new-rules-for-index-derivatives-heres-whats-changing)
- Subsequent lot revisions: BankNifty 30→35 from 25 Apr 2025; Nifty 75→65 and BankNifty 35→30 effective 30 Dec 2025 — [Zerodha on X](https://x.com/zerodhaonline/status/1974363648974881113); [Business Standard](https://www.business-standard.com/amp/markets/capital-market-news/nse-revises-market-lot-sizes-for-nifty-bank-nifty-mid-select-f-o-contracts-125033100440_1.html); [QuantsApp lot table](https://www.quantsapp.com/lot-size)
- Nifty weekly expiry moved to Tuesday from Sep 2025; STT on option sale raised 0.1%→0.15% of premium and futures 0.02%→0.05% from 1 Apr 2026 — [imrawal.com](https://imrawal.com/Website/articles/sebi-fo-study-why-retail-traders-lose.html); Zerodha charges page confirms options STT 0.15% sell-side, ₹20/order, NSE txn 0.03553% on premium — [Zerodha charges](https://zerodha.com/charges/)
- Naked Nifty option sale margin estimates: ₹1.25–1.5 lakh/lot overnight (SPAN+exposure) — [VRD Nation](https://www.vrdnation.com/margin-requirements-for-options-selling/); ₹1.5–2 lakh/lot at lot 65, Nifty 24–25k — [NiftyWise](https://niftywise.org/blog/how-much-capital-do-you-need-for-nifty-options-trading); ₹1.5–2.5 lakh per straddle lot, ₹5–10 lakh suggested minimum — [QuintalMind](https://www.quintalmind.com/blog/time-based-straddle-strategy-nifty-options); Zerodha ORB study used ₹1.5L/lot (buying margin assumption) and ₹3.5L/lot for selling — [In The Money](https://inthemoneybyzerodha.substack.com/p/how-to-trade-opening-range-breakout)
- Sensex: weekly retained (Thursday expiry), lot 20 per QuantsApp 2026 table; Bankex and Sensex 50 weeklies ended 14/18 Nov 2024 — [5paisa](https://www.5paisa.com/news/nse-bse-revise-index-derivatives-framework-lot-sizes-weekly-options); [QuantsApp](https://www.quantsapp.com/lot-size). (One Univest article claims Sensex lot 10 from Jan 2026 — conflicts with other sources; unverified.)
- Agarwal et al.: lot-size increases were offset by retail shifting to small-ticket, riskier (far OTM/short-dated) options — [IDEAS/RePEc](https://ideas.repec.org/p/zbw/cfrwps/327125.html)

### Inferences
- Arithmetic (own calc): Nifty at 25,000 × lot 65 = ₹16.25 lakh notional; a 1% index move = ₹16,250 per lot; the 4 Jun 2024 move (5.9%) ≈ ₹96,000 per lot — i.e., one naked lot on a crash day can wipe an entire ₹1 lakh account even if margin were somehow available.
- ₹1 lakh cannot run naked short straddles/strangles (₹1.5–2.5 lakh/lot) and leaves no buffer for the 2% expiry-day ELM (~₹32,500 at Nifty 25k × 65). Defined-risk spreads/iron flies cut margin 40–60% but still land around ₹60k–1.2 lakh for 1 lot, with ₹0 cushion. Hedged selling at ₹1 lakh means 1 lot, all-in, no scaling and no survival margin.
- Option buying at ₹1 lakh: 1 lot Nifty ATM ≈ ₹150 × 65 = ₹9,750 (9.75% of capital); a 20% premium SL = ₹1,950 ≈ 2% of capital per trade — feasible but concentrated. Sensex (lot 20, index ~80k, ATM premium a few hundred rupees) gives finer sizing (≈₹4–8k per lot), which is why it is the realistic weekly alternative for a small account.
- Stock futures/options are out (lot values ≥₹15 lakh → ₹1–3 lakh margin). Equity intraday with MIS leverage (typically 5x via broker) is the other viable sleeve for ₹1 lakh.

### Gaps
- No exact, dated broker margin figure for a 1-lot Nifty short straddle in 2025–26 (numbers vary ₹1–2.5 lakh by source; margin depends on VIX/day). Use the broker SPAN calculator.
- Current Sensex lot size conflicts between sources (20 vs 10); not resolved.
- No source on Sensex weekly liquidity/spreads vs Nifty for small-lot execution.

---

## KQ3. Expected-value math for a ₹1 lakh account (1%/day target, realistic systems, costs, Kelly, risk of ruin)

### Takeaway
A 1%/day target on ₹1 lakh requires ~0.3–0.5R expectancy per trade at 1% risk and 2–3 trades/day — roughly 3–5x what documented retail systems show; a "good" retail system (55% win, 1.2R, 1% risk, 2.5 trades/day, 0.1R costs) yields ~0.28%/day ≈ 5.8%/month gross-of-tax with median annual max drawdown ~15% (95th pct ~26%). Doubling risk to 2%/trade roughly doubles return but raises P(≥30% drawdown) from ~1% to ~43%.

### Cited Findings
- Cost inputs (Zerodha): options ₹20/order, STT 0.15% sell-side premium, NSE 0.03553% on premium, GST 18% on brokerage+txn; equity intraday brokerage min(0.03%, ₹20)/order, STT 0.025% sell, NSE 0.00307%, stamp 0.003% buy — [Zerodha charges](https://zerodha.com/charges/)
- SEBI FY23: loss-making intraday equity traders paid trading costs equal to an *additional* 57% of their losses; profit-makers paid 19% of profits — [Business Standard](https://www.business-standard.com/amp/markets/news/7-in-10-intraday-traders-in-equity-cash-suffered-losses-in-fy23-sebi-study-124072400975_1.html)
- Observed Nifty ATM spread ₹2 on ₹150 premium (≈1.3%/side) and ₹30 slippage on a market order (Mar 2026) — [Navia](https://navia.co.in/blog/slippage-in-trading/); measured near-ATM half-spreads from one developer's live data: Nifty ~0.125 pt, Sensex ~0.40, BankNifty ~0.725 (fixed assumptions had been 3–7x too high) — [GitHub NfBnf PR#164](https://github.com/sarkarrichard-dev/NfBnf/pull/164)
- Zerodha ORB backtest used 0.2% slippage plus brokerage/taxes — [In The Money](https://inthemoneybyzerodha.substack.com/p/how-to-trade-opening-range-breakout); QuintalMind: live results typically 15–30% worse than backtest; risk ≤1–2% of capital per trade; profit factor >1.3 viable, 1.5–2.0 best — [QuintalMind](https://www.quintalmind.com/blog/time-based-straddle-strategy-nifty-options)
- Zarattini ORB: 24% hit rate, +0.13R/trade (an example of a low-win-rate, positive-expectancy intraday system) — [MQL5 review](https://www.mql5.com/en/blogs/post/776235)
- 60-day challenge winner self-report: "right between 60 to 70% of the times" because he never lets a winner turn into a loss — [Zerodha](https://zerodha.com/z-connect/zerodha-60-day-challenge/winners/intraday-stock-trader-par-excellence)

### Inferences (own calculations, run 2026-10-25; Monte Carlo 5,000 paths, 12 months, 21 days/month)

Cost drag (Zerodha schedule, excl. slippage):
| Trade | Statutory+brokerage round trip | % of traded value |
|---|---|---|
| 1 lot Nifty (65) option @ ₹150 premium | ~₹70 | 0.72% of premium |
| 1 lot Nifty option @ ₹50 premium | ~₹55 | 1.69% of premium |
| Equity intraday ₹1 lakh/side | ~₹83 | 0.083% |
| Equity intraday ₹5 lakh/side (5x MIS) | ~₹225 | 0.045% |
Adding ~1.3%/side spread on ATM options makes options round-trip cost ≈3.3% of premium; with a 20% premium SL (1R = 20% of premium) that is ≈0.15–0.2R per trade — hence the 0.1R cost assumption below is *optimistic* for options and about right for liquid equity.

Expectancy table (E in R after cost, risk per trade = 1% of equity unless noted):
| Win % | R | Trades/day | Cost | E/trade | Day | Month | Monthly σ | Ann. Sharpe |
|---|---|---|---|---|---|---|---|---|
| 55 | 1.2 | 2.5 | 0 | 0.21R | 0.53% | 11.0% | 7.9% | 4.8 |
| 55 | 1.2 | 2.5 | 0.1R | 0.11R | 0.28% | 5.8% | 7.9% | 2.5 |
| 55 | 1.2 | 2.5 (0.5% risk) | 0.1R | 0.11R | 0.14% | 2.9% | 4.0% | 2.5 |
| 45 | 1.5 | 2 | 0.1R | 0.025R | 0.05% | 1.0% | 8.1% | 0.5 |
| 40 | 2.0 | 2 | 0.1R | 0.10R | 0.20% | 4.2% | 9.5% | 1.5 |
| 65 | 0.8 | 3 | 0.1R | 0.07R | 0.21% | 4.4% | 6.8% | 2.2 |
| 70 | 0.5 (straddle-like) | 1 | 0.05R | 0.00R | 0% | 0% | 3.2% | 0 |
| 52 | 1.0 | 3 | 0.1R | −0.06R | −0.18% | −3.8% | — | neg |

- 1%/day requirement: at 1% risk you need 0.50R/trade with 2 trades/day, 0.33R with 3, 0.20R with 5; at 2% risk, 0.25R/0.17R/0.10R. Documented systems sit at 0.03–0.13R net → 1%/day is not achievable at 1–2% risk without ~5+ trades/day at top-decile edge; the "0.5%/day straddle" marketing figure implies a 70%/0.5R profile that is ~breakeven after a realistic 0.05R cost (row 7).
- Kelly fractions: 55%/1.2R → full 17.5%, half 8.8%, quarter 4.4%; 45%/1.5R → 8.3%/4.2%/2.1%; 70%/0.5R → 10%/5%/2.5%. Retail should sit at ≤quarter-Kelly, i.e., 1–2% risk per trade, consistent with the QuintalMind 1–2% guidance.
- Monte Carlo (12 months):
  | Config | Trades/yr | Median max DD | 95th pct max DD | P(DD ≥30%) | Median 1-yr return | 5th pct return |
  |---|---|---|---|---|---|---|
  | 55%/1.2R, 1% risk, 2.5/day, 0.1R cost | 630 | 15.2% | 25.6% | 1.3% | +90% | +23% |
  | same, 2% risk | 630 | 28.5% | 45.4% | 42.5% | +251% | +39% |
  | 45%/1.5R, 1% risk, 2/day | 504 | 24.2% | 42.6% | 28.3% | +10% | −30% |
  | 52%/1.0R, 1% risk, 3/day | 756 | 46.2% | 64.0% | 89.1% | −39% | −61% |
  | 70%/0.5R, 3% risk, 1/day (straddle-like) | 252 | 32.1% | 53.8% | 56.9% | −7% | −46% |
  These assume i.i.d. trades and stationary edge; real intraday returns cluster (regime streaks), so true drawdowns are larger. The +90% median for the "good" system is the ceiling with a real 0.11R edge; realistic edges after decay are closer to the 45%/1.5R row (≈+10%/yr, 28% chance of a 30% DD).
- Risk of ruin at ₹1 lakh is dominated by (a) fat-tail single-day events for option sellers (one lot ≈ ₹16k per 1% move) and (b) fixed-cost drag: ₹20/order brokerage is 0.02% of a ₹1 lakh account per order; at 3 trades/day × 2 orders × 21 days = ₹2,520/month = 2.5% of capital/month before statutory charges, so a ₹1 lakh account must beat ~3–4%/month in costs on equity intraday just to break even.

### Gaps
- No published distribution of *live* retail system expectancies (win rate/R) for NSE; the table is constructed from stated backtest profiles, not measured live data.
- Slippage for Sensex weeklies and for stock MIS (impact of market orders on mid-caps) not quantified in any source found.

---

## KQ4. How practitioners use ML to augment rule strategies (regime filters, meta-labeling, ranking, vol forecasting) — Indian examples

### Takeaway
ML is used almost exclusively as a *filter/sizer on top of rule signals* (meta-labeling, regime gating, vol forecasting), not as a price predictor; the only quantified meta-labeling result found (US ETF breakouts) lifted Sharpe 0.61→0.76 walk-forward with a random-skip control at 0.64, while Indian repos/EPAT projects implementing the same stack (India VIX + breadth regime, triple-barrier meta-labels, purged WF-CV) publish **no performance numbers**.

### Cited Findings
- López de Prado meta-labeling reference implementation (Hudson & Thames, JFDS papers) — [GitHub](https://github.com/hudson-and-thames/meta-labeling); mlfinlab triple-barrier labeling — [GitHub](https://github.com/hudson-and-thames/mlfinlab/blob/master/mlfinlab/labeling/labeling.py)
- Quantified meta-labeling on breakouts (32 US ETFs, LightGBM skipping worse half of trades, $5k capital, costs incl., yearly refit, purged walk-forward + locked holdout from Jul 2024): Sharpe 0.61→0.76 walk-forward (random-skip control 0.64±0.10); holdout 0.67→1.43 (control 0.83±0.28); kept-vs-skipped t=3.6 WF / 2.1 holdout; **no edge on crypto (AUC<0.5)**; jump-model regime filter gave lower DD but lower Sharpe than a 200-DMA filter; HAR vol forecast QLIKE 0.37 vs 0.60 trailing, Sharpe gain only 0.86→0.89; LightGBM vol worse than HAR; ML ranking gain attributed to survivor bias — [GitHub kitchenSinkTrading PR#16](https://github.com/shuazs/kitchenSinkTrading/pull/16)
- Indian repo (Tradng-Ai): rule strategies incl. 15-min ORB on NSE; regime classifier on India VIX, Nifty 50/200 DMA, % of Nifty 500 above 50-DMA, A/D ratio, institutional flow proxies; meta-labeling with triple-barrier labels, take/skip + size multiplier, chronological purged WF-CV with calibration, OOS ΔExpectancy with 95% bootstrap CI, 20% DD kill switch — **no results reported** — [GitHub](https://github.com/ankitraj477/Tradng-Ai)
- Indian repo (nse-trading-assistant): meta-labeling on NSE swing signals, documents rejected ideas incl. a market-flow gate — [GitHub](https://github.com/webtools-dotcom/nse-trading-assistant); nse-engine: Nifty regime gate (index > 50-DMA and up over 20 days) for momentum — [GitHub](https://github.com/RishiRaj210984/nse-engine)
- QuantInsti EPAT: Random Forest regime detection on Nifty 500 breadth (bull/bear/high-vol/low-vol) to scale exposure — no accuracy, returns or DD published — [QuantInsti](https://blog.quantinsti.com/epat-project-machine-learning-market-regime-detection-random-forest-python/); Bank Nifty deep learning on 1-min data to predict next-day open direction: AUC 83% (stock model), >60% (index) — [QuantInsti](https://blog.quantinsti.com/predict-bank-nifty-open-price-deep-learning-epat-project-balamurugan/); Trading index options on index momentum (EPAT) — [QuantInsti](https://blog.quantinsti.com/trading-index-options-index-momentum/)
- Vol forecasting for sizing: intraday pairs repo uses GARCH(1,1)-adjusted entry thresholds — [GitHub avadhi3103](https://github.com/avadhi3103/Intraday-Pairs-Trading); practitioner rule: India VIX 13–18 "sweet spot" for selling, avoid >20 — [QuintalMind](https://www.quintalmind.com/blog/time-based-straddle-strategy-nifty-options)
- Regime evidence from backtests: ORB option-buying lost in May 2024–May 2025 while selling stayed positive; selling calls smoother than puts — [In The Money](https://inthemoneybyzerodha.substack.com/p/how-to-trade-opening-range-breakout)

### Inferences
- Plausible value-add per family: ORB → regime/trend-day classifier (VIX level/change, overnight gap, first-15-min range vs ATR) to skip chop days; straddles → VIX/realised-vol regime + event-calendar gate (election/budget/Fed/tariff days) and vol-forecast-based sizing — this directly targets the documented failure mode (trend days wiping months); stock momentum → cross-sectional ML ranking, though US evidence suggests ranking gains are often vol/survivorship artefacts; pairs → little room, costs dominate.
- Realistic uplift from meta-labeling, per the only controlled test found, is ~+0.15 Sharpe in-sample-ish and noisy on holdout; an Indian retail system should not plan on ML turning a zero-edge rule into a positive one — it trims losers from an already-positive signal.
- Indian ML projects cluster at the "architecture built, results absent" stage; treat any Indian ML-intraday claim without OOS numbers, controls and costs as unproven.

### Gaps
- No Indian example (blog, EPAT, Kaggle, GitHub) with before/after numbers for a regime filter or meta-label on an NSE intraday strategy.
- No published vol-forecasting-for-sizing result on Nifty straddles (GARCH/HAR vs trailing) with P&L impact.

---

## KQ5. Development/validation workflow: backtest → walk-forward → paper → tiny live → scale (NSE specifics)

### Takeaway
The validation stack practitioners and the literature converge on is: survivorship-free data, full Indian cost model (STT 0.15% options sell / 0.025% equity, ₹20/order, exchange charges, GST, stamp) plus measured slippage (≈0.1–0.7 pt half-spread for Nifty/Sensex/BankNifty ATM, ~0.2% assumed by Zerodha), purged/embargoed walk-forward or CPCV with a locked holdout scored once, random-skip controls for ML filters, Deflated Sharpe / MinBTL to penalise the number of variants tried, then a paper and 1-lot live phase expecting 15–30% degradation.

### Cited Findings
- Deflated Sharpe Ratio (Bailey & López de Prado, JPM 2014): corrects observed SR for multiple-testing selection bias and non-normality; keywords include Minimum Track Record Length and Minimum Backtest Length — [SSRN 2460551](https://papers.ssrn.com/abstract=2460551); Probability of Backtest Overfitting / MinBTL (Bailey, Borwein, López de Prado, Zhu): minimum backtest length required rises with the number of configurations tried — [SSRN 2326253](https://papers.ssrn.com/abstract=2326253); [CXO summary](https://www.cxoadvisory.com/big-ideas/insidiousness-of-overfitting-investment-strategies-via-iterative-backtests)
- CPCV: with N groups and k test groups, C(N,k) paths (N=6,k=2 → 15 paths), enabling overfitting statistics vs single walk-forward path — [walk-forward-validation skill page](https://skillselion.com/skills/agiprolabs/claude-trading-skills/walk-forward-validation); Python implementation of purged/embargoed splits, CPCV, PSR/DSR and MinBTL — [purgedcv](https://anaconda.org/conda-forge/purgedcv); [eslazarev/purged-cross-validation](https://github.com/eslazarev/purged-cross-validation)
- Worked examples of the stack: purged walk-forward, locked holdout from Jul 2024 scored once, random-skip control, yearly refits, lookahead unit tests — [kitchenSinkTrading PR#16](https://github.com/shuazs/kitchenSinkTrading/pull/16); Indian repo with chronological purged WF-CV, calibration, bootstrap CI on ΔExpectancy, 20% DD kill switch — [Tradng-Ai](https://github.com/ankitraj477/Tradng-Ai); walk-forward z-score with no lookahead and full Indian cost model (STT, stamp, GST, slippage) — [Intraday-Pairs-Trading](https://github.com/avadhi3103/Intraday-Pairs-Trading); rolling OOS 2019–2026 with robustness checks and half-life time stop — [ou-pairs-trading-nse](https://github.com/AtharvaMistry/ou-pairs-trading-nse)
- In-sample vs OOS decay example: net Sharpe 1.01 IS → 0.34 OOS — [OpenAlgo](https://openalgo.in/stats-arb/the-brutal-reality-check)
- Survivorship: backtesting only current index constituents inflates results (Nifty Smallcap 250 evidence) — [arXiv](https://arxiv.org/pdf/2603.19380); Indian options backtest guide lists survivorship among things a result must survive — [fnotrader](https://www.fnotrader.com/blog/options-backtesting-india)
- Slippage/spread inputs: Nifty ~₹12/lot, BankNifty ~₹16/lot ATM (2021) — [Medium niuhi](https://medium.com/@niuhi/algo-trading-execution-analysis-2d970d6c4aad); measured half-spreads Nifty 0.125 / Sensex 0.40 / BankNifty 0.725 pts — [NfBnf PR#164](https://github.com/sarkarrichard-dev/NfBnf/pull/164); Zerodha used 0.2% slippage + costs — [In The Money](https://inthemoneybyzerodha.substack.com/p/how-to-trade-opening-range-breakout); live 15–30% worse than backtest — [QuintalMind](https://www.quintalmind.com/blog/time-based-straddle-strategy-nifty-options)
- Backtesting-tool constraints: Streak limited to ~1 month of expired contracts (2021) — [TradingQnA](https://tradingqna.com/t/options-streak-algorithmic-for-intraday-uncovered-short-straddle-trading/112663); AlgoTest offers templated straddle backtests with weekly free credits; expiry-day shift (Thu→Tue, Sep 2025) must be handled — [AlgoTest docs](https://docs.algotest.in/Time-Based-Algo-Trading/how-to-backtest/backtest-920-Straddle/)
- Rob Carver (Leveraged Trading): start with a "Starter System" — single instrument, single rule — then add instruments/rules; size by volatility (standard deviation + correlation), not by stop-distance × fixed % — [Pan Macmillan](https://www.panmacmillan.com/authors/robert-carver/leveraged-trading/9780857197221); [Top Traders Unplugged](https://www.toptradersunplugged.com/captivate-podcast/ttu90-why-diversification-is-key-ft-robert-carver-author-trader-2of2/)
- Verification tool for live stage: Zerodha Console Verified P&L (publish P&L for a chosen window) — [TradingQnA thread](https://tradingqna.com/t/fake-pnl-of-live-trading-finfluencers-scam/152081)

### Inferences (recommended workflow, synthesised)
1. **Data**: ≥4–5 years of 1-min NSE data spanning 2020 (COVID), 2022 (rate shock), Jun/Aug 2024, Apr 2025; point-in-time index membership for stocks; expired option chains incl. expiry-day changes.
2. **Costs**: exact statutory schedule + ₹20/order + measured half-spread per instrument (Nifty 0.125, Sensex 0.4, BankNifty 0.725 pt) + adverse-selection slippage on market orders (Navia example ₹30/lot); for equity add 1 tick × 2 and a ₹15.34 DP charge only if delivery.
3. **Backtest hygiene**: no same-bar fills; fill at next-bar open or at limit; log every variant tried (for DSR/MinBTL); hold out the last 12 months and score once.
4. **Walk-forward / CPCV**: anchored or rolling 12-m train / 3-m test; CPCV with embargo ≥ holding period; require positive expectancy in ≥70% of OOS windows, and DSR > 0.95 given the number of trials.
5. **Controls**: for any ML filter, a random-skip control with same skip fraction (as in PR#16); for regime filters, compare vs a dumb VIX threshold.
6. **Paper trade**: ≥60 trading days (the 60-day challenge horizon), live data, same code path, compare fill prices vs backtest assumptions.
7. **Tiny live**: 1 lot / smallest MIS size for 3 months; track slippage vs model; kill switch at 20% DD (Tradng-Ai) or at 2× backtest max DD.
8. **Scale**: only after live expectancy ≥ 0.7× backtest over ≥100 trades; scale risk per trade from 0.5% → 1% → max 2%; add instruments (Sensex, stocks) before adding size per Carver's diversification-first logic.

### Gaps
- No Indian source states a specific minimum paper-trading period or trade count before going live; the 60-day figure is borrowed from the challenge format.
- Exact MinBTL/DSR formulas not extracted (papers behind SSRN pages); only their purpose is cited.

---

## KQ6. Case studies: Indian retail algo traders with public long-run P&L (good and bad); what distinguishes the consistent few

### Takeaway
No independently verified multi-year retail algo P&L was found; the closest hard data are Zerodha's 60-day challenge (7–10% of participants won a challenge, <1% won five) and SEBI's FY22–FY25 studies (7–9% profitable), while the public "verified P&L" ecosystem is polluted by documented fake-P&L apps and SEBI enforcement (Asmita Patel: ₹53.67 crore impounded, claimed 300% returns vs ₹12.3 lakh actual trading profit 2019–Jan 2024).

### Cited Findings
- Nithin Kamath (TradingQnA, 1 Jun 2017): "Usually 7 to 10% of the 60 day challenges are won"; "the same person winning say 5 challenges drops significantly, reduces to lesser than 1%" — [TradingQnA](https://tradingqna.com/t/consistent-profitable-traders-in-zerodha-intraday-what-proportion-of-zerodhas-60-day-challenge-are-successful/14607); earlier (2014) Kamath: ~8–10% win, "most of them are typically managing to stay breakeven" — [Zerodha](https://zerodha.com/z-connect/general/start-the-zerodha-60-day-challenge)
- Challenge discontinued from 1 Jan 2023 (regulatory stance on gamification); required net profit over 60 days — [Zerodha Support](https://support.zerodha.com/category/console/reports/60-day-challenge/articles/what-is-the-60-day-challenge)
- Winner profile (Zerodha-published): intraday stock trader, 60–70% win rate, never lets a winner become a loser — [Zerodha](https://zerodha.com/z-connect/zerodha-60-day-challenge/winners/intraday-stock-trader-par-excellence); self-reported 13 consecutive challenge wins (X thread, unverified) — [X/FunTechAcademy](https://x.com/FunTechAcademy/status/2058437926565073226)
- Fake P&L ecosystem: apps that let users enter strikes and daily P&L and generate Zerodha-lookalike URLs (Moneycontrol, Aug 2023); a Zerodha partner edited P&L in a "150% ROI" video and had referral link blocked; Nithin: Verified P&L exists so audiences can demand a verified link; Zerodha does not track affiliates' P&L — [TradingQnA](https://tradingqna.com/t/fake-pnl-of-live-trading-finfluencers-scam/152081)
- SEBI vs Asmita Patel (Feb 2025 interim order): 6 entities barred, ₹53.67 crore impounded; courses claimed up to 300% returns while actual trading net profit was ₹12,28,365 (FY20–Jan 2024) vs claimed ₹140 crore portfolio — [Moneylife](https://moneylife.in/article/sebi-cracks-whip-on-finfluencer-asmita-patel-impounds-rs5367-crore-unlawful-gain-earned-from-illegal-investment-advisory-business/76321.html); [Angel One](https://www.angelone.in/news/market-updates/sebi-action-on-finfluencer-barred-asmita-patel-and-5-others-from-stock-market); SEBI order vs Avadhut Sathe, ₹546 crore unlawful gains (Dec 2025) — [MediaNama](https://www.medianama.com/2025/12/223-sebi-bans-avadhut-sathe-546-crore-unlawful-gains/)
- Survivorship in social media: visible winners are the noisy minority; quitters rarely post — [DayTrading.com](https://www.daytrading.com/trust-rating/marketing-vs-statistics)
- Academic: retail option selling in India was cumulatively profitable (~₹3 bn) in normal times but lost ~₹11 bn in COVID, erasing gains; even less-constrained sellers were not net beneficiaries of the variance risk premium (search snippet of the paper) — [Agarwal et al. PDF](https://www.ualberta.ca/en/finance-department/media-library/documents/vikas-agarwal.pdf)
- Kamath: biggest reason active traders lose is overtrading; those with another income source do better — [Business Today](https://www.businesstoday.in/amp/markets/stocks/story/zerodhas-nithin-kamath-says-biggest-reason-active-traders-lose-money-is-overtrading-368316-2023-01-31); [Moneylife](https://mas360.moneylife.in/article/nikhil-kamath-no-easy-money-less-than-1-percentage-active-traders-beat-bank-fds/3922.html)
- SEBI FY23 intraday: >500 trades/yr → 80% losers (vs 71% overall) — [Moneylife](https://moneylife.in/article/7-out-of-10-individual-intraday-traders-in-equity-cash-segment-make-losses-sebi-study/74733.html)

### Inferences
- Consistency base rate: ~7–10% profitable in any 60-day window, <1% across five windows, ~7% profitable over 3 years (SEBI) — all converge on roughly 1 in 100 retail traders being durably profitable.
- Traits shared by the documented consistent few: lower trade frequency (SEBI frequency data), strict no-giveback management (60-day winner), external income (Kamath), and surviving tail days — i.e., the differentiator is risk control and selectivity, not signal cleverness.
- Public "0.5%/day" straddle track records should be presumed survivorship/marketing-biased unless accompanied by a broker Verified P&L link covering 2020 and mid-2024–2025.

### Gaps
- No Indian retail algo trader with a public, broker-verified, multi-year (incl. 2020 and 2024–25) P&L was found in this research — neither consistently profitable nor blown-up accounts with full statements.
- Zerodha never published official challenge statistics; figures are Kamath's forum estimates (2014, 2017).
- r/IndianStreetBets and X long-run P&L threads were not directly surveyed (search did not surface verifiable ones).
