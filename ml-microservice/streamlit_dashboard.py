import streamlit as st
import pandas as pd
import sqlite3
import requests
from datetime import datetime

# Set page config
st.set_page_config(page_title="SmartQueue.AI Dashboard", layout="centered")

st.title("📊 SmartQueue.AI - Prediction Dashboard")

# 🔄 Load logs from SQLite
def load_data():
    conn = sqlite3.connect("queue_log.db")
    df = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC", conn)
    conn.close()
    return df

# 🚀 Load the data initially
df = load_data()

# 🔄 Refresh button
if st.button("🔁 Refresh Logs"):
    df = load_data()
    st.success("Logs refreshed!")

# 📄 Show raw log data
st.subheader("📄 Prediction Logs")
st.dataframe(df)

# 🔎 Filters
st.subheader("🔎 Filter by Hour or Day")
col1, col2 = st.columns(2)

with col1:
    selected_hour = st.selectbox("Hour (Optional)", ["All"] + sorted(df["hour"].unique().tolist()))
with col2:
    selected_day = st.selectbox("Day of Week (Optional)", ["All"] + sorted(df["day_of_week"].unique().tolist()))

# ✅ Apply filters
filtered_df = df.copy()
if selected_hour != "All":
    filtered_df = filtered_df[filtered_df["hour"] == int(selected_hour)]
if selected_day != "All":
    filtered_df = filtered_df[filtered_df["day_of_week"] == int(selected_day)]

# 🕒 Convert timestamp for chart
filtered_df["timestamp"] = pd.to_datetime(filtered_df["timestamp"])

# 📈 Line chart
st.subheader("📈 Predicted Customers by Time")
if not filtered_df.empty:
    chart_df = filtered_df.set_index("timestamp").sort_index()
    st.line_chart(chart_df["predicted_customers"])
else:
    st.warning("No data available for the selected filters.")

# 🔮 Live Prediction Section
st.subheader("🔮 Live Queue Prediction")
with st.form("predict_form"):
    hour = st.number_input("Current Hour (0-23)", min_value=0, max_value=23, value=12)
    day = st.number_input("Day of Week (0=Mon, 6=Sun)", min_value=0, max_value=6, value=2)
    prev = st.number_input("Previous Hour Customers", min_value=0, value=10)
    submitted = st.form_submit_button("Predict")

    if submitted:
        try:
            # 🌐 Call FastAPI endpoint
            response = requests.post("http://127.0.0.1:8000/predict", json={
                "hour": hour,
                "day_of_week": day,
                "prev_customers": prev
            })
            if response.status_code == 200:
                result = response.json()
                st.success(f"✅ Predicted Customers for Next Hour: {result['predicted_customers']}")
            else:
                st.error(f"❌ Server Error: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Could not connect to FastAPI: {e}")
