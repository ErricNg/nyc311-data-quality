from pathlib import Path
from urllib.parse import urlencode

import pandas as pd

BASE_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"
START = "2026-09-01T00:00:00"
END = "2026-09-07T23:59:59"
LIMIT = 100_000

params = {
    "$where": f"created_date between '{START}' and '{END}'",
    "$order": "created_date",
    "$limit": LIMIT,
}
url = f"{BASE_URL}?{urlencode(params)}"

df = pd.read_csv(url, dtype=str)
print(f"Downloaded {len(df):,} rows, {df.shape[1]} columns")

out_path = Path("data/raw/311_2026-09-01_to_2026-09-07.csv")
df.to_csv(out_path, index=False)
print(f"Saved to {out_path}")