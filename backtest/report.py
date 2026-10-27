import pandas as pd

import config

SHOCK_DAYS = ["2024-06-04", "2024-08-05", "2025-04-07"]


def metrics(trades: pd.DataFrame) -> dict:
    if trades.empty:
        return {"trades": 0}
    daily = trades.groupby("day")["net"].sum()
    equity = daily.cumsum()
    wins, losses = trades[trades.net > 0], trades[trades.net <= 0]
    months = max(1, pd.to_datetime(daily.index).to_period("M").nunique())
    return {
        "trades": len(trades),
        "per_day": round(len(trades) / daily.index.nunique(), 2),
        "win_rate": round(len(wins) / len(trades) * 100, 1),
        "avg_r": round(trades.r.mean(), 3),
        "pf": round(wins.net.sum() / abs(losses.net.sum()), 2) if len(losses) and losses.net.sum() else float("inf"),
        "net": round(trades.net.sum()),
        "pct_per_month": round(trades.net.sum() / config.CAPITAL * 100 / months, 2),
        "net_per_share": round((trades.net / trades.qty).mean(), 2),
        "max_dd_pct": round((equity - equity.cummax()).min() / config.CAPITAL * 100, 1),
        "cost_pct_of_gross": round(trades.cost.sum() / abs(trades.gross.sum()) * 100) if trades.gross.sum() else None,
    }


def summary(trades: pd.DataFrame) -> str:
    if trades.empty:
        return "no trades"
    m = metrics(trades)
    daily = trades.groupby("day")["net"].sum()
    monthly = daily.groupby(pd.to_datetime(daily.index).to_period("M")).sum()
    shock = daily[daily.index.astype(str).isin(SHOCK_DAYS)]
    lines = [f"{k:<20}{v}" for k, v in m.items()]
    lines += [f"{'exits':<20}{trades.exit_reason.value_counts().to_dict()}", "", "monthly net:", monthly.round(0).to_string(), "",
              "shock days: " + (repr(shock.round(0).to_dict()) if len(shock) else "no trades")]
    return "\n".join(lines)
