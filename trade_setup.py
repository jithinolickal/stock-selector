"""Trade setup calculator for generating entry, stop loss, and target levels"""

import pandas as pd
from typing import Dict, Optional
from indicators import find_swing_low, calculate_atr


class TradeSetupCalculator:
    """Calculates complete trade setup with entry, stop, and target levels"""

    @staticmethod
    def calculate_setup(
        intraday_df: pd.DataFrame,
        daily_df: pd.DataFrame,
        risk_reward: float = 1.2,
        atr_multiplier: float = 0.7,
    ) -> Optional[Dict]:
        """
        Calculate complete trade setup from intraday data

        Args:
            intraday_df: 15-min DataFrame with indicators
            daily_df: Daily DataFrame (for 15-min ATR calculation)
            risk_reward: Target as multiple of risk (default 1.2)
            atr_multiplier: Stop loss as multiple of ATR (default 0.7)

        Returns:
            Dict with trade setup or None if insufficient data
        """
        if intraday_df.empty or len(intraday_df) < 20:
            return None

        latest = intraday_df.iloc[-1]

        # Current LTP (Last Traded Price)
        ltp = latest["close"]

        # Entry levels (EMAs for pullback)
        ema9 = latest.get("ema_9")
        ema20_intraday = latest.get("ema_20_intraday")

        if pd.isna(ema9) or pd.isna(ema20_intraday):
            return None

        # Calculate stop loss options
        # Option 1: Below swing low
        swing_low = find_swing_low(intraday_df, lookback=10)
        stop_swing = swing_low - (swing_low * 0.001)  # 0.1% below swing low

        # Option 2: ATR-based (using 15-min ATR)
        atr_15min = calculate_atr(intraday_df, period=14)
        if len(atr_15min) > 0 and pd.notna(atr_15min.iloc[-1]):
            atr_value = atr_15min.iloc[-1]
        else:
            atr_value = 0

        # Choose the better stop loss (higher is better for long trades)
        stop_atr = ema9 - (atr_value * atr_multiplier) if atr_value > 0 else None

        if stop_atr and stop_swing:
            stop_loss = max(stop_swing, stop_atr)
            stop_method = "swing_low" if stop_loss == stop_swing else "atr_based"
        elif stop_swing:
            stop_loss = stop_swing
            stop_method = "swing_low"
        elif stop_atr:
            stop_loss = stop_atr
            stop_method = "atr_based"
        else:
            return None

        # Calculate targets for both entry levels
        # Entry at EMA9
        risk_ema9 = ema9 - stop_loss
        target_ema9 = ema9 + (risk_ema9 * risk_reward) if risk_ema9 > 0 else None

        # Entry at EMA20
        risk_ema20 = ema20_intraday - stop_loss
        target_ema20 = ema20_intraday + (risk_ema20 * risk_reward) if risk_ema20 > 0 else None

        return {
            "ltp": ltp,
            "ema9": ema9,
            "ema20": ema20_intraday,
            "stop_loss": stop_loss,
            "stop_method": stop_method,
            "swing_low": swing_low,
            "atr_15min": atr_value,
            "target_ema9": target_ema9,
            "target_ema20": target_ema20,
            "risk_ema9": risk_ema9,
            "risk_ema20": risk_ema20,
            "risk_reward_ratio": risk_reward,
        }

    @staticmethod
    def format_trade_setup(setup: Dict, symbol: str) -> str:
        """
        Format trade setup as readable string

        Args:
            setup: Trade setup dictionary
            symbol: Stock symbol

        Returns:
            Formatted string
        """
        if not setup:
            return "⚠️  Insufficient intraday data for trade setup calculation"

        output = f"\n💰 TRADE SETUP FOR {symbol}:\n"
        output += "─" * 60 + "\n"
        output += f"  Current LTP: ₹{setup['ltp']:.2f}\n\n"

        output += "  📍 ENTRY LEVELS (Wait for pullback):\n"
        output += f"    Option 1 - At EMA9:  ₹{setup['ema9']:.2f}\n"
        output += f"    Option 2 - At EMA20: ₹{setup['ema20']:.2f}\n\n"

        output += "  🛑 STOP LOSS:\n"
        output += f"    Stop: ₹{setup['stop_loss']:.2f} ({setup['stop_method']})\n"
        if setup['stop_method'] == 'swing_low':
            output += f"    (Below swing low: ₹{setup['swing_low']:.2f})\n"
        else:
            output += f"    (Based on ATR: ₹{setup['atr_15min']:.2f})\n"
        output += "\n"

        output += "  🎯 TARGETS:\n"
        if setup['target_ema9']:
            output += f"    If enter at EMA9:  ₹{setup['target_ema9']:.2f} "
            output += f"(Risk: ₹{setup['risk_ema9']:.2f})\n"
        if setup['target_ema20']:
            output += f"    If enter at EMA20: ₹{setup['target_ema20']:.2f} "
            output += f"(Risk: ₹{setup['risk_ema20']:.2f})\n"

        output += f"\n  📊 Risk-Reward Ratio: 1:{setup['risk_reward_ratio']}\n"
        output += "─" * 60

        return output
