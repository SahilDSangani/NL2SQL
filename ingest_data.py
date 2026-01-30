import pandas as pd
import sqlite3

csv_file = "batting.csv" 
df = pd.read_csv(csv_file)

# Connect to (or create) the SQLite database
conn = sqlite3.connect("mlb_batting_stats.db")

# Write the data to a table named 'stats'
df.to_sql("stats", conn, if_exists="replace", index=False)

print("Database created successfully as 'mlb_batting_stats.db'!")
conn.close()