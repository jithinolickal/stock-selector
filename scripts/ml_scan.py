"""Does an ML model over symbol-day features find any conditional intraday edge?
Train 2022-2024, test 2025-2026. Reports mean forward return (bps) of the most
confident predictions vs friction. Gradient boosting, no tuning on the test set."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config

t = pd.read_parquet(config.RESULTS_DIR / "scan.parquet").sort_values(["symbol", "day"])
g = t.groupby("symbol")
t["ret_5d"] = g.prev_close.pct_change(5)
t["vol_20d"] = g.prev_close.pct_change().rolling(20).std().reset_index(level=0, drop=True)
t["rng_15_rel"] = t.rng_15 / t.vol_20d
t["dow"] = pd.to_datetime(t.day).dt.day_of_week
t["r_15_rel"] = t.r_15 - t.n_r15
t["gap_rel"] = t.gap - t.n_gap
t["r15_sign_agree"] = (np.sign(t.r_15) == np.sign(t.n_r15)).astype(int)
t = t.dropna()
FEATS = ["gap", "r_15", "rng_15", "rvol_15", "prev_ret", "n_r15", "n_gap", "ret_5d", "vol_20d", "rng_15_rel", "dow", "r_15_rel", "gap_rel", "r15_sign_agree"]
tr, te = t[~t.oos], t[t.oos]
print(f"train {len(tr)} rows (2022-24), test {len(te)} rows (2025-26), {len(FEATS)} features\n")

for target in ["fwd_0930_1515", "fwd_0930_1015"]:
    y_tr = (tr[target] > 0).astype(int)
    clf = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.03, max_depth=4, l2_regularization=1.0, random_state=0).fit(tr[FEATS], y_tr)
    p = clf.predict_proba(te[FEATS])[:, 1]
    conf = np.abs(p - 0.5)
    direction = np.where(p > 0.5, 1, -1)
    realized = direction * te[target].values
    print(f"=== target {target} ===")
    print(f"test accuracy all: {(direction == np.where(te[target] > 0, 1, -1)).mean() * 100:.1f}%   mean realized: {realized.mean():.1f} bps")
    for q in [0.5, 0.8, 0.9, 0.95]:
        m = conf >= np.quantile(conf, q)
        print(f"  top {int((1 - q) * 100):>2}% confidence: n={m.sum():>5} acc={(realized[m] > 0).mean() * 100:>5.1f}% mean={realized[m].mean():>6.1f} bps  (p range {p[m].min():.2f}-{p[m].max():.2f})")
    # realistic budget: 2 most confident per day
    d = pd.DataFrame({"day": te.day.values, "conf": conf, "real": realized}).sort_values(["day", "conf"], ascending=[True, False])
    top2 = d.groupby("day").head(2)
    print(f"  2 most confident per day: n={len(top2)} acc={(top2.real > 0).mean() * 100:.1f}% mean={top2.real.mean():.1f} bps -> {top2.real.mean() * 2 * 21 / 100:.2f}%/month gross on full notional")
    # regression variant: predict magnitude, trade only when |pred| large
    reg = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.03, max_depth=4, l2_regularization=1.0, random_state=0).fit(tr[FEATS], tr[target])
    pr = reg.predict(te[FEATS])
    for thr in [10, 20, 30]:
        m = np.abs(pr) >= thr
        if m.sum():
            r = np.sign(pr[m]) * te[target].values[m]
            print(f"  regression |pred|>={thr}bps: n={m.sum():>5} acc={(r > 0).mean() * 100:>5.1f}% mean={r.mean():>6.1f} bps")
    print()
# sanity: same pipeline on shuffled labels should give ~0
y_shuf = np.random.default_rng(0).permutation((tr["fwd_0930_1515"] > 0).astype(int).values)
clf = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.03, max_depth=4, random_state=0).fit(tr[FEATS], y_shuf)
p = clf.predict_proba(te[FEATS])[:, 1]; conf = np.abs(p - 0.5); m = conf >= np.quantile(conf, 0.9)
r = np.where(p > 0.5, 1, -1) * te["fwd_0930_1515"].values
print(f"control (shuffled labels) top10%: n={m.sum()} mean={r[m].mean():.1f} bps")
print("friction to beat: ~10-15 bps")
