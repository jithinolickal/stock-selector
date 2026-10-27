# Intraday Index-Option Strategies Traded Every Day (India, 2021-2026): Evidence Review

Scope: Nifty / Sensex / Bank Nifty intraday option strategies that run on non-expiry days (or on all days), post-SEBI changes (one weekly expiry per exchange since 20 Nov 2024; NSE expiries on Tuesday and BSE on Thursday since 1 Sep 2025). Evidence grades: A = peer-reviewed/replicated; B = platform/newsletter backtest with costs disclosed; C = anecdote, marketing, or undisclosed costs. Research date: 2026-10-26.

Headline: the only multi-year, cost-inclusive, DTE-separated backtest found (Zerodha "In The Money", 2019-2025) says the plain 9:20 straddle has edge mainly at 0 DTE, 1 DTE faded after 2024, 2 DTE turned positive only recently, and 3-4 DTE are "duds". No source published a cost-adjusted, multi-year positive result for a plain short straddle/strangle/condor on 3+ DTE days. This agrees with the user's own 1-min backtester finding.

## Current expiry calendar and cost regime (context for every strategy below)

### Takeaway
Only two weekly expiries exist now: Nifty (Tuesday) and Sensex (Thursday); every other index is monthly. STT on option sale premium is 0.1% and SEBI/exchange cost drag is what kills small-lot straddles in every cost-inclusive study found.

