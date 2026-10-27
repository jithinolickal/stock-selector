# Free / near-free (≤ ₹500 one-time) historical NSE index-options data for intraday option-selling backtests (as of Oct 2026)

Scope: Nifty / Bank Nifty / Sensex weekly options; need EXPIRED contracts at intraday intervals for 9:20 straddle, iron condor, credit-spread backtests. AlgoTest and Upstox Plus excluded per brief. "Free" = no data fee beyond having a (free/zero-AMC) demat account. Anything paid monthly (Dhan ₹499/mo, Groww ₹499/mo, Kite Connect ₹500/mo) is listed for reference but violates the ≤ ₹500 one-time constraint unless used for a single month.

## Ranked catalogue (free + expired contracts + intraday + depth)

### Takeaway
Only two sources are both genuinely free and serve intraday candles for EXPIRED index options: (1) ICICI Direct Breeze API (fixed-strike, 1-second/1-minute, ~3 years, free with an ICICI Direct account) and (2) the Hugging Face dataset `thetrademarkk/india-index-options-1m` (1-min NIFTY/BANKNIFTY/SENSEX options, 2021–2026, CC-BY-NC, unverified provenance). The next tier is paid-monthly broker data APIs (Dhan ₹499/mo rolling-moneyness minute data with IV, 5 yrs; Groww ₹499/mo fixed-contract 1-min candles from 2020; Kite Connect ₹500/mo but NO expired options). NSE's free F&O bhavcopy gives daily OHLC/OI/settlement per strike back to the 2000s but nothing intraday.

### Ranked table

| Rank | Source | Expired options? | Intervals | Depth | Fields | Cost / prerequisite | Access | Evidence quality |
|---|---|---|---|---|---|---|---|---|
| 1 | ICICI Direct Breeze API | Yes (fixed strike+expiry as input; community tool downloads expired expiries) | 1second, 1minute, 5minute, 30minute, 1day (options) | ~3 yrs (ICICI pages); SDK README claims 10 yrs | OHLCV (+OI in response per SDK), no IV | Free; needs ICICI Direct demat (free to open; brokerage applies only if you trade) | REST / Python SDK `breeze_connect`; 1000 candles per call; 100 calls/min, 5000/day | Official ICICI pages + SDK README; "expired" support confirmed only by community tool + forum users |
| 2 | Hugging Face `thetrademarkk/india-index-options-1m` | Yes (per-expiry parquet files) | 1-min | ~May 2021 → mid-2026 | OHLCV, strike, option_type, expiry; OI documented but not shown in viewer | Free download (~4 GB; options ~1.6 GB); CC-BY-NC-4.0 | Bulk download (parquet) | Dataset card only; provenance unnamed; "far strikes sparse/absent" |
| 3 | NSE F&O bhavcopy (UDiFF since 8 Jul 2024; legacy before) | Yes (every traded strike/expiry daily) | EOD only | Legacy archive verified back to at least Jan 2019 (file 2000s-era exists per packages) | Open/High/Low/Close/Last/Settle/OI/ChgOI/Volume/Turnover/UnderlyingPrice | Free, no account | Direct URL (verified HTTP 200 via curl 26 Oct 2026) or jugaad-data/bhavkit/pybhav | Official NSE files; verified by download |
| 4 | Dhan DhanHQ "Expired Options Data" (Rolling Option API) | Yes, but rolling by MONEYNESS (ATM±N), not fixed strike | 1,5,15,25,60-min | Up to 5 yrs | OHLCV + **IV** + OI + spot + strike | ₹499+GST / 30 days (Data API); Dhan account | `POST /v2/charts/rollingoption`, 30 days per call | Official docs + official FAQ |
| 5 | Groww Trade API (Backtesting APIs) | Appears yes (Expiries + Contracts APIs; docs example fetches Jan-2024 contracts) | 1,2,3,5-min (30 days/req); 10,15,30-min (90 d); 1h+ (180 d) | From 2020 | OHLCV + OI (FNO); no IV | ₹499+taxes/mo (₹0 plan excludes backtesting APIs); Groww account | Python SDK `get_expiries` → `get_contracts` → `get_historical_candles` | Official docs; expired-candle behaviour not explicitly stated |
| 6 | Zerodha Kite Connect | **No** (expired options not served; expired futures day-candles only) | minute…60minute, day (live contracts) | n/a for expired options | OHLCV + OI | ₹500/app/month (free Personal tier has no data) | REST | Official docs + repeated staff forum replies (Aug 2025, Oct 2025, Mar 2026, Sep 2026) |
| 7 | Angel One SmartAPI | **No** | 1-min (30 days/req), 5-min (100 days) etc. for live contracts | n/a | OHLCV, no OI | Free | REST | Staff forum replies; docs page not fetchable |
| 8 | Fyers API | **No** | live contracts only | n/a | | Free with account | REST | Official Fyers KB (Sept 2025) |
| 9 | 5paisa | **No** | 1-min…1-day, ~6 months intraday (live) | n/a | OHLCV | | REST | Official forum |
| 10 | Shoonya/Finvasia | Unknown (not documented) | 1,3,5,10,15,30,60,120,240-min | Not stated | OHLC | Free API | `POST /NorenWClientAPI/TPSeries` | Official docs silent on expired |
| 11 | Kotak Neo | No historical OHLCV per community (official unanswered) | | | | | | GitHub issue (repo archived) |
| 12 | Alice Blue ANT | No (NFO = current expiry only; data API only 17:30–08:00) | Day, Minute | NSE 2 yrs; NFO current expiry | | Free | | Third-party client-library docs |
| — | Paytm Money, HDFC Sky, Motilal | Not found | | | | | | No sources found |

