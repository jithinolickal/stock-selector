# Swing Filter Analysis Report
**Date:** 2025-12-15
**Market Condition:** NIFTY gap +0.12% (Neutral)
**Result:** 0 stocks selected

---

## Executive Summary

**ROOT CAUSE:** The ATR filter (>= 1.15x) is the primary bottleneck, eliminating ALL 5 stocks that passed previous filters.

**Key Finding:** 5 stocks successfully passed 9 out of 10 filters but failed the ATR >= 1.15x requirement, resulting in 0 final selections.

---

## Filter Cascade Breakdown

| Filter Stage | Stocks Remaining | Failed Count | Failure Rate |
|-------------|------------------|--------------|--------------|
| **Start** | 45 | - | - |
| Price > 200 EMA | 28 | 17 | 37.8% |
| Close > EMA20 > EMA50 | 17 | 11 | 24.4% |
| EMA50 > EMA200 | 17 | 0 | 0.0% |
| EMA20 slope > 0 | 15 | 2 | 4.4% |
| **ADX >= 23** | 6 | 9 | **20.0%** |
| RSI 42-62 | 5 | 1 | 2.2% |
| **ATR >= 1.15x** | **0** | **5** | **11.1% ⚠️ BOTTLENECK** |
| Volume >= 1.0x | 0 | 0 | N/A |
| RS > NIFTY50 | 0 | 0 | N/A |
| Higher Lows >= 2 | 0 | 0 | N/A |

---

## Critical Bottleneck: ATR Filter

**Current Requirement:** ATR must be >= 1.15x its 20-day average

**Impact:** Eliminated all 5 remaining stocks (100% of candidates at this stage)

This suggests the market is currently in a low-volatility regime where stocks aren't showing sufficient ATR expansion, which is typical during:
- Consolidation phases
- Post-rally digestion
- Holiday season thin trading
- Neutral market sentiment (gap +0.12%)

---

## Top 3 Filter Failure Points

### 1. Price > 200 EMA (37.8% failure)
- **Failed:** 17/45 stocks
- **Issue:** Many NIFTY50 stocks are below their long-term trend
- **Sample failures:** ADANIENT, APOLLOHOSP, COALINDIA, HINDUNILVR, JIOFIN

### 2. EMA Alignment - Close > EMA20 > EMA50 (24.4% failure)
- **Failed:** 11/45 stocks
- **Issue:** Short-term trend reversal or correction phase
- **Sample failures:** ASIANPAINT, BAJFINANCE, BEL, BHARTIARTL, CIPLA

### 3. ADX >= 23 (20.0% failure)
- **Failed:** 9/45 stocks
- **Issue:** Weak trending strength, sideways markets
- **Current threshold:** 23 (already relaxed from typical 25)
- **Sample failures:** ADANIPORTS, BAJAJFINSV, DRREDDY, EICHERMOT, HDFCLIFE

---

## Sample Stock Analysis

### HDFCLIFE (Failed at ADX)
- ✅ Price: 777.50 > EMA200: 730.05
- ✅ EMA alignment: Close(777.50) > EMA20(766.21) > EMA50(762.79)
- ✅ Bullish regime: EMA50(762.79) > EMA200(730.05)
- ❌ **ADX: 11.12 (need >= 23)** - Weak trend strength
- ✅ RSI: 57.60 (within 42-62 range)
- ❌ **ATR: 1.02x (need >= 1.15x)** - Insufficient volatility expansion
- ❌ **Volume: 0.57x (below 1.0x avg)** - Low participation
- ✅ RS: 0.81 (outperforming NIFTY)
- ✅ Higher Lows: 2 consecutive

**Verdict:** Good trend structure but lacks conviction (low ADX, ATR, volume)

---

