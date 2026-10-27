# Tools, Platforms and Data Sources for an Upstox-Executed AI/Automated Intraday System (India, as of Oct 2026)

Scope note: research done 2026-10-25. Upstox API facts are from the live developer docs (upstox.com/developer/api-documentation, copyright 2026) and Upstox Community posts dated Mar–May 2026 unless noted. Platform pricing is from vendor pages or third-party listings and is flagged accordingly.

## KQ1. Indian no-code / low-code algo platforms (pricing, backtests, live deployment, Upstox support, credibility)

### Takeaway
Only AlgoTest, Quantiply and 1Cliq have a confirmed, Upstox-sponsored integration (subscription fee waived, flat ₹10/order platform fee, locked until 31 Mar 2026 with "possible extension"). Tradetron's own pricing page does NOT list Upstox as a broker; Streak is Zerodha-only; Quantman's Upstox support is unconfirmed. All these platforms are backtest-first, options-centric builders — none offers "AI" in any ML sense, and after the SEBI Feb-2025 framework every third-party platform must be empanelled and run inside broker infrastructure.

### Cited Findings

**Upstox's own algo offering / partner integrations**
- Upstox named exactly three partner platforms with waived subscription fees for Upstox users: 1Cliq, Quantiply and AlgoTest; cost is a flat ₹10 per order charged on the platform; usual list prices cited as ~₹1,599+GST/mo (1Cliq) and ₹250–₹500/mo (Quantiply, AlgoTest); ₹10/order rate and free subscription locked until 31 March 2026 "with a possible extension"; AlgoTest backtesting credits still cost extra; activation is automatic by choosing Upstox at the platform login — [Upstox Community](https://community.upstox.com/t/we-have-worked-with-these-3-algo-platforms-to-get-the-subscription-fees-waived-for-you/13779)
- Separate Upstox Community post: "Automate your trading without coding – now free for Upstox users on AlgoTest"; live execution free of subscription, platform costs such as backtesting credits still apply — [Upstox Community](https://community.upstox.com/t/automate-your-trading-without-coding-now-free-for-upstox-users-on-algotest/13731)
- Upstox moderator on Tradetron: "Please refer to the Tradetron documentation for instructions on how to integrate Upstox as a broker" (i.e., Upstox does not document it) — [Upstox Community](https://community.upstox.com/t/api-keys-for-tradetron/13399)
- Upstox community thread asking whether Upstox API works with Stoxxo; a reply said the Stoxxo link was not working — [Upstox Community](https://community.upstox.com/t/algo-api-and-third-party-algo-bridge-query/11835)
- Upstox itself has no backtesting feature; it relies on integrated partners (AlgoTest claims it is integrated with Upstox) — [AlgoTest blog (competitor marketing)](https://algotest.in/blog/does-upstox-platform-support-backtesting-or-not.md)

**AlgoTest**
- Credit packages: Starter ₹499/500 credits, Explorer ₹999/1,100, Pro ₹2,499/3,000, Advanced ₹5,999/7,500, no expiry; backtesting: Limited plan 100 backtests = 100 credits, or Unlimited Weekly 799 credits / 28-day 2,499 credits — [AlgoTest pricing page (vendor)](https://algotest.in/blog/detailed-pricing-information-for-algotest/)
- Claims 7.5+ years of options history covering Nifty, BankNifty, FinNifty, Midcap, Sensex, Bankex and stock options — [AlgoTest blog (vendor)](https://algotest.in/blog/algotest-vs-stockmock.md)
- Upstox-specific flat ₹10/order brokerage via AlgoTest valid until 31 Mar 2026 — [Upstox Community](https://community.upstox.com/t/automate-your-trading-without-coding-now-free-for-upstox-users-on-algotest/13731)

**Tradetron**
- Official pricing (live bots = simultaneous live strategies): Free ₹0 (Live Offline only, 0 live), Starter ₹250/mo (1), Starter+ ₹708/mo (3), Retail ₹1,000/mo (5), Retail+ ₹2,083/mo (12), Creator ₹4,167/mo (25, 5 marketplace listings), Creator+ ₹7,500/mo (50, 10 listings); yearly billing "save 16%"; markets NSE/NFO/BFO/MCX plus crypto exchanges (Delta, CoinDCX, CoinSwitch, ZebPay); **Upstox is not listed** on the pricing page's broker section; brokers with zero platform fee are INDmoney and Delta Exchange; "Live Offline" mode runs trades without sending to broker (de facto paper trading) — [Tradetron pricing](https://tradetron.tech/pricing)
- Third-party listings give older/different tiers (₹300 Starter / ₹1,200 Retail / ₹2,500 Retail+) — [Techjockey](https://techjockey.com/compare/tradetron-vs-samco); a review says Rs 1,000–15,000/mo — [coinspot](https://coinspot.io/en/reviews/tradetron/). Treat official page as authoritative.
- Regulatory baggage: SEBI adjudication orders dated March 2026 "in the matter of TradeTron and other Algo Platforms" against multiple registered brokers (First Global, ITI Securities, Northeast Broking, Samco, R.K. Stockholding, Ashlar, Growth Securities) for alleged breach of clause 4.2 of SEBI's 2 Sept 2022 algo-platform circular; some brokers had stopped Tradetron services after that circular — [SEBI order](https://www.sebi.gov.in/sebi_data/attachdocs/mar-2026/ORDER_1774428858.pdf), [SEBI order](https://www.sebi.gov.in/sebi_data/attachdocs/mar-2026/ORDER_1774439178.pdf), [SEBI order](https://www.sebi.gov.in/sebi_data/attachdocs/mar-2026/ORDER_1774429674.pdf)
- In 2023 SEBI issued show-cause notices to 110+ brokers (incl. Zerodha, 5Paisa, Motilal Oswal) over unregulated algo-platform tie-ups; 2025 settlement scheme ~₹1–2 lakh per broker — [Angel One news](https://www.angelone.in/news/market-updates/sebi-to-launch-settlement-scheme-for-brokers-in-algo-violation-cases)

**Streak (Zerodha)**
- Zerodha announced 17 Jan 2024 that Streak (scanners, order placement, backtesting, virtual deployment) is free for all Zerodha users; Pro is a legacy paid tier closed to new subscriptions — [Zerodha Z-Connect](https://zerodha.com/z-connect/updates/zerodha-users-now-have-unlimited-access-to-streak), [Chittorgarh](https://www.chittorgarh.com/article/zerodha-streak-review-algo-trading-for-retail-investors/516/)
- Free platform lacks some Pro features (e.g., "Dynamic contracts" not supported) per Streak team on forum — [TradingQnA](https://tradingqna.com/t/streak-unlimited-is-now-accessible-for-all-zerodha-users/159215?page=3)
- Zerodha forum reply: live strategy deployment limited to 5 at a time; users requesting higher backtest caps — [TradingQnA](https://tradingqna.com/t/can-you-please-increase-the-back-test-and-other-limits-per-day/179326)
- Works only inside the Zerodha ecosystem (not usable with Upstox) — [Chittorgarh](https://www.chittorgarh.com/article/zerodha-streak-review-algo-trading-for-retail-investors/516/)

**Quantman**
- Third-party pricing: 7-day trial, Basic ₹1,300/mo (250 backtest credits, 4 live deployment credits), Premium ₹3,300/mo (1,000 backtest, 10 live) — [Techjockey](https://techjockey.com/detail/quantman), [AlgoTest comparison (competitor)](https://algotest.in/blog/algotest-vs-quantman/); backtest history "entire 4.5 years of authentic exchange data" / "past four years" — [Marketcalls](https://www.marketcalls.in/quantman/quantman-simplified-backtesting-and-automated-trading-interface-for-futures-and-options-traders.html)
- Broker list found names Zerodha, Angel One, Fyers "and others"; Upstox not named; official pricing URL (quantman.in → quantman.trade/pricing) returned 404 — [Marketcalls](https://www.marketcalls.in/?p=55215)

**uTrade Algos** (uTrade Solutions; Capterra): starting ₹999/mo, free trial; no-code multi-leg builder, pre-built "uTrade Originals", backtester; review counts conflict (0 ratings in one listing vs 4.9 from 247 in a widget) — [Capterra](https://www.capterra.com/p/10031448/uTrade-Algos/). No Upstox support evidence found.

**Algomojo** (bridge/API platform): 2020-era posts say free platform access for clients opening Upstox account via Algomojo, with Upstox providing 6-month API credit after a ticket — [Marketcalls](https://www.marketcalls.in/?p=54525); NexusFi lists $12–$72 price range with 7-day trial (unverified) — [NexusFi](https://nexusfi.com/d/platforms/algomojo/)

**Stoxxo**: Windows-based trading bridge listed as 5paisa partner — [5paisa](https://5paisa.com/trading-partners/stoxxo); no pricing found; Upstox compatibility unconfirmed.

**Sensibull** (options analytics, not an algo platform): free tier + Pro ~₹392/mo billed annually; integrates with Zerodha, AngelOne, Upstox, 5paisa; no backtesting, forward paper trading only — [strike.money review](https://www.strike.money/reviews/sensibull)

### Inferences
- For an Upstox account specifically, the practical no-code options today are AlgoTest, Quantiply or 1Cliq (fee-waived) — but the ₹10/order platform fee is on top of Upstox brokerage (₹20/order F&O), so an active intraday system pays ~₹30/order round-trip-side before taxes.
- "Live deployment credits" and "live bots" caps across Tradetron/Quantman/Streak mean these platforms are built for a handful of rule-based option strategies, not for an ML/LLM decision loop.
- The Tradetron adjudication orders show regulatory risk concentrates on brokers, which explains why Upstox only promotes a short list of empanelled partners.

### Gaps
- Could not retrieve Quantman's or TrueData/GDFL's official pricing pages (404s); figures are third-party.
- No independent, quantitative user-review data (e.g., slippage vs backtest) found for any platform; reviews are vendor blogs or aggregator sites.
- Speedbot, Kuants/Keev, Dhan's algo features: no results found in this research pass.
- Whether the Upstox ₹10/order partner offer was extended past 31 Mar 2026 is unconfirmed.

## KQ2. Open-source algo/backtesting frameworks usable with Indian data and Upstox

### Takeaway
OpenAlgo is the only open-source project with a first-class Upstox adapter plus Indian exchange support (NSE/BSE/NFO/BFO/CDS/MCX), a sandbox/analyzer paper-trading mode and bridges to TradingView/Amibroker/Python; vectorbt has India-flavoured tooling via marketcalls that uses OpenAlgo as the data layer. General frameworks (backtrader, zipline-reloaded, LEAN, Nautilus) have no documented NSE/Upstox integration — you would supply data and calendars yourself.

### Cited Findings
- OpenAlgo: AGPL-3.0, free, self-hosted (Windows 10/macOS 10.15/Ubuntu 20.04+, Python 3.12+, 2 GB RAM, 10 GB+ storage recommended for historical data); 37 broker plugins (35 securities brokers + Delta Exchange + Dhan sandbox); unified order/positions/holdings/funds/historical API; signal sources: TradingView, Amibroker, ChartInk, GoCharting, MetaTrader 5, N8N, Excel, Google Sheets, Chrome extension; WebSocket streaming of quotes/depth/order updates; Sandbox/Analyzer mode with ₹1 crore virtual capital and simulated orders; Flow no-code builder, Strategy RMS, Historify local data store, "AI trading agent" and MCP server — [OpenAlgo docs](https://docs.openalgo.in/)
- OpenAlgo broker list includes Upstox (`upstox`) alongside Zerodha, Dhan, Fyers, Angel, Groww, Kotak, etc. — [OpenAlgo brokers](https://docs.openalgo.in/connect-brokers/brokers)
- OpenAlgo Upstox plugin: create app at Upstox Developer portal, redirect URL `http://127.0.0.1:5000/upstox/callback`; tradable exchanges NSE, BSE, NFO, BFO, CDS, BCD, MCX; index feeds NSE_INDEX, BSE_INDEX, GLOBAL_INDEX — [OpenAlgo Upstox page](https://docs.openalgo.in/connect-brokers/brokers/upstox.md)
- OpenAlgo docs do not mention SEBI static-IP/algo-ID compliance — [OpenAlgo docs](https://docs.openalgo.in/)
- vectorbt for Indian markets: `marketcalls/vectorbt-backtesting-skills` (~179 stars) uses OpenAlgo as data source (NSE/BSE/NFO/MCX), includes intraday fee modeling, NIFTY 50 benchmark, broker-neutral fee constants — [GitHub](https://github.com/marketcalls/vectorbt-backtesting-skills), [docs](https://vectorbt.marketcalls.in/)
- Upstox official Python SDK: `upstox-python-sdk` (Swagger-generated, targets API v2, supports WebSocket streaming); versions seen 2.17.0–2.19.0 (Nov 2025 mirror); older `upstox` PyPI package deprecated/EOL — [PyPI](https://pypi.org/project/upstox-python-sdk/2.1.0/), [ecosyste.ms mirror](https://awesome.ecosyste.ms/projects/github.com%2Fupstox%2Fupstox-python), [PyPI upstox (deprecated)](https://pypi.org/project/upstox/)
- WebSocket feed is Protobuf; community gist shows compiling `MarketDataFeed.proto` to `MarketDataFeed_pb2.py` — [gist](https://gist.github.com/Rahulzz); official V3 doc confirms Protobuf and binary subscription frames — [Upstox docs](http://upstox.com/developer/api-documentation/v3/get-market-data-feed/)
- Community wrapper `BarathGB007/upstox-python-data` (~22 stars): REST + WebSocket ticks for NSE indices and F&O — found via search, unverified quality.
- Free NSE data libs: `jugaad-data` (NSE/RBI historical + live, bhavcopy, "supports new NSE website", releases through 0.33.1 on 2026-03-16) — [PyPI](https://pypi.org/project/jugaad-data), [piwheels](https://www.piwheels.org/project/jugaad-data); `pybhav` (equity/F&O/currency/SME bhavcopy to pandas) — [PyPI](https://pypi.org/project/pybhav/); `aynse` (lean NSE fetcher incl. F&O bhavcopy) — [PyPI](https://pypi.org/project/aynse/)
- Exchange calendars: `exchange_calendars` library provides 50+ exchange calendars and allows custom ones; search did not confirm XNSE in zipline-reloaded/Nautilus/LEAN — [PyPI exchange-calendars](https://pypi.org/project/exchange-calendars/4.0.1/)
- TradingAgents README says it works with any Yahoo Finance ticker incl. `RELIANCE.NS` / `.BO` — [GitHub](https://github.com/TauricResearch/TradingAgents)

### Inferences
- The lowest-friction stack for an Upstox user is: OpenAlgo (execution + paper trading + Upstox adapter) ← Python strategy/ML model → vectorbt or backtrader for research using OpenAlgo/Upstox candles. This avoids writing the Upstox OAuth, Protobuf and rate-limit plumbing yourself.
- Because OpenAlgo is self-hosted, it is the user's own "algo" from a SEBI standpoint; static-IP and 10-OPS rules still apply to the Upstox orders it sends.
- Frameworks like LEAN/Nautilus/Zipline are viable only for offline research; none ships NSE intraday data or an Upstox broker module.

### Gaps
- Did not verify from source code whether OpenAlgo's Upstox plugin supports historical candles and WebSocket depth (page does not state).
- No confirmation of XNSE calendar presence in zipline-reloaded / Nautilus / LEAN docs.
- NSEPython maintenance status not found.
- Jesse / freqtrade not researched (freqtrade is crypto-only by design; not relevant to NSE).

## KQ3. Indian market data sources for intraday backtesting (1-min/5-min, options)

### Takeaway
Upstox's free V3 candle API gives minute/hour data back to Jan 2022 (1–15-min bars limited to a 1-month window per request, so you must page), and daily back to 2000 — adequate for ~4.5 years of index/futures intraday but not deep options history. For long options history you need a paid vendor (TrueData historical-only ~₹2,599/mo list after Jul 2024; indicative ~₹4,200+GST/yr quotes for BankNifty 1-min weekly options CSV) or a platform's embedded data (AlgoTest 7.5 yrs). Free Kaggle/forum datasets exist but have documented strike-coverage gaps.

### Cited Findings
**Upstox Historical Candle V3 (official doc, 2026)**
- Units/intervals: minutes 1–300, hours 1–5, days/weeks/months = 1 — [Upstox V3 historical](http://upstox.com/developer/api-documentation/v3/get-historical-candle-data/)
- Availability: minutes and hours from January 2022; days/weeks/months from January 2000 — same source
- Per-request window: 1–15-min → one month; >15–300-min and hours → one quarter; days → one decade; weeks/months unlimited; exceeding → "invalid request" error; dates outside range → UDAPI1148 — same source
- V3 adds custom intervals, Global Index, Global Indicators, India VIX (`NSE_INDEX|India VIX`), same response format as V2 — same source
- V2 (legacy) supports 1-minute, 30-minute, daily, weekly, monthly only — [Upstox llms.txt index](http://upstox.com/developer/api-documentation/llms.txt)
- Community confusion: older V2-era replies said 1-min data only for last 6 months; V3 launch post states minutes/hours since Jan 2022 — [Upstox Community V3 launch](https://community.upstox.com/t/get-historical-data-in-any-time-frame-you-wished-we-built-new-releases-at-upstox-api/8845), [older thread](https://community.upstox.com/t/historical-data-how-many-days/6094); a later thread says "Historical minute data is available for last 1 month" (likely referring to per-request window) — [Upstox Community](https://community.upstox.com/t/bug-in-historical-candle-data-error-handling/11912)
- Historical candle calls are "Other Standard APIs": 50/sec, 500/min, 2,000 per 30 min — [Upstox rate limits](http://upstox.com/developer/api-documentation/rate-limiting/)
- API data is free (no monthly API fee; standard brokerage on orders) — [Upstox Community (staff)](https://community.upstox.com/t/upstox-api-charges/6552), [Upstox Community](https://community.upstox.com/t/inquiry-regarding-upstox-api-charges-and-call-limits/8425)

**Paid vendors**
- TrueData price revision effective 1 Jul 2024 (via Fyers notice): Historical Only ₹1,599 → ₹2,599; Real-Time + Historical ₹2,599 → ₹3,999 (per month implied; MCX/BSE separate) — [Fyers notice](https://fyers.in/notice-board/revision-in-truedata-subscription-pricing/)
- TrueData coverage: real-time + historical via API for NSE equity, indices, F&O, currency derivatives, MCX; history available with/without bid-ask — [TrueData KB](https://feedback.truedata.in/knowledge-base/article/getting-started-with-truedata-market-data-api)
- TrueData acknowledged slow 1-min history download server and was rebuilding backend (forum, undated) — [TradingQnA](https://tradingqna.com/t/global-data-feeds-alternatives/56723)
- Global Datafeeds sells historical IEOD 1-min data as compressed CSV; older real-time NSE F&O plans ₹2,775/mo or ₹26,630/yr, Lite ₹20,100/yr (dated) — [TradingQnA](https://tradingqna.com/t/global-data-feeds-alternatives/56723), [Marketcalls](https://www.marketcalls.in/premium/globaldatafeeds/nimbledatapropluslite)
- Trader-reported quote: Rs 4,200 + GST per year for BankNifty 1-min weekly options history, CSV, from June 2016, from an NSE-approved vendor (GDFL/TrueData/Accelpix named) — [TradingQnA](https://tradingqna.com/t/received-quote-for-historical-bank-nifty-1-min-data/135259)
- Forum anecdotes: tick data "15–20k per year" currently, "30k few years back" (unverified) — [TradingQnA](https://tradingqna.com/t/if-anyone-is-looking-for-f-o-data/193880)
- NSE's own 2026 domestic tariff lists 1-minute snapshot F&O product at ₹16,00,000/yr per medium (enterprise/redistributor pricing) — [NSE pricing file](https://nsearchives.nseindia.com//web/mediaattachment/2026-03/NSE_Pricing_file_-_Domestic_clients_20260309171343.pdf)

**Other broker APIs as data sources**
- Dhan: trading APIs free; Data API ₹499 + taxes/month (free-with-trades promo discontinued); OHLC rate limit 10 req/sec; multi-minute + daily OHLC with volume/OI — [Dhan support](https://dhan.co/support/platforms/dhanhq-api/is-the-dhanhq-data-api-subscription-free-if-i-execute-a-minimum-number-of-trades-every-month/), [DhanHQ](https://dhanhq.co/trading-apis)
- Zerodha cut Kite API data charges to ₹500/month after NSE regulatory signal — [Marketcalls](https://www.marketcalls.in/fintech/zerodha-slashes-api-data-charges-to-%e2%82%b9500-month-after-regulatory-green-signal-from-nse.html)
- ICICI Breeze API reported to offer free Nifty/BankNifty 1-min options OHLC/volume/OI, "some data is bad though" — [TradingQnA](https://tradingqna.com/t/historical-options-data-for-indices-for-backtesting/174282)

**Free datasets**
- Kite forum user shared 5 years (2016–2021) of 1-min Nifty/BankNifty F&O OHLC via Kaggle link by DM; another user found a 2016–2022 1-min set had "very less number of strike prices" and inconsistent strikes — [Kite forum](https://kite.trade/forum/discussion/12137/nifty-bank-nifty-futures-options-data)
- Daily data free from NSE website (bhavcopy) — [TradingQnA](https://tradingqna.com/t/historical-options-data-for-indices-for-backtesting/174282); Python access via jugaad-data/pybhav/aynse (see KQ2)
- Platform-embedded options data: AlgoTest 7.5+ yrs (vendor claim) — [AlgoTest](https://algotest.in/blog/algotest-vs-stockmock.md); Quantman ~4–4.5 yrs — [Marketcalls](https://www.marketcalls.in/quantman/quantman-simplified-backtesting-and-automated-trading-interface-for-futures-and-options-traders.html)

### Inferences
- For Nifty/BankNifty index and futures 1-min/5-min research, Upstox V3 alone yields ~Jan 2022→today for free; a full pull requires ~57 monthly requests per instrument at 1–15-min granularity (well within 50/sec limits).
- Expired weekly option contracts are the real bottleneck: Upstox candles are keyed by live instrument keys, so historical expired-option series need a vendor or platform data; budget ₹2.5k–4k/month (TrueData) or a few thousand ₹/yr for CSV dumps.
- Free datasets are fine for prototyping but quality (strike coverage, bad ticks) makes them unsuitable for final validation.

### Gaps
- Could not fetch TrueData's or GDFL's live pricing pages (404); all vendor figures are from broker notices/forums.
- Did not confirm whether Upstox V3 serves candles for expired option contracts.
- Angel SmartAPI historical limits/pricing not found.
- No public Kaggle URL for an NSE 1-min options dataset was located.

## KQ4. "AI trading bot" products marketed in India — what they really are

### Takeaway
No Indian retail product found provides verified, audited AI trading performance. What is sold as "AI" is (a) pattern-recognition/NLP screeners (StockEdge, Tickertape), (b) options analytics with rule-based backtesting (Quantsapp, Opstra, Sensibull), or (c) outright frauds via Telegram/YouTube/WhatsApp that NSE and police have flagged in 2026. SEBI's rules require black-box/AI strategy providers to register (as research analysts for black-box methods) and bar return-based marketing.

### Cited Findings
- StockEdge (Kredent Infoedge) added AI chart-pattern recognition (head-and-shoulders, triangles, flags, wedges) in 2023 in its Pro tier, plus plain-English "Stock AI" Q&A; third-party review says pattern scan "appears inconsistent" and users report performance issues — [Outlook Startup](https://startup.outlookindia.com/sector/saas/kolkata-based-kredent-infoedge-adds-ai-driven-chart-pattern-in-stockedge-news-7298), [strike.money review](https://www.strike.money/?p=10016)
- Tickertape: 200+ filter screener over ~4,600 stocks, scorecard checklist; data updates end-of-day, not suited to intraday — [Techjockey](https://www.techjockey.com/detail/tickertape)
- Quantsapp: free subset; Pro ₹1,350/mo, Pro+ ₹2,500/mo (annual); 100+ analytics, real-time Greeks/OI, rule-based strategy backtesting/optimizer — [strike.money](https://www.strike.money/reviews/quantsapp)
- Opstra (Definedge): strategy builder, options backtesting/simulator, IV charts; no current price found — [strike.money](https://www.strike.money/reviews/definedge-opstra-alternatives)
- Sensibull: no backtesting, forward paper trading only; Upstox integration — [strike.money](https://www.strike.money/reviews/sensibull)
- None of the above results contain backtested returns, accuracy rates or independent verification; content is vendor marketing or affiliate review — [strike.money](https://www.strike.money/reviews/stockedge-alternatives), [officechai](https://officechai.com/learn/ai-tools-for-stock-market-in-india/)
- NSE (Sept 2026) cautioned against individuals offering tips, assured returns, account handling and dabba trading via Telegram/YouTube/Facebook; one operator ran a YouTube channel named "Ai Trading Stock Market Broker"; another asked investors for login ID/password — [Moneylife](https://www.moneylife.in/article/nse-warns-investors-against-8-entities-offering-assured-returns-dabba-trading-and-accounthandling-services/81631.html)
- Mumbai EOW busted an "AI returns" racket (entities incl. "Ojasvi AI") that allegedly misled 8,500+ investors — [Moneylife](https://moneylife.in/article/fraud-alert-ai-returns-forex-and-trading-scams/78981.html)
- Typical pattern: WhatsApp/Telegram groups promising guaranteed returns → fake trading apps → small early withdrawals → fees/taxes to unlock — [Tata MF (Oct 2026)](https://www.tatamutualfund.com/blogs/guaranteed-return-whatsapp-groups-and-fake-trading-apps-how-scam-actually-works)
- SEBI June 2022 warning against unregulated algo platforms advertising returns; Sept 2022 circular ordering brokers to terminate such partnerships within 7 days — [Business Standard](https://www.business-standard.com/article/pf/stick-to-algos-vetted-by-exchange-or-a-reputed-broker-advise-experts-122061300948_1.html), [Angel One](https://www.angelone.in/news/market-updates/sebi-to-launch-settlement-scheme-for-brokers-in-algo-violation-cases)
- Under the Feb-2025 framework providers must be empanelled with exchanges; black-box algos require the provider to register as a research analyst and disclose/re-register on logic changes — [sahi.com](https://www.sahi.com/blogs/is-ai-trading-legal-in-india), [Nishith Desai](https://www.nishithdesai.com/default.aspx?id=6177)
- Commentary: unregistered Telegram/WhatsApp algo vendors' performance claims were "in almost every documented case, either unverifiable or false" — [TaxTMI](https://www.taxtmi.com/tmi_blog_details?id=895432)
- SEBI sought expanded powers (Mar 2025) against unauthorised financial advice on social media — [IMS Today](https://imsuc.ac.in/images/IMS Today March-2025 NEWS PAPER.pdf)

### Inferences
- A self-built AI system that only trades the user's own account is legal and unregistered if it stays ≤10 OPS; selling or sharing its signals (beyond immediate family) would trigger empanelment/RA registration.
- Every "AI bot" sold to Indian retail with return claims should be presumed non-compliant with SEBI's 2022/2025 rules.

### Gaps
- No SEBI (as opposed to NSE/police) 2025–2026 alert specifically naming "AI trading bots" was found.
- No independent audit of any Indian AI/ML trading product's live track record exists in the sources found.

## KQ5. Upstox API as the execution layer (v2/v3, 2026)

### Takeaway
Upstox API is free (brokerage only), OAuth-based with a daily token that dies at 3:30 AM and no refresh token, supports MARKET/LIMIT/SL/SL-M with products I (intraday), D, MTF (no CO/BO in V3), rate-limited to 10 orders/sec (50 for SEBI-registered algos), with a Protobuf WebSocket feed (2 connections, up to 2,000–5,000 instruments) and a separate order-update stream. Since 1 Apr 2026 it enforces SEBI's retail-algo regime: one API app per user, primary + secondary static IP (change once/week), `X-Algo-Name` header for registered algos, MPP default on market orders.

### Cited Findings
**Cost**
- Upstox staff: "no fixed monthly charges for trading through the API"; standard brokerage applies; no daily API-call cap beyond rate limits — [Upstox Community](https://community.upstox.com/t/upstox-api-charges/6552), [Upstox Community](https://community.upstox.com/t/inquiry-regarding-upstox-api-charges-and-call-limits/8425)
- Brokerage: intraday & futures ₹20/order or 0.05% (lower); options flat ₹20/order; Add-On plan ₹22 — [Upstox pricing](https://upstox.com/pricing/), [Upstox help](https://upstox.com/help-center/what-is-upstox-add-on-264254/)
- Upstox Plus (premium API tier): "can be activated for free initially; if chargeable in future Upstox will notify"; Depth-30 data exclusive to Plus — [Upstox Plus T&C PDF](https://upstox.com/files/terms-and-condition/plus-pack.pdf)

**Auth / tokens**
- OAuth 2.0 authorization-code flow via `https://api.upstox.com/v2/login/authorization/dialog` → single-use code → POST `/v2/login/authorization/token`; also semi-automated (notifier URL) and manual token generation from dashboard; TOTP available for 2FA — [Upstox auth docs](http://upstox.com/developer/api-documentation/authentication/)
- Access token expires at 3:30 AM next day regardless of generation time; new token invalidates old; **no refresh tokens** ("must manually create your access token daily for compliance") — [Upstox Community](https://community.upstox.com/t/access-token-validity/4646), [Upstox Community](https://community.upstox.com/t/do-upstox-provides-api-with-refresh-token-as-daily-i-need-to-generate-the-access-token-please-guide/13077)
- "Analytics Token": long-lived read-only access — [Upstox llms.txt](http://upstox.com/developer/api-documentation/llms.txt)
- TOTP login endpoint rate limit: 1/sec, 10/min, 60 per 30 min — [Upstox rate limits](http://upstox.com/developer/api-documentation/rate-limiting/)
- SEBI/NSE standards: 2FA once per trading day, no continuous refresh-token sessions, daily logout of API sessions — [Fyers notice](https://fyers.in/notice-board/new-sebi-framework-for-retail-algo-trading-from-april-01-2026/), [FinSec Law](https://www.finseclaw.com/article/nse-releases-implementation-standards-for-retail-participation-in-algorithmic-trading)

**Rate limits (official, references circular of 5 May 2025)**
- Order APIs (place/modify/cancel/multi/GTT combined): Regular algos 10/sec, 500/min, 2,000 per 30 min; SEBI-registered algos 50/sec, 500/min, 2,000 per 30 min — [Upstox rate limits](http://upstox.com/developer/api-documentation/rate-limiting/)
- Other standard APIs (holdings, positions, funds, historical): 50/sec, 500/min, 2,000/30 min; limits per API per user; exceeding may cause temporary suspension — same source

**Orders (Place Order V3)**
- `order_type`: MARKET, LIMIT, SL, SL-M; `product`: I (Intraday), D (Delivery), MTF; `validity`: DAY, IOC; `slice` auto-splits at freeze qty; `tag` ≤40 chars; `is_amo` ignored (inferred from session); **no bracket/cover order mentioned**; Place Order accessible 5:30 AM–12:00 AM IST (UDAPI100074); optional `X-Algo-Name` header required only for exchange-approved algos (UDAPI1156 if invalid) — [Upstox Place Order V3](http://upstox.com/developer/api-documentation/v3/place-order/)
- Market Price Protection parameter for MARKET and SL-M orders; MPP default from 1 Apr 2026 — [Upstox Community](https://community.upstox.com/t/important-new-sebi-exchange-mandates-for-api-trading-effective-1st-april-2026/14822), [Upstox MPP post](https://community.upstox.com/t/market-price-protection-mpp-on-upstox-trade-smarter-safer/9122)
- Supporting endpoints exist for brokerage/charges calculation and GTT — [Upstox llms.txt](http://upstox.com/developer/api-documentation/llms.txt)

**WebSocket**
- Market Data Feed V3: modes `ltpc`, `option_greeks`, `full` (5-level depth + greeks), `full_d30` (30-level, Plus only); limits (Normal): LTPC 5,000 individual / 2,000 combined; Greeks 3,000/2,000; Full 2,000/1,500; Full D30 (Plus) 50/1,500; connections: Normal 2, Plus 5; Protobuf, binary subscribe frames, market-status → snapshot → live updates, ping/pong — [Upstox Market Data Feed V3](http://upstox.com/developer/api-documentation/v3/get-market-data-feed/)
- Portfolio Stream Feed (order/position updates) is a separate WebSocket with its own authorize URL — [Upstox llms.txt](http://upstox.com/developer/api-documentation/llms.txt)
- Community reports of 403/429 on parallel connections and extra connections receiving no data — [Upstox Community](https://community.upstox.com/t/market-data-feed-v3-multiple-web-socket-connections/10465), [Upstox Community](https://community.upstox.com/t/geting-issue-with-websocket/9150)

**SEBI retail-algo compliance on Upstox (effective 1 Apr 2026)**
- SEBI circular SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/0000013 dated 4 Feb 2025: broker is principal, algo provider is agent; exchange permission per algo; registration via broker above an OPS threshold; sharing only with immediate family; exchange-assigned unique algo ID per order; fast-track + standard registration — [SEBI](https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html), [Mondaq](https://mondaq.com:443/india/commoditiesderivativesstock-exchanges/1581380/sebi-circular-safeguarding-retail-investors-in-algorithmic-trading), [QuantInsti](https://blog.quantinsti.com/sebi-algo-trading-guidelines-retail-investors)
- Dates slipped: originally 1 Aug 2025 → 1 Oct 2025 (SEBI 29 Jul 2025) → broker notices now cite 1 Apr 2026 with old/new frameworks parallel until 31 Mar 2026 — [Mondaq newsletter](https://www.mondaq.com/india/securities/1622512/general-newsletter-may-2025), [Fyers](https://fyers.in/notice-board/new-sebi-framework-for-retail-algo-trading-from-april-01-2026/)
- Upstox announcement (effective 1 Apr 2026): >10 OPS requires exchange registration and Algo ID (process "still being finalized"); one Primary + one Secondary static IP per user, each IP linkable to one customer only, IP change once per calendar week (My Apps or API), IP update invalidates tokens, IPv4/IPv6 accepted; static-IP check applies to place/modify/cancel/multi/GTT/exit-all, not to holdings/positions/funds/historical; `X-Algo-Name` header mandatory on orders from an Algo App — [Upstox algo circular page](http://upstox.com/developer/api-documentation/announcements/algo-trading-circular/)
- Upstox Community (posted 27 Mar 2026): only one active API app per user from 1 Apr 2026 (latest kept, others deleted); static IP mandatory; MPP default; links to NSE circular NSE/INVG/67858; 7 May 2026 reply: family accounts can share static IPs — [Upstox Community](https://community.upstox.com/t/important-new-sebi-exchange-mandates-for-api-trading-effective-1st-april-2026/14822), [NSE circular](https://nsearchives.nseindia.com/content/circulars/INVG67858.pdf), [Family static IP](https://community.upstox.com/t/introducing-family-account-share-static-ip-with-your-family-on-upstox-api/15635)
- Static IP management APIs (get/update, weekly limits) exist — [Upstox llms.txt](http://upstox.com/developer/api-documentation/llms.txt); setup guide — [Upstox Community](https://community.upstox.com/t/static-ip-setup-guide-for-api-traders/14683)
- Cloud bots need a fixed egress IP (vendor blogs on QuotaGuard-style proxies) — [QuotaGuard](https://www.quotaguard.com/blog/upstox-api-static-ip) (vendor marketing)

### Inferences
- Intraday ML/LLM systems with modest order rates (a few orders/minute) sit comfortably under 10 OPS and need no exchange registration — only static IP + single app + daily manual token.
- Absence of bracket/cover orders means SL/target management must be done client-side (two legs) or via GTT; this adds latency and partial-fill handling complexity.
- The 3:30 AM token expiry plus "no refresh token" means a human (or TOTP-assisted semi-automation) must re-auth every morning before 9:15; fully unattended 24×7 operation is by design not supported.
- Rate limits are generous for data (50/sec) but tight for orders at 500/min — a scalping system placing + modifying SLs across many legs could hit the 30-minute 2,000 cap.

### Gaps
- Official page does not state access-token expiry; the 3:30 AM figure comes from staff forum replies.
- Whether Upstox Plus has become chargeable, and its exact price, is unverified.
- Exact Algo-ID registration procedure on Upstox was "to be shared later" as of the docs read.
- Did not read the NSE INVG/67858 circular itself.

## KQ6. Paper-trading / forward-testing options before going live on Upstox

### Takeaway
Upstox's sandbox is an order-format validator, not a paper account (no virtual funds, positions or order book); realistic forward testing requires OpenAlgo's Analyzer mode (₹1 crore virtual, Upstox data), Tradetron's "Live Offline", Streak's virtual deploy (Zerodha only), or a self-built simulator fed by the live Upstox WebSocket.

### Cited Findings
- Upstox sandbox supports only Place/Modify/Cancel Order (incl. V3) and Place Multi Order; rolling out "in phases"; one sandbox app per user; sandbox token valid 30 days; sandbox tokens cannot place live orders — [Upstox sandbox docs](http://upstox.com/developer/api-documentation/sandbox/)
- Community: sandbox is a "request-response simulation environment… no virtual funds or portfolio tracking"; moderator confirmed order-status API not available in sandbox and no plans to extend at that time; developers pair sandbox order placement with live LTP to simulate fills — [Upstox Community](https://community.upstox.com/t/sandbox-vs-prod-data-credentials-and-migration/10369), [Upstox Community](https://community.upstox.com/t/are-sandbox-enabled-endpoints-expanding/10067), [Upstox Community](https://community.upstox.com/t/uat-sandbox-environment-for-strategy-testing-with-live-data/10274)
- Reported sandbox 401 (UDAPI100050) issues on order placement despite valid token — [Upstox Community](https://community.upstox.com/t/urgent-sandbox-api-persistent-401-unauthorized-error-udapi100050-on-order-placement-despite-valid-token/11035)
- OpenAlgo Sandbox/Analyzer: strategies run on live market data with ₹1 crore sandbox capital, isolated simulated orders and account state — [OpenAlgo docs](https://docs.openalgo.in/)
- Tradetron Free plan "Live Offline" runs every trade but sends no orders to broker — [Tradetron pricing](https://tradetron.tech/pricing)
- Streak free tier includes "virtually deploying strategies in live markets" (Zerodha only) — [Zerodha](https://zerodha.com/z-connect/updates/zerodha-users-now-have-unlimited-access-to-streak)
- Sensibull offers forward paper trading of options (no backtest) — [strike.money](https://www.strike.money/reviews/sensibull)
- Third-party comparison of Indian paper-trading APIs notes Upstox uses a separate sandbox app/token with incomplete API coverage — [onetradejournal](https://onetradejournal.com/trading-apis/paper-trading-api-india)

### Inferences
- The most faithful forward test for an Upstox-bound system is OpenAlgo Analyzer mode (same adapter, same instrument keys, live Upstox ticks) followed by a small-lot live phase; the Upstox sandbox only de-risks payload/auth bugs.

### Gaps
- No source quantifies how OpenAlgo's Analyzer models fills/slippage (mid, LTP, depth-based?).

## KQ7. Global open-source AI/LLM trading-agent projects (FinRL, TradingAgents, FinGPT, ai-hedge-fund) — NSE intraday adaptability and limitations

### Takeaway
These projects are research/educational, daily-bar, US-equity oriented; TradingAgents accepts `.NS` Yahoo tickers but none has an NSE intraday data pipeline, Indian cost model, or live broker (Upstox) execution. Academic critiques stress LLM look-ahead/memorisation bias and absent transaction-cost/liquidity modelling, which makes their backtests weak evidence for intraday NSE.

### Cited Findings
- TradingAgents README: works with any Yahoo Finance-covered market via suffix, e.g., `RELIANCE.NS`, `.BO` — [GitHub](https://github.com/TauricResearch/TradingAgents)
- ai-hedge-fund (virattt): "proof-of-concept… educational and research purposes", backtester included, trades simulated only, no live execution; PyPI blurb "not intended for real trading" — [SourcePulse](https://www.sourcepulse.org/projects/1797841), [PyPI ai-rich/related listing](https://pypi.org/project/ai-rich/)
- FinRL paper: environments cover NASDAQ-100, DJIA, S&P 500, HSI, SSE 50, CSI 300; transaction cost and bid-ask spread are user-set parameters — [arXiv](https://arxiv.org/pdf/2011.09607)
- LLM backtest leakage: "a traditional backtest can leak the future through data, and an LLM backtest can also leak it through the model itself"; models may recall which stocks performed well — [arXiv multi-agent debate paper](https://arxiv.org/pdf/2609.29701); Look-Ahead-Bench benchmark for point-in-time LLM look-ahead bias — [arXiv](https://arxiv.org/pdf/2601.13770)
- Realism gaps in LLM-agent studies: small ticker universe, few quarters, no transaction costs/spreads/taxes/liquidity — [arXiv](https://arxiv.org/pdf/2609.29701); latency, exchange priority rules and agent interaction not modelled; repeated iteration risks overfitting — [arXiv PredictionMarketBench](https://arxiv.org/pdf/2602.00133)
- Benchmark critique: existing LLM-finance benchmarks' backtest methodology is "particularly problematic… models have likely been pre-trained on substantial portions of financial history" — [arXiv](https://arxiv.org/pdf/2503.18313v2)
- Backtrader-Bench benchmarks LLM agents on algorithmic trading tasks (2026) — [arXiv](https://arxiv.org/pdf/2608.11232)

### Inferences
- Adapting these to NSE intraday means replacing the data layer with Upstox V3 candles/WebSocket (via OpenAlgo), adding Indian costs (₹20/order, STT, exchange fees, GST), and NSE calendar/lot sizes; the agent logic is reusable, but their published results carry no evidential weight for NSE intraday.
- LLM-driven decision loops on 1-min bars face latency/cost constraints that these daily-bar frameworks never addressed.

### Gaps
- No GitHub issues or forks specifically adapting FinRL/ai-hedge-fund to NSE were found.
- FinGPT not researched in this pass.
- No published live track record for any of these frameworks was found.