### Cited Findings
- Weekly expiries: Nifty 50 every Tuesday (monthly last Tuesday); Sensex every Thursday (monthly last Thursday). Bank Nifty, FinNifty, Midcap Select, Nifty Next 50 are monthly, last Tuesday; Bankex and Sensex 50 monthly, last Thursday. SEBI allowed one weekly benchmark per exchange from 20 Nov 2024; NSE moved all expiries Thursday to Tuesday and BSE to Thursday from 1 Sep 2025. Holiday rule: expiry advances to the previous trading day (e.g., Nifty 20 Oct 2026 -> Mon 19 Oct; 10 Nov -> 9 Nov; 24 Nov -> 23 Nov 2026) — [AlgoTest All Index Expiry Day](https://algotest.in/blog/all-index-expiry-day.md)
- AlgoTest guidance: test pre- and post-1 Sep 2025 Nifty schedules separately so one regime does not hide problems in the other — [AlgoTest](https://algotest.in/blog/all-index-expiry-day.md)
- SEBI FY26 study: 87.7% of individual F&O traders lost money in FY26; aggregate net loss ₹91,685 crore (down 18% YoY); 59% of index-options turnover still on expiry day, 75% within one day of expiry; ~92% of individual losses came from options; ~97% of traders predominantly followed option-buying — [Open Magazine summary of SEBI study](https://openthemagazine.com/business/sebi-fo-loss-study-explained-why-9-in-10-retail-traders-lost-91685-crore-in-fy26); [Moneylife](https://www.moneylife.in/article/retail-fo-traders-lose-91685-crore-in-fy2526-despite-sebi-curbs-average-loss-hits-117-lakh-govt/81318.html)
- SEBI FY25 study: >91% lost; net losses ₹1,05,603 crore in FY25 vs ₹74,812 crore in FY24 after transaction costs; sample = top 13 brokers, ~96 lakh unique F&O traders — [Business Standard](https://www.business-standard.com/amp/markets/news/net-losses-of-traders-in-fo-widens-in-fy25-sebi-study-125070701221_1.html)
- Zerodha ITM (Sensex 0DTE study): results net of ₹20 brokerage/order, transaction costs, 0.25% slippage per leg; "not viable up to five lots because brokerage and transaction costs consume the alpha" — [In The Money, Jun 22 2026](https://inthemoneybyzerodha.substack.com/p/sensex-0dte-straddle-or-strangle)
- Zerodha ITM (7-year 9:20 straddle): same cost model; 5 Nifty lots needed ~₹7.5L margin previously vs ~₹17.5L now (100%+ increase after lot-size change); "alpha doesn't scale well below about five lots because costs eat it" — [In The Money, Oct 9 2025](https://inthemoneybyzerodha.substack.com/p/seven-years-of-the-920-straddle-past)
- Marketcalls estimate: market-order entry, combined transaction cost + slippage = 1-2.5% of premium turnover for a 9:20 straddle — [Marketcalls, Aug 2021](https://www.marketcalls.in/futures-and-options/how-the-9-20-intraday-straddlers-are-being-gamed.html)

### Inferences
- Any candidate on non-expiry days must clear roughly 1-2.5% of premium turnover in costs per round trip; with lower non-expiry theta per hour, this cost bar is proportionally much higher than on expiry day.
- Bank Nifty "expiry-day" straddles are now a once-a-month event; the cross-index "trade whichever index expires today" idea is reduced to Nifty-Tue + Sensex-Thu (+ monthly days).

### Gaps
- No source quantified the STT 0.1%-on-sell-premium impact separately from other costs for intraday straddles.

## Q1. Non-expiry-day short straddle/strangle variants: entry time, premium/delta strikes, wait-and-trade, re-entry, trailing SL, combined-premium SL — any positive expectancy on 1/2/3+ DTE?

### Takeaway
The only cost-inclusive, DTE-separated multi-year evidence (Zerodha ITM, Nifty 2019-2025, 9:20 ATM straddle, 20% per-leg SL, exit 15:20) finds 0 DTE "most consistent", 1 DTE good 2019-2023 then faded after 2024, 2 DTE positive only recently (2024-25), 3 DTE profitable in one year only, 4 DTE "barely worth it". No published cost-adjusted multi-year test of later entries, premium-based strikes, wait-and-trade, re-entry, or trailing SL on non-expiry days was found; all such claims are either single-day heatmaps, asserted ranges without data, or Bank Nifty-era (pre-2024) anecdotes.

### Cited Findings
- Zerodha ITM 7-year study rules: Nifty, sell ATM straddle at 09:20, SL 20% above entry per leg (₹100 CE -> ₹120 stop), square off 15:20, lot normalised to 75, 5 lots, net of ₹20/order brokerage + transaction costs + 0.25% slippage/leg; each DTE (4..0) tested separately "to avoid day-of-week effects" — [In The Money, Oct 9 2025](https://inthemoneybyzerodha.substack.com/p/seven-years-of-the-920-straddle-past)
- Same study, DTE results (qualitative; numbers only in images): 4 DTE "Barely Worth It" (meaningful green only 2019 and 2024); 3 DTE "Another Dud" (worked only 2021); 2 DTE "The New Contender" (non-performance for five years, then recent improvement; author speculates Sensex Tuesday-expiry link); 1 DTE consistent 2019-2023, faded since 2024 as edge moved to 2 DTE; 0 DTE most consistent, weak 2023-2024, recovered 2025 but below pre-2022 — [In The Money, Oct 9 2025](https://inthemoneybyzerodha.substack.com/p/seven-years-of-the-920-straddle-past)
- Same study, year-wise (qualitative): 2019 "dream year", 2020-21 steady, 2022 spike, 2023 weakest, 2024 effective not spectacular, 2025 muted; conclusion "some alpha left… nowhere near heyday"; untested variants suggested: MTM/combined-premium/trailing stops, fixed-premium entries, 12:20 "time-based straddle", IV-threshold entry — [In The Money, Oct 9 2025](https://inthemoneybyzerodha.substack.com/p/seven-years-of-the-920-straddle-past)
- Zerodha ITM position-sizing piece on the same Nifty intraday 20%-SL straddle: historical max drawdown ₹20,000 per lot; author doubles to ₹40,000 for live; margin ~₹3.0-3.25L for 0DTE ATM straddle; recommends ~₹3.65L-₹4.15L capital per straddle; buying ₹3 wings cuts margin to ~₹1.75-2L but is "leverage not hedge" — [In The Money, Position Sizing Part 3](https://inthemoneybyzerodha.substack.com/p/position-sizing-part-3-sizing-option)
- Marketcalls Bank Nifty 9:20 straddle, weekly options since 2017, 35% SL both legs, 0.5% commission+slippage: edge weakened in 2023 as volatility fell; "shifting entry to 10:30 AM could have done much better" vs 9:20 in 2023 (figures only in charts; Bank Nifty weeklies no longer exist) — [Marketcalls, "Is the 920 straddle no more working"](https://www.marketcalls.in/futures-and-options/is-the-920-straddle-no-more-working.html)
- Marketcalls Quantman backtests of 9:20 Nifty straddle (monthly from 1 Jan 2017, weekly from 1 Apr 2019), 40% SL-M per leg, exit 15:10; results only as screenshots; author's caveat that "80% of the profitable system post the transaction and slippage will not yield smooth returns" — [Marketcalls, Aug 2021](https://www.marketcalls.in/futures-and-options/how-the-9-20-intraday-straddlers-are-being-gamed.html)
- TradingQnA "Detailed analysis of 920 Short Straddle" (Jan 2023): ~1,300 trades over 5 years, 25% per-leg SL, stopped leg exited and other leg held to close; Wednesday best weekday, Friday worst; profits on gap-up/gap-down/flat days; "most of its profits will come from few trades" — removing top 10% of trades (~130) turns overall result negative; costs not disclosed; numbers only in images — [TradingQnA](https://tradingqna.com/t/detailed-analysis-of-920-short-straddle-strategy-is-it-stopped-working/130677)
- TradingQnA "Reports of the death of 920 straddle" (Dec 2024, Nifty, 1-min data, 9:20 sell cheapest ATM straddle, no SL, exit 15:15, costs not stated): 20 days, net +434.2 pts, 12 wins/8 losses; non-expiry days 16 trades net +269 pts (10W/6L); expiry days 4 trades net +165.2 (one day, 19 Dec, +168.2); largest loss -79.45 (20 Dec, a 4-DTE Friday) — [TradingQnA](https://tradingqna.com/t/reports-of-the-death-of-920-short-straddle-are-greatly-exaggerated/179061)
- Quintalmind (Nifty weeklies 2019-2024, methodology and costs NOT disclosed, win-rate ranges asserted): 9:20 expiry-day straddle ~65-70% WR at 25% SL (avg loss 2-3x avg win), ~60-65% at 30% SL, ~72-78% at 50% SL; 9:30 entry +2-3 pts WR with 5-10% less premium; 10:00 entry 68-75% WR (25% SL), 10-20% less premium; 13:00 expiry-only 75-80% WR but "one trending session erases several days"; no-SL hold ~55-60% WR; best time-based systems PF 1.5-2.0; live typically 15-30% worse than backtest — [Quintalmind](https://www.quintalmind.com/blog/time-based-straddle-strategy-nifty-options) (Grade C: asserted, no data tables)
- AlgoTest Daily Straddle Heatmap, Fri 20 Dec 2024 (non-expiry for all indices; axes SL 10-100% x entry 09:16/09:45/10:15/10:45/11:15): Nifty total +₹83,893 (best 09:16 +37,528; SL 70-100 strongest), BankNifty -10,762, MidcapNifty -76,128, FinNifty -22,050; costs/lot basis not stated — [AlgoTest heatmap 20 Dec 2024](https://algotest.in/blog/daily-straddle-heatmap---20th-december-2024.md)
- AlgoTest Daily Straddle Heatmap, Thu 16 Jan 2025 (Nifty weekly expiry day under old schedule): Nifty +₹116,276 (best 11:15 +25,706; SL 60-70 best), BankNifty +11,313 (09:16 worst -6,242, 13:15 best), FinNifty -6,060, MidcapNifty -17,753; "early session 09:16-10:45 weakest" — [AlgoTest heatmap 16 Jan 2025](https://algotest.in/blog/daily-straddle-heatmap---16th-january-2025.md)
- Straddle Lab (Quantimental Capital, TradingQnA, 2026): heatmap of "hundreds" of entry-time x SL combos for Nifty/Sensex/BankNifty intraday straddle/strangle/Batman; a user (Danny) reports the best entry time and SL shift across 1-week/1-month/3-month windows; vendor says its Robustness/Consistency metrics "hold up in walk-forward" but shares no numbers; costs not mentioned — [TradingQnA](https://tradingqna.com/t/straddle-lab-a-visual-way-to-explore-hundreds-of-intraday-options-selling-setups/198597) (Grade C)
- IT Jegan (AlgoTest interview, 2023): trades DTE 0 only, "trading on other days adds no advantage… 5 days, 5 expiries is good" (pre-Nov-2024 regime); smaller SL better before 10:00, bigger SL after 10:00; 2023 Jan-Apr +12%, May -7%, Jun-Jul negative; estimates ~20% premium compression from crowding — [AlgoTest](https://algotest.in/blog/in-conversation-with-it-jegan.md) (Grade C)
- Stockmock Bank Nifty intraday straddle, 5 years: 20% SL "much better return" than 30% SL with slightly lower win-%; no numbers, no costs — [TradingQnA](https://tradingqna.com/t/stop-loss-percentage-for-intraday-banknifty-short-straddle/125436) (Grade C)
- Stockmock 9:20 ATM straddle, 50% SL per leg, stopped leg only exited (2020): Nifty and Bank Nifty profitable "almost every month"; no period/costs/numbers — [TradingQnA](https://tradingqna.com/t/atm-short-straddle-intraday-strategy-nifty-bank-nifty/88032) (Grade C)
- Third-party "920 Stradel" report, Oct 2022-Apr 2023, 5-min data: total profit ₹32,292.50, max DD -17.77% (Dec 2022-Feb 2023), annualised Sharpe 1.55; rules/costs not visible — [Scribd](https://www.scribd.com/document/646391264/Backtesting-report) (Grade C)
- Marketcalls on stop-hunting: 20 Aug 2021, Nifty 16450PE jumped 122.70 -> 803.50 in ~1 second, triggering 6,287 lots of SL-M orders; est. slippage 100-680 pts/lot (₹5,000-34,000/lot); 50-ending strikes 3-10x thinner than 100-strikes; exchange later restricted SL-M in options — [Marketcalls](https://www.marketcalls.in/futures-and-options/how-the-9-20-intraday-straddlers-are-being-gamed.html)
- Quantman "Spike Protection": SL fires only if price stays beyond SL for N seconds (e.g., 10 s) to avoid expiry-day spikes; no backtest numbers — [Quantman blog](https://www.quantman.trade/blog/prevent-your-trades-exit-from-temporary-market-spikes/)

### Inferences
- The user's finding (non-expiry straddle negative after costs) is consistent with Zerodha's 3-4 DTE "dud" result; the only non-expiry candidates with any B-grade support are 2 DTE (recent, unproven, regime-dependent) and 1 DTE (historical edge, faded post-2024).
- The 2 DTE Nifty day is Friday (2 trading days before Tuesday expiry) and the 1 DTE day is Monday; the Zerodha author's hypothesis that Sensex Thursday expiry helps Nifty 2-DTE is speculative.
- Single-day heatmaps (AlgoTest) show that on both an expiry and a non-expiry day the "best" entry time swung between 09:16 and 11:15 — supporting the Straddle Lab user's observation that optimal entry time is unstable; any entry-time optimisation should be judged on zones, not cells.
- Re-entry and trailing-SL variants are advertised by platforms (AlgoTest docs) but no cost-inclusive multi-year result for them was found; Zerodha's author explicitly dislikes re-entries (higher VaR).

### Gaps
- No public dataset gives the actual year-wise P&L per DTE from the Zerodha study (images only). Replicating that exact rule set (9:20, 20% SL/leg, 15:20 exit, 0.25% slippage/leg, ₹20/order) in the user's backtester, split by DTE, is the fastest way to calibrate.
- No cost-adjusted backtest found for: premium-based strikes (e.g., sell ₹X each), 0.3-0.5% OTM, 20-30 delta intraday on non-expiry days, wait-and-trade, combined-premium SL, trailing/lock-profit SL, or re-entry on SL. Everything on these is vendor feature documentation or anecdote.
- Medium article "Optimized 920 Straddle… >80% annually" (Bank Nifty, AlgoTest, 5 years) could not be fetched (403); it is Bank Nifty weekly-era anyway.

## Q2. 1-DTE (day-before-expiry) theta strategies

### Takeaway
1-DTE Nifty 9:20 straddle (20% SL) was "consistent" 2019-2023 in Zerodha's cost-inclusive test but "faded since 2024"; no other 1-DTE-specific Indian backtest exists in public. US 1-day NDX ATM straddle selling (with 2-pt slippage) lost in both 2023 and 2024.

### Cited Findings
- Zerodha ITM: "1 DTE: consistent from 2019 to 2023, then faded since 2024 as the edge moved to 2 DTE" (9:20 ATM, 20% SL/leg, exit 15:20, costs included) — [In The Money, Oct 9 2025](https://inthemoneybyzerodha.substack.com/p/seven-years-of-the-920-straddle-past)
- Dec 2024 1-min Nifty no-SL straddle: 1-DTE entries 4 Dec +23.45, 11 Dec +64.00; 2-DTE 3 Dec +26.25 (tiny sample, no costs) — [TradingQnA](https://tradingqna.com/t/reports-of-the-death-of-920-short-straddle-are-greatly-exaggerated/179061)
- US analogue (Nasdaq/Russell Rhoads): consistent seller of NDX 1-day ATM straddles (2 pts/trade slippage) lost in 2023 and 2024; 2024 loss 3,376.85 pts, average short-trade loss 14.13 pts; buyers made >2,400 pts in 2024; mid-2024 seller was +78.37 YTD before H2 losses — [Nasdaq](https://www.nasdaq.com/articles/1-day-nasdaq-100-money-straddle-performance-analysis); [Nasdaq mid-year](https://www.nasdaq.com/articles/ndx-1-day-atm-straddle-mid-year-performance-update)
- Nasdaq/Indiana white paper (NDX 1-day ATM straddles 2022-Q3 2025): buyers did much better than sellers; best day to sell varies by weekday; Tuesday most efficiently priced; weekend volatility overpriced — [Nasdaq](https://www.nasdaq.com/articles/new-white-paper-explores-ndx-straddle-performance-day-week) (page timed out; from search summary)
- Kotak Securities publishes discretionary Nifty short-strangle setups on expiry days with VIX ~12-13 in Jul 2026 — trading commentary, not evidence — [Business Today](https://www.businesstoday.in/markets/stocks/story/nifty-weekly-expiry-strategy-kotak-securities-support-resistance-short-strangle-541316-2026-07-07)

### Inferences
- With Nifty expiring Tuesday, 1-DTE = Monday, which now carries weekend gap risk at entry (Zerodha author flags "weekend effects may now matter"); the historical 1-DTE edge was measured when 1-DTE was Wednesday.
- 1-DTE is the best-supported non-expiry candidate only on pre-2024 data; it should be treated as a hypothesis to re-test on Sep 2025+ data, not as a validated rule.

### Gaps
- No post-Sep-2025 1-DTE (Monday) Nifty or 1-DTE (Wednesday) Sensex backtest found anywhere.

## Q3. Calendar / cross-index: trade the expiry-day straddle on whichever index expires today (Nifty Tue, Sensex Thu); does Sensex have similar edge?

### Takeaway
Sensex 0DTE edge exists in Zerodha's 3-year cost-inclusive test (ATM straddle 50% SL: single 9:20 entry return/MDD 0.64, six-entry basket 2.56; 20-delta strangle 9:20 return/MDD 4.0, win rates 72-78%) but equity curves "flattened since ~Sep 2025". One unverified combined Nifty+Sensex OTM4 strangle page claims ₹7.87L on 1,529 periods, 58.4% WR, MDD ₹37,476 (Jan 2023-Apr 2026) with no costs. Bank Nifty/FinNifty/Midcap expiry-day edges are historical only (weeklies gone).

### Cited Findings
- Zerodha ITM Sensex 0DTE (Jun 22 2026): ~3 years, lot normalised to 20, ₹5L/lot capital, net of ₹20/order + transaction costs + 0.25% slippage/leg; six independent entries 9:20/10:20/11:20/12:20/13:20/14:20, 50% SL per leg; straddle = ATM, strangle = 20-delta — [In The Money](https://inthemoneybyzerodha.substack.com/p/sensex-0dte-straddle-or-strangle)
- Sensex ATM straddle: avg win ₹2,510 at 9:20 falling to ₹948 at 14:20, avg loss does not shrink as much; 10:20 entry worst (return/MDD 0.65, 243-day DD duration); single 9:20 at 6x size return/MDD 0.64; six-entry basket return/MDD 2.56; 9:20-6x makes ~51% more profit but ~3x deeper MDD; basket cuts MDD 63.5% — [In The Money](https://inthemoneybyzerodha.substack.com/p/sensex-0dte-straddle-or-strangle)
- Sensex 20-delta strangle: win rate 72% (9:20), 78% (10:20), 75% (11:20); avg win ₹912/₹620/₹515… ₹236 at 14:20; 14:20 entry total 3-yr profit only ₹2,771; 9:20-6x return/MDD 4.0 vs basket 2.96; 9:20-6x MDD ~₹28,000 on ₹5L; basket gives up 59% profit for 44% less DD — [In The Money](https://inthemoneybyzerodha.substack.com/p/sensex-0dte-straddle-or-strangle)
- Same: "equity curves have flattened since about September 2025, more so for strangles"; author's rule: "Diversify across time when the edge is distributed across time… otherwise concentrate"; not viable up to five lots due to costs — [In The Money](https://inthemoneybyzerodha.substack.com/p/sensex-0dte-straddle-or-strangle)
- "9:16 Expiry Only — Combined Nifty + Sensex" (self-published page): Nifty runs Mon/Tue/Fri, Sensex Tue/Wed/Thu (both Tue); sell 1 lot OTM4 CE + OTM4 PE on current weekly at 09:16; SL 40%/leg no re-entry; target 70%/leg with one immediate re-entry; MTM stop ₹1,000 per index; exit 15:25; margin ₹4L; combined net ₹7,86,804 over 1,529 periods, 58.4% WR, MDD -₹37,476; period 03 Jan 2023-27 Apr 2026; no costs or data source disclosed — [nifty-sensex-strategy.vercel.app](https://nifty-sensex-strategy.vercel.app/) (Grade C; note the schedule contradicts the title "expiry only")
- Aliceblue/1LyAlgos "Sensex 0DTE": enter 13:00 Thursday, sell CE+PE same strike, exit 15:20 or when combined premium drops 30%, no SL; 15-month backtest WR 63.32%, ₹77,603 profit on ₹3.2L; Aug 2026 live ₹6,684 over 4 expiries; costs not stated; broker marketing — [Aliceblue](https://aliceblueonline.com/blog/sensex-0dte-strategy-1lyalgos-complete-guide-for-2026) (Grade C)
- TradingTick Nifty expiry-day straddle 2020-2024: 9:20 sell ATM (nearest 50), hold to 15:20, no SL/adjustments; 68% winning expiries; avg win/avg loss 1.4x; 14.8% annualised pre-tax; costs "assumed" but amounts not given; largest single-day loss >4x average winning day (COVID / 2022) — [TradingTick](https://tradingtick.in/nifty/option-backtesting/nifty-short-straddle-strategy-backtest-results.php) (Grade C+: costs claimed but undisclosed; implied PF ≈ 3.0 is my arithmetic)
- Historical Bank Nifty expiry-day intraday straddle 2016-2018: total ₹1,08,204 (unverified forum post) — [TradingQnA via search](https://tradingqna.com/t/guaranteed-profit-strategy/41956)
- OptionsIQ Nifty weekly conditional PE short (Feb 2019-Nov 2023): short nearest-100 ATM-100 PE only when Nifty closes above prior-day high; 84 trades, 87% WR, PF 2.1, CAGR 3.4%, MDD -4.3% (17 Aug 2022-8 Nov 2023, 420-day recovery) — [OptionsIQ PDF via search](https://optionsiq.substack.com/api/v1/file/e360eb84-5531-4c31-8c7c-30cfbd9d25ea.pdf) (Grade C; not intraday)

### Inferences
- The Sensex Thursday 0DTE straddle/strangle is the strongest B-grade candidate for adding a second "expiry day" each week to the user's already-validated Nifty expiry straddle; expected edge per Zerodha is lower since Sep 2025.
- Bank Nifty monthly expiry (last Tuesday) coincides with Nifty monthly expiry; there is no public evidence that Bank Nifty monthly-expiry-day straddles behave like old weekly expiry days.

### Gaps
- No AlgoTest/Quantman public comparison of Nifty vs Sensex vs Bankex expiry-day straddle PF/DD; AlgoTest pages are how-to only.
- No post-Sep-2025 side-by-side Nifty-Tuesday vs Sensex-Thursday straddle stats beyond Zerodha's qualitative "flattened".

## Q4. Intraday directional option strategies (ORB option buying, VWAP, 9:15 candle, trend-following straddle / exit losing leg, directional adjustment)

### Takeaway
No cost-adjusted, multi-year, positive backtest was found for any intraday index-option buying rule in India; the only numeric claim (viral RSI-50 ATM option buying, 829 trades, 52.96% WR, "₹4 lakh" over 5 years) omits costs, capital and drawdown. Practitioners quoted (IT Jegan) find buying "unprofitable if held to close". Trend-following straddle variants have no published results.

### Cited Findings
- Viral Nifty RSI-50 ATM option buying (buy ATM CE if RSI>50 / PE if <50; example SL ₹75, target ₹150 on ₹100 premium): "5 years", 829 trades, 52.96% WR, "₹4 lakh" P&L, 641 EOD exits vs 188 trailing-SL exits; no capital base, costs, or DD — [multibagg.ai](https://www.multibagg.ai/market-pulse/articles/nifty-algo-backtest-results-2026-cmrg191cpjai5np0jleu5s47x) (Grade C)
- Same article: Nifty futures "dual-confirmation" strategy Jan 2025-Jan 2026, 159 trades, 55.35% WR, PF 1.906, MDD ₹98,727 on ₹4L (≈24.7%, mis-annotated as 0.92%) — futures, not options — [multibagg.ai](https://www.multibagg.ai/market-pulse/articles/nifty-algo-backtest-results-2026-cmrg191cpjai5np0jleu5s47x)
- IT Jegan: "avoids buying strategies… unprofitable if held to the close… require momentum capture" — [AlgoTest](https://algotest.in/blog/in-conversation-with-it-jegan.md)
- Bank Nifty ORB (Amibroker, Marketcalls): range 9:15-11:15, breakout after 11:15, 150-pt target, SL opposite side, exit 15:30; futures; no stats published — [Marketcalls](https://www.marketcalls.in/?p=13736)
- Bank Nifty 2 PM day-high/low breakout (TradingQnA): self-reported ">17,000 points" 2010-2018, futures, unverified — [TradingQnA](https://tradingqna.com/t/orb-opening-range-breakout-2pm-banknifty-intraday-strategy/39756)
- AlgoTest VWAP-on-straddle-premium idea (enter when combined premium closes below VWAP, exit above) — method description only, no backtest — [AlgoTest rolling straddles](https://algotest.in/blog/how-to-backtest-rolling-straddles-with-indicators.md)
- Zerodha ITM Budget-day tests: long straddles with 20% per-leg or combined SL "consistently poor, nearly all windows negative"; long strangle 2% OTM T-5 to T-1 worked some years, inconsistent — event days only — [In The Money, Budget 2026](https://inthemoneybyzerodha.substack.com/p/budget-2026-trading-strategies-what)
- US: Vilkov "0DTE Trading Rules" (SPX, Sep 2016-Jan 2024, 30-min data, open 10:00 hold to 16:00): median returns negative for most popular strategies incl. strangles, spreads, ratio spreads; risk reversals the exception with positive mean and median; mean returns statistically insignificant for most strategies; P&L largely explained by realised skewness — [cxoadvisory summary](https://cxoadvisory.com/equity-options/0dte-strategy-outcomes); [Hull Tactical summary](https://hulltactical.com/2026/07/08/0dte-options-tiny-edge-huge-distribution/) (SSRN 4641356 itself returned 403)
- US 9:15/9:45 "candle" option buying templates (Tability, TradingView) are rule descriptions with no measured win rate — [via search](https://tability.io/templates/strategies/tags/nifty-50)

### Inferences
- Directional option buying on Indian indices has zero B-grade evidence; it should rank last among candidates unless the user's own backtester shows otherwise.
- "Trend-following straddle" (exit losing leg, ride winner) is functionally the standard per-leg-SL straddle; the Jan 2023 TradingQnA analysis says such a system's profit is concentrated in the top 10% of trades (breakout days), i.e., it already behaves like a trend follower.

### Gaps
- No Indian backtest of ATM-option ORB or VWAP option buying with option premium data was found.
- No backtest of "straddle with directional adjustment" (shift/roll losing leg) on intraday Indian data.

## Q5. Volatility-filtered selling (India VIX thresholds, small first-15-min range)

### Takeaway
A VIX-percentile entry filter improves win rate but reduces trade count and total P&L in Zerodha's 45-DTE positional test (straddle WR to ~86% above 75th percentile, no SL hits, but only ~20 trades); for intraday, a 5-year 9:20 straddle analysis says it "made money on high-VIX days" (no numbers) and an academic thesis finds India VIX explains very little of Nifty straddle performance. No first-15-min-range filter backtest was found.

### Cited Findings
- Zerodha ITM 45 DTE Nifty (Jan 2019-Jun 2026, monthly, sell ATM straddle at 15:15 45 cal-days before expiry; exit at 50% profit / 200% premium stop / 21 DTE; checked hourly; net of brokerage, STT, statutory charges): straddle ~70% WR, 4 SL hits; 30-delta strangle 12 SL hits, lower WR; 16-delta "not worth it" (~7.3 pts/trade); negative years 2019 and 2023; year WR 55% (2020) to ~90% (2025); worst trade >1,000 pts despite stop (gap) — [In The Money, Aug 2026](https://inthemoneybyzerodha.substack.com/p/we-backtested-the-famous-45-dte-strategy)
- Same: VIX filter = enter only if VIX percentile rank vs prior 252 sessions > 25/50/75; straddle WR rises with threshold, total P&L falls (fewer trades), DD barely changes below 75th pct; above 75th pct no SL hits, ~86% WR, ~20 trades (~¼ of opportunities), some years zero trades; strangle WRs approach 85% at 75th pct — [In The Money, Aug 2026](https://inthemoneybyzerodha.substack.com/p/we-backtested-the-famous-45-dte-strategy)
- TradingQnA 5-year 9:20 straddle (25% SL): "made money on high-VIX days" (image only) — [TradingQnA](https://tradingqna.com/t/detailed-analysis-of-920-short-straddle-strategy-is-it-stopped-working/130677)
- University of Vaasa MSc thesis (Lalit Kumar, 2025) on Nifty 50 delta-neutral straddles (weekly and monthly): both long and short straddles have negative Sharpe; weekly short straddles more stable than monthly; India VIX "has very small participation in the performance"; small sample — [Osuva record via search](https://osuva.uwasa.fi/handle/11111/19466) (PDF blocked by Anubis; Grade A-/B, academic but unreplicated)
- Straddle Lab "Regime" tab lets users filter by opening index level, VIX and DTE — feature, no results — [TradingQnA](https://tradingqna.com/t/straddle-lab-a-visual-way-to-explore-hundreds-of-intraday-options-selling-setups/198597)
- IT Jegan attributes 2023 straddle weakness to a low-volatility regime, not to expiry structure — [AlgoTest](https://algotest.in/blog/in-conversation-with-it-jegan.md)
- Rhoads NDX: straddle sellers' worst and best 2024 results both in 2024; April 2025 (tariff) "disastrous" for NDX 1-day straddle sellers, -1,850 pts in the month — [Nasdaq](https://www.nasdaq.com/articles/ndx-1-day-atm-straddle-mid-year-performance-update)

### Inferences
- A VIX-rank filter is a reasonable, cheap test for the user's non-expiry straddle: expect higher WR and fewer trades; whether it flips 3-4 DTE expectancy positive is untested.
- Low-VIX years (2023) were the worst for straddle selling in every Indian source; this suggests "sell only when VIX above its 1-yr median" is more plausible than "sell when VIX low".

### Gaps
- No intraday Indian backtest with first-15-min-range or opening-gap filter was published with numbers.

## Q6. Ratio spreads / broken-wing butterflies / jade lizards intraday on Nifty

### Takeaway
No intraday Indian backtest exists in public; the only "backtest" claim (Strike.money: ratio spreads 12-18% average return 2015-2023 in sideways markets) has no methodology. US 0DTE evidence (Vilkov) finds ratio spreads have negative median returns; only risk reversals were positive.

### Cited Findings
- Strike.money: "historical backtesting on Nifty options (2015-2023) shows ratio spreads delivered average returns of 12-18% during sideways markets" — no method, counts, or data — [Strike.money](https://www.strike.money/options/ratio-spread) (Grade C)
- Marketcalls jade lizard on Nifty: single worked example, net credit ₹153.6, est. 80.38% POP; not a backtest — [Marketcalls](https://www.marketcalls.in/option-strategies/understanding-jade-lizard-strategy-options-trading-strategy-tutorial.html)
- Vilkov 0DTE SPX: median returns negative for ratio spreads, strangles, bull/bear spreads; risk reversals positive mean and median — [cxoadvisory](https://cxoadvisory.com/equity-options/0dte-strategy-outcomes)
- TradingQnA Bank Nifty iron condor (StockMock, 2017-2020): condor entered at expiry start and exited expiry day: ₹4,538 after transaction costs over 3+ years; condor entered 2 days before expiry ₹27,600 over ~3.5 years; the matching short strangle >33x the condor profit with >68% WR — [TradingQnA](https://tradingqna.com/t/is-iron-condor-a-profitable-option-trading-strategy/81708) (Grade C; positional, pre-2020)
- TradingQnA user: 0.3-delta Nifty iron condors "mostly ended in red" even with adjustments; brokerage "rose considerably" — anecdote — [TradingQnA](https://tradingqna.com/t/is-short-strangle-of-deep-otm-a-good-strategy-for-regular-returns/93656/15)

### Inferences
- Wings add 4 legs of cost; every Indian source that compares condor vs strangle finds wings destroy most of the P&L — matching the user's negative iron condor/fly results.

### Gaps
- Nothing found on broken-wing butterflies or jade lizards with Indian intraday data.

## Q7. Crash-day outcomes for each strategy family (4 Jun 2024, 5 Aug 2024, 7 Apr 2025, 24 Jan 2022, Feb 2022, Mar 2020)

### Takeaway
Index and VIX moves are well documented, but no source quantifies straddle-family P&L per crash day in rupees; the closest are option-price swings on 4 Jun 2024 (21,800 PE 98 -> 996 intraday) and the Dec-2024 straddle backtest's -79 pt day. US analogues show a single 0DTE miss (9 Apr 2025, SPY +8.72% vs 3.51% implied) "gives back weeks of premium".

### Cited Findings
- 4 Jun 2024 (election result; Tuesday, non-expiry for Nifty then): Nifty -5.93% (-1,379.40 to 21,884.50), Sensex -5.74% (-4,389.73); ~₹30 lakh crore market cap lost; option prices swung up to 10x intraday; Nifty 21,800 PE low ₹98, high ₹996, close ₹515; 22,500 CE fell ~90% — [Outlook Money](https://www.outlookmoney.com/invest/india-elections-2024-investors-lose-around-rs-30-lakh-crore-markets-down-nearly-6); [Business Standard](https://www.business-standard.com/amp/markets/news/lok-sabha-election-results-trends-send-options-market-in-a-tizzy-124060401523_1.html)
- 5 Aug 2024 (Monday, non-expiry): Nifty -662.10 pts (-2.68%) to 24,055.60; India VIX +42.23% to 20.37 — [ICICI Direct](https://icicidirect.com/futures-and-options/news/nifty-august-futures-trade-at-discount/1531538)
- 7 Apr 2025 (Monday, non-expiry): Nifty close -3.24%, Sensex -2.95%; intraday low 21,743.65; India VIX intraday +59.4% to 21.9 (largest since 4 Jun 2024), close 22.79 (+65.63%) — [share.market](https://share.market/buzz/daily-digest/nifty-sensex-see-sharpest-one-day-fall-in-10-months-rbi-rate-cut-likely-and-more); [Business Standard](https://www.business-standard.com/amp/markets/news/india-s-stock-market-volatility-spikes-as-trade-war-fears-rattle-traders-125040700297_1.html)
- 24 Jan 2022: Nifty -468.05 pts (-2.65%); 24 Feb 2022: -815.30 pts (-4.78%); 23 Mar 2020: -1,135.2 pts (-12.98%), largest ever — [Stable Investor list](https://stableinvestor.com/2021/03/biggest-nifty-1-day-falls.html)
- Zerodha 45 DTE: March 2020 cycle was the straddle's best trade (entered into crash at high IV); worst trade >1,000 pts despite 200% stop due to gap — [In The Money](https://inthemoneybyzerodha.substack.com/p/we-backtested-the-famous-45-dte-strategy)
- TradingTick expiry-day straddle 2020-2024: largest single-day loss >4x the average winning day, in COVID and 2022 corrections — [TradingTick](https://tradingtick.in/nifty/option-backtesting/nifty-short-straddle-strategy-backtest-results.php)
- Quintalmind: 2020 COVID period caused 30-50%-of-capital drawdowns for many short-straddle systems (asserted) — [Quintalmind](https://www.quintalmind.com/blog/time-based-straddle-strategy-nifty-options)
- OptionsIQ Budget-day straddle (sell ATM T-1, exit Budget close): max loss -195 pts on 1 Feb 2021; WR 79%; avg loss -60 vs avg win +36 — [OptionsIQ](https://optionsiq.substack.com/p/nifty-short-straddle-performance)
- US: FlashAlpha SPY Wednesday 0DTE (193 sessions Jul 2022-Apr 2026, 10:00 ET straddle, no costs): median implied 1σ 0.72% vs median realised 0.37%; close inside implied band 71.0% vs 68.3% fair; worst miss 9 Apr 2025 implied 3.51% vs realised +8.72% (2.5x) — [FlashAlpha](https://flashalpha.com/articles/are-0dte-straddles-overpriced-193-spy-sessions-data-study)
- US: NDX 1-day straddle sellers April 2025 loss 1,850 pts — [Nasdaq](https://www.nasdaq.com/articles/ndx-1-day-atm-straddle-mid-year-performance-update)

### Inferences
- Three of the six crash days (4 Jun 2024, 5 Aug 2024, 7 Apr 2025) were non-expiry days for Nifty; an "all days" straddle takes these hits while an expiry-only rule misses them — a structural reason the user's expiry-only result beats all-days.
- With per-leg SL at 20-25%, a 3-6% index move implies the losing leg is stopped early but with large slippage (gap/spike), so realised loss per crash day is typically a multiple of a normal win; TradingQnA's "remove top 10% of trades -> negative" is the mirror image on the winning side.

### Gaps
- No source gives rupee P&L of a 9:20 straddle/strangle/condor on each of the six Indian crash dates; the user's 1-min backtester should produce this table directly.

## Q8. What public leaderboards / blogs show as best intraday option strategies 2023-2026 after costs, and what share is positive

### Takeaway
No platform publishes a true after-cost leaderboard. AlgoTest's public output is daily single-day heatmaps (useful for showing instability, not expectancy); Quantman and Stockmock blogs have no results posts; Zerodha "In The Money" is the only recurring source with disclosed costs, and it reports edge only in 0DTE (Nifty, Sensex), recently 2DTE Nifty, and positional 45DTE — nothing on 3-4 DTE intraday. Vendor "verified" claims (1LyAlgos, AlgoTradersLab) are marketing.

### Cited Findings
- Quantman blog index shows only VIX explainer, spike-protection and generic backtesting posts; no strategy results — [Quantman blog](https://quantman.in/blog)
- Stockmock: users note it lacks premium-based or %-based strike selection and IV filters; Nifty data from Feb 2019 — [TradingQnA](https://tradingqna.com/t/how-to-back-test-options-trading-strategy/80121)
- AlgoTest: all strategy pages are how-to; the "920 Straddle Defined" page uses 25% SL/leg, 9:20-15:10, weekly, no numbers — [AlgoTest](https://algotest.in/blog/the-920-straddle-strategy-defined.md); daily heatmaps Dec 2024-Jan 2025 show best entry swinging 09:16 to 12:45 and tight SLs (10-20%) usually worst — [AlgoTest heatmap search](https://algotest.in/blog/daily-straddle-heatmap---20th-december-2024.md)
- AlgoTradersLab marketing dashboard (Sensex 2024-25): net ₹1,24,580, MDD ₹18,200, strategy unspecified — [AlgoTradersLab via search](https://www.algotraderslab.com/) (Grade C)
- Zerodha ITM is the only source found with: disclosed costs (₹20/order + txn + 0.25% slippage/leg), multi-year data, DTE/entry-time breakdowns — [In The Money archive](https://inthemoneybyzerodha.substack.com/archive?sort=search&search=straddle)
- Zerodha ITM 920 straddle Monte Carlo episode (2-year 0DTE Nifty backtest reshuffled) exists but numbers not found in text — [Zerodha Aftermarket Report teaser](https://aftermarketreport.zerodha.com/p/finally-some-relief-as-nifty-ends)
- Marketcalls: "in many cases 80% of the profitable system post the transaction and slippage will not yield smooth returns" — [Marketcalls](https://www.marketcalls.in/futures-and-options/how-the-9-20-intraday-straddlers-are-being-gamed.html)
- HKUST (Carsten Chong, 0DTE 2020-2024): large risk premia exist but "transaction costs and estimation risk make the Sharpe ratios of volatility arbitrage strategies economically insignificant"; 0DTEs "expensive but not mispriced" — [HKUST](https://bm.hkust.edu.hk/bizinsight/2026/04/are-0dte-options-mispriced) (Grade A)
- Breaking NASDAQ summary of Frankfurt School 0DTE study: VRP 10:00-close "0.001 percent", "transaction costs alone swallow it" — [Breaking NASDAQ](https://breakingnasdaq.beehiiv.com/p/the-0dte-illusion) (secondary)

### Inferences
- "Percentage of listed strategies positive after costs" cannot be computed from public data; no platform exposes it. The honest summary is: across 10+ Indian sources, the only cost-inclusive positives are 0DTE straddle/strangle (Nifty, Sensex), 1DTE (pre-2024), 2DTE (2024-25 only), and positional 45DTE.

### Gaps
- No access to AlgoTest/Quantman/Stockmock internal "popular strategies" stats; Twitter/X verified-P&L threads could not be fetched.

## Q9. Candidate strategy shortlist for the other 3 days (rules executable at 1-min; evidence grade)

### Takeaway
Ten candidates below; only #1-#4 have any B-grade support, and #3-#4 only on a sub-period. #5-#10 are hypotheses that platforms let you build but nobody has published cost-adjusted results for. Recommend testing in this order on the user's backtester with Zerodha's cost model (₹20/order, exchange charges, STT 0.1% on sell premium, 0.25% slippage/leg) and reporting per-DTE.

### Cited Findings
| # | Candidate (exact rules) | Days | Evidence & grade | Mechanism claimed |
|---|---|---|---|---|
| 1 | Sensex 0DTE ATM straddle: sell ATM CE+PE at 09:20, SL 50%/leg, exit 15:20; or basket of 6 equal entries at 09:20/10:20/11:20/12:20/13:20/14:20 each with 50%/leg SL | Thursday (Sensex expiry) | B — Zerodha ITM 3-yr, costs incl.; single 9:20 return/MDD 0.64, basket 2.56, avg win ₹2,510 (9:20) -> ₹948 (14:20); flattened since Sep 2025 — [source](https://inthemoneybyzerodha.substack.com/p/sensex-0dte-straddle-or-strangle) | 0DTE theta + IV overpricing |
| 2 | Sensex 0DTE 20-delta strangle: sell 20Δ CE + 20Δ PE at 09:20, SL 50%/leg, exit 15:20, concentrate size at 9:20 (no later entries) | Thursday | B — WR 72% (9:20), return/MDD 4.0, MDD ~₹28k on ₹5L; 14:20 entry worthless (₹2,771 over 3 yrs) — [source](https://inthemoneybyzerodha.substack.com/p/sensex-0dte-straddle-or-strangle) | OTM premium decays fastest early on expiry day |
| 3 | Nifty 2-DTE straddle: Friday, sell ATM CE+PE 09:20, SL 20%/leg, exit 15:20 | Friday | B-/C — Zerodha ITM: "non-performance for five years" then positive 2024-25 ("New Contender"); numbers in images only — [source](https://inthemoneybyzerodha.substack.com/p/seven-years-of-the-920-straddle-past) | Author speculates Sensex Thu expiry resets pricing; unproven |
| 4 | Nifty 1-DTE straddle: Monday, same rules as #3 | Monday | B- — consistent 2019-2023, faded since 2024; now carries weekend gap at entry — [source](https://inthemoneybyzerodha.substack.com/p/seven-years-of-the-920-straddle-past) | Accelerating theta into expiry |
| 5 | Later-entry straddle (time-based): sell ATM at 10:30 or 12:20, SL 25-35%/leg, exit 15:15 | Any DTE | C — Marketcalls: 10:30 beat 9:20 on Bank Nifty 2023 (35% SL, 0.5% costs, charts only); Zerodha suggests 12:20 TBS as untested; AlgoTest single-day heatmaps show best time unstable — [Marketcalls](https://www.marketcalls.in/futures-and-options/is-the-920-straddle-no-more-working.html) | Avoid opening-range whipsaw; sell after morning move |
| 6 | VIX-filtered straddle: trade #3/#4/#5 only when India VIX ≥ 50th (or 75th) percentile of prior 252 sessions | Any | B for positional 45DTE (WR ~86%, ~¼ trades); C for intraday ("made money on high-VIX days", no numbers) — [Zerodha 45DTE](https://inthemoneybyzerodha.substack.com/p/we-backtested-the-famous-45-dte-strategy); [TradingQnA](https://tradingqna.com/t/detailed-analysis-of-920-short-straddle-strategy-is-it-stopped-working/130677) | Sell only when IV rich |
| 7 | Wide-SL straddle: 9:16 ATM, SL 60-100%/leg, exit 15:15 | Any | C — AlgoTest heatmaps (two single days) show SL 60-100 outperformed tight SLs on Nifty; Quintalmind asserts 50% SL WR 72-78% — [AlgoTest](https://algotest.in/blog/daily-straddle-heatmap---16th-january-2025.md) | Fewer whipsaw stop-outs; worse tail |
| 8 | OTM4 strangle with target re-entry (self-published): 09:16 sell OTM4 CE+PE weekly, SL 40%/leg no re-entry, TP 70%/leg with one re-entry, MTM stop ₹1,000/index, exit 15:25; Nifty Mon/Tue/Fri, Sensex Tue/Wed/Thu | Mon-Fri | C — ₹7.87L, 1,529 periods, 58.4% WR, MDD ₹37,476, Jan 2023-Apr 2026, no costs/data disclosed — [source](https://nifty-sensex-strategy.vercel.app/) | Far-OTM theta; "expiry only" title contradicts schedule |
| 9 | Combined-premium SL straddle: sell ATM at 09:20, exit both legs if combined premium ≥ 120-125% of entry, exit 15:20 | Any | C — Zerodha lists as untested variant; Budget-day version favoured 10:30-12:15 entries (event days only) — [Zerodha Budget](https://inthemoneybyzerodha.substack.com/p/budget-2026-trading-strategies-what) | Avoids single-leg stop-hunt |
| 10 | Afternoon expiry straddle (1LyAlgos-style): Sensex Thu, sell ATM CE+PE at 13:00, exit 15:20 or when combined premium -30%; no SL | Thursday | C — vendor 15-month backtest WR 63.32%, ₹77,603 on ₹3.2L, costs not stated — [Aliceblue](https://aliceblueonline.com/blog/sensex-0dte-strategy-1lyalgos-complete-guide-for-2026) | Last-3-hour gamma/theta; Zerodha data says late entries earn least |

- Explicitly negative/no-evidence families for non-expiry days: iron condor/fly (wings consume P&L in every Indian comparison — [TradingQnA](https://tradingqna.com/t/is-iron-condor-a-profitable-option-trading-strategy/81708)); 3-4 DTE plain straddle ([Zerodha](https://inthemoneybyzerodha.substack.com/p/seven-years-of-the-920-straddle-past)); directional option buying (no cost-adjusted evidence — [multibagg](https://www.multibagg.ai/market-pulse/articles/nifty-algo-backtest-results-2026-cmrg191cpjai5np0jleu5s47x)); 16-delta strangles ("not worth it" positionally — [Zerodha](https://inthemoneybyzerodha.substack.com/p/we-backtested-the-famous-45-dte-strategy)).

### Inferences
- Highest-value next test for the user: replicate Zerodha's exact Nifty rule set per DTE (to calibrate the backtester against a cost-inclusive external result), then add Sensex Thursday 0DTE (#1/#2). If those match, candidates #3-#7 can be screened quickly; #8-#10 are low priority.
- Expect "edge only on 0DTE" to survive; the realistic weekly schedule is Tue (Nifty 0DTE) + Thu (Sensex 0DTE), with Mon/Fri 1-2 DTE Nifty as conditional add-ons subject to VIX filter.

### Gaps
- No source provides per-trade logs for any candidate; every B-grade number above comes from charts the author describes, not downloadable data.
- No evidence at all on Bank Nifty monthly-expiry-day straddles post-Nov 2024, Bankex Thursday monthly, or Midcap/FinNifty monthly days.