### Cited Findings (ranking rationale)
- Breeze API: "Only Breeze gives 3 years of second level LTP data", "3 years of Futures and Options historical data", "No charges at all to connect your systems, creating apps or for access to the historical data" — [ICICI Breeze home](https://api.icicidirect.com/apiuser/home)
- Breeze SDK README: options intervals "1second","1minute","5minute","30minute","1day"; "Maximum candle intervals in one single request is 1000"; feature list "Access to 10 years of historical market data including 1 sec OHLCV"; no rate limit stated for historical calls — [Breeze-Python-SDK](https://github.com/Idirect-Tech/Breeze-Python-SDK); contradicted on depth by ICICI's own "3 years" — [ICICI FAQ](https://www.icicidirect.com/faqs/fno/is-there-availability-of-f-o-historical-data-with-breeze-api)
- HF dataset: NIFTY, BANKNIFTY, SENSEX; 1-minute; ~2021–2026; `options/{SYMBOL}/{EXPIRY}.parquet`; ~4 GB, ~376.5M rows; CC-BY-NC-4.0; "illiquid/far strikes are often sparse or absent"; "Verify against official exchange data" — [HF dataset card](https://huggingface.co/datasets/thetrademarkk/india-index-options-1m); options folder 1.6 GB, latest expiry files 2026-07-28 (BANKNIFTY), 2026-08-04 (NIFTY), 2026-07-30 (SENSEX) — [HF tree](https://huggingface.co/datasets/thetrademarkk/india-index-options-1m/tree/main/options)
- Dhan rolling-option endpoint `POST https://api.dhan.co/v2/charts/rollingoption`; intervals 1/5/15/25/60; `strike` = ATM or offset; `requiredData` includes `iv`, `oi`, `spot`; "up to the last 5 years"; 30 days per call; strike range ATM±10 for index options near expiry, ATM±3 otherwise — [Dhan docs](https://dhanhq.co/docs/v2/expired-options-data/)
- Dhan Data API ₹499 + taxes per month, renews every 30 days; free-with-trades promo discontinued — [Dhan FAQ](https://dhan.co/support/platforms/dhanhq-api/how-does-the-dhanhq-data-api-subscription-work/), [Dhan FAQ](https://dhan.co/support/platforms/dhanhq-api/is-the-dhanhq-data-api-subscription-free-if-i-execute-a-minimum-number-of-trades-every-month/)
- Groww: Historical Data APIs launched 3 Oct 2025, "from 2020 onwards", 1min–1month, Expiries API, Contracts API — [Groww changelog](https://groww.in/trade-api/docs/curl/changelog); ₹499 + taxes/month, ₹0 plan "excludes live data and backtesting APIs" — [Groww blog](https://groww.in/blog/api-trading-on-groww)
- Kite Connect ₹500/app/month includes historical candles; Personal tier free but no data; from Oct 2026 ₹500 credited back if prior-month brokerage ≥ ₹2,000 — [Zerodha support](https://support.zerodha.com/category/trading-and-markets/kite-api/articles/what-are-the-charges-for-kite-apis); "We do not provide historical data for expired option instruments" (staff, Aug 2025) — [Kite forum](https://kite.trade/forum/discussion/16179/does-100-day-historical-api-include-expired-index-option-candles); "reviewing the feasibility… no timeline" (Zerodha, 21 Sep 2026) — [TradingQnA](https://tradingqna.com/t/historical-expired-options-data/188274)
- Angel One: "We do not provide historical data for expires futures and options contracts as of now" (moderator) — [SmartAPI forum](https://smartapi.angelone.in/topic/2679/how-to-get-historical-data-for-expired-contracts/4); moderator: 100 days of 5-min and 30 days of 1-min per request; users report 500-candle truncation — [SmartAPI forum](https://smartapi.angelone.in/smartapi/forum/post/10902)
- Fyers: "FYERS does not currently provide direct access to historical or expired option chain data" (KB updated Sept 2025) — [Fyers support](https://support.fyers.in/portal/en/kb/articles/can-i-view-expired-contracts-in-fyers)
- 5paisa: "we support Historical Candle data only for live scripts. Expired contracts are not supported" — [5paisa forum](https://tradebetter.5paisa.com/t/how-can-i-get-historic-candles-data-of-options/773)
- Shoonya TPSeries: `POST https://api.shoonya.com/NorenWClientAPI/TPSeries`, intervals 1–240 min, depth and expired support not stated — [Shoonya docs](https://shoonya.com/api-documentation/time-price-series)
- Kotak Neo: "Kotak doesn't provide historical OHLCV" (community reply, May 2026; repo archived) — [GitHub issue](https://github.com/Kotak-Neo/Kotak-neo-api-v2/issues/70)
- Alice Blue: Day & Minute only; data API 17:30–08:00 weekdays; NSE 2 yrs, NFO current-expiry only (third-party client docs) — [NuGet OptionEdge.API.AliceBlue](https://www-0.nuget.org/packages/OptionEdge.API.AliceBlue/1.0.0.4-beta)

### Inferences
- For a ≤ ₹500 one-time budget, the realistic plan is: Breeze (free, fixed-strike 1-min/1-sec, ~3 yrs) as the primary intraday source, cross-checked against the HF 1-min dataset, with NSE bhavcopy as the free EOD ground truth for OI/settlement and for extending history before 2023.
- A single month of Dhan (₹499) is the cheapest way to get IV-tagged minute data for 5 years, and its ATM-relative design maps directly onto a 9:20 ATM straddle (sell "ATM at 09:20" = the strike the API returns at 09:20 — but see the fixed-strike gotcha below).
- Groww at ₹499 for one month gives fixed-contract 1-min candles from 2020 (≈ 6 yrs) — deeper than Breeze — but the 30-day-per-request cap means ~70 requests per contract-year; heavy scripting needed.

### Gaps
- No official ICICI statement that Breeze serves EXPIRED option contracts; evidence is a community package built on it and forum users. Must be tested with one expired expiry before relying on it.
- Breeze history depth conflicts (3 yrs official vs 10 yrs SDK README).
- Groww docs never say "expired" explicitly; inference from the Jan-2024 example.
- Paytm Money, HDFC Sky, Motilal Oswal: no sources found on expired-option history.
- Shoonya depth for options unknown.

## Broker APIs — detail per broker

### Takeaway
Among free-with-account APIs, only Breeze is credibly useful for expired index options at intraday intervals. Dhan and Groww do it for ₹499/month. Zerodha, Angel One, Fyers, 5paisa explicitly do not serve expired options.

### Cited Findings

**ICICI Direct Breeze**
- v2 historical endpoint `GET https://breezeapi.icicidirect.com/api/v2/historicalcharts`; mandatory for options: `product_type="options"`, `expiry_date` (ISO 8601), `right` ("call"/"put"), `strike_price`; `exchange_code` "NFO" (sample also uses `BFO` with `BSESEN`) — [Breeze API docs](https://api.icicidirect.com/breezeapi/documents/index.html)
- Rate limit: 100 calls/min, 5,000 calls/day — [ICICI FAQ](https://www.icicidirect.com/faqs/fno/what-is-the-rate-limit-for-breeze-api); v1 docs state the same — [Breeze API docs](https://api.icicidirect.com/breezeapi/documents/index.html)
- "with Breeze API users can easily fetch 1sec, 1min data for historical backtesting purposes" (example uses `get_historical_data_v2(interval="1second", ...)`) — [ICICI FAQ](https://www.icicidirect.com/faqs/fno/does-breeze-api-allows-fetching-of-1sec-data)
- SDK v2 example for options: `stock_code="NIFTY", exchange_code="NFO", product_type="options", expiry_date="2025-02-06T07:00:00.000Z", right="call", strike_price="23200"`; "does not account for corporate adjusted data" — [Breeze-Python-SDK](https://github.com/Idirect-Tech/Breeze-Python-SDK)
- Community tool `breeze-historical-options`: "historic options data (starting from seconds) using the ICICI Breeze API"; needs only "a free ICICI Direct account"; takes scrip (`CNXBAN` = Bank Nifty), `NFO`, expiry date, start/end datetime, strike range/step, `max_threads`; ships `expiries.json` list of expiry dates — [PyPI](https://pypi.org/project/breeze-historical-options/)
- Forum user: "Breeze gives consistent data but only for last 3 years" — [Upstox community](https://community.upstox.com/t/get-expired-future-option-contract-api-returning-empty-data/14043); forum user: "ICICI Breeze API has it for Nifty and Bank Nifty, free of charge" — [TradingQnA](https://tradingqna.com/t/historical-options-data-for-indices-for-backtesting/174282)
- Stability complaints exist (thread title "Is ICICI Breeze API stable?") — [TradingQnA](https://tradingqna.com/t/is-icici-breeze-api-stable/150332)

**Dhan (DhanHQ v2)**
- Expired options are served via a dedicated endpoint, "not fetched using expired security IDs"; params: expiry type, strike selection, option type, date range — [Dhan FAQ](https://dhan.co/support/platforms/dhanhq-api/do-dhan-provides-expired-options-data-via-the-api-s/)
- Exchanges: NSE index options, NSE stock options, BSE index options, BSE stock options; MCX excluded — [Dhan FAQ](https://dhan.co/support/platforms/dhanhq-api/which-exchanges-support-expired-options-data/)
- Fixed strike NOT trackable: "If the index opens at 25,000, the API initially returns the 25,000 strike. If the index moves to 25,100 and that becomes ATM, the API switches to the 25,100 strike" — [Dhan FAQ](https://dhan.co/support/platforms/dhanhq-api/can-i-fetch-ohlc-data-for-a-fixed-option-strike-throughout-the-entire-trading-session-using-the-rolling-option-data-api/)
- Request fields: `exchangeSegment` (e.g. `NSE_FNO`), `interval` (1/5/15/25/60), `securityId` (underlying), `instrument` (`OPTIDX`), `expiryFlag` (`WEEK`/`MONTH`), `expiryCode`, `strike` (`ATM`, ATM±n), `drvOptionType` (`CALL`/`PUT`), `requiredData` [open,high,low,close,iv,volume,strike,oi,spot], `fromDate`/`toDate` (toDate non-inclusive); response has `ce` and `pe` objects with arrays `iv, oi, strike, spot, open, high, low, close, volume, timestamp` — [Dhan docs](https://dhanhq.co/docs/v2/expired-options-data/)
- Regular intraday endpoint `POST https://api.dhan.co/v2/charts/intraday` (1/5/15/25/60 min, OI flag) covers last 5 years but "active instruments" only; 90 days per poll — [Dhan docs](https://dhanhq.co/docs/v2/historical-data/)
- Expired FUTURES intraday not available via any endpoint; daily continuous only — [Dhan FAQ](https://dhan.co/support/platforms/dhanhq-api/how-can-i-retrieve-data-for-expired-futures-contracts-using-the-apis/)

**Groww Trade API**
- `get_expiries(exchange, underlying_symbol, year[2020..], month)` → dates; `get_contracts(exchange, underlying_symbol, expiry_date)` → Groww symbols; `get_historical_candles(exchange, segment=FNO, groww_symbol, start_time, end_time, candle_interval)` → candles with OHLCV + open interest (FNO only); limits 1/2/3/5-min 30 days, 10/15/30-min 90 days, 1h+ 180 days; "Equities, indices, and FNO data are available from 2020"; "Backtesting APIs only support CASH and FNO segments" — [Groww docs](https://groww.in/trade-api/docs/python-sdk/backtesting)
- Legacy `get_historical_candle_data` (deprecated) had only 3 months of intraday — [Groww docs](https://groww.in/trade-api/docs/python-sdk/historical-data)
- Pricing: ₹499 + taxes monthly or ₹4,999/yr; ₹0 plan excludes backtesting APIs — [Groww blog](https://groww.in/blog/api-trading-on-groww); third-party: "historical OHLC data for backtesting" incl. CE/PE — [Marketcalls](https://www.marketcalls.in/fintech/groww-enters-the-algo-arena-with-powerful-trading-apis.html)

**Zerodha Kite Connect**
- Historical API intervals `minute, day, 3minute, 5minute, 10minute, 15minute, 30minute, 60minute`; `oi=1` flag; `continuous=1` returns day candles of expired FUTURES only; expired instrument tokens cannot be retrieved unless cached — [Kite docs](https://kite.trade/docs/connect/v3/historical/)
- Staff (Aug 2025): "We do not provide historical data for expired option instruments"; expired futures day-level only; suggests recording WebSocket ticks or buying from NSE-authorised vendors — [Kite forum](https://kite.trade/forum/discussion/16179/does-100-day-historical-api-include-expired-index-option-candles)
- Staff timeline: 31 Oct 2025 "no plans"; 9 Mar 2026 "will take some more time"; 21 Sep 2026 "reviewing the feasibility… no timeline" — [TradingQnA](https://tradingqna.com/t/historical-expired-options-data/188274)
- Pricing history: historical add-on charge stopped 8 Feb 2025 — [Kite forum](https://kite.trade/forum/discussion/comment/49067); fee revised ₹2000 → ₹500/month — [Kite forum](https://kite.trade/forum/discussion/comment/49597); current ₹500/app/month, Personal free (no data), brokerage-credit scheme from Oct 2026 — [Zerodha support](https://support.zerodha.com/category/trading-and-markets/kite-api/articles/what-are-the-charges-for-kite-apis)
- Kite web: "historical data for expired options contracts cannot be accessed on Kite" — [Zerodha support](https://support.zerodha.com/category/trading-and-markets/charts-and-orders/charts/articles/historical-data-for-expired-f-o-contract)

**Angel One SmartAPI**
- Free historical data release note exists for indices/NSE/NFO/BSE/BFO/MCX/CDS — [SmartAPI forum](https://smartapi.angelone.in/topic/4012/release-note-free-historical-data-access-for-indices-nse-nfo-bse-bfo-mcx-and-cds-with-smartapi/20)
- "Currently we are not providing the historical data for expired contracts on SmartAPI"; also "This API does not provide Open Interest info for now" — [SmartAPI forum](https://smartapi.angelone.in/smartapi/forum/post/17472), [SmartAPI forum](https://smartapi.angelone.in/topic/2679/how-to-get-historical-data-for-expired-contracts/4)

**Fyers**
- Official KB: no historical/expired option chain data; points to NSE archives — [Fyers support](https://support.fyers.in/portal/en/kb/articles/can-i-view-expired-contracts-in-fyers); staff: "we don't provide the historical expired option data" — [Fyers community](https://fyers.in/community/fyers-api-rha0riqv/post/historical-option-data-for-expired-contracts-not-fetched-mkS4HwdCX44BQjf)

**Others**
- 5paisa: intraday 1-min→1-day, "6 months of historical intraday data", live scrips only — [5paisa forum](https://forum.5paisa.com/portal/en/community/topic/5paisa-developer-apis-update), [5paisa forum](https://tradebetter.5paisa.com/t/how-can-i-get-historic-candles-data-of-options/773)
- Kotak Neo: marketing lists "Historical Data API" — [Kotak Neo bulletin](https://www.kotakneo.com/bulletins/kotak-neo-trade-apis-just-got-more-powerful/); but community says no OHLCV; endpoint `GET {baseUrl}/charts/v1/scrip/history` returned 503 — [GitHub issue](https://github.com/Kotak-Neo/Kotak-neo-api-v2/issues/70)

### Inferences
- A Breeze download of one expiry at 1-min for ATM±10 strikes ≈ 21 contracts × ~375 candles/day × 5 days ≈ 40k candles → ~40 calls at 1000 candles/call; at 100 calls/min and 5000/day you can pull roughly 100+ expiries/day — the whole 3-yr NIFTY weekly history is a few days of polling.
- Dhan's rolling ATM output is ideal for "sell ATM straddle at 09:20 and hold" P&L only if you reconstruct the fixed strike: query `ATM` at 09:20 to learn the strike (response includes `strike`), then for subsequent minutes you need ATM±k where k changes as spot moves — doable because the response carries `strike` and `spot` per bar, but stop-loss logic on a fixed strike becomes a stitching exercise.

### Gaps
- No official Breeze statement on expired-contract availability or on BFO (SENSEX) historical options; SDK mentions BFO only as an exchange code.
- Dhan `expiryCode` enumeration values not documented on the fetched page.
- Groww rate limits not found.

## NSE official data: F&O bhavcopy (UDiFF), bulk download, intraday availability, paid products

### Takeaway
The free NSE F&O bhavcopy gives daily OHLC/Last/Settle/OI/Volume per strike per expiry for every traded contract; URL patterns for both the UDiFF (≥ 8 Jul 2024) and legacy (< 8 Jul 2024, verified back to 2019) formats resolve with a browser User-Agent. NSE publishes nothing free at intraday resolution; its historical trade (tick) data is a paid annual product (₹18k students / ₹90k others per segment, 2022 tariff).

### Cited Findings
- UDiFF F&O URL: `https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_{YYYYMMDD}_F_0000.csv.zip`, from 8 Jul 2024; legacy: `https://nsearchives.nseindia.com/content/historical/DERIVATIVES/{yyyy}/{MMM}/fo{dd}{MMM}{yyyy}bhav.csv.zip`; fallback API `https://www.nseindia.com/api/daily-reports?key=FO` (current/previous day only) — [jugaad-data source](https://raw.githubusercontent.com/jugaad-py/jugaad-data/master/jugaad_data/nse/archives.py)
- Verified by this researcher (curl with Chrome UA, 26 Oct 2026): `BhavCopy_NSE_FO_0_0_0_20251024_F_0000.csv.zip` → HTTP 200, 1.22 MB zip, 37,127 rows; `.../2019/JAN/fo01JAN2019bhav.csv.zip` → HTTP 200 (434 KB); `BhavCopy_NSE_FO_0_0_0_20240708_F_0000.csv.zip` → HTTP 200 (direct observation, no URL)
- UDiFF columns (observed): `TradDt,BizDt,Sgmt,Src,FinInstrmTp,FinInstrmId,ISIN,TckrSymb,SctySrs,XpryDt,FininstrmActlXpryDt,StrkPric,OptnTp,FinInstrmNm,OpnPric,HghPric,LwPric,ClsPric,LastPric,PrvsClsgPric,UndrlygPric,SttlmPric,OpnIntrst,ChngInOpnIntrst,TtlTradgVol,TtlTrfVal,TtlNbOfTxsExctd,SsnId,NewBrdLotQty,...`; index options have `FinInstrmTp=IDO`; sample row `NIFTY25DEC26750CE` open 279.10 high 279.10 low 217.15 close 230.40 OI 11400 (direct observation)
- Legacy columns (observed): `INSTRUMENT,SYMBOL,EXPIRY_DT,STRIKE_PR,OPTION_TYP,OPEN,HIGH,LOW,CLOSE,SETTLE_PR,CONTRACTS,VAL_INLAKH,OPEN_INT,CHG_IN_OI,TIMESTAMP`; `OPTIDX,BANKNIFTY,...` rows; untraded strikes show OPEN/HIGH/LOW = 0 (direct observation)
- Legacy F&O bhavcopy discontinued from 8 Jul 2024, replaced by "F&O-UDiFF Common Bhavcopy Final (zip)" per NSE Circular 62424 (12 Jun 2024) — [NSE all-reports-derivatives](https://www.nseindia.com/all-reports-derivatives); UDiFF specs and sample files — [NSE forms/formats](https://www.nseindia.com/static/resources/forms-formats-members)
- NSE member extranet path for F&O bhavcopy `.DAT` files (`FNO_BCDDMMYYYY.DAT` under `/faoftp/faocommon/Bhavcopy`, w.e.f. 6 Jul 2026) — [NSE circular](https://nsearchives.nseindia.com/content/circulars/MSD76877.pdf) (members only; not relevant to retail)
- Python helpers: `jugaad-data` `bhavcopy_fo_save(date, dir)` (v0.33.1, Mar 2026) — [PyPI](https://pypi.org/project/jugaad-data); `pybhav` `segment="FO"` — [PyPI](https://pypi.org/project/pybhav/); `bhavkit` (DuckDB store; "Zero OHLC values in F&O are legitimate for illiquid strikes"; keep `rate_limit_sleep ≥ 0.3`) — [PyPI](https://pypi.org/project/bhavkit/); `nse` package switched F&O download to UDiFF — [PyPI](https://pypi.org/project/nse/1.0.3); R `nser::fobhav` from 1 Jan 2020 — [CRAN nser](https://search.r-project.org/CRAN/packages/nser/nser.pdf)
- NSE historical trade (tick) data sold via NSE Data & Analytics Ltd (formerly DotEx) — [NSE](https://www.nseindia.com/static/nse-data-and-analytics); 2022 tariff: Historical Trade Data CM and F&O = ₹18,000 (students/researchers) / ₹90,000 (others) per entity location, USD 300/1,500 international — [NSE pricing PDF](https://archives.nseindia.com/content/press/Other_Data_Product_Pricing_effective_Apr012022.pdf); 2024 tariff sheet (per annum) — [NSE tariff PDF](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Download%20Other%20Products%20Tariff%20%28Effective%20April%2001%202024%29_7.pdf)
- Historical vendor quotes (2018, dated): GFDL ₹1,450/month NSE F&O tick; TrueData ₹2,598+GST/month F&O — [TradingQnA](https://tradingqna.com/t/nse-tick-data-best-offer/61580); 2026 forum claim: third-party vendors ₹5,000–₹20,000/month — [TradingQnA](https://tradingqna.com/t/historical-expired-options-data/188274); "about 1500 for each year's data" from an authorised vendor (forum) — [TradingQnA](https://tradingqna.com/t/is-there-a-place-when-we-can-get-intraday-data-for-nifty-options-or-even-index-for-free-preferably-in-csv-format/674)

### Bulk download snippet (verified pattern)
```bash
# UDiFF (>= 2024-07-08)
curl -A "Mozilla/5.0" -o fo_20251024.zip \
  "https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_20251024_F_0000.csv.zip"
# Legacy (< 2024-07-08)
curl -A "Mozilla/5.0" -o fo_01JAN2019.zip \
  "https://nsearchives.nseindia.com/content/historical/DERIVATIVES/2019/JAN/fo01JAN2019bhav.csv.zip"
```
```python
from jugaad_data.nse import bhavcopy_fo_save
from datetime import date
bhavcopy_fo_save(date(2025,10,24), "./bhav")   # handles UDiFF/legacy switch
```

### Inferences
- NSE has no free intraday option-chain history; the "option chain" page is live-only. Any "historical option chain" on niftytrader/opstra-type sites is EOD snapshots.
- Weekday 404s = holidays (bhavkit treats server as authority), so a bulk loop should tolerate 404s.

### Gaps
- Billing period (annual vs one-time) for NSE Historical Trade Data not confirmed from the tariff snippets; the NSE "historical option chain snapshots" product was not found.
- Exact earliest date of the legacy DERIVATIVES archive not verified (2019 verified; packages reference 2000s).

## Open datasets (Kaggle, GitHub, Hugging Face, Drive/Telegram dumps)

### Takeaway
One substantive open dataset exists: Hugging Face `thetrademarkk/india-index-options-1m` (1-min NIFTY/BANKNIFTY/SENSEX options, 2021–2026). No Kaggle dataset of Indian index-option intraday data was found; GitHub repos hold index (not options) minute data or download scripts. Drive/Telegram dumps are typically re-shared vendor data with licensing and quality problems.

### Cited Findings
- HF dataset details: see Ranked table; `index/{SYMBOL}.parquet` spot 1-min + `options/{SYMBOL}/{EXPIRY}.parquet`; BANKNIFTY spot volume shows 0; `open_interest` documented but not visible in viewer — [HF dataset card](https://huggingface.co/datasets/thetrademarkk/india-index-options-1m)
- Kaggle index-only: Nifty Bank 1-min OHLC Jan 2015–Jan 2022, no options — [Kaggle mirror](https://baselight.app/u/kaggle/dataset/debashis74017_nifty_bank_minute_data); Nifty strategy indices daily 2000–2024 — [Kaggle mirror](https://baselight.app/u/kaggle/dataset/visheshgupta2004_nifty_strategy_indices_dataset)
- GitHub `aeron7/nifty-banknifty-intraday-data`: 1-min NIFTY/BANKNIFTY (and some stocks) text files, year folders up to 2023, columns Symbol,Date,Time,O,H,L,C,Volume,OI; no options — [GitHub](https://github.com/aeron7/nifty-banknifty-intraday-data)
- GitHub `ashwanthkumar/kite-history`: Node script downloading 1-min option candles for NIFTY/BANKNIFTY/FINNIFTY via Kite (live contracts only; last push Jun 2021) — [awesome.ecosyste.ms](https://awesome.ecosyste.ms/projects/github.com%2Fashwanthkumar%2Fkite-history)
- Kite forum: 2016–2021 1-min options data offered via Kaggle link (link not shown); another thread says shared data "missing strikes at various times" — [Kite forum](https://kite.trade/forum/discussion/12137/nifty-bank-nifty-futures-options-data), [Kite forum](https://kite.trade/forum/discussion/comment/41566/)
- Licensing: buyer of TrueData options data "not allowed to share"; another user collects own 1-min data since Jan 2024 — [TradingQnA](https://tradingqna.com/t/historical-intraday-data-for-nifty-options-including-iv/82296?page=2), [TradingQnA](https://tradingqna.com/t/is-there-a-place-when-we-can-get-intraday-data-for-nifty-options-or-even-index-for-free-preferably-in-csv-format/674)
- Requests for pendrive / Google-Drive sharing of expired index options data continue (Sep 2026) — [TradingQnA](https://tradingqna.com/t/historical-expired-options-data/188274)

### Inferences
- The HF dataset's licence (CC-BY-NC) permits personal backtesting; its unknown provenance means spot-check against NSE bhavcopy daily OHLC/OI before trusting (e.g., compare 1-min aggregated daily high/low to `HghPric/LwPric`).
- Drive/Telegram dumps are likely redistributed GFDL/TrueData exports (licensing violation) and frequently have missing strikes/expiries.

### Gaps
- Could not search Kaggle directly (JS-rendered); no Indian index-options intraday Kaggle dataset surfaced via web search.
- HF dataset: exact expiry-file count, OI column presence, and whether 2021–2023 SENSEX weeklies are included not verifiable from the tree view.

## Free tiers / trials of paid platforms and vendors

### Takeaway
No platform gives free intraday expired-option history for backtesting beyond short trials: StockMock has a limited free trial, Opstra's free tier excludes backtesting (PRO ~₹1,300/mo), Sensibull has no backtester at all, TrueData offers ~10-day API trials, and Quantman/GDFL trial terms could not be verified.

### Cited Findings
- StockMock: free trial, starting ~$9/month (directory listing); trial lacks day-of-week entry/exit — [SoftwareSuggest](https://www.softwaresuggest.com/stockmock/pricing), [AlgoTest blog (competitor)](https://algotest.in/blog/algotest-vs-stockmock.md)
- Opstra: free Basic (option chain/Greeks 15-min delayed, EOD IV charts, strategy builder ≤2 legs); PRO = backtesting + intraday simulation + skew/surface; free plan tied to Definedge demat — [Strike.money review](https://www.strike.money/reviews/definedge-opstra); PRO ₹1,300/mo, ₹6,000/half-yr, ₹11,000/yr (third-party) — [AlgoTest blog (competitor)](https://algotest.in/blog/algotest-vs-opstra.md)
- Sensibull: Zerodha users get Pro free; others free tier; Pro ₹1,300/mo; "does not offer backtesting or a historical-data options simulator" — [Strike.money](https://www.strike.money/reviews/sensibull), [AlgoTest blog (competitor)](https://algotest.in/blog/sensibull-review-2026-features-pricing-and-who-its-for.md); 7-day trial — [5paisa KB](https://forum.5paisa.com/portal/en/kb/articles/i-just-want-to-check-how-does-sensibull-works-do-you-provide-any-free-trial-version)
- TrueData: "up to 10 days of trial for API integration", paid trial another 10 days; bar sizes tick/1/5/15/30-min/EOD — [TrueData KB](https://feedback.truedata.in/knowledge-base/article/getting-started-with-truedata-market-data-api), [PyPI truedata-ws](https://pypi.org/project/truedata-ws/0.3.8/)
- Quantman: forum says "not free" with "50 backtest credit" allowance (ambiguous) — [TradingQnA](https://tradingqna.com/t/free-tool-or-platform-for-f-o-back-testing/164339); pricing page returned 404 — [quantman.trade/pricing](https://www.quantman.trade/pricing)
- niftytrader.in offers a Bank Nifty options backtesting page (web UI) — [niftytrader](https://www.niftytrader.in/options-trading-backtesting/banknifty)

### Inferences
- Trials are useful only to sanity-check your own backtest results (e.g., run a 9:20 straddle on StockMock trial and compare equity curve shape), not as a data source — none export raw candles.

### Gaps
- GDFL trial terms, MarketDataFeed, iCharts free tiers: no sources found.
- Quantman current pricing/trial not verifiable.

## Python scraping/aggregation libraries

### Takeaway
Libraries (jugaad-data, nsepython, nsedt, openchart, nse) wrap NSE website endpoints: they deliver EOD bhavcopy and live option chains reliably, intraday only for indices/live contracts (openchart), and "historical option chain" only as EOD per-strike series from NSE's archives — not intraday expired-option data.

### Cited Findings
- openchart: "downloading intraday and end-of-day (EOD) historical data from NSE and NFO", timeframes 1-min to monthly, `NSEData().historical(...)`, v0.1.0 Oct 2024 — [Marketcalls](https://www.marketcalls.in/python/introducing-openchart-a-python-library-for-nse-and-nfo-historical-data.html), [piwheels](https://www.piwheels.org/project/openchart)
- nsepython: option chain, ATM strikes, NSE historical data — [PyPI](https://www.pypi.org/project/nsepython/0.0.971/)
- nsedt: `get_historical_option_data(symbol, date range, option type, strike, expiry)` — [PyPI](https://pypi.org/project/nsedt/)
- jugaad-data: `bhavcopy_fo_save` — [PyPI](https://pypi.org/project/jugaad-data)

### Inferences
- openchart relies on NSE's charting backend, which historically serves intraday candles only for currently listed symbols; not a route to expired options.

### Gaps
- No documentation found on openchart's depth for NFO options or whether expired symbols work.

## What can be built from EOD-only bhavcopy and its limits; synthetic intraday repricing

### Takeaway
Bhavcopy supports expiry-to-expiry and close-to-close option-selling backtests (OI/settlement/daily range per strike), but a 9:20 straddle with intraday stop-losses cannot be evaluated from it: entry (09:20 price), per-leg stop hits, and 15:15 exit are all intraday events that daily OHLC cannot locate. Repricing with Black-Scholes from EOD IV plus index minute data is a recognised fallback (used e.g. where expired data is unavailable) but ignores intraday IV crush/spikes and skew changes, so it will systematically mis-estimate stop-loss hits and drawdowns; no study quantifying this error for Indian index options was found.

### Cited Findings
- Bhavcopy fields include daily Open/High/Low/Close/Last/Settle/OI/ChgOI/Volume/UnderlyingPrice per strike (direct observation of UDiFF header, above)
- Forum critique of EOD option backtests: "the option values are at the EOD when you might have exited during the day, at a different price"; counter-view: fixed snapshot acceptable if consistently applied — [EliteTrader](https://elitetrader.com/et/threads/how-to-backtest-this-option-idea.376136/)
- Straddle value ≈ MAD ≈ 0.8σ and "the value of the straddle changes by root time (assuming vol is unchanged)" — heuristic, not validated model — [Moontower](https://moontowermeta.com/a-birdie-asked-how-to-model-a-1-day-option/)
- Synthetic BS pricing from underlying daily series with historical vol substituted for IV ("synthetic-data mode… no real option market data is required") — [Tessl/Vibe-Trading skill](https://tessl.io/registry/skills/github/HKUDS/Vibe-Trading/options-strategy)
- `optionsbt` GitHub project "works well with EOD bhav data" — [optionsbt mirror](https://backiee.wasmer.app/https_github_com/abbazs/optionsbt)
- Interactive Brokers campus article describes reconstructing expired option prices with Black-Scholes because "there is no such provision for expired option contracts" (search-result summary; article not fetched) — [IBKR campus](https://www.interactivebrokers.com/campus/wp-json/wp/v2/posts/117502)
- BS pricing error is larger for OTM options and slightly worse near expiry (Swedish index options study) — [Gothenburg thesis](https://gupea.ub.gu.se/handle/2077/21964); IV higher for shorter maturities, U-shaped smile in Nifty options — [JIBR paper](https://www.doi.org/10.1108/JIBR-12-2013-0103); OTM puts carry higher IV than equidistant calls on Nifty/Bank Nifty — [TrueData blog](https://truedata.in/blog/what-is-volatility-skew-how-to-trade-it)
- 9:20 straddle practice: sell ATM CE+PE at 09:20, per-leg SL (e.g. 35%), exit ~15:15; edge weakened in 2023 as vol fell; stop-market slippage in thin strikes is material — [Marketcalls](https://www.marketcalls.in/futures-and-options/is-the-920-straddle-no-more-working.html), [Marketcalls](https://www.marketcalls.in/futures-and-options/how-the-9-20-intraday-straddlers-are-being-gamed.html); minute-data hobby backtest of a no-SL 9:20 straddle (Dec 2024) — [TradingQnA](https://tradingqna.com/t/reports-of-the-death-of-920-short-straddle-are-greatly-exaggerated/179061); Straddle Lab scans entry-time/SL combos on intraday data — [TradingQnA](https://tradingqna.com/t/straddle-lab-a-visual-way-to-explore-hundreds-of-intraday-options-selling-setups/198597)

### Inferences (what EOD supports vs not)
- Supported from bhavcopy alone: (a) overnight/positional short strangles & iron condors entered at close, exited at close/expiry (use `ClsPric`/`SttlmPric`); (b) daily OI/PCR filters; (c) worst-case intraday range per leg (`HghPric`/`LwPric`) → an upper bound on whether a stop level was touched during the day, but not when, nor whether both legs were touched.
- Not supported: 9:20 entry price (open ≠ 09:20 price), ordering of SL hits between legs, intraday re-entry, 15:15 exit price.
- Synthetic method recipe: for each minute, price = BS(spot_t from index 1-min data, K, T remaining, r, σ) with σ fixed at the prior day's/current day's EOD IV from bhavcopy close. Main error sources: (1) IV intraday path (opening IV spike and expiry-day IV crush not captured → stop-hit frequency understated on expiry days), (2) skew ignored if a single σ is used for both legs (use per-strike EOD IV to reduce), (3) bid-ask/slippage absent, (4) daily IV itself must be back-solved from bhavcopy close with a consistent spot and dividend/rate assumption. Expect directional bias: P&L smoother, drawdowns understated — adequate for ranking strategy variants, not for sizing or drawdown estimation. (Researcher inference; no quantitative study found.)
- Practical hybrid: calibrate the synthetic model on the ~3 years where Breeze/HF real 1-min data exists, measure error on stop-hit counts and max drawdown, then apply to pre-2021 bhavcopy years only if the error is acceptable.

### Gaps
- No academic or practitioner source quantifying the error of EOD-IV + BS repricing vs actual Indian index-option minute prices; no source on intraday IV patterns specific to Nifty/Bank Nifty (only cross-sectional skew/term-structure studies found).
- MarketCalls' 9:20 straddle P&L heatmaps are images; numbers not extractable.