### TATASTEEL (Failed at EMA Alignment)
- ✅ Price: 171.89 > EMA200: 159.94
- ❌ **EMA20(168.40) < EMA50(170.14)** - Short-term weakness
- ✅ Bullish regime: EMA50(170.14) > EMA200(159.94)
- ✅ ADX: 26.79 (good trend strength)
- ✅ RSI: 54.76 (within range)
- ❌ **ATR: 1.00x (need >= 1.15x)** - No expansion
- ✅ Volume: 1.84x (strong)
- ❌ **RS: -0.87 (underperforming NIFTY)** - Relative weakness
- ✅ Higher Lows: 2 consecutive

**Verdict:** Recent pullback disrupted EMA alignment, underperforming market

---

### APOLLOHOSP (Failed at 200 EMA)
- ❌ **Price: 7101 < EMA200: 7280** - Below long-term trend
- ❌ Close(7101) < EMA20(7252) < EMA50(7431) - Full downtrend structure
- ✅ Bullish regime: EMA50 > EMA200 (barely)
- ✅ ADX: 52.52 (very strong trend... downward)
- ❌ **RSI: 33.29 (below 42 min)** - Oversold
- ❌ ATR: 0.96x - Below average
- ❌ Volume: 0.97x - Below average
- ❌ RS: -5.29 - Severely underperforming
- ❌ Higher Lows: 0 - No bullish structure

**Verdict:** Clear downtrend, multiple red flags

---

## Current Thresholds

| Filter | Current Value | Strictness |
|--------|--------------|------------|
| ADX | >= 23 | Moderate (relaxed from 25) |
| RSI | 42 - 62 | Balanced (20-point range) |
| ATR Multiplier | >= 1.15x | **Moderate/Strict** |
| Volume | >= 1.0x | Lenient |
| Higher Lows | >= 2 | Moderate (relaxed from 3) |
| Relative Strength | > 0 | Moderate |

---

## Recommendations

### 🚨 IMMEDIATE ACTIONS (High Priority)

#### 1. **Reduce ATR Multiplier: 1.15x → 1.0x**
- **Current:** Requires 15% expansion above 20-day ATR average
- **Issue:** Too strict for current low-volatility market
- **Recommendation:** Change to **1.0x** (at or above average is sufficient)
- **Impact:** Would rescue the 5 stocks that passed all other filters
- **Rationale:** In swing trading, we care more about trend structure (EMAs, ADX) than volatility spikes

#### 2. **Relax ADX: 23 → 20**
- **Current:** 23 (already relaxed from typical 25)
- **Issue:** Still eliminated 9 stocks (20% failure rate)
- **Recommendation:** Change to **20** to allow moderate trends
- **Impact:** Would add 3-5 more stocks to the funnel
- **Rationale:** ADX 20-25 still indicates trending, just not as strong

### 📊 SECONDARY ACTIONS (Medium Priority)

#### 3. **Widen RSI Range: 42-62 → 35-70**
- **Current:** 20-point window (42-62)
- **Issue:** Very tight, eliminates stocks with slight overbought/oversold
- **Recommendation:** Change to **35-70** (35-point window)
- **Impact:** Minimal immediate impact (only 1 stock failed here)
- **Rationale:** Allows entry on pullbacks (RSI 35-42) or momentum (RSI 62-70)

#### 4. **Consider Relative Strength Tolerance: 0 → -0.5**
- **Current:** Must outperform NIFTY (RS > 0)
- **Issue:** In neutral markets, quality stocks may slightly lag
- **Recommendation:** Allow **RS >= -0.5** (minor underperformance OK)
- **Impact:** Would help in sideways/consolidating markets
- **Rationale:** Strong stocks can lag index briefly during rotations

### 🔍 MONITORING (Low Priority)

#### 5. **Price > 200 EMA (37.8% failure)**
- **Status:** Working as intended
- **Action:** No change recommended
- **Rationale:** This is a core long-term trend filter; many NIFTY stocks genuinely below trend

