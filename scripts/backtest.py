import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
from backtest import engine, report
from data import upstox
from strategy.orb import ORB

p = argparse.ArgumentParser()
p.add_argument("--symbols", nargs="*", default=config.NIFTY50)
p.add_argument("--start")
p.add_argument("--end")
p.add_argument("--rr", type=float, default=1.5)
p.add_argument("--range", type=int, default=15, help="opening range minutes")
p.add_argument("--min-range", type=float, default=0.0)
p.add_argument("--max-range", type=float, default=1.5)
p.add_argument("--rvol", type=float, default=0.0, help="min opening-range relative volume")
p.add_argument("--bvol", type=float, default=0.0, help="breakout bar volume vs range bars")
p.add_argument("--stall", type=int, default=None, help="exit if < --stall-r after N minutes")
p.add_argument("--stall-r", type=float, default=0.0)
a = p.parse_args()

data = {}
for s in a.symbols:
    try:
        data[s] = upstox.load(s)
    except FileNotFoundError:
        print(f"{s}: no data, run scripts/download.py")
strategy = ORB(range_minutes=a.range, rr=a.rr, min_range_pct=a.min_range, max_range_pct=a.max_range,
               min_rvol=a.rvol, breakout_vol_mult=a.bvol, stall_minutes=a.stall, stall_min_r=a.stall_r)
trades = engine.run(data, strategy, a.start, a.end)
print(report.summary(trades))
config.RESULTS_DIR.mkdir(exist_ok=True)
out = config.RESULTS_DIR / f"{strategy.name}_trades.csv"
trades.to_csv(out, index=False)
print(f"\ntrades -> {out}")
