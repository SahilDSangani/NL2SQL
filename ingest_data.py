# =============================================================================
# ingest_data.py — Load CSV data into the SQLite database
# =============================================================================
# HOW TO RUN:
#   python3 ingest_data.py
#
# This script reads CSV files and writes them into mlb_batting_stats.db.
# Re-run this whenever you add or update a CSV file.
#
# Required CSV files (place in the same directory as this script):
#   batting.csv   — MLB batting stats (required, already present)
#   pitching.csv  — MLB pitching stats (optional, add when available)
#   fielding.csv  — MLB fielding stats (optional, add when available)
#
# CSV files can be downloaded from Baseball Reference (https://www.baseball-reference.com).
# Export standard batting/pitching/fielding season totals for the years you want.
# Both should include Name, Year, Tm, and mlbID columns.
# =============================================================================

import os
import pandas as pd
import sqlite3

DB_PATH = "mlb_batting_stats.db"
conn = sqlite3.connect(DB_PATH)

# --- Batting (required) ---
if os.path.exists("batting.csv"):
    df = pd.read_csv("batting.csv")
    df.to_sql("stats", conn, if_exists="replace", index=False)
    print(f"batting.csv → 'stats' table ({len(df)} rows)")
else:
    print("WARNING: batting.csv not found — skipping batting table")

# --- Pitching (optional) ---
if os.path.exists("pitching.csv"):
    df = pd.read_csv("pitching.csv")
    df.to_sql("pitching", conn, if_exists="replace", index=False)
    print(f"pitching.csv → 'pitching' table ({len(df)} rows)")
else:
    print("pitching.csv not found — skipping pitching table (add the file to enable pitching queries)")

# --- Fielding (optional) ---
if os.path.exists("fielding.csv"):
    df = pd.read_csv("fielding.csv")
    df.to_sql("fielding", conn, if_exists="replace", index=False)
    print(f"fielding.csv → 'fielding' table ({len(df)} rows)")
else:
    print("fielding.csv not found — skipping fielding table (add the file to enable fielding queries)")

conn.close()
print(f"\nDatabase ready: {DB_PATH}")
