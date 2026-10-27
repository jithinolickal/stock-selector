📌 PROJECT GOAL

Build a Python script that runs daily between 9:30–10:00 AM IST and selects 1–3 high-probability NIFTY50 stocks for 1–3 day swing trades, using rule-based technical filters only.

📌 DATA REQUIREMENTS

Universe: NIFTY50 stocks

Data source: Upstox API

Timeframes:

Daily candles (for trend & filtering)

15-minute candles (for intraday confirmation)

No real-time tick data required

📌 SCRIPT EXECUTION FLOW
STEP 1 — Fetch Data

For each NIFTY50 stock:

Last 100–200 daily candles

Today’s 15-min candles from 9:15 onwards

STEP 2 — DAILY TIMEFRAME FILTERS (MANDATORY)

Only include stocks that satisfy ALL:

1. Price > 200 EMA (long-term trend confirmation)
2. Close > EMA20 > EMA50 (intermediate trend)
3. 50 EMA > 200 EMA (bullish market regime)
4. EMA20 slope positive (last 5 days)
5. ADX(14) > 25 (strong trend, not choppy)
6. RSI(14) between 40 and 65 (allows pullbacks + momentum)
7. ATR(14) ≥ 1.5× its 20-day average (dynamic volatility filter)
8. Current daily volume > 20-day average volume
9. Relative Strength vs NIFTY50 > 0 (outperforming index)


If any condition fails → discard stock.

STEP 3 — INTRADAY CONFIRMATION (15-MIN)

Evaluate candles between 9:30–10:00 AM:

6. Price above intraday VWAP
7. First two 15-min candles hold above VWAP
8. No large upper wick (>50% of candle range)
9. 15-min volume ≥ 1.2 × 20-period average


If intraday confirmation fails → discard stock.

STEP 4 — RANKING (RULE-BASED, NO AI)

Assign score to remaining stocks:

Trend strength (ADX + EMA alignment) → 35%
RSI proximity to 50–60              → 25%
Relative Strength vs NIFTY50        → 15%
Volume expansion                    → 15%
ATR percentage                      → 10%


Sort descending by score.

STEP 5 — OUTPUT

Return top 1–3 stocks with:

{
  "symbol": "",
  "daily_trend": true,
  "above_200ema": true,
  "ADX": value,
  "RSI": value,
  "ATR_ratio": value,
  "relative_strength": value,
  "volume_confirmed": true,
  "intraday_bias": "bullish",
  "final_score": value,
  "entry_reason": "trend + momentum continuation"
}

📌 TRADING RULES (OUTSIDE SCRIPT)

(For human execution)

Entry: Pullback to 9 or 20 EMA on 15-min chart

Stop loss:

Below last 15-min swing low

Or 0.6–0.8 × 15-min ATR

Target:

Fixed 1R–1.3R

Risk per trade: ≤ 0.5% of capital

Max trades/day: 1–2

📌 EXPECTED SYSTEM BEHAVIOR

Some days → zero stocks returned (this is correct behavior)

Average trades/week: 2–4

Expected win rate: 65–75%

Weekly return target: 1–2%

Low drawdowns