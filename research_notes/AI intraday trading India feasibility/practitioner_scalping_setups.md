# Practitioner Scalping / Quick-Intraday Setups on NSE Large Caps (5-min bars): Rules and Evidence

Scope note: ~35 searches/fetches across QuantInsti/EPAT, Zerodha (Streak, Varsity, Aftermarket Report, TradingQnA), marketcalls.in, AlgoTest, TradingView, Unofficed, SSRN/JFE/MPRA, Reddit. Headline result: **no setup below has an A- or B-grade backtest on NSE large-cap equities at 5-min with Indian costs that I could retrieve.** The only NSE-specific, cost-inclusive evidence found is *negative* (VWAP pullback on index futures, 9/21 EMA on Nifty-50 stocks). Rule specifications in "Inferences" are my own unambiguous codifications of the practitioner lore, written for the 2022-2026 backtest; they are not copied from any verified source unless stated.

Evidence grades used: **A** = peer-reviewed/replicated; **B** = platform/blog backtest with stated costs; **B-** = backtest with no costs; **C** = anecdotal / YouTube / Telegram / self-reported TradingView claims.

Cost floor the reader specified: ~0.03-0.05% round trip + slippage; targets below ~0.2% are not viable. All rules below use targets >= 0.3% or structural targets that are typically larger.

---

## Q0. Base rates: what does the evidence say about intraday/scalping viability in India at all?

### Takeaway
SEBI's FY23 cash-segment study shows ~71% of individual intraday traders lose, rising to 80% for >500 trades/yr, with costs equal to 57% of loss-makers' losses; the only NSE-specific backtests with costs that surfaced (VWAP pullback on index futures, 9/21 EMA on Nifty-50 stocks) turned negative after charges.

