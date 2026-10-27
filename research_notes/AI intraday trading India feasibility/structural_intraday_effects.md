# Where intraday profits come from (Part A) and structural intraday effects in NSE cash equities (Part B)

Research date: 2026-10-25. Scope: Indian cash equities (Nifty 50), 2018–2026 regime. IMPORTANT regime note up front: the close-of-day microstructure changed on 3 Aug 2026 (Closing Auction Session, "CAS") and changes again on 7 Dec 2026. Any "last 30 minutes" rule below must be tested separately in three regimes: (i) pre-Aug-2026 VWAP close, (ii) Aug–Dec 2026 CAS 15:15–15:35 with continuous trading ending 15:15, (iii) from 7 Dec 2026 CAS 15:30–15:40.

---

## Regime timeline the report writer needs (all Part B rules depend on it)

### Takeaway
Nifty 50 stocks are all F&O stocks, so all of them are "CAS-eligible"; since 3 Aug 2026 their continuous trading stops at 15:15 and the close is an auction price, not a VWAP. Broker MIS square-off times moved earlier accordingly (Zerodha 15:12, Upstox 15:05 for CAS stocks).

### Cited Findings
- SEBI circular (NSE file CMPT72373, Zerodha bulletin 23 Jan 2026): CAS introduced 3 Aug 2026 for stocks with F&O contracts; phases 15:15 reference-price/transition (5 min), 15:20 order entry limit+market (5 min), 15:25 limit-only with random close in last 2 min (closes randomly 15:28–15:30), 15:30 matching (5 min); derivatives trade to 15:40; post-close 15:50–16:00 at closing price. Pre-open modified from 7 Sep 2026: 09:00 order entry (5 min), 09:05 limit-only with random close 09:08–09:10, 09:10 matching (2 min), 09:12–09:15 transition — [Zerodha Marketintel bulletin](https://zerodha.com/marketintel/bulletin/439989/introduction-of-closing-auction-session-cas-in-the-equity-cash-segment-and-certain-modifications-in-the-pre-open-auction-session)
- CAS price band is a static ±3% around a fresh afternoon reference price with normal band-widening suspended; stop-loss/iceberg/IOC blocked; unexecuted daytime limit orders within band carry into the auction with original timestamps; if an index circuit breaker halts the market before the auction, close reverts to the 30-min VWAP; non-F&O stocks keep continuous trading to 15:30 and the old VWAP close — [Outlook Money](https://www.outlookmoney.com/invest/nse-extended-fo-timings-and-new-closing-auction-session-rules-explained)
- Old method (pre-Aug 2026): closing price = VWAP of trades in the last 30 minutes of continuous trading; F&O expiry settlement used the same VWAP — [TheTaxCorp summary of SEBI Sep 2026 consultation](https://thetaxcorp.in/article/sebi-consultation-paper-on-closing-auction-session-settlement-methodology)
- Revision (SEBI, reported 16 Oct 2026): CAS becomes a 10-minute session 15:30–15:40 on all days, order entry closes randomly 15:38–15:40; stock and index derivatives trade to 15:45; on expiry days expiring index derivatives stop at 15:30; expiry settlement for index and stock derivatives = VWAP of the final 30 minutes of continuous trading (i.e., SEBI reverted F&O settlement to VWAP after pushback); effective 7 Dec 2026 (order-transition provisions 8 Feb 2027) — [NewsOnAir](https://newsonair.gov.in/sebi-revises-timings-and-operational-framework-of-closing-auction-session/); [Outlook Money](https://www.outlookmoney.com/invest/sebi-cas-vwap-based-fo-expiry-settlement-revised-rules); SEBI received ~20,000 suggestions on the Sep-12-2026 consultation — [5paisa/Reuters](https://www.5paisa.com/blog/sebi-may-step-back-from-closing-auction-based-derivatives-settlement-after-market-pushback)
- One secondary source says the revised CAS reference price will be the VWAP of the last 15 minutes of continuous trading — reported via search summary of [TheTaxCorp](https://thetaxcorp.in/article/sebi-consultation-paper-on-closing-auction-session-settlement-methodology); NOT verified against the SEBI circular (PDF could not be parsed locally).
- Zerodha current MIS auto square-off: CAS stocks 15:12, non-CAS stocks 15:25, F&O 15:26; ₹50+GST per squared-off order; RMS may change timings on volatile days — [Zerodha Support](https://support.zerodha.com/category/trading-and-markets/trading-faqs/market-sessions/articles/intraday-auto-square-off-timings). History: equity MIS was 15:20 until 26 Dec 2025, then 15:25 — [Z-Connect](https://zerodha.com/z-connect/updates/changes-to-the-auto-square-off-timings-for-equity-and-fo); CAS-stock square-off was 15:10 at launch and moved to 15:12 on 10 Aug 2026 — [Z-Connect product updates](https://zerodha.com/z-connect/?p=454739)
- Upstox current: intraday equity non-CAS 15:20, CAS-eligible equity 15:05, equity derivatives 15:20 — [Upstox Help](https://help.upstox.com/support/solutions/articles/252251-what-is-auto-square-off-and-what-is-the-auto-square-off-timings-for-different-segments). 5paisa (30 Jul 2026 schedule): CAS stocks 15:10, non-CAS 15:20, F&O 15:25 — [5paisa](https://www.5paisa.com/news/market-timings-to-change-from-august-3-as-closing-auction-session-takes-effect). Kotak: 15:20 equities (pre-CAS page) — [Kotak](https://kotaksecurities.com/support/what-are-the-auto-square-off-timings-for-open-intraday-positions). Angel One: 15:15 cash, 15:20 F&O (pre-CAS) — [Angel One](https://www.angelone.in/support/your-orders/square-off). SEBI does not mandate the square-off time; it is a broker RMS convention — [TradingQnA](https://tradingqna.com/t/square-off-time-for-intra-day-orders/19421)
- NSE weekly/monthly index derivatives expiry moved to Tuesday from 1 Sep 2025 (BSE Thursday); monthly contracts expire last Tuesday — [Moneylife](https://moneylife.in/article/nse-equity-fo-contracts-to-expire-on-tuesdays-bse-on-thursdays-from-1st-september/77434.html)
- Block deal windows since 1 Jan 2018: 08:45–09:00 (reference = previous close) and 14:05–14:20 (reference = VWAP of 13:45–14:00), orders within ±1% of reference, min ₹10 crore — [NSE circular CMTR36573](https://nsearchives.nseindia.com/content/circulars/CMTR36573.pdf); still the same in SEBI's Jan 2026 consultation annexure — [SEBI](https://www.sebi.gov.in/sebi_data/commondocs/jan-2026/Consultation%20paper%20Annexure_A_p.pdf)

### Inferences
- For Nifty 50 names, "last 30 minutes" in the Aug–Dec 2026 regime means 14:45–15:15 of continuous trading plus a 15:15–15:35 auction with no 1-min bars; charts show blank space 15:15–15:30 and a single close print — [TradingQnA CAS thread](https://tradingqna.com/t/everything-you-need-to-know-about-the-closing-auction-session-cas-starting-august-3/195801?page=3). From 7 Dec 2026 bars return to 15:30 but the close is still the auction price.
- Broker square-off times will very likely shift again after 7 Dec 2026 (they moved in Aug 2026 to track the 15:15 halt). Any square-off rule must be parameterised by broker-time, not hard-coded.

### Gaps
- Could not read the SEBI Jan 2026 circular PDF (binary); exact CAS reference-price and equilibrium tie-break rules come from secondary sources only.
- Could not confirm the Dec-2026 revised reference-price definition (VWAP of last 15 min) from a primary source.

---

## Part A — Q1: How do consistently profitable participants (HFT/market makers, prop desks, FPIs, profitable retail minority) generate intraday returns?

### Takeaway
The participants that make money do so with algos (96–97% of prop/FPI F&O profits), mostly by capturing spread/arbitrage/short-horizon imbalance at a per-trade edge of roughly 0.1–1 bp of notional, which is only viable because they trade at member-level cost, mostly passively, at very high volume. Retail profitability is a thin minority (29% of intraday cash traders net positive in FY23; ~1% beat an FD over 3 years per Kamath).

### Cited Findings
- SEBI F&O study (Sep 2024, FY22–FY24): 93% of ~1 crore individual F&O traders lost money (avg ~₹2 lakh incl. costs); aggregate individual loss >₹1.8 lakh crore; in FY24 proprietary traders booked gross trading profit ₹33,000 crore and FPIs ₹28,000 crore (before transaction costs) while individuals+others lost >₹61,000 crore; 97% of FPI profits and 96% of prop profits came from algorithmic trading — [Business Standard](https://www.business-standard.com/markets/capital-market-news/sebi-study-exposes-massive-losses-for-individual-f-o-traders-in-india-124092400948_1.html); [Moneylife](https://www.moneylife.in/article/93-percentage-of-individual-traders-lost-rs18-lakh-crore-in-equity-fo-in-past-3-years-sebi/75210.html); [TradingQnA discussion of the study](https://tradingqna.com/t/sebis-latest-analysis-of-profits-losses-in-the-equity-derivatives-segment-fy22-fy24/173596)
- SEBI intraday cash study (24 Jul 2024, FY23 data, clients of top-10 brokers = 86% of individual cash clients): 71% of individual intraday traders made a net loss; 80% among those with >500 trades/yr; 76% among under-30s; loss-makers' trading costs = 57% of their trading losses; profit-makers spent 19% of their trading profits on costs; average loss ₹5,371 per trader; intraday participation up >300% vs FY19 — [SEBI research page](https://www.sebi.gov.in/reports-and-statistics/research/jul-2024/study-analysis-of-intraday-trading-by-individuals-in-equity-cash-segment_84946.html); [Moneylife](https://moneylife.in/article/7-out-of-10-individual-intraday-traders-in-equity-cash-segment-make-losses-sebi-study/74733.html); [NewsOnAir](https://www.newsonair.gov.in/sebi-study-over-70-of-intra-day-equity-traders-face-losses-in-2022-23-fiscal)
- Nithin Kamath (Jan 2022): only ~1% of active traders earn more than a bank FD over a 3-year window — [Moneylife](https://mas360.moneylife.in/article/nikhil-kamath-no-easy-money-less-than-1-percentage-active-traders-beat-bank-fds/3922.html); Value Research argued the figure may be overstated but agreed most active traders do poorly — [Value Research](https://www.valueresearchonline.com/stories/50287/more-active-less-money/). Zerodha 60-day challenge: ~7–10% of challenges won, <1% for repeat winners (forum reply, attribution unclear) — [TradingQnA](https://tradingqna.com/t/consistent-profitable-traders-in-zerodha-intraday-what-proportion-of-zerodhas-60-day-challenge-are-successful/14607)
- Algo share of NSE cash turnover crossed 50% in FY25 (17% in FY11), attributed to prop desks, co-located HFTs and global firms — [Business Standard](https://www.business-standard.com/markets/news/in-a-first-machines-overtake-humans-in-nse-s-cash-market-trades-125041500893_1.html); [Moneycontrol via TradingView](https://it.tradingview.com/news/moneycontrol:b80f3d49f094b:0-co-location-based-hfts-global-trading-firms-lead-to-4x-jump-in-share-of-algo-trading-in-last-decade). NSE co-location launched Jan 2010; ~21.7% of turnover from colo in Q1 2015 — [Wikipedia summary of NSE colo case](https://en.wikipedia.org/wiki/NSE_co-location_scam)
- Market-making economics (Menkveld 2013, Dutch index stocks): one HFT traded ~1,397 times per stock per day, gross profit €0.88 per trade = €1.55 spread profit net of fees minus €0.68 positioning (inventory) loss; i.e., profit comes from spread capture, inventory is a cost — [Tinbergen/VU](https://research.vu.nl/en/publications/high-frequency-trading-and-the-new-market-makers/)
- Baron–Brogaard–Kirilenko (E-mini S&P, CFTC): aggressive (liquidity-taking) HFTs earned ~$45,267/day vs passive ~$2,461/day (Aug 2010 draft); median firm Sharpe 4.3, four-factor alpha 22%; revenue concentrated in a few firms ("winner takes all"); new entrants less profitable and exit more — [CFTC paper](https://www.cftc.gov/idc/groups/public/@economicanalysis/documents/file/oce_riskandreturn0414.pdf); [ai-cio summary](https://www.ai-cio.com/news/high-frequency-trading-winner-takes-all/)
- Jane Street (SEBI interim order 3 Jul 2025): net gains ₹36,671 crore in India Jan 2023–Mar 2025, driven by ₹44,358 crore in index options, partly offset by losses in stock futures, index futures and cash equities; on 17 Jan 2024 it bought ₹4,370 crore of Bank Nifty constituents (cash+futures) in the morning and sold ₹5,372 crore in the afternoon, profit ₹735 crore that day via options — [Moneylife](https://moneylife.in/article/explainer-what-are-sebis-findings-on-jane-street-groups-market-manipulation/77594.html); [Legal500](https://www.legal500.com/developments/thought-leadership/sebi-update-interim-order-against-jane-street-group-for-alleged-index-manipulation/). Allegations, not adjudicated.
- Industry commentary (opinion piece): HFT firms ">90% of Indian market volumes"; cash-futures arbitrage spreads fell from 82 bps (Oct 2024) to 64 bps (Jan 2025) after STT hike — [Basis Point Insight](https://www.basispointinsight.com/Story/with-stt-now-taking-a-shark-bite--rethink-needed-to-restore-liquidity--confidence_a03d8f9f9b77.html) (unverified opinion figures)
- Kamath (May 2024): STT on intraday equity and futures is higher than on options and, with leverage curbs, "has hurt the volumes"; intraday equity hasn't recovered despite the bull run — [Business Today](https://www.businesstoday.in/amp/markets/stocks/story/abandoned-baby-of-indian-markets-zerodha-co-founder-nithin-kamath-laments-high-stt-on-intraday-equity-430041-2024-05-18)

### Inferences
- The profitable class is defined by (a) algorithmic, (b) high-frequency, (c) mostly passive or arbitrage execution, (d) cross-segment (cash vs futures vs options) rather than directional cash-only bets. Jane Street's cash equity leg was loss-making; the money was in options. A retail cash-only trader cannot replicate that structure.
- The "small profitable retail minority" in SEBI data is characterised by fewer trades (loss-makers trade more) and costs = 19% of profits, i.e., they trade less frequently with a larger gross edge per trade, the opposite of scalping.

### Gaps
- No Indian source quantifies prop-desk edge per trade in bps or Indian HFT firm P&L (search for Graviton/Quadeye/AlphaGrep returned nothing relevant). Menkveld/BBK are non-Indian proxies.
- No published breakdown of NSE cash-segment profits by participant type (SEBI's participant-level P&L work covers F&O only).

---

## Part A — Q2: Effective cost per trade (institution vs retail), passive vs aggressive execution, and why 5–15 bps gross edges are tradeable for them but not for a ₹1 lakh account

### Takeaway
A ₹1 lakh retail round trip in a Nifty 50 stock costs ≈8 bps in statutory+brokerage charges before slippage (≈10–15 bps all-in with market orders); a member-level desk pays ≈3–4 bps (dominated by the 2.5 bp sell-side STT) and, when passive, earns the spread instead of paying it. A 10 bp gross edge is therefore roughly break-even for retail and ≈6–7 bps net for a desk, which then needs only volume and a positive hit rate to compound.

### Cited Findings
- Statutory charges, intraday equity: STT 0.025% on sell side only; NSE exchange transaction charge ~0.00297% per side (BSE 0.00375%); SEBI turnover fee 0.0001% (₹10/crore; some broker pages still show 0.0002%); stamp duty 0.003% on buy side; 18% GST on brokerage + exchange + SEBI charges — [Bigul pricing](https://www.bigul.co/pricing); [Interactive Brokers India fee table](https://www.interactivebrokers.com.sg/en/accounts/fees/indiaStockExchangeFees.php); [Kotak](https://www.kotaksecurities.com/ksweb/intraday-trading/cost-of-intraday-trading)
- Discount brokerage: flat ₹20/order (or lower) — [ICICI Direct](https://icicidirect.com/ilearn/stocks/articles/what-is-intraday-brokerage-and-charges); Zerodha's forced square-off adds ₹50+GST per order — [Zerodha](https://support.zerodha.com/category/account-opening/charges-at-zerodha/articles/auto-square-off)
- Nifty 50 names (Reliance, HDFC Bank, TCS, Infosys) typically quote 5–25 paise wide, often one tick; a 5-paise spread on a ₹1,400 stock ≈0.36 bps — [OneTradeJournal](https://onetradejournal.com/glossary/bid-ask-spread) (blog; indicative only). NSE market-wide LOB spread study: 0.77% of median price across all listed stocks (not Nifty 50) — [NSE research paper](https://nsearchives.nseindia.com/content/research/comppaper128.pdf)
- Loss-making retail intraday traders' costs were 57% of their losses; profit-makers' costs were 19% of profits (SEBI FY23) — [Moneylife](https://moneylife.in/article/7-out-of-10-individual-intraday-traders-in-equity-cash-segment-make-losses-sebi-study/74733.html)
- Passive vs aggressive: Menkveld's HFT earned €1.55 spread profit per trade and lost €0.68 on positioning — [VU](https://research.vu.nl/en/publications/high-frequency-trading-and-the-new-market-makers/); BBK: aggressive HFTs ~18x the daily profit of passive ones, but passive provide liquidity at scale — [CFTC](https://www.cftc.gov/idc/groups/public/@economicanalysis/documents/file/oce_riskandreturn0414.pdf)
- Co-location gives order/data latency advantage; SEBI later mandated free tick-by-tick feeds and published latency stats — [IIIT explainer](https://jpmc.iiit.ac.in/static/news_pages/3485.html)

### Inferences (arithmetic from cited rates; my calculation)
- Retail, ₹1,00,000 notional, buy+sell, discount broker: STT ₹25 (2.5 bp) + exchange ₹5.9 (0.6 bp) + stamp ₹3 (0.3 bp) + SEBI ₹0.2 + brokerage ₹40 (4.0 bp) + GST ~₹8.3 (0.8 bp) ≈ ₹82 ≈ 8.2 bps. Add spread-crossing twice (~0.5–1 bp in Nifty 50) and market-order slippage (assume 2–5 bps) → ~11–15 bps all-in. Forced square-off adds ₹59 (5.9 bps) on that order.
- Retail, ₹10 lakh notional: brokerage falls to 0.4 bp → ≈4.8 bps statutory + slippage ≈ 7–10 bps all-in. Fixed ₹20 brokerage is why sub-₹5 lakh accounts are structurally disadvantaged.
- Member/prop desk: no per-order brokerage, exchange charges at volume slabs, STT 2.5 bps on sell still applies (Kamath's complaint), so ≈3.5 bps round trip when aggressive; when passive the desk receives ~0.3–0.5 bp of spread rather than paying it, so net friction ≈3 bps and the effective hurdle for a cash-only strategy is ~3–4 bps vs ~10–15 bps for small retail.
- Cash-futures arbitrage at 64–82 bps annualised-type spreads (opinion figure) illustrates that desks also run carry/arbitrage, not just directional intraday.

### Gaps
- No primary measurement of average effective spread/slippage in bps for Nifty 50 1-min trading in 2018–2026; the 0.36 bp figure is one blog example. Slippage assumption (2–5 bps) is a hypothesis.
- No public NSE member fee schedule by slab was retrieved; "≈3–4 bps" desk cost is an estimate from statutory rates only.

---

## Part B — Effect 1: Broker MIS auto square-off window and bounce after it

### Takeaway
The mechanism is real and now time-compressed (Upstox 15:05, 5paisa 15:10, Zerodha 15:12 for Nifty 50/CAS stocks; continuous trading ends 15:15), but I found no published or community data measuring a systematic sell-off into the square-off and bounce afterward. This is a hypothesis with a plausible mechanism, not an evidenced effect.

### Cited Findings
- Timings: Zerodha CAS stocks 15:12 (changed from 15:10 on 10 Aug 2026), non-CAS 15:25, F&O 15:26 — [Zerodha Support](https://support.zerodha.com/category/trading-and-markets/trading-faqs/market-sessions/articles/intraday-auto-square-off-timings); Upstox CAS 15:05 / non-CAS 15:20 — [Upstox](https://help.upstox.com/support/solutions/articles/252251-what-is-auto-square-off-and-what-is-the-auto-square-off-timings-for-different-segments); 5paisa CAS 15:10 — [5paisa](https://www.5paisa.com/news/market-timings-to-change-from-august-3-as-closing-auction-session-takes-effect); pre-CAS regime: Zerodha 15:20 (to Dec 2025) then 15:25; Angel One 15:15; Kotak 15:20 — sources above.
- Square-offs are executed as market orders (slippage) — [TradingQnA](https://tradingqna.com/t/suppose-i-brought-a-share-of-100rs-at-11-30am-and-forget-to-sell-before-3-20pm-at-that-time-the-price-was-97rs-does-the-intraday-square-off-takes-place-at-this-price-or-above-this-price/1602)
- Anecdotal only: a TradingView post claims prices stay "somewhat volatile for the next 5 minutes" after the 15:20 square-off; a TradingQnA user reports "big movement after this cut off time" — [TradingView post](https://it.tradingview.com/chart/INDOSTAR/0nKCAWKf-Why-is-Closing-Price-important); [TradingQnA](https://tradingqna.com/t/square-off-time-for-intra-day-orders/19421)
- Retail is net-long intraday in cash? Not directly evidenced. SEBI's intraday study does not report long/short skew; the F&O study notes individuals are net losers to prop/FPI — [Business Standard](https://www.business-standard.com/markets/capital-market-news/sebi-study-exposes-massive-losses-for-individual-f-o-traders-in-india-124092400948_1.html)
- Intraday volume/volatility is U-shaped on NSE (high at open and close) — [Sampath & Gopalaswamy, JEMF 2020](https://ideas.repec.org/a/sae/emffin/v19y2020i3p271-295.html)

### Testable rules (hypotheses)
- Pre-Aug-2026 regime (1-min bars): for each Nifty 50 stock, compute r1 = close(15:19)/close(15:09)−1 and r2 = close(15:29)/close(15:20)−1. Test corr(r1, r2) < 0 and mean(r2 | r1 < −x) > 0, conditioning on the stock's day return sign (retail long-skew should make the effect stronger on down days). Compare with placebo windows (e.g., 14:40–14:50 → 14:50–15:00).
- Aug–Dec 2026 regime: forced flow cluster is 15:05–15:12; test r1 = 15:04→15:12, r2 = 15:12→15:15 (last three continuous bars) and r3 = 15:15 last trade → CAS close. Note Zerodha moved 15:10→15:12, implying brokers already found 15:10 too early/thin.
- From 7 Dec 2026: re-estimate once broker timings republish.
- Expected size: unknown. Given statutory+brokerage friction ≈8 bps for ₹1 lakh, the mean reversal would need to exceed ~10–15 bps net of slippage to be tradeable; nothing found suggests reversals of that size on average in Nifty 50 names.

### Gaps
- No dataset, paper, Varsity/TradingQnA thread, or NSE study quantifying price pressure at square-off times was found.
- Retail net-long assumption is untested.

---

## Part B — Effect 2: Closing price mechanism and close-of-day pressure (index rebalances, expiry, month-end)

### Takeaway
Under the old VWAP close, SEBI's own consultation data show last-30-minute volatility 1.5–3.3x normal on rebalance days and FPIs doing 56–60% of affected-stock value on MSCI days; under CAS the auction absorbed ₹39,718 crore (22% of NSE cash turnover) on 31 Aug 2026 with 60/210 stocks hitting the ±3% band. The close-of-day pressure exists, but it is now expressed in a single auction print rather than in tradeable 1-min bars.

### Cited Findings
- SEBI consultation data (as summarised): Nifty 50 last-30-min volatility vs 09:15–14:30 = 1.8x on MSCI rebalance day 31 May 2024, 1.5x on FTSE day 21 Jun 2024; Indian MSCI Standard constituents 3.3x (May 2024) and 2.9x (Aug 2024); MSCI Small Cap 2x and 2.3x; on MSCI India days (29 Feb and 31 May 2024) share of gross traded value in affected stocks: FPIs 56–60%, prop 17%, retail 11%, domestic MFs 8–9%; reference-vs-closing price difference on rebalance days across jurisdictions 0.61%–4.04% vs −0.2% to 0.5% on ±7 surrounding days; Nifty 50 index fund tracking difference +0.76 bp on rebalance days vs −0.12 bp otherwise — [TradingQnA summary of SEBI paper](https://tradingqna.com/t/sebis-consultation-paper-on-introducing-close-auction-session-in-equity-cash-segment/176851)
- Passive funds ≈29% of FPI equity AUM; SEBI's paper gave no empirical Indian volatility comparison (critique) — [IndiaCorpLaw](https://indiacorplaw.in/2025/10/02/sebis-shift-in-closing-price-mechanism-rationale-and-reality/)
- CAS day one (3 Aug 2026): Nifty rose ~201 points between 15:28 and 15:30 (i.e., auction vs last continuous); 4 Aug: ~152 points 15:00–15:15; SEBI found no manipulation; gaps "narrowed considerably" afterwards — [Outlook Business](https://www.outlookbusiness.com/markets/sebi-finds-no-manipulation-in-new-closing-auction-system); experts attributed it to thin liquidity — [Multibagg](https://www.multibagg.ai/market-pulse/articles/nifty-50-closing-auction-spike-cmsdz3qe0cees0zoyzco4ee6f)
- MSCI rebalance 31 Aug 2026 under CAS: ₹39,718 crore auction turnover (~22% of NSE cash turnover that day; 42x the prior session's CAS turnover); 514 mn shares in 19 impacted stocks ≈86% of brokerages' estimated 595 mn rebalance shares; 60 of 210 auction stocks touched the ±3% band; weight-gainers saw stronger participation than weight-losers; 98,000+ unique investors — [Outlook Money](https://www.outlookmoney.com/invest/msci-rebalancing-drives-historic-rs-39718-crore-turnover-as-closing-auction-framework-clears-crucial-test); [5paisa](https://www.5paisa.com/blog/msci-rejig-cas-turnover)
- Expiry-day turnover share (expiring index options, NSE, 26 pre-CAS expiries Feb–Jul 2026): 14:30–15:00 = 8.83% of day; 15:00–15:30 = 5.72%; post-CAS (5 expiries): 14:45–15:15 = 9.80%, 15:15–15:20 transition 1.72%, 15:20–15:30 CAS 4.13% — [TheTaxCorp](https://thetaxcorp.in/article/sebi-consultation-paper-on-closing-auction-session-settlement-methodology) (options premium turnover, not cash)
- Historical VWAP-close manipulation: Varma/Mohanram (2013) show cash-settled stock futures with 30-min VWAP settlement are vulnerable to HFT manipulation targeting price-insensitive execution algos; SEBI flagged a circular-trading case on 27 Sep 2012; authors note successful manipulation appears rare — [J.R. Varma blog](https://jrvarma.in/blog/Y2013/HFT-manipulation.html)
- Nifty Bank rejig (Dec 2025): HDFC Bank and ICICI Bank fell 1.25% on weight cuts — [Business Standard](https://www.business-standard.com/amp/markets/news/nifty-bank-rejig-trims-hdfc-and-icici-bank-heft-shares-fall-1-25-125120201155_1.html)

### Testable rules
- Pre-Aug-2026: on index-rebalance effective dates (Nifty semi-annual: effective last trading day of Mar/Sep; MSCI: last business day of Feb/May/Aug/Nov; FTSE: third Friday Mar/Jun/Sep/Dec — dates from announcements), compute for affected stocks the 15:00→15:30 return vs the stock's direction of estimated passive flow (Nuvama/brokerage estimates). Test whether price moves in the flow direction into 15:30 and reverts 09:15–09:30 next day. Also test non-affected Nifty 50 stocks on the same days (spillover).
- Aug–Dec 2026: compute auction close vs 15:15 last trade (one number per stock per day) and next-day open vs auction close; test whether the sign of the auction gap on rebalance/expiry days is predictable from the 14:45–15:15 imbalance (volume-weighted up-tick ratio) and whether it reverts at the open. This is a close-to-open trade, not a 1-min intraday trade.
- Expected size: index-fund tracking difference of +0.76 bp per rebalance day implies the aggregate "cost" to passive flow is small at index level; stock-level moves on rebalance days (0.6–4.0% reference-vs-close across jurisdictions) are large but concentrated in a few affected names, which are known in advance.

### Gaps
- No Indian study with 1-min data isolating last-30-min return direction (as opposed to volatility/volume) on ordinary days.
- No published stock-level statistics on CAS auction-price vs 15:15 deviations beyond the two index anecdotes.

---

## Part B — Effect 3: Pre-open call auction (09:00–09:08) and the 09:15 open

### Takeaway
Academic evidence on NSE's pre-open (introduced Oct 2010) is mixed on price-discovery efficiency, and I found no NSE study on a first-1-to-5-minute reversal/continuation after 09:15. International evidence (Hong Kong reversal, Singapore momentum) shows the sign is market-specific, so this must be tested empirically.

### Cited Findings
- Sharma & Gupta (2015, Indian Journal of Finance): Nifty + 10 constituents, 3 years before/after Oct 2010 call auction; no significant change in returns, lower volatility; conclude price discovery efficiency improved — [IJF](https://indianjournalofentrepreneurship.com/index.php/IJF/article/view/81127)
- Bag (working paper): information content of pre-open order imbalance "improved little" over the sample — [Distant Reader PDF](https://distantreader.org/stacks/journals/cjfa/cjfa-30366.pdf)
- Cogent/NITK (2014): market-model R² declined for both opening and closing returns for call-auction stocks and controls; decline smaller for opening prices of call-auction stocks — [NITK IDR](https://idr.nitk.ac.in/handle/123456789/26541)
- Older NSE time-of-day study: "open jump effect" and "persistent end of session effect"; post-rolling-settlement only the first 20 minutes had significant returns across all trading days — [i-scholar (Asian Journal of Management)](https://i-scholar.in/index.php/Ajm/article/view/179374) (abstract only; could not fetch)
- Hong Kong: pre-open price change reverses intraday; Singapore: momentum — [Bloomberg Tick Signals](https://www.bloomberg.com/professional/insights/data/tick-signals-using-tick-history-data-in-trading-strategies)
- Pre-open mechanics: equilibrium price = max tradable quantity; ties → smaller imbalance → closest to previous close — [Belong explainer](https://getbelong.com/blog/nifty-pre-open-session-explained.md); revised phases from 7 Sep 2026 (random close 09:08–09:10, matching 09:10–09:12, transition 09:12–09:15) — [Zerodha bulletin](https://zerodha.com/marketintel/bulletin/439989/introduction-of-closing-auction-session-cas-in-the-equity-cash-segment-and-certain-modifications-in-the-pre-open-auction-session)
- NSE intraday volatility and volume are highest in opening minutes (U-shape) — [Sampath & Gopalaswamy](https://ideas.repec.org/a/sae/emffin/v19y2020i3p271-295.html); 1-min Nifty futures 2011–2018 also U-shaped — reported in [MPRA 89689](https://mpra.ub.uni-muenchen.de/89689/1/MPRA_paper_89689.pdf)

### Testable rules
- Gap-fade: g = open(09:15 bar)/prev_close − 1 (prev_close = CAS/VWAP close). Test mean of r(09:15→09:20) and r(09:15→09:30) conditional on |g| deciles and on market-wide gap (Nifty); sort by whether the stock's gap exceeds the index gap (idiosyncratic gap) — idiosyncratic overshoot is where pre-open imbalance unwinding should appear.
- Opening-range continuation: r(09:20→09:45) conditional on sign of r(09:15→09:20) and relative volume in the first 5 min.
- Expected size: unknown for NSE; needs > ~10 bps after costs. The 09:15 bar carries the widest spreads of the day, so test with 09:16 entries, not 09:15 opens.

### Gaps
- No NSE paper found that uses 1-min/5-min data on post-open reversal; the i-scholar abstract could not be opened.

---

## Part B — Effect 4: Expiry-day effects on cash stocks (weekly index Tue; monthly stock F&O last Tuesday since Sep 2025)

### Takeaway
Indian expiry-day studies consistently find higher volume but weak/mixed evidence of price reversal; the strongest documented expiry effect in cash is manipulation of the last-30-min VWAP settlement window (rare, but SEBI-flagged) and Jane Street-style index-constituent buying/selling, which is institutional-scale and not a retail rule.

### Cited Findings
- Debasish (2010), Nifty futures Jun 2001–May 2009: expiry-day volume higher; no price distortions on expiry day/week for full sample and second sub-period; first sub-period showed higher volatility — [IDEAS](https://ideas.repec.org/a/rnd/arjebs/v1y2010i1p9-19.html)
- Gupta, Metia & Trivedi (2003/04), NSE stock options: higher expiry-day volume; tests of reversal/pinning — [EconWPA](https://econwpa.ub.uni-muenchen.de/econ-wp/fin/papers/0411/0411035.pdf)
- Mehta & Shah (2020), individual stock futures: overall negative effect on price and volume pre/post expiry — [Publishing India](https://publishingindia.com/storage/PDFBrochures/6206.pdf)
- VWAP settlement window vulnerability (Varma/Mohanram 2013) — [J.R. Varma](https://jrvarma.in/blog/Y2013/HFT-manipulation.html)
- Jane Street: concentrated activity in the final hour on expiry days aimed at index settlement; ₹4,370 crore bought in the morning and ₹5,372 crore sold in the afternoon on 17 Jan 2024 — [Moneylife](https://moneylife.in/article/explainer-what-are-sebis-findings-on-jane-street-groups-market-manipulation/77594.html)
- Expiry-day options turnover concentration: 14:30–15:00 = 8.83% and 15:00–15:30 = 5.72% of day (pre-CAS) — [TheTaxCorp](https://thetaxcorp.in/article/sebi-consultation-paper-on-closing-auction-session-settlement-methodology)
- Current regime: from 7 Dec 2026 expiring index derivatives stop at 15:30 and settle on the VWAP of the last 30 min of continuous trading; stock derivatives trade to 15:45 — [NewsOnAir](https://newsonair.gov.in/sebi-revises-timings-and-operational-framework-of-closing-auction-session/)
- Forum allegation (unverified): institutions use final-minute trades to hit target closes on expiry days — [TradingQnA](https://tradingqna.com/t/everything-you-need-to-know-about-the-closing-auction-session-cas-starting-august-3/195801?page=3)

### Testable rules
- Settlement-window reversal (pre-Aug-2026 and post-Dec-2026 regimes): for Nifty 50 constituents on expiry days, r_settle = VWAP(15:00–15:30)/close(14:59) − 1; test next-day r(09:15→09:30) and same-day (post-Dec) r(15:30 → CAS close) against r_settle. Hypothesis: forced VWAP-tracking flow overshoots and partially reverts.
- Monthly stock-futures expiry (last Tuesday): arbitrage unwind — cash-futures basis convergence requires arbitrageurs to sell cash (if long cash/short futures) into the settlement window; test whether high-OI stocks show negative 15:00–15:30 drift vs low-OI stocks on monthly expiry. Needs OI data (not OHLCV) for the sort; OHLCV-only proxy: relative volume in 15:00–15:30 vs 20-day mean.
- Expected size: Indian literature reports no systematic expiry-day price distortion at index level; per-stock settlement-window effects are undocumented. Hypothesis only.

### Gaps
- No post-Sep-2025 (Tuesday expiry) or post-Aug-2026 (CAS) study of cash-equity expiry behaviour found.

---

## Part B — Effect 5: F&O ban list entries/exits, Nifty inclusion/exclusion effective dates, MSCI/FTSE days

### Takeaway
Nifty inclusion/exclusion has well-documented effective-day price pressure that reverses within ~9 days (Kumar; Joshipura & Janakiramanan), and MSCI/FTSE days carry the largest last-30-min volatility; F&O ban entries/exits have only anecdotal (Zee −11%, +4% on exit) evidence. All are close-of-day flows — now expressed in the CAS print for Nifty 50 names.

### Cited Findings
- Kumar (NSE working paper, 1996–2003 data, reported): effective-day price effect for Nifty inclusions ≈ +1.47%, reversed by day 9; no announcement-day effect — [NSE research paper](https://nsearchives.nseindia.com/content/research/comppaper90.pdf) (full text could not be fetched; figure from search summary); same 1996–2003 study described: effective-day effects for Nifty reversed by ninth day, Jr. Nifty none → price pressure — [SAGE mirror](https://https-sage-cnpereading-com-443.webvpn1.xju.edu.cn/doi/10.1177/0972622520070103)
- Joshipura & Janakiramanan (2015, AAJFA): inclusions — no significant announcement abnormal return, significant positive effective-day return that does not persist; exclusions — significant negative effect in the announcement window and around effective day, fading; effective-day volume spike attributed to index funds/ETFs; support price pressure over liquidity hypothesis — [IDEAS](https://ideas.repec.org/a/ids/afasfa/v5y2015i1p21-36.html)
- S&P CNX Nifty study: added stocks significant price and volume rise on effective date; deleted stocks significant volume, insignificant price — [PSAU/Elsevier](https://psau.sa.elsevierpure.com/en/publications/associated-effects-of-index-composition-changes-an-evidence-from-)
- Community backtest (33 Nifty 50 inclusions 2015–2025, t=0 effective date, price-only, not benchmark-adjusted): 1 week before −1.60%; 2 weeks after +2.21% mean / +3.07% median, 78.8% win rate, s.d. 5.6%; 3 months after +3.19% mean / −0.07% median; author calls the 2-week edge "real but quite modest" — [TradingQnA](https://tradingqna.com/t/the-nifty-50-inclusion-trade-does-it-still-work/195419)
- Nuvama passive-flow estimates are routinely published ahead of effective dates (e.g., Vedanta demerged entities ~$159 mn for 30 Sep 2026 NSE rebalance; Wipro −$246 mn / BSE +$741 mn for a Nifty 50 reconstitution; Reliance −$523 mn MSCI Aug 2026) — [Outlook Business](https://www.outlookbusiness.com/markets/nse-index-changes-may-drive-159-mn-into-vedanta-demerged-stocks); [Swastika](https://www.swastika.co.in/blog/wipro-share-price-and-nifty-50-reconstitution-bse-flows-free-float-shifts-and-re); [NiftyTrader](https://www.niftytrader.in/markets/reliances-5000-crore-msci-outflow-new-auction/)
- MSCI Aug 2026 under CAS: 60 of 210 stocks hit the ±3% auction band; weight-losers saw lower execution — [5paisa](https://www.5paisa.com/blog/msci-rejig-cas-turnover)
- F&O ban mechanics: entry when aggregate OI ≥95% of MWPL (checked end of day, effective next day); exit when OI ≤80%; cash trading unrestricted during ban — [Angel One](https://www.angelone.in/knowledge-center/futures-and-options/what-is-f-and-o-ban); [Liquide](https://blog.liquide.life/fo-ban-meaning-mwpl-trading-guide/). Zee case: −4% on ban day (15 Jun), −11% from pre-ban close by 20 Jun, +4% on exit (21 Jun) — [ICICI Direct](https://www.icicidirect.com/ilearn/stocks/articles/future-and-options-ban-impact-on-stock) (single anecdote)

### Testable rules
- Inclusion effective date (regime-dependent): pre-Aug-2026, r(15:00→15:30) on effective day for included vs excluded stocks, and next-day r(09:15→10:00); post-Aug-2026, auction-close vs 15:15 last trade, and next-day open-to-10:00 reversal. Expected size: ~+1.5% effective-day (old data), reverting over days; the intraday component is unmeasured.
- F&O ban entry/exit (Nifty 50 names rarely enter bans; this is mainly a mid-cap effect): on ban-entry day (known from NSE's prior-day list), test r(09:15→09:30) and full-day; on exit day test r(09:15→10:00). Evidence: anecdotal only.
- MSCI/FTSE days: same close-pressure template as Effect 2, with Nuvama estimates giving flow sign.

### Gaps
- No stock-level intraday (1-min) decomposition of effective-day price pressure in India.
- No systematic F&O ban return study found; only broker blogs.

---

## Part B — Effect 6: Intraday post-earnings announcement drift (results released during market hours)

### Takeaway
Indian PEAD evidence is daily-frequency and mixed (drift over elongated windows in 2002–2011 data; Gupta & Dhusia 2021 find prices adjust properly for 2014–2018). I found no Indian study using 1-min/5-min data around in-session announcements; this is an open empirical question.

### Cited Findings
- 469-company study (2002–2011): significant pre- and post-event abnormal returns in most quarters; most abnormal return over an elongated window rather than close to the event — [SAGE mirror, DOI 10.1177/0972262914564042](https://https-sage-cnpereading-com-443.webvpn1.xju.edu.cn/doi/10.1177/0972262914564042)
- Gupta & Dhusia (2021), 100 NSE firms 2014–2018: abnormal returns negatively associated with earnings surprises; conclude prices adjust properly after announcements — [Trends Economics and Management](https://journals.vutbr.cz/index.php/trends/article/view/541)
- IIMB repository study: post-earnings drift exists over a 120-day window plus pre-announcement effects — [IIMB](https://repository.iimb.ac.in/handle/2074/17935)
- US intraday benchmark: Woodruff & Senchack (1988) found NYSE reaction began ~15 minutes after announcement — cited in [Inflibnet thesis](https://gnanaganga.inflibnet.ac.in:8443/jspui/bitstream/123456789/7961/1/A%20Study%20of%20Efficiency%20of%20The%20Indian%20Stock%20Market.pdf)
- Anecdotes of in-session result reactions (Ranbaxy reversed intraday gain after weak Q3 on 28 Jan 2015; Hero MotoCorp reversed losses after Q2 2013) — [Business Standard](https://www.business-standard.com/amp/article/news-cm/key-indices-end-flat-after-high-intraday-volatility-115012801105_1.html); [Business Standard](https://www.business-standard.com/amp/article/news-cm/hero-motocorp-reverses-intraday-losses-after-declaring-q2-result-113102300673_1.html)

### Testable rules
- Event time t0 = exchange filing timestamp (NSE/BSE corporate announcements carry a timestamp; OHLCV alone cannot identify t0, so this needs the announcement feed). Rule: r(t0+5 → t0+60) and r(t0+5 → t0+180) conditional on sign and size of r(t0 → t0+5) and relative volume. Alternative OHLCV-only proxy: a 5-min bar with volume >5x the 20-day same-time mean and |return| >1% during 09:30–14:30 on a known results date.
- Expected size: unknown for India; US intraday literature suggests most adjustment within ~15–30 minutes, implying little tradeable drift after costs.

### Gaps
- No Indian 1-min/5-min earnings-reaction study found.

---

## Part B — Effect 7: Block deal windows (08:45–09:00, 14:05–14:20)

### Takeaway
Block trades on NSE show front-running starting ~8 minutes before block purchases (not sales) and a temporary impact larger than the permanent one for purchases (Agarwalla & Pandey); since 2018 blocks execute in a separate window within ±1% of the 13:45–14:00 VWAP, so the testable question is whether 13:45–14:05 drift precedes a 14:05–14:20 block print and reverts afterwards.

### Cited Findings
- Agarwalla & Pandey (IIMA): permanent impact larger for block purchases than sales; temporary > permanent for purchases (unlike other markets); prices rise ("front running") 8 minutes before block purchases, not before sales; block sale prices revert quickly with small permanent impact; non-AON trades have higher impact; multiple blocks same day raise permanent impact — [IIMA](https://www.iima.ac.in/publication/price-impact-block-trades-and-price-behavior-surrounding-block-trades-indian-capital) (pre-2018 regime, when blocks traded 09:15–09:50)
- BSE block deals 2006–2012 (125 deals): average +1.32% on block date — [IUP](https://www.iupindia.in/1507/Applied%20Finance/Price_Impact_of_Block.html)
- Window rules: 08:45–09:00 reference = previous close; 14:05–14:20 reference = VWAP 13:45–14:00; ±1% band; min ₹10 crore — [NSE circular CMTR36573](https://nsearchives.nseindia.com/content/circulars/CMTR36573.pdf)

### Testable rules
- Afternoon window: for Nifty 50 stocks on days with an afternoon block (from NSE block-deal disclosures; identifiable post hoc), compare r(13:45→14:05) and r(14:20→14:50) to non-block days. Hypothesis: the reference-price window (13:45–14:00) attracts positioning by parties who know a block is coming, followed by reversion after 14:20.
- Pure OHLCV proxy: abnormal 1-min volume spike at 14:05–14:20 (block prints are reported in the cash segment) → test r(14:20→15:00).
- Expected size: Agarwalla & Pandey do not give bps in the abstract; the BSE study's +1.32% is a daily effect on mostly mid-caps. For Nifty 50 names the intraday signature is probably <10 bps (hypothesis).

### Gaps
- No post-2018 study of the 14:05–14:20 window's price footprint was found.

---

## Part B — Effect 8: Lunch-hour and 14:00–15:00 "institutional VWAP program" persistence / intraday time-series momentum

### Takeaway
Intraday time-series momentum (first half-hour predicts last half-hour) is documented for the S&P 500 and in 11 of 16 international markets, but I could not confirm India is in that sample and found no Nifty 50 test; NSE evidence only establishes the U-shaped volume/volatility profile (mid-day trough), which is the pre-condition for afternoon VWAP-program persistence, not evidence of it.

### Cited Findings
- Gao, Han, Li & Zhou: S&P 500 ETF 1993–2013, first half-hour return predicts last half-hour return; stronger on volatile, high-volume, and macro-news days — [Alpha Architect summary](https://alphaarchitect.com/2014/08/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/)
- International extension: significant in most of 16 countries; 11/16 positive OOS R² — [Nottingham repository](https://nottingham-repository.worktribe.com/OutputFile/5273196) (country list not retrievable; India inclusion unconfirmed)
- Indonesia: first-30-min return significantly positive predictor of last-30-min return for winners and losers — [IJBS](https://publisher.unimas.my/ojs/index.php/IJBS/article/view/7630)
- Srivastava, Chakravorty & Singhal (SSRN 3345280) test momentum in Indian equity futures on daily and intraday bars, 2010–2019 — [Quantpedia note](https://vvv.quantpedia.com/?p=4230) (findings not retrieved)
- NSE: U-shaped intraday volume, trades and volatility; mid-day trough; volatility differences disappear after controlling for volume — [Sampath & Gopalaswamy](https://ideas.repec.org/a/sae/emffin/v19y2020i3p271-295.html); Nifty futures 1-min 2011–2018 U-shape — [MPRA 89689](https://mpra.ub.uni-muenchen.de/89689/1/MPRA_paper_89689.pdf); NSE liquidity measures U-shaped (Krishnan & Mishra 2012) — [IDEAS](https://ideas.repec.org/p/zbw/esprep/183471.html)

### Testable rules
- ITSM for Nifty 50 (regime-aware last half hour): r_last = r(14:45→15:15) in Aug–Dec 2026, r(15:00→15:30) otherwise; regress on r_first = r(09:15→09:45) and r_overnight; report OOS R² and a long/short sign strategy with 8–15 bps round-trip cost.
- Afternoon persistence: P(sign r(14:00→15:00) = sign r(09:15→14:00)) vs 50%, conditional on relative volume in 12:00–13:30 being low (quiet lunch → programs dominate afternoon).
- Expected size: Gao et al. report economically significant but small per-day returns in the US (ETF, near-zero costs); for Indian single stocks at ~10 bps cost this is likely marginal unless conditioned on high-volatility days.

### Gaps
- No Nifty/NSE ITSM result found; India's membership in the 16-country sample unverified.

---

## Part B — Effect 9: Short covering / long unwinding near close on big-move days; price-band (circuit) dynamics

### Takeaway
No Indian study was found quantifying end-of-day reversal on large-move days or next-day returns after band hits; Nifty 50 stocks have no daily price bands (F&O stocks), so circuit dynamics are a mid/small-cap effect and out of scope for Nifty 50 OHLCV testing.

### Cited Findings
- Price bands of 2%/5%/10% apply only to non-F&O stocks; F&O stocks have no daily band (dynamic bands instead); 20% for others; index circuit breakers since 2 Jul 2001 — [IIFL](https://indiainfoline.com/knowledge-center/online-share-trading/what-are-circuit-filters-limits-and-how-are-they-used/)
- Under CAS, F&O stocks face a static ±3% auction band — [Outlook Money](https://www.outlookmoney.com/invest/nse-extended-fo-timings-and-new-closing-auction-session-rules-explained); 60/210 stocks hit it on MSCI day 31 Aug 2026 — [5paisa](https://www.5paisa.com/blog/msci-rejig-cas-turnover)
- Band revisions move prices (Adani stocks +4.5% after bands widened, 2023) — [Business Standard](https://www.business-standard.com/amp/companies/news/adani-stocks-gain-up-to-5-after-stock-exchanges-widen-circuit-filters-123060700684_1.html)
- End-of-day volatility is elevated (U-shape) — [Sampath & Gopalaswamy](https://ideas.repec.org/a/sae/emffin/v19y2020i3p271-295.html)

### Testable rules
- Big-move-day close reversal: on days where |r(09:15→14:30)| > 2σ (20-day), test r(14:30→15:15 or 15:30) and the close-to-open return. Mechanism: intraday shorts must cover before square-off (shorts in cash are intraday-only in India since there is no retail stock lending at scale), so down days should show more pre-square-off covering than up days show selling. This asymmetry (short covering stronger than long unwinding) is the specific hypothesis.
- CAS-band clip: when the auction indicative price is at the ±3% band (observable post hoc as close exactly 3% from reference), test next-day open drift in the band direction (unfilled imbalance).
- Expected size: unknown; hypothesis.

### Gaps
- No study on Indian end-of-day reversal conditional on intraday move size; no next-day-return study after band hits.

---

## Cross-cutting: friction assumptions to use when sizing any Part B edge

### Takeaway
Use ≈8 bps statutory+brokerage (₹1 lakh), ≈5 bps (₹10 lakh), plus 1 bp spread and 2–5 bps slippage for market orders in Nifty 50 names; forced square-off adds ~6 bps on ₹1 lakh. Any effect must show >15 bps mean per trade (₹1 lakh) or >10 bps (₹10 lakh) to be worth testing live.

### Cited Findings
- Rates: STT 0.025% sell; NSE 0.00297%/side; SEBI 0.0001%; stamp 0.003% buy; GST 18% on brokerage/exchange/SEBI — [Bigul](https://www.bigul.co/pricing); [IBKR India](https://www.interactivebrokers.com.sg/en/accounts/fees/indiaStockExchangeFees.php); brokerage ₹20/order — [ICICI Direct](https://icicidirect.com/ilearn/stocks/articles/what-is-intraday-brokerage-and-charges); Zerodha square-off ₹50+GST — [Zerodha](https://support.zerodha.com/category/account-opening/charges-at-zerodha/articles/auto-square-off)
- Nifty 50 spreads ≈1 tick (5 paise) ≈0.3–0.5 bp on ₹1,000–3,000 stocks — [OneTradeJournal](https://onetradejournal.com/glossary/bid-ask-spread)
- SEBI: loss-makers' costs = 57% of losses; profit-makers' = 19% of profits — [Moneylife](https://moneylife.in/article/7-out-of-10-individual-intraday-traders-in-equity-cash-segment-make-losses-sebi-study/74733.html)

### Inferences
- Arithmetic (mine): ₹1 lakh round trip ≈ ₹82 (8.2 bps) before slippage; ₹10 lakh ≈ ₹478 (4.8 bps). The STT sell-side 2.5 bps is the floor nobody escapes (Kamath's point), so even a zero-brokerage member needs >3 bps gross on every cash round trip.

### Gaps
- No measured average slippage for 1-min market orders in Nifty 50 names; 2–5 bps is an assumption to be calibrated from the user's own fills.

---

## Overall evidence vs hypothesis summary

- Evidence (published, Indian): U-shaped intraday volume/volatility (Sampath & Gopalaswamy); Nifty inclusion effective-day price pressure ~+1.5% reverting within ~9 days (Kumar; Joshipura & Janakiramanan); rebalance-day last-30-min volatility 1.5–3.3x with FPIs 56–60% of affected-stock value (SEBI consultation data via TradingQnA); block-purchase front-running from 8 min before (Agarwalla & Pandey); VWAP-settlement manipulability (Varma/Mohanram; SEBI 2012 case; Jane Street 2025 order); expiry-day volume up, price reversal weak/mixed; retail intraday loss rates (SEBI 71%/93%); algos = 96–97% of prop/FPI profits; algos >50% of cash turnover.
- Hypothesis (no Indian data found): MIS square-off sell-off and bounce; post-open 1–5 min reversal/continuation; intraday PEAD on in-session results; 14:05–14:20 block-window footprint post-2018; afternoon VWAP-program persistence / ITSM for Nifty 50; big-move-day short-covering asymmetry; CAS band-clip next-day drift; F&O ban entry/exit returns.
- Regime caveat: every close-of-day rule has three regimes (VWAP close → CAS 15:15–15:35 → CAS 15:30–15:40 from 7 Dec 2026); the Aug–Dec 2026 window has no 1-min bars after 15:15 for Nifty 50 stocks.
