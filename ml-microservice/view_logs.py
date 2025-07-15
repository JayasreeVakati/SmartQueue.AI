
import sqlite3
import pandas as pd
import os

print("🚀 Running view_logs.py...")

db_path = "queue_log.db"

# Check if DB exists
if not os.path.exists(db_path):
    print(f"❌ '{db_path}' not found in this folder.")
else:
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC", conn)
        conn.close()

        if df.empty:
            print("⚠️ No prediction logs found.")
        else:
            print(f"✅ Showing {len(df)} prediction log entries:\n")
            print(df.to_string(index=False))
    except Exception as e:
        print(f"❌ Error reading database: {e}")