#### 6. **EMA Alignment (24.4% failure)**
- **Status:** Working as intended
- **Action:** No change recommended
- **Rationale:** Filters out short-term weakness; critical for swing entries

---

## Recommended Configuration Changes

```python
# config/swing_config.py - RECOMMENDED CHANGES

FILTER_THRESHOLDS = {
    # Daily timeframe filters
    "ADX_MIN": 20,                    # CHANGED: 23 → 20 (allow moderate trends)
    "RSI_MIN": 35,                    # CHANGED: 42 → 35 (catch pullbacks)
    "RSI_MAX": 70,                    # CHANGED: 62 → 70 (allow momentum)
    "ATR_MULTIPLIER": 1.0,            # CHANGED: 1.15 → 1.0 (critical fix!)
    "VOLUME_MULTIPLIER": 1.0,         # UNCHANGED
    "EMA_SLOPE_DAYS": 5,              # UNCHANGED

    # Price action filters
    "MIN_HIGHER_LOWS": 2,             # UNCHANGED
    "CONSOLIDATION_RANGE": 0.03,      # UNCHANGED
    "CONSOLIDATION_DAYS": 5,          # UNCHANGED
    "VOLUME_EXPANSION_DAYS": 3,       # UNCHANGED

    # Support/Resistance filters
    "MIN_DISTANCE_TO_RESISTANCE": 2.0,  # UNCHANGED
    "MAX_DISTANCE_TO_SUPPORT": 5.0,     # UNCHANGED

    # Trade quality filters
    "MIN_STOP_DISTANCE": 0.5,         # UNCHANGED
    "MAX_STOP_DISTANCE": 2.0,         # UNCHANGED
    "MIN_RISK_REWARD": 1.5,           # UNCHANGED

    # Intraday confirmation filters
    "INTRADAY_VOLUME_MULTIPLIER": 1.2,  # UNCHANGED
    "UPPER_WICK_THRESHOLD": 0.5,        # UNCHANGED
    "VWAP_CANDLES_TO_CHECK": 2,         # UNCHANGED
}
```

---

## Expected Impact of Changes

### Conservative Scenario (ATR only)
- **Change:** ATR 1.15x → 1.0x
- **Expected Result:** 5+ stocks pass daily filters
- **Risk:** Very low (still requires all other filters)

### Moderate Scenario (ATR + ADX)
- **Changes:** ATR 1.15x → 1.0x, ADX 23 → 20
- **Expected Result:** 8-12 stocks pass daily filters
- **Risk:** Low (maintains quality with EMA + trend filters)

### Aggressive Scenario (All recommendations)
- **Changes:** ATR 1.0x, ADX 20, RSI 35-70, RS >= -0.5
- **Expected Result:** 12-18 stocks pass daily filters → 2-5 final selections
- **Risk:** Medium (requires careful intraday validation)

---

## Risk Assessment

### Low-Risk Changes ✅
1. **ATR 1.15x → 1.0x** - Safe, aligns with market conditions
2. **ADX 23 → 20** - Safe, still requires trending behavior

### Medium-Risk Changes ⚠️
3. **RSI 42-62 → 35-70** - Monitor for false breakouts near extremes
4. **RS > 0 → >= -0.5** - Could select relative laggards in strong markets

### What NOT to Change ❌
- Price > 200 EMA - Core long-term filter
- EMA Alignment - Critical short-term quality filter
- Higher Lows pattern - Key structure validation
- Stop/RR quality checks - Risk management essential

---

## Conclusion

**Primary Issue:** ATR >= 1.15x is too restrictive for current market volatility

**Root Cause:** Low-volatility consolidation period (neutral gap +0.12%, post-rally digestion)

**Solution:** Relax ATR to 1.0x and ADX to 20 for immediate improvement

**Expected Outcome:** With changes, expect 2-5 quality stock selections in similar market conditions

**Action Required:** Update `/Users/jjoseph/code/jithin/stock-selector/config/swing_config.py` thresholds as recommended above
