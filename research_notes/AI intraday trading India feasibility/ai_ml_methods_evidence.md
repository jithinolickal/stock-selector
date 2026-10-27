# AI / ML Methods for Intraday Equity & Index Trading: Evidence Map (with Indian-market focus)

Scope: which ML approaches have documented, out-of-sample, post-cost edge for intraday equity/index trading; what fails; what the Indian (NSE) literature actually shows. Evidence grades used below: **A** = peer-reviewed/replicated, walk-forward, post-cost, multiple-testing aware; **B** = out-of-sample but missing costs or significance; **C** = in-sample / single split / price-level regression / no trading simulation.

## Q1. Supervised ML on OHLCV/technical features for intraday direction (XGBoost/LightGBM, LSTM, Transformers)

### Takeaway
Best-case peer-reviewed intraday results come from large cross-sectional long-short portfolios (hundreds of stocks, decades of data) and decay sharply post-2010; single-instrument intraday direction models on a few years of minute bars repeatedly show accuracy statistically indistinguishable from the base rate, and in the one rigorous multi-asset cost-aware study only ~12% of assets were profitable per trade after costs.

### Cited Findings
- **Ghosh, Neufeld & Sahoo (2022, Finance Research Letters; arXiv 2004.10178)** — LSTM & random forest predicting open-to-close direction for S&P 500 constituents, 1993–2018, 26 yearly walk-forward test windows, long top-10/short bottom-10. Mean daily return before→after 0.2%/day slippage: LSTM 0.644%→0.444%, RF 0.539%→0.339%. Sharpe before→after costs: LSTM 6.34→4.32, RF 5.20→3.22. Max drawdown ~22% pre-cost, ~39–40% post-cost. Authors describe three sub-periods: strong (dot-com), moderate (2000s), and "deterioration" afterward, attributing decay to wider ML availability; no post-2010 figures given in text; no classification accuracy reported, no commissions/borrow costs, survivorship handling unstated, no significance test. — [ar5iv 2004.10178](https://ar5iv.labs.arxiv.org/html/2004.10178); [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1544612321003202). Grade **B** (walk-forward and slippage, but 10/10 long-short across 500 names is not a retail-feasible setup; shorting constraints and impact ignored).
- **Gaona, Rangel-Madariaga & Uribe (2026, Frontiers in Applied Mathematics and Statistics)** — "Intraday trading strategy selection under transaction costs with machine learning." 40 assets (24 US stocks, 10 FX, 6 crypto), 1-minute bars Jan 2022–Dec 2023, horizons 1–30 min, DT/RF/XGBoost with walk-forward validation, Optuna tuning, precision-weighted F-beta. Average stock precision ~45.35% (recall 33%). With standardized costs (200 pips one-way for stocks), **only 5 of 40 assets (12.5%) had positive average return per trade**; 6 had positive cumulative P&L (TSLA, AAPL, MSFT, BNB, BTC, ETH). XGBoost selected most often (18/40). Authors: "predictive quality did not reliably translate into profit." Deflated Sharpe used only as a diagnostic (one preliminary config: Sharpe 2.08, DSR 0.987). Only one cost level, two years, no regime split. — [Frontiers 2026](https://www.frontiersin.org/journals/applied-mathematics-and-statistics/articles/10.3389/fams.2026.1888767/full). Grade **A-** (cost-aware walk-forward; costs are assumptions not observed spreads).
- **Sequential structure in intraday futures data: LSTM vs gradient boosting on MNQ (arXiv 2605.17724)** — 5-min MNQ bars, 944 trading days 2021–2025, target = session close > 10:30 open + 10 pts, expanding-window walk-forward over 3 OOS periods. Base rate 51.8%; OOS accuracy 50.00–50.89% (GB variants), 50.59% (LSTM). Permutation p-values 0.135 (best GB), 0.515 (LSTM). "No configuration produces statistically significant out-of-sample accuracy above the base rate"; unstable feature importances across folds attributed to noise-fitting; author concludes 4 years of single-instrument 5-min data is insufficient. — [arXiv 2605.17724](https://arxiv.org/abs/2605.17724). Grade **A** (negative result, properly tested).
- **Chen (arXiv 2608.26106), "A Statistical-Finance Benchmark for Same-Day Directional Stock Prediction: Walk-Forward Evidence from SPY"** — daily SPY Feb 1993–Mar 2024, predict same-day close vs prior close using open + 2 lagged prices, expanding-window walk-forward. Last-800-day accuracy: logistic regression 71.09%, RF 61.20%, XGBoost 58.45% (95% CI 54.94–62.08%). Search-result snippet reported long/flat XGBoost Sharpe 3.456 at 0 bps → 3.043 at 5 bps → 2.626 at 10 bps → 1.785 at 20 bps (not visible in abstract; PDF not parseable, so treat as unverified). Author explicitly urges "careful sample-size accounting and limited economic claims." — [arXiv abs](https://arxiv.org/abs/2608.26106). Grade **B** (single author, preprint, no multiple-testing adjustment stated; the "open vs prior close" feature means much of the "same-day" accuracy is the overnight gap already realised at the open).
- **Chinese intraday momentum with XGBoost (MDPI IJFS 2026)** — XGBoost intraday momentum strategy reports Sharpe 3.02 at 6 bps baseline cost; single cost scenario in snippet, not verified in full text. — [MDPI](https://www.mdpi.com/2227-7072/14/2/47). Grade **B/C** (unverified).
- **Gu, Kelly & Xiu (RFS 2020)** — the canonical ML-in-equities result, but **monthly** cross-sectional: value-weighted long-short decile strategy from NN forecasts Sharpe 1.35; S&P 500 timing Sharpe 0.77 vs 0.51 buy-and-hold; trees & NNs best because of nonlinear interactions; dominant predictors are momentum, liquidity, volatility; OLS with 900+ predictors has negative OOS R², penalized models recover ~0.26% monthly R² (secondhand figure). — [NBER w25398](https://www.nber.org/papers/w25398.pdf); [Mirova summary](https://www.research-center.mirova.com/en/research-library/Empirical-Asset-Pricing-via-Machine-Learning). Grade **A** for monthly cross-section; **not** evidence for intraday.
- **2026 Springer review (Discover/Springer "Machine learning in stock market forecasting: a comprehensive review")** — ML/DL models "often improve reported forecasting metrics under controlled experimental conditions, but the evidence does not establish universal real-world superiority"; "leakage and look-ahead effects can inflate apparent predictive performance." — [Springer](https://link.springer.com/article/10.1007/s10791-026-10491-5).
- **"Hidden Leaks in Time Series Forecasting" (arXiv 2512.06932)** — documents the common LSTM flaw of constructing input/output windows before the train/test split, leaking future info into training. — [arXiv](https://arxiv.org/html/2512.06932v1).
- **Nature Humanities & Social Sciences Communications 2025, chart-based DNN** — reported accuracies up to ~97% are "misleading because the models only forecast the next day" and ignore real-world complexities. — [Nature](https://www.nature.com/articles/s41599-025-04761-8).

### Inferences
- The gap between the Ghosh et al. Sharpe (4.3 post-cost) and the MNQ/Frontiers results is explained by (a) breadth (500 names → cross-sectional diversification), (b) 26 years of data, (c) 1990s-era inefficiencies now gone. A retail trader on 1–5 Indian instruments has none of these.
- Direction accuracy in the 52–58% range is what honest intraday studies report; the Frontiers paper shows this does not clear a 400-pip round-trip cost on most stocks. Indian round-trip costs (STT, exchange, GST, stamp, brokerage, slippage) make the hurdle at least as high (cost figures themselves are out of scope here).
- Published accuracy >70% on intraday or daily direction should be treated as a leakage/labeling red flag unless the paper shows walk-forward + significance test.

### Gaps
- No peer-reviewed paper found with a true minute-level Nifty/BankNifty direction model using walk-forward + transaction costs (see Q7).
- Could not parse full text of Chen (2608.26106) to confirm the Sharpe-by-cost table.
- No Transformer-specific intraday equity study with post-cost results surfaced in searches.

## Q2. Deep reinforcement learning trading agents (FinRL, DQN/PPO)

### Takeaway
DRL trading results come overwhelmingly from the FinRL authors' own group, in bull test periods, with admitted sim-to-real gaps; the one Indian RL paper found (Nifty 50, 15-min) reports Sharpe 0.74–1.23 on only 15 test trades over one year. No independent replication showing robust post-cost edge was found.

### Cited Findings
- **FinRL (Liu et al., 2020/2021)** — ensemble strategy reported Sharpe 2.81, 52.61% annual return; authors note the test period "is a bullish market with an annual return of 32.84%" and concede "a simulation-to-reality gap between the testing performance and real-live market performance." — [arXiv 2011.09607](https://arxiv.org/pdf/2011.09607); [arXiv 2111.09395](https://arxiv.org/pdf/2111.09395).
- **Original ensemble paper (Yang et al., 2020)** — ensemble Sharpe 1.30 on 2016–2020 OOS. — [Columbia PDF](https://openfin.engineering.columbia.edu/sites/default/files/content/publications/ensemble.pdf).
- **FinRL-Meta (NeurIPS 2022 D&B)** — says earlier DRL market-simulator works "are difficult to reproduce"; own re-run of ensemble July 2020–Mar 2022 gives Sharpe 1.53 (not independent). — [NeurIPS](https://papers.neurips.cc/paper_files/paper/2022/file/0bf54b80686d2c4dc0808c2e98d430f7-Paper-Datasets_and_Benchmarks.pdf).
- **FinRL Contests 2023–24 (arXiv 2504.02281)** — Ensemble-1 cumulative return 62.60% / Sharpe 1.48 vs plain PPO 63.37% / Sharpe 1.55 (Sep 2022–Oct 2023): ensemble advantage disappears vs best single agent. — [arXiv](https://arxiv.org/html/2504.02281v3).
- **DRL crypto with backtest-overfitting control (arXiv 2209.05559)** — states prior DRL "optimistic backtest profits" may be "a false positive issue due to overfitting"; frames overfitting detection as a hypothesis test, rejects over-fit agents; less-overfit agents had higher return in May–June 2022 test. — [arXiv](https://arxiv.org/abs/2209.05559).
- **2025 comparative DRL analysis (NHSJS, student journal)** — "DRL models are prone to overfitting and fail during structural breaks." — [NHSJS](https://nhsjs.com/2025/comparative-analysis-of-the-effectiveness-of-deep-reinforcement-learning-models-for-trading-in-the-stock-market/). Low-authority source.
- **Indian RL paper: "A Deep Reinforcement Learning Framework for Strategic Indian NIFTY 50 Index Trading" (MDPI *AI* 2025, 6(8):183)** — Nifty 50 15-min OHLC, train Apr 2015–Apr 2024, test May 2024–Apr 2025; DQN/DDQN/Dueling DDQN. DDQN V3: Sharpe 0.7394, 73.33% win rate across **15 test trades**; Dueling DDQN V3: Sharpe 1.2278, "100% win rate" on a small number of trades. — [MDPI](https://www.mdpi.com/2673-2688/6/8/183). Full text 403'd; costs and drawdown unverified. Grade **C/B** (15 trades is statistically meaningless; a 100% win rate is a small-sample artifact).
- **Review of RL in finance (arXiv 2411.12746)** and **RL for quant trading survey (arXiv 2109.13851)** exist for context; neither provides independent post-cost replication. — [arXiv 2411.12746](https://arxiv.org/pdf/2411.12746); [arXiv 2109.13851](https://arxiv.org/pdf/2109.13851).
- Where RL has credible, long-standing evidence is **execution**, not alpha: Nevmyvaka, Feng & Kearns, "Reinforcement Learning for Optimized Trade Execution" (ICML 2006). — [UPenn PDF](https://www.cis.upenn.edu/~mkearns/papers/rlexec.pdf).

### Inferences
- DRL for intraday alpha at retail scale has no grade-A evidence; the reward-shaping, sample-inefficiency and non-stationarity problems are acknowledged by the FinRL authors themselves.
- DRL results that beat buy-and-hold in bull periods with ≤20 trades should be treated as uninformative.

### Gaps
- No independent (non-FinRL-affiliated) replication reporting FinRL ensemble failure in 2022–23 was found; equally, none confirming success.
- No BankNifty RL paper found.

## Q3. LLM / NLP sentiment trading (news, X/Twitter, Moneycontrol, earnings calls)

### Takeaway
Lopez-Lira & Tang's headline result is real but: the ~90% hit rate is on the *non-tradable* initial reaction, drift returns are concentrated in small stocks and negative news, cumulative return collapses from 350% to 50% going from 10 to 25 bps/trade, and the authors themselves report returns declining as LLM adoption rises; Indian social-sentiment studies show correlation but mostly no causal/predictive power at useful horizons.

### Cited Findings
- **Lopez-Lira & Tang (2023–2026 versions), "Can ChatGPT Forecast Stock Price Movements?"** — GPT-4 on headlines post-knowledge-cutoff (sample Oct 2021–May 2024 per later version): captures initial price response with ~90% portfolio-day hit rate (non-tradable), also predicts subsequent drift, "stronger for small stocks and negative news"; "strategy returns decline as LLM adoption rises"; at 10 bps (25 bps) per trade cumulative return 350% (50%). Replication package on Mendeley. — [arXiv 2304.07619](https://arxiv.org/abs/2304.07619); [Mendeley replication package](https://data.mendeley.com/datasets/f39x226htv/2); [Lancaster PDF](http://wp.lancs.ac.uk/fofi2024/files/2024/04/FoFI-2024-139-Alejandro-Lopez-Lira.pdf).
- **Glasserman & Lin (JFDS Winter 2024; arXiv 2309.17322), "Assessing Look-Ahead Bias in Stock Return Predictions Generated by GPT Sentiment Analysis"** — identifies look-ahead bias and a "distraction effect"; anonymizing company names in headlines *improved* performance within the training window, implying GPT's company knowledge distracts more than it leaks, but both are validity threats. — [SSRN 4586726](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4586726); [PM Research](https://www.pm-research.com/content/iijjfds/6/1/25).
- **Sarkar & Vafa (2024)** on lookahead bias in pretrained LMs is cited by Lopez-Lira & Tang as evidence one must use post-cutoff samples; I could not retrieve the paper itself. — cited in [arXiv 2609.20554](https://arxiv.org/pdf/2609.20554).
- **Look-Ahead-Bench (arXiv 2601.13770)** and **"Detecting Lookahead Bias in LLM Forecasts" (arXiv 2512.23847)** — benchmarks confirming point-in-time LLMs leak future knowledge. — [arXiv 2601.13770](https://arxiv.org/pdf/2601.13770); [arXiv 2512.23847](https://arxiv.org/pdf/2512.23847).
- **Chen, Green, Gulen & Zhou, "What Does ChatGPT Make of Historical Stock Returns?" (arXiv 2409.11540; AEA 2026)** — LLM return forecasts over-extrapolate trends where actual returns reverse, are over-optimistic, and have too-narrow confidence intervals; "LLMs manifest common behavioral biases." — [arXiv 2409.11540](https://www.arxiv.org/abs/2409.11540).
- **"The New Quant" LLM-trading survey (arXiv 2510.05533)** — "many studies report accuracy or correlation without a trading grade evaluation"; latent knowledge "can leak into answers" even without future documents. — [arXiv](https://arxiv.org/pdf/2510.05533).
- **Indian sentiment studies:**
  - VADER on #SBI tweets 2021–2024: sentiment predicted daily direction ~60%; negative sentiment correlation significant, positive weaker (Bangladesh Journal of Multidisciplinary Scientific Research, 2024). — [ResearchGate](https://www.researchgate.net/publication/384106488_VADER_SENTIMENT_ANALYSIS_ON_TWITTER_PREDICTING_PRICE_TRENDS_AND_DAILY_RETURNS_IN_INDIA'S_STOCK_MARKET). Grade **C** (single stock, no trading sim).
  - Saini & Bodla (2024, SAGE) financial-community tweets 2015–2022: correlation with market but "no dynamic or causal relationship." — [SAGE](https://journals.sagepub.com/doi/10.1177/23210222241289700).
  - Tweets vs Nifty 50 hourly returns, Jan 2023: "low positive correlation." — [RS Publication IJRMF](https://rspublication.com/IJRMF/2026/e1/15.pdf). Grade **C**.
  - 7.4M posts (X, Reddit, Indian forums) 2018–2024: sentiment Granger-causes Nifty 50 returns and volatility (Zenodo preprint, unreviewed). — [Zenodo](https://zenodo.org/records/18770670).
  - Nifty 500 investor-sentiment index (seven proxies, Cogent Economics & Finance 2024): significant positive sentiment effect on returns — a macro, not intraday, result. — [T&F](https://www.tandfonline.com/doi/full/10.1080/23322039.2024.2303896).

### Inferences
- The tradable part of LLM-news edge is post-announcement drift in small/illiquid names, which on NSE means names where impact and circuit limits bite, not Nifty/BankNifty. Index-level intraday sentiment edge has no supporting evidence.
- Latency: the ~90% hit rate is on the initial jump — i.e., prices move before a retail pipeline (API call → LLM → order) can act. No source quantified this latency gap for India.
- Indian-language/Moneycontrol-specific NLP: no study found.

### Gaps
- No Indian earnings-call or Moneycontrol NLP trading study found.
- Lopez-Lira & Tang headline Sharpe figures not extracted (PDFs not parseable).

## Q4. Where ML is more credibly useful: regime detection, volatility forecasting, cross-sectional ranking, sizing, execution, meta-labeling/filtering

### Takeaway
The best-supported uses are (i) volatility forecasting (ML/HAR beats plain GARCH on realized-vol inputs, with hybrids best), (ii) cross-sectional ranking at monthly horizon (Gu-Kelly-Xiu), (iii) RL/ML for execution, and (iv) meta-labeling as a *precision filter* on an existing rule — but the largest reproduction study finds meta-labeling does **not** produce a deflated-Sharpe edge at scale; HMM regime detection shows modest, benchmark-dependent gains.

### Cited Findings
- **Meta-labeling reproduction (Daru Finance, 42 instruments: 27 crypto perps, 7 US equity ETFs, 8 FX; EMA-crossover primary, triple-barrier labels):** median precision lift +5–6 pp; profit factor improved in 38/42, DSR in 39/42; instruments with PF>1 went 12→24. But **none of 42 cleared DSR>0.95**; US-equity Sharpe −0.68→+0.31, PF 0.75→1.03; PBO 0.38–0.41. At scale (154 configs) median PF 0.967→0.986, pooled meta-strategy DSR 0.0, PF 0.98 over 14,725 OOS trades. Verdict: "a precision filter, not an alpha source." Purged CV: leakage inflation sub-2 pp AUC, but CPCV path dispersion (~15 pp accuracy range on BTC) is ~50× the leakage bias — a single split is a weak basis. — [Daru Finance](https://daru.finance/research-review/lopez-de-prado/labeling-and-cross-validation). Grade **A-** (independent, deflated, but crypto-heavy).
- **Singh & Joubert (Hudson & Thames), "Does Meta-Labeling Add to Signal Efficacy?"** — reports improvement from event sampling + triple-barrier + meta-labeling; vendor-affiliated. — [PDF](https://hudsonthames.org/wp-content/uploads/2022/04/Does-Meta-Labeling-Add-to-Signal-Efficacy.pdf).
- **QuantConnect forum, "Why Meta-Labeling Is Not a Silver Bullet"** — only fits high-recall primaries; don't reuse model confidence directly as position size. — [QuantConnect](https://www.quantconnect.com/forum/discussion/14706/why-meta-labeling-is-not-a-silver-bullet/).
- **Ernest Chan (PredictNow.ai) view** — pure ML alpha-finding "unproductive so far"; useful for flagging factors that could derail a trade (deciding when *not* to trade) and classifying regimes; momentum more predictable in low-vol regimes, mean reversion struggles when vol fluctuates. — [Algo Advantage 032](https://algoadvantage.substack.com/p/032-dr-ernest-chan-the-breakthrough); [Better System Trader 192](https://bettersystemtrader.com/192-predicting-profitability-using-machine-learning-ernie-chan/). Secondary summaries, not primary text.
- **HMM regime detection:**
  - Wang, Lin & Mikhelson (JRFM 2020), HMM on S&P 500 ETF, OOS Sep 2017–Apr 2020: regime-switched factor strategy beats each single factor; Sharpe not confirmed. — [MDPI](https://www.mdpi.com/1911-8074/13/12/311).
  - Asian indices (Thai journal), 3-state Gaussian HMM frozen Jan 2022, 4-yr OOS: hybrid rule beats buy-and-hold on Sharpe in 3 of 5 markets (Nikkei 0.71 vs 0.47; STI 0.84 vs 0.53). — [TCI-Thaijo](https://so09.tci-thaijo.org/index.php/PMR/article/view/10023).
  - HMM + RL allocation (arXiv 2605.27848): HMM rotations Sharpe 0.79–0.82 vs SPY 0.65 but ≈ equal-weight 0.83 — gain not separable from diversification. — [arXiv](https://arxiv.org/pdf/2605.27848).
  - Statistical jump models beat HMM on Sharpe/vol/drawdown OOS (arXiv 2402.05272). — [arXiv](https://arxiv.org/html/2402.05272v2).
- **Volatility forecasting:**
  - Energy markets: ML beats GARCH OOS on RMSE/MAE for most commodities; ML under-predicts, GARCH over-predicts → hybrid recommended. — [arXiv 2405.19849](https://arxiv.org/html/2405.19849v1).
  - Computational Economics 2024: DL beats GARCH-type in many scenarios but winner depends on train/test ratio, loss, RV formula; GARCH best with 5-min RV. — [Springer](https://link.springer.com/article/10.1007/s10614-024-10694-2).
  - "Volatility forecasting with machine learning and intraday commonality" (arXiv 2202.08962) — ML with cross-asset intraday features improves RV forecasts. — [arXiv](https://arxiv.org/pdf/2202.08962).
  - Time-series foundation models vs econometric RV benchmarks (arXiv 2607.05291). — [arXiv](https://arxiv.org/pdf/2607.05291).
  - India: Christ University 2026 (GARCH vs RF vs LSTM on Nifty returns): GARCH strong for conditional vol, RF/LSTM capture fluctuations better, combination best. — [Christ archive](https://archives.christuniversity.in/items/show/26568). IEEE MysuruCon 2022: on 3 NSE sector stocks LSTM better for pharma, E-GARCH for banking, GJR-GARCH for IT. — [search snippet; see IIM-A 2003 GARCH/EGARCH vs 5-min realized vol on Nifty](https://www.iima.ac.in/hindi/node/16918).
- **Cross-sectional ranking:** Gu-Kelly-Xiu (Q1) — long-short decile Sharpe 1.35 monthly. — [NBER](https://www.nber.org/papers/w25398.pdf).
- **Execution:** Nevmyvaka/Feng/Kearns RL execution (ICML 2006). — [UPenn](https://www.cis.upenn.edu/~mkearns/papers/rlexec.pdf).
- **Bailey & López de Prado DSR / PBO** as the tooling for validating any of the above (see Q5).

### Inferences
- For a retail intraday system, the defensible ML roles are: (1) vol/regime gate that turns a rule-based strategy off (Chan's "when not to trade"), (2) a meta-label filter on a primary rule that already has positive expectancy (it cannot rescue a losing primary — Daru: PF 0.75→1.03 is still ~breakeven after deflation), (3) vol forecast for position sizing. None of these are an alpha source by themselves.
- Signal ranking across a universe is well-evidenced only at monthly horizon; no intraday Indian cross-sectional study found.

### Gaps
- No Indian-market meta-labeling or regime-gating study found.
- No study quantifying ML position-sizing benefit intraday found (Kelly/vol-targeting literature not searched here).

## Q5. Known failure modes

### Takeaway
The dominant, documented failure modes are backtest overfitting via multiple trials (DSR/PBO), CV leakage in time series, look-ahead (incl. LLM knowledge leakage), next-day/price-level targets that inflate accuracy, and "accuracy >50% but unprofitable after costs" — the Frontiers 2026 study is a direct demonstration of the last.

### Cited Findings
- **Deflated Sharpe Ratio (Bailey & López de Prado, JPM 2014)** — corrects for selection bias under multiple testing and non-normal returns; raises the Sharpe benchmark to reflect all trials. — [SSRN 2460551](https://papers.ssrn.com/abstract=2460551).
- **Probability of Backtest Overfitting (Bailey, Borwein, López de Prado, Zhu; J. Computational Finance)** — CSCV estimates probability the IS-best strategy is in the OOS bottom half; needs full trial record. — [SSRN 2326253](https://papers.ssrn.com/abstract=2326253); [eScholarship PDF](https://escholarship.org/content/qt2329p290/qt2329p290.pdf).
- **López de Prado, "The 10 Reasons Most Machine Learning Funds Fail" (JPM 2018; earlier 7-reason SSRN version)** — Sisyphus paradigm (siloed researchers), integer differentiation, inefficient sampling, wrong labeling, weighting non-IID samples, CV leakage, backtest overfitting; the common mistake: "take some data, run it through an ML algorithm, backtest the predictions, and repeat ... until a nice-looking backtest shows up." — [GARP white paper](https://www.garp.org/white-paper/the-10-reasons-most-machine-learning-funds-fail); [Quantpedia summary](https://quantpedia.com/why-machine-learning-funds-fail/); [Oxford Business Law Blog](https://blogs.law.ox.ac.uk/business-law-blog/blog/2018/03/machine-learning-funds-and-investment-malpractice).
- **Accuracy without profit:** Frontiers 2026 — precision ~45–52% across 40 assets, only 12.5% profitable per trade after costs. — [Frontiers](https://www.frontiersin.org/journals/applied-mathematics-and-statistics/articles/10.3389/fams.2026.1888767/full).
- **Noise-fitting signature:** MNQ study — unstable feature importances across folds + p>0.1. — [arXiv 2605.17724](https://arxiv.org/abs/2605.17724).
- **Time-series CV leakage:** "Hidden Leaks" (arXiv 2512.06932); Daru: leaky k-fold inflates AUC up to +1.69 pp but path dispersion dwarfs it. — [arXiv](https://arxiv.org/html/2512.06932v1); [Daru](https://daru.finance/research-review/lopez-de-prado/labeling-and-cross-validation).
- **Look-ahead in fundamentals/data timestamps:** recorded date reflects calculation, not availability. — [arXiv 2512.16251](https://arxiv.org/pdf/2512.16251).
- **LLM look-ahead:** Glasserman & Lin; Look-Ahead-Bench; "Does Training on Future Data Pay?" (arXiv 2609.20554). — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4586726); [arXiv 2601.13770](https://arxiv.org/pdf/2601.13770); [arXiv 2609.20554](https://arxiv.org/pdf/2609.20554).
- **Inflated accuracy from next-day/price-level targets:** Nature HSSC 2025 (97% "accuracy" critique). — [Nature](https://www.nature.com/articles/s41599-025-04761-8).
- **Regime change / alpha decay:** Ghosh et al. document deterioration post-2008; Lopez-Lira & Tang report returns declining with LLM adoption. — [ar5iv](https://ar5iv.labs.arxiv.org/html/2004.10178); [arXiv 2304.07619](https://arxiv.org/abs/2304.07619).
- **Rob Carver**: window lengths most traders use are "far too short to give statistically meaningful results"; averaging rule variations beats picking the single best in walk-forward; strong skepticism of "data-first" (data in → rules out) approaches and of LLM use in systematic trading. — [Better System Trader 026](https://bettersystemtrader.com/026-robert-carver/); [Top Traders Unplugged, "AI Hype"](https://www.toptradersunplugged.com/podcast/the-ai-hype-within-investing-a-step-too-far-ft-rob-carver/).

### Inferences
- Any Indian retail ML backtest should report: number of trials, DSR, PBO (CSCV), purged/embargoed walk-forward, cost sensitivity at ≥3 levels, and trade count. Nearly all Indian papers found report none of these (Q7).
- Survivorship bias is a specific Indian risk: Nifty constituent churn and delistings; no study found that uses point-in-time NSE constituents.

### Gaps
- Could not retrieve the full 10-reason list text (GARP PDF not fetched).
- r/algotrading and Quant StackExchange content could not be searched (reddit.com blocks the crawler; no SE results surfaced).

## Q6. Practitioner consensus (López de Prado, Chan, Carver, QuantConnect, r/algotrading)

### Takeaway
Across López de Prado, Chan and Carver the consistent line is: ML for *finding* alpha from price data mostly fails; ML is defensible for risk/regime filtering, labeling/structuring (triple-barrier, meta-labeling), and validation (DSR/PBO); simple, averaged rules with long histories beat optimized ML on short windows.

### Cited Findings
- López de Prado: ML funds fail from methodological errors, not lack of ML power; advocates assembly-line research org, fractional differentiation, purged CV, meta-labeling, DSR. — [GARP](https://www.garp.org/white-paper/the-10-reasons-most-machine-learning-funds-fail); [CXO Advisory](https://www.cxoadvisory.com/big-ideas/10-steps-to-becoming-a-better-quant).
- Chan: ML alpha "unproductive so far"; ML as risk-management/regime classifier; "deciding when not to trade." — [Algo Advantage 032](https://algoadvantage.substack.com/p/032-dr-ernest-chan-the-breakthrough); [IBKR Campus](https://www.interactivebrokers.com/campus/ibkr-quant-news/algo-advantage-032-dr-ernest-chan-the-breakthrough-uses-of-machine-learning-in-risk-management/). Goodreads reviewers call the ML chapter of *Machine Trading* shallow. — [Goodreads](https://www.goodreads.com/book/show/33650313-machine-trading).
- Carver: self-described "strong bias against the use of big data and AI in financial markets"; "most users of these sophisticated tools have no idea what they're doing"; prefers rules-first, long-window, averaged systems. — [Top Traders Unplugged](https://www.toptradersunplugged.com/podcast/the-ai-hype-within-investing-a-step-too-far-ft-rob-carver/); [Better System Trader 026](https://bettersystemtrader.com/026-robert-carver/).
- QuantConnect community: meta-labeling not a silver bullet; requires high-recall primary. — [QuantConnect](https://www.quantconnect.com/forum/discussion/14706/why-meta-labeling-is-not-a-silver-bullet/).
- Quantpedia summary of LdP: the 7 errors list. — [Quantpedia](https://quantpedia.com/why-machine-learning-funds-fail/).

### Inferences
- Consensus maps cleanly onto the evidence in Q1–Q4: ML helps where the label is well-defined and stationary-ish (vol, execution, filtering) and hurts where it's asked to find direction from a short price history.

### Gaps
- r/algotrading threads not retrievable (crawler blocked). Quantopian post-mortems not found in searches.

## Q7. Indian-market ML studies: what exists and how good it is

### Takeaway
Indian Nifty/BankNifty ML papers are almost entirely daily-frequency, price-level regression (RMSE/MAPE) or small-sample classification, published in MDPI/Springer-conference/Taylor & Francis-applied venues, with no transaction costs, no walk-forward, and no multiple-testing control; the single intraday RL paper has 15 test trades. None constitutes evidence of intraday edge.

### Cited Findings
- **"Stock Market Prediction of NIFTY 50 Index Applying Machine Learning Techniques" (Applied Artificial Intelligence, T&F 2022)** — RNN vs LSTM vs CNN on Nifty 50 returns, historical data only; full text 403'd so metrics unverified. — [T&F](https://www.tandfonline.com/doi/full/10.1080/08839514.2022.2111134). Grade **C** (pending).
- **Sisodia et al. (IEEE conf. 2022), LSTM on Nifty 50 2011–2021** — claims 83.88% accuracy; no comparison to other methods; daily. — [ResearchGate](https://www.researchgate.net/publication/360038159_Stock_Market_Analysis_and_Prediction_for_Nifty50_using_LSTM_Deep_Learning_Approach). Grade **C**.
- **Backward elimination + LSTM for Nifty 50 close (MDPI JRFM 2023, 16(10):423)** — 30-day-ahead price level forecast; full text 403'd. — [MDPI](https://www.mdpi.com/1911-8074/16/10/423). Grade **C** (price-level regression).
- **Mehtab & Sen (arXiv 2009.10819, 2001.09769)** — LSTM/CNN on Nifty 50; authors state it is "not addressing short-term forecasting of interest to intra-day traders" — weekly horizon. — [arXiv 2009.10819](https://arxiv.org/pdf/2009.10819); [arXiv 2001.09769](https://arxiv.org/pdf/2001.09769). Grade **C** for intraday purposes.
- **"Hyper Parameterized LSTM Models for Predicting NSE Intraday Bias Based on Global Market Trends" (Springer LNNS 2023)** — predicts NSE intraday *bias* from overnight global market patterns, not from Nifty's own intraday series; no metrics in abstract. — [Springer](https://link.springer.com/chapter/10.1007/978-981-99-3478-2_13). Grade **C**.
- **LSTM for Nifty Midcap 50 (Springer 2025)** — daily index forecasting. — [Springer](https://link.springer.com/chapter/10.1007/978-981-96-5955-5_22). Grade **C**.
- **Nifty 50 DRL (MDPI AI 2025)** — the only intraday (15-min) Indian paper found; 15 test trades, Sharpe 0.74–1.23. — [MDPI](https://www.mdpi.com/2673-2688/6/8/183). Grade **C/B**.
- **"Bank Nifty: Study of Stock Price Predictions using ML and Sentiment Analysis" (ResearchGate 2025)** — survey-style; frequency/results not visible. — [ResearchGate](https://www.researchgate.net/publication/390422199_Bank_Nifty_Study_of_Stock_Price_Predictions_using_Machine_Learning_and_Sentiment_Analysis). Grade **C**.
- **Kumar, Kotal, Bhattad, "Machine Learning for Nifty Trading" (SSRN 4293548)** — daily OHLC Nifty derivatives, ML/DL + news sentiment + risk layer; daily not intraday. — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4293548). Grade **C/B**.
- **Indian sentiment studies** — see Q3 (correlation yes, causal/predictive mostly no).
- **Indian volatility studies** — see Q4 (GARCH competitive; hybrids best; mostly stock-level).

### Inferences
- The Indian academic literature does not contain a single study that would pass the Q5 checklist (walk-forward + costs + DSR/PBO + adequate trade count) for intraday Nifty/BankNifty. Anyone building such a system is in uncharted territory relative to published evidence and must generate their own validation.
- Because Indian studies are predominantly price-level regression with high R², their reported "accuracy" is not comparable to direction-accuracy numbers and should not be used to size expectations.

### Gaps
- Several Indian paper full texts returned HTTP 403 (T&F, MDPI); metrics taken from abstracts/snippets.
- No IIT/IIM intraday ML trading paper with costs surfaced; IIM-A (2003) and IIM-C working papers found are econometric volatility studies.
- Kaggle NSE dataset quality not assessed (not surfaced in searches).
- Transaction-cost structure for Indian intraday (STT, etc.) is out of this researcher's scope; no cost-adjusted Indian ML backtest was found to cite.
