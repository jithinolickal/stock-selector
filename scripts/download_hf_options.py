"""Download Nifty/Sensex 1-min options + index parquet from HF dataset thetrademarkk/india-index-options-1m (CC BY-NC)."""
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data" / "external" / "hf_options"
REPO = "thetrademarkk/india-index-options-1m"
API = f"https://huggingface.co/api/datasets/{REPO}/tree/main/"
RAW = f"https://huggingface.co/datasets/{REPO}/resolve/main/"
SYMS = sys.argv[1:] or ["NIFTY", "SENSEX"]


def listing(path):
    return [x for x in requests.get(API + path, timeout=60).json() if x["type"] == "file"]


def fetch(item, retries=5):
    out = DEST / item["path"]
    if out.exists() and out.stat().st_size == item.get("size", -1):
        return "skip"
    out.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(retries):
        try:
            with requests.get(RAW + item["path"], stream=True, timeout=120) as r:
                r.raise_for_status()
                tmp = out.with_suffix(".part")
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(1 << 20):
                        f.write(chunk)
                tmp.rename(out)
            return "ok"
        except (requests.RequestException, OSError) as e:
            err = e
            time.sleep(2 ** attempt)
    return f"FAILED {err}"


items = [i for s in SYMS for i in listing("index") if i["path"].endswith(f"{s}.parquet")]
for s in SYMS:
    items += listing(f"options/{s}")
print(f"{len(items)} files, {sum(i.get('size', 0) for i in items) / 1e9:.2f} GB", flush=True)
with ThreadPoolExecutor(4) as ex:
    for n, (i, res) in enumerate(zip(items, ex.map(fetch, items)), 1):
        if n % 25 == 0 or res != "skip":
            print(f"[{n}/{len(items)}] {i['path']} {res}", flush=True)
print("done")
