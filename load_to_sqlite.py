import sqlite3
import pandas as pd
from pathlib import Path

FILES = {
    "bajaj_auto":    "Bajaj Auto.csv",
    "eicher_motors": "Eicher Motors.csv",
    "hero_motocorp": "Hero Motocorp.csv",
    "infosys":       "Infosys.csv",
    "tcs":           "TCS.csv",
    "tvs_motors":    "TVS Motors.csv",
}

DATA_DIR = Path(".")
DB_PATH = DATA_DIR / "stocks.db"

if DB_PATH.exists():
    DB_PATH.unlink()  # fresh start

conn = sqlite3.connect(DB_PATH)

COLS = ["date", "open_price", "high_price", "low_price", "close_price",
        "wap", "no_of_shares", "no_of_trades", "total_turnover",
        "deliverable_qty", "pct_deli_qty", "spread_high_low",
        "spread_close_open"]

for table, fname in FILES.items():
    df = pd.read_csv(DATA_DIR / fname)
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%B-%Y").dt.strftime("%Y-%m-%d")
    df.columns = COLS
    df.to_sql(table, conn, if_exists="replace", index=False)
    cur = conn.cursor()
    cur.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table}_date ON {table}(date)")
    conn.commit()
    print(f"{table:15s} -> {len(df)} rows")

print("\nVerification:")
for table in FILES:
    n = pd.read_sql(f"SELECT COUNT(*) AS n FROM {table}", conn).iloc[0, 0]
    d1 = pd.read_sql(f"SELECT MIN(date) AS d FROM {table}", conn).iloc[0, 0]
    d2 = pd.read_sql(f"SELECT MAX(date) AS d FROM {table}", conn).iloc[0, 0]
    print(f"  {table:15s} {n} rows   {d1} -> {d2}")

conn.close()
print(f"\nDone. Database saved to: {DB_PATH}")