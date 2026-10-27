"""1-min microstructure scan: opening minutes, OR liquidity sweeps, square-off minutes."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config

T = lambda s: pd.Timestamp(s).time()
rows, sweeps = [], []
for f in sorted((config.DATA_DIR / "minutes_1").glob("*.parquet")):
    sym = f.stem
    if sym == "NIFTY50":
        continue
    df = pd.read_parquet(f)
    for day, b in df.groupby(df.index.date):
        if len(b) < 300 or b.index[0].time() != T("09:15"):
            continue
        tt = b.index.time
        px = lambda t: b.loc[tt <= T(t), "close"].iloc[-1]
        o = b["open"].iloc[0]
        first = b.iloc[0]
        rows.append(dict(symbol=sym, day=day, open=o, c0915=first["close"], h0915=first["high"], l0915=first["low"], v0915=first["volume"],
                         v_avg=b["volume"].iloc[1:60].mean(), c0916=px("09:16"), c0917=px("09:17"), c0920=px("09:20"), c0930=px("09:30"), c1000=px("10:00"),
                         c1510=px("15:10"), c1515=px("15:15"), c1519=px("15:19"), c1521=px("15:21"), c1524=px("15:24"), c1526=px("15:26"), c1528=px("15:28"), close=b["close"].iloc[-1]))
        # liquidity sweep of the 09:15-09:29 range: within 09:30-11:30, a 1-min low pierces OR low by <=0.1% and closes back above it
        orb = b.loc[tt < T("09:30")]
        hi, lo = orb["high"].max(), orb["low"].min()
        w = b.loc[(tt >= T("09:30")) & (tt <= T("11:30"))]
        for side, cond in (("BUY", (w["low"] < lo) & (w["low"] >= lo * 0.999) & (w["close"] > lo)),
                           ("SELL", (w["high"] > hi) & (w["high"] <= hi * 1.001) & (w["close"] < hi))):
            if cond.any():
                i = np.argmax(cond.values)
                ts = w.index[i]
                after = b.loc[b.index > ts]
                if len(after) < 31:
                    continue
                e = after["open"].iloc[0]
                sgn = 1 if side == "BUY" else -1
                sweeps.append(dict(symbol=sym, day=day, side=side, entry=e, r30=sgn * (after["close"].iloc[29] / e - 1) * 1e4,
                                   r_close=sgn * (after["close"].iloc[-1] / e - 1) * 1e4,
                                   hit_target=((after["high"].iloc[:60] >= hi).any() if side == "BUY" else (after["low"].iloc[:60] <= lo).any()),
                                   hit_stop=((after["low"].iloc[:60] < w["low"].iloc[i]).any() if side == "BUY" else (after["high"].iloc[:60] > w["high"].iloc[i]).any())))
t = pd.DataFrame(rows)
t["oos"] = pd.to_datetime(t.day) >= "2025-01-01"
print(f"{len(t)} symbol-days, {t.symbol.nunique()} symbols (1-min)\n")


def show(label, r, mask=None):
    for oos in (False, True):
        m = (t.oos == oos) & (mask if mask is not None else True)
        rr = r[m]
        print(f"{label:<58} {'OOS' if oos else 'IS '} n={m.sum():>5} mean={rr.mean():>6.1f}bps hit={(rr > 0).mean() * 100:>4.0f}%")


bps = lambda a, c: (t[c] / t[a] - 1) * 1e4
s1 = np.sign(t.c0915 - t.open)
print("--- Opening minute ---")
show("follow 09:15 bar direction -> 09:16->09:20", s1 * bps("c0916", "c0920"))
show("follow 09:15 bar direction -> 09:16->09:30", s1 * bps("c0916", "c0930"))
show("follow 09:15 bar direction -> 09:16->10:00", s1 * bps("c0916", "c1000"))
show("fade 09:15 bar -> 09:16->09:30 | first-bar vol > 3x avg", -s1 * bps("c0916", "c0930"), t.v0915 > 3 * t.v_avg)
show("follow 09:15 bar -> 09:16->09:30 | |bar| > 0.5%", s1 * bps("c0916", "c0930"), (t.c0915 / t.open - 1).abs() > 0.005)
s2 = np.sign(t.c0917 - t.c0915)
show("follow 09:16-09:17 move -> 09:17->09:30", s2 * bps("c0917", "c0930"))
print("--- Square-off minutes ---")
show("15:19->15:21", bps("c1519", "c1521"))
show("15:24->15:26", bps("c1524", "c1526"))
show("15:21->15:28", bps("c1521", "c1528"))
show("15:26->close", bps("c1526", "close"))
d = np.sign(t.c1510 - t.open)
show("against day direction 15:15->15:26 (forced unwind)", -d * bps("c1515", "c1526"))
show("with day direction 15:26->close (rebound)", d * bps("c1526", "close"))
show("fade 15:15->15:26 move over 15:26->close", -np.sign(bps("c1515", "c1526")) * bps("c1526", "close"))
sw = pd.DataFrame(sweeps)
sw["oos"] = pd.to_datetime(sw.day) >= "2025-01-01"
print("\n--- OR liquidity sweep reversal (pierce <=0.1%, close back inside), 09:30-11:30 ---")
for oos in (False, True):
    m = sw[sw.oos == oos]
    print(f"{'OOS' if oos else 'IS '} n={len(m)} r30={m.r30.mean():.1f}bps hit30={(m.r30 > 0).mean() * 100:.0f}%  r_close={m.r_close.mean():.1f}bps  target(OR other side) within 60m={m.hit_target.mean() * 100:.0f}%  stop(sweep low) within 60m={m.hit_stop.mean() * 100:.0f}%")
