import sqlite3
import pandas as pd

conn = sqlite3.connect("queue_log.db")

try:
    df = pd.read_sql_query("SELECT * FROM logs ORDER BY id DESC", conn)
    print("✅ Found", len(df), "records in the log.")
    print(df.head())
except Exception as e:
    print("❌ Error reading database:", e)

conn.close()
