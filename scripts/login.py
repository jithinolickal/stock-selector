"""Daily Upstox login for ORDERS: prints auth URL, you paste the redirect URL back, token saved as
UPSTOX_TRADE_TOKEN in .env. (UPSTOX_ACCESS_TOKEN stays the 1-year Analytics token used for data.)"""
import os
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
from dotenv import load_dotenv, set_key

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"
load_dotenv(ENV)
key, secret = os.getenv("UPSTOX_API_KEY"), os.getenv("UPSTOX_API_SECRET")
redirect = os.getenv("UPSTOX_REDIRECT_URI", "http://127.0.0.1:5000/callback")
if not key or not secret:
    sys.exit("set UPSTOX_API_KEY and UPSTOX_API_SECRET in .env")

print("1. Open and log in:\n")
print(f"https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={key}&redirect_uri={redirect}\n")
pasted = input("2. Paste the redirect URL you landed on: ").strip()
code = parse_qs(urlparse(pasted).query).get("code", [None])[0] or pasted
r = requests.post(
    "https://api.upstox.com/v2/login/authorization/token",
    headers={"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
    data={"code": code, "client_id": key, "client_secret": secret, "redirect_uri": redirect, "grant_type": "authorization_code"},
    timeout=30,
)
r.raise_for_status()
set_key(str(ENV), "UPSTOX_TRADE_TOKEN", r.json()["access_token"])
print("UPSTOX_TRADE_TOKEN saved to .env (valid till 3:30 AM tomorrow)")