### Cited Findings
- SEBI study (FY 2022-23): over 70% (71%) of individual intraday equity-cash traders made losses; loss-maker share rose to 80% among traders making >500 trades/year; loss-makers' trading costs equaled 57% of their trading losses; profit-makers spent 19% of profits on costs; intraday traders at top-10 brokers rose from 1.5M (FY19) to 6.9M (FY23). — [Motilal Oswal summary of SEBI study](https://www.motilaloswal.com/learning-centre/2024/7/sebi-study-reveals-key-insights-on-individual-intraday-traders-in-india); also [Angel One](https://www.angelone.in/news/market-updates/sebi-highlights-intraday-trading-risk)
- SEBI F&O study: 9 of 10 retail F&O traders lost money in FY24; 93% of >1 crore individual F&O traders lost ~Rs 2 lakh each on average over FY22-FY24. — [Outlook Business](https://www.outlookbusiness.com/ampstories/markets/sebi-flags-90-loss-rate-in-fo-trades-by-retail-investorsheres-what-data-shows)
- Nithin Kamath called intraday equity the "abandoned baby of Indian markets" because of high STT on intraday equity. — [Business Today](https://www.businesstoday.in/amp/markets/stocks/story/abandoned-baby-of-indian-markets-zerodha-co-founder-nithin-kamath-laments-high-stt-on-intraday-equity-430041-2024-05-18)
- Streak user example: a backtest fell from ~+7.3% to ~-2.5% once "brokerage" (which Zerodha defines as all costs: STT, brokerage, stamp duty, GST, exchange and SEBI charges) was switched on. — [Zerodha Z-Connect / TradingQnA via search](https://tradingqna.com/t/zerodha-streak-brokerage-issue/46202)
- Streak user "Walker" (July 2025): 9/21 EMA crossover, 5-min, all NIFTY 50 constituents, Rs 10 lakh, 1% target / 1% stop — results "just shocking", worse with charges; Streak support replied "the overall trading charges will also be significantly higher especially when testing across 50 stocks" and suggested limiting to 1-2 trades/day; Streak states its pre-built strategies are "intended solely for educational and learning purposes". — [TradingQnA thread](https://tradingqna.com/t/algo-trading-streak-not-at-all-profitable/184440)
- Marketcalls VWAP pullback system (15-min, Nifty & Bank Nifty futures, Jan 2011-Dec 2019, "reasonable trading commissions and slippages"): "Visually strategy looks good but backtesting failed to produce impressive results"; Nifty futures profitable before costs but not after; Bank Nifty unprofitable even before costs. — [marketcalls.in](https://www.marketcalls.in/amibroker/vwap-intraday-trading-strategy-do-simple-trading-strategies-really-work-part4.html)
- AlgoTest's "45% advantage" marketing figure is explicitly gross "before brokerage, taxes, and charges" and only for positions booked through AlgoTest. — [AlgoTest blog](https://algotest.in/blog/algo-trading-edge.md); AlgoTest's own guide warns a backtest ignoring brokerage/STT/exchange charges/slippage "will always look better than real trading does". — [AlgoTest backtest guide](https://algotest.in/blog/how-to-backtest-algo-trading-strategies.md)
- Streak backtest limits: max 1 month per scrip per backtest (user report); Streak "does not consider margin while backtesting". — [TradingQnA](https://tradingqna.com/t/streak-chart-to-backtest/136821)

### Inferences
- Platform "community backtests" (Streak/AlgoTest/Tradetron) are not a usable evidence base: Streak caps lookback, AlgoTest publishes only gross aggregate marketing numbers, and no public per-strategy, after-cost summaries for equity intraday were found on any of the three.
- Any 5-min rule that trades every signal across 50 stocks will be cost-dominated; trade-count caps (1-2/day/stock) and minimum target distance are the first-order design constraints, more than entry logic.

### Gaps
- No public after-cost leaderboard for equity intraday strategies on AlgoTest, Streak, Tradetron or Quantman was found.
- Exact STT/exchange charge schedule for 2024-2026 not verified in this research; use the reader's 0.03-0.05% round-trip assumption.

---

## Q1. VWAP setups (bounce/pullback, cross with volume, ±1σ/±2σ band mean reversion)

### Takeaway
The only NSE VWAP backtest with costs found (marketcalls, 15-min pullback on Nifty/BankNifty futures 2011-2019) failed after costs; no NSE stock-level VWAP-band backtest exists publicly. VWAP is well-grounded as an institutional execution benchmark, which is the behavioural rationale, but the stock-level 5-min edge is unverified (grade C for all three variants).

### Cited Findings
- Marketcalls VWAP system rules: "When an instrument is trading above previous day closing VWAP, it is bullish and if it is trading below, it is bearish"; Buy "When instrument crosses high of Bullish 15 min candle which touched and closed above current day VWAP"; Sell mirror; target "30 Points for Nifty, 90 Points for Bank Nifty and 1.5 % stocks"; stop "20 Points for Nifty, 60 Points for Bank Nifty and 1 % stocks"; result: failed after costs on index futures. Stock results were not published. — [marketcalls.in](https://www.marketcalls.in/amibroker/vwap-intraday-trading-strategy-do-simple-trading-strategies-really-work-part4.html)
- TrendSpider (US data) tested VWAP-based strategies across timeframes and reported "the win rate is abysmal in every test", with a 15-min long-bias version performing best. — [TrendSpider blog](https://trendspider.com/blog/daytrading-with-the-vwap-indicator/)
- Streak forum: users asking about VWAP entries got no published results; Streak explained indicators need closed candles since historical data is OHLC only. — [TradingQnA](https://tradingqna.com/t/atp-and-vwap-on-streak-strategy/54569)
- Quantified Strategies' VWAP backtest page could not be fetched (bot wall). — [quantifiedstrategies.com](https://www.quantifiedstrategies.com/vwap-trading-strategy/)

### Inferences (exact rules to backtest)
**S1. VWAP pullback-continuation (trend day)** — grade C (adapted from marketcalls rules to 5-min)
- Universe: Nifty 50 constituents. Session VWAP = cumsum(typical_price*vol)/cumsum(vol) reset at 09:15.
- Regime filter: at bar close t (t >= 10:00), close_t > VWAP and the day's open > previous day's close (gap-up/trend bias) for longs; mirror for shorts.
- Setup bar: a 5-min bar whose low <= VWAP and close > VWAP (touch-and-reject), with close > open.
- Entry: buy stop at setup-bar high + 1 tick, valid for the next 3 bars only; cancel if not filled.
- Stop: setup-bar low - 1 tick, or 0.5% from entry, whichever is nearer.
- Target: 1.5x stop distance (minimum 0.4% from entry; skip trade if 1.5x stop < 0.4%).
- Time window: entries 10:00-14:00; hard exit at 15:10. Max 1 trade per stock per direction per day.
- Why it supposedly works: institutional VWAP-execution algos defend VWAP on trend days; retail stops cluster just beyond it.
- Known failure: range/chop days (price criss-crosses VWAP), expiry days, news gaps >2%.

**S2. VWAP ±2σ band mean reversion** — grade C
- Bands: sigma_t = sqrt(cumsum(vol*(tp - VWAP)^2)/cumsum(vol)) computed intraday from 09:15; upper2 = VWAP + 2*sigma_t, lower2 = VWAP - 2*sigma_t. Require at least 12 bars (10:15) before signals.
- Entry long: bar closes below lower2, next bar closes back above lower2 -> buy at that bar's close. Short mirror at upper2.
- Filter: skip if |open - prev_close| > 1.5% (gap days behave as trend days); skip if the 20-bar ATR(5-min) > 2x its 20-day median (event volatility).
- Stop: 1.0% from entry or below the extreme low of the two signal bars, whichever is nearer.
- Target: VWAP (exit at first bar whose high >= VWAP for longs). Skip trade if VWAP - entry < 0.3%.
- Time: signals 10:15-14:30; hard exit 15:10. Max 2 trades/stock/day.
- Why: 2σ excursions on liquid large caps are usually liquidity-driven, and VWAP algos' remaining order flow pulls price back.
- Failure: trend days; stocks with news; bands too tight early in session (hence 10:15 start).

**S3. VWAP cross with volume** — grade C; included as negative control. Entry: first 5-min close above VWAP after >= 3 closes below, with bar volume > 2x 20-bar average; stop below signal-bar low; target 2x stop; max 1/day. Expect cost-dominated results (frequent whipsaws).

### Gaps
- No NSE stock-level, cost-inclusive VWAP backtest (pullback or bands) was found anywhere public. The reader's backtest will be the first datapoint.
- Marketcalls' numeric table was an image and could not be read.

---

## Q2. EMA scalps (9/20 crossover, 20-EMA pullback, EMA ribbon)

### Takeaway
The one NSE-specific test found (Streak, 9/21 EMA crossover, 5-min, all Nifty-50 stocks, 1%/1%) lost money after charges per the user; no positive after-cost evidence for any EMA scalp on NSE 5-min exists publicly. Grade C (and the available evidence points negative).

### Cited Findings
- Streak user 9/21 EMA 5-min across Nifty-50 with 1% target/1% stop: results "shocking", worse with charges; Streak blamed trade count across 50 stocks and suggested the "Daily strategy cycle" limit of 1-2 trades/day. — [TradingQnA](https://tradingqna.com/t/algo-trading-streak-not-at-all-profitable/184440)
- AlgoTest tutorial 20/50 EMA crossover on 5-min; no performance figures. — [AlgoTest](https://algotest.in/blog/automate-ema-indicator-without-coding.md)
- QuantInsti EPAT "Automation using trend-following indicators" automates an intraday 200 SMA / 50 EMA strategy; no results in snippet. — [QuantInsti](https://blog.quantinsti.com/automation-trend-following-indicators-project-rajesh)
- TradingView 9/21 EMA scripts have built-in stat tables but state no results in descriptions. — [TradingView search](https://www.tradingview.com/scripts/search/profit%20factor/page-5)

### Inferences (exact rules)
**S4. 20-EMA pullback in established trend (not crossover)** — grade C
- Trend filter: EMA(20) > EMA(50) on 5-min AND close > session VWAP AND EMA(20) slope positive (EMA20_t > EMA20_{t-6}).
- Setup: bar low touches or penetrates EMA(20) (low <= EMA20) and bar closes above EMA20. At least 6 bars since last signal.
- Entry: buy stop at setup-bar high + 1 tick, valid 2 bars.
- Stop: min(setup-bar low - 1 tick, entry - 0.6%).
- Target: 2x stop (skip if < 0.4%). Alternative exit: close below EMA(20) by > 0.1%.
- Time: 10:00-14:30 entries; exit 15:10; max 2/day/stock.
- Why: trend-day order flow (momentum algos, delta-hedging) refills at a short moving average that most retail charts show.
- Failure: first hour (EMA not yet meaningful), lunch chop 12:00-13:30, mean-reverting days.

**S5. 9/20 EMA crossover** — negative control (grade C, evidence negative). Long when EMA9 crosses above EMA20 and close > VWAP; stop 0.5%; target 1%; max 1/day. Expected to be cost-dominated; include so the reader can quantify how bad.

### Gaps
- Walker's actual numbers (before/after charges) were images; exact P&L not retrievable.

---

## Q3. PDH/PDL break & retest; first-5-min candle breakout; 15-min ORB with retest

### Takeaway
ORB is the most-discussed intraday setup in India (Zerodha's "In The Money" tested a time-based ORB on NIFTY; QuantInsti EPAT project built first-candle breakout rules on Nifty-50 stocks) but no retrieved source reports win rate / PF after costs for stocks; TradingView self-reports (60-70% win) are unverifiable (grade C; ORB on US futures/ETFs has B-grade support, which does not transfer).

### Cited Findings
- QuantInsti EPAT (Raj TK, Jan 2020): first 5-min candle patterns on Nifty-50 stocks (5/15/30-min data); ten patterns (gap up/down green/red with body >= 0.5 and open >= 2 pts beyond prior high/low; gap-reversal needing close beyond Bollinger band; engulfing; long-shadow with shadow >= 2x body). Entry: "close of a subsequent candle completely outside of the initial opening candle". Stop: first-candle low/high (engulfing: +3 pts). Trailing: after 1-pt move, stop to +1 pt beyond entry; trail each 1 pt. Take-profit (gap family): SMA_t - SMA_{t-1} > 0.2. Max 2 trades/day (1 for engulfing). Only reported stat: "Average 4-5 trades per month per script"; win rate/returns were in images; each stock "needs its own backtest before it is selected". — [QuantInsti](https://blog.quantinsti.com/intraday-low-frequency-trading-strategy-project-rajtk/)
- Zerodha "In The Money" episode: "testing a time-based ORB on NIFTY across multiple windows" comparing equity curves, drawdowns, win rates, long/short behaviour; numbers only in the video, not retrievable. — [Zerodha Aftermarket Report](https://aftermarketreport.zerodha.com/p/nifty-stalls-near-25500-after-volatile)
- Marketcalls 15-min ORB: range = first 15 min (or 20-30 min if clearer); long on break of range high after gap-up open, short mirror; "Sell the stock after 2 hours"; no stop/target numbers; no backtest. — [marketcalls.in](https://www.marketcalls.in/nifty-technicals/15-minute-opening-range-breakout.html)
- Marketcalls Bank Nifty ORB AFL: 09:15-11:15 range, 150-pt target; code only. — [marketcalls.in](https://www.marketcalls.in/amibroker/backtestable-open-range-breakout-orb-study-for-amibroker.html)
- Onetradejournal ORB guide: "No verified Indian-market win rate or return is supplied here"; defines 15-min range as 09:15 up to but not including 09:30, entry variants = touch / close beyond / retest. — [onetradejournal.com](https://onetradejournal.com/strategies/opening-range-breakout)
- TradingView first-candle breakout script for Nifty 50 claims "60%-70% win rate" with no methodology or period. — [TradingView](https://br.tradingview.com/scripts/indian)
- TradingView "Pivot Strategy [Indian Market Timing]" (5-min, NIFTY): search snippet reported ~60% win rate, PF 1.45, ~Rs 21,500 net over 6 months, 128 trades, commission included (rate unstated); the script page itself shows no numbers. — [TradingView](https://tr.tradingview.com/scripts/indianmarkets/)
- TradingView S/R breakout on NSE:TCS 5-min: snippet reported ~60% profitability, PF 1.8, ~Rs 30,000 over 6 months, 100 trades, closes all at 3pm. Self-reported, not verifiable. — [TradingView search](https://tr.tradingview.com/scripts/indianmarkets/)
- Edgeful: 5-min ORB on ES futures "108% return in 6 months" (US, not transferable). — [edgeful.com](https://www.edgeful.com/blog/posts/5-minute-opening-range-breakout-es-strategy)

### Inferences (exact rules)
**S6. 15-min ORB with retest entry** — grade C (most-tested in India, but numbers not public)
- OR = high/low of 09:15-09:29 bars (three 5-min bars). Require OR range between 0.3% and 1.5% of open (skip otherwise).
- Breakout: first 5-min close > OR_high (long) after 09:30.
- Retest: within the next 6 bars, a bar whose low <= OR_high + 0.05% and close > OR_high. Entry = that bar's close. If no retest within 6 bars, no trade (compare separately with direct-breakout variant: entry at breakout close).
- Stop: OR midpoint (OR_low + 0.5*OR range), capped at 0.8% from entry (skip trade if midpoint is > 0.8% away).
- Target: 1x OR range above OR_high (min 0.4%); hard exit 15:10. Max 1 trade/stock/day; first signal only.
- Volume confirmation variant: breakout bar volume > 1.5x average of the three OR bars.
- Why: overnight order imbalance resolves in first 15 min; retest filters the failed-breakout stop-run.
- Failure: inside-range days (no follow-through), RBI/Fed/budget days, OR too wide on gap days.

**S7. First 5-min candle breakout** — grade C
- Candle = 09:15-09:19 bar. Require body >= 40% of range and range between 0.25% and 1.2% of open.
- Entry: first subsequent 5-min close fully above candle high (long) / below low (short), by 09:45 at the latest.
- Stop: opposite extreme of first candle, capped at 0.7%.
- Target: 1.5x stop (min 0.4%) OR trail: exit on close below EMA(9). Hard exit 11:30 (QuantInsti variant exits via SMA-slope rule).
- Max 1 trade/day/stock.

**S8. PDH/PDL break-and-retest** — grade C (no backtest found at all)
- Levels: previous session high (PDH) / low (PDL) from daily bar.
- Break: 5-min close > PDH by >= 0.1% between 09:30 and 14:00, with bar volume > 1.5x 20-bar average.
- Retest: within next 8 bars, a bar with low <= PDH + 0.05% and close > PDH. Entry at that bar's close.
- Stop: retest-bar low - 1 tick, capped at 0.6% from entry.
- Target: 2x stop (min 0.5%). Hard exit 15:10. One trade per level per day.
- Why: stop orders of yesterday's shorts rest above PDH; breakout traders chase; retest = absorption.
- Failure: PDH too close to open (<0.3%): gap-through days; wide-range prior days.

### Gaps
- Zerodha In The Money ORB numbers (window comparison, win rates, DD) are video-only; not retrieved.
- QuantInsti Raj TK trade statistics were images; not retrieved.
- No PDH/PDL retest backtest on NSE found.

---

## Q4. Narrow-range / squeeze: NR7, inside bar, Bollinger bandwidth squeeze

### Takeaway
Unofficed's NR7+inside-bar backtest on F&O stocks (2015-present, no costs) shows positive net points but a derived win rate of only ~24-31% (payoff-driven), and same-day exit is the weakest of three horizons; BB squeeze has no NSE evidence and a US self-test shows ~50% directional accuracy. Grade B- for NR7+IB (no costs), C for BB squeeze.

### Cited Findings
- Unofficed NR7+IB (all F&O stocks exhibiting the pattern since 2015; 2238-2239 buy and sell trades each): same-day exit net buy points 278,051.6 vs sell 1,057,877.7; positive buy 546 / negative 611 (win rate ~24.4%); positive sell 642 / negative 484 (as published; 642/2238 = ~28.7% win rate); 2-day exit: buy 626,660.7, sell 226,256.9; 5-day: buy 1,087,522.4, sell 412,298.9. Avg winning buy (same-day) 5,465 points vs avg losing buy -4,428 points. No currency/position sizing/costs stated. — [Unofficed](https://unofficed.com/?p=22881)
- Unofficed index inside-bar backtest: "generated a positive net profit, but the average profits per trade were relatively lower than its positional variant". — [Unofficed](https://unofficed.com/lessons/backtesting-index-inside-bar-positional-strategy-using-python/)
- Crabel: very narrow days tend to be followed by wide days (NR7 rationale); traders place buy stop above high / sell stop below low. — [MarketInOut NR7 screener (India)](https://www.marketinout.com/stock-screener/nr7-inside-day/india)
- Reddit self-test: 399 BB squeeze events on 50 S&P 500 stocks 2023-2026: 49.6% direction accuracy unfiltered; 71.4% with author's grading (unverified). — [Reddit snapshot](https://reddit.sentinel-team.org/posts/1rdji47/snapshots/2026-02-27T22%3A12%3A05.0165Z)
- Quantified Strategies weekly-bar BB squeeze: "doesn't do particularly well for any asset". — [quantifiedstrategies.substack.com](https://quantifiedstrategies.substack.com/p/bollinger-band-squeeze-strategy-backtest-4a6)
- TradingQnA on BB squeeze in Pi: anecdotal view it is "best suited for commodities". — [TradingQnA](https://tradingqna.com/t/bollinger-bands-squeeze-strategy-conversion-to-tradescript-for-backtesting-in-pi/48939)

### Inferences (exact rules)
**S9. NR7 / inside-day breakout traded on 5-min** — grade B- (daily pattern has NSE evidence without costs)
- Daily filter (computed from daily bars, previous session): yesterday's range = min of last 7 daily ranges (NR7) AND yesterday's high < day-before high and low > day-before low (inside day). Either condition alone = looser variant to test separately.
- Entry: first 5-min close above yesterday's high (long) / below yesterday's low (short) between 09:20 and 13:00. Buy at that close.
- Stop: yesterday's low (long), capped at 0.8%; if > 0.8%, use 0.8%.
- Target: 1.5x yesterday's range projected from breakout level (min 0.5%); hard exit 15:10.
- One trade per day per stock; if stopped, allow one reverse trade on opposite break.
- Why: volatility contraction -> expansion; stops clustered just outside the narrow range.
- Failure: Unofficed data says same-day exit is weakest; expect low win rate (~25-30%) and payoff dependence; costs/slippage on stop-outs not modelled anywhere.

**S10. BB squeeze (bandwidth percentile) breakout on 5-min** — grade C
- BB(20,2) on 5-min; bandwidth = (upper-lower)/middle. Squeeze = bandwidth <= 10th percentile of its trailing 500-bar distribution, for >= 6 consecutive bars.
- Entry: first close outside the bands after the squeeze, with bar volume > 2x 20-bar average, 10:00-14:00.
- Stop: BB middle (SMA20) at entry, capped 0.6%.
- Target: 2x stop (min 0.4%) or close back inside bands after 3 bars. Hard exit 15:10. Max 1/day/stock.
- Known: US evidence ~coin-flip direction; the edge, if any, is payoff asymmetry, not hit rate.

### Gaps
- Unofficed does not model costs or slippage, nor give per-trade % returns; "points" P&L cannot be converted to % without position-size assumptions.
- No NSE BB-squeeze backtest found.

---

## Q5. Momentum ignition: volume spike + range expansion; "stocks in play" by relative volume

### Takeaway
No NSE backtest of volume-spike continuation or RVOL-based stock selection was found; only screener definitions (e.g., MarketInOut: >3% move on >= 2x 21-day volume, ATR > 3% of price). Grade C.

### Cited Findings
- MarketInOut India "Stocks in Play" screen: up or down > 3% today on at least 2x 21-day average volume, ATR > 3% of price, average daily traded value >= Rs 50M. Screener, not a backtest. — [MarketInOut](https://www.marketinout.com/stock-screener/stocks-in-play/india?view=charts)
- Popular RVOL script: intraday-only; compares current cumulative volume against a 20-period average with 3-14 day lookback (default 4); other sources confirm breakouts on >1.5-2x average volume. — [TradingView RVOL](https://www.tradingview.com/script/tJRw7QVP-RVOL-R4Rocket)
- NSE publishes security-wise volume and bhavcopy delivery data daily; intraday RVOL needs minute data from a vendor. — [share.market](https://www.share.market/buzz/learn/volume-indicator-in-trading/)

### Inferences (exact rules)
**S11. Volume-spike + range-expansion continuation** — grade C
- Selection at 09:30: RVOL = cumulative volume 09:15-09:29 / median of the same 15-min window over the prior 20 sessions. Trade only the top 5 Nifty-50 stocks by RVOL with RVOL >= 2.0.
- Ignition bar (any time 09:30-14:00): bar range >= 2x ATR(20 bars) AND bar volume >= 3x 20-bar average AND close in top 25% of bar range (long) / bottom 25% (short).
- Entry: next bar open (continuation), or buy stop at ignition-bar high + 1 tick valid 2 bars (compare both).
- Stop: ignition-bar midpoint, capped 0.7%.
- Target: 1.5x stop (min 0.4%) or trail on EMA(9) close; hard exit 15:10. Max 1/day/stock.
- Why: institutional participation (algos splitting large orders) persists after the first visible print; RVOL identifies where institutions are active.
- Failure: ignition on news (circuit-limit risk, reversals), block/bulk deal prints, index rebalancing days.

### Gaps
- No Indian RVOL or volume-spike backtest with any numbers found; closest US work (Ross Cameron style "stocks in play") is anecdotal and not searched here.

---

## Q6. Mean reversion scalps: RSI(2)/RSI(3) on 5-min; 3-bar reversal; first-15-min spike fade to VWAP; gap-fill fade >1%

### Takeaway
RSI(2) was designed for daily bars; a ProRealCode commenter found 1-min/15-min results poor and the author said it "wasn't designed for day trading". Gap-fill odds for Nifty are circulated as unverified commentary (65-75% for 0.3-0.6% gaps, 25-40% for >1.2%); the only EPAT gap project is a daily overnight long strategy without costs. Grade C for all; gap-fade numbers are explicitly unverifiable.

### Cited Findings
- Connors RSI-2 (ProRealCode, daily CAC40): commenter reported 1-min and 15-min results poor; author replied the system wasn't designed for day trading. — [ProRealCode](https://www.prorealcode.com/prorealtime-trading-strategies/rsi-2-strategy-larry-connors/?pnum=1)
- Nifty-50 RSI study (journal, index-level, not 5-min): 50-50 variant better long-term, 60-40 better short-term. — [JMRA](https://doi.org:/10.18231/j.jmra.2021.033)
- Gap-fill commentary (Nifty index, no methodology): 0.3-0.6% gaps fill same day ~65-75%; 0.6-1.2% ~45-60%; >1.2% ~25-40%. — [multibagg.ai](https://www.multibagg.ai/market-pulse/articles/nifty-gap-fill-trade-key-levels-cmv1aez0x000x39qp99w1zvrr) (unverified)
- Onetradejournal gap-fill page: "No verified Nifty or Bank Nifty fill-rate dataset is provided here, so there is no claimed win rate"; warns "fills aren't profits" (a gap can fill after a stop-out) and daily OHLC cannot order stop vs target. — [onetradejournal.com](https://onetradejournal.com/strategies/gap-fill-strategy)
- QuantInsti EPAT Markov gap strategy: long-only, daily, buy at close / sell at next open if today's true range > yesterday's, close > open, |return| < 2%, Nifty ATR/close <= 3%; 10 stocks (Reliance, SBI, LT, M&M, Bharti, Coal India, Colpal, Trent, Zydus, Solaris) 2014-2024; portfolio CAGR ~24.9%, max DD ~2.4%, "theoretical" Sharpe >5; **"The transaction costs are not included"** and "could be pretty high". Not a gap fade. — [QuantInsti](https://blog.quantinsti.com/epat-project-gap-trading-strategy-based-on-the-markov-rule/)
- E-mini study: probability of gap fill decreases with gap size (US). — via [search summary](https://catalogimages.wiley.com/images/db/pdf/0471484857.c01.pdf)

### Inferences (exact rules)
**S12. RSI(2) extreme with VWAP filter** — grade C (expect weak)
- RSI(2) on 5-min closes. Long: RSI2 < 10 AND close > session VWAP AND close > EMA(50, 5-min) (buy dips in uptrend only). Short mirror (RSI2 > 90, close < VWAP, < EMA50).
- Entry at signal-bar close, 10:00-14:30.
- Exit: RSI2 > 60 (long) or 6 bars elapsed, whichever first; stop 0.6%. Skip if expected move (VWAP distance) < 0.3%.
- Max 2/day/stock.

**S13. First-15-min spike fade to VWAP** — grade C
- At 09:30: if close_09:30 is >= 1.0% above session VWAP (or above open by >= 1.0% with the 3-bar range > 1.2%), short at 09:30 close; mirror for long.
- Filter: skip if |gap| (open vs prev close) > 2% or stock has results/news (not codable: use |gap| > 2% proxy).
- Stop: 09:15-09:29 high + 0.1% (capped 0.8%). Target: VWAP touch; hard exit 11:00. 1/day.
- Why: opening auction imbalance over-shoots; VWAP algos lean the other way after 09:30.
- Failure: genuine news days -> trend continuation; this is the costliest failure mode (fat left tail).

**S14. Gap-fill fade for gaps > 1%** — grade C (fill-rate claims unverified)
- Gap = (open - prev_close)/prev_close; trade only 1.0% <= |gap| <= 2.5%.
- Entry (gap-up fade): wait for 09:15-09:29; short at 09:30 open only if close_09:29 < open_09:15 (first 15 min already reversing). Mirror for gap-down.
- Stop: day high so far + 0.1% (capped 1.0%). Target: 50% gap fill (first), full fill = prev_close (second half). Hard exit 12:00. 1/day.
- Known: large gaps fill least often (all sources); expect ~40-50% hit at best; payoff must carry it.

**S15. 3-bar reversal** — grade C, not found in any Indian source; define as 3 consecutive lower closes with each bar's volume rising, then a bar closing above the prior bar's high -> long; stop below the 3-bar low (cap 0.6%); target 1.5x; 10:00-14:30. Include only as a comparison.

### Gaps
- No NSE stock-level gap-fill frequency table with methodology exists publicly; the multibagg numbers have no source.
- No RSI(2) 5-min test on NSE found.

---

## Q7. Time-based: last-hour momentum (14:30-15:15), avoid first 15 min, lunch-hour chop avoidance

### Takeaway
The only A-grade effect in this whole catalogue is intraday time-series momentum (first half-hour return predicts last half-hour return; Gao/Han/Li/Zhou JFE 2018, extended internationally), but it is tested on index ETFs, not NSE stocks; for NSE, peer-reviewed work confirms the U-shaped volatility profile on Nifty futures (1-min, 2011-2018) and an "open jump effect" and "end-of-session effect" on Nifty 50, which supports the avoid-first-15-min / trade-last-hour heuristics qualitatively but not quantitatively.

### Cited Findings
- Gao, Han, Li, Zhou (JFE 2018), SPY 1993-2013: first half-hour return (from prior close) predicts last half-hour return; stronger on volatile, high-volume, recession and macro-news days; also present in 10 other ETFs. — [Alpha Architect summary](https://alphaarchitect.com/2014/08/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/); [WashU publication record](https://profiles.wustl.edu/en/publications/market-intraday-momentum/)
- International extension: intraday time-series momentum "economically and statistically significant in international stock markets"; US first half-hour predicts international last half-hours. — [Reading eprints](https://reading-9.eprints-hosting.org/95566/1/Accepted-Version.pdf)
- Singh & Gangwar (2018, MPRA 89689), Nifty futures 1-min, Jan 2011-Aug 2018: intraday volatility U-shaped (high near open and close); hourly volatility declined over the period; no numeric table on abstract page. — [MPRA](https://mpra.ub.uni-muenchen.de/89689/)
- Nifty 50 intraday returns study (Asian Journal of Management, i-scholar): significant "open jump effect" and persistent "end-of-session effect"; first 20 minutes significant on all weekdays; results differ pre/post rolling settlement. Full text not retrievable (DNS failure). — [i-scholar](https://i-scholar.in/index.php/Ajm/article/view/179374)
- Practitioner blogs describe 14:30-15:30 as when activity picks up for square-offs; no return evidence. — [swastika.co.in](https://www.swastika.co.in/blog/intraday-trading-time-analysis)
- ETF study (non-Indian): first-15-min average returns highest, converging to ~0 later in session. — [CUD repository](https://repository.cud.ac.ae/items/8f5324a0-d40e-499b-9d93-75b4064b40d7)

### Inferences (exact rules)
**S16. Last-hour intraday momentum (Gao-style, applied per stock and via Nifty)** — grade A for the effect on indices (US/international), C for NSE large-cap stocks
- Signals at 14:30: r_first = close_09:45 / prev_close - 1 (first 30 min incl. overnight); r_sofar = close_14:30 / prev_close - 1.
- Long if r_first > +0.3% AND r_sofar > 0 AND close_14:30 > VWAP; short mirror. Use the stock's own returns (variant A) and Nifty-index returns applied to all stocks (variant B, closer to the paper).
- Entry: 14:30 close. Exit: 15:15 close (avoid closing-auction volatility), stop 0.5%.
- Expected per-trade magnitude is small (last-half-hour index moves are typically well under 0.5%), so this will be cost-sensitive at stock level; the paper's edge is a regression coefficient, not a scalping P&L.
- Why: late-day rebalancing by institutions/ETFs and delta-hedgers chasing the day's direction; retail intraday square-off at ~15:15-15:20 (broker auto square-off) amplifies.

**Time filters to apply across S1-S15 (quantified evidence only for volatility, not P&L):**
- No new entries 09:15-09:29 (open jump / U-shape volatility: slippage highest).
- Optional lunch filter: no entries 12:00-13:30; test with/without. No NSE evidence either way beyond the volatility trough.
- Hard exit 15:10 for everything (before broker auto square-off and closing auction).

### Gaps
- No NSE replication of Gao et al. on Nifty futures or Nifty-50 stocks found (searched SSRN keywords; nothing surfaced).
- Lunch-hour return/chop evidence for NSE: none quantitative; only volatility U-shape.

---

## Q8. Pair / relative scalps on same-sector large caps (HDFCBANK/ICICIBANK, TCS/INFY) intraday

### Takeaway
Only daily-frequency Indian evidence exists: a 2025 EPAT walk-forward cointegration study on 25 NSE large caps (5 bps/leg/side) produced Sharpe 0.089 and -34% max DD and did not select HDFCBANK/ICICIBANK; no intraday spread backtest was found, so intraday feasibility is unproven (grade B for daily, none for intraday).

### Cited Findings
- EPAT cointegrated pairs (2015-2025, walk-forward, 252-day train / 21-day test, |z| > 1.5 entry, exit at z=0, 30-day rolling z, 5 bps per leg per side): pairs chosen HDFCBANK/KOTAKBANK, HEROMOTOCO/ULTRACEMCO, HCLTECH/ICICIBANK; 271 trades, win ratio 63.47%, PnL/capital 11.04% total, annualized return 0.30%, ann. vol 13.34%, Sharpe 0.089, max DD -34.31%. — [QuantInsti](https://blog.quantinsti.com/cointegrated-pairs-trading-indian-equity-market-epat-project/)
- Earlier EPAT sector pairs project (Vivek Jain) used ADF at >= 90% significance; daily. — [QuantInsti](https://blog.quantinsti.com/epat-project-mean-reversion-statistical-arbitrage-pair-trading-strategy-indian-market-sectors/)
- Onetradejournal HDFC/ICICI worked ratio example (1.42 -> 1.50) is explicitly illustrative; notes relationship breaks (merger, fraud, RBI action) make both legs lose. — [onetradejournal.com](https://onetradejournal.com/glossary/pairs-trading)
- A paper on HDFCBANK/ICICIBANK applies 0.10% cost per signal change; results not in snippet. — [IJIRT](https://ijirt.org/publishedpaper/IJIRT205972_PAPER.pdf)
- Kite forum spread script works on daily closes only. — [kite.trade forum](https://kite.trade/forum/uploads/editor/c3/tzi4cx1tqob8.txt)

### Inferences (exact rules)
**S17. Intraday spread reversion HDFCBANK/ICICIBANK, TCS/INFY** — grade C (feasibility only)
- Spread s_t = log(P_A,t) - beta*log(P_B,t), beta = OLS over prior 20 sessions' 5-min closes; z_t = (s_t - mean_60bars)/std_60bars computed intraday (rolling 60 bars, 5 hours).
- Entry at |z| >= 2.0 (short the rich leg, long the cheap leg, rupee-neutral), 10:00-14:00; exit at z crosses 0 or at 15:10; stop at |z| >= 3.5.
- Cost: two legs -> round-trip cost doubles (~0.06-0.10% + 2x slippage); require expected spread move at entry (2σ of spread in %) >= 0.5%, else skip.
- Feasibility verdict: with daily Sharpe ~0.09 at 5 bps/leg, intraday at ~2x the cost burden and smaller moves is unlikely to clear costs on these mega-cap pairs; the reader should treat this as a null-result check, not a candidate.

### Gaps
- No intraday (1-5 min) HDFCBANK-ICICIBANK or TCS-INFY backtest with Sharpe/DD exists publicly.

---

## Q9. What do Indian algo platforms (AlgoTest, Streak, Tradetron, Quantman) show as most-backtested / best-performing for equity intraday?

### Takeaway
Nothing usable: AlgoTest publishes only a gross marketing aggregate; Streak caps backtests at ~1 month/scrip and labels pre-built strategies "educational"; Tradetron hits were freelancer gigs; Quantman had no public results; the platforms' public equity-intraday discourse is dominated by ORB/EMA-crossover/VWAP templates, and the only after-cost anecdotes are losses.

### Cited Findings
- AlgoTest "45% advantage": gross, before brokerage/taxes/charges, positions booked through AlgoTest only. — [AlgoTest](https://algotest.in/blog/algo-trading-edge.md)
- AlgoTest tutorial templates: 20/50 EMA crossover on 5-min; no results. — [AlgoTest](https://algotest.in/blog/automate-ema-indicator-without-coding.md)
- Streak: pre-built strategies "intended solely for educational and learning purposes"; 1 month/scrip limit; costs defined as all statutory charges; margin not modelled. — [TradingQnA 184440](https://tradingqna.com/t/algo-trading-streak-not-at-all-profitable/184440); [TradingQnA 136821](https://tradingqna.com/t/streak-chart-to-backtest/136821); [TradingQnA 46202](https://tradingqna.com/t/zerodha-streak-brokerage-issue/46202)
- Tradetron: only freelancer requests to build/backtest intraday stock strategies; no published results. — [freelancer.de](https://www.freelancer.de/projects/risk-management/intraday-stocks-strategy-tradetron)

### Inferences
- The platform ecosystem's revealed preference is for index-options strategies (straddles etc.), not equity scalps; equity intraday templates exist for onboarding, not because they test well.

### Gaps
- Quantman: no search hits with results. No platform leaderboard for equity intraday found.

---

## Q10. Honest assessment: which setups have evidence of positive expectancy net of Indian costs on liquid large caps, and which are lore?

### Takeaway
None of the 17 rule-sets above has public, after-cost, NSE-stock-level evidence of positive expectancy at 5-min; the best-supported *effects* are (1) intraday time-series momentum (A, index ETFs, non-India), (2) NR7/inside-day expansion (B-, NSE F&O stocks, no costs, ~25-30% win rate), (3) opening-range breakout (widely tested on US futures; India tests exist but numbers not public). Everything VWAP/EMA/RSI/gap/pair at 5-min on NSE is lore (C), with the two NSE cost-inclusive datapoints found being negative.

### Cited Findings (summary table of evidence)
| # | Setup | Best evidence | Grade | Direction of evidence |
|---|---|---|---|---|
| S1 | VWAP pullback-continuation | [marketcalls 2011-2019 idx futures, with costs](https://www.marketcalls.in/amibroker/vwap-intraday-trading-strategy-do-simple-trading-strategies-really-work-part4.html) | B (negative) | Failed after costs |
| S2 | VWAP ±2σ bands MR | none on NSE; [TrendSpider US "abysmal"](https://trendspider.com/blog/daytrading-with-the-vwap-indicator/) | C | Unknown/negative |
| S3 | VWAP cross + volume | none | C | Unknown |
| S4 | 20-EMA pullback | none | C | Unknown |
| S5 | 9/20 EMA cross | [Streak user, Nifty-50, 5-min, with charges](https://tradingqna.com/t/algo-trading-streak-not-at-all-profitable/184440) | B (negative) | Lost after charges |
| S6 | 15-min ORB + retest | [Zerodha ITM video (no numbers)](https://aftermarketreport.zerodha.com/p/nifty-stalls-near-25500-after-volatile); [QuantInsti EPAT (no numbers)](https://blog.quantinsti.com/intraday-low-frequency-trading-strategy-project-rajtk/) | C (India) / B (US futures) | Unknown for NSE stocks |
| S7 | First 5-min candle break | TradingView "60-70%" claim | C | Unverified |
| S8 | PDH/PDL break-retest | none | C | Unknown |
| S9 | NR7 + inside day | [Unofficed, F&O stocks 2015-, no costs](https://unofficed.com/?p=22881) | B- | Positive gross, ~25-30% WR |
| S10 | BB squeeze | [Reddit US 49.6%](https://reddit.sentinel-team.org/posts/1rdji47/snapshots/2026-02-27T22%3A12%3A05.0165Z) | C | Coin-flip direction |
| S11 | Volume spike / RVOL | screeners only | C | Unknown |
| S12 | RSI(2) 5-min | [ProRealCode comments](https://www.prorealcode.com/prorealtime-trading-strategies/rsi-2-strategy-larry-connors/?pnum=1) | C | Poor intraday (non-India) |
| S13 | First-15-min spike fade | none | C | Unknown |
| S14 | Gap fade >1% | [unsourced fill-rate commentary](https://www.multibagg.ai/market-pulse/articles/nifty-gap-fill-trade-key-levels-cmv1aez0x000x39qp99w1zvrr) | C | Large gaps fill least |
| S15 | 3-bar reversal | none | C | Unknown |
| S16 | Last-hour intraday momentum | [Gao et al. JFE 2018](https://profiles.wustl.edu/en/publications/market-intraday-momentum/) | A (US/intl index) / C (NSE stocks) | Positive on indices |
| S17 | Intraday pair spread | [EPAT daily 2015-2025: Sharpe 0.089](https://blog.quantinsti.com/cointegrated-pairs-trading-indian-equity-market-epat-project/) | B (daily, negative-ish) | Weak even daily |

### Inferences
- Prioritise for the 2022-2026 backtest: S16 (only A-grade effect; test index-driven variant), S9 (only NSE-positive gross result), S6/S7 (most-tested structure; trade-count naturally capped at 1/day). Run S1, S5, S12 as negative controls to calibrate the cost model.
- Design constraints that matter more than entry logic, given the SEBI cost finding (costs = 57% of losses) and the Streak experience: cap trades to 1-2/day/stock, require target >= 0.4%, no entries 09:15-09:29, hard exit 15:10, and model slippage at >= 1 tick + 0.02% per side on stop-outs.
- Behavioural rationales (VWAP algo flow, stop clustering at PDH/OR, late-day rebalancing) are plausible but the only one with academic support is end-of-day rebalancing/intraday momentum.

### Gaps
- No source gives win rate + profit factor + drawdown + costs for any 5-min NSE large-cap equity setup; the reader's backtest will create the first such table.
- Zerodha "In The Money" ORB numbers, QuantInsti Raj TK statistics, and Streak user Walker's P&L were all images/video and not retrievable.
- quantifiedstrategies.com VWAP page blocked (bot wall); i-scholar Nifty time-of-day paper unreachable (DNS).
- Quantpedia was not productively searched (no India-specific intraday entries surfaced via web search).
