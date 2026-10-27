# stock-selector

Research repo for intraday trading on Indian markets via Upstox. Outcome so far (see `PLAN.md`
and `reports/`): equity intraday and scalping have no edge after costs; the one usable setup is
the **Nifty expiry-day 9:20 short ATM straddle**, implemented in `live/` (read `live/README.md`).

```
backtest/, strategy/   equity research engine (closed, kept for reference)
options/               option backtest engine + data loaders
scripts/               research runs (options_*.py, spike_fade.py, pairs_scan.py, ...), download.py, login.py
live/                  the only order-capable code: paper / sandbox / live straddle runner
tests/                 pytest (19 tests)
reports/, research_notes/   findings; results/ is output (git-ignored)
legacy/                the original stock-selector (swing/scalping screener), untouched
```

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
cp .env.example .env                       # UPSTOX_ACCESS_TOKEN (1-yr Analytics token) at minimum
python scripts/download.py                 # equity 5-min candles (data/parquet/, ignored)
python scripts/download_hf_options.py      # option history (data/external/, ignored, ~1.6 GB)
pytest
python -m live.straddle                    # paper-trade the straddle on an expiry day
```
