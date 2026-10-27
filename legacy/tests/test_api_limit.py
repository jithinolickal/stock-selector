import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("UPSTOX_ACCESS_TOKEN")

instrument_key = "NSE_EQ|INE002A01018"  # RELIANCE
to_date = datetime.now().strftime("%Y-%m-%d")

# Try different day ranges
for days in [200, 365, 500]:
    from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    url = f"https://api.upstox.com/v3/historical-candle/{instrument_key}/days/1/{to_date}/{from_date}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers, timeout=30)
    data = response.json()
    
    candles = data.get("data", {}).get("candles", [])
    print(f"Requested {days} days ({from_date} to {to_date}): Got {len(candles)} candles")
