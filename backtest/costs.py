"""Upstox intraday equity (MIS) charges, 2026 tariff."""

BROKERAGE_MAX = 20.0          # per order, or 0.05% whichever lower
BROKERAGE_PCT = 0.0005
STT_SELL = 0.00025            # intraday: sell side only
EXCHANGE = 0.0000307          # NSE, both sides
SEBI = 0.000001               # Rs 10 / crore, both sides
STAMP_BUY = 0.00003           # buy side only
GST = 0.18                    # on brokerage + exchange + sebi


def round_trip(buy_value: float, sell_value: float) -> float:
    brokerage = min(BROKERAGE_MAX, buy_value * BROKERAGE_PCT) + min(BROKERAGE_MAX, sell_value * BROKERAGE_PCT)
    turnover = buy_value + sell_value
    exchange = turnover * EXCHANGE
    sebi = turnover * SEBI
    stt = sell_value * STT_SELL
    stamp = buy_value * STAMP_BUY
    gst = (brokerage + exchange + sebi) * GST
    return round(brokerage + exchange + sebi + stt + stamp + gst, 2)
